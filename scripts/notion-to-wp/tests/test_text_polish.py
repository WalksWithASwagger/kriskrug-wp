import sys
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import text_polish  # noqa: E402


class TextPolishTests(unittest.TestCase):
    def test_purge_em_dashes_normalizes_spacing(self):
        self.assertEqual(
            text_polish.purge_em_dashes("culture—content and people — practice"),
            "culture, content and people, practice",
        )

    def test_purge_em_dashes_preserves_numeric_en_dash_ranges(self):
        self.assertEqual(
            text_polish.purge_em_dashes("Use 2024–2026, not idea – execution."),
            "Use 2024–2026, not idea-execution.",
        )

    def test_polish_text_applies_dash_rules_to_plain_text(self):
        self.assertEqual(
            text_polish.polish_text("AI — culture from 0–5"),
            "AI, culture from 0–5",
        )


if __name__ == "__main__":
    unittest.main()
