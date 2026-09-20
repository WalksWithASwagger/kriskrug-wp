"""#1025 in-repo crawl-waste policy: robots/sitemap/noindex, no live WP."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "fixes/issue-1025-crawl-policy.json"
DOC = ROOT / "docs/current-state/CRAWL-WASTE-AUTHORITY-HUB-2026-09-20.md"
APPLY = ROOT / "fixes/issue-1025-apply.md"
ROBOTS = ROOT / "fixes/robots.txt"
SNIPPET = ROOT / "fixes/issue-1025-crawl-hygiene.php"
CURRENT_STATE = ROOT / "docs/current-state/README.md"
DOCS_INDEX = ROOT / "docs/INDEX.md"
SEO_RUNBOOK = ROOT / "docs/current-state/SEO-INDEXING-RUNBOOK.md"
FIXES_README = ROOT / "fixes/README.md"
PACK = ROOT / "content/drafts/issue-1025-authority-hub"
MODULE = PACK / "organizations-module.html"
EM_DASH = "\u2014"


class Issue1025CrawlPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy = json.loads(POLICY.read_text(encoding="utf-8"))
        cls.doc = DOC.read_text(encoding="utf-8")
        cls.apply = APPLY.read_text(encoding="utf-8")
        cls.robots = ROBOTS.read_text(encoding="utf-8")
        cls.snippet = SNIPPET.read_text(encoding="utf-8")
        cls.module = MODULE.read_text(encoding="utf-8")

    def test_policy_files_exist(self):
        for path in (
            POLICY,
            DOC,
            PACK / "README.md",
            PACK / "STATUS.md",
            MODULE,
            PACK / "contextual-links.md",
            PACK / "thin-legacy-triage.md",
        ):
            self.assertTrue(path.is_file(), path)

    def test_policy_is_in_repo_only(self):
        self.assertEqual(1025, self.policy["issue"])
        self.assertEqual("in_repo_only", self.policy["status"])
        self.assertFalse(self.policy["live_wordpress_changed"])
        self.assertFalse(self.policy["robots"]["change_live"])
        self.assertFalse(self.policy["robots"]["change_repo_source"])
        self.assertTrue(self.policy["noindex"]["do_not_broaden_331"])
        self.assertTrue(self.policy["noindex"]["do_not_bulk_noindex_thin_posts"])
        self.assertTrue(self.policy["feeds"]["do_not_disable_main_rss"])
        self.assertIn("https://kriskrug.co/feed/", self.policy["feeds"]["preserve"])
        self.assertIn("bulk_delete", self.policy["thin_legacy_posts"]["forbidden"])
        self.assertIn("bulk_request_indexing", self.policy["thin_legacy_posts"]["forbidden"])

    def test_robots_recommendations_do_not_block_archives_or_main_feed(self):
        robots = self.policy["robots"]
        self.assertEqual("fixes/robots.txt", robots["repo_source"])
        self.assertIn("Sitemap: https://kriskrug.co/sitemap.xml", robots["keep"])
        self.assertIn("Disallow: /?s=", robots["keep"])
        for forbidden in (
            "Disallow: /tag/",
            "Disallow: /category/",
            "Disallow: /author/",
            "Disallow: /feed/",
            "Disallow: /*/feed/",
            "Sitemap: https://kriskrug.co/news-sitemap.xml",
        ):
            self.assertIn(forbidden, robots["do_not_add"])
            self.assertNotIn(forbidden, self.robots)
        self.assertIn("Sitemap: https://kriskrug.co/sitemap.xml", self.robots)
        self.assertIn("Do **not** add", self.doc)
        self.assertIn("Do not change `robots.txt`", self.apply)
        self.assertNotIn("robots_txt", self.snippet)
        self.assertNotIn("wp_robots", self.snippet)

    def test_sitemap_and_noindex_match_331_and_home_alias(self):
        sitemap = self.policy["sitemap"]
        self.assertEqual(["post", "page"], sitemap["include"])
        self.assertEqual(
            ["users", "category", "post_tag", "page:home"],
            sitemap["exclude"],
        )
        self.assertEqual("home", sitemap["exclude_page_slug"])
        self.assertEqual(2315, sitemap["exclude_page_id"])
        self.assertIn(
            "https://kriskrug.co/news-sitemap.xml",
            sitemap["do_not_submit"],
        )
        self.assertEqual("noindex, follow", self.policy["noindex"]["directive"])
        self.assertEqual(
            ["is_author", "is_tag", "is_category", "is_date", "is_tax"],
            self.policy["noindex"]["keep_classes"],
        )
        self.assertIn("singular_posts", self.policy["noindex"]["do_not_noindex"])
        self.assertIn("https://kriskrug.co/feed/", self.policy["noindex"]["do_not_noindex"])

    def test_docs_are_wired_from_the_front_door(self):
        needle = "CRAWL-WASTE-AUTHORITY-HUB-2026-09-20.md"
        self.assertIn(needle, CURRENT_STATE.read_text(encoding="utf-8"))
        self.assertIn(needle, DOCS_INDEX.read_text(encoding="utf-8"))
        self.assertIn("#1025", SEO_RUNBOOK.read_text(encoding="utf-8"))
        self.assertIn("issue-1025-crawl-policy.json", FIXES_README.read_text(encoding="utf-8"))
        self.assertIn("Not live; prep only", FIXES_README.read_text(encoding="utf-8"))
        self.assertIn("Do not edit", self.doc)
        self.assertIn("in-repo only", self.doc.lower())
        self.assertIn("No live WordPress change", self.doc)

    def test_authority_module_has_descriptive_deep_links(self):
        status = (PACK / "STATUS.md").read_text(encoding="utf-8")
        self.assertIn("paste_ready_not_live", status)
        self.assertIn("Do not invent a WP login", status)
        self.assertNotIn(EM_DASH, self.module)
        required = {
            "https://bc-ai.ca/": "BC + AI Ecosystem Association",
            "https://bc-ai.ca/certification/responsible-ai-professional/": (
                "Responsible AI Professional Certification"
            ),
            "https://www.futureproof.website/festival/": "Futureproof Festival of AI",
            "https://www.futureproof.website/speakers/kris-krug/": "Kris Krüg at Futureproof",
        }
        for url, anchor in required.items():
            self.assertIn(f'href="{url}"', self.module)
            self.assertIn(anchor, self.module)
        policy_links = {
            item["url"]: item["anchor"]
            for item in self.policy["authority_hub"]["required_deep_links"]
        }
        self.assertEqual(required, policy_links)
        links_doc = (PACK / "contextual-links.md").read_text(encoding="utf-8")
        self.assertIn("1–3", links_doc)
        self.assertIn("issue-1030-cross-link-matrix", links_doc)
        triage = (PACK / "thin-legacy-triage.md").read_text(encoding="utf-8")
        self.assertIn("bulk delete", triage.lower())
        self.assertIn("Request Indexing", triage)

    def test_gsc_before_state_is_dated_and_not_claimed_live(self):
        gsc = self.policy["gsc_before_state_dated"]
        self.assertTrue(gsc["do_not_treat_as_live_counts"])
        self.assertEqual(1371, gsc["indexed"])
        self.assertEqual(892, gsc["crawled_currently_not_indexed"])
        self.assertIn("not re-exported", gsc["source"])
        self.assertIn("Dated GSC before-state", self.doc)


if __name__ == "__main__":
    unittest.main()
