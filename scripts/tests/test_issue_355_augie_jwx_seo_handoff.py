import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "fixes/issue-355-augie-jwx-seo-handoff-2026-07-13.json"
HANDOFF = ROOT / "fixes/issue-355-augie-jwx-seo-handoff-2026-07-13.md"


class Issue355AugieJwxSeoHandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.handoff = HANDOFF.read_text(encoding="utf-8")

    def test_digest_safe_evidence_is_exact(self):
        evidence = self.data["evidence"]

        self.assertEqual("2026-06-12", evidence["window_start"])
        self.assertEqual("2026-07-09", evidence["window_end"])
        self.assertFalse(evidence["private_analytics_export_included"])
        self.assertEqual(
            {
                "impressions": 186,
                "clicks": 0,
                "ctr_percent": 0.0,
                "average_position": 11.62,
            },
            evidence["landing_page"],
        )
        self.assertEqual(
            [
                {
                    "text": "augie ai",
                    "impressions": 45,
                    "clicks": 0,
                    "ctr_percent": 0.0,
                    "average_position": 12.73,
                },
                {
                    "text": "augie studio",
                    "impressions": 32,
                    "clicks": 0,
                    "ctr_percent": 0.0,
                    "average_position": 17.19,
                },
            ],
            evidence["queries"],
        )

    def test_target_identity_and_public_state_are_locked(self):
        target = self.data["target"]
        public = self.data["current_public_metadata"]

        self.assertEqual(6019, target["id"])
        self.assertEqual("publish", target["status"])
        self.assertEqual("2026-06-14T20:11:57", target["modified"])
        self.assertEqual(
            target["url"],
            f"https://kriskrug.co/2024/06/18/{target['slug']}/",
        )
        self.assertEqual(target["url"], public["canonical"])
        self.assertEqual(200, public["http_status"])
        self.assertEqual(1, public["h1_count"])
        self.assertTrue(public["indexable"])
        self.assertFalse(public["standard_meta_description_present"])
        self.assertEqual(["footnotes"], public["public_rest_meta_keys"])
        self.assertFalse(public["jetpack_seo_meta_fields_exposed"])

    def test_first_party_sources_and_claims_are_narrow(self):
        sources = self.data["first_party_sources"]

        self.assertEqual(
            {
                "https://jwx.com/news/jwx-augie-acquisition",
                "https://jwx.com/jwx-studio",
                "https://my.augie.studio/",
            },
            {source["url"] for source in sources.values()},
        )
        self.assertTrue(all(source["http_status"] == 200 for source in sources.values()))
        self.assertEqual("2026-01-15", sources["acquisition"]["published_on"])

        claims = " ".join(
            claim
            for source in sources.values()
            for claim in source["confirmed_facts"]
        ).lower()
        for phrase in (
            "acquired aug x labs",
            "sunset its direct-to-consumer product",
            "publishers and media enterprises",
            "consumer product is no longer offered",
        ):
            self.assertIn(phrase, claims)
        for forbidden in ("purchase price", "deal value", "millions", "guaranteed"):
            self.assertNotIn(forbidden, claims)

    def test_proposed_metadata_is_measured_and_within_limits(self):
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
        self.assertIn("Augie Studio", fields["jetpack_seo_html_title"])
        self.assertIn("AI", fields["jetpack_seo_html_title"])
        self.assertIn("JWX", fields["jetpack_seo_html_title"])
        self.assertFalse(proposed["post_title_change"])
        self.assertFalse(proposed["metadata_rest_write_allowed_while_fields_unregistered"])

    def test_body_change_is_one_guarded_insertion(self):
        insertion = self.data["body_insertion"]

        self.assertEqual("insert_before_exact_html", insertion["operation"])
        self.assertEqual(1, insertion["expected_needle_count_before"])
        self.assertEqual(0, insertion["expected_update_note_count_before"])
        self.assertEqual(1, insertion["expected_update_note_count_after"])
        self.assertTrue(insertion["original_review_otherwise_byte_preserved"])
        self.assertEqual(
            insertion["note_html"] + insertion["separator"] + insertion["needle"],
            insertion["replacement"],
        )
        self.assertTrue(insertion["replacement"].endswith(insertion["needle"]))

        note = insertion["note_html"]
        for phrase in (
            "Update, July 2026:",
            "January 2026",
            "direct-to-consumer product",
            "publishers and media enterprises",
            "snapshot of the 2024 product",
        ):
            self.assertIn(phrase, note)

        links = dict(
            re.findall(r'<a href="([^"]+)">([^<]+)</a>', note)
        )
        self.assertEqual(
            {
                "https://jwx.com/news/jwx-augie-acquisition": "JWX acquired Aug X Labs",
                "https://jwx.com/jwx-studio": "JWX Studio",
            },
            links,
        )

    def test_future_write_boundary_is_content_only_and_reversible(self):
        boundary = self.data["future_write_boundary_if_separately_approved"]

        self.assertEqual(["content"], boundary["body_allowed_rest_top_level_keys"])
        self.assertFalse(boundary["metadata_rest_write_allowed"])
        self.assertEqual(
            {"jetpack_seo_html_title", "advanced_seo_description"},
            set(boundary["metadata_editor_fields"]),
        )
        self.assertTrue(
            {
                "title",
                "slug",
                "status",
                "date",
                "categories",
                "tags",
                "meta",
                "excerpt",
                "featured_media",
            }.issubset(boundary["forbidden_rest_top_level_keys"])
        )
        self.assertIn("before-post-6019-content.raw.html", boundary["snapshot"]["required_files"])
        self.assertIn("rollback-content-only.json", boundary["snapshot"]["required_files"])
        self.assertTrue(any("byte-preserved" in item for item in boundary["readback"]))
        self.assertTrue(any("later edit" in item for item in boundary["rollback"]))

    def test_handoff_keeps_live_actions_and_secrets_out_of_scope(self):
        normalized = " ".join(self.handoff.split())

        self.assertIn("no live WordPress write", self.handoff)
        self.assertIn("Do not apply this handoff from the worker lane.", self.handoff)
        self.assertIn("must not use a generic REST metadata write", normalized)
        self.assertFalse(self.data["live_wordpress_write_performed"])

        serialized = (json.dumps(self.data) + self.handoff).lower()
        for marker in (
            "authorization:",
            "bearer ",
            "wp_app_password",
            "wp_user",
            "client_secret",
            "oauth_token",
        ):
            self.assertNotIn(marker, serialized)

    def test_next_digest_has_14_and_28_day_measurements(self):
        verification = self.data["next_digest"]

        self.assertEqual(14, verification["earliest_full_days_after_live_change"])
        self.assertEqual(28, verification["second_measurement_full_days_after_live_change"])
        self.assertEqual(["augie ai", "augie studio"], verification["queries"])
        self.assertEqual(self.data["target"]["url"], verification["landing_page"])
        self.assertEqual(
            {
                "impressions",
                "clicks",
                "ctr_percent",
                "average_position",
            },
            set(verification["required_metrics"]),
        )


if __name__ == "__main__":
    unittest.main()
