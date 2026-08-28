"""Offline safety tests for the issue #832 events routing helper."""

from __future__ import annotations

import importlib.util
import json
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).parents[1] / "apply_issue_832_events_routing.py"
SPEC = importlib.util.spec_from_file_location("apply_issue_832_events_routing", SCRIPT)
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
        mock.patch.object(sys, "argv", ["apply_issue_832_events_routing.py", *args]),
        mock.patch.object(MODULE, "auth_header", return_value="Basic offline-test"),
    ):
        return MODULE.main()


class ApplyIssue832EventsRoutingTests(unittest.TestCase):
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
            if "/pages/2250" in url and body is not None:
                raise AssertionError("page 2250 must never be in a write URL")
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
            if item_id == 2250:
                raise AssertionError("page 2250 is not in the write set")
            live = json.loads(json.dumps(self.lives[item_id]))
            if body is not None:
                if "content" in body:
                    live["content"] = {"raw": body["content"]}
                self.lives[item_id] = live
            return live

        return fake_request

    def test_targets_match_rows_18_through_25(self):
        ids = [row["id"] for row in TARGETS["items"]]
        self.assertEqual(ids, [4495, 9197, 8418, 6815, 6251, 5768, 4348, 12315])
        self.assertNotIn(2250, ids)
        self.assertEqual(TARGETS["must_not_write_ids"], [2250])
        slugs = {row["id"]: row["slug"] for row in TARGETS["items"]}
        self.assertEqual(
            slugs[4495], "inside-the-innaugural-vancouver-ai-community-meetup"
        )
        self.assertEqual(slugs[12315], "vancouver-ai")
        anchors = [
            (row["row"], row["text"], row["href"])
            for spec in TARGETS["items"]
            for row in spec["anchors"]
        ]
        self.assertEqual(
            anchors,
            [
                (
                    18,
                    "we still do this every month, and the next one is on the calendar",
                    "https://kriskrug.co/events/",
                ),
                (19, "the next one", "https://kriskrug.co/events/"),
                (20, "come to the next one", "https://kriskrug.co/events/"),
                (21, "the current calendar", "https://kriskrug.co/events/"),
                (22, "where the next one lands", "https://kriskrug.co/events/"),
                (
                    23,
                    "still monthly, still free, still worth the trip",
                    "https://kriskrug.co/events/",
                ),
                (
                    24,
                    "the live calendar, which is the version that stays current",
                    "https://kriskrug.co/events/",
                ),
                (25, "the calendar", "https://kriskrug.co/events/"),
            ],
        )

    def test_write_set_never_includes_2250(self):
        self.assertNotIn(2250, MODULE.write_ids(TARGETS))
        MODULE.assert_targets_safe(TARGETS)
        with self.assertRaises(SystemExit) as caught:
            MODULE.refuse_write_id(2250, TARGETS)
        self.assertIn("2250", str(caught.exception))
        with self.assertRaises(SystemExit):
            run_main("--item-id", "2250", "--from-files")

    def test_rewrite_recaps_add_one_events_link_and_keep_vancouver_ai(self):
        for item_id in (4495, 9197, 8418, 6815, 6251, 5768, 4348):
            spec = spec_by_id(item_id)
            before = before_body(item_id)
            after = MODULE.rewrite_body(before, spec, TARGETS)
            self.assertIsNotNone(after, msg=item_id)
            self.assertEqual(
                after.count('<a href="https://kriskrug.co/events/">'),
                before.count('<a href="https://kriskrug.co/events/">') + 1,
            )
            self.assertGreaterEqual(
                MODULE.vancouver_ai_count(after), MODULE.vancouver_ai_count(before)
            )
            if spec.get("preserve_footer"):
                self.assertEqual(
                    before.count("kk-collection-footer"),
                    after.count("kk-collection-footer"),
                )
            if after.find("kk-collection-footer") >= 0:
                self.assertLess(
                    after.find(spec["anchors"][0]["text"]),
                    after.find("kk-collection-footer"),
                )
            self.assertNotIn("\u2014", MODULE.inserted_fragment(spec))
            self.assertNotIn("Sept", MODULE.inserted_fragment(spec))
            self.assertIsNone(MODULE.rewrite_body(after, spec, TARGETS))

    def test_rewrite_4348_sits_in_the_intro_ahead_of_the_2023_list(self):
        spec = spec_by_id(4348)
        after = MODULE.rewrite_body(before_body(4348), spec, TARGETS)
        self.assertIsNotNone(after)
        anchor = after.find("the live calendar, which is the version that stays current")
        listed = after.find("lu.ma/ai-trends")
        footer = after.find("kk-collection-footer")
        self.assertGreater(listed, anchor)
        self.assertGreater(footer, listed)

    def test_rewrite_8418_accepts_authenticated_raw_block_shape(self):
        spec = spec_by_id(8418)
        before = f"<p>existing body</p>\n\n{spec['find']}"
        after = MODULE.rewrite_body(before, spec, TARGETS)
        self.assertIsNotNone(after)
        self.assertIn(
            '<a href="https://kriskrug.co/events/">come to the next one</a>',
            after,
        )
        self.assertEqual(
            before.count("kk-collection-footer"),
            after.count("kk-collection-footer"),
        )
        self.assertIsNone(MODULE.rewrite_body(after, spec, TARGETS))

    def test_rewrite_8418_refuses_ambiguous_raw_and_rendered_variants(self):
        spec = spec_by_id(8418)
        alternate = spec["alternate_rewrites"][0]["find"]
        with self.assertRaises(ValueError):
            MODULE.rewrite_body(f"{spec['find']}\n{alternate}", spec, TARGETS)

    def test_rewrite_12315_adds_calendar_and_keeps_browse_ai_events(self):
        spec = spec_by_id(12315)
        before = before_body(12315)
        after = MODULE.rewrite_body(before, spec, TARGETS)
        self.assertIsNotNone(after)
        self.assertIn('href="/ai-events/"', after)
        self.assertIn("Browse AI events", after)
        self.assertIn('<a href="https://kriskrug.co/events/">the calendar</a>', after)
        self.assertEqual(before.count("Browse AI events"), after.count("Browse AI events"))
        self.assertNotIn("2250", after)

    def test_missing_needle_aborts(self):
        spec = spec_by_id(4495)
        with self.assertRaises(ValueError):
            MODULE.rewrite_body("<p>no toast</p>", spec, TARGETS)

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
        for item_id, kind in (
            (4495, "post"),
            (9197, "post"),
            (8418, "post"),
            (6815, "post"),
            (6251, "post"),
            (5768, "post"),
            (4348, "post"),
            (12315, "page"),
        ):
            self.assertTrue((after_dir / f"{kind}-{item_id}-content.raw.html").is_file())
        self.assertFalse((after_dir / "page-2250-content.raw.html").exists())

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
        self.assertTrue(all("2250" not in url for url, _ in calls))

    def test_slug_mismatch_aborts_before_any_write(self):
        self.lives[12315]["slug"] = "wrong-slug"
        calls = []
        snapshot_dir = self.tmp_path / "snapshots"
        with (
            mock.patch.object(MODULE, "SNAPSHOT_DIR", snapshot_dir),
            mock.patch.object(
                MODULE, "request", side_effect=self._patch_request(calls)
            ),
        ):
            with self.assertRaises(SystemExit) as caught:
                run_main("--apply", "--allow-before-826", "--item-id", "12315")
        self.assertIn("slug is", str(caught.exception))
        self.assertTrue(all(body is None for _, body in calls))
        self.assertFalse(snapshot_dir.exists())

    def test_apply_refuses_when_826_is_not_live(self):
        calls = []
        with mock.patch.object(
            MODULE, "request", side_effect=self._patch_request(calls)
        ):
            with self.assertRaises(SystemExit) as caught:
                run_main("--apply", "--item-id", "4495")
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
            self.assertEqual(0, run_main("--apply", "--item-id", "6815"))
        writes = [body for _, body in calls if body is not None]
        self.assertEqual(1, len(writes))
        self.assertEqual(set(writes[0]), {"content"})
        self.assertIn("the current calendar", writes[0]["content"])
        self.assertIn("https://kriskrug.co/vancouver-ai/", writes[0]["content"])
        self.assertTrue(all("2250" not in url for url, _ in calls))
        snapshots = list(snapshot_dir.glob("*.json"))
        self.assertEqual(1, len(snapshots))
        self.assertEqual(stat.S_IMODE(snapshots[0].stat().st_mode), 0o600)

    def test_restore_refuses_page_2250(self):
        snapshot = self.tmp_path / "rest-page-2250-before.json"
        snapshot.write_text(
            json.dumps(
                {
                    "id": 2250,
                    "slug": "events",
                    "type": "page",
                    "content": {"raw": "<p>no</p>"},
                }
            ),
            encoding="utf-8",
        )
        with self.assertRaises(SystemExit) as caught:
            run_main("--restore", str(snapshot))
        self.assertIn("2250", str(caught.exception))

    def test_apply_md_does_not_claim_the_write_already_happened(self):
        apply_md = (MODULE.PACK / "APPLY.md").read_text(encoding="utf-8")
        self.assertIn("Prepared, not applied", apply_md)
        self.assertIn("--apply", apply_md)
        self.assertIn("2250", apply_md)
        self.assertIn("#635", apply_md)
        self.assertNotIn("\u2014", apply_md)
        self.assertNotIn("Fixes #832", apply_md)
        self.assertNotIn("Fixes #402", apply_md)


if __name__ == "__main__":
    unittest.main()
