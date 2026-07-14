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
        self.assertIn("function public_meta_description", functions)
        self.assertIn("function suppress_jetpack_meta_description", functions)
        self.assertIn("jetpack_seo_meta_tags", functions)
        self.assertIn("function twitter_card_tag_fallbacks", functions)
        self.assertIn("function render_social_meta_tags", functions)
        self.assertIn("$tags = twitter_card_tag_fallbacks($tags);", functions)
        self.assertIn("KK_OG_SNIPPET_ACTIVE", functions)
        self.assertIn("render_social_meta_tags', 5", functions)
        self.assertIn("advanced_seo_description", functions)
        self.assertIn("get_category_feed_link", functions)
        self.assertIn("rel=\\\"alternate\\\" type=\\\"application/rss+xml\\\"", functions)

        feed_links = re.findall(r'href=\"/category/[^\"]+/feed/\"', home_template)
        self.assertGreaterEqual(len(feed_links), 8)
        self.assertIn('aria-label="Category RSS feeds"', home_template)

    def test_aurora_owns_one_standard_meta_description(self):
        functions = (ROOT / "theme/kk-aurora/functions.php").read_text()

        self.assertIn("get_option('advanced_seo_front_page_description', '')", functions)
        self.assertIn("get_post_meta($post->ID, 'advanced_seo_description', true)", functions)
        self.assertIn("$description = writing_archive_meta_description();", functions)
        self.assertIn("$description = term_description();", functions)
        self.assertIn("$tags['description'] = $description;", functions)
        self.assertIn("'og:description' => $description !== '' ? $description", functions)
        self.assertIn("$name === 'description' || str_starts_with($name, 'twitter:')", functions)
        self.assertIn("unset($tags['description']);", functions)
        self.assertIn("KK_OG_SNIPPET_ACTIVE", functions)
        self.assertIn("PHP_INT_MAX", functions)

    def test_aurora_honors_approved_singular_search_titles(self):
        functions = (ROOT / "theme/kk-aurora/functions.php").read_text()
        title_module = (ROOT / "theme/kk-aurora/inc/seo-title.php").read_text()

        self.assertIn("require_once get_template_directory() . '/inc/seo-title.php';", functions)
        self.assertIn("function filter_pre_get_document_title", title_module)
        self.assertIn("'jetpack_seo_html_title'", title_module)
        self.assertIn("wp_strip_all_tags", title_module)
        self.assertIn("'pre_get_document_title'", title_module)
        self.assertIn("PHP_INT_MAX", title_module)

    def test_twitter_card_snippet_uses_current_site_handle(self):
        snippet = (ROOT / "fixes/issue-43-twitter-cards.php").read_text()
        note = (ROOT / "fixes/issue-43-twitter-cards.md").read_text()

        self.assertIn("KK_ISSUE_43_TWITTER_HANDLE', '@feelmoreplants'", snippet)
        self.assertNotIn("@YourTwitterHandle", snippet)
        self.assertIn("@feelmoreplants", note)


if __name__ == "__main__":
    unittest.main()
