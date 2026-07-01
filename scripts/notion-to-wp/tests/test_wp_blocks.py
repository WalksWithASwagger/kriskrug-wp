import sys
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import wp_blocks  # noqa: E402


class WpBlocksTests(unittest.TestCase):
    def test_image_int_id_lightbox_no_anchor(self):
        h = wp_blocks.image(123, "https://x/y.png", "alt text")
        self.assertIn('"id":123', h)
        self.assertIn('"lightbox":{"enabled":true}', h)
        self.assertIn('class="wp-image-123"', h)
        self.assertNotIn("<a href", h)            # lightbox provides zoom, no link wrapper
        self.assertNotIn("linkDestination", h)

    def test_image_tbd_id_omits_id_keeps_class(self):
        # main Notion pipeline dry-run: id not yet known
        h = wp_blocks.image("TBD", "https://x/y.png", "a")
        self.assertNotIn('"id":', h)
        self.assertIn('class="wp-image-TBD"', h)

    def test_image_none_id_no_id_no_class(self):
        h = wp_blocks.image(None, "x.png", "a", align=None, size_slug=None, lightbox=False)
        self.assertNotIn('"id":', h)
        self.assertNotIn("wp-image-", h)
        self.assertIn('"linkDestination":"none"', h)

    def test_inline_image_is_460_and_resized(self):
        h = wp_blocks.inline_image(5, "u", "a", caption="cap")
        self.assertIn('"width":"460px"', h)
        self.assertIn('style="width:460px"', h)
        self.assertIn("is-resized", h)
        self.assertIn('<figcaption class="wp-element-caption">cap</figcaption>', h)

    def test_hero_image_full_width(self):
        h = wp_blocks.hero_image(7, "u", "a")
        self.assertNotIn("width", h)
        self.assertIn("aligncenter", h)
        self.assertIn('"lightbox":{"enabled":true}', h)

    def test_gallery_wraps_lightbox_images(self):
        h = wp_blocks.gallery([(1, "u1", "a1", "c1"), (2, "u2", "a2", None)], columns=3)
        self.assertIn("<!-- wp:gallery", h)
        self.assertIn("columns-3", h)
        self.assertEqual(h.count("<!-- wp:image "), 2)
        self.assertEqual(h.count('"lightbox":{"enabled":true}'), 2)

    def test_separator(self):
        self.assertIn('wp-block-separator', wp_blocks.separator())

    def test_heading_default_h2_no_level_attr(self):
        h = wp_blocks.heading("Title")
        self.assertIn("<!-- wp:heading -->", h)
        self.assertIn('<h2 class="wp-block-heading">Title</h2>', h)

    def test_heading_level_3(self):
        h = wp_blocks.heading("Sub", level=3)
        self.assertIn('<!-- wp:heading {"level":3} -->', h)
        self.assertIn('<h3 class="wp-block-heading">Sub</h3>', h)

    def test_pullquote(self):
        h = wp_blocks.pullquote("punch")
        self.assertIn('wp-block-pullquote', h)
        self.assertIn("<blockquote><p>punch</p></blockquote>", h)

    def test_inline_links_bold_italic(self):
        ext = wp_blocks.inline("see [docs](https://example.com)")
        self.assertIn('target="_blank" rel="noopener noreferrer"', ext)
        internal = wp_blocks.inline("see [home](https://kriskrug.co/about)")
        self.assertNotIn("target=", internal)
        self.assertIn("<strong>x</strong>", wp_blocks.inline("**x**"))
        self.assertIn("<em>y</em>", wp_blocks.inline("*y*"))


if __name__ == "__main__":
    unittest.main()
