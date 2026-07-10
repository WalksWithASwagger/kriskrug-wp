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
import wp_blocks  # noqa: E402


class PublishCommonTests(unittest.TestCase):
    def test_inline_delegates_to_wp_blocks(self):
        html = wp_blocks.inline("[x](https://example.com)")
        self.assertIn('target="_blank"', html)
        self.assertIn('rel="noopener noreferrer"', html)

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

    def test_one_off_scripts_import_publish_common(self):
        for name in (
            "publish_dc_protest_draft.py",
            "publish_you_cant_drink_data.py",
            "publish_proximity_game.py",
        ):
            src = (SCRIPT_DIR / name).read_text(encoding="utf-8")
            self.assertIn("publish_common", src, f"{name} should import publish_common")


if __name__ == "__main__":
    unittest.main()
