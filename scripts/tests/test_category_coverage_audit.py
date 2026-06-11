import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from category_coverage_audit import (  # noqa: E402
    build_audit,
    category_from_item,
    post_from_item,
    render_human,
)


class CategoryCoverageAuditTests(unittest.TestCase):
    def test_fixture_posts_produce_category_counts_and_misc_callout(self):
        categories = {
            category.wp_id: category
            for category in [
                category_from_item({"id": 1, "name": "Misc", "slug": "misc", "count": 769}),
                category_from_item({"id": 7, "name": "AI Creatives", "slug": "ai-creatives", "count": 12}),
                category_from_item({"id": 8, "name": "Field Notes", "slug": "field-notes", "count": 3}),
            ]
        }
        posts = [
            post_from_item(
                {
                    "id": 101,
                    "slug": "one",
                    "title": {"rendered": "One"},
                    "link": "https://kriskrug.co/one/",
                    "date": "2026-06-01T00:00:00",
                    "categories": [1],
                }
            ),
            post_from_item(
                {
                    "id": 102,
                    "slug": "two",
                    "title": {"rendered": "Two"},
                    "link": "https://kriskrug.co/two/",
                    "date": "2026-06-02T00:00:00",
                    "categories": [7, 8],
                }
            ),
            post_from_item(
                {
                    "id": 103,
                    "slug": "three",
                    "title": {"rendered": "Three"},
                    "link": "https://kriskrug.co/three/",
                    "date": "2026-06-03T00:00:00",
                    "categories": [7],
                }
            ),
        ]

        audit = build_audit(posts, categories)

        counts = {row["slug"]: row["recent_post_count"] for row in audit["category_counts"]}
        self.assertEqual(counts["misc"], 1)
        self.assertEqual(counts["ai-creatives"], 2)
        self.assertEqual(counts["field-notes"], 1)
        self.assertEqual(audit["misc"]["recent_post_count"], 1)
        self.assertEqual(audit["misc"]["live_count"], 769)
        self.assertEqual(
            audit["multi_category_distribution"],
            [{"categories_per_post": 1, "posts": 2}, {"categories_per_post": 2, "posts": 1}],
        )
        self.assertEqual([post["slug"] for post in audit["multi_category_posts"]], ["two"])

    def test_empty_categories_are_reported_without_posts(self):
        categories = {
            12: category_from_item({"id": 12, "name": "Empty Topic", "slug": "empty-topic", "count": 0})
        }

        audit = build_audit([], categories)
        report = {
            "base_url": "https://kriskrug.co",
            "post_limit": 100,
            "audit": audit,
        }
        human = render_human(report)
        payload = json.dumps(audit)

        self.assertIn("Empty Topic", human)
        self.assertIn("No posts scanned", human)
        self.assertIn("empty-topic", payload)

    def test_post_parser_handles_missing_or_empty_categories(self):
        post = post_from_item(
            {
                "id": 104,
                "slug": "bare",
                "title": {"rendered": "Bare &amp; Clean"},
                "link": "https://kriskrug.co/bare/",
                "date": "2026-06-04T00:00:00",
                "categories": [],
            }
        )

        self.assertEqual(post.title, "Bare & Clean")
        self.assertEqual(post.category_ids, ())
        audit = build_audit([post], {})
        self.assertEqual(audit["multi_category_distribution"], [{"categories_per_post": 0, "posts": 1}])


if __name__ == "__main__":
    unittest.main()
