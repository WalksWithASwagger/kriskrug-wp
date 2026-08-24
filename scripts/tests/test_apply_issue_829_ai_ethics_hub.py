"""Offline safety tests for the issue #829 AI ethics hub helper."""

from __future__ import annotations

import importlib.util
import json
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).parents[1] / "apply_issue_829_ai_ethics_hub.py"
SPEC = importlib.util.spec_from_file_location("apply_issue_829_ai_ethics_hub", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

TARGETS = MODULE.load_targets()


def spec_by_id(item_id: int) -> dict:
    return next(row for row in TARGETS["items"] if row["id"] == item_id)


def before_body(item_id: int) -> str:
    spec = spec_by_id(item_id)
    stem = f"{spec['kind'][:-1]}-{item_id}"
    raw = MODULE.BEFORE_DIR / f"{stem}-content.raw.html"
    rendered = MODULE.BEFORE_DIR / f"{stem}-content.rendered.html"
    if raw.is_file():
        return raw.read_text(encoding="utf-8")
    return rendered.read_text(encoding="utf-8")


def fake_item(spec: dict, *, raw: str | None = None, slug: str | None = None) -> dict:
    return {
        "id": spec["id"],
        "slug": slug or spec["slug"],
        "type": "page" if spec["kind"] == "pages" else "post",
        "content": {"raw": raw if raw is not None else before_body(spec["id"])},
    }


def run_main(*args: str) -> int:
    with (
        mock.patch.object(sys, "argv", ["apply_issue_829_ai_ethics_hub.py", *args]),
        mock.patch.object(MODULE, "auth_header", return_value="Basic offline-test"),
    ):
        return MODULE.main()


class ApplyIssue829AiEthicsHubTests(unittest.TestCase):
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

    def test_targets_match_rows_7_through_10(self):
        ids = [row["id"] for row in TARGETS["items"]]
        self.assertEqual(ids, [12318, 12030, 6144, 11882])
        self.assertEqual(spec_by_id(12318)["slug"], "ai-ethics")
        self.assertEqual(
            spec_by_id(12030)["slug"],
            "canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one",
        )
        self.assertEqual(
            spec_by_id(6144)["slug"],
            "ai-is-not-your-friend-why-we-need-to-rethink-our-relationship-with-artificial-intelligence",
        )
        self.assertEqual(spec_by_id(11882)["slug"], "we-trained-ai-on-stolen-work")
        anchors = [
            (row["row"], row["text"], row["href"])
            for spec in TARGETS["items"]
            for row in spec["anchors"]
        ]
        self.assertEqual(
            anchors,
            [
                (
                    7,
                    "You Can't Drink Data",
                    "https://kriskrug.co/2026/05/23/you-cant-drink-data/",
                ),
                (
                    8,
                    "what the water math looks like from street level",
                    "https://kriskrug.co/2026/05/23/you-cant-drink-data/",
                ),
                (
                    9,
                    "two years later I went to the protest and wrote down what the signs said",
                    "https://kriskrug.co/2026/05/23/you-cant-drink-data/",
                ),
                (
                    10,
                    "the march where the illustrators showed up as a guild",
                    "https://kriskrug.co/2026/05/23/you-cant-drink-data/",
                ),
            ],
        )
        self.assertNotIn(11936, ids)
        self.assertNotIn(11929, ids)

    def test_rewrite_12318_inserts_first_card_and_keeps_existing_cards(self):
        spec = spec_by_id(12318)
        before = before_body(12318)
        after = MODULE.rewrite_body(before, spec, TARGETS)
        self.assertIsNotNone(after)
        self.assertIn("You Can't Drink Data", after)
        self.assertIn(TARGETS["card_blurb"], after)
        self.assertLess(after.find("You Can't Drink Data"), after.find("Punk Rock AI"))
        self.assertIn("Responsible AI Professional", after)
        self.assertIn("AI ethics archive", after)
        for href in TARGETS["existing_source_trail_hrefs"]:
            self.assertEqual(before.count(href), after.count(href))
        self.assertEqual(after.count("you-cant-drink-data"), 1)
        self.assertEqual(after.count("aurora-media-card"), 4)
        self.assertNotIn("\u2014", MODULE.inserted_fragment(spec))
        self.assertIsNone(MODULE.rewrite_body(after, spec, TARGETS))

    def test_rewrite_12030_uses_first_compute_paragraph_and_skips_closing(self):
        spec = spec_by_id(12030)
        before = before_body(12030)
        after = MODULE.rewrite_body(before, spec, TARGETS)
        self.assertIsNotNone(after)
        self.assertIn("what the water math looks like from street level", after)
        water = after.find("what the water math looks like from street level")
        closing = after.find("just a faster leak")
        self.assertGreater(closing, water)
        self.assertEqual(
            before.count("just a faster leak"), after.count("just a faster leak")
        )
        self.assertEqual(before.count("/about/"), after.count("/about/"))
        self.assertNotIn("/about/", after)
        self.assertIn("We lack consent architecture.", after)
        self.assertIsNone(MODULE.rewrite_body(after, spec, TARGETS))

    def test_rewrite_6144_inserts_before_footer_and_does_not_duplicate_it(self):
        spec = spec_by_id(6144)
        before = before_body(6144)
        after = MODULE.rewrite_body(before, spec, TARGETS)
        self.assertIsNotNone(after)
        self.assertEqual(
            before.count("kk-collection-footer"), after.count("kk-collection-footer")
        )
        self.assertLess(
            after.find("two years later I went to the protest and wrote down what the signs said"),
            after.find("kk-collection-footer"),
        )
        self.assertIn("Peace out! ???", after)
        self.assertIsNone(MODULE.rewrite_body(after, spec, TARGETS))

    def test_rewrite_11882_adds_guild_anchor_and_keeps_older_11936_links(self):
        spec = spec_by_id(11882)
        before = before_body(11882)
        self.assertEqual(before.count("you-cant-drink-data"), 2)
        self.assertNotIn("the march where the illustrators showed up as a guild", before)
        after = MODULE.rewrite_body(before, spec, TARGETS)
        self.assertIsNotNone(after)
        self.assertEqual(after.count("you-cant-drink-data"), 3)
        self.assertIn("environmental cost</a>", after)
        self.assertIn("notes from my first AI protest", after)
        self.assertIn(
            'href="https://kriskrug.co/2026/05/23/you-cant-drink-data/">the march where the illustrators showed up as a guild</a>',
            after,
        )
        self.assertIn("training material without consent.", after)

    def test_stale_block_index_is_ignored_text_match_wins(self):
        spec = spec_by_id(12318)
        before = before_body(12318)
        self.assertIn("Source trail", before)
        self.assertIn(spec["find"], before)
        self.assertEqual(before.count(spec["find"]), 1)
        self.assertIn("We lack consent architecture.</p>", before_body(12030))
        self.assertEqual(
            before_body(12030).count("We lack consent architecture.</p>"), 1
        )

    def test_missing_needle_aborts(self):
        spec = spec_by_id(12030)
        with self.assertRaises(ValueError):
            MODULE.rewrite_body("<p>no compute paragraph</p>", spec, TARGETS)

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
        self.assertTrue((after_dir / "page-12318-content.raw.html").is_file())
        self.assertTrue((after_dir / "post-12030-content.raw.html").is_file())
        self.assertTrue((after_dir / "post-6144-content.raw.html").is_file())
        self.assertTrue((after_dir / "post-11882-content.raw.html").is_file())

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
        self.lives[12318]["slug"] = "wrong-slug"
        calls = []
        snapshot_dir = self.tmp_path / "snapshots"
        with (
            mock.patch.object(MODULE, "SNAPSHOT_DIR", snapshot_dir),
            mock.patch.object(
                MODULE, "request", side_effect=self._patch_request(calls)
            ),
        ):
            with self.assertRaises(SystemExit) as caught:
                run_main("--apply", "--allow-before-826", "--item-id", "12318")
        self.assertIn("slug is", str(caught.exception))
        self.assertTrue(all(body is None for _, body in calls))
        self.assertFalse(snapshot_dir.exists())

    def test_apply_refuses_when_826_is_not_live(self):
        calls = []
        with mock.patch.object(
            MODULE, "request", side_effect=self._patch_request(calls)
        ):
            with self.assertRaises(SystemExit) as caught:
                run_main("--apply", "--item-id", "12318")
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
            self.assertEqual(0, run_main("--apply", "--item-id", "12030"))
        writes = [body for _, body in calls if body is not None]
        self.assertEqual(1, len(writes))
        self.assertEqual(set(writes[0]), {"content"})
        self.assertIn(
            "what the water math looks like from street level", writes[0]["content"]
        )
        self.assertIn("just a faster leak", writes[0]["content"])
        self.assertNotIn("/about/", writes[0]["content"])
        snapshots = list(snapshot_dir.glob("*.json"))
        self.assertEqual(1, len(snapshots))
        self.assertEqual(stat.S_IMODE(snapshots[0].stat().st_mode), 0o600)

    def test_apply_md_does_not_claim_the_write_already_happened(self):
        apply_md = (MODULE.PACK / "APPLY.md").read_text(encoding="utf-8")
        self.assertIn("Prepared, not applied", apply_md)
        self.assertIn("--apply", apply_md)
        self.assertIn("#826", apply_md)
        self.assertIn("ai-ethics", apply_md)
        self.assertIn("just a faster leak", apply_md)
        self.assertNotIn("\u2014", apply_md)
        self.assertNotIn("Fixes #829", apply_md)
        self.assertNotIn("Fixes #402", apply_md)


if __name__ == "__main__":
    unittest.main()
