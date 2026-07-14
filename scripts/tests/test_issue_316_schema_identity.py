import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEPLOYED = ROOT / "fixes/schema-snippets-deployed.php"
MU_PLUGIN = ROOT / "fixes/schema-snippets.php"
MANIFEST = ROOT / "fixes/issue-316-schema-identity-handoff-2026-07-13.json"
HANDOFF = ROOT / "fixes/issue-316-schema-identity-handoff-2026-07-13.md"


def scalar_constant(source: str, key: str) -> str:
    match = re.search(rf"'{re.escape(key)}'\s*=>\s*'([^']*)'", source)
    if match is None:
        raise AssertionError(f"missing scalar schema constant: {key}")
    return match.group(1)


def array_constant(source: str, key: str) -> list[str]:
    match = re.search(
        rf"'{re.escape(key)}'\s*=>\s*array\((.*?)\),",
        source,
        re.DOTALL,
    )
    if match is None:
        raise AssertionError(f"missing array schema constant: {key}")
    return re.findall(r"'([^']*)'", match.group(1))


class Issue316SchemaIdentityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.deployed = DEPLOYED.read_text(encoding="utf-8")
        cls.mu_plugin = MU_PLUGIN.read_text(encoding="utf-8")

    def test_live_before_evidence_is_exact(self):
        live = self.data["live_before"]

        self.assertEqual("2026-07-13", live["observed_on"])
        self.assertEqual(
            "Kris Krug | AI Keynote Speaker & Creative Technologist",
            live["homepage_document_title"],
        )
        self.assertEqual(
            "Kris Krüg | Generative AI Tools & Techniques",
            live["website_schema_name"],
        )
        self.assertEqual(
            "Generative AI Strategist, Photographer, Community Builder",
            live["person_job_title"],
        )
        self.assertFalse(live["person_image_present"])
        self.assertEqual(3, len(live["sample_urls"]))
        self.assertTrue(all(row["http_status"] == 200 for row in live["sample_urls"]))

    def test_concise_site_name_and_alternatives_follow_google_guidance(self):
        proposed = self.data["proposed_identity"]

        self.assertEqual("Kris Krug", proposed["website_name"])
        self.assertEqual(
            ["Kris Krüg", "kriskrug.co"],
            proposed["website_alternate_names"],
        )
        self.assertNotIn("|", proposed["website_name"])
        self.assertEqual(
            "https://developers.google.com/search/docs/appearance/site-names",
            self.data["guidance"]["google_site_names"],
        )

    def test_both_schema_sources_share_the_reviewed_identity(self):
        expected = self.data["proposed_identity"]

        for source in (self.deployed, self.mu_plugin):
            self.assertEqual(expected["website_name"], scalar_constant(source, "site_name"))
            self.assertEqual(
                expected["website_alternate_names"],
                array_constant(source, "site_alternate_names"),
            )
            self.assertEqual(expected["person_image"], scalar_constant(source, "person_image"))
            self.assertEqual(expected["person_job"], scalar_constant(source, "person_job"))
            self.assertEqual(
                expected["person_description"],
                scalar_constant(source, "person_descr"),
            )
            self.assertRegex(
                source,
                r"'alternateName'\s*=>\s*\$c\['site_alternate_names'\]",
            )
            self.assertNotIn("Generative AI Tools & Techniques", source)

    def test_person_image_is_an_existing_public_about_portrait(self):
        image = self.data["person_image_evidence"]

        self.assertEqual(self.data["proposed_identity"]["person_image"], image["url"])
        self.assertEqual("https://kriskrug.co/about/", image["observed_on_page"])
        self.assertEqual("Portrait of Kris Krug", image["public_alt_text"])
        self.assertEqual(200, image["http_status"])
        self.assertEqual("image/jpeg", image["content_type"])
        self.assertGreater(image["content_length_bytes"], 100_000)

    def test_worker_lane_is_repo_only_and_deployment_is_guarded(self):
        deployment = self.data["future_code_snippets_update_if_separately_approved"]

        self.assertFalse(self.data["live_wordpress_write_performed"])
        self.assertEqual(5, deployment["expected_snippet_id"])
        self.assertEqual("KK Schema", deployment["proposed_snippet_name"])
        self.assertIn("fresh wp-admin ID and scope verification", deployment["requires"])
        self.assertIn("full current snippet rollback snapshot", deployment["requires"])
        self.assertIn("one active Person owner", deployment["post_deploy_invariants"])
        self.assertIn("one homepage WebSite owner", deployment["post_deploy_invariants"])

        text = HANDOFF.read_text(encoding="utf-8")
        self.assertIn("no live WordPress write", text)
        self.assertIn("Do not apply this handoff from the worker lane.", text)
        self.assertIn("Open Graph site-name mismatch", text)

    def test_post_deploy_eval_has_routes_and_rollback(self):
        evaluation = self.data["post_deploy_evaluation"]

        self.assertEqual(5, len(evaluation["sample_urls"]))
        self.assertIn("schema_markup_validator", evaluation["checks"])
        self.assertIn("anonymous_cache_busted_html", evaluation["checks"])
        self.assertIn("restore the full captured snippet", evaluation["rollback"])
        self.assertIn("purge only the affected cache surface", evaluation["rollback"])

    def test_packet_contains_no_secret_material(self):
        serialized = json.dumps(self.data).lower()
        for marker in (
            "authorization",
            "bearer ",
            "wp_app_password",
            "wp_user",
            "oauth",
        ):
            self.assertNotIn(marker, serialized)


if __name__ == "__main__":
    unittest.main()
