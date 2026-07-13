import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "fixes/issue-335-lotr-drinking-game-seo-handoff-2026-07-13.json"
HANDOFF = ROOT / "fixes/issue-335-lotr-drinking-game-seo-handoff-2026-07-13.md"


class Issue335LotrSeoHandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_digest_safe_evidence_is_exact(self):
        evidence = self.data["evidence"]

        self.assertEqual(
            {"start": "2026-07-04", "end": "2026-07-10"},
            evidence["current_window"],
        )
        self.assertEqual(
            {
                "impressions": 47,
                "clicks": 0,
                "ctr_percent": 0.0,
                "average_position": 10.43,
            },
            evidence["page"]["current"],
        )
        self.assertEqual("lord of the rings drinking game", evidence["query"]["text"])
        self.assertEqual(27, evidence["query"]["current"]["impressions"])
        self.assertEqual(0, evidence["query"]["current"]["clicks"])
        self.assertEqual(9.96, evidence["query"]["current"]["average_position"])

    def test_target_identity_and_public_state_are_locked(self):
        target = self.data["target"]
        public = self.data["current_public_metadata"]

        self.assertEqual(35, target["id"])
        self.assertEqual("publish", target["status"])
        self.assertEqual(
            target["url"],
            f"https://kriskrug.co/2004/05/27/{target['slug']}/",
        )
        self.assertEqual(target["url"], public["canonical"])
        self.assertEqual(200, public["http_status"])
        self.assertEqual(1, public["h1_count"])
        self.assertFalse(public["standard_meta_description_present"])
        self.assertFalse(public["jetpack_seo_meta_fields_exposed"])
        self.assertEqual(["footnotes"], public["rest_meta_keys"])

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
        self.assertGreaterEqual(lengths["advanced_seo_description"], 140)
        self.assertLessEqual(lengths["advanced_seo_description"], 160)
        self.assertIn(
            "The Lord of the Rings Drinking Game",
            fields["jetpack_seo_html_title"],
        )
        self.assertIn("Play responsibly.", fields["advanced_seo_description"])
        self.assertFalse(proposed["post_title_change"])
        self.assertFalse(proposed["excerpt_change"])

    def test_related_link_pair_is_relevant_and_not_claimed_write_ready(self):
        review = self.data["related_link_review"]
        patches = self.data["link_patches"]

        self.assertEqual(58, review["selected_related_post"]["id"])
        self.assertIn("Elvish or Yiddish", review["selected_related_post"]["relevance"])
        self.assertEqual(5236, review["rejected_candidate"]["id"])
        self.assertEqual(
            {"inbound_to_target", "outbound_from_target"},
            {patch["direction"] for patch in patches},
        )
        self.assertEqual({35, 58}, {patch["source_id"] for patch in patches})
        for patch in patches:
            self.assertFalse(patch["exact_raw_patch_ready"])
            self.assertTrue(patch["human_review_required"])
            self.assertEqual(1, patch["expected_current_related_href_count"])
            self.assertEqual(0, patch["expected_proposed_href_count_before"])

    def test_future_write_boundaries_are_explicit(self):
        boundary = self.data["future_write_boundary_if_separately_approved"]

        self.assertEqual(["content"], boundary["content_allowed_top_level_keys"])
        self.assertEqual(
            {"jetpack_seo_html_title", "advanced_seo_description"},
            set(boundary["metadata_allowed_fields"]),
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
                "meta",
            }.issubset(boundary["forbidden_rest_top_level_keys"])
        )
        self.assertFalse(self.data["live_wordpress_write_performed"])

    def test_handoff_keeps_production_and_secrets_out_of_scope(self):
        text = HANDOFF.read_text(encoding="utf-8")
        normalized_text = " ".join(text.split())

        self.assertIn("no live WordPress write", text)
        self.assertIn("Do not apply this handoff from the worker lane.", text)
        self.assertIn(
            "must not attempt a generic REST metadata write",
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
        self.assertEqual(28, verification["secondary_review_days_after_live_change"])
        self.assertEqual(self.data["evidence"]["query"]["text"], verification["query"])
        self.assertEqual(self.data["target"]["url"], verification["landing_page"])
        self.assertEqual(1, verification["success_signal"]["page_clicks_at_least"])
        self.assertEqual(1, verification["success_signal"]["query_clicks_at_least"])


if __name__ == "__main__":
    unittest.main()
