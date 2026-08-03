import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from inventory_lib import (  # noqa: E402
    SEORecord,
    extract_rendered_seo,
    meta_keys_registered,
    record_from_item,
    record_from_rendered,
    render_markdown,
    summarize,
)


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


class UnregisteredMetaTests(unittest.TestCase):
    """The false negative that made the audit report all 1016 items as missing."""

    def test_absent_keys_are_not_mistaken_for_empty_values(self):
        # What REST returns with Jetpack deactivated: the SEO keys are gone.
        items = [{"id": 1, "meta": {"footnotes": ""}}]
        self.assertFalse(meta_keys_registered(items))

    def test_registered_but_empty_keys_still_count_as_registered(self):
        items = [{"id": 1, "meta": {"jetpack_seo_html_title": "", "footnotes": ""}}]
        self.assertTrue(meta_keys_registered(items))

    def test_any_item_carrying_a_key_proves_registration(self):
        items = [
            {"id": 1, "meta": {"footnotes": ""}},
            {"id": 2, "meta": {"advanced_seo_description": "set"}},
        ]
        self.assertTrue(meta_keys_registered(items))

    def test_empty_result_set_is_not_treated_as_unregistered(self):
        self.assertFalse(meta_keys_registered([]))


class RenderedSourceTests(unittest.TestCase):
    def test_extracts_title_and_description(self):
        page = (
            "<html><head><title>You Can&#039;t Drink Data | Notes</title>"
            '<meta name="description" content="A post about an AI protest." />'
            "</head><body></body></html>"
        )
        title, description = extract_rendered_seo(page)
        self.assertEqual(title, "You Can't Drink Data | Notes")
        self.assertEqual(description, "A post about an AI protest.")

    def test_handles_content_attribute_before_name(self):
        page = '<meta content="Reversed order." name="description">'
        _, description = extract_rendered_seo(page)
        self.assertEqual(description, "Reversed order.")

    def test_missing_tags_report_absent_not_crash(self):
        title, description = extract_rendered_seo("<html><head></head></html>")
        self.assertEqual(title, "")
        self.assertEqual(description, "")

    def test_record_from_rendered_marks_social_unmeasurable(self):
        item = {
            "id": 9,
            "slug": "p",
            "title": {"rendered": "P"},
            "link": "https://kriskrug.co/p/",
        }
        record = record_from_rendered("post", item, "<title>Real Title</title>")
        self.assertTrue(record.has_seo_title)
        self.assertFalse(record.has_social_message)

    def test_rendered_summary_does_not_claim_social_gaps(self):
        records = [SEORecord("post", 1, "a", "A", "u", True, 5, True, 8, False, 0)]
        self.assertIn("not measurable", render_markdown(records, "rendered"))
        self.assertNotIn("not measurable", render_markdown(records, "meta"))


if __name__ == "__main__":
    unittest.main()
