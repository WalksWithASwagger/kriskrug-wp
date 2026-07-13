import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "fixes/issue-336-ai-second-brain-seo-handoff-2026-07-13.json"
HANDOFF = ROOT / "fixes/issue-336-ai-second-brain-seo-handoff-2026-07-13.md"


class Issue336AiSecondBrainSeoHandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_digest_safe_evidence_is_exact(self):
        evidence = self.data["evidence"]

        self.assertEqual("2026-06-12", evidence["window_start"])
        self.assertEqual("2026-07-09", evidence["window_end"])
        self.assertEqual(
            {
                "impressions": 1053,
                "clicks": 10,
                "ctr_percent": 0.95,
                "average_position": 11.27,
            },
            evidence["page"],
        )
        self.assertEqual("ai second brain", evidence["query"]["text"])
        self.assertEqual(46, evidence["query"]["impressions"])
        self.assertEqual(2, evidence["query"]["clicks"])
        self.assertEqual(17.52, evidence["query"]["average_position"])

    def test_target_identity_and_public_state_are_locked(self):
        target = self.data["target"]
        public = self.data["current_public_metadata"]

        self.assertEqual(8802, target["id"])
        self.assertEqual("publish", target["status"])
        self.assertEqual(
            target["url"],
            f"https://kriskrug.co/2025/04/01/{target['slug']}/",
        )
        self.assertEqual(target["url"], public["canonical"])
        self.assertEqual(200, public["http_status"])
        self.assertEqual(1, public["h1_count"])
        self.assertFalse(public["standard_meta_description_present"])
        self.assertFalse(public["jetpack_seo_meta_fields_exposed"])
        self.assertEqual(["footnotes"], public["authenticated_rest_meta_keys"])

    def test_proposed_metadata_is_narrow_and_within_policy(self):
        proposed = self.data["proposed_metadata"]
        fields = proposed["field_values"]
        lengths = proposed["field_lengths"]

        self.assertEqual(
            {"jetpack_seo_html_title", "advanced_seo_description"},
            set(fields),
        )
        for key, value in fields.items():
            self.assertEqual(len(value), lengths[key])

        self.assertLessEqual(lengths["jetpack_seo_html_title"], 60)
        self.assertGreaterEqual(lengths["advanced_seo_description"], 150)
        self.assertLessEqual(lengths["advanced_seo_description"], 160)
        self.assertIn("AI Second Brain", fields["jetpack_seo_html_title"])
        self.assertFalse(proposed["post_title_change"])

    def test_link_patches_only_wrap_existing_copy(self):
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
            self.assertNotIn(patch["source_id"], source_ids)
            source_ids.add(patch["source_id"])

        self.assertEqual({9774, 12327}, source_ids)

    def test_future_write_boundaries_are_explicit(self):
        boundary = self.data["future_write_boundary_if_separately_approved"]

        self.assertEqual(["meta"], boundary["target_allowed_rest_top_level_keys"])
        self.assertEqual(
            {"jetpack_seo_html_title", "advanced_seo_description"},
            set(boundary["target_allowed_meta_keys"]),
        )
        self.assertEqual(
            ["content"],
            boundary["source_allowed_rest_top_level_keys"],
        )
        self.assertTrue(
            {
                "title",
                "slug",
                "status",
                "date",
                "categories",
                "tags",
                "excerpt",
            }.issubset(boundary["forbidden_rest_top_level_keys"])
        )
        self.assertIn(
            "no REST metadata write while the two Jetpack fields are unregistered",
            boundary["requires"],
        )
        self.assertFalse(self.data["live_wordpress_write_performed"])

    def test_handoff_keeps_production_and_secrets_out_of_scope(self):
        text = HANDOFF.read_text(encoding="utf-8")
        normalized_text = " ".join(text.split())
        self.assertIn("no live WordPress write", text)
        self.assertIn("Do not apply this handoff from the worker lane.", text)
        self.assertIn(
            "must not attempt a generic REST meta write",
            normalized_text,
        )

        serialized = json.dumps(self.data).lower()
        for marker in (
            "authorization",
            "bearer ",
            "wp_app_password",
            "wp_user",
            "oauth",
        ):
            self.assertNotIn(marker, serialized)

    def test_next_digest_has_a_measurable_wait_and_signal(self):
        verification = self.data["next_digest"]

        self.assertEqual(14, verification["earliest_full_days_after_live_change"])
        self.assertEqual(self.data["evidence"]["query"]["text"], verification["query"])
        self.assertEqual(self.data["target"]["url"], verification["landing_page"])
        self.assertEqual(
            {
                "page_average_position_below": 10.0,
                "page_ctr_percent_above": 1.2,
                "query_average_position_below": 15.0,
            },
            verification["success_signal"],
        )


if __name__ == "__main__":
    unittest.main()
