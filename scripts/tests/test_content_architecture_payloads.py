import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "content/source-packs/content-architecture-2026"
PAYLOADS = PACK / "wp-payloads"


class ContentArchitecturePayloadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page_map = json.loads((PAYLOADS / "page-map.json").read_text(encoding="utf-8"))

    def test_all_mapped_payloads_exist(self):
        for page in self.page_map.values():
            self.assertTrue((PAYLOADS / page["payload"]).exists(), page["payload"])

    def test_payloads_have_required_readback_markers(self):
        for name, page in self.page_map.items():
            html = (PAYLOADS / page["payload"]).read_text(encoding="utf-8")
            for marker in page["markers"]:
                self.assertIn(marker, html, f"{name} missing marker {marker!r}")

    def test_payloads_do_not_reintroduce_retired_page_css_systems(self):
        retired_prefixes = ("kk-", "kkp-", "kkx-", "kk-services-", "kk-publications-")
        for path in PAYLOADS.glob("*.html"):
            html = path.read_text(encoding="utf-8")
            for class_attr in re.findall(r'class="([^"]+)"', html):
                tokens = class_attr.split()
                bad = [token for token in tokens if token.startswith(retired_prefixes)]
                self.assertEqual([], bad, f"{path.name} retired classes: {bad}")

    def test_payloads_are_body_only_and_public_safe(self):
        forbidden_fragments = (
            "<h1",
            "</h1>",
            "<style",
            "notion.so",
            "notionusercontent",
            "wp-json/wp/v2",
            "authorization",
            "bearer ",
            "wp_app_password",
            "wp_user",
        )
        for path in PAYLOADS.glob("*.html"):
            html = path.read_text(encoding="utf-8")
            lowered = html.lower()
            for fragment in forbidden_fragments:
                self.assertNotIn(fragment, lowered, f"{path.name} contains {fragment}")

    def test_contact_preserves_existing_email_path(self):
        html = (PAYLOADS / "contact.html").read_text(encoding="utf-8")
        self.assertIn("mailto:feelmoreplants@gmail.com", html)
        self.assertIn("Send the note", html)


if __name__ == "__main__":
    unittest.main()
