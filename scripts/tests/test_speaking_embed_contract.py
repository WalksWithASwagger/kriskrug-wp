import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlparse


ROOT = Path(__file__).resolve().parents[2]
PAYLOAD = (
    ROOT
    / "content"
    / "drafts"
    / "2026-07-26-speaking-page"
    / "payload-body.html"
)
FIRST_PARTY_IMAGE_HOSTS = {"kriskrug.co", "www.kriskrug.co"}


class EmbedParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.buttons = []
        self.iframes = []
        self.images = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "button":
            self.buttons.append(values)
        elif tag == "iframe":
            self.iframes.append(values)
        elif tag == "img":
            self.images.append(values)


class SpeakingEmbedContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAYLOAD.read_text(encoding="utf-8")
        cls.parser = EmbedParser()
        cls.parser.feed(cls.html)

    def test_embeds_start_behind_keyboard_accessible_facades(self):
        wrappers = re.findall(
            r'<div class="kk-speak-embed">(.*?)</div>', self.html, re.DOTALL
        )
        self.assertGreaterEqual(len(wrappers), 2)

        for wrapper in wrappers:
            parser = EmbedParser()
            parser.feed(wrapper)
            self.assertEqual(1, len(parser.buttons))
            self.assertEqual(1, len(parser.iframes))
            self.assertEqual(1, len(parser.images))
            self.assertIn("<template", wrapper)

            button = parser.buttons[0]
            self.assertIn("kk-speak-embed-facade", button.get("class", "").split())
            self.assertEqual("button", button.get("type"))
            self.assertTrue(button.get("aria-label"))
            self.assertNotEqual("-1", button.get("tabindex"))
            self.assertNotIn("disabled", button)

            poster = parser.images[0]
            self.assertIn("kk-speak-embed-poster", poster.get("class", "").split())
            self.assertEqual("lazy", poster.get("loading"))
            self.assertEqual("", poster.get("alt"))
            self.assertTrue(poster.get("width"))
            self.assertTrue(poster.get("height"))

        active_html = re.sub(
            r"<template\b.*?</template>", "", self.html, flags=re.DOTALL
        )
        self.assertNotIn("<iframe", active_html.lower())

    def test_deferred_iframes_are_private_lazy_and_accessible(self):
        self.assertGreaterEqual(len(self.parser.iframes), 2)
        for iframe in self.parser.iframes:
            self.assertEqual("lazy", iframe.get("loading"))
            self.assertTrue(iframe.get("title"))
            serialized_attrs = " ".join(
                f"{name}={value or ''}" for name, value in iframe.items()
            ).lower()
            self.assertNotIn("autoplay", serialized_attrs)

            parsed = urlparse(iframe.get("src", ""))
            self.assertEqual("https", parsed.scheme)
            self.assertEqual("www.youtube-nocookie.com", parsed.hostname)
            self.assertNotIn("autoplay", parse_qs(parsed.query))

    def test_facade_click_loads_and_focuses_the_deferred_iframe(self):
        self.assertIn(".kk-speak-embed-facade", self.html)
        self.assertIn(r'content: "\25B6";', self.html)
        self.assertNotIn('content: "▶";', self.html)
        self.assertRegex(self.html, r"addEventListener\(['\"]click['\"]")
        self.assertIn("template.content.cloneNode(true)", self.html)
        self.assertIn("replaceChildren", self.html)
        self.assertRegex(self.html, r"iframe\.focus\(\)")

    def test_hero_stays_the_only_eager_media_candidate(self):
        self.assertLess(
            self.html.index('class="kk-speak-hero"'), self.html.index('id="watch"')
        )
        self.assertIn('loading="eager"', self.html)
        self.assertIn('fetchpriority="high"', self.html)

    def test_payload_does_not_hotlink_third_party_images(self):
        self.assertGreaterEqual(len(self.parser.images), 1)
        urls = []
        for image in self.parser.images:
            urls.append(image.get("src", ""))
            urls.extend(
                candidate.strip().split()[0]
                for candidate in image.get("srcset", "").split(",")
                if candidate.strip()
            )

        for url in urls:
            parsed = urlparse(url)
            if parsed.scheme:
                self.assertIn(parsed.hostname, FIRST_PARTY_IMAGE_HOSTS, url)


if __name__ == "__main__":
    unittest.main()
