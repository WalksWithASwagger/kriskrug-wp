#!/usr/bin/env python3
"""Read-only #274 sitemap follow-through (public HTTP/XML/HTML only).

Checks the live WordPress sitemap after the #331 archive-policy deploy:
robots.txt declaration, `/sitemap.xml` 301 handoff, index children, child
counts, leftover archive-sitemap paths, and representative robots.

Never writes WordPress. Never submits, resubmits, removes, or requests
indexing in Google Search Console. If GSC API credentials are absent, the
script reports a precise blocker and prints the manual click path. It does
not invent last-read dates, statuses, or discovered counts.

Usage:
    python3 scripts/sitemap_followthrough.py
    python3 scripts/sitemap_followthrough.py --base https://kriskrug.co
    python3 scripts/sitemap_followthrough.py --json
    python3 scripts/sitemap_followthrough.py --full-crawl   # opt-in; every loc

`make sitemap-followthrough` is the operator entry point. Default mode does
not crawl every retained URL.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

DEFAULT_BASE = "https://kriskrug.co"
USER_AGENT = "kk-274-sitemap-followthrough/1.0 (+https://github.com/WalksWithASwagger/kriskrug-wp)"
SITEMAP_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

APPROVED_CHILD_SUFFIXES = (
    "wp-sitemap-posts-post-1.xml",
    "wp-sitemap-posts-page-1.xml",
)
FORBIDDEN_CHILD_NEEDLES = (
    "taxonomies-category",
    "taxonomies-post_tag",
    "wp-sitemap-users",
)

GSC_ENV_NAMES = (
    "GOOGLE_APPLICATION_CREDENTIALS",
    "GSC_CREDENTIALS",
    "GSC_CLIENT_SECRET",
    "SEARCH_CONSOLE_CREDENTIALS",
    "GOOGLE_GSC_CREDENTIALS",
)

GSC_MISSING_FIELDS = (
    "property_confirmation",
    "submitted_row_last_read",
    "status",
    "discovered_pages",
    "discovered_videos",
    "child_level_inventory",
    "fetch_error_detail",
    "indexed_totals",
)

REPRESENTATIVE_PATHS = (
    ("Home", "/", "indexable"),
    ("Page", "/about/", "indexable"),
    ("Page", "/blog/", "indexable"),
    ("Page", "/work/", "indexable"),
    ("Page", "/contact/", "indexable"),
    ("Post", "/2026/09/18/all-in-montreal-final-day-a-heartbeat-under-my-boots/", "indexable"),
    ("Post", "/2026/09/07/ai-already-campaign-issue-vancouver/", "indexable"),
    ("#996 primary", "/2024/01/31/exploring-the-intersection-of-photography-and-generative-ai/", "indexable"),
    ("Category", "/category/ai-ethics-philosophy/", "archive_noindex_follow"),
    ("Tag", "/tag/sxsw-sxswi/", "archive_noindex_follow"),
    ("Tag", "/tag/ai/", "archive_noindex_follow"),
    ("Author", "/author/kk/", "archive_noindex_follow"),
    ("Date", "/2026/08/", "archive_noindex_follow"),
    ("Share", "/2024/01/31/exploring-the-intersection-of-photography-and-generative-ai/?share=twitter", "share_redirect"),
    ("Login", "/wp-login.php", "login_noindex"),
    ("Embed", "/2024/01/31/exploring-the-intersection-of-photography-and-generative-ai/embed/", "embed_noindex_follow"),
    ("Search", "/?s=photography", "search_noindex_follow"),
)

LEFTOVER_PATHS = (
    "/wp-sitemap-taxonomies-category-1.xml",
    "/wp-sitemap-taxonomies-post_tag-1.xml",
    "/wp-sitemap-users-1.xml",
    "/sitemap_index.xml",
    "/sitemap-1.xml",
    "/news-sitemap.xml",
)

GSC_CLICK_PATH = """Manual GSC click path (signed-in human; do not invent results):

1. Sign in to Google as the owner of property sc-domain:kriskrug.co
   (dated comments used kk@bc-ai.ca).
2. Open https://search.google.com/search-console/sitemaps?resource_id=sc-domain%3Akriskrug.co
3. Confirm the property selector says sc-domain:kriskrug.co (domain property).
4. Find the existing row for https://kriskrug.co/sitemap.xml. Do not Submit.
   Do not resubmit. Do not remove rows. Do not Request indexing.
5. Record, with a real clock timestamp:
   - property id
   - submitted URL
   - last read
   - status
   - discovered pages (and videos if shown)
   - child-level list if the UI expands one
   - any fetch-error text
6. Close #274 only when last-read is after 2026-09-03, status is Success with
   no fetch error, and the discovered count is explained against the live
   inventory in the latest receipt. If last-read is still pre-deploy, wait.
"""


class Redirect(Exception):
    def __init__(self, status: int, location: str, headers: dict[str, str]):
        super().__init__(f"HTTP {status} -> {location}")
        self.status = status
        self.location = location
        self.headers = headers


class NoFollow(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise Redirect(code, headers.get("Location") or newurl, dict(headers.items()))


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_locs(xml_text: str) -> list[str]:
    """Return every <loc> from a sitemap index or urlset, namespace-safe."""
    text = (xml_text or "").strip()
    if not text:
        return []
    try:
        root = ET.fromstring(text)
    except ET.ParseError:
        return re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", text, flags=re.I)

    locs: list[str] = []
    for tag in ("sitemap", "url"):
        for node in root.findall(f"sm:{tag}", SITEMAP_NS):
            loc = (node.findtext("sm:loc", default="", namespaces=SITEMAP_NS) or "").strip()
            if loc:
                locs.append(loc)
        # Also accept documents that dropped the default namespace.
        for node in root.findall(tag):
            loc = (node.findtext("loc") or "").strip()
            if loc and loc not in locs:
                locs.append(loc)
    if not locs:
        locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", text, flags=re.I)
    return locs


def sitemap_lines_from_robots(robots_txt: str) -> list[str]:
    lines = []
    for raw in (robots_txt or "").splitlines():
        line = raw.strip()
        if line.lower().startswith("sitemap:"):
            lines.append(line.split(":", 1)[1].strip())
    return lines


def extract_meta(html: str, name: str) -> str:
    if not html:
        return ""
    name_re = re.escape(name)
    patterns = (
        rf'<meta[^>]+name=["\']{name_re}["\'][^>]+content=["\']([^"\']*)["\']',
        rf'<meta[^>]+content=["\']([^"\']*)["\'][^>]+name=["\']{name_re}["\']',
    )
    for pattern in patterns:
        match = re.search(pattern, html, flags=re.I)
        if match:
            return match.group(1).strip()
    return ""


def extract_canonical(html: str) -> str:
    if not html:
        return ""
    patterns = (
        r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']',
        r'<link[^>]+href=["\']([^"\']+)["\'][^>]+rel=["\']canonical["\']',
    )
    for pattern in patterns:
        match = re.search(pattern, html, flags=re.I)
        if match:
            return match.group(1).strip()
    return ""


def classify_child(url: str) -> str:
    lowered = url.lower()
    if "wp-sitemap-posts-post" in lowered:
        return "posts"
    if "wp-sitemap-posts-page" in lowered:
        return "pages"
    if "taxonomies-category" in lowered:
        return "category"
    if "taxonomies-post_tag" in lowered:
        return "tag"
    if "wp-sitemap-users" in lowered:
        return "users"
    return "other"


def looks_like_xml_sitemap(body: str, content_type: str) -> bool:
    ctype = (content_type or "").lower()
    head = (body or "").lstrip()[:200].lower()
    if "html" in ctype and "xml" not in ctype:
        return False
    return head.startswith("<?xml") or "<sitemapindex" in head or "<urlset" in head


def gsc_probe(env: dict[str, str] | None = None) -> dict[str, Any]:
    """Report whether this process can honestly read GSC. Never invents values."""
    source = env if env is not None else os.environ
    present = [name for name in GSC_ENV_NAMES if source.get(name)]
    available = bool(present)
    return {
        "available": available,
        "present_env_names": present,
        "blocker": None
        if available
        else "GSC API credentials are absent. Public checks are not a Search Console last-read.",
        "observed": {} if available else {field: "missing" for field in GSC_MISSING_FIELDS},
        "invented": False,
        "click_path": GSC_CLICK_PATH,
    }


def _header_map(headers) -> dict[str, str]:
    return {k.lower(): v for k, v in headers.items()}


def fetch(url: str, *, follow: bool = True, timeout: int = 25) -> dict[str, Any]:
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    handlers = [] if follow else [NoFollow()]
    opener = build_opener(*handlers)
    try:
        with opener.open(request, timeout=timeout) as resp:
            raw = resp.read()
            headers = _header_map(resp.headers)
            charset = resp.headers.get_content_charset() or "utf-8"
            body = raw.decode(charset, errors="replace")
            return {
                "url": url,
                "status": resp.status,
                "final_url": resp.geturl(),
                "location": headers.get("location", ""),
                "headers": headers,
                "body": body,
                "sha256": hashlib.sha256(raw).hexdigest(),
                "error": None,
            }
    except Redirect as exc:
        return {
            "url": url,
            "status": exc.status,
            "final_url": url,
            "location": exc.location,
            "headers": {k.lower(): v for k, v in exc.headers.items()},
            "body": "",
            "sha256": "",
            "error": None,
        }
    except HTTPError as exc:
        raw = exc.read() if exc.fp else b""
        headers = _header_map(exc.headers) if exc.headers is not None else {}
        charset = "utf-8"
        if exc.headers is not None:
            charset = exc.headers.get_content_charset() or "utf-8"
        return {
            "url": url,
            "status": exc.code,
            "final_url": url,
            "location": headers.get("location", ""),
            "headers": headers,
            "body": raw.decode(charset, errors="replace"),
            "sha256": hashlib.sha256(raw).hexdigest() if raw else "",
            "error": None,
        }
    except (URLError, TimeoutError, OSError) as exc:
        return {
            "url": url,
            "status": 0,
            "final_url": url,
            "location": "",
            "headers": {},
            "body": "",
            "sha256": "",
            "error": str(exc),
        }


def _abs(base: str, path: str) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        return path
    if path.startswith("?"):
        return base.rstrip("/") + "/" + path
    return base.rstrip("/") + path


def _cache_status(headers: dict[str, str]) -> str:
    return headers.get("x-gateway-cache-status", "")


def _robots_ok(expectation: str, status: int, location: str, robots: str) -> bool:
    robots_l = robots.lower()
    if expectation == "indexable":
        return status == 200 and "noindex" not in robots_l
    if expectation == "archive_noindex_follow":
        return status == 200 and "noindex" in robots_l and "follow" in robots_l
    if expectation == "share_redirect":
        return status in {301, 302} and bool(location)
    if expectation == "login_noindex":
        return status == 200 and "noindex" in robots_l
    if expectation == "embed_noindex_follow":
        return status == 200 and "noindex" in robots_l and "follow" in robots_l
    if expectation == "search_noindex_follow":
        return status == 200 and "noindex" in robots_l and "follow" in robots_l
    return False


def inspect_page(url: str, *, follow: bool = False) -> dict[str, Any]:
    result = fetch(url, follow=follow)
    html = result["body"]
    return {
        "url": url,
        "status": result["status"],
        "final_url": result["final_url"],
        "location": result["location"],
        "robots": extract_meta(html, "robots"),
        "googlebot": extract_meta(html, "googlebot"),
        "description": extract_meta(html, "description"),
        "canonical": extract_canonical(html),
        "x_robots_tag": result["headers"].get("x-robots-tag", ""),
        "cache": _cache_status(result["headers"]),
        "error": result["error"],
    }


def retained_url_ok(page: dict[str, Any]) -> tuple[bool, str]:
    if page.get("error"):
        return False, f"fetch error: {page['error']}"
    if page["status"] != 200:
        return False, f"HTTP {page['status']}"
    if page.get("location"):
        return False, f"redirected to {page['location']}"
    robots = (page.get("robots") or "").lower()
    if "noindex" in robots:
        return False, f"robots noindex ({page['robots']})"
    googlebot = (page.get("googlebot") or "").lower()
    if "noindex" in googlebot:
        return False, f"googlebot noindex ({page['googlebot']})"
    xrt = (page.get("x_robots_tag") or "").lower()
    if "noindex" in xrt:
        return False, f"X-Robots-Tag noindex ({page['x_robots_tag']})"
    canonical = page.get("canonical") or ""
    if not canonical:
        return False, "missing canonical"
    if canonical.rstrip("/") != page["url"].rstrip("/"):
        return False, f"canonical {canonical} != {page['url']}"
    if not page.get("description"):
        return False, "missing description"
    return True, "ok"


def run_public_checks(base: str, *, cache_bust: str, full_crawl: bool, concurrency: int) -> dict[str, Any]:
    started = utc_now()
    failures: list[str] = []
    notes: list[str] = []

    robots = fetch(_abs(base, "/robots.txt"))
    sitemap_decls = sitemap_lines_from_robots(robots["body"])
    if robots["status"] != 200:
        failures.append(f"robots.txt HTTP {robots['status']}")
    if sitemap_decls != [f"{base.rstrip('/')}/sitemap.xml"]:
        failures.append(f"robots.txt Sitemap lines {sitemap_decls!r}")

    handoff = fetch(_abs(base, "/sitemap.xml"), follow=False)
    expected_location = f"{base.rstrip('/')}/wp-sitemap.xml"
    if handoff["status"] != 301 or handoff["location"] != expected_location:
        failures.append(
            f"/sitemap.xml expected 301 to {expected_location}, "
            f"got {handoff['status']} {handoff['location']!r}"
        )

    index = fetch(_abs(base, "/wp-sitemap.xml"), follow=True)
    index_cb = fetch(_abs(base, f"/wp-sitemap.xml?cb={cache_bust}"), follow=True)
    children = parse_locs(index["body"])
    children_cb = parse_locs(index_cb["body"])
    kinds = [classify_child(url) for url in children]

    if index["status"] != 200:
        failures.append(f"/wp-sitemap.xml HTTP {index['status']}")
    if children != children_cb or index["sha256"] != index_cb["sha256"]:
        failures.append("normal vs cache-busted sitemap index differ")
    if set(kinds) != {"posts", "pages"} or len(children) != 2:
        failures.append(f"index children {children} (kinds={kinds})")
    for needle in FORBIDDEN_CHILD_NEEDLES:
        if any(needle in url for url in children):
            failures.append(f"index still lists {needle}")

    child_rows = []
    total_urls = 0
    retained: list[str] = []
    for child_url in children:
        bare = fetch(child_url)
        cb_url = child_url + ("&" if "?" in child_url else "?") + f"cb={cache_bust}"
        busted = fetch(cb_url)
        locs = parse_locs(bare["body"])
        locs_cb = parse_locs(busted["body"])
        kind = classify_child(child_url)
        if bare["status"] != 200 or busted["status"] != 200:
            failures.append(f"{child_url} HTTP {bare['status']}/{busted['status']}")
        if locs != locs_cb or bare["sha256"] != busted["sha256"]:
            failures.append(f"{child_url} cache-busted body differs")
        if kind not in {"posts", "pages"}:
            failures.append(f"unexpected child kind {kind}: {child_url}")
        total_urls += len(locs)
        retained.extend(locs)
        child_rows.append(
            {
                "url": child_url,
                "kind": kind,
                "status": bare["status"],
                "cache": _cache_status(bare["headers"]),
                "urls": len(locs),
                "cache_busted_urls": len(locs_cb),
                "sha256": bare["sha256"],
                "sha_match": bare["sha256"] == busted["sha256"],
                "newest": locs[-1] if locs else "",
            }
        )

    leftovers = []
    for path in LEFTOVER_PATHS:
        result = fetch(_abs(base, path), follow=True)
        xmlish = looks_like_xml_sitemap(result["body"], result["headers"].get("content-type", ""))
        leftover = {
            "url": _abs(base, path),
            "status": result["status"],
            "final_url": result["final_url"],
            "xml_sitemap": xmlish,
            "loc_count": len(parse_locs(result["body"])) if xmlish else 0,
            "content_type": result["headers"].get("content-type", ""),
        }
        leftovers.append(leftover)
        if path.endswith("taxonomies-category-1.xml") and result["status"] != 404:
            notes.append(f"{path} expected 404, got {result['status']}")
        if path.endswith("taxonomies-post_tag-1.xml") and result["status"] != 404:
            notes.append(f"{path} expected 404, got {result['status']}")

    representatives = []
    for label, path, expectation in REPRESENTATIVE_PATHS:
        # Share variants must not be followed: the 301 is the approved behavior.
        # Embeds may add a trailing slash; following once is fine.
        follow = expectation == "embed_noindex_follow"
        page = inspect_page(_abs(base, path), follow=follow)
        ok = _robots_ok(expectation, page["status"], page["location"], page["robots"])
        if not ok:
            failures.append(f"{label} {path} failed {expectation}: HTTP {page['status']} robots={page['robots']!r}")
        representatives.append({"label": label, "expectation": expectation, "ok": ok, **page})

    crawl: dict[str, Any] = {
        "ran": False,
        "reason": "default mode skips the full retained-URL crawl; pass --full-crawl to opt in",
        "ok": 0,
        "fail": 0,
        "failures": [],
    }
    if full_crawl:
        crawl = {"ran": True, "reason": "opt-in --full-crawl", "ok": 0, "fail": 0, "failures": []}
        workers = max(1, min(concurrency, 4))

        def _one(url: str) -> tuple[str, bool, str]:
            page = inspect_page(url, follow=False)
            good, why = retained_url_ok(page)
            return url, good, why

        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = [pool.submit(_one, url) for url in retained]
            for future in as_completed(futures):
                url, good, why = future.result()
                if good:
                    crawl["ok"] += 1
                else:
                    crawl["fail"] += 1
                    if len(crawl["failures"]) < 20:
                        crawl["failures"].append({"url": url, "reason": why})
        if crawl["fail"]:
            failures.append(f"full crawl {crawl['fail']} failures / {len(retained)} urls")

    gsc = gsc_probe()
    finished = utc_now()
    return {
        "issue": 274,
        "mode": "read-only-public",
        "started_at": started,
        "finished_at": finished,
        "base": base.rstrip("/"),
        "robots": {
            "status": robots["status"],
            "sitemaps": sitemap_decls,
        },
        "handoff": {
            "status": handoff["status"],
            "location": handoff["location"],
            "redirect_by": handoff["headers"].get("x-redirect-by", ""),
            "cache": _cache_status(handoff["headers"]),
        },
        "index": {
            "status": index["status"],
            "cache": _cache_status(index["headers"]),
            "sha256": index["sha256"],
            "children": children,
            "kinds": kinds,
            "cache_busted_sha256": index_cb["sha256"],
            "cache_busted_match": index["sha256"] == index_cb["sha256"],
        },
        "children": child_rows,
        "inventory": {
            "posts": next((row["urls"] for row in child_rows if row["kind"] == "posts"), 0),
            "pages": next((row["urls"] for row in child_rows if row["kind"] == "pages"), 0),
            "total": total_urls,
        },
        "leftovers": leftovers,
        "representatives": representatives,
        "crawl": crawl,
        "gsc": gsc,
        "failures": failures,
        "notes": notes,
        "public_ok": not failures,
    }


def format_human(report: dict[str, Any]) -> str:
    inv = report["inventory"]
    gsc = report["gsc"]
    lines = [
        f"#274 sitemap follow-through  {report['started_at']}  {report['base']}",
        f"robots Sitemap: {report['robots']['sitemaps']}",
        f"/sitemap.xml: HTTP {report['handoff']['status']} -> {report['handoff']['location']}",
        f"index children: {report['index']['children']}",
        f"inventory: {inv['posts']} posts + {inv['pages']} pages = {inv['total']}",
        f"public_ok: {report['public_ok']}",
    ]
    if report["failures"]:
        lines.append("failures:")
        lines.extend(f"  - {item}" for item in report["failures"])
    if gsc["available"]:
        lines.append("GSC credentials present in env. This script still does not call GSC.")
        lines.append("Record last-read from a signed-in UI or a dedicated GSC client; do not invent it.")
    else:
        lines.append(f"GSC: BLOCKED. {gsc['blocker']}")
        lines.append("Missing fields: " + ", ".join(gsc["observed"]))
        lines.append("")
        lines.append(gsc["click_path"].rstrip())
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default=DEFAULT_BASE, help="site base URL")
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    parser.add_argument(
        "--full-crawl",
        action="store_true",
        help="GET every retained sitemap URL (bounded, opt-in; default is index + samples)",
    )
    parser.add_argument("--concurrency", type=int, default=4, help="full-crawl workers (capped at 4)")
    parser.add_argument("--cache-bust", default="", help="override cache-bust token")
    args = parser.parse_args(argv)

    cache_bust = args.cache_bust or str(int(datetime.now(timezone.utc).timestamp()))
    report = run_public_checks(
        args.base.rstrip("/"),
        cache_bust=cache_bust,
        full_crawl=args.full_crawl,
        concurrency=args.concurrency,
    )
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(format_human(report))
    return 0 if report["public_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
