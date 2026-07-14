import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "fixes/issue-342-both-hands-full-link-handoff-2026-07-13.json"
HANDOFF = ROOT / "fixes/issue-342-both-hands-full-link-handoff-2026-07-13.md"


class Issue342BothHandsFullLinkHandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_search_evidence_is_digest_safe_and_exact(self):
        evidence = self.data["evidence"]

        self.assertEqual(
            {"start": "2026-06-13", "end": "2026-07-10"},
            evidence["current_window"],
        )
        self.assertEqual(
            {
                "impressions": 56,
                "clicks": 3,
                "ctr_percent": 5.36,
                "average_position": 8.27,
            },
            evidence["source_page"],
        )
        self.assertEqual(6, evidence["target_property"]["impressions"])
        self.assertEqual(0, evidence["target_property"]["clicks"])
        self.assertEqual(21.67, evidence["target_property"]["average_position"])
        self.assertEqual(4, evidence["target_homepage"]["impressions"])
        self.assertEqual(16.5, evidence["target_homepage"]["average_position"])

    def test_source_and_target_public_state_are_locked(self):
        source = self.data["source"]
        target = self.data["target"]

        self.assertEqual(11171, source["id"])
        self.assertEqual("both-hands-full", source["slug"])
        self.assertEqual("publish", source["status"])
        self.assertEqual("2026-06-28T20:26:51", source["modified"])
        self.assertEqual(source["url"], source["canonical"])
        self.assertEqual(200, source["http_status"])
        self.assertEqual(1, source["h1_count"])

        self.assertEqual("https://www.bothhandsfull.com", target["url"])
        self.assertEqual(target["url"], target["canonical"])
        self.assertEqual(200, target["http_status"])
        self.assertEqual(1, target["h1_count"])

    def test_patch_changes_only_the_href(self):
        patch = self.data["link_patch"]
        anchor_pattern = r'<a href="([^"]+)"(?: rel="([^"]+)")?>([^<]+)</a>'
        before = re.fullmatch(anchor_pattern, patch["current_anchor_html"])
        after = re.fullmatch(anchor_pattern, patch["replacement_anchor_html"])

        self.assertIsNotNone(before)
        self.assertIsNotNone(after)
        self.assertEqual("both hands full", before.group(3))
        self.assertEqual(before.group(3), after.group(3))
        self.assertIsNone(before.group(2))
        self.assertIsNone(after.group(2))
        self.assertNotEqual(before.group(1), after.group(1))
        self.assertEqual(self.data["target"]["url"], after.group(1))
        self.assertEqual(
            patch["context_before"].replace(
                patch["current_anchor_html"], patch["replacement_anchor_html"], 1
            ),
            patch["context_after"],
        )
        self.assertEqual(1, patch["expected_current_anchor_count"])
        self.assertEqual(1, patch["expected_context_count"])
        self.assertEqual(0, patch["expected_target_href_count_before"])
        self.assertEqual(1, patch["expected_target_href_count_after"])
        self.assertFalse(patch["copy_change"])
        self.assertFalse(patch["rel_attribute_added"])
        self.assertEqual("public_rest_content_rendered", patch["observed_in"])
        self.assertTrue(patch["future_authenticated_raw_guard_required"])

    def test_future_write_boundary_is_content_only(self):
        boundary = self.data["future_write_boundary_if_separately_approved"]

        self.assertEqual(["content"], boundary["allowed_rest_top_level_keys"])
        self.assertTrue(
            {
                "title",
                "slug",
                "status",
                "date",
                "categories",
                "tags",
                "excerpt",
                "meta",
            }.issubset(boundary["forbidden_rest_top_level_keys"])
        )
        self.assertIn(
            "fresh ID, slug, status, and modified-date checks",
            boundary["requires"],
        )
        self.assertIn("retained content.raw rollback snapshot", boundary["requires"])

    def test_worker_lane_has_no_live_write_or_secret_material(self):
        self.assertEqual("human-review-required", self.data["status"])
        self.assertFalse(self.data["live_wordpress_write_performed"])

        serialized = json.dumps(self.data).lower()
        for marker in (
            "authorization",
            "bearer ",
            "wp_app_password",
            "wp_user",
            "oauth",
        ):
            self.assertNotIn(marker, serialized)

        text = HANDOFF.read_text(encoding="utf-8")
        self.assertIn("no live WordPress write", text)
        self.assertIn("Do not apply this handoff from the worker lane.", text)
        self.assertIn("#339", text)
        self.assertIn("duplicate", text.lower())

    def test_measurement_waits_for_recrawl(self):
        measurement = self.data["next_digest"]

        self.assertEqual(14, measurement["earliest_full_days_after_live_change"])
        self.assertEqual(28, measurement["secondary_review_days_after_live_change"])
        self.assertEqual(self.data["source"]["url"], measurement["source_page"])
        self.assertEqual(self.data["target"]["url"], measurement["target_homepage"])
        self.assertIn("source_page_clicks", measurement["compare"])
        self.assertIn("target_property_impressions", measurement["compare"])


if __name__ == "__main__":
    unittest.main()
