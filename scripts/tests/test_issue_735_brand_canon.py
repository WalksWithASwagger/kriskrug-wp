"""#735: live Aurora chrome uses BC + AI (spaces) and Kris Krüg."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
THEME = ROOT / "theme/kk-aurora"
LIVE_CHROME = [
    THEME / "parts/header.html",
    THEME / "parts/footer.html",
    THEME / "patterns/hero-gradient.php",
    THEME / "patterns/stats-counter.php",
]


class Issue735BrandCanonTests(unittest.TestCase):
    def test_live_chrome_does_not_use_unspaced_bc_ai(self):
        offenders = []
        for path in LIVE_CHROME:
            text = path.read_text(encoding="utf-8")
            if "BC+AI" in text:
                offenders.append(path.relative_to(ROOT).as_posix())
        self.assertEqual(offenders, [])

    def test_header_and_footer_use_krug_umlaut(self):
        header = (THEME / "parts/header.html").read_text(encoding="utf-8")
        footer = (THEME / "parts/footer.html").read_text(encoding="utf-8")
        self.assertIn("Kris Krüg home", header)
        self.assertIn('aria-label="Kris Krüg"', footer)
        self.assertIn("Kris Krüg", footer)
        self.assertNotIn("Kris Krug home", header)
        self.assertNotIn("Copyright 2026 Kris Krug.", footer)

    def test_title_separator_is_not_an_em_dash(self):
        source = (THEME / "functions.php").read_text(encoding="utf-8")
        self.assertNotIn("return '\u2014';", source)
        self.assertIn("return '|';", source)
        self.assertNotIn("Writing \u2014", source)


if __name__ == "__main__":
    unittest.main()
