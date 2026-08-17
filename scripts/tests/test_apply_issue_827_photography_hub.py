"""Offline safety tests for the issue #827 photography hub helper."""

from __future__ import annotations

import importlib.util
import json
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).parents[1] / "apply_issue_827_photography_hub.py"
SPEC = importlib.util.spec_from_file_location("apply_issue_827_photography_hub", SCRIPT)
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
        mock.patch.object(sys, "argv", ["apply_issue_827_photography_hub.py", *args]),
        mock.patch.object(MODULE, "auth_header", return_value="Basic offline-test"),
    ):
        return MODULE.main()


class ApplyIssue827PhotographyHubTests(unittest.TestCase):
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

    def test_targets_match_rows_11_through_14(self):
        ids = [row["id"] for row in TARGETS["items"]]
        self.assertEqual(ids, [12013, 1222, 1056])
        self.assertEqual(spec_by_id(12013)["slug"], "photography")
        self.assertEqual(
            spec_by_id(1222)["slug"], "to-all-you-wannabe-fashion-photographers"
        )
        self.assertEqual(spec_by_id(1056)["slug"], "kk-on-modelmayhemcom")
        anchors = [
            (row["row"], row["text"], row["href"])
            for spec in TARGETS["items"]
            for row in spec["anchors"]
        ]
        self.assertEqual(
            anchors,
            [
                (
                    11,
                    "the whole archive, twenty years of it",
                    "https://kriskrug.co/category/photography-visual-storytelling/",
                ),
                (
                    12,
                    "the fashion and model years, 2006 to 2008",
                    "https://kriskrug.co/2006/10/23/kk-on-modelmayhemcom/",
                ),
                (
                    13,
                    "how I found those people in the first place",
                    "https://kriskrug.co/2006/10/23/kk-on-modelmayhemcom/",
                ),
                (
                    14,
                    "where all of that ended up",
                    "https://kriskrug.co/photography/",
                ),
            ],
        )

    def test_rewrite_12013_adds_two_links_and_keeps_style_and_flickr(self):
        spec = spec_by_id(12013)
        before = before_body(12013)
        after = MODULE.rewrite_body(before, spec, TARGETS)
        self.assertIsNotNone(after)
        self.assertEqual(before.count("<style>"), 1)
        self.assertEqual(MODULE.style_sha256(before), TARGETS["style_sha256_12013"])
        self.assertEqual(MODULE.style_sha256(after), MODULE.style_sha256(before))
        self.assertEqual(
            before.count(TARGETS["flickr_exit"]), after.count(TARGETS["flickr_exit"])
        )
        self.assertIn(TARGETS["flickr_button"], after)
        self.assertNotIn("checklist-of-model-photographer-negotiation-items", after)
        self.assertEqual(after.count("the whole archive, twenty years of it"), 1)
        self.assertEqual(after.count("the fashion and model years, 2006 to 2008"), 1)
        self.assertNotIn("\u2014", MODULE.inserted_fragment(spec))

    def test_rewrite_1222_inserts_before_footer_and_does_not_duplicate_it(self):
        spec = spec_by_id(1222)
        before = before_body(1222)
        after = MODULE.rewrite_body(before, spec, TARGETS)
        self.assertIsNotNone(after)
        self.assertEqual(
            before.count("kk-collection-footer"), after.count("kk-collection-footer")
        )
        self.assertLess(
            after.find("how I found those people in the first place"),
            after.find("kk-collection-footer"),
        )
        self.assertNotIn("1210", after)
        self.assertIsNone(MODULE.rewrite_body(after, spec, TARGETS))

    def test_rewrite_1056_follows_the_peeps_line(self):
        spec = spec_by_id(1056)
        before = before_body(1056)
        after = MODULE.rewrite_body(before, spec, TARGETS)
        self.assertIsNotNone(after)
        peeps = after.find("I've met a couple cool peeps already.")
        hub = after.find("where all of that ended up")
        footer = after.find("kk-collection-footer")
        self.assertGreater(hub, peeps)
        self.assertGreater(footer, hub)
        self.assertIn('href="https://kriskrug.co/photography/"', after)
        self.assertEqual(
            before.count("kk-collection-footer"), after.count("kk-collection-footer")
        )

    def test_stale_block_index_is_ignored_text_match_wins(self):
        spec = spec_by_id(12013)
        before = before_body(12013)
        self.assertIn("This is a fraction of it", before)
        self.assertIn(spec["find"], before)
        self.assertEqual(before.count(spec["find"]), 1)

    def test_missing_needle_aborts(self):
        spec = spec_by_id(1056)
        with self.assertRaises(ValueError):
            MODULE.rewrite_body("<p>no peeps</p>", spec, TARGETS)

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
        self.assertTrue((after_dir / "page-12013-content.raw.html").is_file())
        self.assertTrue((after_dir / "post-1222-content.raw.html").is_file())
        self.assertTrue((after_dir / "post-1056-content.raw.html").is_file())

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
        self.lives[12013]["slug"] = "wrong-slug"
        calls = []
        snapshot_dir = self.tmp_path / "snapshots"
        with (
            mock.patch.object(MODULE, "SNAPSHOT_DIR", snapshot_dir),
            mock.patch.object(
                MODULE, "request", side_effect=self._patch_request(calls)
            ),
        ):
            with self.assertRaises(SystemExit) as caught:
                run_main("--apply", "--allow-before-826", "--item-id", "12013")
        self.assertIn("slug is", str(caught.exception))
        self.assertTrue(all(body is None for _, body in calls))
        self.assertFalse(snapshot_dir.exists())

    def test_apply_refuses_when_826_is_not_live(self):
        calls = []
        with mock.patch.object(
            MODULE, "request", side_effect=self._patch_request(calls)
        ):
            with self.assertRaises(SystemExit) as caught:
                run_main("--apply", "--item-id", "1056")
        self.assertIn("#826", str(caught.exception))
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
            self.assertEqual(0, run_main("--apply", "--item-id", "1056"))
        writes = [body for _, body in calls if body is not None]
        self.assertEqual(1, len(writes))
        self.assertEqual(set(writes[0]), {"content"})
        self.assertIn("where all of that ended up", writes[0]["content"])
        self.assertIn("kk-collection-footer", writes[0]["content"])
        snapshots = list(snapshot_dir.glob("*.json"))
        self.assertEqual(1, len(snapshots))
        self.assertEqual(stat.S_IMODE(snapshots[0].stat().st_mode), 0o600)

    def test_apply_md_does_not_claim_the_write_already_happened(self):
        apply_md = (MODULE.PACK / "APPLY.md").read_text(encoding="utf-8")
        self.assertIn("Prepared, not applied", apply_md)
        self.assertIn("--apply", apply_md)
        self.assertIn("#480", apply_md)
        self.assertNotIn("\u2014", apply_md)
        self.assertNotIn("Fixes #827", apply_md)


if __name__ == "__main__":
    unittest.main()
