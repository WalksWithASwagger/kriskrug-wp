import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from public_image_audit import ImageParser, is_filename_style_alt, media_id_from_class, summarize


class PublicImageAuditTests(unittest.TestCase):
    def test_parser_classifies_decorative_and_problem_alt_states(self):
        parser = ImageParser("https://kriskrug.co/example/")
        parser.feed(
            """
            <img class="aurora-brand-logo" src="/logo.png" alt="">
            <img class="wp-image-123" src="/wp-content/uploads/flickr-photographr-badge.jpg" alt="flickr-photographr-badge.jpg" srcset="x 1x" loading="lazy">
            <img src="/missing.jpg">
            """
        )

        self.assertEqual(len(parser.images), 3)
        self.assertEqual(media_id_from_class(parser.images[1]["class"]), 123)
        self.assertTrue(is_filename_style_alt(parser.images[1]["alt"], parser.images[1]["src"]))

    def test_summary_counts_alt_states(self):
        from public_image_audit import RenderedImage

        rows = [
            RenderedImage("u", "url", None, "home", "/logo.png", "", None, "", False, "aurora-brand-logo", "", "", ""),
            RenderedImage("u", "url", None, "home", "/flickr-photographr-badge.jpg", "flickr-photographr-badge.jpg", 123, "lazy", True, "", "", "", ""),
            RenderedImage("u", "url", None, "home", "/missing.jpg", None, None, "", False, "", "", "", ""),
        ]

        stats = summarize(rows)

        self.assertEqual(stats["decorative_empty"], 1)
        self.assertEqual(stats["filename_style"], 1)
        self.assertEqual(stats["missing_attr"], 1)


if __name__ == "__main__":
    unittest.main()
