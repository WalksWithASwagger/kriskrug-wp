"""#1099: enrichment must not create confirmation or lose documentation/media."""

import copy
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "events_page"))
import catalog_contract as contract  # noqa: E402
import lib  # noqa: E402
import render_events_page as render  # noqa: E402


def event(**updates):
    row = {
        "id": "event",
        "date": "2026-10-28",
        "status": "confirmed",
        "url": "https://example.com/register",
        "image": {
            "media_id": 42,
            "url": "https://kriskrug.co/wp-content/uploads/frame.jpg",
            "photographer": "Credit",
        },
    }
    row.update(updates)
    return row


class CatalogContractTests(unittest.TestCase):
    def test_only_explicit_public_statuses_are_public(self):
        for value in (
            None,
            "",
            "unconfirmed",
            "unknown",
            "CONFIRMED?",
            1,
            *contract.PRIVATE_STATUSES,
        ):
            with self.subTest(value=value):
                self.assertFalse(render.public_status({"status": value}))
        for value in ("confirmed", "scaffold", " CONFIRMED "):
            self.assertTrue(render.public_status({"status": value}))

    def test_missing_status_cannot_arrive_public_from_any_source(self):
        row = event()
        row.pop("status")
        self.assertEqual(lib._norm_event(row)["status"], "unconfirmed")
        fragment = lib.merge_fragments([], [("new.yaml", [row])])[0]
        harvest = lib.merge_meetup_editions(
            [],
            {
                "editions": [
                    {
                        "edition": 1,
                        "date": "2024-01-31",
                        "date_confidence": "documented",
                    }
                ]
            },
        )[0]
        self.assertFalse(render.public_status(fragment))
        self.assertFalse(render.public_status(harvest))

    def test_enrichment_cannot_promote_private_status(self):
        for status in contract.PRIVATE_STATUSES | {"typo", ""}:
            for public in contract.PUBLIC_STATUSES:
                base = event(status=status)
                overlay = event(status=public, date="2026-10-29")
                for merged in (
                    lib.merge_fragments([base], [("patch.yaml", [overlay])])[0],
                    lib.merge_meetup_editions([base], {"events": [overlay]})[0],
                ):
                    self.assertFalse(render.public_status(merged))
                    self.assertEqual(merged["date"], "2026-10-29")

    def test_overlay_without_status_preserves_explicit_confirmation(self):
        for status in contract.PUBLIC_STATUSES:
            base = event(status=status)
            merged = lib.merge_meetup_editions(
                [base],
                {
                    "events": [
                        {"id": "event", "kind": "one-off", "image": {"alt": "New alt"}}
                    ]
                },
            )[0]
            self.assertEqual(merged["status"], status)
            self.assertEqual(merged["image"]["media_id"], 42)
            self.assertEqual(merged["image"]["photographer"], "Credit")

    def test_restrictive_overlay_hides_an_existing_public_record(self):
        merged = lib.merge_fragments(
            [event()], [("patch.yaml", [event(status="unconfirmed")])]
        )[0]
        self.assertFalse(render.public_status(merged))

    def test_harvest_does_not_invent_end_time(self):
        row = lib._edition_to_event({"edition": 1, "date": "2026-11-05"})
        self.assertIsNone(row["end"])

    def test_duplicate_base_harvest_and_edition_identities_fail(self):
        with self.assertRaises(SystemExit):
            contract.index_events([event(), event()], "catalog")
        with self.assertRaises(SystemExit):
            lib.merge_meetup_editions(
                [], {"editions": [{"edition": 1}, {"edition": 1}]}
            )
        with self.assertRaises(ValueError):
            contract.validate_editions([event(edition=1), event(id="other", edition=1)])

    def test_invalid_editions_fail(self):
        for value in (0, -1, True, "33", 3.5):
            with self.subTest(value=value), self.assertRaises(ValueError):
                contract.validate_editions([event(edition=value)])

    def test_optional_docs_legacy_recap_and_source_url_are_preserved(self):
        recap = "https://kriskrug.co/2026/09/29/recap/"
        row = event(
            recap_url=recap,
            docs={
                "recap": [recap, "https://bc-ai.ca/recap/"],
                "photos": "https://example.com/photos",
                "video": ["https://youtu.be/pwrjlS7yh5E"],
            },
        )
        before = copy.deepcopy(row)
        normalized = contract.normalize_contract(row)
        self.assertEqual(row, before)
        self.assertEqual(normalized["url"], before["url"])
        self.assertEqual(normalized["recap_url"], recap)
        self.assertEqual(
            normalized["docs"]["recap"], [recap, "https://bc-ai.ca/recap/"]
        )
        self.assertEqual(normalized["docs"]["photos"], ["https://example.com/photos"])
        self.assertEqual(normalized["image"], before["image"])
        self.assertEqual(
            contract.normalize_contract(event())["docs"],
            {"recap": [], "photos": [], "video": []},
        )

    def test_unsafe_or_local_documentation_links_fail_closed(self):
        for link in (
            "javascript:alert(1)",
            "data:text/plain,test",
            "file:///tmp/photo.jpg",
            "/relative",
            "http://example.com/a",
            "https://localhost/a",
            "https://127.0.0.1/a",
            "https://user:secret@example.com/a",
            "https://example.com:8080/a",
            "https://example.com/\npath",
            'https://example.com/a" onclick="x',
            "https://example.com\\@evil.test/a",
        ):
            with self.subTest(link=link), self.assertRaises(ValueError):
                contract.normalize_docs(event(docs={"video": link}))
        with self.assertRaises(ValueError):
            contract.normalize_docs(
                event(recap_url="https://kriskrug.co.example.com/recap")
            )
        with self.assertRaises(ValueError):
            contract.normalize_docs(event(docs={"other": "https://example.com"}))

    def test_docs_merge_by_slot_without_losing_source_media_or_credit(self):
        base = event(
            docs={
                "recap": "https://kriskrug.co/recap/",
                "photos": "https://example.com/photos",
            }
        )
        merged = contract.merge_event(
            base,
            {
                "docs": {"video": "https://youtu.be/example", "photos": None},
                "image": {"alt": "Alt"},
            },
        )
        self.assertEqual(merged["docs"]["recap"], base["docs"]["recap"])
        self.assertEqual(merged["docs"]["photos"], base["docs"]["photos"])
        self.assertEqual(merged["image"]["photographer"], "Credit")
        self.assertEqual(merged["url"], base["url"])

    def test_dates_are_validated_without_filling_missing_time(self):
        for updates in (
            {"date": "2026-02-30"},
            {"end": "not-a-date"},
            {"end": "2026-10-28T21:00:00"},
            {"end": "2026-10-27"},
            {"date": None},
        ):
            with self.subTest(updates=updates), self.assertRaises(ValueError):
                contract.normalize_contract(event(**updates))
        self.assertNotIn("end", contract.normalize_contract(event()))
        contract.normalize_contract(event(end="2026-10-30T23:00:00-07:00"))
        contract.normalize_contract(
            event(date=None, status="scaffold", bucket_hint="past")
        )

    def test_complete_base_harvest_fragment_precedence_and_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            catalog = root / "catalog.yaml"
            harvest = root / "harvest.yaml"
            fragments = root / "fragments"
            fragments.mkdir()
            catalog.write_text(
                yaml.safe_dump({"events": [event(status="unconfirmed")]})
            )
            harvest.write_text(
                yaml.safe_dump(
                    {"events": [event(date="2026-10-29", status="confirmed")]}
                )
            )
            (fragments / "one.yaml").write_text(
                yaml.safe_dump(
                    {
                        "events": [
                            {
                                "id": "event",
                                "date": "2026-10-30",
                                "docs": {"video": "https://youtu.be/example"},
                            }
                        ]
                    }
                )
            )
            with patch.object(lib, "MEETUP_EDITIONS_PATH", harvest):
                row = lib.load_catalog(catalog, fragments)["events"][0]
            self.assertEqual(row["date"], "2026-10-30")
            self.assertEqual(row["status"], "unconfirmed")
            self.assertEqual(row["image"]["media_id"], 42)
            self.assertEqual(row["docs"]["video"], ["https://youtu.be/example"])

    def test_existing_1108_records_and_legacy_recap_survive(self):
        rows = {row["id"]: row for row in lib.load_catalog()["events"]}
        for ident in (
            "vancouver-ai-meetup-2026-08-26",
            "vancouver-ai-meetup-2026-09-30",
            "2026-11-05-prompt-victoria",
            "trecsa-world-tourism-day-2026",
        ):
            self.assertEqual(rows[ident]["status"], "confirmed")
        self.assertEqual(rows["vancouver-ai-meetup-2026-08-26"]["edition"], 32)
        self.assertEqual(rows["vancouver-ai-meetup-2026-09-30"]["edition"], 33)
        self.assertEqual(
            rows["trecsa-world-tourism-day-2026"]["docs"]["recap"],
            [rows["trecsa-world-tourism-day-2026"]["recap_url"]],
        )
        self.assertEqual(rows["van-ai-meetup-27"]["status"], "scaffold")


if __name__ == "__main__":
    unittest.main()
