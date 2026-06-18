import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
THEME_DIR = ROOT / "theme/kk-aurora"


class AuroraSkipLinkTests(unittest.TestCase):
    def test_header_skip_link_has_template_targets(self):
        header = (THEME_DIR / "parts/header.html").read_text(encoding="utf-8")

        self.assertIn('class="skip-link"', header)
        self.assertIn('href="#aurora-main"', header)

        missing = []
        for template_path in sorted((THEME_DIR / "templates").glob("*.html")):
            template = template_path.read_text(encoding="utf-8")
            if '"slug":"header"' not in template:
                continue
            if 'id="aurora-main"' not in template:
                missing.append(template_path.name)

        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
