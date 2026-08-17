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

    def test_both_hands_full_links_to_make_culture_post(self):
        html, applied = text_polish.auto_link_first_occurrence(
            "<p>Both Hands Full is the project.</p>"
        )
        self.assertEqual(len(applied), 1)
        self.assertEqual(
            applied[0]["url"],
            "https://kriskrug.co/2026/05/16/make-culture-not-content/",
        )
        self.assertIn(
            'title="Both Hands Full: Make Culture, Not Content"',
            html,
        )
        self.assertNotIn("—", html)

        # Distinct phrase must not steal the Both Hands Full target.
        html2, applied2 = text_polish.auto_link_first_occurrence(
            "<p>Both Hands on the Power Cord is a different post.</p>"
        )
        self.assertFalse(
            any(
                item.get("url")
                == "https://kriskrug.co/2026/05/16/make-culture-not-content/"
                for item in applied2
            )
        )

    def test_link_map_titles_have_no_em_dashes(self):
        for _pattern, _url, title in text_polish.LINK_MAP:
            if title:
                self.assertNotIn("—", title, msg=title)


if __name__ == "__main__":
    unittest.main()
