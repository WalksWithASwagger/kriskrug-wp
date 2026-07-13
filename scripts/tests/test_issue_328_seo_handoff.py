import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "fixes/issue-328-most-benevolent-seo-handoff-2026-07-12.json"
HANDOFF = ROOT / "fixes/issue-328-most-benevolent-seo-handoff-2026-07-12.md"


class Issue328SeoHandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_evidence_is_limited_to_the_issue_aggregate(self):
        evidence = self.data["evidence"]
        self.assertEqual("most benevolent", evidence["query"])
        self.assertEqual(20, evidence["impressions"])
        self.assertEqual(8.4, evidence["average_position"])
        self.assertEqual(0.0, evidence["ctr_percent"])

    def test_target_identity_and_metadata_observation_are_stable(self):
        target = self.data["target"]
        metadata = self.data["current_public_metadata"]

        self.assertEqual(3814, target["id"])
        self.assertEqual(
            target["url"],
            f"https://kriskrug.co/2023/11/04/{target['slug']}/",
        )
        self.assertEqual(
            metadata["document_title_chars"],
            len(metadata["document_title"]),
        )
        self.assertFalse(metadata["standard_meta_description_present"])
        self.assertTrue(metadata["open_graph_description_present"])

    def test_link_replacements_only_wrap_existing_copy(self):
        target_url = self.data["target"]["url"]
        source_ids = set()

        for patch in self.data["link_patches"]:
            match = re.fullmatch(
                r'<a href="([^"]+)">([^<]+)</a>',
                patch["replacement"],
            )
            self.assertIsNotNone(match)
            self.assertEqual(target_url, match.group(1))
            self.assertEqual(patch["needle"], match.group(2))
            self.assertEqual(1, patch["expected_needle_count"])
            self.assertEqual(0, patch["expected_target_href_count_before"])
            self.assertFalse(patch["copy_change"])
            self.assertTrue(patch["source_url"].startswith("https://kriskrug.co/"))
            self.assertNotIn(patch["source_id"], source_ids)
            source_ids.add(patch["source_id"])

        self.assertEqual({2950, 2665}, source_ids)

    def test_future_write_boundary_is_body_only(self):
        boundary = self.data["future_write_boundary_if_separately_approved"]
        self.assertEqual(["content"], boundary["allowed_rest_top_level_keys"])
        self.assertEqual(
            {
                "title",
                "slug",
                "status",
                "date",
                "categories",
                "tags",
                "meta",
            },
            set(boundary["forbidden_rest_top_level_keys"]),
        )
        self.assertFalse(self.data["live_wordpress_write_performed"])

    def test_handoff_keeps_live_and_private_surfaces_out_of_scope(self):
        text = HANDOFF.read_text(encoding="utf-8")
        self.assertIn("no live WordPress write", text)
        self.assertIn("Do not apply these patches from this PR.", text)
        self.assertIn("The only allowed top-level REST key is", text)

        serialized = json.dumps(self.data).lower()
        for secret_marker in (
            "authorization",
            "bearer ",
            "wp_app_password",
            "wp_user",
            "oauth",
        ):
            self.assertNotIn(secret_marker, serialized)

    def test_next_digest_has_a_page_pair_and_measurable_signal(self):
        verification = self.data["next_digest"]
        self.assertEqual(self.data["evidence"]["query"], verification["query"])
        self.assertEqual(self.data["target"]["url"], verification["landing_page"])
        self.assertEqual(
            {"impressions", "clicks", "ctr_percent", "average_position"},
            set(verification["compare"]),
        )
        self.assertEqual(7.0, verification["success_signal"]["average_position_below"])
        self.assertEqual(1, verification["success_signal"]["clicks_at_least"])


if __name__ == "__main__":
    unittest.main()
