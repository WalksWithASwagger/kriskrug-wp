import json
import unittest
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "fixes/issue-340-legacy-bcai-links-handoff-2026-07-13.json"
HANDOFF = ROOT / "fixes/issue-340-legacy-bcai-links-handoff-2026-07-13.md"


def canonical_key(url: str) -> str:
    parts = urlsplit(url)
    path = parts.path.rstrip("/")
    return f"{parts.scheme}://{parts.netloc}{path}"


class Issue340LegacyBcaiLinksHandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_inventory_and_link_counts_are_complete(self):
        summary = self.data["summary"]
        sources = self.data["sources"]
        replacements = sum(
            patch["expected_old_href_count"]
            for source in sources
            for patch in source["link_patches"]
        )
        unresolved = sum(
            link["expected_href_count"]
            for source in sources
            for link in source["unresolved_links"]
        )

        self.assertEqual(13, summary["source_post_count"])
        self.assertEqual(41, summary["legacy_link_count"])
        self.assertEqual(30, summary["approved_replacement_count"])
        self.assertEqual(11, summary["unresolved_link_count"])
        self.assertEqual(summary["source_post_count"], len(sources))
        self.assertEqual(summary["approved_replacement_count"], replacements)
        self.assertEqual(summary["unresolved_link_count"], unresolved)
        self.assertEqual(summary["legacy_link_count"], replacements + unresolved)

    def test_every_source_has_stable_public_guards(self):
        expected_ids = {
            11620,
            11252,
            11171,
            9549,
            9374,
            9197,
            9044,
            8947,
            8859,
            8663,
            8508,
            8418,
            8314,
        }
        sources = self.data["sources"]

        self.assertEqual(expected_ids, {source["id"] for source in sources})
        for source in sources:
            self.assertEqual("publish", source["status"])
            self.assertTrue(source["slug"])
            self.assertTrue(source["modified"])
            self.assertTrue(source["url"].startswith("https://kriskrug.co/"))
            self.assertTrue(source["link_patches"])

    def test_only_approved_href_mappings_can_be_applied(self):
        mappings = {
            mapping["old_href"]: mapping["new_href"]
            for mapping in self.data["approved_mappings"]
        }
        targets = {canonical_key(target["url"]) for target in self.data["canonical_targets"]}

        for source in self.data["sources"]:
            for patch in source["link_patches"]:
                self.assertEqual(mappings[patch["old_href"]], patch["new_href"])
                self.assertIn(canonical_key(patch["new_href"]), targets)
                self.assertGreater(patch["expected_old_href_count"], 0)
                self.assertEqual(0, patch["expected_new_href_count_before"])
                self.assertTrue(patch["anchor_texts"])
                self.assertFalse(patch["copy_change"])

    def test_canonical_targets_are_indexable_and_in_the_sitemap(self):
        expected_targets = {
            canonical_key("https://bc-ai.ca/"),
            canonical_key("https://bc-ai.ca/communities/vancouver-ai"),
            canonical_key("https://bc-ai.ca/communities/futures-lab"),
            canonical_key("https://bc-ai.ca/communities/surrey"),
            canonical_key("https://bc-ai.ca/communities/mac"),
        }
        targets = self.data["canonical_targets"]

        self.assertEqual(expected_targets, {canonical_key(target["url"]) for target in targets})
        for target in targets:
            self.assertEqual(200, target["status"])
            self.assertTrue(target["indexable"])
            self.assertEqual(1, target["sitemap_count"])
            self.assertEqual(canonical_key(target["url"]), canonical_key(target["canonical"]))

    def test_ambiguous_hackathon_and_squamish_links_stay_unresolved(self):
        unresolved = [
            link
            for source in self.data["sources"]
            for link in source["unresolved_links"]
        ]
        approved_old_hrefs = {
            mapping["old_href"] for mapping in self.data["approved_mappings"]
        }

        self.assertEqual(11, sum(link["expected_href_count"] for link in unresolved))
        for link in unresolved:
            self.assertNotIn(link["href"], approved_old_hrefs)
            self.assertRegex(link["href"], r"(?:hackathon|squamish)\.bc-ai\.net")
            self.assertEqual("no_truthful_indexed_successor", link["reason"])

    def test_measurement_baseline_is_aggregate_and_page_paired(self):
        baseline = self.data["measurement_baseline"]

        self.assertEqual("bc ai", baseline["query"])
        self.assertEqual(
            "https://kriskrug.co/2025/02/16/"
            "bcs-ai-ecosystem-a-mycelial-network-of-creation/",
            baseline["landing_page"],
        )
        self.assertEqual(
            {"clicks": 0, "impressions": 49, "ctr_percent": 0.0, "average_position": 8.73},
            baseline["current"],
        )
        self.assertEqual(50, baseline["prior"]["impressions"])
        self.assertEqual(9.2, baseline["prior"]["average_position"])

    def test_future_write_boundary_is_body_only_and_review_gated(self):
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
                "featured_media",
            },
            set(boundary["forbidden_rest_top_level_keys"]),
        )
        self.assertFalse(self.data["live_wordpress_write_performed"])

        text = HANDOFF.read_text(encoding="utf-8")
        self.assertIn("no live WordPress write", text)
        self.assertIn("Do not apply these patches from this PR.", text)
        self.assertIn("exact action-time approval", text)
        self.assertIn("Nine historical Data Storytelling Hackathon links remain unchanged", text)
        self.assertIn("Two Squamish AI links remain unchanged", text)

    def test_manifest_contains_no_secret_material(self):
        serialized = json.dumps(self.data).lower()
        for marker in (
            "authorization",
            "bearer ",
            "wp_app_password",
            "wp_user",
            "client_secret",
            "refresh_token",
        ):
            self.assertNotIn(marker, serialized)


if __name__ == "__main__":
    unittest.main()
