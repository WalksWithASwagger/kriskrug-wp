import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from inventory_lib import SEORecord, record_from_item, summarize  # noqa: E402


class InventoryTests(unittest.TestCase):
    def test_record_from_item_detects_populated_meta(self):
        item = {
            "id": 42,
            "slug": "sample-post",
            "title": {"rendered": "Sample Post"},
            "link": "https://kriskrug.co/sample-post/",
            "meta": {
                "jetpack_seo_html_title": "Custom SEO Title",
                "advanced_seo_description": "Custom meta description.",
                "jetpack_publicize_message": "Share hook",
            },
        }
        record = record_from_item("post", item)
        self.assertTrue(record.has_seo_title)
        self.assertTrue(record.has_meta_description)
        self.assertTrue(record.has_social_message)

    def test_record_from_item_handles_missing_meta(self):
        item = {
            "id": 7,
            "slug": "bare-page",
            "title": {"rendered": "Bare Page"},
            "link": "https://kriskrug.co/bare-page/",
            "meta": {},
        }
        record = record_from_item("page", item)
        self.assertFalse(record.has_seo_title)
        self.assertFalse(record.has_meta_description)

    def test_summarize_counts_gaps(self):
        records = [
            SEORecord("post", 1, "a", "A", "https://x/a", True, 5, False, 0, False, 0),
            SEORecord("page", 2, "b", "B", "https://x/b", False, 0, True, 10, False, 0),
        ]
        stats = summarize(records)
        self.assertEqual(stats["missing_seo_title"], 1)


if __name__ == "__main__":
    unittest.main()
