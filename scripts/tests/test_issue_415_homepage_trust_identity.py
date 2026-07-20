import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
THEME_FUNCTIONS = ROOT / "theme/kk-aurora/functions.php"
FRONT_PAGE = ROOT / "theme/kk-aurora/templates/front-page.html"
SCHEMA_SOURCE = ROOT / "fixes/schema-snippets-deployed.php"
SITE_NAME = "Kris Krug"
STALE_IDENTITY = "Generative AI Tools & Techniques"
HOME_DESCRIPTION = (
    "Kris Krug is a Vancouver AI keynote speaker, creative technologist, and "
    "community builder leading BC + AI and curating Futureproof Festival."
)


class Issue415HomepageTrustIdentityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.theme = THEME_FUNCTIONS.read_text(encoding="utf-8")
        cls.schema = SCHEMA_SOURCE.read_text(encoding="utf-8")

    @staticmethod
    def _function_block(source: str, name: str, next_name: str) -> str:
        pattern = rf"function {re.escape(name)}\(.*?(?=function {re.escape(next_name)}\()"
        match = re.search(pattern, source, re.DOTALL)
        if match is None:
            raise AssertionError(f"missing function block: {name}")
        return match.group(0)

    @staticmethod
    def _scalar_constant(source: str, key: str) -> str:
        match = re.search(rf"'{re.escape(key)}'\s*=>\s*'([^']*)'", source)
        if match is None:
            raise AssertionError(f"missing schema constant: {key}")
        return match.group(1)

    def test_homepage_metadata_uses_a_useful_fallback(self):
        public_description = self._function_block(
            self.theme,
            "public_meta_description",
            "writing_archive_canonical_url",
        )

        self.assertIn(f"return '{HOME_DESCRIPTION}';", self.theme)
        self.assertIn("homepage_meta_description()", public_description)
        self.assertRegex(
            public_description,
            re.compile(
                r"advanced_seo_front_page_description.*?trim\(\$description\).*?homepage_meta_description\(\)",
                re.DOTALL,
            ),
        )
        self.assertGreaterEqual(len(HOME_DESCRIPTION), 120)
        self.assertLessEqual(len(HOME_DESCRIPTION), 160)

    def test_social_and_feed_metadata_use_the_current_site_identity(self):
        social = self._function_block(
            self.theme,
            "social_meta_tags",
            "render_social_meta_tags",
        )

        self.assertIn(f"return '{SITE_NAME}';", self.theme)
        self.assertIn("'og:site_name'   => public_site_name()", social)
        self.assertNotIn("get_bloginfo('name')", social)
        self.assertIn("function filter_feed_bloginfo", self.theme)
        self.assertIn("function filter_feed_title", self.theme)
        self.assertIn("add_filter('get_bloginfo_rss'", self.theme)
        self.assertIn("add_filter('get_wp_title_rss'", self.theme)
        self.assertNotIn(STALE_IDENTITY, social)

    def test_homepage_removes_unverified_quotes_and_routes_to_real_work(self):
        source = FRONT_PAGE.read_text(encoding="utf-8")

        for placeholder in (
            "Fresh proof belongs here before launch",
            "replace with verified",
            "Event organizer quote",
            "Workshop host quote",
            "Leadership audience quote",
        ):
            self.assertNotIn(placeholder, source)
        self.assertNotIn("<blockquote", source)
        self.assertNotIn("aurora-testimonial-band", source)
        self.assertIn('id="aurora-relationships-title"', source)
        self.assertIn('href="/work/"', source)
        self.assertIn('href="https://bc-ai.ca/"', source)
        self.assertIn('href="https://www.futureproof.website/"', source)
        self.assertNotIn('href="https://futureproof.website/"', source)

    def test_rendered_schema_source_names_kris_and_his_current_projects(self):
        self.assertEqual(SITE_NAME, self._scalar_constant(self.schema, "site_name"))
        alternate_names = re.search(
            r"'site_alternate_names'\s*=>\s*array\((.*?)\),",
            self.schema,
            re.DOTALL,
        )
        self.assertIsNotNone(alternate_names)
        self.assertEqual(
            ["Kris Krüg", "kriskrug.co"],
            re.findall(r"'([^']*)'", alternate_names.group(1)),
        )
        relationships = dict(
            re.findall(
                r"array\('name'\s*=>\s*'([^']+)',\s*'url'\s*=>\s*'([^']+)'\)",
                self.schema,
            )
        )
        self.assertEqual(
            {
                "BC + AI Ecosystem Industry Association": "https://bc-ai.ca/",
                "Vancouver AI": "https://vancouver.ai/",
                "Futureproof Festival": "https://futureproof.website/",
            },
            relationships,
        )
        self.assertNotIn(STALE_IDENTITY, self.schema)


if __name__ == "__main__":
    unittest.main()
