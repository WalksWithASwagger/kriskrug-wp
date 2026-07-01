#!/usr/bin/env python3
"""Read-only public performance audit for kriskrug.co.

Measures route timing, cache headers, image payloads, blocking script candidates,
and URL hygiene without needing browser automation or third-party dependencies.
"""

from __future__ import annotations

import argparse
import html.parser
import json
import re
import statistics
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_BASE_URL = "https://kriskrug.co"
DEFAULT_ROUTES = ("/", "/about/", "/blog/", "/projects/", "/work/")
DEFAULT_LONGFORM = (
    "/2026/06/30/zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey/"
)
CACHE_HEADERS = {
    "cf-cache-status",
    "x-cache",
    "x-gateway-cache-status",
    "x-jetpack-boost-cache",
    "x-pagely-cache",
}
USER_AGENT = "kriskrug-performance-audit/1.0"


@dataclass
class Probe:
    url: str
    final_url: str
    status: int | str
    redirects: int
    ttfb: float
    total: float
    bytes_count: int
    headers: dict[str, str]
    body: bytes
    error: str | None = None


class PageParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.images: list[dict[str, str]] = []
        self.scripts: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []
        self.in_head = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        data = {key.lower(): value or "" for key, value in attrs}
        if tag == "head":
            self.in_head = True
        elif tag == "body":
            self.in_head = False
        elif tag == "img" and data.get("src"):
            self.images.append(data)
        elif tag == "script" and data.get("src"):
            data["_in_head"] = "yes" if self.in_head else "no"
            self.scripts.append(data)
        elif tag == "a" and data.get("href"):
            self.links.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "head":
            self.in_head = False


class RedirectCounter(urllib.request.HTTPRedirectHandler):
    redirects = 0

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
        type(self).redirects += 1
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url: str, *, timeout: int, method: str = "GET", cache_bust: bool = False) -> Probe:
    if cache_bust:
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}auditcb={time.time_ns()}"
    RedirectCounter.redirects = 0
    headers = {"User-Agent": USER_AGENT}
    if cache_bust:
        headers["Cache-Control"] = "no-cache"
        headers["Pragma"] = "no-cache"
    req = urllib.request.Request(url, headers=headers, method=method)
    opener = urllib.request.build_opener(RedirectCounter)
    started = time.perf_counter()
    try:
        with opener.open(req, timeout=timeout) as resp:
            first_byte = time.perf_counter()
            body = b"" if method == "HEAD" else resp.read()
            finished = time.perf_counter()
            return Probe(
                url=url,
                final_url=resp.geturl(),
                status=resp.status,
                redirects=RedirectCounter.redirects,
                ttfb=first_byte - started,
                total=finished - started,
                bytes_count=len(body),
                headers=dict(resp.headers.items()),
                body=body,
            )
    except Exception as err:
        finished = time.perf_counter()
        return Probe(
            url=url,
            final_url=url,
            status="ERR",
            redirects=RedirectCounter.redirects,
            ttfb=finished - started,
            total=finished - started,
            bytes_count=0,
            headers={},
            body=b"",
            error=str(err),
        )


def median(values: list[float]) -> float:
    return statistics.median(values) if values else 0.0


def cache_status(headers: dict[str, str]) -> str:
    return ", ".join(
        f"{key}={value}"
        for key, value in headers.items()
        if key.lower() in CACHE_HEADERS
    )


def parse_page(body: bytes) -> PageParser:
    parser = PageParser()
    parser.feed(body.decode("utf-8", errors="replace"))
    return parser


def absolute(base_url: str, value: str) -> str:
    return urllib.parse.urljoin(base_url.rstrip("/") + "/", value)


def image_size(src: str, timeout: int) -> tuple[int, int | str]:
    probe = fetch(src, timeout=timeout, method="HEAD")
    if probe.status != "ERR":
        length = probe.headers.get("Content-Length") or probe.headers.get("content-length")
        if length and length.isdigit():
            return int(length), probe.status
    probe = fetch(src, timeout=timeout)
    return probe.bytes_count, probe.status


def route_matrix(base_url: str, routes: list[str], samples: int, timeout: int) -> tuple[list[dict[str, Any]], dict[str, bytes]]:
    rows: list[dict[str, Any]] = []
    bodies: dict[str, bytes] = {}
    for route in routes:
        url = absolute(base_url, route)
        cold = [fetch(url, timeout=timeout, cache_bust=True) for _ in range(samples)]
        warm = [fetch(url, timeout=timeout) for _ in range(samples)]
        last = warm[-1]
        bodies[route] = last.body
        rows.append(
            {
                "route": route,
                "status": last.status,
                "redirects": last.redirects,
                "cold_ttfb": median([probe.ttfb for probe in cold]),
                "cold_total": median([probe.total for probe in cold]),
                "warm_ttfb": median([probe.ttfb for probe in warm]),
                "warm_total": median([probe.total for probe in warm]),
                "bytes": last.bytes_count,
                "cache": cache_status(last.headers),
                "final_url": last.final_url,
                "errors": [probe.error for probe in cold + warm if probe.error],
            }
        )
    return rows, bodies


def asset_rows(base_url: str, pages: list[str], timeout: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for page in pages:
        page_url = absolute(base_url, page)
        page_probe = fetch(page_url, timeout=timeout)
        parser = parse_page(page_probe.body)
        for image in parser.images:
            src = absolute(page_url, image.get("src", ""))
            key = (page_url, src)
            if key in seen:
                continue
            seen.add(key)
            bytes_count, status = image_size(src, timeout)
            rows.append(
                {
                    "page": page_probe.final_url,
                    "src": src,
                    "bytes": bytes_count,
                    "status": status,
                    "dimensions": "yes" if image.get("width") and image.get("height") else "no",
                    "loading": image.get("loading", ""),
                    "fetchpriority": image.get("fetchpriority", ""),
                    "srcset": "yes" if image.get("srcset") else "no",
                }
            )
    return sorted(rows, key=lambda row: int(row["bytes"]), reverse=True)


def script_candidates(base_url: str, pages: list[str], timeout: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for page in pages:
        page_url = absolute(base_url, page)
        probe = fetch(page_url, timeout=timeout)
        parser = parse_page(probe.body)
        candidates = []
        for script in parser.scripts:
            has_async = "async" in script
            has_defer = "defer" in script
            is_module = script.get("type") == "module"
            if script.get("_in_head") == "yes" and not (has_async or has_defer or is_module):
                candidates.append(absolute(page_url, script.get("src", "")))
        rows.append({"page": probe.final_url, "count": len(candidates), "sources": candidates})
    return rows


def html_checks(base_url: str, homepage_body: bytes, timeout: int) -> dict[str, Any]:
    homepage = homepage_body.decode("utf-8", errors="replace")
    style_probe = fetch(
        absolute(base_url, f"/wp-content/themes/kk-aurora/style.css?cb={time.time_ns()}"),
        timeout=timeout,
    )
    version_match = re.search(rb"^Version:\s*(.+)$", style_probe.body, re.M)
    critical_mentions = len(re.findall(r"critical-css|critical css|jetpack-boost", homepage, re.I))
    return {
        "style_version": version_match.group(1).decode().strip() if version_match else "",
        "resized_vancouver_png_present": "june-meetup-30-full-lineup-hero-1024x1024.png?w=720" in homepage,
        "direct_heavy_vancouver_src_absent": 'src="https://bc-ai.ca/wp-content/uploads/2026/06/june-meetup-30-full-lineup-hero-1024x1024.png"' not in homepage,
        "hero_dimensions_present": 'width="1800" height="1200"' in homepage,
        "vancouver_dimensions_present": 'width="1024" height="1024"' in homepage,
        "critical_css_mentions": critical_mentions,
    }


def internal_url_hygiene(base_url: str, pages: list[str], timeout: int) -> dict[str, Any]:
    base_host = urllib.parse.urlparse(base_url).netloc
    missing_trailing: set[str] = set()
    for page in pages:
        page_url = absolute(base_url, page)
        probe = fetch(page_url, timeout=timeout)
        parser = parse_page(probe.body)
        for link in parser.links:
            href = link.get("href", "")
            resolved = absolute(page_url, href)
            parsed = urllib.parse.urlparse(resolved)
            if parsed.netloc != base_host or parsed.query or parsed.fragment:
                continue
            if parsed.path in ("", "/") or parsed.path.endswith("/"):
                continue
            if "." in parsed.path.rsplit("/", 1)[-1]:
                continue
            missing_trailing.add(resolved)
    return {"missing_trailing_slash": sorted(missing_trailing)}


def render_markdown(data: dict[str, Any]) -> str:
    lines = [
        "# Performance Audit Report",
        "",
        f"- Generated: `{data['generated']}`",
        f"- Base URL: `{data['base_url']}`",
        f"- Route samples: `{data['samples']}` cold and `{data['samples']}` warm probes per route",
        f"- Asset pages: {', '.join(data['asset_pages'])}",
        "",
        "## Matrix A - Route Baseline",
        "",
        "| Route | HTTP | Redirects | Cold TTFB p50 | Cold total p50 | Warm TTFB p50 | Warm total p50 | Bytes | Cache status | Final URL |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    for row in data["routes"]:
        lines.append(
            "| `{route}` | {status} | {redirects} | {cold_ttfb:.3f} | {cold_total:.3f} | "
            "{warm_ttfb:.3f} | {warm_total:.3f} | {bytes} | {cache} | {final_url} |".format(**row)
        )
    lines += [
        "",
        "## Matrix B - Top Image Requests",
        "",
        "| Page | Bytes | HTTP | Width/height | Loading | Fetch priority | Srcset | Source |",
        "|---|---:|---:|---|---|---|---|---|",
    ]
    for row in data["images"][:20]:
        lines.append(
            f"| {row['page']} | {row['bytes']} | {row['status']} | {row['dimensions']} | "
            f"{row['loading']} | {row['fetchpriority']} | {row['srcset']} | {row['src']} |"
        )
    lines += [
        "",
        "## Matrix C - Blocking Script Candidates",
        "",
        "| Page | Count | Sources |",
        "|---|---:|---|",
    ]
    for row in data["scripts"]:
        lines.append(f"| {row['page']} | {row['count']} | {', '.join(row['sources'])} |")
    lines += [
        "",
        "## Matrix D - URL Hygiene",
        "",
        "| Check | Result |",
        "|---|---|",
    ]
    redirect_depth = "All sampled routes are 0-1 redirect hop."
    if any(int(row["redirects"]) > 1 for row in data["routes"]):
        redirect_depth = "One or more sampled routes exceed 1 redirect hop."
    missing = data["url_hygiene"]["missing_trailing_slash"]
    lines.append(f"| Route redirect depth | {redirect_depth} |")
    lines.append(
        "| Homepage/post internal links missing trailing slash | "
        + ("None found in inspected pages." if not missing else ", ".join(missing[:20]))
        + " |"
    )
    lines += [
        "",
        "## HTML / Theme Checks",
        "",
    ]
    for key, value in data["checks"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines += [
        "",
        "## Immediate Diagnostic Notes",
        "",
        "- Use cold TTFB and cache headers to separate origin/render cost from warm-cache behavior.",
        "- Treat `X-Jetpack-Boost-Cache=miss` on warm canonical probes as a cache-behavior finding to explain before deeper script changes.",
        "- Chrome DevTools/Lighthouse metrics are not included unless a DevTools MCP or local Lighthouse runner is available.",
    ]
    return "\n".join(lines) + "\n"


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    routes = [route.strip() for route in args.routes.split(",") if route.strip()]
    longform = args.longform_url or DEFAULT_LONGFORM
    asset_pages = ["/", longform]
    route_rows, bodies = route_matrix(args.base_url, routes, args.samples, args.timeout)
    homepage_body = bodies.get("/", b"")
    return {
        "generated": datetime.now(timezone.utc).isoformat(),
        "base_url": args.base_url,
        "samples": args.samples,
        "asset_pages": [absolute(args.base_url, page) for page in asset_pages],
        "routes": route_rows,
        "images": asset_rows(args.base_url, asset_pages, args.timeout),
        "scripts": script_candidates(args.base_url, asset_pages, args.timeout),
        "url_hygiene": internal_url_hygiene(args.base_url, asset_pages, args.timeout),
        "checks": html_checks(args.base_url, homepage_body, args.timeout),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--routes", default=",".join(DEFAULT_ROUTES))
    parser.add_argument("--samples", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--longform-url", default="")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = build_report(args)
    rendered = json.dumps(report, indent=2) + "\n" if args.format == "json" else render_markdown(report)
    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered, encoding="utf-8")
        print(f"report={path.resolve()}")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
