#!/usr/bin/env python3
"""Scan docs for stale current-state claims.

This check is intentionally non-mutating. It does not prove live truth; it
blocks known-bad claims that have repeatedly confused repo agents.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


DEFAULT_BASES = [
    Path("README.md"),
    Path("AGENTS.md"),
    Path("CONTRIBUTING.md"),
    Path("docs"),
]

DEFAULT_EXCLUDES = [
    Path("docs/current-state/reports"),
    Path("docs/current-state/raw"),
]


@dataclass(frozen=True)
class Finding:
    path: Path
    line_number: int
    message: str
    line: str


KNOWN_STALE_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (
        re.compile(r"/projects/.*(?:still\s+)?returns\s+`?404`?", re.I),
        "`/projects/` no longer documents as 404; verify the 301 redirect with curl.",
    ),
    (
        re.compile(r"Public\s+`/projects/`\s+still\s+returns", re.I),
        "`/projects/` live-state wording is stale; use the current redirect wording.",
    ),
    (
        re.compile(r"(?:Work|Work page).*still\s+emits.*blank", re.I),
        "Work OG blank-image wording is stale; cache-busted readback is currently non-blank.",
    ),
    (
        re.compile(r"blank WordPress\.com OG", re.I),
        "Work OG blank-image wording is stale; cite the current OG readback instead.",
    ),
    (
        re.compile(r"s0\.wp\.com/i/blank\.jpg", re.I),
        "The old WordPress.com blank image should not appear in current guidance.",
    ),
    (
        re.compile(r"Safety-net (?:CSS )?marker (?:is )?present", re.I),
        "Homepage reveal safety-net wording is stale; current readback says the marker is absent.",
    ),
    (
        re.compile(r"Live site is still Catch Responsive", re.I),
        "The live site now runs the Aurora `kk-aurora` theme.",
    ),
    (
        re.compile(r"Current live queue count is 43", re.I),
        "Draft queue count is stale; rerun or cite `make draft-queue-audit`.",
    ),
    (
        re.compile(r"WordPress has `?42`? draft posts", re.I),
        "Draft queue count is stale; current normalized count is 71 draft posts.",
    ),
    (
        re.compile(r"Open issues:\s*`?(?:61|63)`?", re.I),
        "Open issue count is stale; current normalized count is 66 open issues.",
    ),
    (
        re.compile(r"Open issues\s*\|\s*(?:61|63|64)\s*\|", re.I),
        "Open issue table count is stale; current normalized count is 66 open issues.",
    ),
    (
        re.compile(r"Open PRs\s*\|\s*2\s*\|", re.I),
        "Open PR table count is stale; current normalized count is 0 open PRs.",
    ),
    (
        re.compile(r"auto-implement`?\s*(?:issues)?\s*[:|]\s*`?(?:45|47|62)`?", re.I),
        "Historical `auto-implement` count is stale; current normalized count is 44.",
    ),
    (
        re.compile(r"GitHub shows 64 open issues", re.I),
        "Open issue count is stale; current normalized count is 66 open issues.",
    ),
    (
        re.compile(r"Draft posts\s*\|\s*32\s*\|", re.I),
        "Draft-post table count is stale; current normalized count is 71 draft posts.",
    ),
    (
        re.compile(r"Draft pages\s*\|\s*3\s*\|", re.I),
        "Draft-page table count is stale; current normalized count is 5 draft pages.",
    ),
    (
        re.compile(r"authenticated WordPress (?:currently|now) has 32 draft posts", re.I),
        "Draft queue wording is stale; current normalized count is 71 draft posts.",
    ),
]

STALE_FRONT_DOOR_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (
        re.compile(r"WORK-PLAN-2026-05-23\.md.*current (?:execution roadmap|front door)", re.I),
        "`WORK-PLAN-2026-05-23.md` is historical; current guidance must point to handoff + morning-truth.",
    ),
    (
        re.compile(r"current next-session front door", re.I),
        "Avoid undated current-front-door wording; point at the dated handoff and morning-truth report.",
    ),
]

CURRENT_LANGUAGE_PATTERNS = [
    re.compile(r"\bcurrent (?:front door|execution truth|startup context|startup truth)\b", re.I),
    re.compile(r"\blatest startup truth\b", re.I),
]

ANCHOR_PATTERN = re.compile(
    r"2026-\d\d-\d\d|morning-truth|reports/|HANDOFF-2026-05-24|TRACK-A-MORNING-TRUTH|AURORA-V3-QA",
    re.I,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base",
        action="append",
        type=Path,
        help="File or directory to scan. May be repeated. Defaults to root gateway docs plus docs/.",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        type=Path,
        default=[],
        help="File or directory to exclude. May be repeated.",
    )
    return parser.parse_args()


def is_relative_to(path: Path, other: Path) -> bool:
    try:
        path.relative_to(other)
        return True
    except ValueError:
        return False


def iter_markdown_files(repo_root: Path, bases: list[Path], excludes: list[Path]) -> list[Path]:
    files: set[Path] = set()
    exclude_paths = [(repo_root / path).resolve() for path in excludes]

    for base in bases:
        resolved = (repo_root / base).resolve()
        if not resolved.exists():
            continue
        candidates = [resolved] if resolved.is_file() else resolved.rglob("*.md")
        for candidate in candidates:
            if candidate.suffix.lower() != ".md":
                continue
            candidate = candidate.resolve()
            if any(candidate == excluded or is_relative_to(candidate, excluded) for excluded in exclude_paths):
                continue
            files.add(candidate)

    return sorted(files)


def scan_file(repo_root: Path, path: Path) -> list[Finding]:
    findings: list[Finding] = []
    relative_path = path.relative_to(repo_root)
    text = path.read_text(encoding="utf-8")

    for line_number, line in enumerate(text.splitlines(), start=1):
        for pattern, message in KNOWN_STALE_PATTERNS + STALE_FRONT_DOOR_PATTERNS:
            if pattern.search(line):
                findings.append(Finding(relative_path, line_number, message, line.strip()))

        if any(pattern.search(line) for pattern in CURRENT_LANGUAGE_PATTERNS) and not ANCHOR_PATTERN.search(line):
            findings.append(
                Finding(
                    relative_path,
                    line_number,
                    "Current-state wording needs a concrete date, report, or verification-command anchor.",
                    line.strip(),
                )
            )

    return findings


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    bases = args.base if args.base else DEFAULT_BASES
    excludes = DEFAULT_EXCLUDES + args.exclude

    findings: list[Finding] = []
    for path in iter_markdown_files(repo_root, bases, excludes):
        findings.extend(scan_file(repo_root, path))

    if not findings:
        print("docs truth check passed")
        return 0

    print("docs truth check failed:")
    for finding in findings:
        print(f"{finding.path}:{finding.line_number}: {finding.message}")
        print(f"  {finding.line}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
