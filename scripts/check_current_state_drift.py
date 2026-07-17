#!/usr/bin/env python3
"""Compare declared current-state values against live read-only checks."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from common import WPClient, wp_queue_counts


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
    has_env_file = env_path.exists()
    has_process_creds = bool(os.environ.get("WP_USER") and os.environ.get("WP_APP_PASSWORD"))
    if not has_env_file and not has_process_creds:
        return None, (
            f"WordPress credentials unavailable: missing env file: {env_path} "
            "and WP_USER/WP_APP_PASSWORD not set in process env"
        )

    try:
        client = WPClient.from_env(env_path if has_env_file else None, timeout=30)
        return wp_queue_counts(client), None
    except Exception as exc:
        return None, f"failed to fetch live draft queue counts: {exc}"


def build_observed(
    prs_json: Any,
    issues_json: Any,
    wp_counts: dict[str, int] | None,
    smoke_json: Any,
) -> dict[str, Any]:
    """Map raw check payloads to observed values; failed sources stay None, never 0."""
    return {
        "open_prs": len(prs_json) if isinstance(prs_json, list) else None,
        "open_issues": len(issues_json) if isinstance(issues_json, list) else None,
        "wp_version": smoke_json.get("observed_wordpress_version") if isinstance(smoke_json, dict) else None,
        "future_posts": wp_counts["future_posts"] if wp_counts else None,
        "draft_posts": wp_counts["draft_posts"] if wp_counts else None,
        "draft_pages": wp_counts["draft_pages"] if wp_counts else None,
    }


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
        evaluated = declared_value is not None and observed_value is not None
        drift = evaluated and declared_value != observed_value
        if drift:
            status = "drift"
        elif evaluated:
            status = "no drift"
        else:
            status = "not evaluated"
        checks.append(
            {
                "key": key,
                "label": label,
                "declared": declared_value,
                "observed": observed_value,
                "evaluated": evaluated,
                "drift": drift,
                "status": status,
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
        observed = check["observed"] if check["observed"] is not None else "unavailable"
        if not check.get("evaluated", True):
            drift = "not evaluated"
        else:
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
    parser.add_argument(
        "--fail-on-drift",
        action="store_true",
        help="Exit non-zero if any drift or check error is detected (opt-in automation gate).",
    )
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

    observed = build_observed(prs_json, issues_json, wp_counts, smoke_json)

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
