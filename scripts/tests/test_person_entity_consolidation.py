"""Render the canonical schema snippet and pin the cross-site Person entity.

bothhandsfull.com and darkcrystal.app point their Person nodes at
https://kriskrug.co/#person, so this snippet must keep emitting that @id with
the umlaut name, the linked BC + AI organization, and the verified sameAs set.
"""

import json
import re
import shutil
import subprocess
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_SOURCE = ROOT / "fixes/schema-snippets-deployed.php"
SCRIPT_PATTERN = re.compile(
    r'<script type="application/ld\+json">(.*?)</script>',
    re.DOTALL,
)
PERSON_ID = "https://kriskrug.co/#person"


def render_front_page_person_and_website() -> list[dict]:
    schema_path = json.dumps(str(SCHEMA_SOURCE))
    harness = textwrap.dedent(
        f"""
        <?php
        function add_action($hook, $callback, $priority = 10, $accepted_args = 1) {{}}
        function is_front_page() {{ return true; }}
        function is_home() {{ return false; }}
        function wp_json_encode($value, $flags = 0) {{
            return json_encode($value, $flags | JSON_THROW_ON_ERROR);
        }}

        require {schema_path};

        kk_schema_person();
        kk_schema_website();
        """
    ).lstrip()
    result = subprocess.run(
        ["php"],
        input=harness,
        text=True,
        capture_output=True,
        check=True,
    )
    return [json.loads(block) for block in SCRIPT_PATTERN.findall(result.stdout)]


@unittest.skipIf(shutil.which("php") is None, "php CLI not installed")
class PersonEntityConsolidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.person, cls.website = render_front_page_person_and_website()

    def test_person_keeps_the_canonical_id_and_umlaut_name(self):
        self.assertEqual("Person", self.person["@type"])
        self.assertEqual(PERSON_ID, self.person["@id"])
        self.assertEqual("Kris Krüg", self.person["name"])
        self.assertEqual("Kris Krug", self.person["alternateName"])
        self.assertEqual("https://kriskrug.co", self.person["url"])

    def test_website_name_uses_the_umlaut_spelling(self):
        self.assertEqual("WebSite", self.website["@type"])
        self.assertEqual("Kris Krüg", self.website["name"])
        self.assertEqual(["Kris Krug", "kriskrug.co"], self.website["alternateName"])
        self.assertEqual({"@id": PERSON_ID}, self.website["publisher"])

    def test_works_for_links_bc_ai_by_id_and_uses_www_futureproof(self):
        self.assertEqual(
            [
                {
                    "@type": "Organization",
                    "@id": "https://bc-ai.ca/#organization",
                    "name": "BC + AI Ecosystem Association",
                    "url": "https://bc-ai.ca/",
                },
                {
                    "@type": "Organization",
                    "name": "Vancouver AI",
                    "url": "https://vancouver.ai/",
                },
                {
                    "@type": "Organization",
                    "name": "Futureproof Festival",
                    "url": "https://www.futureproof.website/",
                },
            ],
            self.person["worksFor"],
        )

    def test_same_as_lists_only_profiles_the_site_already_links(self):
        self.assertEqual(
            [
                "https://twitter.com/kriskrug",
                "https://x.com/kriskrug",
                "https://www.instagram.com/kriskrug/",
                "https://www.linkedin.com/in/kriskrug/",
                "https://www.youtube.com/kriskrug",
                "https://www.flickr.com/photos/kk/",
            ],
            self.person["sameAs"],
        )
        footer = (ROOT / "theme/kk-aurora/parts/footer.html").read_text(encoding="utf-8")
        self.assertIn('href="https://www.linkedin.com/in/kriskrug/"', footer)
        self.assertIn('href="https://www.youtube.com/kriskrug"', footer)
        photography = (
            ROOT / "content/source-packs/keynotes-2026/wp-payloads/photography.html"
        ).read_text(encoding="utf-8")
        self.assertIn('href="https://www.flickr.com/photos/kk/"', photography)


if __name__ == "__main__":
    unittest.main()
