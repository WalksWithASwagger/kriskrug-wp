"""Offline safety tests for the issue #830 Cyber Love Garden hub helper."""

from __future__ import annotations

import importlib.util
import json
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).parents[1] / "apply_issue_830_cyber_love_garden.py"
SPEC = importlib.util.spec_from_file_location(
    "apply_issue_830_cyber_love_garden", SCRIPT
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

TARGETS = MODULE.load_targets()
GARDEN = TARGETS["garden_url"]


def spec_by_id(item_id: int) -> dict:
    return next(row for row in TARGETS["items"] if row["id"] == item_id)


def before_body(item_id: int) -> str:
    spec = spec_by_id(item_id)
    return (
        MODULE.BEFORE_DIR / f"{spec['kind'][:-1]}-{item_id}-content.raw.html"
    ).read_text(encoding="utf-8")


def fake_item(spec: dict, *, raw: str | None = None, slug: str | None = None) -> dict:
    return {
        "id": spec["id"],
        "slug": slug or spec["slug"],
        "type": "page" if spec["kind"] == "pages" else "post",
        "content": {"raw": raw if raw is not None else before_body(spec["id"])},
    }


def run_main(*args: str) -> int:
    with (
        mock.patch.object(sys, "argv", ["apply_issue_830_cyber_love_garden.py", *args]),
        mock.patch.object(MODULE, "auth_header", return_value="Basic offline-test"),
    ):
        return MODULE.main()


class ApplyIssue830CyberLoveGardenTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.tmp_path = Path(self.tempdir.name)
        self.lives = {row["id"]: fake_item(row) for row in TARGETS["items"]}

    def _patch_request(self, calls, *, gate_ready=False):
        def fake_request(url, _header, body=None):
            calls.append((url, body))
            if "/posts/2819" in url:
                live = json.loads(json.dumps(self.lives[2819]))
                if not gate_ready:
                    live["content"] = {
                        "raw": (
                            '<p>If this resonates, '
                            '<a href="http://www.kriskrug.com/contact">'
                            "connect with me</a>.</p>"
                        )
                    }
                elif body is not None and "content" in body:
                    live["content"] = {"raw": body["content"]}
                    self.lives[2819] = live
                return live
            if "/pages/" in url:
                item_id = int(url.split("/pages/")[1].split("?")[0])
            else:
                item_id = int(url.split("/posts/")[1].split("?")[0])
            live = json.loads(json.dumps(self.lives[item_id]))
            if body is not None:
                if "content" in body:
                    live["content"] = {"raw": body["content"]}
                self.lives[item_id] = live
            return live

        return fake_request

    def test_targets_match_rows_26_through_29(self):
        ids = [row["id"] for row in TARGETS["items"]]
        self.assertEqual(ids, [12316, 2819, 2661, 3567])
        self.assertEqual(spec_by_id(12316)["slug"], "ai-for-creatives")
        self.assertEqual(
            spec_by_id(2819)["slug"],
            "exquisite-corpse-collaborative-ai-art-experiment-on-discord-w-midjourney-zoom-out",
        )
        self.assertEqual(
            spec_by_id(2661)["slug"],
            "headed-to-burning-man-shambhala-or-coachella-ignite-your-festival-persona",
        )
        self.assertEqual(
            spec_by_id(3567)["slug"], "community-art-project-development-process-guide"
        )
        self.assertEqual(TARGETS["destination"]["id"], 2650)
        self.assertFalse(TARGETS["destination"]["write_target"])
        self.assertNotIn(2650, ids)
        anchors = [
            (row["row"], row["text"], row["href"])
            for spec in TARGETS["items"]
            for row in spec["anchors"]
        ]
        self.assertEqual(
            anchors,
            [
                (26, "The Cyber Love Garden", GARDEN),
                (27, "the garden where we ran this in person", GARDEN),
                (28, "what we built at Otherworld", GARDEN),
                (29, "a worked example of all of this", GARDEN),
            ],
        )

    def test_rewrite_12316_adds_garden_card_and_keeps_existing_cards(self):
        spec = spec_by_id(12316)
        before = before_body(12316)
        after = MODULE.rewrite_body(before, spec, TARGETS)
        self.assertIsNotNone(after)
        self.assertIn("<h3>The Cyber Love Garden</h3>", after)
        self.assertIn(TARGETS["garden_blurb"], after)
        self.assertIn(GARDEN, after)
        self.assertEqual(
            before.count("https://kriskrug.co/2026/01/24/both-hands-full/"),
            after.count("https://kriskrug.co/2026/01/24/both-hands-full/"),
        )
        self.assertEqual(
            before.count("https://kriskrug.co/2026/05/15/your-taste-is-your-moat/"),
            after.count("https://kriskrug.co/2026/05/15/your-taste-is-your-moat/"),
        )
        self.assertEqual(before.count("<h3>Both Hands Full</h3>"), 1)
        self.assertEqual(after.count("<h3>Both Hands Full</h3>"), 1)
        self.assertEqual(before.count("<h3>Your taste is your moat</h3>"), 1)
        self.assertEqual(after.count("<h3>Your taste is your moat</h3>"), 1)
        self.assertLess(after.find("Your taste is your moat"), after.find("The Cyber Love Garden"))
        self.assertLess(
            after.find("The Cyber Love Garden"), after.find("AI creatives archive")
        )
        self.assertNotIn("\u2014", MODULE.inserted_fragment(spec))
        self.assertIsNone(MODULE.rewrite_body(after, spec, TARGETS))

    def test_rewrite_2819_inserts_garden_sentence_and_leaves_contact_alone(self):
        spec = spec_by_id(2819)
        before = before_body(2819)
        after = MODULE.rewrite_body(before, spec, TARGETS)
        self.assertIsNotNone(after)
        self.assertIn("the garden where we ran this in person", after)
        self.assertIn(GARDEN, after)
        self.assertEqual(
            before.count("https://kriskrug.co/contact/"),
            after.count("https://kriskrug.co/contact/"),
        )
        self.assertEqual(before.count("kriskrug.com/contact"), 0)
        self.assertEqual(after.count("kriskrug.com/contact"), 0)
        self.assertEqual(
            before.count("kk-collection-footer"), after.count("kk-collection-footer")
        )
        garden = after.find("the garden where we ran this in person")
        contact = after.find("https://kriskrug.co/contact/")
        footer = after.find("kk-collection-footer")
        self.assertGreater(contact, garden)
        self.assertGreater(footer, garden)
        self.assertIsNone(MODULE.rewrite_body(after, spec, TARGETS))

    def test_rewrite_2661_inserts_before_footer(self):
        spec = spec_by_id(2661)
        before = before_body(2661)
        after = MODULE.rewrite_body(before, spec, TARGETS)
        self.assertIsNotNone(after)
        self.assertLess(
            after.find("what we built at Otherworld"), after.find("kk-collection-footer")
        )
        self.assertEqual(
            before.count("kk-collection-footer"), after.count("kk-collection-footer")
        )
        self.assertIn(GARDEN, after)

    def test_rewrite_3567_follows_the_intro(self):
        spec = spec_by_id(3567)
        before = before_body(3567)
        after = MODULE.rewrite_body(before, spec, TARGETS)
        self.assertIsNotNone(after)
        intro = after.find("the communal experience can be the message.")
        example = after.find("a worked example of all of this")
        footer = after.find("kk-collection-footer")
        self.assertGreater(example, intro)
        self.assertGreater(footer, example)
        self.assertEqual(
            before.count("kk-collection-footer"), after.count("kk-collection-footer")
        )

    def test_rewrite_3567_accepts_raw_without_em(self):
        spec = spec_by_id(3567)
        raw = (
            "<p>where technology can be a medium and the communal experience "
            "can be the message.</p>\n"
            '<p class="kk-collection-footer">footer</p>'
        )
        after = MODULE.rewrite_body(raw, spec, TARGETS)
        self.assertIsNotNone(after)
        self.assertIn("a worked example of all of this", after)
        self.assertIn(GARDEN, after)

    def test_stale_block_index_is_ignored_text_match_wins(self):
        spec = spec_by_id(2819)
        before = before_body(2819)
        self.assertIn("glimpse into our journey", before)
        self.assertIn(spec["find"], before)
        self.assertEqual(before.count(spec["find"]), 1)

    def test_missing_needle_aborts(self):
        spec = spec_by_id(2661)
        with self.assertRaises(ValueError):
            MODULE.rewrite_body("<p>no dance floor</p>", spec, TARGETS)

    def test_from_files_writes_after_payloads_and_does_not_call_wordpress(self):
        calls = []
        after_dir = self.tmp_path / "after"
        with (
            mock.patch.object(MODULE, "AFTER_DIR", after_dir),
            mock.patch.object(
                MODULE, "request", side_effect=self._patch_request(calls)
            ),
        ):
            self.assertEqual(0, run_main("--from-files"))
        self.assertEqual(calls, [])
        self.assertTrue((after_dir / "page-12316-content.raw.html").is_file())
        self.assertTrue((after_dir / "post-2819-content.raw.html").is_file())
        self.assertTrue((after_dir / "post-2661-content.raw.html").is_file())
        self.assertTrue((after_dir / "post-3567-content.raw.html").is_file())
        self.assertFalse((after_dir / "post-2650-content.raw.html").exists())

    def test_live_dry_run_performs_no_wordpress_writes(self):
        calls = []
        snapshot_dir = self.tmp_path / "snapshots"
        with (
            mock.patch.object(MODULE, "SNAPSHOT_DIR", snapshot_dir),
            mock.patch.object(
                MODULE, "request", side_effect=self._patch_request(calls, gate_ready=True)
            ),
        ):
            self.assertEqual(0, run_main())
        self.assertFalse(snapshot_dir.exists())
        self.assertTrue(calls)
        self.assertTrue(all(body is None for _, body in calls))

    def test_slug_mismatch_aborts_before_any_write(self):
        self.lives[12316]["slug"] = "wrong-slug"
        calls = []
        snapshot_dir = self.tmp_path / "snapshots"
        with (
            mock.patch.object(MODULE, "SNAPSHOT_DIR", snapshot_dir),
            mock.patch.object(
                MODULE, "request", side_effect=self._patch_request(calls)
            ),
        ):
            with self.assertRaises(SystemExit) as caught:
                run_main("--apply", "--allow-before-826", "--item-id", "12316")
        self.assertIn("slug is", str(caught.exception))
        self.assertTrue(all(body is None for _, body in calls))
        self.assertFalse(snapshot_dir.exists())

    def test_apply_refuses_when_826_contact_repair_is_not_live(self):
        calls = []
        with mock.patch.object(
            MODULE, "request", side_effect=self._patch_request(calls)
        ):
            with self.assertRaises(SystemExit) as caught:
                run_main("--apply", "--item-id", "2661")
        self.assertIn("#826", str(caught.exception))
        self.assertIn("2819", str(caught.exception))
        self.assertTrue(all(body is None for _, body in calls))

    def test_apply_snapshots_then_posts_content_only(self):
        calls = []
        snapshot_dir = self.tmp_path / "snapshots"
        with (
            mock.patch.object(MODULE, "SNAPSHOT_DIR", snapshot_dir),
            mock.patch.object(
                MODULE,
                "request",
                side_effect=self._patch_request(calls, gate_ready=True),
            ),
        ):
            self.assertEqual(0, run_main("--apply", "--item-id", "2819"))
        writes = [body for _, body in calls if body is not None]
        self.assertEqual(1, len(writes))
        self.assertEqual(set(writes[0]), {"content"})
        self.assertIn("the garden where we ran this in person", writes[0]["content"])
        self.assertIn("https://kriskrug.co/contact/", writes[0]["content"])
        self.assertNotIn("kriskrug.com/contact", writes[0]["content"])
        self.assertIn("kk-collection-footer", writes[0]["content"])
        snapshots = list(snapshot_dir.glob("*.json"))
        self.assertEqual(1, len(snapshots))
        self.assertEqual(stat.S_IMODE(snapshots[0].stat().st_mode), 0o600)

    def test_apply_md_does_not_claim_the_write_already_happened(self):
        apply_md = (MODULE.PACK / "APPLY.md").read_text(encoding="utf-8")
        self.assertIn("Prepared, not applied", apply_md)
        self.assertIn("--apply", apply_md)
        self.assertIn("#826", apply_md)
        self.assertNotIn("\u2014", apply_md)
        self.assertNotIn("Fixes #830", apply_md)
        self.assertNotIn("Fixes #402", apply_md)


if __name__ == "__main__":
    unittest.main()
