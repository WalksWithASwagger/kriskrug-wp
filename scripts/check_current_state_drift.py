#!/usr/bin/env python3
"""Compare declared current-state values against live read-only checks."""

from __future__ import annotations

import base64
import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


@dataclass
class CommandResult:
    command: list[str]
    returncode: int
    stdout: str
    stderr: str


def run_command(command: list[str], cwd: Path) -> CommandResult:
    completed = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    return CommandResult(
        command=command,
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
    )


def load_json_result(command: list[str], cwd: Path) -> tuple[Any | None, str | None]:
    result = run_command(command, cwd)
    if result.returncode != 0:
        message = (
            f"command failed ({result.returncode}): {' '.join(command)}\n"
            f"stderr: {result.stderr.strip() or '(empty)'}"
        )
        return None, message
    try:
        return json.loads(result.stdout), None
    except json.JSONDecodeError as exc:
        message = (
            f"invalid JSON from command: {' '.join(command)}\n"
            f"error: {exc}\n"
            f"stdout (first 200 chars): {result.stdout[:200]!r}"
        )
        return None, message


def parse_declared_values(work_plan: Path) -> dict[str, Any]:
    text = work_plan.read_text(encoding="utf-8")
    patterns: dict[str, str] = {
        "open_prs": r"Open PRs:\s*`(\d+)`",
        "open_issues": r"Open issues:\s*`(\d+)`",
        "wp_version": r"Production still publicly reports WordPress `([^`]+)`",
        "future_posts": r"WordPress draft queue:\s*`(\d+)`\s*scheduled posts,",
        "draft_posts": r"WordPress draft queue:\s*`\d+`\s*scheduled posts,\s*`(\d+)`\s*draft posts,",
        "draft_pages": r"WordPress draft queue:\s*`\d+`\s*scheduled posts,\s*`\d+`\s*draft posts,\s*`(\d+)`\s*draft pages\.",
    }
    declared: dict[str, Any] = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if not match:
            declared[key] = None
            continue
        value = match.group(1)
        declared[key] = int(value) if key != "wp_version" else value
    return declared


def fetch_wp_queue_counts(repo_root: Path) -> tuple[dict[str, int] | None, str | None]:
    env_path = repo_root / "scripts/notion-to-wp/.env"
    if not env_path.exists():
        return None, f"missing env file: {env_path}"

    values: dict[str, str] = {}
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")

    base_url = values.get("WP_BASE_URL", "https://kriskrug.co").rstrip("/")
    user = values.get("WP_USER", "")
    app_password = (values.get("WP_APP_PASSWORD", "") or "").replace(" ", "")
    if not user or not app_password:
        return None, "WordPress credentials missing in scripts/notion-to-wp/.env"

    token = base64.b64encode(f"{user}:{app_password}".encode()).decode()
    headers = {"Authorization": f"Basic {token}", "Accept": "application/json"}

    def count(kind: str, status: str) -> int:
        query = urlencode({"status": status, "per_page": 1, "context": "edit"})
        url = f"{base_url}/wp-json/wp/v2/{kind}?{query}"
        request = Request(url, headers=headers)
        try:
            with urlopen(request, timeout=30) as response:
                return int(response.headers.get("X-WP-Total", "0") or "0")
        except HTTPError as exc:
            if exc.code == 400:
                return 0
            raise
        except URLError:
            raise

    try:
        return {
            "future_posts": count("posts", "future"),
            "draft_posts": count("posts", "draft"),
            "draft_pages": count("pages", "draft"),
        }, None
    except Exception as exc:
        return None, f"failed to fetch live draft queue counts: {exc}"


def evaluate_drift(declared: dict[str, Any], observed: dict[str, Any]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    labels = [
        ("open_prs", "Open PRs"),
        ("open_issues", "Open Issues"),
        ("wp_version", "WordPress Version"),
        ("future_posts", "Scheduled Posts"),
        ("draft_posts", "Draft Posts"),
        ("draft_pages", "Draft Pages"),
    ]
    for key, label in labels:
        declared_value = declared.get(key)
        observed_value = observed.get(key)
        drift = declared_value is not None and observed_value is not None and declared_value != observed_value
        checks.append(
            {
                "key": key,
                "label": label,
                "declared": declared_value,
                "observed": observed_value,
                "drift": drift,
            }
        )
    return checks


def render_human(report: dict[str, Any]) -> str:
    lines = [
        "# Current-State Drift Check",
        "",
        f"- Work plan: `{report['work_plan']}`",
        f"- Base URL: `{report['base_url']}`",
        "",
        "| Signal | Declared | Observed | Drift |",
        "|---|---:|---:|---|",
    ]
    for check in report["checks"]:
        declared = check["declared"] if check["declared"] is not None else "(missing)"
        observed = check["observed"] if check["observed"] is not None else "(missing)"
        drift = "YES" if check["drift"] else "no"
        lines.append(f"| {check['label']} | {declared} | {observed} | {drift} |")

    errors = report.get("errors", [])
    if errors:
        lines.extend(["", "## Command Errors", ""])
        for error in errors:
            lines.append(f"- {error}")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--work-plan",
        type=Path,
        default=Path("docs/current-state/WORK-PLAN-2026-05-23.md"),
        help="Path to the state doc containing declared snapshot values.",
    )
    parser.add_argument("--base-url", default="https://kriskrug.co", help="Site URL for smoke checks.")
    parser.add_argument("--json", action="store_true", help="Print JSON report.")
    parser.add_argument("--fail-on-drift", action="store_true", help="Exit non-zero if any drift is detected.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    work_plan = (repo_root / args.work_plan).resolve() if not args.work_plan.is_absolute() else args.work_plan

    declared = parse_declared_values(work_plan)
    errors: list[str] = []

    prs_json, prs_error = load_json_result(
        ["gh", "pr", "list", "--state", "open", "--limit", "50", "--json", "number"],
        repo_root,
    )
    issues_json, issues_error = load_json_result(
        ["gh", "issue", "list", "--state", "open", "--limit", "200", "--json", "number"],
        repo_root,
    )

    wp_counts, wp_counts_error = fetch_wp_queue_counts(repo_root)

    smoke_json, smoke_error = load_json_result(
        [sys.executable, "scripts/wp7-public-smoke.py", "--base-url", args.base_url, "--json"],
        repo_root,
    )

    for error in (prs_error, issues_error, wp_counts_error, smoke_error):
        if error:
            errors.append(error)

    observed = {
        "open_prs": len(prs_json or []),
        "open_issues": len(issues_json or []),
        "wp_version": (smoke_json or {}).get("observed_wordpress_version"),
        "future_posts": None if not wp_counts else wp_counts["future_posts"],
        "draft_posts": None if not wp_counts else wp_counts["draft_posts"],
        "draft_pages": None if not wp_counts else wp_counts["draft_pages"],
    }

    checks = evaluate_drift(declared, observed)
    report = {
        "work_plan": str(work_plan),
        "base_url": args.base_url,
        "checks": checks,
        "errors": errors,
    }

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(render_human(report))

    drift_found = any(check["drift"] for check in checks)
    if args.fail_on_drift and (drift_found or errors):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
