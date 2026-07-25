"""Unit tests for publish_common helpers (issue #254)."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import publish_common  # noqa: E402


class PublishCommonTests(unittest.TestCase):
    def test_render_text_post_skips_title_and_uses_wp_blocks(self):
        body = "# Title\n\n## Section\n\n---\n\nA [link](https://example.com) here.\n\n### Sub"
        out = publish_common.render_text_post(body)
        self.assertNotIn("<h1", out)
        self.assertIn("<!-- wp:heading -->", out)
        self.assertIn("<!-- wp:separator -->", out)
        self.assertIn('target="_blank"', out)
        self.assertIn('{"level":3}', out)

    def test_parse_markdown_image_order(self):
        body = (
            "# T\n\n"
            "![alt one](images/01-a.png)\n\n"
            "para\n\n"
            "![alt two](images/02-b.png)\n"
        )
        order = publish_common.parse_markdown_image_order(body)
        self.assertEqual(order, [("01-a.png", "alt one"), ("02-b.png", "alt two")])

    def test_load_captions(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            (path / "captions.txt").write_text("a.jpg|Alt A\nb.jpg|Alt B\n")
            self.assertEqual(
                publish_common.load_captions(path),
                {"a.jpg": "Alt A", "b.jpg": "Alt B"},
            )

    def test_upload_image_manifest_dry_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp)
            uploaded, log = publish_common.upload_image_manifest(
                None,
                [("a.png", "alt")],
                src,
                write=False,
            )
        self.assertEqual(uploaded["a.png"]["id"], 0)
        self.assertEqual(uploaded["a.png"]["url"], "DRYRUN/a.png")
        self.assertEqual(log, [])

    def test_find_media_by_stem(self):
        wp = mock.Mock()
        wp.base = "https://example.test"
        wp.s.get.return_value.json.return_value = [
            {"id": 9, "source_url": "https://example.test/wp-content/uploads/stem.jpg"}
        ]
        found = publish_common.find_media_by_stem(wp, "stem")
        self.assertEqual(found, (9, "https://example.test/wp-content/uploads/stem.jpg"))

    def test_validate_term_ids_raises(self):
        wp = mock.Mock()
        wp.base = "https://example.test"
        wp.s.get.return_value.status_code = 404
        with self.assertRaises(SystemExit):
            publish_common.validate_term_ids(wp, "categories", [1678])

    def test_validate_media_id_raises(self):
        wp = mock.Mock()
        wp.base = "https://example.test"
        wp.s.get.return_value.status_code = 404
        with self.assertRaises(SystemExit):
            publish_common.validate_media_id(wp, 11976)

    def test_build_seo_meta_strips_combining_marks(self):
        meta = publish_common.build_seo_meta("Ethọ́s Lab", "desc")
        self.assertFalse(
            any(__import__("unicodedata").combining(c) for c in meta["jetpack_seo_html_title"])
        )

    def test_parse_publish_argv(self):
        flags = publish_common.parse_publish_argv(["--execute", "--update"])
        self.assertTrue(flags.execute)
        self.assertTrue(flags.update)
        self.assertTrue(flags.write)


class FindOrUploadMediaTests(unittest.TestCase):
    """Extracted from the copy-pasted resolve-or-upload loops (issue #254)."""

    def test_dry_run_never_touches_wordpress(self):
        wp = mock.Mock()
        media_id, url = publish_common.find_or_upload_media(
            wp, Path("/tmp/poster-1.png"), "alt", mime="image/png", write=False
        )
        self.assertEqual((media_id, url), (0, "DRYRUN/poster-1.png"))
        wp.s.get.assert_not_called()
        wp.upload_media.assert_not_called()

    def test_reuse_logs_and_does_not_upload(self):
        wp = mock.Mock()
        wp.base = "https://example.test"
        wp.s.get.return_value.json.return_value = [
            {"id": 42, "source_url": "https://example.test/u/poster-1.png"}
        ]
        log: list[str] = []
        media_id, url = publish_common.find_or_upload_media(
            wp, Path("/tmp/poster-1.png"), "alt", mime="image/png", write=True, log=log
        )
        self.assertEqual((media_id, url), (42, "https://example.test/u/poster-1.png"))
        self.assertEqual(log, ["poster-1.png -> REUSE id=42"])
        wp.upload_media.assert_not_called()

    def test_new_upload_logs_id_and_url(self):
        wp = mock.Mock()
        wp.base = "https://example.test"
        wp.s.get.return_value.json.return_value = []
        wp.upload_media.return_value = {"id": 43, "source_url": "https://example.test/u/new.png"}
        log: list[str] = []
        media_id, url = publish_common.find_or_upload_media(
            wp, Path("/tmp/new.png"), "alt", mime="image/png", write=True, log=log
        )
        self.assertEqual((media_id, url), (43, "https://example.test/u/new.png"))
        self.assertEqual(log, ["new.png -> NEW id=43 https://example.test/u/new.png"])

    def test_label_prefixes_the_log_line(self):
        """load_photos_from_dir logs `subdir/filename`; the shape must not change."""
        wp = mock.Mock()
        wp.base = "https://example.test"
        wp.s.get.return_value.json.return_value = [
            {"id": 7, "source_url": "https://example.test/u/01-a.jpg"}
        ]
        log: list[str] = []
        publish_common.find_or_upload_media(
            wp, Path("/tmp/01-a.jpg"), "alt", mime="image/jpeg", write=True,
            label="photos/best/01-a.jpg", log=log,
        )
        self.assertEqual(log, ["photos/best/01-a.jpg -> REUSE id=7"])


class LoadPhotosFromDirTests(unittest.TestCase):
    def test_dry_run_shape_is_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            stage = Path(tmp)
            directory = stage / "photos" / "best"
            directory.mkdir(parents=True)
            (directory / "01-water.jpg").write_bytes(b"x")
            (directory / "_skipped.jpg").write_bytes(b"x")
            (directory / "captions.txt").write_text("01-water.jpg|A caption\n")
            items = publish_common.load_photos_from_dir(
                mock.Mock(), stage, "photos/best", write=False
            )
        self.assertEqual(
            items, [(0, "DRYRUN/01-water.jpg", "A caption", "A caption", "01-water.jpg")]
        )

    def test_alt_from_slug_appends_protest_sign(self):
        with tempfile.TemporaryDirectory() as tmp:
            stage = Path(tmp)
            directory = stage / "photos" / "best"
            directory.mkdir(parents=True)
            (directory / "01-water-the-servers.jpg").write_bytes(b"x")
            items = publish_common.load_photos_from_dir(
                mock.Mock(), stage, "photos/best", write=False, alt_from_slug=True
            )
        self.assertEqual(items[0][2], "water the servers protest sign")


class FindExistingPostBySlugTests(unittest.TestCase):
    def test_returns_first_hit(self):
        wp = mock.Mock()
        wp.base = "https://example.test"
        wp.s.get.return_value.json.return_value = [{"id": 11}, {"id": 12}]
        self.assertEqual(publish_common.find_existing_post_by_slug(wp, "a-slug"), {"id": 11})

    def test_queries_any_status_in_edit_context(self):
        wp = mock.Mock()
        wp.base = "https://example.test"
        wp.s.get.return_value.json.return_value = []
        publish_common.find_existing_post_by_slug(wp, "a-slug")
        _, kwargs = wp.s.get.call_args
        self.assertEqual(
            kwargs["params"], {"slug": "a-slug", "status": "any", "context": "edit"}
        )

    def test_returns_none_when_absent_or_malformed(self):
        wp = mock.Mock()
        wp.base = "https://example.test"
        wp.s.get.return_value.json.return_value = []
        self.assertIsNone(publish_common.find_existing_post_by_slug(wp, "a-slug"))
        wp.s.get.return_value.json.return_value = {"code": "rest_no_route"}
        self.assertIsNone(publish_common.find_existing_post_by_slug(wp, "a-slug"))


class RawParagraphTests(unittest.TestCase):
    def test_differs_from_br_joined_paragraph_on_multiline_blocks(self):
        block = "line one\nline two"
        self.assertIn("line one\nline two", publish_common.raw_paragraph(block))
        self.assertIn(
            "line one<br>line two", publish_common.render_paragraph_from_markdown(block)
        )

    def test_agrees_on_single_line_blocks(self):
        block = "just one line with a [link](https://example.com)"
        self.assertEqual(
            publish_common.raw_paragraph(block),
            publish_common.render_paragraph_from_markdown(block),
        )


if __name__ == "__main__":
    unittest.main()
