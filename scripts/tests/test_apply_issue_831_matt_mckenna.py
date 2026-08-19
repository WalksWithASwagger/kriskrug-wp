"""Offline safety tests for the issue #831 Matt McKenna hub helper."""

from __future__ import annotations

import importlib.util
import json
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).parents[1] / "apply_issue_831_matt_mckenna.py"
SPEC = importlib.util.spec_from_file_location("apply_issue_831_matt_mckenna", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

TARGETS = MODULE.load_targets()


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
        mock.patch.object(sys, "argv", ["apply_issue_831_matt_mckenna.py", *args]),
        mock.patch.object(MODULE, "auth_header", return_value="Basic offline-test"),
    ):
        return MODULE.main()


class ApplyIssue831MattMckennaTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.tmp_path = Path(self.tempdir.name)
        self.lives = {row["id"]: fake_item(row) for row in TARGETS["items"]}
        self.gate = {
            row["id"]: {
                "id": row["id"],
                "slug": row["slug"],
                "categories": [row["from_category"]],
            }
            for row in TARGETS["child1_gate"]
        }

    def _patch_request(self, calls, *, gate_ready=False):
        def fake_request(url, _header, body=None):
            calls.append((url, body))
            if "/posts/" in url and "context=edit" not in url:
                post_id = int(url.split("/posts/")[1].split("?")[0])
                live = json.loads(json.dumps(self.gate[post_id]))
                if gate_ready:
                    spec = next(
                        row for row in TARGETS["child1_gate"] if row["id"] == post_id
                    )
                    live["categories"] = [spec["to_category"]]
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

    def test_targets_match_rows_15_through_17(self):
        ids = [row["id"] for row in TARGETS["items"]]
        self.assertEqual(ids, [12319, 2833, 2423])
        self.assertEqual(spec_by_id(12319)["slug"], "ai-conversations")
        self.assertEqual(
            spec_by_id(2833)["slug"],
            "dent-the-future-an-insiders-experiences-at-the-dent-conference",
        )
        self.assertEqual(spec_by_id(2423)["slug"], "dent-2019-photo-recap-gallery")
        self.assertNotIn(3183, ids)
        self.assertNotIn(3330, ids)
        anchors = [
            (row["row"], row["text"], row["href"])
            for spec in TARGETS["items"]
            for row in spec["anchors"]
        ]
        self.assertEqual(
            anchors,
            [
                (
                    15,
                    "Matt McKenna's decade at DENT",
                    "https://kriskrug.co/2023/09/22/coffee-community-and-sobriety-matt-mckennas-decade-at-dent/",
                ),
                (
                    16,
                    "Matt McKenna, who has been at every single one",
                    "https://kriskrug.co/2023/09/22/coffee-community-and-sobriety-matt-mckennas-decade-at-dent/",
                ),
                (
                    17,
                    "I sat down with Matt McKenna a few years after this",
                    "https://kriskrug.co/2023/09/22/coffee-community-and-sobriety-matt-mckennas-decade-at-dent/",
                ),
            ],
        )
        gate_3330 = next(row for row in TARGETS["child1_gate"] if row["id"] == 3330)
        self.assertEqual(gate_3330["from_category"], 1757)
        self.assertEqual(gate_3330["to_category"], 1676)

    def test_rewrite_12319_inserts_card_and_keeps_other_cards(self):
        spec = spec_by_id(12319)
        before = before_body(12319)
        after = MODULE.rewrite_body(before, spec, TARGETS)
        self.assertIsNotNone(after)
        self.assertEqual(before.count("aurora-media-card"), 3)
        self.assertEqual(after.count("aurora-media-card"), 4)
        self.assertIn("Matt McKenna's decade at DENT", after)
        self.assertIn(
            "Ten years of DENT, ten years sober, and a coffee shop in Miami.", after
        )
        self.assertIn("matt-mckennas-decade-at-dent", after)
        for href in TARGETS["preserve_existing_hrefs"]:
            self.assertEqual(before.count(href), after.count(href))
        self.assertLess(
            after.find("matt-mckennas-decade-at-dent"),
            after.find("category/conversations-interviews/"),
        )
        self.assertNotIn("\u2014", MODULE.inserted_fragment(spec))
        self.assertIsNone(MODULE.rewrite_body(after, spec, TARGETS))

    def test_rewrite_2833_wraps_existing_name_inline(self):
        spec = spec_by_id(2833)
        before = before_body(2833)
        after = MODULE.rewrite_body(before, spec, TARGETS)
        self.assertIsNotNone(after)
        community = after[
            after.find("DENT has grown into a support network") : after.find(
                "Jason and Steve"
            )
        ]
        self.assertIn(
            '<a href="https://kriskrug.co/2023/09/22/coffee-community-and-sobriety-matt-mckennas-decade-at-dent/">Matt McKenna, who has been at every single one</a>',
            community,
        )
        self.assertNotIn("instagram.com/real_mckenna", community)
        self.assertIn(
            "Seeing familiar faces like my buddy <a href=\"https://kriskrug.co/2023/09/22/coffee-community-and-sobriety-matt-mckennas-decade-at-dent/\">Matt McKenna, who has been at every single one</a>, and exploring",
            community,
        )
        self.assertEqual(community.count("</p>"), 1)
        self.assertNotIn(
            "I sat down with Matt McKenna a few years after this", after
        )
        self.assertEqual(
            before.count("kk-collection-footer"), after.count("kk-collection-footer")
        )
        self.assertIsNone(MODULE.rewrite_body(after, spec, TARGETS))

    def test_rewrite_2423_inserts_trailing_intro_sentence(self):
        spec = spec_by_id(2423)
        before = before_body(2423)
        after = MODULE.rewrite_body(before, spec, TARGETS)
        self.assertIsNotNone(after)
        intro_end = after.find("who have become friends and collaborators.")
        figure = after.find("<figure")
        footer = after.find("kk-collection-footer")
        self.assertGreater(figure, intro_end)
        self.assertGreater(footer, after.find("I sat down with Matt McKenna"))
        self.assertIn(
            '<a href="https://kriskrug.co/2023/09/22/coffee-community-and-sobriety-matt-mckennas-decade-at-dent/">I sat down with Matt McKenna a few years after this</a>',
            after,
        )
        self.assertEqual(
            before.count("kk-collection-footer"), after.count("kk-collection-footer")
        )
        self.assertIn("Just back from Sante Fe", before)
        self.assertEqual(before.count(spec["find"]), 1)

    def test_stale_block_index_is_ignored_text_match_wins(self):
        spec = spec_by_id(2423)
        before = before_body(2423)
        self.assertIn("Just back from Sante Fe", before)
        self.assertIn(spec["find"], before)
        self.assertEqual(before.count(spec["find"]), 1)

    def test_missing_needle_aborts(self):
        spec = spec_by_id(2833)
        with self.assertRaises(ValueError):
            MODULE.rewrite_body("<p>no Matt here</p>", spec, TARGETS)

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
        self.assertTrue((after_dir / "page-12319-content.raw.html").is_file())
        self.assertTrue((after_dir / "post-2833-content.raw.html").is_file())
        self.assertTrue((after_dir / "post-2423-content.raw.html").is_file())
        self.assertFalse((after_dir / "post-3183-content.raw.html").is_file())
        self.assertFalse((after_dir / "post-3330-content.raw.html").is_file())

    def test_live_dry_run_performs_no_wordpress_writes(self):
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
        self.assertTrue(calls)
        self.assertTrue(all(body is None for _, body in calls))

    def test_slug_mismatch_aborts_before_any_write(self):
        self.lives[12319]["slug"] = "wrong-slug"
        calls = []
        snapshot_dir = self.tmp_path / "snapshots"
        with (
            mock.patch.object(MODULE, "SNAPSHOT_DIR", snapshot_dir),
            mock.patch.object(
                MODULE, "request", side_effect=self._patch_request(calls)
            ),
        ):
            with self.assertRaises(SystemExit) as caught:
                run_main("--apply", "--allow-before-826", "--item-id", "12319")
        self.assertIn("slug is", str(caught.exception))
        self.assertTrue(all(body is None for _, body in calls))
        self.assertFalse(snapshot_dir.exists())

    def test_apply_refuses_when_826_is_not_live(self):
        calls = []
        with mock.patch.object(
            MODULE, "request", side_effect=self._patch_request(calls)
        ):
            with self.assertRaises(SystemExit) as caught:
                run_main("--apply", "--item-id", "2423")
        self.assertIn("#826", str(caught.exception))
        self.assertIn("3330", str(caught.exception))
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
            self.assertEqual(0, run_main("--apply", "--item-id", "2423"))
        writes = [body for _, body in calls if body is not None]
        self.assertEqual(1, len(writes))
        self.assertEqual(set(writes[0]), {"content"})
        self.assertIn(
            "I sat down with Matt McKenna a few years after this",
            writes[0]["content"],
        )
        self.assertIn("kk-collection-footer", writes[0]["content"])
        snapshots = list(snapshot_dir.glob("*.json"))
        self.assertEqual(1, len(snapshots))
        self.assertEqual(stat.S_IMODE(snapshots[0].stat().st_mode), 0o600)

    def test_do_not_touch_item_id_is_refused(self):
        with self.assertRaises(SystemExit) as caught:
            run_main("--from-files", "--item-id", "3183")
        self.assertIn("unknown --item-id", str(caught.exception))

    def test_apply_md_does_not_claim_the_write_already_happened(self):
        apply_md = (MODULE.PACK / "APPLY.md").read_text(encoding="utf-8")
        self.assertIn("Prepared, not applied", apply_md)
        self.assertIn("--apply", apply_md)
        self.assertIn("#826", apply_md)
        self.assertNotIn("\u2014", apply_md)
        self.assertNotIn("Fixes #831", apply_md)
        self.assertNotIn("Fixes #402", apply_md)


if __name__ == "__main__":
    unittest.main()
