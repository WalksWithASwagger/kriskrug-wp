import json
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FUNCTIONS = ROOT / "theme/kk-aurora/functions.php"


def render_archive_identity(*, page: int, page_url: str, is_home: bool = True) -> dict:
    functions_path = json.dumps(str(FUNCTIONS))
    theme_path = json.dumps(str(FUNCTIONS.parent))
    page_url_literal = json.dumps(page_url)
    is_home_literal = "true" if is_home else "false"
    php = textwrap.dedent(
        f"""
        <?php
        define('ABSPATH', __DIR__);

        $GLOBALS['kk_test_hooks'] = [];
        $GLOBALS['kk_test_page'] = {page};
        $GLOBALS['kk_test_page_url'] = {page_url_literal};
        $GLOBALS['kk_test_is_home'] = {is_home_literal};

        function add_action($hook, $callback, $priority = 10, $accepted_args = 1) {{
            $GLOBALS['kk_test_hooks'][] = compact('hook', 'callback', 'priority', 'accepted_args');
        }}
        function add_filter($hook, $callback, $priority = 10, $accepted_args = 1) {{}}
        function get_template_directory() {{ return {theme_path}; }}
        function is_home() {{ return $GLOBALS['kk_test_is_home']; }}
        function is_front_page() {{ return false; }}
        function get_query_var($name, $default = '') {{
            return $name === 'paged' ? $GLOBALS['kk_test_page'] : $default;
        }}
        function get_pagenum_link($page, $escape = true) {{
            return $GLOBALS['kk_test_page_url'];
        }}
        function wp_parse_url($url, $component = -1) {{ return parse_url($url, $component); }}
        function home_url($path = '') {{ return 'https://kriskrug.co' . $path; }}
        function get_option($name, $default = false) {{
            return $name === 'page_for_posts' ? 4242 : $default;
        }}
        function get_permalink($post = 0) {{ return 'https://kriskrug.co/blog/'; }}
        function get_post_meta($post_id, $key, $single = false) {{ return ''; }}
        function wp_strip_all_tags($value) {{ return strip_tags($value); }}
        function trailingslashit($value) {{ return rtrim($value, '/') . '/'; }}
        function user_trailingslashit($value, $type = '') {{ return trailingslashit($value); }}
        function esc_url($value) {{ return $value; }}
        function esc_url_raw($value) {{ return $value; }}

        require {functions_path};

        $canonical = KK_Aurora\\writing_archive_canonical_url();
        ob_start();
        KK_Aurora\\render_writing_archive_canonical();
        $link = ob_get_clean();
        $tags = KK_Aurora\\writing_archive_open_graph_fallback([
            'og:url' => 'https://kriskrug.co/',
            'og:title' => 'Writing — Kris Krug',
        ]);
        $canonical_hooks = array_values(array_filter(
            $GLOBALS['kk_test_hooks'],
            fn($row) => $row['callback'] === 'KK_Aurora\\\\render_writing_archive_canonical'
        ));

        echo json_encode([
            'canonical' => $canonical,
            'link' => $link,
            'tags' => $tags,
            'canonical_hooks' => $canonical_hooks,
        ], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
        """
    ).lstrip()

    with tempfile.NamedTemporaryFile("w", suffix=".php", encoding="utf-8") as handle:
        handle.write(php)
        handle.flush()
        result = subprocess.run(
            ["php", handle.name],
            check=True,
            capture_output=True,
            text=True,
        )
    return json.loads(result.stdout)


class Issue347BlogCanonicalTests(unittest.TestCase):
    def test_page_one_strips_irrelevant_query_parameters(self):
        result = render_archive_identity(
            page=1,
            page_url="https://kriskrug.co/blog/?utm_source=canonical-test",
        )

        self.assertEqual("https://kriskrug.co/blog/", result["canonical"])
        self.assertEqual(result["canonical"], result["tags"]["og:url"])
        self.assertEqual(
            '<link rel="canonical" href="https://kriskrug.co/blog/" />',
            result["link"].strip(),
        )
        self.assertEqual(1, result["link"].count('rel="canonical"'))

    def test_page_two_keeps_its_own_clean_paginated_url(self):
        result = render_archive_identity(
            page=2,
            page_url="https://kriskrug.co/blog/page/2/?utm_medium=canonical-test",
        )

        self.assertEqual("https://kriskrug.co/blog/page/2/", result["canonical"])
        self.assertEqual(result["canonical"], result["tags"]["og:url"])
        self.assertIn('href="https://kriskrug.co/blog/page/2/"', result["link"])
        self.assertEqual("Writing — Kris Krug", result["tags"]["og:title"])

    def test_non_blog_routes_do_not_gain_an_archive_canonical(self):
        result = render_archive_identity(
            page=1,
            page_url="https://kriskrug.co/about/",
            is_home=False,
        )

        self.assertEqual("", result["canonical"])
        self.assertEqual("", result["link"])
        self.assertEqual("https://kriskrug.co/", result["tags"]["og:url"])

    def test_canonical_renderer_has_one_early_head_hook(self):
        result = render_archive_identity(
            page=1,
            page_url="https://kriskrug.co/blog/",
        )

        self.assertEqual(1, len(result["canonical_hooks"]))
        self.assertLess(result["canonical_hooks"][0]["priority"], 5)


if __name__ == "__main__":
    unittest.main()
