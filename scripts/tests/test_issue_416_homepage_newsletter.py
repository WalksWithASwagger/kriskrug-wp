import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FRONT_PAGE = ROOT / "theme/kk-aurora/templates/front-page.html"


def _newsletter_block(source: str) -> str:
    match = re.search(
        r'<section id="newsletter".*?</section>',
        source,
        re.DOTALL,
    )
    if match is None:
        raise AssertionError("missing #newsletter band")
    return match.group(0)


class Issue416HomepageNewsletterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.front = FRONT_PAGE.read_text(encoding="utf-8")
        cls.band = _newsletter_block(cls.front)

    def test_one_clear_cta_and_kept_thumbnails(self):
        self.assertIn("Weekly email", self.band)
        self.assertIn("Give me your email. I'll earn every open.", self.band)
        self.assertIn("Get the weekly email", self.band)
        self.assertEqual(1, self.band.count("kriskrug.beehiiv.com"))
        self.assertEqual(1, self.band.count("aurora-button-primary"))
        self.assertIn("aurora-newsletter-thumbs-query", self.band)
        self.assertIn("aurora-newsletter-thumb-media", self.band)
        self.assertIn("Recent writing", self.band)

    def test_cliche_stays_gone_and_e2e_is_not_claimed(self):
        self.assertNotRegex(self.band, re.compile(r"field notes", re.I))
        self.assertNotRegex(self.band, re.compile(r"dispatch", re.I))
        self.assertNotIn("\u2014", self.band)
        self.assertIn("Beehiiv signup E2E remains KK-owned", self.band)


if __name__ == "__main__":
    unittest.main()
