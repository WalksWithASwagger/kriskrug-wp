import hashlib
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "fixes/issue-249-you-cant-drink-data-seo-handoff-2026-07-12.json"
HANDOFF = ROOT / "fixes/issue-249-you-cant-drink-data-seo-handoff-2026-07-12.md"


class Issue249SeoHandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_issue_baseline_is_exact_and_digest_safe(self):
        baseline = self.data["baseline"]
        page = baseline["landing_page"]
        query = baseline["normalized_query_cluster"]

        self.assertEqual(249, self.data["issue"])
        self.assertEqual(
            {"start": "2026-06-12", "end": "2026-07-09", "days": 28},
            baseline["window"],
        )
        self.assertEqual(
            {"impressions": 294, "clicks": 6, "ctr_percent": 2.04, "average_position": 7.96},
            {key: page[key] for key in ("impressions", "clicks", "ctr_percent", "average_position")},
        )
        self.assertEqual("you cant drink data", query["query"])
        self.assertTrue(query["impressions_present"])
        self.assertEqual(0, query["clicks"])
        self.assertEqual({"min": 8.4, "max": 8.7}, query["average_position_range"])
        self.assertFalse(self.data["evidence"]["private_analytics_export_included"])

    def test_target_and_source_identity_guards_are_stable(self):
        target = self.data["target"]
        source = self.data["source_selection"]["selected"]
        stale_guard = self.data["future_publisher_gate"]["stale_guard"]

        self.assertEqual(11936, target["id"])
        self.assertEqual("you-cant-drink-data", target["slug"])
        self.assertEqual("publish", target["status"])
        self.assertEqual("2026-06-28T18:40:25", target["modified"])
        self.assertEqual(target["url"], target["canonical"])

        self.assertEqual(1208, source["id"])
        self.assertEqual("about", source["slug"])
        self.assertEqual("publish", source["status"])
        self.assertEqual("2026-07-01T11:33:51", source["modified"])
        self.assertEqual(source["url"], source["canonical"])
        self.assertEqual(
            {key: source[key] for key in ("id", "slug", "status", "modified")},
            stale_guard["expected_identity"],
        )
        self.assertTrue(stale_guard["stop_if_any_guard_differs"])

    def test_selected_source_payload_and_marker_have_not_drifted(self):
        source = self.data["source_selection"]["selected"]
        payload_path = ROOT / source["repo_payload"]
        payload = payload_path.read_text(encoding="utf-8")
        digest = hashlib.sha256(payload_path.read_bytes()).hexdigest()

        self.assertEqual(source["repo_payload_sha256"], digest)
        self.assertEqual(1, payload.count(source["content_marker"]))
        self.assertEqual(
            self.data["link_proposal"]["expected_current_paragraph_count"],
            payload.count(self.data["link_proposal"]["current_paragraph_html"]),
        )
        self.assertEqual(0, payload.lower().count("you can't drink data"))
        self.assertEqual(0, payload.count(self.data["target"]["url"]))

    def test_sentence_proposal_adds_one_contextual_internal_link(self):
        proposal = self.data["link_proposal"]
        current = proposal["current_paragraph_html"]
        replacement = proposal["replacement_paragraph_html"]
        sentence = proposal["added_sentence_html"]
        anchor_match = re.fullmatch(
            r'.*<a href="([^"]+)">([^<]+)</a>\.',
            sentence,
        )

        self.assertFalse(proposal["phrase_present_before"])
        self.assertIsNotNone(anchor_match)
        self.assertEqual(self.data["target"]["url"], anchor_match.group(1))
        self.assertEqual("you can't drink data", anchor_match.group(2))
        self.assertEqual(current[:-4] + " " + sentence + "</p>", replacement)
        self.assertEqual(1, replacement.count("<a "))
        self.assertEqual(1, proposal["sentences_added"])
        self.assertEqual(1, proposal["expected_anchor_count_after"])
        self.assertEqual(1, proposal["expected_target_href_count_after"])
        self.assertNotIn("target=", sentence)
        self.assertNotIn("rel=", sentence)

    def test_future_write_and_rollback_are_body_only(self):
        gate = self.data["future_publisher_gate"]
        write = gate["write"]
        rollback = gate["rollback"]
        snapshot = gate["snapshot"]

        self.assertEqual(["content"], write["allowed_rest_top_level_keys"])
        self.assertEqual(["content"], rollback["allowed_rest_top_level_keys"])
        self.assertTrue(write["requires_human_review_of_exact_diff"])
        self.assertTrue(snapshot["required_before_write"])
        self.assertEqual(
            {"id", "slug", "status", "modified", "content.raw"},
            set(snapshot["required_edit_snapshot_fields"]),
        )
        self.assertTrue(
            {"title", "slug", "status", "date", "author", "excerpt", "featured_media", "meta"}
            <= set(write["forbidden_rest_top_level_keys"])
        )
        self.assertFalse(self.data["scope"]["live_wordpress_write_performed"])
        self.assertFalse(self.data["scope"]["publish_or_deploy_performed"])

    def test_handoff_contains_no_credentials_or_live_action_claim(self):
        artifacts = json.dumps(self.data) + HANDOFF.read_text(encoding="utf-8")
        lowered = artifacts.lower()

        for marker in (
            "authorization:",
            "bearer ",
            "wp_app_password",
            "wp_user",
            "client_secret",
            "access_token",
            "refresh_token",
            "application password",
        ):
            self.assertNotIn(marker, lowered)

        self.assertIn("no live WordPress write", artifacts)
        self.assertIn("Do not apply this proposal from this PR.", artifacts)
        self.assertIn("Refs #249", artifacts)
        self.assertIsNone(re.search(r"(?m)^(?:Closes|Fixes) #249\b", artifacts))

    def test_next_digest_gate_and_success_signal_are_measurable(self):
        verification = self.data["next_digest"]
        gate = verification["measurement_gate"]
        signal = verification["positive_signal"]

        self.assertEqual(7, gate["minimum_full_days_after_verified_live_edit"])
        self.assertTrue(gate["requires_recorded_live_edit_timestamp"])
        self.assertTrue(gate["requires_public_link_readback"])
        self.assertEqual(self.data["target"]["url"], verification["landing_page"])
        self.assertEqual(
            {"impressions", "clicks", "ctr_percent", "average_position"},
            set(verification["required_metrics"]),
        )
        self.assertTrue(verification["comparison"]["preserve_28_day_window_length"])
        self.assertEqual(1, signal["query_cluster_clicks_at_least"])
        self.assertEqual(8.4, signal["query_cluster_average_position_below"])
        self.assertTrue(self.data["github_handoff"]["issue_remains_open"])


if __name__ == "__main__":
    unittest.main()
