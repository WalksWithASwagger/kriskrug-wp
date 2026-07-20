#!/usr/bin/env python3
"""Read-only publisher/schema smoke checks for KrisKrug.co (issue #425).

Verifies the discovery surfaces stay healthy and that recent posts emit an
Article-family JSON-LD block with the fields Google needs for a publisher
pattern. Read-only: it makes GET requests only and never writes to WordPress.

Usage:
    python3 scripts/seo_publisher_smoke.py                 # check live site
    python3 scripts/seo_publisher_smoke.py --base URL      # check another host
    python3 scripts/seo_publisher_smoke.py --posts 5       # sample N recent posts

Exit code is non-zero if a required surface is broken or a sampled post is
missing a required schema field. The absent Google-News sitemap is reported as
a known gap (see docs/current-state/SEO-PUBLISHER-SCHEMA-2026-07-19.md), not a
failure, so this stays green until that work is deliberately shipped.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_BASE = "https://kriskrug.co"

# Fields every publisher-grade Article-family node should carry.
REQUIRED_SCHEMA_FIELDS = (
    "headline",
    "datePublished",
    "dateModified",
    "author",
    "publisher",
    "image",
    "mainEntityOfPage",
)
ARTICLE_TYPES = {"Article", "NewsArticle", "BlogPosting"}

JSONLD_RE = re.compile(
    r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.DOTALL | re.IGNORECASE,
)


def fetch(url: str, timeout: int = 20) -> tuple[int, str]:
    req = Request(url, headers={"User-Agent": "kk-seo-smoke/1.0"})
    try:
        with urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except HTTPError as exc:
        return exc.code, ""
    except (URLError, TimeoutError) as exc:
        return 0, str(exc)


def iter_jsonld_nodes(html: str):
    """Yield every JSON-LD node, flattening @graph containers."""
    for block in JSONLD_RE.findall(html):
        try:
            data = json.loads(block.strip())
        except json.JSONDecodeError:
            continue
        graph = data.get("@graph") if isinstance(data, dict) else None
        for node in (graph if isinstance(graph, list) else [data]):
            if isinstance(node, dict):
                yield node


def article_node(html: str) -> dict | None:
    for node in iter_jsonld_nodes(html):
        node_type = node.get("@type")
        types = node_type if isinstance(node_type, list) else [node_type]
        if any(t in ARTICLE_TYPES for t in types):
            return node
    return None


def check_surface(base: str, path: str, must_contain: str = "") -> tuple[bool, str]:
    status, body = fetch(base + path)
    if status != 200:
        return False, f"{path} -> HTTP {status}"
    if must_contain and must_contain not in body:
        return False, f"{path} -> 200 but missing '{must_contain}'"
    return True, f"{path} -> 200"


def recent_post_links(base: str, count: int) -> list[str]:
    status, body = fetch(f"{base}/wp-json/wp/v2/posts?per_page={count}&_fields=link")
    if status != 200:
        return []
    try:
        return [item["link"] for item in json.loads(body)]
    except (json.JSONDecodeError, KeyError, TypeError):
        return []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default=DEFAULT_BASE, help="site base URL")
    parser.add_argument("--posts", type=int, default=3, help="recent posts to sample")
    args = parser.parse_args()
    base = args.base.rstrip("/")

    failures: list[str] = []
    notes: list[str] = []

    # 1. Discovery surfaces that must stay healthy.
    for path, needle in (
        ("/wp-sitemap.xml", "wp-sitemap-posts-post"),
        ("/feed/", "<rss"),
    ):
        ok, msg = check_surface(base, path, needle)
        print(("PASS " if ok else "FAIL ") + msg)
        if not ok:
            failures.append(msg)

    # 2. Google-News style sitemap: known gap, reported not enforced.
    news_found = False
    for path in ("/news-sitemap.xml", "/sitemap-news.xml", "/wp-sitemap-news.xml"):
        status, _ = fetch(base + path)
        if status == 200:
            news_found = True
            print(f"PASS news sitemap present: {path}")
            break
    if not news_found:
        notes.append("No Google-News sitemap (known gap; see #425 doc).")
        print("NOTE no news sitemap yet (known gap, not a failure)")

    # 3. Recent posts must emit an Article-family node with required fields.
    links = recent_post_links(base, args.posts)
    if not links:
        failures.append("could not list recent posts via wp-json")
        print("FAIL could not list recent posts")
    for link in links:
        status, html = fetch(link)
        if status != 200:
            failures.append(f"{link} -> HTTP {status}")
            print(f"FAIL {link} -> HTTP {status}")
            continue
        node = article_node(html)
        if node is None:
            failures.append(f"{link} -> no Article-family JSON-LD")
            print(f"FAIL {link} -> no Article-family schema")
            continue
        missing = [f for f in REQUIRED_SCHEMA_FIELDS if not node.get(f)]
        node_type = node.get("@type")
        if missing:
            failures.append(f"{link} -> {node_type} missing {missing}")
            print(f"FAIL {link} -> {node_type} missing {missing}")
        else:
            print(f"PASS {link} -> {node_type} with all required fields")

    print()
    for note in notes:
        print(f"NOTE: {note}")
    if failures:
        print(f"\n{len(failures)} failure(s).")
        return 1
    print("\nAll publisher/schema smoke checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
