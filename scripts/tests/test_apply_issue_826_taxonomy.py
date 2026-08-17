"""Offline safety tests for the issue #826 taxonomy apply helper."""

from __future__ import annotations

import importlib.util
import json
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).parents[1] / "apply_issue_826_taxonomy.py"
SPEC = importlib.util.spec_from_file_location("apply_issue_826_taxonomy", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

TARGETS = MODULE.load_targets()


def spec_by_id(post_id: int) -> dict:
    return next(row for row in TARGETS["posts"] if row["id"] == post_id)


def fake_post(spec: dict, *, categories=None, raw: str | None = None) -> dict:
    if spec.get("href_repair"):
        body = raw or (
            '<p>If this resonates, <a href="http://www.kriskrug.com/contact">'
            "connect with me</a>.</p>"
        )
        cats = categories if categories is not None else [1680]
    else:
        from_id = TARGETS["term_ids"][spec["from_category"]]
        cats = categories if categories is not None else [from_id]
        if raw is not None:
            body = raw
        elif spec.get("old_pillar_href"):
            body = (
                '<!-- wp:paragraph {"className":"kk-collection-footer"} -->\n'
                f'<p class="kk-collection-footer">Part of the '
                f'<a href="{spec["old_pillar_href"]}">{spec["old_pillar_label"]}</a> '
                "collection. See also: "
                '<a href="https://kriskrug.co/example/">Sibling</a>.</p>\n'
                "<!-- /wp:paragraph -->"
            )
        else:
            body = "<p>No collection footer on this post.</p>"
    return {
        "id": spec["id"],
        "slug": spec["slug"],
        "categories": cats,
        "content": {"raw": body},
    }


def run_main(*args: str) -> int:
    with (
        mock.patch.object(sys, "argv", ["apply_issue_826_taxonomy.py", *args]),
        mock.patch.object(MODULE, "auth_header", return_value="Basic offline-test"),
    ):
        return MODULE.main()


class ApplyIssue826TaxonomyTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.tmp_path = Path(self.tempdir.name)
        self.lives = {row["id"]: fake_post(row) for row in TARGETS["posts"]}

    def _patch_request(self, calls):
        def fake_request(url, _header, body=None):
            post_id = int(url.split("/posts/")[1].split("?")[0])
            calls.append((url, body))
            live = json.loads(json.dumps(self.lives[post_id]))
            if body is not None:
                if "categories" in body:
                    live["categories"] = body["categories"]
                if "content" in body:
                    live["content"] = {"raw": body["content"]}
                self.lives[post_id] = live
            return live

        return fake_request

    def test_targets_match_the_live_reconfirm_table(self):
        ids = [row["id"] for row in TARGETS["posts"]]
        self.assertEqual(ids, [3814, 3330, 1067, 1063, 1147, 2819])
        self.assertEqual(TARGETS["term_ids"]["web-early-blog"], 1757)
        self.assertEqual(TARGETS["term_ids"]["photography-visual-storytelling"], 1756)
        self.assertEqual(TARGETS["contact_find"], "http://www.kriskrug.com/contact")
        self.assertEqual(TARGETS["contact_replace"], "https://kriskrug.co/contact/")
        self.assertTrue(spec_by_id(2819).get("href_repair"))
        self.assertIsNone(spec_by_id(3330)["old_pillar_href"])

    def test_swap_primary_preserves_extra_terms(self):
        self.assertEqual(
            MODULE.swap_primary_category([1757, 99], 1757, 1678),
            [1678, 99],
        )
        self.assertIsNone(MODULE.swap_primary_category([1678], 1757, 1678))
        with self.assertRaises(ValueError):
            MODULE.swap_primary_category([1662], 1757, 1678)

    def test_footer_rewrite_keeps_the_see_also_sibling(self):
        spec = spec_by_id(1067)
        pillar = TARGETS["pillars"]["1756"]
        raw = fake_post(spec)["content"]["raw"]
        rewritten = MODULE.rewrite_footer_pillar(
            raw,
            spec["old_pillar_href"],
            spec["old_pillar_label"],
            pillar["url"],
            pillar["label"],
        )
        self.assertIsNotNone(rewritten)
        self.assertIn(pillar["url"], rewritten)
        self.assertIn(pillar["label"], rewritten)
        self.assertIn("https://kriskrug.co/example/", rewritten)
        self.assertIn("Sibling", rewritten)
        self.assertNotIn("vancouver-ai", rewritten)
        self.assertIsNone(
            MODULE.rewrite_footer_pillar(
                rewritten,
                spec["old_pillar_href"],
                spec["old_pillar_label"],
                pillar["url"],
                pillar["label"],
            )
        )

    def test_dry_run_performs_no_local_or_wordpress_writes(self):
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
        self.lives[1067]["slug"] = "wrong-slug"
        calls = []
        snapshot_dir = self.tmp_path / "snapshots"
        with (
            mock.patch.object(MODULE, "SNAPSHOT_DIR", snapshot_dir),
            mock.patch.object(
                MODULE, "request", side_effect=self._patch_request(calls)
            ),
        ):
            with self.assertRaises(SystemExit) as caught:
                run_main("--apply", "--post-id", "1067")
        self.assertIn("slug is", str(caught.exception))
        self.assertTrue(all(body is None for _, body in calls))
        self.assertFalse(snapshot_dir.exists())

    def test_apply_snapshots_then_posts_categories_and_footer(self):
        calls = []
        snapshot_dir = self.tmp_path / "snapshots"
        with (
            mock.patch.object(MODULE, "SNAPSHOT_DIR", snapshot_dir),
            mock.patch.object(
                MODULE, "request", side_effect=self._patch_request(calls)
            ),
        ):
            self.assertEqual(0, run_main("--apply", "--post-id", "1067"))
        writes = [body for _, body in calls if body is not None]
        self.assertEqual(1, len(writes))
        self.assertEqual(writes[0]["categories"], [1756])
        self.assertIn("photography-visual-storytelling", writes[0]["content"])
        self.assertIn("Sibling", writes[0]["content"])
        snapshots = list(snapshot_dir.glob("*.json"))
        self.assertEqual(1, len(snapshots))
        self.assertEqual(stat.S_IMODE(snapshots[0].stat().st_mode), 0o600)

    def test_3330_is_category_only(self):
        calls = []
        snapshot_dir = self.tmp_path / "snapshots"
        with (
            mock.patch.object(MODULE, "SNAPSHOT_DIR", snapshot_dir),
            mock.patch.object(
                MODULE, "request", side_effect=self._patch_request(calls)
            ),
        ):
            self.assertEqual(0, run_main("--apply", "--post-id", "3330"))
        writes = [body for _, body in calls if body is not None]
        self.assertEqual(writes[0], {"categories": [1676]})

    def test_2819_replaces_exactly_one_dead_href_and_leaves_categories(self):
        calls = []
        snapshot_dir = self.tmp_path / "snapshots"
        with (
            mock.patch.object(MODULE, "SNAPSHOT_DIR", snapshot_dir),
            mock.patch.object(
                MODULE, "request", side_effect=self._patch_request(calls)
            ),
        ):
            self.assertEqual(0, run_main("--apply", "--post-id", "2819"))
        writes = [body for _, body in calls if body is not None]
        self.assertEqual(1, len(writes))
        self.assertNotIn("categories", writes[0])
        self.assertEqual(
            writes[0]["content"].count("http://www.kriskrug.com/contact"), 0
        )
        self.assertEqual(writes[0]["content"].count("https://kriskrug.co/contact/"), 1)
        self.assertIn("connect with me", writes[0]["content"])

    def test_2819_aborts_if_the_dead_href_is_missing_or_duplicated(self):
        self.lives[2819]["content"]["raw"] = "<p>no contact link</p>"
        with mock.patch.object(MODULE, "request", side_effect=self._patch_request([])):
            with self.assertRaises(SystemExit):
                run_main("--post-id", "2819")
        self.lives[2819] = fake_post(
            spec_by_id(2819),
            raw=(
                '<a href="http://www.kriskrug.com/contact">a</a>'
                '<a href="http://www.kriskrug.com/contact">b</a>'
            ),
        )
        with mock.patch.object(MODULE, "request", side_effect=self._patch_request([])):
            with self.assertRaises(SystemExit):
                run_main("--post-id", "2819")

    def test_skip_when_already_applied(self):
        spec = spec_by_id(3814)
        pillar = TARGETS["pillars"]["1678"]
        self.lives[3814] = fake_post(
            spec,
            categories=[1678],
            raw=fake_post(spec)["content"]["raw"].replace(
                f'<a href="{spec["old_pillar_href"]}">{spec["old_pillar_label"]}</a>',
                f'<a href="{pillar["url"]}">{pillar["label"]}</a>',
            ),
        )
        calls = []
        with mock.patch.object(
            MODULE, "request", side_effect=self._patch_request(calls)
        ):
            self.assertEqual(0, run_main("--apply", "--post-id", "3814"))
        self.assertTrue(all(body is None for _, body in calls))

    def test_apply_md_does_not_claim_the_write_already_happened(self):
        apply_md = (
            MODULE.REPO_ROOT
            / "content/drafts/2026-08-02-seo-authority-hubs/fix-826/APPLY.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Prepared, not applied", apply_md)
        self.assertIn("--apply", apply_md)
        self.assertNotIn("\u2014", apply_md)


if __name__ == "__main__":
    unittest.main()
