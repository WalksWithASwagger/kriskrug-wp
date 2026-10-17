"""#1131: sitewide chrome and the page sitemap point at final URLs."""

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
THEME = ROOT / "theme/kk-aurora"
HEADER = THEME / "parts/header.html"
FOOTER = THEME / "parts/footer.html"
FRONT = THEME / "templates/front-page.html"
CHROME = (HEADER, FOOTER, FRONT)
SNIPPET = ROOT / "fixes/issue-1131-exclude-home-sitemap.php"
APPLY = ROOT / "fixes/issue-1131-apply.md"
FIXES_README = ROOT / "fixes/README.md"
SCHEMA = ROOT / "fixes/schema-snippets-deployed.php"
EVENTS_CATALOG = ROOT / "scripts/events_page/events-catalog.yaml"
SNIPPET_1025 = ROOT / "fixes/issue-1025-crawl-hygiene.php"

FORBIDDEN_HREFS = (
    'href="/services/"',
    'href="https://kriskrug.co/services/"',
    'href="http://kriskrug.co/services/"',
    'href="https://futureproof.website/"',
    'href="http://futureproof.website/"',
)


class Issue1131FinalUrlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.header = HEADER.read_text(encoding="utf-8")
        cls.footer = FOOTER.read_text(encoding="utf-8")
        cls.front = FRONT.read_text(encoding="utf-8")
        cls.snippet = SNIPPET.read_text(encoding="utf-8")
        cls.apply = APPLY.read_text(encoding="utf-8")
        cls.fixes_readme = FIXES_README.read_text(encoding="utf-8")
        cls.schema = SCHEMA.read_text(encoding="utf-8")
        cls.catalog = EVENTS_CATALOG.read_text(encoding="utf-8")
        cls.behavior = cls._run_php_harness()

    @staticmethod
    def _run_php_harness():
        snippet_path = json.dumps(str(SNIPPET))
        harness = f"""<?php
class WP_Post {{
    public $ID;
    public $post_status;
    public function __construct($id, $status = 'publish') {{
        $this->ID = $id;
        $this->post_status = $status;
    }}
}}

function add_filter() {{
    return true;
}}

function get_page_by_path($path) {{
    global $home_page;
    if ($path !== 'home') {{
        return null;
    }}
    return $home_page;
}}

function absint($value) {{
    return abs((int) $value);
}}

$home_page = new WP_Post(2315, 'publish');
require {snippet_path};

$sitemap_pages = kk_1131_exclude_home_from_page_sitemap(array('post__not_in' => array(9)), 'page');
$sitemap_posts = kk_1131_exclude_home_from_page_sitemap(array('post__not_in' => array()), 'post');
$draft_home = new WP_Post(2315, 'draft');
$home_page = $draft_home;
$draft_result = kk_1131_exclude_home_from_page_sitemap(array(), 'page');

echo json_encode(
    array(
        'sitemap_page_excludes_home' => $sitemap_pages['post__not_in'],
        'sitemap_posts_untouched' => $sitemap_posts['post__not_in'],
        'draft_home_stays_in_sitemap' => $draft_result,
    ),
    JSON_THROW_ON_ERROR
);
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

    def test_required_paths_exist(self):
        for path in CHROME + (SNIPPET, APPLY, SCHEMA, EVENTS_CATALOG, SNIPPET_1025):
            self.assertTrue(path.is_file(), path)

    def test_header_footer_and_homepage_use_final_hrefs(self):
        for path, source in (
            (HEADER, self.header),
            (FOOTER, self.footer),
            (FRONT, self.front),
        ):
            for needle in FORBIDDEN_HREFS:
                self.assertNotIn(needle, source, f"{path}: {needle}")
            self.assertIn('href="/generative-ai-services/"', source, path)

        self.assertIn('href="https://www.futureproof.website/"', self.footer)
        self.assertNotIn("https://futureproof.website/", self.footer)
        self.assertIn("Work with me", self.header)
        self.assertIn("Work with me", self.footer)
        self.assertIn("Futureproof Festival", self.footer)

    def test_events_catalog_futureproof_uses_www_host(self):
        self.assertIn("url: https://www.futureproof.website/", self.catalog)
        self.assertNotIn("url: https://futureproof.website/", self.catalog)

    def test_home_page_is_excluded_from_page_sitemap_only(self):
        self.assertEqual([9, 2315], self.behavior["sitemap_page_excludes_home"])
        self.assertEqual([], self.behavior["sitemap_posts_untouched"])
        self.assertEqual([], self.behavior["draft_home_stays_in_sitemap"])
        self.assertIn("wp_sitemaps_posts_query_args", self.snippet)
        self.assertIn("kk_1131_exclude_home_from_page_sitemap", self.snippet)
        self.assertIn("2315", self.snippet)
        self.assertIn("get_page_by_path( 'home' )", self.snippet)

    def test_sitemap_snippet_is_narrow_and_prep_only(self):
        result = subprocess.run(
            ["php", "-l", str(SNIPPET)],
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertIn("No syntax errors detected", result.stdout)
        self.assertEqual(1, self.snippet.count("add_filter("))
        self.assertNotIn("add_action(", self.snippet)
        self.assertNotIn("template_redirect", self.snippet)
        self.assertNotIn("wp_robots", self.snippet)
        self.assertNotIn("robots_txt", self.snippet)
        self.assertNotIn("kk_schema_emit", self.snippet)
        self.assertNotIn("application/ld+json", self.snippet)
        self.assertIn("PREP ONLY", self.snippet)
        self.assertIn("issue-1131-exclude-home-sitemap.php", self.fixes_readme)
        self.assertIn("Not live; prep only", self.fixes_readme)
        self.assertIn("/home/", self.apply)
        self.assertIn("2315", self.apply)
        self.assertIn("#1114", self.apply)
        self.assertIn("Do **not** activate", self.apply)
        self.assertIn("issue-1025-crawl-hygiene.php", self.apply)

    def test_person_schema_is_untouched_by_this_packet(self):
        self.assertNotIn("kk_1131", self.schema)
        self.assertNotIn("#1131", self.schema)
        self.assertIn("https://www.futureproof.website/", self.schema)


if __name__ == "__main__":
    unittest.main()
