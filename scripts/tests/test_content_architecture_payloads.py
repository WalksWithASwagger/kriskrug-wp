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

    # These page payloads use inline CSS scoped to their own markup.
    STYLE_ALLOWED = {"speaking.html", "testimonials.html", "work.html"}

    def test_work_inline_css_is_scoped_to_work_page(self):
        html = (PAYLOADS / "work.html").read_text(encoding="utf-8")
        styles = re.findall(r"<style>(.*?)</style>", html, re.DOTALL)
        self.assertEqual(1, len(styles))
        selectors = re.findall(r"([^{}]+)\{[^{}]*\}", styles[0])
        self.assertTrue(selectors)
        for selector_list in selectors:
            for selector in selector_list.split(","):
                self.assertRegex(
                    selector.strip(),
                    r"^(?:\.work-editorial|body\.aurora-theme\.page-id-2672 #aurora-main)(?:\s|:|$)",
                )

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
                if fragment == "<style" and (
                    path.name in self.STYLE_ALLOWED
                    or path.parent == PAYLOADS and path.name in self.SCOPED_PAGE_STYLES
                ):
                    continue
                self.assertNotIn(fragment, lowered, f"{path.name} contains {fragment}")

    SCOPED_PAGE_STYLES = {
        "about.html": 1208,
        "contact.html": 2418,
        "motleykrug-podcast.html": 2828,
        "photography.html": 12013,
        "services.html": 2666,
    }

    def test_inline_styles_are_scoped_to_their_wordpress_pages(self):
        page_ids = {
            directory / page["payload"]: page["id"]
            for directory, _name, page in self.mapped_pages
        }
        for filename, page_id in self.SCOPED_PAGE_STYLES.items():
            path = PAYLOADS / filename
            self.assertEqual(page_id, page_ids[path])
            html = path.read_text(encoding="utf-8")
            styles = re.findall(r"<style>(.*?)</style>", html, re.DOTALL)
            self.assertEqual(1, len(styles), filename)
            self.assertNotIn("/wp-content/uploads/showpiece-review/", html)
            css = re.sub(r"/\*.*?\*/", "", styles[0], flags=re.DOTALL)
            if filename == "photography.html":
                css = re.sub(
                    r"@keyframes photo-enter\s*\{\s*from\s*\{[^{}]+\}\s*to\s*\{[^{}]+\}\s*\}",
                    "",
                    css,
                )
            self.assertNotIn("@import", css)
            selectors = re.findall(r"(?:^|(?<=[{}]))\s*([^{}]+?)\s*\{", css)
            self.assertTrue(selectors, filename)
            scope = f"body.aurora-theme.page-id-{page_id} #aurora-main"
            for selector_list in selectors:
                if selector_list.startswith("@media "):
                    continue
                for selector in re.split(r",\s*(?![^()]*\))", selector_list):
                    self.assertRegex(selector.strip(), rf"^{re.escape(scope)}(?:[\s.:]|$)", filename)

    def test_contact_preserves_existing_email_path(self):
        html = (PAYLOADS / "contact.html").read_text(encoding="utf-8")
        self.assertIn("mailto:feelmoreplants@gmail.com", html)
        self.assertIn('href="mailto:feelmoreplants@gmail.com">Email Kris</a>', html)

    def test_work_payloads_include_the_sky_smoked_back(self):
        paths = (
            PAYLOADS / "work.html",
            ROOT / "content/source-packs/keynotes-2026/wp-payloads/work.html",
        )
        for path in paths:
            html = path.read_text(encoding="utf-8")
            self.assertEqual(1, html.count('href="https://lightningstrike.org/"'), path)
            self.assertIn("The Sky Smoked Back", html, path)

    def test_work_index_lists_tidepool_and_supercluster_after_unofficial_city(self):
        # Only the content-architecture payload deploys to page 2672; the
        # keynotes-2026 copy diverges on purpose (#1212).
        html = (PAYLOADS / "work.html").read_text(encoding="utf-8")
        hrefs = (
            'href="https://unofficial.city/"',
            'href="https://tidepool.ing/"',
            'href="https://littlesupercluster.com/"',
        )
        for href in hrefs:
            self.assertEqual(1, html.count(href), href)
        positions = [html.index(href) for href in hrefs]
        self.assertEqual(sorted(positions), positions)


if __name__ == "__main__":
    unittest.main()
