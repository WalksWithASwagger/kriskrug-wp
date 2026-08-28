import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SNIPPET = ROOT / "fixes/issue-767-hide-user-sitemap.php"
FIXES_README = ROOT / "fixes/README.md"


class Issue767UserSitemapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SNIPPET.read_text(encoding="utf-8")
        cls.fixes_readme = FIXES_README.read_text(encoding="utf-8")
        cls.behavior = cls._run_php_harness()

    @staticmethod
    def _run_php_harness():
        snippet_path = json.dumps(str(SNIPPET))
        harness = f"""<?php
function add_filter() {{
    return true;
}}

require {snippet_path};

$provider          = new stdClass();
$users_result      = kk_767_sitemap_provider($provider, 'users');
$posts_result      = kk_767_sitemap_provider($provider, 'posts');
$taxonomies_result = kk_767_sitemap_provider($provider, 'taxonomies');

echo json_encode(
    array(
        'users_removed'        => false === $users_result,
        'posts_preserved'      => $provider === $posts_result,
        'taxonomies_preserved' => $provider === $taxonomies_result,
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

    def test_removes_only_the_users_sitemap_provider(self):
        self.assertTrue(self.behavior["users_removed"])
        self.assertTrue(self.behavior["posts_preserved"])
        self.assertTrue(self.behavior["taxonomies_preserved"])

    def test_registers_one_narrow_filter_and_no_archive_policy(self):
        result = subprocess.run(
            ["php", "-l", str(SNIPPET)],
            text=True,
            capture_output=True,
            check=True,
        )

        self.assertIn("No syntax errors detected", result.stdout)
        self.assertEqual(1, self.source.count("add_filter("))
        self.assertIn(
            "add_filter('wp_sitemaps_add_provider', "
            "'kk_767_sitemap_provider', PHP_INT_MAX, 2);",
            self.source,
        )
        for excluded_surface in (
            "wp_sitemaps_taxonomies",
            "wp_robots",
            "template_redirect",
            "rest_pre_dispatch",
        ):
            self.assertNotIn(excluded_surface, self.source)

    def test_documents_prep_only_scope_and_rollback(self):
        for expected in (
            "PREP ONLY",
            "Not deployed",
            "issue-331-archive-sitemap-policy",
            "Rollback",
            "scripts/check_user_enumeration.sh",
        ):
            self.assertIn(expected, self.source)

        self.assertIn("issue-767-hide-user-sitemap.php", self.fixes_readme)
        self.assertIn("users sitemap provider only", self.fixes_readme)


if __name__ == "__main__":
    unittest.main()
