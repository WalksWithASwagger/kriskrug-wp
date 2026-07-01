#!/usr/bin/env python3
"""Run a repeatable public performance audit for kriskrug.co.

The script is read-only. It measures cold-ish and warm route timings with curl,
then inspects homepage plus one current post for image payload and blocking
script candidates.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import statistics
import subprocess
import time
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit

import requests


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASE_URL = "https://kriskrug.co"
DEFAULT_ROUTES = ("/", "/about/", "/blog/", "/projects/", "/work/")
IMAGE_EXTENSIONS = (".avif", ".gif", ".jpeg", ".jpg", ".png", ".webp")


@dataclasses.dataclass(frozen=True)
class RouteProbe:
    route: str
    mode: str
    http_code: int | None
    redirects: int | None
    size_download: int | None
    ttfb_seconds: float | None
    total_seconds: float | None
    final_url: str
    cache_status: str


@dataclasses.dataclass(frozen=True)
class AssetProbe:
    page_url: str
    src: str
    status: int | None
    bytes: int | None
    has_width: bool
    has_height: bool
    loading: str
    fetchpriority: str
    has_srcset: bool


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.images: list[dict[str, str]] = []
        self.scripts: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {key.lower(): (value or "") for key, value in attrs}
        if tag.lower() == "img" and data.get("src"):
            self.images.append(data)
        elif tag.lower() == "script" and data.get("src"):
            self.scripts.append(data)
        elif tag.lower() == "a" and data.get("href"):
            self.links.append(data)


def cache_bust(url: str) -> str:
    split = urlsplit(url)
    query = dict(parse_qsl(split.query, keep_blank_values=True))
    query["_perf_audit"] = str(int(time.time() * 1000))
    return urlunsplit((split.scheme, split.netloc, split.path, urlencode(query), split.fragment))


def last_response_headers(raw: str) -> dict[str, str]:
    blocks = [block for block in raw.replace("\r\n", "\n").split("\n\n") if block.startswith("HTTP/")]
    if not blocks:
        return {}

    headers: dict[str, str] = {}
    for line in blocks[-1].splitlines()[1:]:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        headers[key.strip().lower()] = value.strip()
    return headers


def cache_hint(headers: dict[str, str]) -> str:
    values = []
    for key in ("x-jetpack-boost-cache", "x-gateway-cache-status", "cf-cache-status", "x-cache"):
        if headers.get(key):
            values.append(f"{key}={headers[key]}")
    return ", ".join(values) if values else "(not exposed)"


def parse_int(value: str) -> int | None:
    try:
        return int(value)
    except ValueError:
        return None


def parse_float(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return None


def route_url(base_url: str, route: str) -> str:
    if route.startswith("http://") or route.startswith("https://"):
        return route
    return urljoin(base_url.rstrip("/") + "/", route.lstrip("/"))


def probe_route(base_url: str, route: str, mode: str, timeout: int) -> RouteProbe:
    url = route_url(base_url, route)
    if mode == "cold":
        url = cache_bust(url)

    command = [
        "curl",
        "-L",
        "-sS",
        "-o",
        "/dev/null",
        "-D",
        "-",
        "--max-time",
        str(timeout),
        "-w",
        "\n__METRICS__\t%{http_code}\t%{num_redirects}\t%{size_download}\t%{time_starttransfer}\t%{time_total}\t%{url_effective}\n",
        "-H",
        "User-Agent: kriskrug-performance-audit/1.0",
    ]
    if mode == "cold":
        command.extend(["-H", "Cache-Control: no-cache", "-H", "Pragma: no-cache"])
    command.append(url)

    try:
        completed = subprocess.run(command, capture_output=True, text=True, timeout=timeout + 5)
    except subprocess.TimeoutExpired:
        return RouteProbe(route, mode, None, None, None, None, None, url, "timeout")

    stdout = completed.stdout
    if "__METRICS__" not in stdout:
        return RouteProbe(route, mode, None, None, None, None, None, url, "curl-failed")

    header_text, metrics = stdout.rsplit("__METRICS__", 1)
    fields = metrics.strip().split("\t")
    if len(fields) != 6:
        return RouteProbe(route, mode, None, None, None, None, None, url, "parse-failed")

    headers = last_response_headers(header_text)
    return RouteProbe(
        route=route,
        mode=mode,
        http_code=parse_int(fields[0]),
        redirects=parse_int(fields[1]),
        size_download=parse_int(fields[2]),
        ttfb_seconds=parse_float(fields[3]),
        total_seconds=parse_float(fields[4]),
        final_url=fields[5],
        cache_status=cache_hint(headers),
    )


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, round((len(ordered) - 1) * pct)))
    return ordered[index]


def metric_summary(probes: list[RouteProbe], field: str) -> dict[str, float | int | None]:
    values = [getattr(probe, field) for probe in probes]
    clean = [value for value in values if isinstance(value, float)]
    if not clean:
        return {"count": 0, "p50": None, "p95": None, "avg": None}
    return {
        "count": len(clean),
        "p50": round(statistics.median(clean), 3),
        "p95": round(percentile(clean, 0.95), 3),
        "avg": round(sum(clean) / len(clean), 3),
    }


def fetch_html(session: requests.Session, url: str, timeout: int) -> str:
    response = session.get(url, timeout=timeout)
    response.raise_for_status()
    return response.text


def latest_post_url(session: requests.Session, base_url: str, timeout: int) -> str:
    try:
        response = session.get(
            f"{base_url.rstrip('/')}/wp-json/wp/v2/posts",
            params={"per_page": 1, "orderby": "date", "order": "desc", "_fields": "link"},
            timeout=timeout,
        )
        response.raise_for_status()
        posts = response.json()
    except requests.RequestException:
        return f"{base_url.rstrip('/')}/blog/"
    if not posts:
        return f"{base_url.rstrip('/')}/blog/"
    return str(posts[0].get("link") or f"{base_url.rstrip('/')}/blog/")


def is_image_url(url: str) -> bool:
    path = urlsplit(url).path.lower()
    return path.endswith(IMAGE_EXTENSIONS)


def asset_size(session: requests.Session, url: str, timeout: int) -> tuple[int | None, int | None]:
    try:
        response = session.head(url, allow_redirects=True, timeout=timeout)
        if response.status_code in (405, 429) or response.status_code >= 500:
            response = session.get(url, stream=True, timeout=timeout)
        length = response.headers.get("content-length", "")
        return response.status_code, int(length) if length.isdigit() else None
    except requests.RequestException:
        return None, None


def inspect_page(session: requests.Session, base_url: str, page_url: str, timeout: int) -> dict[str, Any]:
    parser = PageParser()
    parser.feed(fetch_html(session, page_url, timeout))

    blocking_scripts = [
        urljoin(base_url.rstrip("/") + "/", script["src"])
        for script in parser.scripts
        if not script.get("async") and not script.get("defer")
    ]

    internal_noncanonical_links = []
    for link in parser.links:
        href = link.get("href", "").strip()
        if not href.startswith("/"):
            continue
        path = urlsplit(href).path
        if path and "." not in path.rsplit("/", 1)[-1] and not path.endswith("/"):
            internal_noncanonical_links.append(href)

    image_probes = []
    seen_images: set[str] = set()
    for image in parser.images:
        src = urljoin(base_url.rstrip("/") + "/", image["src"])
        if src in seen_images or not is_image_url(src):
            continue
        seen_images.add(src)
        status, length = asset_size(session, src, timeout)
        image_probes.append(
            AssetProbe(
                page_url=page_url,
                src=src,
                status=status,
                bytes=length,
                has_width=bool(image.get("width")),
                has_height=bool(image.get("height")),
                loading=image.get("loading", ""),
                fetchpriority=image.get("fetchpriority", ""),
                has_srcset=bool(image.get("srcset")),
            )
        )

    return {
        "url": page_url,
        "blocking_scripts": blocking_scripts,
        "internal_noncanonical_links": internal_noncanonical_links,
        "images": image_probes,
    }


def serialize_probe(probe: Any) -> dict[str, Any]:
    if dataclasses.is_dataclass(probe):
        return dataclasses.asdict(probe)
    raise TypeError(f"unsupported JSON value: {probe!r}")


def fmt_seconds(value: float | int | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:.3f}"


def render_markdown(data: dict[str, Any]) -> str:
    lines = [
        "# Performance Audit Report",
        "",
        f"- Generated: `{data['generated_at']}`",
        f"- Base URL: `{data['base_url']}`",
        f"- Route samples: `{data['samples']}` cold and `{data['samples']}` warm probes per route",
        f"- Asset pages: `{', '.join(data['asset_pages'])}`",
        "",
        "## Matrix A - Route Baseline",
        "",
        "| Route | HTTP | Redirects | Cold TTFB p50 | Cold total p50 | Warm TTFB p50 | Warm total p50 | Cache status | Final URL |",
        "|---|---:|---:|---:|---:|---:|---:|---|---|",
    ]

    for row in data["routes"]:
        cold_ttfb = metric_summary(row["cold"], "ttfb_seconds")
        cold_total = metric_summary(row["cold"], "total_seconds")
        warm_ttfb = metric_summary(row["warm"], "ttfb_seconds")
        warm_total = metric_summary(row["warm"], "total_seconds")
        representative = row["warm"][-1] if row["warm"] else row["cold"][-1]
        lines.append(
            "| {route} | {http_code} | {redirects} | {cold_ttfb} | {cold_total} | {warm_ttfb} | {warm_total} | {cache} | {final_url} |".format(
                route=row["route"],
                http_code=representative.http_code or "",
                redirects=representative.redirects or 0,
                cold_ttfb=fmt_seconds(cold_ttfb["p50"]),
                cold_total=fmt_seconds(cold_total["p50"]),
                warm_ttfb=fmt_seconds(warm_ttfb["p50"]),
                warm_total=fmt_seconds(warm_total["p50"]),
                cache=representative.cache_status,
                final_url=representative.final_url,
            )
        )

    lines.extend(
        [
            "",
            "## Matrix B - Top Image Requests",
            "",
            "| Page | Bytes | Status | Width/height | Loading | Fetch priority | Srcset | Source |",
            "|---|---:|---:|---|---|---|---|---|",
        ]
    )

    images = sorted(
        [image for page in data["page_inspections"] for image in page["images"]],
        key=lambda image: image.bytes or 0,
        reverse=True,
    )
    for image in images[:20]:
        dimensions = "yes" if image.has_width and image.has_height else "no"
        lines.append(
            "| {page} | {bytes} | {status} | {dimensions} | {loading} | {priority} | {srcset} | {src} |".format(
                page=image.page_url,
                bytes=image.bytes or "",
                status=image.status or "",
                dimensions=dimensions,
                loading=image.loading or "",
                priority=image.fetchpriority or "",
                srcset="yes" if image.has_srcset else "no",
                src=image.src[:180],
            )
        )

    lines.extend(
        [
            "",
            "## Matrix C - Blocking Script Candidates",
            "",
            "| Page | Count | Sources |",
            "|---|---:|---|",
        ]
    )
    for page in data["page_inspections"]:
        lines.append(
            f"| {page['url']} | {len(page['blocking_scripts'])} | {', '.join(page['blocking_scripts'][:4])} |"
        )

    lines.extend(
        [
            "",
            "## Matrix D - URL Hygiene",
            "",
            "| Check | Result |",
            "|---|---|",
        ]
    )
    redirect_findings = []
    for row in data["routes"]:
        representative = row["warm"][-1] if row["warm"] else row["cold"][-1]
        if representative.redirects and representative.redirects > 1:
            redirect_findings.append(f"{row['route']} has {representative.redirects} redirects")
    lines.append(
        f"| Route redirect depth | {'; '.join(redirect_findings) if redirect_findings else 'All sampled routes are 0-1 redirect hop.'} |"
    )

    link_findings = []
    for page in data["page_inspections"]:
        link_findings.extend(page["internal_noncanonical_links"])
    unique_links = sorted(set(link_findings))
    lines.append(
        f"| Homepage/post internal links missing trailing slash | {', '.join(unique_links[:20]) if unique_links else 'None found in inspected pages.'} |"
    )

    lines.extend(
        [
            "",
            "## Immediate Recommendations",
            "",
            "- Use this report as the baseline for issue #125 before changing Jetpack Boost, theme scripts, or image payloads.",
            "- Prioritize any image over 500 KB that lacks local ownership, explicit dimensions, or responsive metadata.",
            "- Keep Track A image/content updates separate from Track B theme/script updates.",
            "- Re-run this command after every optimization pass and compare the Matrix A route table plus Matrix B top images.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    base_url = args.base_url.rstrip("/")
    session = requests.Session()
    session.headers.update({"User-Agent": "kriskrug-performance-audit/1.0"})
    routes = [route.strip() for route in args.routes.split(",") if route.strip()]

    route_rows = []
    for route in routes:
        cold = [probe_route(base_url, route, "cold", args.timeout) for _ in range(args.samples)]
        probe_route(base_url, route, "warm", args.timeout)
        warm = [probe_route(base_url, route, "warm", args.timeout) for _ in range(args.samples)]
        route_rows.append({"route": route, "cold": cold, "warm": warm})

    asset_pages = [base_url + "/"]
    longform = args.longform_url or latest_post_url(session, base_url, args.timeout)
    asset_pages.append(route_url(base_url, longform))
    page_inspections = [inspect_page(session, base_url, page_url, args.timeout) for page_url in asset_pages]

    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "base_url": base_url,
        "samples": args.samples,
        "routes": route_rows,
        "asset_pages": asset_pages,
        "page_inspections": page_inspections,
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
    data = build_report(args)
    if args.format == "json":
        output = json.dumps(data, default=serialize_probe, indent=2)
    else:
        output = render_markdown(data)

    if args.output:
        path = Path(args.output)
        if not path.is_absolute():
            path = REPO_ROOT / path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(output, encoding="utf-8")
        print(f"report={path}")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
