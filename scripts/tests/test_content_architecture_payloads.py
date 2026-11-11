import json
import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "content/source-packs/content-architecture-2026"
PAYLOADS = PACK / "wp-payloads"

sys.path.insert(0, str(ROOT / "scripts"))
from content_architecture_deploy import retired_class_tokens  # noqa: E402


class ContentArchitecturePayloadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.maps = [
            path for path in sorted(PAYLOADS.rglob("page-map.json")) if path.is_file()
        ]
        cls.mapped_pages = []
        for path in cls.maps:
            page_map = json.loads(path.read_text(encoding="utf-8"))
            for name, page in page_map.items():
                cls.mapped_pages.append((path.parent, name, page))

    def test_all_mapped_payloads_exist(self):
        self.assertTrue(self.maps, "no content architecture page maps found")
        for payload_dir, _name, page in self.mapped_pages:
            self.assertTrue((payload_dir / page["payload"]).exists(), page["payload"])
            self.assertNotIn("title", page)

    def test_payloads_have_required_readback_markers(self):
        for payload_dir, name, page in self.mapped_pages:
            html = (payload_dir / page["payload"]).read_text(encoding="utf-8")
            for marker in page["markers"]:
                self.assertIn(marker, html, f"{name} missing marker {marker!r}")

    def test_payloads_do_not_reintroduce_retired_page_css_systems(self):
        page_ids = {
            directory / page["payload"]: page["id"]
            for directory, _name, page in self.mapped_pages
        }
        for path in PAYLOADS.rglob("*.html"):
            html = path.read_text(encoding="utf-8")
            bad = retired_class_tokens(html, page_id=page_ids.get(path))
            self.assertEqual([], bad, f"{path.name} retired classes: {bad}")

    def test_testimonials_class_allowance_is_limited_to_page_2409(self):
        html = '<div class="kk-testimonials kk-test-reader kk-publications-card"></div>'
        self.assertEqual(["kk-publications-card"], retired_class_tokens(html, page_id=2409))
        self.assertEqual(
            ["kk-testimonials", "kk-test-reader", "kk-publications-card"],
            retired_class_tokens(html, page_id=2250),
        )

    # These approved page repairs use inline CSS; Work is restricted to one card.
    STYLE_ALLOWED = {"about.html", "speaking.html", "testimonials.html", "work.html"}

    def test_work_inline_css_is_scoped_to_one_card(self):
        html = (PAYLOADS / "work.html").read_text(encoding="utf-8")
        styles = re.findall(r"<style>(.*?)</style>", html, re.DOTALL)
        self.assertEqual(1, len(styles))
        selectors = re.findall(r"(?:^|})\s*([^{}]+)\{", styles[0])
        self.assertTrue(selectors)
        for selector_list in selectors:
            for selector in selector_list.split(","):
                self.assertRegex(selector.strip(), r"^#kk-work-bcai-card(?:\s|$)")

    def test_speaking_preserves_direct_recordings_without_eager_player(self):
        html = (PAYLOADS / "speaking.html").read_text(encoding="utf-8")
        self.assertNotIn("<iframe", html)
        self.assertIn('href="https://www.youtube.com/watch?v=hYT-hsml_ds"', html)
        self.assertIn('href="https://www.youtube.com/watch?v=-c7mgY2aSgM&amp;t=11s"', html)
        self.assertIn('href="/contact/#inquiries"', html)
        self.assertEqual(6, html.count('<article class="speaking-talk"'))

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
        for path in PAYLOADS.rglob("*.html"):
            html = path.read_text(encoding="utf-8")
            lowered = html.lower()
            for fragment in forbidden_fragments:
                if fragment == "<style" and path.name in self.STYLE_ALLOWED:
                    continue
                self.assertNotIn(fragment, lowered, f"{path.name} contains {fragment}")

    def test_contact_preserves_existing_email_path(self):
        html = (PAYLOADS / "contact.html").read_text(encoding="utf-8")
        self.assertIn("mailto:feelmoreplants@gmail.com", html)
        self.assertIn("Send the note", html)

    def test_work_payloads_include_the_sky_smoked_back(self):
        paths = (
            PAYLOADS / "work.html",
            ROOT / "content/source-packs/keynotes-2026/wp-payloads/work.html",
        )
        for path in paths:
            html = path.read_text(encoding="utf-8")
            self.assertEqual(1, html.count('href="https://lightningstrike.org/"'), path)
            self.assertIn("The Sky Smoked Back", html, path)


if __name__ == "__main__":
    unittest.main()
