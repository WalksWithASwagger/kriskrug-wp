#!/usr/bin/env python3
"""Generate a Track-A morning truth report."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from common import WPClient, wp_queue_counts


@dataclass
class CommandResult:
    title: str
    command: list[str]
    returncode: int
    stdout: str
    stderr: str


def run_command(title: str, command: list[str], cwd: Path, timeout: int = 120) -> CommandResult:
    try:
        completed = subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        return CommandResult(
            title=title,
            command=command,
            returncode=124,
            stdout=(exc.stdout or "").strip(),
            stderr=f"command timed out after {timeout}s",
        )
    return CommandResult(
        title=title,
        command=command,
        returncode=completed.returncode,
        stdout=completed.stdout.strip(),
        stderr=completed.stderr.strip(),
    )


def run_json_command(title: str, command: list[str], cwd: Path) -> tuple[CommandResult, Any | None]:
    result = run_command(title, command, cwd)
    if result.returncode != 0 or not result.stdout:
        return result, None
    try:
        return result, json.loads(result.stdout)
    except json.JSONDecodeError:
        return result, None


def parse_status_line(headers: str) -> str:
    for line in headers.splitlines():
        if line.startswith("HTTP/"):
            return line.strip()
    return "(status line not found)"


def parse_og_image(html: str) -> str:
    match = re.search(r'<meta\s+property=["\']og:image["\']\s+content=["\']([^"\']+)', html, flags=re.I)
    if not match:
        return "(not found)"
    return match.group(1)


def parse_worktree_sections(porcelain: str) -> list[dict[str, str]]:
    sections: list[dict[str, str]] = []
    current: dict[str, str] = {}
    for raw_line in porcelain.splitlines():
        line = raw_line.strip()
        if not line:
            if current:
                sections.append(current)
                current = {}
            continue
        key, _, value = line.partition(" ")
        current[key] = value
    if current:
        sections.append(current)
    return sections


def build_label_counts(issues_json: list[dict[str, Any]]) -> dict[str, int]:
    counts = {
        "priority:high": 0,
        "aurora-v2": 0,
        "track-b": 0,
        "swarm-ready": 0,
        "swarm-parked": 0,
        "needs-human-review": 0,
        "auto-implement": 0,
    }
    for issue in issues_json:
        labels = {label.get("name", "") for label in issue.get("labels", [])}
        for key in counts:
            if key in labels:
                counts[key] += 1
    return counts


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


def format_json_count(payload: Any) -> str:
    """Render a list length, or 'unavailable' when the source query failed."""
    return str(len(payload)) if isinstance(payload, list) else "unavailable"


def summarize_smoke(smoke_json: Any) -> dict[str, Any]:
    """Summarize public smoke JSON; an unavailable result never reads as 0 failures."""
    if not isinstance(smoke_json, dict):
        return {"available": False, "failures": None, "warnings": None, "observed_version": None}
    failures = 0
    warnings = 0
    for check in smoke_json.get("checks", []):
        if check.get("status") == "fail":
            failures += 1
        elif check.get("status") == "warn":
            warnings += 1
    return {
        "available": True,
        "failures": failures,
        "warnings": warnings,
        "observed_version": smoke_json.get("observed_wordpress_version"),
    }


def collect_truth_errors(
    prs_json: Any,
    issues_json: Any,
    queue_error: str | None,
    smoke_available: bool,
    drift_json: Any,
) -> list[str]:
    """List startup truth data sources that could not be evaluated."""
    errors: list[str] = []
    if not isinstance(prs_json, list):
        errors.append("open PR list unavailable (gh pr list JSON failed or was unparsable)")
    if not isinstance(issues_json, list):
        errors.append("open issue list unavailable (gh issue list JSON failed or was unparsable)")
    if queue_error:
        errors.append(f"draft queue counts unavailable: {queue_error}")
    if not smoke_available:
        errors.append("public smoke result unavailable (missing or unparsable JSON); treat as degraded")
    if not isinstance(drift_json, dict):
        errors.append("current-state drift report unavailable (command or parsing failure)")
    return errors


def render_command_block(result: CommandResult) -> str:
    lines = [
        f"### {result.title}",
        "",
        f"- Command: `{ ' '.join(result.command) }`",
        f"- Exit code: `{result.returncode}`",
    ]
    if result.stdout:
        lines.extend(["", "```text", result.stdout, "```"])
    if result.stderr:
        lines.extend(["", "stderr:", "```text", result.stderr, "```"])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="https://kriskrug.co")
    parser.add_argument("--expect-version", default="6.9.4")
    parser.add_argument(
        "--work-plan",
        default="docs/current-state/WORK-PLAN-2026-05-23.md",
        help="Declared state doc used for drift checks.",
    )
    parser.add_argument("--command-timeout", type=int, default=120, help="Timeout for shell subcommands in seconds.")
    parser.add_argument("--request-timeout", type=int, default=20, help="Timeout for each public smoke HTTP request.")
    parser.add_argument("--out", help="Write report to this path.")
    parser.add_argument("--stdout", action="store_true", help="Print the report instead of writing a file.")
    parser.add_argument("--skip-fetch", action="store_true", help="Skip git fetch for strictly non-mutating runs.")
    parser.add_argument(
        "--fail-on-error",
        action="store_true",
        help="Exit non-zero when any startup truth data source is unavailable (opt-in automation gate).",
    )
    args = parser.parse_args()
    if args.stdout and args.out:
        parser.error("--stdout cannot be combined with --out")

    repo_root = Path(__file__).resolve().parents[1]
    now = datetime.now(UTC)
    stamp = now.strftime("%Y%m%d-%H%M%SZ")
    out_path = None
    if not args.stdout:
        out_path = Path(args.out) if args.out else repo_root / "docs/current-state/reports" / f"morning-truth-{stamp}.md"
        if not out_path.is_absolute():
            out_path = (repo_root / out_path).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)

    startup_results = []
    if not args.skip_fetch:
        startup_results.append(
            run_command("Git Fetch", ["git", "fetch", "--prune"], repo_root, timeout=args.command_timeout)
        )
    startup_results.extend([
        run_command("Git Status", ["git", "status", "--short", "--branch"], repo_root, timeout=args.command_timeout),
        run_command("Recent Log", ["git", "log", "--oneline", "-n", "20"], repo_root, timeout=args.command_timeout),
        run_command("Open PRs", ["gh", "pr", "list", "--state", "open", "--limit", "50"], repo_root, timeout=args.command_timeout),
        run_command("Open Issues", ["gh", "issue", "list", "--state", "open", "--limit", "200"], repo_root, timeout=args.command_timeout),
        run_command("Worktrees", ["git", "worktree", "list", "--porcelain"], repo_root, timeout=args.command_timeout),
        run_command("Main Divergence", ["git", "rev-list", "--left-right", "--count", "origin/main...main"], repo_root, timeout=args.command_timeout),
        run_command(
            "Aurora vs Main Divergence",
            ["git", "rev-list", "--left-right", "--count", "origin/aurora/v2...origin/main"],
            repo_root,
            timeout=args.command_timeout,
        ),
    ])

    issues_json_result, issues_json = run_json_command(
        "Issue JSON",
        ["gh", "issue", "list", "--state", "open", "--limit", "200", "--json", "number,title,labels,updatedAt"],
        repo_root,
    )
    prs_json_result, prs_json = run_json_command(
        "PR JSON",
        ["gh", "pr", "list", "--state", "open", "--limit", "50", "--json", "number,title,updatedAt"],
        repo_root,
    )

    queue_counts, queue_error = fetch_wp_queue_counts(repo_root)
    draft_result = CommandResult(
        title="Draft Queue Counts (REST, read-only)",
        command=["python3", "scripts/morning_truth_report.py", "(internal queue fetch)"],
        returncode=0 if not queue_error else 1,
        stdout=(
            f"future_posts={queue_counts['future_posts']}, "
            f"draft_posts={queue_counts['draft_posts']}, "
            f"draft_pages={queue_counts['draft_pages']}"
            if queue_counts
            else ""
        ),
        stderr=queue_error or "",
    )
    smoke_result, smoke_json = run_json_command(
        "WP7 Public Smoke (JSON)",
        [
            sys.executable,
            "scripts/wp7-public-smoke.py",
            "--base-url",
            args.base_url,
            "--expect-version",
            args.expect_version,
            "--timeout",
            str(args.request_timeout),
            "--json",
        ],
        repo_root,
    )
    drift_result, drift_json = run_json_command(
        "Current-State Drift Check (JSON)",
        [
            sys.executable,
            "scripts/check_current_state_drift.py",
            "--base-url",
            args.base_url,
            "--work-plan",
            args.work_plan,
            "--json",
        ],
        repo_root,
    )

    cache_bust = now.strftime("%Y%m%d%H%M%S")
    projects_headers = run_command(
        "Projects URL Headers",
        ["curl", "-sI", f"{args.base_url.rstrip('/')}/projects/"],
        repo_root,
    )
    work_page_html = run_command(
        "Work Page HTML",
        ["curl", "-sL", f"{args.base_url.rstrip('/')}/recent-projects-include/?cachebust={cache_bust}"],
        repo_root,
    )
    home_page_html = run_command(
        "Homepage HTML",
        ["curl", "-sL", f"{args.base_url.rstrip('/')}/?cachebust={cache_bust}"],
        repo_root,
    )

    worktrees_output = next((item.stdout for item in startup_results if item.title == "Worktrees"), "")
    aurora_branch_section = None
    for section in parse_worktree_sections(worktrees_output):
        if section.get("branch") == "refs/heads/aurora/v2":
            aurora_branch_section = section
            break

    aurora_local_divergence = None
    aurora_local_status = None
    if aurora_branch_section and aurora_branch_section.get("worktree"):
        aurora_path = Path(aurora_branch_section["worktree"])
        aurora_local_divergence = run_command(
            "Aurora Local vs Origin Divergence",
            ["git", "-C", str(aurora_path), "rev-list", "--left-right", "--count", "origin/aurora/v2...aurora/v2"],
            repo_root,
        )
        aurora_local_status = run_command(
            "Aurora Local Status",
            ["git", "-C", str(aurora_path), "status", "--short", "--branch"],
            repo_root,
        )

    if isinstance(issues_json, list):
        label_counts = build_label_counts(issues_json)
        label_lines = [f"- `{key}`: `{count}`" for key, count in label_counts.items()]
    else:
        label_lines = ["- Issue label counts: `unavailable` (open issue JSON query failed)"]
    draft_queue_summary = (
        f"future posts `{queue_counts['future_posts']}`, "
        f"draft posts `{queue_counts['draft_posts']}`, "
        f"draft pages `{queue_counts['draft_pages']}`"
        if queue_counts
        else "`unavailable` (see Draft Queue Counts stderr)"
    )

    smoke = summarize_smoke(smoke_json)
    if smoke["available"]:
        observed_wp_version = smoke["observed_version"] or "(unknown)"
    else:
        observed_wp_version = "unavailable"

    projects_status = parse_status_line(projects_headers.stdout)
    work_og_image = parse_og_image(work_page_html.stdout)
    has_reveal_safety_net = "Aurora reveal safety net" in home_page_html.stdout
    gsap_from_cdn = "cdn.jsdelivr.net/npm/gsap" in home_page_html.stdout

    lines: list[str] = [
        f"# Morning Truth Report - {now.strftime('%Y-%m-%d %H:%M:%S UTC')}",
        "",
        "Scope: Track A (`main`) read-only verification and repo-state stabilization.",
        "",
        "## Snapshot Summary",
        "",
        f"- Open PRs: `{format_json_count(prs_json)}`",
        f"- Open issues: `{format_json_count(issues_json)}`",
        f"- WordPress version (smoke): `{observed_wp_version}`",
        f"- Draft queue: {draft_queue_summary}",
        f"- `/projects/` status: `{projects_status}`",
        f"- `/recent-projects-include/` og:image: `{work_og_image}`",
        f"- Homepage reveal safety net detected: `{'yes' if has_reveal_safety_net else 'no'}`",
        f"- GSAP/ScrollTrigger CDN detected: `{'yes' if gsap_from_cdn else 'no'}`",
        "",
        "## Issue Label Signals",
        "",
        *label_lines,
        "",
        "## Drift Check",
        "",
    ]

    if drift_json and drift_json.get("checks"):
        lines.extend(
            [
                "| Signal | Declared | Observed | Drift |",
                "|---|---:|---:|---|",
            ]
        )
        for check in drift_json["checks"]:
            declared = check.get("declared")
            observed = check.get("observed")
            if not check.get("evaluated", True):
                drift = "not evaluated"
            else:
                drift = "YES" if check.get("drift") else "no"
            lines.append(
                f"| {check.get('label')} | {declared if declared is not None else '(missing)'} | "
                f"{observed if observed is not None else 'unavailable'} | {drift} |"
            )
        if drift_json.get("errors"):
            lines.extend(["", "Drift checker errors:"])
            for error in drift_json["errors"]:
                lines.append(f"- {error}")
    else:
        lines.append("- Drift report unavailable (command/parsing failure).")

    if smoke["available"]:
        smoke_lines = [
            f"- Failures: `{smoke['failures']}`",
            f"- Warnings: `{smoke['warnings']}`",
        ]
    else:
        smoke_lines = [
            "- Result: `unavailable` (public smoke output missing or unparsable; treat as degraded, not passing)",
        ]

    truth_errors = collect_truth_errors(prs_json, issues_json, queue_error, smoke["available"], drift_json)
    if truth_errors:
        availability_lines = [f"- `unavailable`: {error}" for error in truth_errors]
    else:
        availability_lines = ["- All startup truth data sources resolved."]

    lines.extend(
        [
            "",
            "## WP Smoke Summary",
            "",
            *smoke_lines,
            "",
            "## Data Availability",
            "",
            *availability_lines,
            "",
            "## Aurora Risk (Read-Only)",
            "",
        ]
    )

    if aurora_local_divergence:
        lines.append(
            f"- Local `aurora/v2` vs `origin/aurora/v2`: `{aurora_local_divergence.stdout or '(no output)'}`"
        )
    else:
        lines.append("- Local `aurora/v2` worktree not detected from porcelain list.")
    if aurora_local_status:
        lines.append(f"- Local `aurora/v2` status: `{aurora_local_status.stdout or '(clean/no output)'}`")

    lines.extend(["", "## Startup Command Outputs", ""])
    for result in startup_results:
        lines.append(render_command_block(result))
        lines.append("")

    lines.extend(["## Supporting Command Outputs", ""])
    for result in (
        issues_json_result,
        prs_json_result,
        draft_result,
        smoke_result,
        drift_result,
        projects_headers,
    ):
        lines.append(render_command_block(result))
        lines.append("")
    if aurora_local_divergence:
        lines.append(render_command_block(aurora_local_divergence))
        lines.append("")
    if aurora_local_status:
        lines.append(render_command_block(aurora_local_status))
        lines.append("")

    report = "\n".join(lines).rstrip() + "\n"
    if args.stdout:
        print(report, end="")
    else:
        out_path.write_text(report, encoding="utf-8")
        print(out_path)
    if args.fail_on_error and truth_errors:
        print(
            f"morning-truth: {len(truth_errors)} data source(s) unavailable (--fail-on-error)",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
