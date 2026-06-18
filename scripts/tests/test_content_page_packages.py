import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VANCOUVER_AI_DIR = ROOT / "content/drafts/2026-06-11-vancouver-ai-community-page"


class ContentPagePackageTests(unittest.TestCase):
    def test_vancouver_ai_package_carries_public_proof_points(self):
        html = (VANCOUVER_AI_DIR / "post.html").read_text(encoding="utf-8")
        markdown = (VANCOUVER_AI_DIR / "post.md").read_text(encoding="utf-8")
        combined = html + "\n" + markdown

        for marker in ("250+", "3,000+", "94+", "Est. 2023", "T5ANAthZewE"):
            self.assertIn(marker, combined)
        for url in ("https://luma.com/vancouver-ai", "https://bc-ai.ca/membership/"):
            self.assertIn(url, combined)
        self.assertIn("<!-- wp:html -->", html)
        self.assertNotIn("notion.so", combined.lower())
        self.assertNotIn("notionusercontent", combined.lower())


if __name__ == "__main__":
    unittest.main()
