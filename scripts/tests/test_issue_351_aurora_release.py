import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
STYLE = ROOT / "theme/kk-aurora/style.css"
FUNCTIONS = ROOT / "theme/kk-aurora/functions.php"
README = ROOT / "theme/kk-aurora/readme.txt"


class Issue351AuroraReleaseTests(unittest.TestCase):
    def test_release_version_is_consistent(self):
        style = STYLE.read_text(encoding="utf-8")
        functions = FUNCTIONS.read_text(encoding="utf-8")

        style_version = re.search(r"^Version:\s*(\S+)$", style, re.MULTILINE)
        cache_version = re.search(
            r"define\('KK_AURORA_VERSION',\s*'([^']+)'\);",
            functions,
        )

        self.assertIsNotNone(style_version)
        self.assertIsNotNone(cache_version)
        self.assertEqual("1.3.39", style_version.group(1))
        self.assertEqual(style_version.group(1), cache_version.group(1))

    def test_changelog_names_both_metadata_repairs(self):
        readme = README.read_text(encoding="utf-8")

        release_start = readme.index("= 1.3.39 =")
        prior_start = readme.index("= 1.3.38 =")
        release = readme[release_start:prior_start]

        self.assertLess(release_start, prior_start)
        self.assertIn("homepage Open Graph title", release)
        self.assertIn("Blog archive", release)
        self.assertIn("canonical", release)
        self.assertIn("Open Graph URL", release)
        self.assertIn("#346", release)
        self.assertIn("#347", release)

    def test_release_keeps_the_expected_metadata_owners(self):
        functions = FUNCTIONS.read_text(encoding="utf-8")

        self.assertIn("function render_social_meta_tags", functions)
        self.assertIn("KK_OG_SNIPPET_ACTIVE", functions)
        self.assertIn("function writing_archive_canonical_url", functions)
        self.assertIn("function render_writing_archive_canonical", functions)
        self.assertIn("wp_get_document_title()", functions)


if __name__ == "__main__":
    unittest.main()
