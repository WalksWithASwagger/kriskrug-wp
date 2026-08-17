import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FRONT_PAGE = ROOT / "theme/kk-aurora/templates/front-page.html"
SPIKE = (
    ROOT
    / "content/drafts/2026-07-26-what-people-say/network-diagram-spike/index.html"
)


def _people_say_block(source: str) -> str:
    match = re.search(
        r'<section class="aurora-people-say-band".*?</section>',
        source,
        re.DOTALL,
    )
    if match is None:
        raise AssertionError("missing #what-people-say band")
    return match.group(0)


class Issue415HomepagePeopleSayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.front = FRONT_PAGE.read_text(encoding="utf-8")
        cls.band = _people_say_block(cls.front)
        cls.spike = SPIKE.read_text(encoding="utf-8")

    def test_clustered_quotes_are_attributed_and_already_public(self):
        self.assertIn('id="what-people-say"', self.band)
        self.assertIn("The rooms talk back.", self.band)
        self.assertIn(">Stages<", self.band)
        self.assertIn(">Rooms<", self.band)
        self.assertIn(">Practice<", self.band)
        self.assertIn("Jai Djwa", self.band)
        self.assertIn("Ed Kennedy", self.band)
        self.assertIn("Audience feedback", self.band)
        self.assertIn('href="/testimonials/"', self.band)
        self.assertIn('href="/speaking/"', self.band)
        self.assertNotIn("beehiiv.com", self.band)
        self.assertNotIn("Named people", self.band)

    def test_no_placeholder_or_invented_cites(self):
        self.assertNotRegex(self.front, re.compile(r"fresh proof", re.I))
        self.assertNotIn("Event organizer quote", self.front)
        self.assertNotIn("Workshop host quote", self.front)
        self.assertNotIn("Leadership audience quote", self.front)
        self.assertNotIn("\u2014", self.band)

    def test_network_spike_is_standalone_with_no_cdn(self):
        self.assertTrue(SPIKE.is_file())
        self.assertIn("Not for live embed", self.spike)
        self.assertNotRegex(self.spike, re.compile(r'<script[^>]+src=', re.I))
        self.assertNotRegex(self.spike, re.compile(r'<link[^>]+href=', re.I))
        self.assertNotIn("unpkg.com", self.spike)
        self.assertNotIn("jsdelivr", self.spike)
        self.assertIn("tabindex=\"0\"", self.spike)
        self.assertIn("Kris Krüg", self.spike)


if __name__ == "__main__":
    unittest.main()
