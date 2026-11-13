"""Marquee slugs fold accents to the slug WordPress stores (#1257).

Unfolded, "Krüg" stayed in the slug sent to WordPress, which stores "krug", so
an exact slug lookup could never find the board again.
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/marquee"))
sys.path.insert(0, str(ROOT / "scripts/notion-to-wp"))

from marquee_lib import slugify  # noqa: E402
from notion_client import slugify as publisher_slugify  # noqa: E402

ACCENTED = {
    "Kris Krüg Live": "kris-krug-live",
    "MØTLEYKRÜG": "motleykrug",
    "Eth\N{LATIN SMALL LETTER O WITH DOT BELOW}\N{COMBINING ACUTE ACCENT}s": "ethos",
    "Etho\N{COMBINING DOT BELOW}\N{COMBINING ACUTE ACCENT}s": "ethos",
    "Æsir Œuvre Straße Łódź Þór Đorđe": "aesir-oeuvre-strasse-lodz-thor-dorde",
    "Krüg’s Café": "krugs-cafe",
}


class MarqueeSlugifyTests(unittest.TestCase):
    def test_folds_accented_latin_to_ascii(self):
        for phrase, slug in ACCENTED.items():
            with self.subTest(phrase=phrase):
                self.assertEqual(slugify(phrase), slug)

    def test_fold_matches_the_publisher_slugify(self):
        for phrase in ACCENTED:
            with self.subTest(phrase=phrase):
                self.assertEqual(slugify(phrase), publisher_slugify(phrase))

    def test_ascii_slugs_are_unchanged(self):
        self.assertEqual(
            slugify("THE MODEL IS THE MESSAGE"), "the-model-is-the-message"
        )
        self.assertEqual(slugify("snake_case & more!"), "snake-case-more")

    def test_length_cap_counts_folded_letters(self):
        self.assertEqual(slugify("Straße " * 20), ("strasse-" * 8)[:60])


if __name__ == "__main__":
    unittest.main()
