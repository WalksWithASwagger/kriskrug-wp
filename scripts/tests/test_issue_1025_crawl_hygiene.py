import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SNIPPET = ROOT / "fixes/issue-1025-crawl-hygiene.php"
APPLY = ROOT / "fixes/issue-1025-apply.md"
FIXES_README = ROOT / "fixes/README.md"
SNIPPET_8 = ROOT / "fixes/gsc-404-query-param-canonicalize.php"
POLICY_331 = ROOT / "fixes/issue-331-archive-sitemap-policy-v2.php"


class Issue1025CrawlHygieneTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SNIPPET.read_text(encoding="utf-8")
        cls.apply = APPLY.read_text(encoding="utf-8")
        cls.fixes_readme = FIXES_README.read_text(encoding="utf-8")
        cls.snippet_8 = SNIPPET_8.read_text(encoding="utf-8")
        cls.policy_331 = POLICY_331.read_text(encoding="utf-8")
        cls.behavior = cls._run_php_harness()

    @staticmethod
    def _run_php_harness():
        snippet_path = json.dumps(str(SNIPPET))
        harness = f"""<?php
$is_admin = false;
$is_feed = false;
$is_comment_feed = false;
$is_tag = false;
$is_author = false;
$is_category = false;
$query_vars = array('paged' => 0, 'page' => 0);
$queried_object = null;
$queried_object_id = 0;
$home_page = null;
$redirects = array();

class WP_Post {{
    public $ID;
    public $post_status;
    public function __construct($id, $status = 'publish') {{
        $this->ID = $id;
        $this->post_status = $status;
    }}
}}

class WP_Term {{
    public $term_id;
    public $taxonomy;
    public function __construct($id, $taxonomy) {{
        $this->term_id = $id;
        $this->taxonomy = $taxonomy;
    }}
}}

class WP_Error {{
}}

function add_action() {{
    return true;
}}

function add_filter() {{
    return true;
}}

function is_admin() {{
    global $is_admin;
    return $is_admin;
}}

function wp_doing_ajax() {{
    return false;
}}

function wp_doing_cron() {{
    return false;
}}

function is_feed() {{
    global $is_feed;
    return $is_feed;
}}

function is_comment_feed() {{
    global $is_comment_feed;
    return $is_comment_feed;
}}

function is_tag() {{
    global $is_tag;
    return $is_tag;
}}

function is_author() {{
    global $is_author;
    return $is_author;
}}

function is_category() {{
    global $is_category;
    return $is_category;
}}

function get_query_var($key) {{
    global $query_vars;
    return $query_vars[$key] ?? 0;
}}

function get_queried_object() {{
    global $queried_object;
    return $queried_object;
}}

function get_queried_object_id() {{
    global $queried_object_id;
    return $queried_object_id;
}}

function get_term_link($term) {{
    if (!$term instanceof WP_Term) {{
        return new WP_Error();
    }}
    return 'https://kriskrug.co/tag/' . $term->term_id . '/';
}}

function get_author_posts_url($author_id) {{
    return 'https://kriskrug.co/author/kk/';
}}

function is_wp_error($thing) {{
    return $thing instanceof WP_Error;
}}

function get_page_by_path($path) {{
    global $home_page;
    if ($path !== 'home') {{
        return null;
    }}
    return $home_page;
}}

function home_url($path = '/') {{
    return 'https://kriskrug.co' . $path;
}}

function absint($value) {{
    return abs((int) $value);
}}

function sanitize_key($value) {{
    return strtolower((string) $value);
}}

function sanitize_text_field($value) {{
    return (string) $value;
}}

function wp_unslash($value) {{
    return $value;
}}

function wp_parse_url($url, $component = -1) {{
    return parse_url($url, $component);
}}

function wp_safe_redirect($location, $status = 302, $x_redirect_by = 'WordPress') {{
    global $redirects;
    $redirects[] = array(
        'location' => $location,
        'status' => $status,
        'by' => $x_redirect_by,
    );
}}

function remove_query_arg($keys, $query) {{
    $keys = (array) $keys;
    $parts = parse_url($query);
    if (empty($parts['query'])) {{
        return $query;
    }}
    parse_str($parts['query'], $qs);
    foreach ($keys as $key) {{
        unset($qs[$key]);
    }}
    $scheme = isset($parts['scheme']) ? $parts['scheme'] . '://' : '';
    $host = $parts['host'] ?? '';
    $path = $parts['path'] ?? '';
    $base = $scheme . $host . $path;
    if (!$qs) {{
        return $base;
    }}
    return $base . '?' . http_build_query($qs);
}}

$_SERVER['REQUEST_METHOD'] = 'GET';
$_SERVER['REQUEST_URI'] = '/home/';

require {snippet_path};

$cases = array();

$cases['home_alias_slash'] = kk_1025_is_home_alias_path('/home/');
$cases['home_alias_bare'] = kk_1025_is_home_alias_path('/home');
$cases['home_alias_nested'] = kk_1025_is_home_alias_path('/home/generative-ai-1/');
$cases['home_alias_root'] = kk_1025_is_home_alias_path('/');

$_SERVER['REQUEST_URI'] = '/home/';
$cases['should_redirect_home'] = kk_1025_should_redirect_home_alias();

$_SERVER['REQUEST_URI'] = '/home/generative-ai-1/';
$cases['should_not_redirect_nested_home'] = kk_1025_should_redirect_home_alias();

$_SERVER['REQUEST_URI'] = '/home/';
$_SERVER['REQUEST_METHOD'] = 'POST';
$cases['should_not_redirect_home_post'] = kk_1025_should_redirect_home_alias();
$_SERVER['REQUEST_METHOD'] = 'GET';

$is_feed = true;
$is_tag = true;
$cases['should_redirect_tag_feed'] = kk_1025_should_redirect_archive_feed();

$is_tag = false;
$is_author = true;
$cases['should_redirect_author_feed'] = kk_1025_should_redirect_archive_feed();

$is_author = false;
$is_category = true;
$cases['should_not_redirect_category_feed'] = kk_1025_should_redirect_archive_feed();

$is_category = false;
$is_comment_feed = true;
$cases['should_not_redirect_comment_feed'] = kk_1025_should_redirect_archive_feed();

$is_feed = true;
$is_comment_feed = false;
$is_tag = false;
$is_author = false;
$cases['should_not_redirect_main_feed'] = kk_1025_should_redirect_archive_feed();

$is_feed = false;
$is_author = true;
$query_vars['paged'] = 2;
$cases['should_redirect_author_page_2'] = kk_1025_should_redirect_author_paged();

$query_vars['paged'] = 1;
$cases['should_not_redirect_author_page_1'] = kk_1025_should_redirect_author_paged();

$is_feed = true;
$query_vars['paged'] = 2;
$cases['should_not_treat_author_feed_as_paged'] = kk_1025_should_redirect_author_paged();

$is_feed = false;
$is_author = false;
$query_vars['paged'] = 2;
$cases['should_not_redirect_blog_page_2'] = kk_1025_should_redirect_author_paged();

$is_tag = true;
$queried_object = new WP_Term(246, 'post_tag');
$cases['tag_feed_target'] = kk_1025_archive_feed_target_url();

$is_tag = false;
$is_author = true;
$queried_object_id = 1;
$cases['author_feed_target'] = kk_1025_archive_feed_target_url();
$cases['author_first_page'] = kk_1025_author_first_page_url();

$is_author = false;
$cases['main_feed_has_no_archive_target'] = kk_1025_archive_feed_target_url();

$cases['strip_share'] = kk_1025_strip_tracking_query_args(
    'https://kriskrug.co/about/?share=twitter&nb=1&utm_source=x'
);
$cases['strip_clean'] = kk_1025_strip_tracking_query_args('https://kriskrug.co/about/');

$home_page = new WP_Post(2315, 'publish');
$cases['home_permalink'] = kk_1025_rewrite_home_page_link('https://kriskrug.co/home/', 2315);
$cases['other_permalink'] = kk_1025_rewrite_home_page_link('https://kriskrug.co/about/', 12);

$sitemap_pages = kk_1025_exclude_home_from_page_sitemap(array('post__not_in' => array(9)), 'page');
$sitemap_posts = kk_1025_exclude_home_from_page_sitemap(array('post__not_in' => array()), 'post');
$cases['sitemap_page_excludes_home'] = $sitemap_pages['post__not_in'];
$cases['sitemap_posts_untouched'] = $sitemap_posts['post__not_in'];

$home_page = new WP_Post(2315, 'draft');
$cases['draft_home_stays_in_sitemap'] = kk_1025_exclude_home_from_page_sitemap(array(), 'page');

echo json_encode($cases, JSON_THROW_ON_ERROR);
"""
        result = subprocess.run(
            ["php"],
            input=harness,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            raise AssertionError(result.stderr or result.stdout)
        return json.loads(result.stdout)

    def test_php_syntax_and_narrow_hooks(self):
        result = subprocess.run(
            ["php", "-l", str(SNIPPET)],
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertIn("No syntax errors detected", result.stdout)
        self.assertIn("add_action( 'template_redirect', 'kk_1025_redirect_home_alias', -1 );", self.source)
        self.assertIn("add_filter( 'feed_links_extra_show_tag_feed', '__return_false' );", self.source)
        self.assertIn("add_filter( 'feed_links_extra_show_author_feed', '__return_false' );", self.source)
        self.assertNotIn("robots_txt", self.source)
        self.assertNotIn("wp_robots", self.source)
        self.assertNotIn("feed_links_extra_show_category_feed", self.source)
        self.assertIn("It does NOT:", self.source)

    def test_home_alias_is_exact_and_single_target(self):
        self.assertTrue(self.behavior["home_alias_slash"])
        self.assertTrue(self.behavior["home_alias_bare"])
        self.assertFalse(self.behavior["home_alias_nested"])
        self.assertFalse(self.behavior["home_alias_root"])
        self.assertTrue(self.behavior["should_redirect_home"])
        self.assertFalse(self.behavior["should_not_redirect_nested_home"])
        self.assertFalse(self.behavior["should_not_redirect_home_post"])
        self.assertEqual("https://kriskrug.co/", self.behavior["home_permalink"])
        self.assertEqual("https://kriskrug.co/about/", self.behavior["other_permalink"])
        self.assertEqual([9, 2315], self.behavior["sitemap_page_excludes_home"])
        self.assertEqual([], self.behavior["sitemap_posts_untouched"])
        self.assertEqual([], self.behavior["draft_home_stays_in_sitemap"])

    def test_archive_feeds_redirect_without_touching_main_rss(self):
        self.assertTrue(self.behavior["should_redirect_tag_feed"])
        self.assertTrue(self.behavior["should_redirect_author_feed"])
        self.assertFalse(self.behavior["should_not_redirect_category_feed"])
        self.assertFalse(self.behavior["should_not_redirect_comment_feed"])
        self.assertFalse(self.behavior["should_not_redirect_main_feed"])
        self.assertEqual("https://kriskrug.co/tag/246/", self.behavior["tag_feed_target"])
        self.assertEqual("https://kriskrug.co/author/kk/", self.behavior["author_feed_target"])
        self.assertEqual("", self.behavior["main_feed_has_no_archive_target"])

    def test_only_unnecessary_author_pagination_is_collapsed(self):
        self.assertTrue(self.behavior["should_redirect_author_page_2"])
        self.assertFalse(self.behavior["should_not_redirect_author_page_1"])
        self.assertFalse(self.behavior["should_not_treat_author_feed_as_paged"])
        self.assertFalse(self.behavior["should_not_redirect_blog_page_2"])
        self.assertEqual("https://kriskrug.co/author/kk/", self.behavior["author_first_page"])

    def test_parameter_strip_keeps_unrelated_query_args(self):
        self.assertEqual(
            "https://kriskrug.co/about/?utm_source=x",
            self.behavior["strip_share"],
        )
        self.assertEqual("https://kriskrug.co/about/", self.behavior["strip_clean"])
        self.assertIn("share", self.snippet_8)
        self.assertIn("nb", self.snippet_8)
        self.assertIn("amp", self.snippet_8)
        self.assertIn("kk_gsc404_redirect_tracking_query_params", self.snippet_8)

    def test_does_not_broaden_331_archive_robots(self):
        self.assertIn("kk_archive_policy_v2_robots", self.policy_331)
        self.assertIn("noindex", self.policy_331)
        self.assertNotIn("kk_archive_policy_v2_robots", self.source)
        self.assertNotIn("is_category()", self.source)

    def test_apply_note_locks_live_before_after_and_gates(self):
        for expected in (
            "x-redirect-by: redirection",
            "KK GSC404",
            "https://kriskrug.co/feed/",
            "SEO LGTM",
            "Do not change",
            "robots.txt",
            "noindex, follow",
            "Deactivate the snippet",
            "20 `<item>`s",
        ):
            self.assertIn(expected, self.apply)
        self.assertIn("issue-1025-crawl-hygiene.php", self.fixes_readme)
        self.assertIn("PREP ONLY", self.source)
        self.assertIn("Not live; prep only", self.fixes_readme)


if __name__ == "__main__":
    unittest.main()
