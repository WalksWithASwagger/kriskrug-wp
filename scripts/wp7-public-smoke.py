#!/usr/bin/env python3
"""Read-only public smoke checks for the WordPress 7 rollout."""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from dataclasses import dataclass
from html import unescape
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


DEFAULT_PATHS = (
    "/",
    "/blog/",
    "/speaking/",
    "/work/",
    "/contact/",
    "/wp-json/",
    "/sitemap.xml",
    "/?s=ai",
)

FATAL_PATTERNS = (
    "Fatal error",
    "Parse error",
    "There has been a critical error",
    "Error establishing a database connection",
    "Briefly unavailable for scheduled maintenance",
)


@dataclass
class FetchResult:
    url: str
    status: int | None
    final_url: str | None
    content_type: str
    body: str
    error: str | None = None


def build_url(base_url: str, path: str) -> str:
    base = base_url.rstrip("/") + "/"
    if path.startswith("http://") or path.startswith("https://"):
        return path
    if path.startswith("?"):
        return base + path
    return urljoin(base, path.lstrip("/"))


def fetch(url: str, timeout: int) -> FetchResult:
    request = Request(
        url,
        headers={
            "User-Agent": "kriskrug-wp7-smoke/1.0 (+https://github.com/WalksWithASwagger/kriskrug-wp)",
            "Accept": "text/html,application/json,application/xml;q=0.9,*/*;q=0.8",
        },
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            raw = response.read(2_000_000)
            charset = response.headers.get_content_charset() or "utf-8"
            return FetchResult(
                url=url,
                status=response.status,
                final_url=response.geturl(),
                content_type=response.headers.get("content-type", ""),
                body=raw.decode(charset, errors="replace"),
            )
    except HTTPError as exc:
        raw = exc.read(200_000)
        charset = exc.headers.get_content_charset() or "utf-8"
        return FetchResult(
            url=url,
            status=exc.code,
            final_url=exc.geturl(),
            content_type=exc.headers.get("content-type", ""),
            body=raw.decode(charset, errors="replace"),
            error=str(exc),
        )
    except URLError as exc:
        return FetchResult(url=url, status=None, final_url=None, content_type="", body="", error=str(exc))


def extract_wordpress_version(html: str) -> str | None:
    match = re.search(r'<meta\s+name=["\']generator["\']\s+content=["\']WordPress\s+([^"\']+)["\']', html, re.I)
    if match:
        return unescape(match.group(1)).strip()
    match = re.search(r"wp-emoji-release\.min\.js\?ver=([0-9][^\"'&< ]*)", html)
    return match.group(1).strip() if match else None


def extract_theme(html: str) -> str | None:
    match = re.search(r"wp-content/themes/([^/]+)/", html)
    if not match:
        return None
    slug = match.group(1)
    version = re.search(rf"wp-content/themes/{re.escape(slug)}/[^\"']+\?ver=([^\"'&< ]+)", html)
    return f"{slug} {unescape(version.group(1))}" if version else slug


def extract_plugin_versions(html: str) -> dict[str, str]:
    plugins: dict[str, str] = {}
    for slug in ("jetpack", "popup-maker", "google-site-kit", "zero-bs-crm"):
        plugin_match = re.search(rf"wp-content/plugins/{re.escape(slug)}/[^\"']+\?[^\"']*ver=([^\"'&< ]+)", html)
        if plugin_match:
            plugins[slug] = unescape(plugin_match.group(1))
    sitekit = re.search(r'<meta\s+name=["\']generator["\']\s+content=["\']Site Kit by Google\s+([^"\']+)["\']', html, re.I)
    if sitekit:
        plugins["google-site-kit"] = unescape(sitekit.group(1))
    popup = re.search(r"pum-site-[^\"']+ver=([^\"'&< ]+)", html)
    if popup:
        plugins["popup-maker"] = unescape(popup.group(1))
    return plugins


def has_metadata(html: str) -> bool:
    return bool(re.search(r'property=["\']og:title["\']', html, re.I)) and bool(
        re.search(r'name=["\']twitter:(card|title)["\']', html, re.I)
    )


def has_schema(html: str) -> bool:
    return bool(re.search(r'<script[^>]+application/ld\+json', html, re.I))


def check_rest_root(result: FetchResult) -> tuple[list[str], list[str], dict[str, Any]]:
    failures: list[str] = []
    warnings: list[str] = []
    details: dict[str, Any] = {}
    try:
        payload = json.loads(result.body)
    except json.JSONDecodeError as exc:
        return [f"REST root did not return JSON: {exc}"], warnings, details

    namespaces = set(payload.get("namespaces", []))
    details["site_name"] = payload.get("name")
    details["namespaces"] = sorted(namespaces)
    for namespace in ("wp/v2", "wp-site-health/v1"):
        if namespace not in namespaces:
            failures.append(f"missing REST namespace {namespace}")
    for namespace in ("jetpack/v4", "google-site-kit/v1", "redirection/v1", "code-snippets/v1"):
        if namespace not in namespaces:
            warnings.append(f"namespace not observed: {namespace}")
    return failures, warnings, details


def check_page(path: str, result: FetchResult) -> tuple[list[str], list[str], dict[str, Any]]:
    failures: list[str] = []
    warnings: list[str] = []
    details: dict[str, Any] = {"status": result.status, "content_type": result.content_type, "final_url": result.final_url}

    if result.status is None:
        failures.append(result.error or "request failed")
        return failures, warnings, details
    if result.status >= 400:
        failures.append(f"HTTP {result.status}")
    for pattern in FATAL_PATTERNS:
        if pattern.lower() in result.body.lower():
            failures.append(f"found fatal marker: {pattern}")

    if path == "/":
        details["wordpress_version"] = extract_wordpress_version(result.body)
        details["theme"] = extract_theme(result.body)
        details["plugins"] = extract_plugin_versions(result.body)
        if not details["wordpress_version"]:
            warnings.append("WordPress version not visible in public HTML")
        if not details["theme"]:
            warnings.append("theme asset not visible in public HTML")

    if path in ("/", "/speaking/", "/work/"):
        if not has_metadata(result.body):
            warnings.append("OG/Twitter metadata not fully visible")
        if not has_schema(result.body):
            warnings.append("JSON-LD schema not visible")

    if path == "/contact/" and "form" not in result.body.lower():
        warnings.append("contact page did not expose obvious form markup")

    return failures, warnings, details


def run(args: argparse.Namespace) -> dict[str, Any]:
    checks = []
    public_version = None
    started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    for path in args.path:
        url = build_url(args.base_url, path)
        result = fetch(url, args.timeout)
        if path == "/wp-json/":
            failures, warnings, details = check_rest_root(result)
            if result.status is not None and result.status >= 400:
                failures.insert(0, f"HTTP {result.status}")
        else:
            failures, warnings, details = check_page(path, result)
            if path == "/":
                public_version = details.get("wordpress_version")
        checks.append(
            {
                "path": path,
                "url": url,
                "status": "fail" if failures else "warn" if warnings else "pass",
                "failures": failures,
                "warnings": warnings,
                "details": details,
            }
        )

    if args.expect_version and public_version != args.expect_version:
        checks.append(
            {
                "path": "(version gate)",
                "url": args.base_url,
                "status": "fail",
                "failures": [f"expected WordPress {args.expect_version}, observed {public_version or 'unknown'}"],
                "warnings": [],
                "details": {},
            }
        )

    return {
        "base_url": args.base_url,
        "started_at": started,
        "observed_wordpress_version": public_version,
        "checks": checks,
    }


def print_human(report: dict[str, Any]) -> None:
    print(f"WordPress public smoke: {report['base_url']}")
    print(f"Started: {report['started_at']}")
    print(f"Observed WordPress version: {report.get('observed_wordpress_version') or 'unknown'}")
    print("")
    for check in report["checks"]:
        label = check["status"].upper()
        print(f"{label:4} {check['path']}")
        for failure in check["failures"]:
            print(f"     fail: {failure}")
        for warning in check["warnings"]:
            print(f"     warn: {warning}")
        details = check.get("details") or {}
        if details.get("theme"):
            print(f"     theme: {details['theme']}")
        if details.get("plugins"):
            plugins = ", ".join(f"{name}={version}" for name, version in sorted(details["plugins"].items()))
            print(f"     plugins: {plugins}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run read-only public smoke checks for a WordPress 7 rollout.")
    parser.add_argument("--base-url", default="https://kriskrug.co", help="Production or staging site URL.")
    parser.add_argument("--path", action="append", default=None, help="Path or URL to check. Repeat to override defaults.")
    parser.add_argument("--expect-version", help="Fail if the public WordPress version does not match.")
    parser.add_argument("--timeout", type=int, default=20, help="Request timeout in seconds.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of human-readable output.")
    parser.add_argument("--fail-on-warning", action="store_true", help="Return non-zero for warnings as well as failures.")
    args = parser.parse_args()
    args.path = args.path or list(DEFAULT_PATHS)
    return args


def main() -> int:
    args = parse_args()
    report = run(args)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_human(report)
    has_failure = any(check["status"] == "fail" for check in report["checks"])
    has_warning = any(check["status"] == "warn" for check in report["checks"])
    return 1 if has_failure or (args.fail_on_warning and has_warning) else 0


if __name__ == "__main__":
    raise SystemExit(main())
