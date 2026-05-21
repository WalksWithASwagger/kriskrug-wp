import sys
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import kk_notion_to_wp  # noqa: E402


class CategoryRoutingTests(unittest.TestCase):
    def test_known_type_routes_directly(self):
        category, route = kk_notion_to_wp.resolve_category("Report", [])

        self.assertEqual(category, "Vancouver AI Ecosystem")
        self.assertEqual(route, "type:Report")

    def test_explicit_override_wins(self):
        category, route = kk_notion_to_wp.resolve_category(
            "Feature",
            ["AI Ethics"],
            category_override="Field Notes",
        )

        self.assertEqual(category, "Field Notes")
        self.assertEqual(route, "override")

    def test_feature_routes_from_community_tags(self):
        category, route = kk_notion_to_wp.resolve_category(
            "Feature",
            ["BC + AI", "Comox", "Community Spotlight"],
        )

        self.assertEqual(category, "Vancouver AI Ecosystem")
        self.assertEqual(route, "feature-tags")

    def test_feature_routes_from_ethics_tags(self):
        category, route = kk_notion_to_wp.resolve_category(
            "Feature",
            ["Responsible AI", "Certification"],
        )

        self.assertEqual(category, "AI Ethics & Philosophy")
        self.assertEqual(route, "feature-tags")

    def test_ambiguous_feature_requires_review(self):
        category, route = kk_notion_to_wp.resolve_category("Feature", [])

        self.assertEqual(category, kk_notion_to_wp.CATEGORY_REVIEW_REQUIRED)
        self.assertEqual(route, "feature-needs-category")
        self.assertTrue(kk_notion_to_wp.category_requires_review(category))


if __name__ == "__main__":
    unittest.main()
