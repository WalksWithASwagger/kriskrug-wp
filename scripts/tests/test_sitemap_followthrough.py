"""CI-safe unit tests for the #274 sitemap follow-through helpers.

Parser and GSC-blocker logic only. The live GET path in
sitemap_followthrough.main() is not invoked here.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import sitemap_followthrough as sft  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
RECEIPT = ROOT / "docs/current-state/reports/issue-274-sitemap-followthrough-20260921.md"
PREVIOUS = ROOT / "docs/current-state/reports/issue-274-sitemap-followthrough-20260908.md"
MAKEFILE = ROOT / "Makefile"
SCRIPT = ROOT / "scripts/sitemap_followthrough.py"
RUNBOOK = ROOT / "docs/current-state/SEO-INDEXING-RUNBOOK.md"

INDEX_XML = """<?xml version='1.0' encoding='UTF-8'?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap><loc>https://kriskrug.co/wp-sitemap-posts-post-1.xml</loc></sitemap>
  <sitemap><loc>https://kriskrug.co/wp-sitemap-posts-page-1.xml</loc></sitemap>
</sitemapindex>
"""

STALE_INDEX_XML = """<?xml version='1.0' encoding='UTF-8'?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap><loc>https://kriskrug.co/wp-sitemap-posts-post-1.xml</loc></sitemap>
  <sitemap><loc>https://kriskrug.co/wp-sitemap-posts-page-1.xml</loc></sitemap>
  <sitemap><loc>https://kriskrug.co/wp-sitemap-taxonomies-category-1.xml</loc></sitemap>
  <sitemap><loc>https://kriskrug.co/wp-sitemap-taxonomies-post_tag-1.xml</loc></sitemap>
  <sitemap><loc>https://kriskrug.co/wp-sitemap-users-1.xml</loc></sitemap>
</sitemapindex>
"""

CHILD_XML = """<?xml version='1.0' encoding='UTF-8'?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://kriskrug.co/about/</loc>
    <lastmod>2026-09-20T10:05:25-08:00</lastmod>
  </url>
  <url>
    <loc>https://kriskrug.co/work/</loc>
  </url>
</urlset>
"""

ROBOTS = """# source: fixes/robots.txt
Sitemap: https://kriskrug.co/sitemap.xml

User-agent: *
Disallow: /wp-admin/
"""

INDEXABLE_HTML = """
<html><head>
<meta name="robots" content="max-image-preview:large" />
<meta name="description" content="About Kris Krug." />
<link rel="canonical" href="https://kriskrug.co/about/" />
</head></html>
"""

ARCHIVE_HTML = """
<meta name="robots" content="max-image-preview:large, noindex, follow" />
"""


class ParseTests(unittest.TestCase):
    def test_parse_index_children(self):
        locs = sft.parse_locs(INDEX_XML)
        self.assertEqual(
            [
                "https://kriskrug.co/wp-sitemap-posts-post-1.xml",
                "https://kriskrug.co/wp-sitemap-posts-page-1.xml",
            ],
            locs,
        )
        self.assertEqual(["posts", "pages"], [sft.classify_child(url) for url in locs])

    def test_stale_five_child_index_is_detectable(self):
        kinds = [sft.classify_child(url) for url in sft.parse_locs(STALE_INDEX_XML)]
        self.assertIn("category", kinds)
        self.assertIn("tag", kinds)
        self.assertIn("users", kinds)

    def test_parse_urlset(self):
        self.assertEqual(
            ["https://kriskrug.co/about/", "https://kriskrug.co/work/"],
            sft.parse_locs(CHILD_XML),
        )

    def test_robots_sitemap_line(self):
        self.assertEqual(
            ["https://kriskrug.co/sitemap.xml"],
            sft.sitemap_lines_from_robots(ROBOTS),
        )

    def test_extract_robots_and_canonical(self):
        self.assertEqual("max-image-preview:large", sft.extract_meta(INDEXABLE_HTML, "robots"))
        self.assertEqual("https://kriskrug.co/about/", sft.extract_canonical(INDEXABLE_HTML))
        self.assertIn("noindex", sft.extract_meta(ARCHIVE_HTML, "robots"))
        self.assertIn("follow", sft.extract_meta(ARCHIVE_HTML, "robots"))

    def test_html_users_path_is_not_an_xml_sitemap(self):
        self.assertFalse(
            sft.looks_like_xml_sitemap(
                "<html><title>Kris Krug</title></html>",
                "text/html; charset=UTF-8",
            )
        )
        self.assertTrue(
            sft.looks_like_xml_sitemap(INDEX_XML, "application/xml; charset=UTF-8")
        )

    def test_retained_url_ok(self):
        page = {
            "url": "https://kriskrug.co/about/",
            "status": 200,
            "location": "",
            "robots": "max-image-preview:large",
            "googlebot": "",
            "description": "About Kris Krug.",
            "canonical": "https://kriskrug.co/about/",
            "x_robots_tag": "",
            "error": None,
        }
        ok, why = sft.retained_url_ok(page)
        self.assertTrue(ok, why)
        page["robots"] = "noindex, follow"
        ok, why = sft.retained_url_ok(page)
        self.assertFalse(ok)
        self.assertIn("noindex", why)


class GscBlockerTests(unittest.TestCase):
    def test_missing_env_is_a_blocker_not_a_fake_read(self):
        probe = sft.gsc_probe({})
        self.assertFalse(probe["available"])
        self.assertFalse(probe["invented"])
        self.assertIn("absent", probe["blocker"])
        self.assertEqual(
            {field: "missing" for field in sft.GSC_MISSING_FIELDS},
            probe["observed"],
        )
        self.assertIn("Do not Submit", probe["click_path"])
        self.assertIn("sc-domain:kriskrug.co", probe["click_path"])

    def test_present_env_still_does_not_invent_last_read(self):
        probe = sft.gsc_probe({"GOOGLE_APPLICATION_CREDENTIALS": "/tmp/fake.json"})
        self.assertTrue(probe["available"])
        self.assertEqual({}, probe["observed"])
        self.assertFalse(probe["invented"])

    def test_human_format_prints_blocker_not_counts(self):
        report = {
            "started_at": "2026-09-21T00:00:00Z",
            "base": "https://kriskrug.co",
            "robots": {"sitemaps": ["https://kriskrug.co/sitemap.xml"]},
            "handoff": {"status": 301, "location": "https://kriskrug.co/wp-sitemap.xml"},
            "index": {"children": ["post", "page"]},
            "inventory": {"posts": 979, "pages": 46, "total": 1025},
            "public_ok": True,
            "failures": [],
            "gsc": sft.gsc_probe({}),
        }
        text = sft.format_human(report)
        self.assertIn("GSC: BLOCKED", text)
        self.assertNotIn("last-read: September", text)
        self.assertNotIn("discovered pages: 1666", text)


class ReceiptAndWiringTests(unittest.TestCase):
    def test_dated_receipt_documents_blocker_and_does_not_close(self):
        text = RECEIPT.read_text(encoding="utf-8")
        self.assertIn("Refs #274", text)
        self.assertIn("not `Closes #274`", text)
        self.assertNotRegex(text, r"(?m)^(Closes|Fixes) #274")
        self.assertIn("external-wait", text)
        self.assertIn("blocker", text.lower())
        self.assertIn("Do not resubmit", text)
        self.assertIn("search.google.com/search-console/sitemaps", text)
        self.assertIn("#331", text)
        self.assertIn("1,025", text)
        self.assertNotRegex(text, r"(?i)this session.*last read.*september 2")
        self.assertIn("missing", text.lower())

    def test_previous_receipt_points_forward(self):
        text = PREVIOUS.read_text(encoding="utf-8")
        self.assertIn("issue-274-sitemap-followthrough-20260921.md", text)

    def test_makefile_and_runbook_wire_the_dry_run(self):
        makefile = MAKEFILE.read_text(encoding="utf-8")
        self.assertIn("sitemap-followthrough", makefile)
        self.assertIn("scripts/sitemap_followthrough.py", makefile)
        self.assertIn("make sitemap-followthrough", RUNBOOK.read_text(encoding="utf-8"))

    def test_script_has_no_gsc_write_verbs(self):
        source = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("Never submits", source)
        self.assertNotIn("webmasters.sitemaps.submit", source)
        self.assertNotIn("searchconsole.sitemaps.submit", source)


if __name__ == "__main__":
    unittest.main()
