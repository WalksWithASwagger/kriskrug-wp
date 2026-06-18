import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GLOSSARY_DIR = ROOT / "content/drafts/ai-glossary-2026-05"


class GlossaryDraftTests(unittest.TestCase):
    def test_markdown_has_enough_alphabetized_terms(self):
        markdown = (GLOSSARY_DIR / "post.md").read_text(encoding="utf-8")
        terms = re.findall(r"^\*\*([^:*]+):\*\*", markdown, re.MULTILINE)

        self.assertGreaterEqual(len(terms), 50)
        self.assertEqual(terms, sorted(terms, key=str.lower))

    def test_html_has_accessible_search_gate(self):
        html = (GLOSSARY_DIR / "post.html").read_text(encoding="utf-8")

        self.assertIn("data-kk-glossary", html)
        self.assertIn("Search glossary terms", html)
        self.assertIn('role="search"', html)
        self.assertIn('aria-live="polite"', html)
        self.assertIn("data-glossary-no-results", html)
        self.assertIn("data-glossary-search-text", html)
        self.assertIn("input.addEventListener('input', update)", html)
        terms = re.findall(r"<article[^>]+data-glossary-term\b", html)
        self.assertGreaterEqual(len(terms), 50)


if __name__ == "__main__":
    unittest.main()
