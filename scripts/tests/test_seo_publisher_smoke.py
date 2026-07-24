"""CI-safe unit tests for the #425 publisher/schema smoke parser.

These exercise the JSON-LD extraction logic with fixtures only; the live
network checks in seo_publisher_smoke.main() are not invoked here.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import seo_publisher_smoke as sps  # noqa: E402

GRAPH_HTML = """
<html><head>
<script type="application/ld+json">
{"@graph":[
  {"@type":"WebPage","@id":"https://x/"},
  {"@type":"Article","headline":"H","datePublished":"2026-01-01",
   "dateModified":"2026-01-02","author":{"@id":"#person"},
   "publisher":{"@id":"#person"},"image":{"@type":"ImageObject"},
   "mainEntityOfPage":"https://x/"}
]}
</script>
</head><body></body></html>
"""

MISSING_HTML = """
<script type="application/ld+json">
{"@type":"BlogPosting","headline":"H","datePublished":"2026-01-01"}
</script>
"""

NO_ARTICLE_HTML = """
<script type="application/ld+json">
{"@type":"WebSite","name":"x"}
</script>
"""


class ArticleNodeTests(unittest.TestCase):
    def test_finds_article_inside_graph(self):
        node = sps.article_node(GRAPH_HTML)
        self.assertIsNotNone(node)
        self.assertEqual(node["@type"], "Article")

    def test_all_required_fields_present(self):
        node = sps.article_node(GRAPH_HTML)
        missing = [f for f in sps.REQUIRED_SCHEMA_FIELDS if not node.get(f)]
        self.assertEqual(missing, [])

    def test_detects_missing_fields(self):
        node = sps.article_node(MISSING_HTML)
        self.assertIsNotNone(node)
        missing = [f for f in sps.REQUIRED_SCHEMA_FIELDS if not node.get(f)]
        self.assertIn("author", missing)
        self.assertIn("image", missing)

    def test_no_article_family_node(self):
        self.assertIsNone(sps.article_node(NO_ARTICLE_HTML))

    def test_type_list_is_matched(self):
        html = '<script type="application/ld+json">{"@type":["NewsArticle","Thing"],"headline":"h"}</script>'
        node = sps.article_node(html)
        self.assertIsNotNone(node)


if __name__ == "__main__":
    unittest.main()
