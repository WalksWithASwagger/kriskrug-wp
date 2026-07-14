import html
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "fixes/issue-345-og-site-name-handoff-2026-07-13.json"
HANDOFF = ROOT / "fixes/issue-345-og-site-name-handoff-2026-07-13.md"
THEME_FUNCTIONS = ROOT / "theme/kk-aurora/functions.php"
OG_BRIDGE = ROOT / "fixes/og-restore-snippet.php"


class Issue345OpenGraphSiteNameTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.theme = THEME_FUNCTIONS.read_text(encoding="utf-8")
        cls.bridge = OG_BRIDGE.read_text(encoding="utf-8")
        cls.handoff = HANDOFF.read_text(encoding="utf-8")

    def test_live_wordpress_identity_and_owner_are_exact(self):
        live = self.data["live_before"]

        self.assertEqual("2026-07-13", live["observed_on"])
        self.assertEqual(200, live["public_rest_root"]["http_status"])
        self.assertEqual(
            "Kris Krüg | Generative AI Tools &amp; Techniques",
            live["public_rest_root"]["raw_name"],
        )
        self.assertEqual(
            "Kris Krüg | Generative AI Tools & Techniques",
            html.unescape(live["public_rest_root"]["raw_name"]),
        )
        self.assertEqual("1.3.37", live["active_aurora_version"])
        self.assertEqual(12, live["inactive_bridge_snippet_id"])
        self.assertEqual(
            "theme/kk-aurora/functions.php::render_social_meta_tags",
            live["active_social_metadata_owner"],
        )

    def test_route_matrix_proves_the_site_name_mismatch(self):
        routes = self.data["live_before"]["route_matrix"]

        self.assertEqual(5, len(routes))
        self.assertEqual(
            {"/", "/about/", "/speaking/", "/blog/", "/2026/01/24/both-hands-full/"},
            {route["path"] for route in routes},
        )
        for route in routes:
            self.assertEqual(200, route["normal_http_status"])
            self.assertEqual(200, route["cache_busted_http_status"])
            self.assertEqual(1, route["normal_og_site_name_count"])
            self.assertEqual(1, route["cache_busted_og_site_name_count"])
            self.assertEqual(
                "Kris Krüg | Generative AI Tools & Techniques",
                route["og_site_name"],
            )
            self.assertTrue(route["document_title"])

    def test_change_is_one_scoped_wordpress_option(self):
        change = self.data["proposed_change"]

        self.assertEqual("blogname", change["wordpress_option"])
        self.assertEqual("Kris Krug", change["target_value"])
        self.assertEqual(["wordpress_option:blogname"], change["allowed_writes"])
        self.assertFalse(change["repo_rendering_code_change_required"])
        self.assertFalse(self.data["live_wordpress_write_performed"])

    def test_repo_owners_derive_site_name_and_preserve_title_positioning(self):
        self.assertRegex(
            self.theme,
            re.compile(r"'og:site_name'\s*=>\s*get_bloginfo\('name'\)"),
        )
        self.assertRegex(
            self.bridge,
            re.compile(r"\$site\s*=\s*get_bloginfo\('name'\)"),
        )
        self.assertIn(
            "Kris Krug | AI Keynote Speaker & Creative Technologist",
            self.theme,
        )
        self.assertIn("Code Snippet 12 is inactive", self.handoff)
        self.assertIn("No live WordPress write was performed", self.handoff)

    def test_deployment_requires_approval_snapshot_and_public_readback(self):
        deployment = self.data["future_deployment_if_separately_approved"]

        self.assertIn("explicit approval of the exact blogname change", deployment["requires"])
        self.assertIn("fresh authenticated readback of the current blogname", deployment["requires"])
        self.assertIn("complete rollback snapshot of the current blogname", deployment["requires"])
        self.assertEqual(["set blogname to Kris Krug"], deployment["allowed_actions"])
        self.assertIn("restore the exact captured blogname", deployment["rollback"])
        self.assertIn("purge PressCACHE", deployment["rollback"])

    def test_post_deploy_eval_preserves_titles_and_one_metadata_owner(self):
        evaluation = self.data["post_deploy_evaluation"]

        self.assertEqual(5, len(evaluation["sample_urls"]))
        self.assertIn("public_rest_root", evaluation["checks"])
        self.assertIn("anonymous_cache_busted_html", evaluation["checks"])
        self.assertIn("crawler_user_agents", evaluation["checks"])
        self.assertIn("exactly one og:site_name with value Kris Krug", evaluation["expected"])
        self.assertIn("document titles remain unchanged", evaluation["expected"])
        self.assertIn("Aurora remains the only active social metadata owner", evaluation["expected"])

    def test_adjacent_defects_are_separately_tracked(self):
        adjacent = self.data["adjacent_findings"]

        self.assertEqual(346, adjacent["missing_homepage_og_title"]["issue"])
        self.assertEqual(347, adjacent["missing_blog_canonical"]["issue"])
        self.assertIn(316, self.data["out_of_scope_issue_numbers"])
        self.assertIn(346, self.data["out_of_scope_issue_numbers"])
        self.assertIn(347, self.data["out_of_scope_issue_numbers"])

    def test_packet_contains_no_secret_material(self):
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
