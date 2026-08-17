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


if __name__ == "__main__":
    unittest.main()
