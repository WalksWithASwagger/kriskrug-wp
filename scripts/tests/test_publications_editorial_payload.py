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
        self.assertEqual(18, self.payload.count('<article class="kk-press-entry'))
        self.assertEqual(25, self.payload.count("<li><time"))

        dates = re.findall(r'datetime="(\d{4}-\d{2}-\d{2})"', self.payload)
        self.assertEqual(46, len(dates))
        self.assertEqual(sorted(dates, reverse=True), dates)

    def test_markup_and_voice_guards(self):
        self.assertNotRegex(self.payload, r"<h1\b")
        self.assertNotIn("—", self.payload)
        self.assertIn("@media (max-width:620px)", self.payload)
        self.assertIn("@media (prefers-reduced-motion:reduce)", self.payload)

    def test_images_have_dimensions_and_alt_text(self):
        self.assertEqual(9, len(self.parser.images))
        for image in self.parser.images:
            self.assertTrue(image.get("alt"))
            self.assertTrue(image.get("width"))
            self.assertTrue(image.get("height"))

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


if __name__ == "__main__":
    unittest.main()
