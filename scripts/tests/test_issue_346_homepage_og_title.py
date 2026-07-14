import html
import json
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
THEME_FUNCTIONS = ROOT / "theme/kk-aurora/functions.php"
DOCUMENT_TITLE = "Kris Krug | AI Keynote Speaker & Creative Technologist"
META_PATTERN = re.compile(
    r'<meta (?:property|name)="(?P<name>[^"]+)" content="(?P<content>[^"]*)" />'
)


class Issue346HomepageOpenGraphTitleTests(unittest.TestCase):
    @staticmethod
    def _run_php_harness(*, snippet_guard=False):
        functions_path = json.dumps(str(THEME_FUNCTIONS))
        guard = "define('KK_OG_SNIPPET_ACTIVE', true);" if snippet_guard else ""
        harness = f"""<?php
define('ABSPATH', __DIR__);
{guard}

class WP_Post {{
    public int $ID = 42;
    public string $post_content = '';
}}

$current_title = '';
$queried_post = new WP_Post();

function add_action(...$args) {{}}
function add_filter(...$args) {{}}
function is_front_page() {{ return true; }}
function is_home() {{ return false; }}
function is_page($page = '') {{ return false; }}
function is_feed() {{ return false; }}
function is_singular($post_type = '') {{ return '' === $post_type; }}
function get_option($name, $default = '') {{ return $default; }}
function get_bloginfo($show = '') {{
    return 'name' === $show ? 'Kris Krug' : 'Keynotes and creative technology';
}}
function wp_get_document_title() {{ return {json.dumps(DOCUMENT_TITLE)}; }}
function home_url($path = '') {{ return 'https://kriskrug.co' . $path; }}
function get_queried_object() {{ global $queried_post; return $queried_post; }}
function get_the_title($post = null) {{ global $current_title; return $current_title; }}
function get_permalink($post = null) {{ return 'https://kriskrug.co/about/'; }}
function get_the_post_thumbnail_url($post = null, $size = 'post-thumbnail') {{ return false; }}
function has_site_icon() {{ return false; }}
function wp_strip_all_tags($text) {{ return strip_tags((string) $text); }}
function esc_attr($text) {{
    return htmlspecialchars((string) $text, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}}

require {functions_path};

function render_case($title) {{
    global $current_title;
    $current_title = $title;
    ob_start();
    KK_Aurora\\render_social_meta_tags();
    return ob_get_clean();
}}

echo json_encode(
    array(
        'empty'             => render_case(''),
        'whitespace_markup' => render_case("  \\n<span> </span>\\t"),
        'singular'          => render_case('About Kris Krug'),
    ),
    JSON_THROW_ON_ERROR
);
"""
        result = subprocess.run(
            ["php"],
            input=harness,
            text=True,
            capture_output=True,
            check=True,
        )
        return json.loads(result.stdout)

    @staticmethod
    def _meta_values(rendered, name):
        return [
            html.unescape(match.group("content"))
            for match in META_PATTERN.finditer(rendered)
            if match.group("name") == name
        ]

    def test_empty_singular_titles_render_the_document_title_once(self):
        rendered = self._run_php_harness()

        for case in ("empty", "whitespace_markup"):
            with self.subTest(case=case):
                self.assertEqual(
                    [DOCUMENT_TITLE],
                    self._meta_values(rendered[case], "og:title"),
                )

    def test_non_empty_singular_title_still_overrides_document_title(self):
        rendered = self._run_php_harness()

        self.assertEqual(
            ["About Kris Krug"],
            self._meta_values(rendered["singular"], "og:title"),
        )

    def test_snippet_owner_guard_still_suppresses_theme_metadata(self):
        rendered = self._run_php_harness(snippet_guard=True)

        self.assertEqual({"empty": "", "whitespace_markup": "", "singular": ""}, rendered)


if __name__ == "__main__":
    unittest.main()
