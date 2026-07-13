"""Marquee Tier 2 guarantees: OG image meta, Article schema, sitemap, on-brand OG card.

Browser-free (stdlib only) so it runs in CI. The actual PNG render is exercised by the local
build; here we lock the metadata/schema/sitemap that every board page must emit.
"""
import html as H
import json
import re
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/marquee"))

import build  # noqa: E402
import og  # noqa: E402

BOARD = {
    "id": "2026-w26-x", "status": "live", "week": "2026-W26", "date": "2026-06-26",
    "after": "Marshall McLuhan", "skin": "led", "board": ["THE MODEL", "IS THE", "MESSAGE"],
    "kicker": "now showing", "dek": "why it matters",
    "source": {"title": "Understanding Media", "author": "Marshall McLuhan, 1964"},
    "tags": ["mcluhan", "ai"],
    "seo": {"title": "The Model Is the Message", "description": "A marquee board.", "slug": "the-model-is-the-message"},
}
PERSON = "https://kriskrug.co/#person"


class OgMetaTests(unittest.TestCase):
    def test_page_head_emits_full_image_set(self):
        head = build.page_head("T", "D", "https://kriskrug.co/marquee/x/", "T",
                               og_image="https://kriskrug.co/marquee/x/og.png", og_alt="alt")
        for needle in ('property="og:image"', 'property="og:image:secure_url"',
                       'property="og:image:width" content="1200"',
                       'property="og:image:height" content="630"',
                       'property="og:image:alt"', 'name="twitter:site" content="@feelmoreplants"',
                       'name="twitter:image"', 'name="twitter:image:alt"'):
            self.assertIn(needle, head, needle)

    def test_page_head_omits_image_when_none(self):
        head = build.page_head("T", "D", "u", "T")
        self.assertNotIn("og:image", head)


class SchemaTests(unittest.TestCase):
    def test_board_page_jsonld_is_article_linked_to_person(self):
        _slug, htmlout = build.board_page(BOARD, None, None)
        m = re.search(r'<script type="application/ld\+json">(.*?)</script>', htmlout, re.S)
        data = json.loads(H.unescape(m.group(1)))
        self.assertEqual(data["@type"], "Article")
        self.assertEqual(data["author"]["@id"], PERSON)
        self.assertEqual(data["publisher"]["@id"], PERSON)
        self.assertEqual(data["articleSection"], "Marquee")
        self.assertEqual(data["image"]["width"], 1200)
        self.assertTrue(data["image"]["url"].endswith("/og.png"))

    def test_board_page_references_og_image(self):
        _slug, htmlout = build.board_page(BOARD, None, None)
        self.assertIn("the-model-is-the-message/og.png", htmlout)


class SitemapTests(unittest.TestCase):
    def test_sitemap_lists_board_and_image(self):
        xml = build.sitemap_xml([BOARD])
        self.assertIn("<loc>https://kriskrug.co/marquee/</loc>", xml)
        self.assertIn("<loc>https://kriskrug.co/marquee/the-model-is-the-message/</loc>", xml)
        self.assertIn("<image:loc>https://kriskrug.co/marquee/the-model-is-the-message/og.png</image:loc>", xml)
        self.assertIn("<lastmod>2026-06-26</lastmod>", xml)


class OgCardTests(unittest.TestCase):
    def test_card_is_static_and_branded(self):
        card = og.card_html(BOARD)
        self.assertIn("kkm-cell", card)               # the board
        self.assertIn("The Marquee", card)            # wordmark
        self.assertIn("after Marshall McLuhan", card)  # attribution
        self.assertNotIn("<script", card)             # static — no animation in the share card

    @mock.patch.object(og.shutil, "which", return_value=None)
    def test_og_unavailable_without_node(self, _which):
        self.assertFalse(og.og_available())

    @mock.patch.object(og.glob, "glob", return_value=["/opt/pw-browsers/chromium-1/chrome-linux/chrome"])
    @mock.patch.object(og.shutil, "which", return_value="/usr/bin/node")
    def test_og_available_with_node_and_chromium(self, _which, _glob):
        self.assertTrue(og.og_available())


if __name__ == "__main__":
    unittest.main()
