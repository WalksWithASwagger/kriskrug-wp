"""#587 hero fetch engine: resolution order, YouTube URL construction, skips.

Everything here runs offline with temp fixtures. The engine's dry-run path is
pure planning, so no test touches the network or WordPress.
"""

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/events_page"))

import fetch_event_heroes as feh  # noqa: E402


class YoutubeHelpers(unittest.TestCase):
    def test_thumb_url_construction(self):
        self.assertEqual(
            feh.youtube_thumb_url("abc-_123XYZ"),
            "https://img.youtube.com/vi/abc-_123XYZ/maxresdefault.jpg",
        )

    def test_thumb_url_fallback_name(self):
        self.assertEqual(
            feh.youtube_thumb_url("abc-_123XYZ", "hqdefault"),
            "https://img.youtube.com/vi/abc-_123XYZ/hqdefault.jpg",
        )

    def test_id_from_watch_url_with_leading_dash(self):
        # Real catalog row: LaSalle keynote video id starts with a dash.
        self.assertEqual(
            feh.youtube_id_from_url("https://www.youtube.com/watch?v=-c7mgY2aSgM"),
            "-c7mgY2aSgM",
        )

    def test_id_from_youtu_be(self):
        self.assertEqual(
            feh.youtube_id_from_url("https://youtu.be/1OcC-0X6Nb8"),
            "1OcC-0X6Nb8",
        )

    def test_non_youtube_url_gives_none(self):
        self.assertIsNone(feh.youtube_id_from_url("https://lu.ma/vancouver-ai"))
        self.assertIsNone(feh.youtube_id_from_url(None))


class OgImageExtract(unittest.TestCase):
    def test_property_before_content(self):
        html = '<meta property="og:image" content="https://cdn.example/a.png"/>'
        self.assertEqual(feh.extract_og_image(html), "https://cdn.example/a.png")

    def test_content_before_property(self):
        html = '<meta content="https://cdn.example/b.jpg" property="og:image">'
        self.assertEqual(feh.extract_og_image(html), "https://cdn.example/b.jpg")

    def test_ignores_og_image_width(self):
        html = '<meta property="og:image:width" content="1200">'
        self.assertIsNone(feh.extract_og_image(html))

    def test_no_og_image(self):
        self.assertIsNone(feh.extract_og_image("<html><head></head></html>"))


class ResolutionOrder(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        base = Path(self.tmp.name).resolve()
        self.roots = {"repo": base / "repo", "kk_kb": base / "kb"}
        (self.roots["repo"] / "art").mkdir(parents=True)
        self.roots["kk_kb"].mkdir(parents=True)
        self.hero = self.roots["repo"] / "art" / "hero.jpg"
        self.hero.write_bytes(b"jpegish")
        self.cache = base / "cache"

    def plan(self, event, allow_rafiki=False):
        return feh.plan_event(event, self.roots, self.cache, allow_rafiki=allow_rafiki)

    def test_repo_asset_wins_over_youtube(self):
        row = self.plan(
            {
                "id": "e1",
                "image": {"path": "repo:art/hero.jpg"},
                "youtube_id": "abc123xyz",
            }
        )
        self.assertEqual(row["source"], "repo-asset")
        self.assertEqual(row["local_path"], str(self.hero))
        self.assertFalse(row["fetched"])

    def test_youtube_when_no_asset(self):
        row = self.plan({"id": "e2", "image": {}, "youtube_id": "abc123xyz"})
        self.assertEqual(row["source"], "youtube")
        self.assertEqual(
            row["remote_url"],
            "https://img.youtube.com/vi/abc123xyz/maxresdefault.jpg",
        )
        self.assertTrue(row["local_path"].endswith("e2-youtube.jpg"))

    def test_missing_asset_falls_through_to_youtube_url(self):
        row = self.plan(
            {
                "id": "e3",
                "image": {"path": "repo:art/nope.jpg"},
                "url": "https://www.youtube.com/watch?v=zzz999aaa",
            }
        )
        self.assertEqual(row["source"], "youtube")
        self.assertEqual(row["youtube_id"], "zzz999aaa")
        self.assertIn("missing on disk", row["note"])

    def test_og_snapshot_hit(self):
        snapshot = self.roots["kk_kb"] / "appearance.html"
        snapshot.write_text(
            '<html><head><meta content="https://cdn.example/ev.png" '
            'property="og:image"/></head></html>',
            encoding="utf-8",
        )
        row = self.plan(
            {"id": "e4", "image": {}, "og_html_path": "kk_kb:appearance.html"}
        )
        self.assertEqual(row["source"], "og-image")
        self.assertEqual(row["og_from"], "snapshot")
        self.assertEqual(row["remote_url"], "https://cdn.example/ev.png")
        self.assertTrue(row["local_path"].endswith("e4-og.png"))

    def test_og_page_deferred_in_dry_run(self):
        row = self.plan({"id": "e5", "image": {}, "url": "https://lu.ma/sept-ai"})
        self.assertEqual(row["source"], "og-image")
        self.assertEqual(row["og_from"], "page")
        self.assertIsNone(row["remote_url"])
        self.assertIsNone(row["local_path"])

    def test_missing_fields_skip(self):
        row = self.plan({"id": "e6", "image": {}})
        self.assertEqual(row["source"], "none")
        self.assertIsNone(row["local_path"])
        self.assertIn("MISSING hero_hint", row["note"])

    def test_rafiki_only_with_flag(self):
        gap = {"id": "e7", "image": {}}
        self.assertEqual(self.plan(gap)["source"], "none")
        row = self.plan(gap, allow_rafiki=True)
        self.assertEqual(row["source"], "rafiki")
        self.assertIsNone(row["local_path"])

    def test_wp_media_short_circuit(self):
        row = self.plan({"id": "e8", "image": {"media_id": 12660}})
        self.assertEqual(row["source"], "wp-media")
        self.assertIsNone(row["local_path"])

    def test_event_without_id_is_skipped(self):
        rows, skipped = feh.resolve_events(
            [{"image": {}}, {"id": "ok", "image": {}}], self.roots, self.cache
        )
        self.assertEqual(skipped, 1)
        self.assertEqual([r["id"] for r in rows], ["ok"])


class CliDryRun(unittest.TestCase):
    def test_events_json_dry_run_exits_zero_and_prints_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            events_path = Path(tmp) / "events.json"
            events_path.write_text(
                json.dumps(
                    [
                        {"id": "x1", "image": {}, "youtube_id": "abc123xyz"},
                        {"id": "x2", "image": {}},
                    ]
                ),
                encoding="utf-8",
            )
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                rc = feh.main(["--events-json", str(events_path), "--dry-run"])
            self.assertEqual(rc, 0)
            rows = json.loads(out.getvalue())
            self.assertEqual(len(rows), 2)
            for row in rows:
                for key in ("id", "source", "local_path"):
                    self.assertIn(key, row)
            by_id = {row["id"]: row for row in rows}
            self.assertEqual(by_id["x1"]["source"], "youtube")
            self.assertEqual(by_id["x2"]["source"], "none")
            self.assertIn("DRY-RUN", err.getvalue())

    def test_ids_filter(self):
        with tempfile.TemporaryDirectory() as tmp:
            events_path = Path(tmp) / "events.json"
            events_path.write_text(
                json.dumps(
                    [
                        {"id": "keep", "image": {}, "youtube_id": "abc123xyz"},
                        {"id": "drop", "image": {}},
                    ]
                ),
                encoding="utf-8",
            )
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                rc = feh.main(["--events-json", str(events_path), "--ids", "keep"])
            self.assertEqual(rc, 0)
            rows = json.loads(out.getvalue())
            self.assertEqual([row["id"] for row in rows], ["keep"])


if __name__ == "__main__":
    unittest.main()
