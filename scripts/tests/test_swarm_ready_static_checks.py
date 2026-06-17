import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class SwarmReadyStaticChecks(unittest.TestCase):
    def test_aurora_search_blocks_get_accessible_names(self):
        functions = (ROOT / "theme/kk-aurora/functions.php").read_text()

        self.assertIn("function enhance_search_block_accessibility", functions)
        self.assertIn("set_attribute('role', 'search')", functions)
        self.assertIn("set_attribute('aria-label', $label)", functions)
        self.assertIn("Submit search", functions)

    def test_writing_archive_exposes_category_feed_discovery(self):
        functions = (ROOT / "theme/kk-aurora/functions.php").read_text()
        home_template = (ROOT / "theme/kk-aurora/templates/home.html").read_text()

        self.assertIn("function writing_archive_category_feed_discovery", functions)
        self.assertIn("get_category_feed_link", functions)
        self.assertIn("rel=\\\"alternate\\\" type=\\\"application/rss+xml\\\"", functions)

        feed_links = re.findall(r'href=\"/category/[^\"]+/feed/\"', home_template)
        self.assertGreaterEqual(len(feed_links), 8)
        self.assertIn('aria-label="Category RSS feeds"', home_template)

    def test_twitter_card_snippet_uses_current_site_handle(self):
        snippet = (ROOT / "fixes/issue-43-twitter-cards.php").read_text()
        note = (ROOT / "fixes/issue-43-twitter-cards.md").read_text()

        self.assertIn("KK_ISSUE_43_TWITTER_HANDLE', '@feelmoreplants'", snippet)
        self.assertNotIn("@YourTwitterHandle", snippet)
        self.assertIn("@feelmoreplants", note)


if __name__ == "__main__":
    unittest.main()
