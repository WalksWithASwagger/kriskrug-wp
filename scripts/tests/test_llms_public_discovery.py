"""#1129 offline llms.txt public-discovery contract. No live network."""

from __future__ import annotations

import re
import unittest
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]
LLMS = ROOT / "fixes/llms.txt"
ROBOTS = ROOT / "fixes/robots.txt"
GUIDE = ROOT / "fixes/llms-txt-template.md"

MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
EVENTS_URL = "https://kriskrug.co/events/"
KNOWN_NON_FINAL_URL_RE = re.compile(
    r"(?:"
    r"[?&]s="
    r"|/search(?:/|\?|$)"
    r"|https?://futureproof\.website(?:/|$)"
    r"|https://kriskrug\.co/projects(?:/|\?|$)"
    r"|https://kriskrug\.co/home(?:/|\?|$)"
    r")",
    re.IGNORECASE,
)


def markdown_links(text: str) -> list[tuple[str, str]]:
    return [(match.group(1), match.group(2)) for match in MARKDOWN_LINK_RE.finditer(text)]


def is_search_or_query_url(url: str) -> bool:
    parts = urlsplit(url)
    path = parts.path.rstrip("/") or "/"
    if path == "/search" or path.startswith("/search/"):
        return True
    if parts.query:
        return True
    return False


def looks_like_final_canonical_url(url: str) -> bool:
    parts = urlsplit(url)
    if parts.scheme != "https":
        return False
    if parts.username or parts.password or not parts.netloc:
        return False
    if parts.query or parts.fragment:
        return False
    if not parts.path.endswith("/"):
        return False
    return True


class LlmsLinkHelperTests(unittest.TestCase):
    def test_parser_reads_markdown_links_only(self):
        text = (
            "# Title\n"
            "- [Events](https://kriskrug.co/events/): gatherings\n"
            "- bare https://kriskrug.co/about/\n"
            "- [Search](https://kriskrug.co/?s=vancouver+ai+meetup): no\n"
        )
        self.assertEqual(
            [
                ("Events", "https://kriskrug.co/events/"),
                ("Search", "https://kriskrug.co/?s=vancouver+ai+meetup"),
            ],
            markdown_links(text),
        )

    def test_helpers_reject_search_and_non_final_shapes(self):
        self.assertTrue(is_search_or_query_url("https://kriskrug.co/?s=vancouver+ai+meetup"))
        self.assertTrue(is_search_or_query_url("https://kriskrug.co/search/"))
        self.assertTrue(is_search_or_query_url("https://kriskrug.co/events/?utm=1"))
        self.assertFalse(is_search_or_query_url(EVENTS_URL))
        self.assertTrue(looks_like_final_canonical_url(EVENTS_URL))
        self.assertFalse(
            looks_like_final_canonical_url("https://kriskrug.co/?s=vancouver+ai+meetup")
        )
        self.assertFalse(looks_like_final_canonical_url("http://kriskrug.co/events/"))
        self.assertFalse(looks_like_final_canonical_url("https://kriskrug.co/events"))
        self.assertTrue(KNOWN_NON_FINAL_URL_RE.search("https://futureproof.website/"))
        self.assertFalse(KNOWN_NON_FINAL_URL_RE.search("https://www.futureproof.website/"))


class LlmsPublicDiscoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.llms = LLMS.read_text(encoding="utf-8")
        cls.robots = ROBOTS.read_text(encoding="utf-8")
        cls.guide = GUIDE.read_text(encoding="utf-8")
        cls.links = markdown_links(cls.llms)

    def test_payload_and_guide_exist(self):
        self.assertTrue(LLMS.is_file(), LLMS)
        self.assertTrue(GUIDE.is_file(), GUIDE)
        self.assertTrue(self.llms.startswith("# Kris Krüg\n"))
        self.assertIn("https://kriskrug.co/llms.txt", self.guide)
        self.assertIn("source change in this repo is not evidence", self.guide.lower())

    def test_meetup_uses_events_not_search(self):
        meetup = [url for label, url in self.links if label == "Vancouver AI Meetup"]
        events = [url for label, url in self.links if label == "Events"]
        self.assertEqual([EVENTS_URL], meetup)
        self.assertEqual([EVENTS_URL], events)
        self.assertNotIn("?s=", self.llms)
        self.assertNotIn("/search/", self.llms)
        self.assertNotIn("vancouver+ai+meetup", self.llms)

    def test_every_link_is_a_final_https_url(self):
        self.assertGreaterEqual(len(self.links), 20)
        seen = []
        for label, url in self.links:
            with self.subTest(label=label, url=url):
                self.assertFalse(is_search_or_query_url(url), url)
                self.assertTrue(looks_like_final_canonical_url(url), url)
                self.assertIsNone(KNOWN_NON_FINAL_URL_RE.search(url), url)
            seen.append(url)
        self.assertEqual(len(seen), len(self.links))

    def test_internal_targets_stay_on_the_public_host(self):
        internal = [url for _, url in self.links if "kriskrug.co" in urlsplit(url).netloc]
        self.assertGreaterEqual(len(internal), 15)
        for url in internal:
            parts = urlsplit(url)
            self.assertEqual("kriskrug.co", parts.netloc)
            self.assertTrue(parts.path.startswith("/"))
            self.assertFalse(parts.path.startswith("/wp-admin/"))
            self.assertFalse(parts.path.startswith("/wp-json/"))

    def test_search_stays_disallowed_in_repo_robots(self):
        self.assertIn("Disallow: /?s=", self.robots)
        self.assertIn("Disallow: /search/", self.robots)
        self.assertGreaterEqual(self.robots.count("Disallow: /?s="), 2)
        self.assertGreaterEqual(self.robots.count("Disallow: /search/"), 2)

    def test_guide_keeps_apply_and_rollback_on_the_existing_handler(self):
        lowered = self.guide.lower()
        self.assertIn("code snippets", lowered)
        self.assertIn("rollback", lowered)
        self.assertIn("fixes/llms.txt", self.guide)
        self.assertIn("text/plain", lowered)
        self.assertIn("snapshot the current snippet body", lowered)


if __name__ == "__main__":
    unittest.main()
