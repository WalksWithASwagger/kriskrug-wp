import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SNIPPET = ROOT / "fixes/issue-331-archive-sitemap-policy-v2.php"
APPLY = ROOT / "fixes/issue-331-apply.md"
V1 = ROOT / "fixes/issue-331-archive-sitemap-policy.php"


class Issue331ArchivePolicyV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SNIPPET.read_text(encoding="utf-8")
        cls.apply = APPLY.read_text(encoding="utf-8")
        cls.v1 = V1.read_text(encoding="utf-8")
        cls.behavior = cls._run_php_harness()

    @staticmethod
    def _run_php_harness():
        snippet_path = json.dumps(str(SNIPPET))
        harness = f"""<?php
$archive_context = 'single';

function add_filter() {{
    return true;
}}

function is_author() {{
    global $archive_context;
    return 'author' === $archive_context;
}}

function is_tag() {{
    global $archive_context;
    return 'tag' === $archive_context;
}}

function is_category() {{
    global $archive_context;
    return 'category' === $archive_context;
}}

function is_date() {{
    global $archive_context;
    return 'date' === $archive_context;
}}

function is_tax() {{
    global $archive_context;
    return 'tax' === $archive_context;
}}

require {snippet_path};

$provider          = new stdClass();
$users_result      = kk_archive_policy_v2_sitemap_provider($provider, 'users');
$posts_result      = kk_archive_policy_v2_sitemap_provider($provider, 'posts');
$taxonomies_result = kk_archive_policy_v2_sitemap_taxonomies(
    array('category' => new stdClass(), 'post_tag' => new stdClass(), 'genre' => new stdClass())
);

$robots_results = array();
foreach (array('author', 'tag', 'category', 'date', 'tax') as $context) {{
    $archive_context = $context;
    $robots_results[$context] = kk_archive_policy_v2_robots(
        array(
            'index'             => true,
            'nofollow'          => true,
            'none'              => true,
            'max-image-preview' => 'large',
        )
    );
}}

$archive_context = 'single';
$singular_robots = array('max-image-preview' => 'large');
$singular_result = kk_archive_policy_v2_robots($singular_robots);

echo json_encode(
    array(
        'sitemaps' => array(
            'users_removed'   => false === $users_result,
            'posts_preserved' => $provider === $posts_result,
            'taxonomy_keys'   => array_keys($taxonomies_result),
        ),
        'robots' => array(
            'archives'           => $robots_results,
            'singular_unchanged' => $singular_robots === $singular_result,
        ),
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

    def test_snippet_has_valid_php_and_registers_only_narrow_filters(self):
        result = subprocess.run(
            ["php", "-l", str(SNIPPET)],
            text=True,
            capture_output=True,
            check=True,
        )

        self.assertIn("No syntax errors detected", result.stdout)
        self.assertEqual(3, self.source.count("add_filter("))
        for registration in (
            "add_filter( 'wp_sitemaps_add_provider', 'kk_archive_policy_v2_sitemap_provider', PHP_INT_MAX, 2 );",
            "add_filter( 'wp_sitemaps_taxonomies', 'kk_archive_policy_v2_sitemap_taxonomies', PHP_INT_MAX );",
            "add_filter( 'wp_robots', 'kk_archive_policy_v2_robots', PHP_INT_MAX );",
        ):
            self.assertIn(registration, self.source)
        self.assertNotIn("template_redirect", self.source)
        self.assertNotIn("wp_sitemaps_post_types", self.source)
        self.assertNotIn("rest_endpoints", self.source)
        self.assertNotIn("robots_txt", self.source)

    def test_v1_is_preserved_and_does_not_cover_dates(self):
        self.assertTrue(V1.is_file())
        self.assertNotIn("is_date()", self.v1)
        self.assertIn("is_date()", self.source)

    def test_archive_providers_are_removed_without_touching_posts_or_pages(self):
        sitemaps = self.behavior["sitemaps"]

        self.assertTrue(sitemaps["users_removed"])
        self.assertEqual([], sitemaps["taxonomy_keys"])
        self.assertTrue(sitemaps["posts_preserved"])

    def test_archive_robots_are_noindex_follow_without_conflicts(self):
        for context, robots in self.behavior["robots"]["archives"].items():
            with self.subTest(context=context):
                self.assertIs(True, robots["noindex"])
                self.assertIs(True, robots["follow"])
                self.assertEqual("large", robots["max-image-preview"])
                self.assertNotIn("index", robots)
                self.assertNotIn("nofollow", robots)
                self.assertNotIn("none", robots)

        self.assertTrue(self.behavior["robots"]["singular_unchanged"])

    def test_apply_note_locks_live_inventory_and_gates(self):
        for expected in (
            "1,668",
            "973",
            "633",
            "wp-sitemap-users-1.xml",
            "Option A",
            "Do not change `robots.txt`",
            "Deactivate the snippet",
            "#767",
            "merged PR #793",
            "2026-08-16 19:28 PT",
        ):
            self.assertIn(expected, self.apply)


if __name__ == "__main__":
    unittest.main()
