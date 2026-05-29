#!/usr/bin/env python3
"""PII-safe, read-only Jetpack Forms feedback audit."""

from __future__ import annotations

import argparse
import base64
import json
import re
from dataclasses import dataclass
from html import unescape
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


DEFAULT_ENV_FILE = Path("scripts/notion-to-wp/.env")


@dataclass
class Config:
    base_url: str
    user: str
    app_password: str


def load_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def load_config(env_file: Path, base_url: str | None) -> Config:
    values = load_env(env_file)
    resolved_base_url = (base_url or values.get("WP_BASE_URL") or "https://kriskrug.co").rstrip("/")
    user = values.get("WP_USER")
    app_password = (values.get("WP_APP_PASSWORD") or "").replace(" ", "")
    if not user or not app_password:
        raise SystemExit(f"Missing WP_USER/WP_APP_PASSWORD in {env_file}")
    return Config(base_url=resolved_base_url, user=user, app_password=app_password)


def auth_header(config: Config) -> str:
    token = base64.b64encode(f"{config.user}:{config.app_password}".encode()).decode()
    return f"Basic {token}"


def get_json(config: Config, path: str, timeout: int, params: dict[str, Any] | None = None) -> dict[str, Any]:
    url = config.base_url + path
    if params:
        url += "?" + urlencode(params, doseq=True)
    request = Request(
        url,
        headers={
            "Authorization": auth_header(config),
            "Accept": "application/json",
            "User-Agent": "kriskrug-jetpack-feedback-audit/1.0",
        },
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            body = response.read(2_000_000).decode(response.headers.get_content_charset() or "utf-8", "replace")
            return {
                "http_status": response.status,
                "headers": {
                    "x_wp_total": response.headers.get("X-WP-Total"),
                    "x_wp_total_pages": response.headers.get("X-WP-TotalPages"),
                },
                "payload": json.loads(body),
            }
    except HTTPError as exc:
        body = exc.read(500_000).decode("utf-8", "replace")
        try:
            payload: Any = json.loads(body)
        except json.JSONDecodeError:
            payload = body[:1000]
        return {"http_status": exc.code, "headers": {}, "payload": payload}
    except (URLError, TimeoutError, json.JSONDecodeError) as exc:
        return {"http_status": None, "headers": {}, "payload": str(exc)}


def strip_html(value: str | None) -> str:
    if not value:
        return ""
    text = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", unescape(text)).strip()


def summarize_config(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {"available": False, "raw_type": type(payload).__name__}
    return {
        "available": True,
        "has_classic_forms": bool(payload.get("hasClassicForms")),
        "has_feedback": bool(payload.get("hasFeedback")),
        "central_form_management_enabled": bool(payload.get("isCentralFormManagementEnabled")),
        "integrations_enabled": bool(payload.get("isIntegrationsEnabled")),
        "mailpoet_enabled": bool(payload.get("isMailPoetEnabled")),
        "notes_enabled": bool(payload.get("isNotesEnabled")),
        "webhooks_enabled": bool(payload.get("isWebhooksEnabled")),
        "dashboard_available": bool(payload.get("formsResponsesUrl") or payload.get("dashboardURL")),
    }


def find_form_blocks(page: dict[str, Any]) -> dict[str, Any] | None:
    raw_content = page.get("content", {}).get("raw") or ""
    if not re.search(r"jetpack/(contact-form|field)|contact-form|wpforms|gravityform|formidable", raw_content, re.I):
        return None

    jetpack_forms = []
    for match in re.finditer(r"<!--\s+wp:jetpack/contact-form\s+(\{.*?\})\s+-->", raw_content):
        try:
            attrs = json.loads(match.group(1))
        except json.JSONDecodeError:
            attrs = {}
        routing_keys = sorted(key for key in attrs if re.search(r"email|recipient|subject|to", key, re.I))
        jetpack_forms.append({"routing_attr_keys": routing_keys})

    title = page.get("title", {}).get("rendered")
    return {
        "id": page.get("id"),
        "slug": page.get("slug"),
        "status": page.get("status"),
        "title": strip_html(title),
        "jetpack_contact_form_blocks": len(jetpack_forms),
        "routing_attrs_redacted": jetpack_forms,
    }


def scan_pages_for_forms(config: Config, timeout: int) -> dict[str, Any]:
    result = get_json(
        config,
        "/wp-json/wp/v2/pages",
        timeout,
        {
            "context": "edit",
            "status": "publish,draft,private",
            "per_page": 100,
            "_fields": "id,slug,status,title,content.raw",
        },
    )
    payload = result.get("payload")
    pages = payload if isinstance(payload, list) else []
    form_pages = [summary for page in pages if (summary := find_form_blocks(page))]
    return {
        "http_status": result.get("http_status"),
        "pages_scanned": len(pages),
        "form_pages": form_pages,
    }


def collect(config: Config, timeout: int) -> dict[str, Any]:
    counts = get_json(config, "/wp-json/wp/v2/feedback/counts", timeout)
    sample = get_json(
        config,
        "/wp-json/wp/v2/feedback",
        timeout,
        {"per_page": 1, "_fields": "id,date,status,type"},
    )
    forms_config = get_json(config, "/wp-json/wp/v2/feedback/config", timeout)
    jetpack_forms = get_json(
        config,
        "/wp-json/wp/v2/jetpack-forms",
        timeout,
        {"per_page": 1, "_fields": "id,date,status,slug,title"},
    )
    return {
        "base_url": config.base_url,
        "privacy": {
            "message_bodies_requested": False,
            "names_or_emails_requested": False,
            "attachments_requested": False,
            "csv_export_requested": False,
        },
        "feedback_counts": {
            "http_status": counts.get("http_status"),
            "payload": counts.get("payload"),
        },
        "feedback_meta_only_sample": {
            "http_status": sample.get("http_status"),
            "total": sample.get("headers", {}).get("x_wp_total"),
            "fields_requested": ["id", "date", "status", "type"],
            "sample_count": len(sample.get("payload") or []) if isinstance(sample.get("payload"), list) else None,
        },
        "feedback_config": {
            "http_status": forms_config.get("http_status"),
            "payload": summarize_config(forms_config.get("payload")),
        },
        "jetpack_forms": {
            "http_status": jetpack_forms.get("http_status"),
            "total": jetpack_forms.get("headers", {}).get("x_wp_total"),
        },
        "page_form_scan": scan_pages_for_forms(config, timeout),
    }


def has_failure(report: dict[str, Any]) -> bool:
    checks = [
        report["feedback_counts"]["http_status"],
        report["feedback_meta_only_sample"]["http_status"],
        report["feedback_config"]["http_status"],
        report["jetpack_forms"]["http_status"],
        report["page_form_scan"]["http_status"],
    ]
    return any(status != 200 for status in checks)


def print_human(report: dict[str, Any]) -> None:
    print(f"Jetpack feedback audit: {report['base_url']}")
    counts = report["feedback_counts"]["payload"]
    if isinstance(counts, dict):
        print(
            "Feedback counts: "
            f"inbox {counts.get('inbox', 0)}, spam {counts.get('spam', 0)}, trash {counts.get('trash', 0)}"
        )
    else:
        print(f"Feedback counts unavailable: {counts}")
    print(f"Feedback endpoint total: {report['feedback_meta_only_sample']['total']}")
    print(f"Jetpack form records total: {report['jetpack_forms']['total']}")
    config = report["feedback_config"]["payload"]
    print(f"Forms config: {json.dumps(config, sort_keys=True)}")
    scan = report["page_form_scan"]
    print(f"Page form scan: {scan['pages_scanned']} pages scanned, {len(scan['form_pages'])} form pages found")
    for page in scan["form_pages"]:
        print(f"  - {page['slug']} ({page['id']}): routing keys redacted {page['routing_attrs_redacted']}")
    print("")
    print("Privacy guard: did not request names, emails, message bodies, attachments, or CSV exports.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a PII-safe, read-only Jetpack Forms feedback audit.")
    parser.add_argument("--env-file", default=str(DEFAULT_ENV_FILE), help="Path to gitignored WordPress connector .env.")
    parser.add_argument("--base-url", help="Override WP_BASE_URL from the env file.")
    parser.add_argument("--timeout", type=int, default=30, help="Request timeout in seconds.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of human-readable output.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = load_config(Path(args.env_file), args.base_url)
    report = collect(config, args.timeout)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_human(report)
    return 1 if has_failure(report) else 0


if __name__ == "__main__":
    raise SystemExit(main())
