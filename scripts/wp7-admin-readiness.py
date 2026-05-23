#!/usr/bin/env python3
"""Authenticated read-only WordPress readiness snapshot for the WP 7 rollout."""

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
from urllib.request import Request, urlopen


DEFAULT_ENV_FILE = Path("scripts/notion-to-wp/.env")
SITE_HEALTH_TESTS = (
    "https-status",
    "loopback-requests",
    "dotorg-communication",
    "authorization-header",
    "background-updates",
    "page-cache",
)


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


def load_config(path: Path) -> Config:
    values = load_env(path)
    base_url = values.get("WP_BASE_URL", "https://kriskrug.co").rstrip("/")
    user = values.get("WP_USER")
    app_password = (values.get("WP_APP_PASSWORD") or "").replace(" ", "")
    if not user or not app_password:
        raise SystemExit(f"Missing WP_USER/WP_APP_PASSWORD in {path}")
    return Config(base_url=base_url, user=user, app_password=app_password)


def auth_header(config: Config) -> str:
    token = base64.b64encode(f"{config.user}:{config.app_password}".encode()).decode()
    return f"Basic {token}"


def get_json(config: Config, path: str, timeout: int) -> dict[str, Any]:
    request = Request(
        config.base_url + path,
        headers={
            "Authorization": auth_header(config),
            "Accept": "application/json",
            "User-Agent": "kriskrug-wp7-admin-readiness/1.0",
        },
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            body = response.read(2_000_000).decode(response.headers.get_content_charset() or "utf-8", "replace")
            return {"http_status": response.status, "payload": json.loads(body)}
    except HTTPError as exc:
        body = exc.read(500_000).decode("utf-8", "replace")
        try:
            payload: Any = json.loads(body)
        except json.JSONDecodeError:
            payload = body[:1000]
        return {"http_status": exc.code, "payload": payload}
    except (URLError, TimeoutError, json.JSONDecodeError) as exc:
        return {"http_status": None, "payload": str(exc)}


def strip_html(value: str | None) -> str | None:
    if value is None:
        return None
    text = re.sub(r"<[^>]+>", " ", value)
    text = re.sub(r"\s+", " ", unescape(text)).strip()
    return text


def summarize_user(payload: Any) -> Any:
    if not isinstance(payload, dict):
        return payload
    capabilities = payload.get("capabilities") or {}
    return {
        "id": payload.get("id"),
        "slug": payload.get("slug"),
        "roles": payload.get("roles"),
        "can_update_core": bool(capabilities.get("update_core")),
        "can_update_plugins": bool(capabilities.get("update_plugins")),
        "can_activate_plugins": bool(capabilities.get("activate_plugins")),
    }


def summarize_plugins(payload: Any) -> Any:
    if not isinstance(payload, list):
        return payload
    return [
        {
            "plugin": item.get("plugin"),
            "name": item.get("name"),
            "version": item.get("version"),
            "status": item.get("status"),
        }
        for item in payload
    ]


def summarize_themes(payload: Any) -> Any:
    if not isinstance(payload, list):
        return payload
    themes = []
    for item in payload:
        name = item.get("name")
        if isinstance(name, dict):
            name = name.get("rendered")
        themes.append(
            {
                "stylesheet": item.get("stylesheet"),
                "name": name,
                "version": item.get("version"),
                "status": item.get("status"),
            }
        )
    return themes


def summarize_health(payload: Any) -> Any:
    if not isinstance(payload, dict):
        return payload
    return {
        "label": payload.get("label"),
        "status": payload.get("status"),
        "badge": payload.get("badge"),
        "description": strip_html(payload.get("description")),
    }


def collect(config: Config, timeout: int) -> dict[str, Any]:
    report: dict[str, Any] = {"base_url": config.base_url, "checks": {}}
    endpoints = {
        "current_user": ("/wp-json/wp/v2/users/me?context=edit", summarize_user),
        "active_theme": ("/wp-json/wp/v2/themes?status=active", summarize_themes),
        "active_plugins": ("/wp-json/wp/v2/plugins?status=active&context=edit", summarize_plugins),
        "inactive_plugins": ("/wp-json/wp/v2/plugins?status=inactive&context=edit", summarize_plugins),
    }
    for name, (path, summarizer) in endpoints.items():
        result = get_json(config, path, timeout)
        report["checks"][name] = {"http_status": result["http_status"], "payload": summarizer(result["payload"])}
    for test in SITE_HEALTH_TESTS:
        result = get_json(config, f"/wp-json/wp-site-health/v1/tests/{test}", timeout)
        report["checks"][f"site_health_{test}"] = {
            "http_status": result["http_status"],
            "payload": summarize_health(result["payload"]),
        }
    return report


def has_endpoint_failure(report: dict[str, Any]) -> bool:
    return any(check.get("http_status") != 200 for check in report["checks"].values())


def has_health_critical(report: dict[str, Any]) -> bool:
    for name, check in report["checks"].items():
        if not name.startswith("site_health_"):
            continue
        payload = check.get("payload")
        if isinstance(payload, dict) and payload.get("status") == "critical":
            return True
    return False


def print_human(report: dict[str, Any]) -> None:
    print(f"WordPress admin readiness: {report['base_url']}")
    user = report["checks"]["current_user"]
    print(f"Auth user: {json.dumps(user['payload'], sort_keys=True)}")
    print("")
    for theme in report["checks"]["active_theme"]["payload"]:
        print(f"Theme: {theme['name']} ({theme['stylesheet']}) {theme['version']} [{theme['status']}]")
    print("")
    print("Active plugins:")
    for plugin in report["checks"]["active_plugins"]["payload"]:
        print(f"  - {plugin['name']} {plugin['version']} ({plugin['plugin']})")
    print("")
    inactive = report["checks"]["inactive_plugins"]["payload"]
    if inactive:
        print("Inactive plugins:")
        for plugin in inactive:
            print(f"  - {plugin['name']} {plugin['version']} ({plugin['plugin']})")
        print("")
    print("Site Health REST tests:")
    for name, check in report["checks"].items():
        if not name.startswith("site_health_"):
            continue
        payload = check["payload"]
        status = payload.get("status") if isinstance(payload, dict) else "unknown"
        label = payload.get("label") if isinstance(payload, dict) else payload
        print(f"  - {status}: {label}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Collect an authenticated read-only WordPress 7 readiness snapshot.")
    parser.add_argument("--env-file", default=str(DEFAULT_ENV_FILE), help="Path to gitignored WordPress connector .env.")
    parser.add_argument("--timeout", type=int, default=30, help="Request timeout in seconds.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of human-readable output.")
    parser.add_argument("--fail-on-health-critical", action="store_true", help="Return non-zero when Site Health reports critical checks.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = load_config(Path(args.env_file))
    report = collect(config, args.timeout)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_human(report)
    if has_endpoint_failure(report):
        return 1
    if args.fail_on_health_critical and has_health_critical(report):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
