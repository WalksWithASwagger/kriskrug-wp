import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "fixes/issue-284-topic-hub-links-handoff-2026-07-12.json"
HANDOFF = ROOT / "fixes/issue-284-topic-hub-links-handoff-2026-07-12.md"


class Issue284TopicHubLinksHandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.handoff = HANDOFF.read_text(encoding="utf-8")
        cls.sources = {source["id"]: source for source in cls.data["sources"]}

    def test_packet_is_repo_only_and_does_not_claim_live_results(self):
        self.assertEqual(284, self.data["issue"])
        self.assertEqual("repo-only-human-review-handoff", self.data["status"])
        self.assertTrue(self.data["observed"]["public_read_only"])
        self.assertFalse(self.data["observed"]["wordpress_write_performed"])
        self.assertFalse(self.data["claims"]["links_live_from_this_packet"])
        self.assertFalse(self.data["claims"]["ranking_lift_claimed"])
        self.assertIn("no live WordPress write", self.handoff)
        self.assertIn("does not make the links live", self.handoff)

    def test_target_identity_is_locked(self):
        expected = {
            "ai_ethics": (
                12318,
                "ai-ethics",
                "https://kriskrug.co/ai-ethics/",
                "2026-07-01T12:27:51",
            ),
            "ai_tools": (
                12321,
                "ai-tools",
                "https://kriskrug.co/ai-tools/",
                "2026-07-01T12:27:55",
            ),
            "indigenous_ai": (
                12322,
                "indigenous-ai",
                "https://kriskrug.co/indigenous-ai/",
                "2026-07-01T12:28:09",
            ),
        }

        self.assertEqual(set(expected), set(self.data["targets"]))
        for key, (target_id, slug, url, modified) in expected.items():
            target = self.data["targets"][key]
            self.assertEqual(target_id, target["id"])
            self.assertEqual(slug, target["slug"])
            self.assertEqual(url, target["url"])
            self.assertEqual(modified, target["modified"])
            self.assertEqual("publish", target["status"])
            self.assertEqual(200, target["public_http_status"])

    def test_source_identity_and_public_state_are_locked(self):
        expected = {
            5723: (
                "unpacking-ai-ethics-at-american-marketing-associationvisionconf2024",
                "2026-06-28T20:34:21",
            ),
            5489: (
                "cognitive-ai-creativity-and-ethics-w-professor-steve-dipaola",
                "2026-06-28T20:34:50",
            ),
            4635: (
                "bridging-innovation-and-ethics-future-proof-creatives-and-the-path-forward-in-ai",
                "2026-07-01T16:24:10",
            ),
            12030: (
                "canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one",
                "2026-06-28T14:14:24",
            ),
            12257: (
                "why-we-built-the-responsible-ai-professional-certification",
                "2026-06-28T20:25:58",
            ),
            4773: ("creative-toolbox", "2026-06-14T20:08:44"),
            3275: (
                "how-ai-tools-like-midjourney-dall%c2%b7e-chatgpt-are-reshaping-the-creative-landscape",
                "2026-06-14T20:34:30",
            ),
            2781: (
                "audio-deep-fakes-ai-chatbots-and-new-web-development-tools",
                "2026-06-28T20:39:27",
            ),
            12035: (
                "ai-wont-fix-your-broken-permit-process",
                "2026-07-01T16:24:28",
            ),
            7450: (
                "indigenomics-now-2024-redefining-the-future-of-indigenous-economic-and-digital-sovereignty-through-ai",
                "2026-06-28T20:31:08",
            ),
            11905: ("sovereign-ai-for-whom", "2026-07-01T16:24:30"),
        }

        self.assertEqual(set(expected), set(self.sources))
        for source_id, (slug, modified) in expected.items():
            source = self.sources[source_id]
            self.assertEqual(slug, source["slug"])
            self.assertEqual(modified, source["modified"])
            self.assertEqual("publish", source["status"])
            self.assertEqual(200, source["public_http_status"])
            self.assertEqual(
                {"ai_ethics", "ai_tools", "indigenous_ai"},
                set(source["target_href_counts"]),
            )
            self.assertGreaterEqual(source["total_anchor_count"], source["internal_link_count"])

    def test_url_manifest_matches_source_counts_and_target_urls(self):
        rows = self.data["before_after_url_manifest"]
        self.assertEqual(list(range(1, 16)), [row["map_order"] for row in rows])

        for row in rows:
            source = self.sources[row["source_id"]]
            target = self.data["targets"][row["target_key"]]
            self.assertEqual(source["url"], row["source_url"])
            self.assertEqual(target["url"], row["target_url"])
            self.assertEqual(
                source["target_href_counts"][row["target_key"]],
                row["before_target_href_count"],
            )
            self.assertIn(
                row["after_state"],
                {"unchanged-current-public-state", "proposed-not-live"},
            )
            if row["disposition"] == "already-linked-no-op":
                self.assertGreater(row["before_target_href_count"], 0)
                self.assertEqual(
                    row["before_target_href_count"],
                    row["proposed_after_target_href_count"],
                )
            elif row["after_state"] == "proposed-not-live":
                self.assertEqual(0, row["before_target_href_count"])
                self.assertEqual(1, row["proposed_after_target_href_count"])

    def test_review_ready_order_and_exact_anchor_wrappers_are_locked(self):
        writes = self.data["review_ready_source_writes"]
        self.assertEqual([1, 2, 3, 4], [write["priority"] for write in writes])
        self.assertEqual(
            [12035, 12257, 2781, 12030],
            [write["source_id"] for write in writes],
        )

        expected_patches = {
            "12035-ai-tools": ("https://kriskrug.co/ai-tools/", "AI tools"),
            "12257-ai-ethics": (
                "https://kriskrug.co/ai-ethics/",
                "ethical practice",
            ),
            "2781-ai-tools": (
                "https://kriskrug.co/ai-tools/",
                "the entire field of AI technology",
            ),
            "12030-ai-ethics": ("https://kriskrug.co/ai-ethics/", "AI ethics"),
            "12030-ai-tools": (
                "https://kriskrug.co/ai-tools/",
                "community-built tools",
            ),
        }
        found = {}

        for write in writes:
            source = self.sources[write["source_id"]]
            self.assertEqual(source["slug"], write["source_slug"])
            self.assertEqual(source["modified"], write["source_modified_guard"])
            self.assertTrue(write["publisher_review_required"])
            for patch in write["patches"]:
                found[patch["patch_id"]] = self._assert_copy_preserving_wrapper(patch)
                self.assertEqual(1, patch["expected_needle_count_before"])
                self.assertEqual(0, patch["inside_existing_anchor_count_before"])
                self.assertEqual(0, patch["expected_target_href_count_before"])
                self.assertEqual(1, patch["expected_target_href_count_after"])
                self.assertEqual(
                    patch["context_before"],
                    patch["context_after"].replace(
                        patch["replacement"],
                        patch["needle"],
                    ),
                )

        self.assertEqual(expected_patches, found)

    def test_repo_mirrors_contain_reviewed_needles_where_available(self):
        for write in self.data["review_ready_source_writes"]:
            source = self.sources[write["source_id"]]
            if source["repo_mirror"] is None:
                continue
            mirror = (ROOT / source["repo_mirror"]).read_text(encoding="utf-8")
            for patch in write["patches"]:
                self.assertEqual(1, mirror.count(patch["needle"]))

    def test_every_indigenous_row_is_human_review_required(self):
        queue = self.data["indigenous_ai_review_queue"]
        self.assertEqual(5, len(queue))
        self.assertEqual([1, 2, 3, 4, 5], [item["priority_after_human_approval"] for item in queue])

        for item in queue:
            self.assertTrue(item["human_review_required"])
            self.assertIn("human-review-required", item["status"])
            self.assertTrue(item["editorial_context"])
            self.assertTrue(item["human_decision_required"])
            self.assertEqual(
                self.sources[item["source_id"]]["slug"],
                item["source_slug"],
            )
            if item["patch"] is None:
                self.assertEqual(1, item["expected_target_href_count_before"])
                self.assertEqual(1, item["proposed_target_href_count_after"])
            else:
                href, text = self._assert_copy_preserving_wrapper(item["patch"])
                self.assertEqual("https://kriskrug.co/indigenous-ai/", href)
                self.assertEqual(item["patch"]["needle"], text)
                self.assertEqual(0, item["expected_target_href_count_before"])
                self.assertEqual(1, item["proposed_target_href_count_after"])

        indigenous_rows = [
            row
            for row in self.data["before_after_url_manifest"]
            if row["target_key"] == "indigenous_ai"
        ]
        self.assertEqual(5, len(indigenous_rows))
        self.assertTrue(
            all("human-review-required" in row["disposition"] for row in indigenous_rows)
        )
        self.assertGreaterEqual(self.handoff.count("HUMAN REVIEW REQUIRED"), 5)

    def test_future_rest_boundary_is_content_only(self):
        boundary = self.data["future_write_boundary_if_separately_approved"]
        self.assertFalse(boundary["live_write_approved_by_this_packet"])
        self.assertEqual(["content"], boundary["allowed_rest_top_level_keys"])
        self.assertEqual(
            {
                "title",
                "slug",
                "status",
                "date",
                "date_gmt",
                "categories",
                "tags",
                "meta",
                "excerpt",
                "author",
                "featured_media",
                "comment_status",
                "ping_status",
                "template",
                "format",
                "sticky",
                "password",
            },
            set(boundary["forbidden_rest_top_level_keys"]),
        )
        self.assertTrue(boundary["one_source_write_at_a_time"])
        self.assertTrue(boundary["indigenous_ai_requires_separate_per_patch_approval"])
        self.assertEqual(
            [12035, 12257, 2781, 12030],
            boundary["deterministic_source_write_order"],
        )

    def test_snapshot_stale_readback_rollback_and_smoke_gates_are_present(self):
        boundary = self.data["future_write_boundary_if_separately_approved"]
        self.assertEqual(
            {
                "source_identity",
                "target_identity",
                "per_source_snapshot",
                "modified_date_stale_guard",
                "exact_needle_and_href_counts",
                "body_only_payload",
                "one_write_at_a_time",
                "authenticated_readback",
                "public_source_and_target_smoke",
                "rollback_ready",
            },
            set(boundary["verification_gates"]),
        )
        self.assertIn("before-edit.json", boundary["required_snapshot_files_per_source"])
        self.assertIn(
            "before-content.raw.html",
            boundary["required_snapshot_files_per_source"],
        )
        self.assertIn(
            "rollback-content-only.json",
            boundary["required_snapshot_files_per_source"],
        )
        self.assertTrue(
            any("modified" in guard for guard in boundary["stale_guards"])
        )
        self.assertTrue(
            any("content.raw" in check for check in boundary["readback_after_each_write"])
        )
        self.assertTrue(
            any("before-content.raw.html" in step for step in boundary["rollback"])
        )
        self.assertTrue(
            any("homepage and blog" in check for check in boundary["final_smoke_checks"])
        )

    def test_packet_contains_no_secret_material(self):
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

    def _assert_copy_preserving_wrapper(self, patch):
        self.assertEqual("wrap_exact_text", patch["operation"])
        self.assertFalse(patch["copy_change"])
        match = re.fullmatch(
            r'<a href="([^"]+)">([^<]+)</a>',
            patch["replacement"],
        )
        self.assertIsNotNone(match)
        self.assertEqual(patch["needle"], match.group(2))
        target = self.data["targets"][patch["target_key"]]
        self.assertEqual(target["url"], match.group(1))
        return match.group(1), match.group(2)


if __name__ == "__main__":
    unittest.main()
