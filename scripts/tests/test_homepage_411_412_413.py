"""Homepage cluster #411 / #412 / #413 source guards.

No live WordPress writes. These assert the tracked front-page template and
the Revive sheet, not production HTML.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FRONT_PAGE = ROOT / "theme/kk-aurora/templates/front-page.html"
REVIVE = ROOT / "theme/kk-aurora/assets/css/revive-port.css"


def _section(source: str, class_name: str) -> str:
    match = re.search(
        rf"<section[^>]*class=\"[^\"]*{re.escape(class_name)}[^\"]*\"[\s\S]*?</section>",
        source,
    )
    if match is None:
        raise AssertionError(f"missing section .{class_name}")
    return match.group(0)


class Homepage411WorkBandTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.front = FRONT_PAGE.read_text(encoding="utf-8")
        cls.css = REVIVE.read_text(encoding="utf-8")
        cls.work = _section(cls.front, "aurora-work-band")

    def test_work_band_uses_named_heading_and_receipts_copy(self):
        self.assertIn("BC + AI. Futureproof. The", self.work)
        self.assertIn("250+ members, 94+ events, 3,000+ through the door", self.work)
        self.assertIn("Frontier tech without the hype deck", self.work)
        self.assertIn("No doom sermon", self.work)
        self.assertNotIn("What Kris is", self.work)
        self.assertNotIn("trust layer", self.work)
        self.assertNotIn("operating conditions", self.work)

    def test_work_band_has_zero_rooms_and_zero_em_dashes(self):
        self.assertEqual(0, len(re.findall(r"rooms?", self.work, flags=re.I)))
        self.assertNotIn("\u2014", self.work)
        self.assertIn("BC + AI", self.work)

    def test_work_band_cards_align_and_drop_numeral_is_quiet(self):
        self.assertIn("align-items: stretch", self.css)
        self.assertIn(".aurora-work-card:nth-child(2) {\n    margin-top: 0;", self.css)
        self.assertNotIn("margin-top: -2.5rem", self.css)
        self.assertIn('aria-hidden="true"', self.work)
        self.assertIn("font-size: 0.72rem", self.css)
        self.assertIn(".aurora-work-card:focus-visible", self.css)
        self.assertIn(".aurora-work-band .aurora-section-head a:focus-visible", self.css)


class Homepage412CreativeLabsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.front = FRONT_PAGE.read_text(encoding="utf-8")
        cls.css = REVIVE.read_text(encoding="utf-8")
        cls.labs = _section(cls.front, "aurora-creative-labs")

    def test_labs_section_names_four_public_builds(self):
        self.assertIn("Creative Labs", self.labs)
        self.assertIn("The labs around the", self.labs)
        for title in ("Vancouver AI", "Punk Rock AI", "Both Hands Full", "AI Garden"):
            self.assertIn(title, self.labs)
        self.assertIn("https://vancouver.ai/", self.labs)
        self.assertIn("https://www.punkrockai.com/", self.labs)
        self.assertIn("https://www.bothhandsfull.com/", self.labs)
        self.assertIn("https://kriskrug.ai/", self.labs)

    def test_labs_copy_is_plain_and_has_no_rooms_or_em_dashes(self):
        self.assertEqual(0, len(re.findall(r"rooms?", self.labs, flags=re.I)))
        self.assertNotIn("\u2014", self.labs)
        self.assertNotIn("trust layer", self.labs)
        self.assertIn("Kris Krüg", self.labs)

    def test_labs_images_are_local_or_media_library(self):
        srcs = re.findall(r"<img[^>]+src=\"([^\"]+)\"", self.labs)
        self.assertEqual(4, len(srcs))
        for src in srcs:
            self.assertTrue(
                src.startswith("/wp-content/themes/kk-aurora/")
                or "kriskrug.co/wp-content/uploads/" in src
                or "i0.wp.com/kriskrug.co/" in src,
                f"lab image is a hotlink: {src}",
            )
        self.assertNotIn("punkrockai.com", " ".join(srcs))
        self.assertNotIn("bothhandsfull.com/opengraph", " ".join(srcs))

    def test_labs_layout_puts_text_below_the_photo(self):
        self.assertIn("aspect-ratio: 4 / 5", self.css)
        self.assertIn(".aurora-lab-card-body", self.css)
        self.assertIn(".aurora-lab-card:focus-visible", self.css)
        self.assertIn("object-position: center 35%", self.css)


if __name__ == "__main__":
    unittest.main()
