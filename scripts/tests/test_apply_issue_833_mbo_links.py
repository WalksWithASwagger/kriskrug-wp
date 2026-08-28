"""Offline safety tests for the issue #833 MBO link package."""

from __future__ import annotations

import importlib.util
import json
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).parents[1] / "apply_issue_833_mbo_links.py"
SPEC = importlib.util.spec_from_file_location("apply_issue_833_mbo_links", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

TARGETS = MODULE.load_targets()


def spec_by_id(item_id: int) -> dict:
    return next(row for row in TARGETS["items"] if row["id"] == item_id)


def fake_item(spec: dict, *, raw: str | None = None, slug: str | None = None) -> dict:
    item = {
        "id": spec["id"],
        "slug": slug or spec["slug"],
        "status": spec["status"],
        "date": spec["date"],
        "title": {"raw": spec["title"]},
        "type": "page" if spec["kind"] == "pages" else "post",
        "content": {"raw": raw if raw is not None else MODULE.fixture_body(spec)},
    }
    if "categories" in spec:
        item["categories"] = list(spec["categories"])
    return item


def run_main(*args: str) -> int:
    with (
        mock.patch.object(sys, "argv", ["apply_issue_833_mbo_links.py", *args]),
        mock.patch.object(MODULE, "auth_header", return_value="Basic offline-test"),
    ):
        return MODULE.main()


class ApplyIssue833MboLinksTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.tmp_path = Path(self.tempdir.name)
        self.lives = {row["id"]: fake_item(row) for row in TARGETS["items"]}
        self.dependency = {
            "id": 3814,
            "slug": spec_by_id(3814)["slug"],
            "status": "publish",
            "categories": [1678],
        }

    def _patch_request(self, calls):
        def fake_request(url, _header, payload=None):
            calls.append((url, payload))
            if "_fields=id,slug,status,categories" in url:
                return json.loads(json.dumps(self.dependency))
            kind = "pages" if "/pages/" in url else "posts"
            item_id = int(url.split(f"/{kind}/")[1].split("?")[0])
            live = json.loads(json.dumps(self.lives[item_id]))
            if payload is not None:
                live["content"] = {"raw": payload["content"]}
                self.lives[item_id] = live
            return live

        return fake_request

    def test_targets_cover_rows_one_through_six_and_exact_identities(self):
        self.assertEqual(
            [row["id"] for row in TARGETS["items"]],
            [3948, 11936, 11358, 11700, 3814],
        )
        self.assertEqual(spec_by_id(3948)["slug"], "the-kk-worldview")
        self.assertEqual(spec_by_id(11936)["slug"], "you-cant-drink-data")
        self.assertEqual(spec_by_id(11358)["slug"], "spa-at-the-end-of-time")
        self.assertEqual(spec_by_id(11700)["slug"], "punk-rock-ai")
        self.assertEqual(
            spec_by_id(3814)["slug"],
            "the-power-of-most-benevolent-outcomes-a-prayer-for-blessings-for-all-living-things",
        )
        self.assertTrue(all(row["status"] == "publish" for row in TARGETS["items"]))
        anchors = [
            (operation["row"], operation["text"], operation["href"])
            for spec in TARGETS["items"]
            for operation in spec["operations"]
        ]
        self.assertEqual([row for row, _, _ in anchors], [1, 2, 3, 4, 5, 6])
        self.assertEqual(
            [text for _, text, _ in anchors],
            [
                "there is a prayer I actually say about this",
                "I say a prayer about this most mornings, which is either funny or the whole point",
                "I have my own version of the seance",
                "the optimistic version of the same argument",
                "the rest of my lens, written out plainly",
                "the less mystical version of this, which is how I actually practice it",
            ],
        )

    def test_each_fixture_rewrites_exactly_once_and_is_idempotent(self):
        for spec in TARGETS["items"]:
            with self.subTest(item_id=spec["id"]):
                before = MODULE.fixture_body(spec)
                after = MODULE.rewrite_body(before, spec)
                self.assertIsNotNone(after)
                for operation in spec["operations"]:
                    self.assertEqual(after.count(MODULE.anchor_html(operation)), 1)
                    self.assertNotIn("\u2014", MODULE.inserted_fragment(operation))
                    self.assertNotIn("\u2013", MODULE.inserted_fragment(operation))
                self.assertIsNone(MODULE.rewrite_body(after, spec))

    def test_worldview_paragraph_lands_after_truth_list(self):
        spec = spec_by_id(3948)
        after = MODULE.rewrite_body(MODULE.fixture_body(spec), spec)
        self.assertLess(
            after.find("<!-- /wp:list -->"), after.find(spec["operations"][0]["text"])
        )
        self.assertLess(
            after.find(spec["operations"][0]["text"]),
            after.find("This is but one lens"),
        )

    def test_punk_rock_insert_is_final_paragraph_and_preserves_glossary_surface(self):
        spec = spec_by_id(11700)
        before = MODULE.fixture_body(spec)
        after = MODULE.rewrite_body(before, spec)
        anchor_at = after.find("the optimistic version of the same argument")
        footer_at = after.find(MODULE.FOOTER_OPEN)
        self.assertLess(anchor_at, footer_at)
        self.assertEqual(before.count("/glossary/"), after.count("/glossary/"))
        self.assertIn("Room for one more.</p>", after)

    def test_3814_partial_state_adds_only_missing_row(self):
        spec = spec_by_id(3814)
        before = MODULE.fixture_body(spec)
        row5 = spec["operations"][0]
        partial = before.replace(row5["find"], row5["replace"], 1)
        after = MODULE.rewrite_body(partial, spec)
        self.assertIsNotNone(after)
        self.assertEqual(after.count(MODULE.anchor_html(row5)), 1)
        self.assertEqual(after.count(MODULE.anchor_html(spec["operations"][1])), 1)

    def test_3814_ai_ethics_link_stays_before_how_to_heading(self):
        spec = spec_by_id(3814)
        after = MODULE.rewrite_body(MODULE.fixture_body(spec), spec)
        self.assertLess(
            after.find("the less mystical version of this"),
            after.find("How To Practice MBOs"),
        )

    def test_missing_or_duplicate_needle_aborts(self):
        spec = spec_by_id(11358)
        with self.assertRaises(ValueError):
            MODULE.rewrite_body("<p>wrong body</p>", spec)
        duplicate = MODULE.fixture_body(spec) + spec["operations"][0]["find"]
        with self.assertRaises(ValueError):
            MODULE.rewrite_body(duplicate, spec)

    def test_from_spec_validates_without_network(self):
        calls = []
        with mock.patch.object(
            MODULE, "request", side_effect=self._patch_request(calls)
        ):
            self.assertEqual(0, run_main("--from-spec"))
        self.assertEqual(calls, [])

    def test_live_dry_run_uses_gets_only_and_creates_no_snapshot(self):
        calls = []
        snapshot_dir = self.tmp_path / "snapshots"
        with (
            mock.patch.object(MODULE, "SNAPSHOT_DIR", snapshot_dir),
            mock.patch.object(
                MODULE, "request", side_effect=self._patch_request(calls)
            ),
        ):
            self.assertEqual(0, run_main())
        self.assertFalse(snapshot_dir.exists())
        self.assertEqual(len(calls), 6)
        self.assertTrue(all(payload is None for _, payload in calls))

    def test_apply_refuses_when_826_category_gate_is_not_live(self):
        self.dependency["categories"] = [1757]
        calls = []
        with mock.patch.object(
            MODULE, "request", side_effect=self._patch_request(calls)
        ):
            with self.assertRaises(SystemExit) as caught:
                run_main("--apply", "--item-id", "3948")
        self.assertIn("#826", str(caught.exception))
        self.assertTrue(all(payload is None for _, payload in calls))

    def test_slug_and_status_mismatches_abort_before_write(self):
        for field, value, expected in (
            ("slug", "wrong-slug", "slug is"),
            ("status", "draft", "status is"),
        ):
            with self.subTest(field=field):
                self.lives[11936] = fake_item(spec_by_id(11936))
                self.lives[11936][field] = value
                calls = []
                with mock.patch.object(
                    MODULE, "request", side_effect=self._patch_request(calls)
                ):
                    with self.assertRaises(SystemExit) as caught:
                        run_main("--item-id", "11936")
                self.assertIn(expected, str(caught.exception))
                self.assertTrue(all(payload is None for _, payload in calls))

    def test_single_item_apply_snapshots_writes_content_only_and_reads_back(self):
        calls = []
        snapshot_dir = self.tmp_path / "snapshots"
        with (
            mock.patch.object(MODULE, "SNAPSHOT_DIR", snapshot_dir),
            mock.patch.object(
                MODULE, "request", side_effect=self._patch_request(calls)
            ),
        ):
            self.assertEqual(0, run_main("--apply", "--item-id", "3948"))
        writes = [payload for _, payload in calls if payload is not None]
        self.assertEqual(1, len(writes))
        self.assertEqual(set(writes[0]), {"content"})
        self.assertIn(
            "there is a prayer I actually say about this", writes[0]["content"]
        )
        snapshots = list(snapshot_dir.glob("*.json"))
        self.assertEqual(1, len(snapshots))
        self.assertEqual(stat.S_IMODE(snapshots[0].stat().st_mode), 0o600)

    def test_runbook_keeps_live_write_and_834_as_separate_gates(self):
        runbook = (MODULE.PACK / "APPLY.md").read_text(encoding="utf-8")
        self.assertIn("fresh explicit live approval", runbook)
        self.assertIn("No live write has been made", runbook)
        self.assertIn("#834", runbook)
        self.assertIn("--restore", runbook)
        self.assertNotIn("Fixes #833", runbook)


if __name__ == "__main__":
    unittest.main()
