import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
PAYLOAD_PATH = (
    REPO_ROOT
    / "content"
    / "source-packs"
    / "keynotes-2026"
    / "wp-payloads"
    / "publications.html"
)
META_PATH = PAYLOAD_PATH.parent / "page-meta.json"
MEDIA_MANIFEST_PATH = (
    REPO_ROOT
    / "content"
    / "source-packs"
    / "keynotes-2026"
    / "assets"
    / "publications-press-media.md"
)
PUBLISH_GATE_PATH = (
    REPO_ROOT
    / "content"
    / "source-packs"
    / "keynotes-2026"
    / "verification"
    / "PUBLICATIONS-EDITORIAL-PUBLISH-GATE-2026-07-24.md"
)
GAP_REPORT_PATH = (
    REPO_ROOT
    / "content"
    / "source-packs"
    / "keynotes-2026"
    / "verification"
    / "PUBLICATIONS-KB-GAP-REPORT-2026-08-01.md"
)

FORBIDDEN_SKIN_MARKERS = (
    "kk-publications",
    "#00e5ff",
    "#ff6a6a",
    "--press-night",
)


class LinkAndImageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.external_links = []
        self.images = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "a" and values.get("href", "").startswith("http"):
            self.external_links.append(values)
        if tag == "img":
            self.images.append(values)


class PublicationsEditorialPayloadTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = PAYLOAD_PATH.read_text(encoding="utf-8")
        cls.parser = LinkAndImageParser()
        cls.parser.feed(cls.payload)

    def test_complete_reverse_chronological_inventory(self):
        self.assertEqual(3, self.payload.count('<a class="kk-press-feature'))
        self.assertEqual(20, self.payload.count('<article class="kk-press-entry'))
        self.assertEqual(25, self.payload.count("<li><time"))

        dates = re.findall(r'datetime="(\d{4}-\d{2}-\d{2})"', self.payload)
        self.assertEqual(48, len(dates))
        self.assertEqual(sorted(dates, reverse=True), dates)

    def test_structure_and_reciprocal_links(self):
        self.assertIn('class="kk-press-featured"', self.payload)
        self.assertIn('class="kk-press-feed"', self.payload)
        self.assertIn('class="kk-press-legacy"', self.payload)
        self.assertIn('class="kk-press-board"', self.payload)
        self.assertIn('class="kk-press-outlets"', self.payload)
        self.assertIn('class="kk-press-pull"', self.payload)
        self.assertIn("/podcast-guesting-page-epk/", self.payload)
        self.assertIn(
            "/2026/07/02/ai-media-appearances-podcast-guesting/", self.payload
        )
        self.assertIn("Media Appearances", self.payload)
        self.assertIn("vanmag.com/city/power-50/", self.payload)

    def test_forbids_dark_neon_ghost_skin(self):
        lowered = self.payload.lower()
        for marker in FORBIDDEN_SKIN_MARKERS:
            self.assertNotIn(marker.lower(), lowered)
        self.assertNotRegex(self.payload, r"--press-night\s*:")
        self.assertNotIn("background:var(--press-night)", self.payload)
        self.assertNotIn("background:#0d1014", self.payload)

    def test_markup_and_voice_guards(self):
        self.assertNotRegex(self.payload, r"<h1\b")
        self.assertNotIn("—", self.payload)
        self.assertRegex(self.payload, r"@media\s*\(max-width:\s*620px\)")
        self.assertRegex(self.payload, r"@media\s*\(prefers-reduced-motion:\s*reduce\)")
        self.assertIn("Space Grotesk", self.payload)
        self.assertIn("DM Sans", self.payload)
        self.assertIn("--aurora-paper", self.payload)
        self.assertIn("--aurora-ink", self.payload)
        self.assertIn("--aurora-signal", self.payload)

    def test_images_have_dimensions_and_alt_text(self):
        keys = [img.get("data-media-key") for img in self.parser.images]
        self.assertGreaterEqual(len(self.parser.images), 16)
        self.assertGreaterEqual(len(set(keys)), 16)
        for image in self.parser.images:
            self.assertTrue(image.get("alt"))
            self.assertTrue(image.get("width"))
            self.assertTrue(image.get("height"))
            self.assertTrue(image.get("src", "").startswith("../assets/"))
            self.assertEqual(Path(image["src"]).name, image.get("data-media-key"))
            self.assertTrue((PAYLOAD_PATH.parent / image["src"]).resolve().exists())

    def test_external_links_open_safely(self):
        self.assertGreaterEqual(len(self.parser.external_links), 47)
        for link in self.parser.external_links:
            self.assertEqual("_blank", link.get("target"))
            self.assertEqual("noopener noreferrer", link.get("rel"))

    def test_seo_metadata_and_media_manifest(self):
        page_meta = json.loads(META_PATH.read_text(encoding="utf-8"))
        publications = next(
            page for page in page_meta["pages"] if page["slug"] == "publications"
        )
        self.assertEqual(
            "Press, Interviews & Media Coverage | Kris Krüg",
            publications["meta"]["jetpack_seo_html_title"],
        )
        self.assertTrue(MEDIA_MANIFEST_PATH.exists())
        manifest = MEDIA_MANIFEST_PATH.read_text(encoding="utf-8")
        self.assertIn("Excluded from the publication set", manifest)
        self.assertIn("explicit media approval", manifest)
        self.assertIn("superseded", manifest.lower())
        gate = PUBLISH_GATE_PATH.read_text(encoding="utf-8")
        self.assertIn("WordPress page ID: `1895`", gate)
        self.assertRegex(gate, r"authenticated\s+`context=edit` snapshot")
        self.assertIn("Do not delete uploaded media during emergency rollback", gate)
        self.assertIn("superseded", gate.lower())
        self.assertIn("Aurora paper", gate)
        self.assertTrue(GAP_REPORT_PATH.exists())
        gap = GAP_REPORT_PATH.read_text(encoding="utf-8")
        self.assertIn("Power 50", gap)
        self.assertIn("cyan", gap.lower())


if __name__ == "__main__":
    unittest.main()
