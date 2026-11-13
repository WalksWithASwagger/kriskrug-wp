#!/usr/bin/env python3
"""Print merged pull requests grouped by area, ready to paste into CHANGELOG.md.

Usage:
    python3 scripts/changelog_from_prs.py --since 2026-09-29 [--until 2026-11-12]
    gh pr list --state merged --json number,title,mergedAt,files ... | \
        python3 scripts/changelog_from_prs.py --stdin

Area comes from the title prefix when it names one, otherwise from the changed paths.
Entries are the PR titles with the prefix stripped; nothing else is invented.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter

AREAS = ("Content", "Theme", "Publisher and tooling", "CI and tests", "Docs and ops")

PREFIX_AREA = {
    "content": "Content",
    "events": "Content",
    "events catalog": "Content",
    "seo": "Content",
    "theme": "Theme",
    "ci": "CI and tests",
    "test": "CI and tests",
    "docs": "Docs and ops",
    "ops": "Docs and ops",
}
GENERIC_PREFIXES = {
    "fix",
    "feat",
    "chore",
    "refactor",
    "perf",
    "build",
    "style",
    "revert",
}

PREFIX_RE = re.compile(r"^([A-Za-z][A-Za-z ]*?)(\(([^)]*)\))?:\s+(.*)$")

PATH_RULES = (
    ("fixes/schema-snippets", "Publisher and tooling"),
    ("theme/", "Theme"),
    ("content/", "Content"),
    ("all-in-2026/", "Content"),
    ("scripts/events_page/", "Content"),
    ("docs/", "Docs and ops"),
    ("fixes/", "Docs and ops"),
    ("issues-to-create/", "Docs and ops"),
    ("backup/", "Docs and ops"),
    (".github/", "CI and tests"),
    ("scripts/tests/", "CI and tests"),
    ("package.json", "CI and tests"),
    ("package-lock.json", "CI and tests"),
    ("composer.", "CI and tests"),
    ("requirements", "CI and tests"),
    ("phpcs.", "CI and tests"),
    (".css-budget", "CI and tests"),
    ("scripts/", "Publisher and tooling"),
    ("plugins/", "Publisher and tooling"),
    ("inc/", "Publisher and tooling"),
    ("Makefile", "Publisher and tooling"),
    (".env.schema", "Publisher and tooling"),
)


def split_title(title: str) -> tuple[str | None, str]:
    match = PREFIX_RE.match(title)
    if not match:
        return None, title
    prefix = match.group(1).strip().lower()
    if prefix in PREFIX_AREA or prefix in GENERIC_PREFIXES:
        return prefix, match.group(4)
    return None, title


def area_from_paths(paths: list[str]) -> str:
    votes: Counter[str] = Counter()
    for path in paths:
        for start, area in PATH_RULES:
            if path.startswith(start):
                votes[area] += 1
                break
        else:
            votes["Docs and ops"] += 1
    if not votes:
        return "Docs and ops"
    top = max(votes.values())
    return next(area for area in AREAS if votes[area] == top)


def classify(pr: dict) -> str:
    prefix, _ = split_title(pr["title"])
    if prefix in PREFIX_AREA:
        return PREFIX_AREA[prefix]
    match = PREFIX_RE.match(pr["title"])
    if match and match.group(3) and match.group(3).startswith("deps"):
        return "CI and tests"
    return area_from_paths([f["path"] for f in pr.get("files", [])])


def clean_title(title: str) -> str:
    _, text = split_title(title)
    text = re.sub(r"\s+[—–]\s+", " - ", text)
    text = text.replace("—", "-").replace("–", "-")
    return text[:1].upper() + text[1:]


def group(prs: list[dict]) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = {area: [] for area in AREAS}
    for pr in sorted(prs, key=lambda p: p["mergedAt"], reverse=True):
        grouped[classify(pr)].append(pr)
    return grouped


def render(prs: list[dict]) -> str:
    blocks = []
    for area, items in group(prs).items():
        if not items:
            continue
        lines = [f"### {area}", ""]
        lines += [f"- {clean_title(p['title'])} (#{p['number']})" for p in items]
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks) + "\n"


def in_range(pr: dict, since: str | None, until: str | None) -> bool:
    day = pr["mergedAt"][:10]
    return (since is None or day >= since) and (until is None or day <= until)


def fetch(since: str) -> list[dict]:
    result = subprocess.run(
        [
            "gh",
            "pr",
            "list",
            "--state",
            "merged",
            "--search",
            f"merged:>={since}",
            "--limit",
            "500",
            "--json",
            "number,title,mergedAt,files",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--since", help="first merge date, YYYY-MM-DD (UTC)")
    parser.add_argument("--until", help="last merge date, YYYY-MM-DD (UTC), inclusive")
    parser.add_argument(
        "--stdin", action="store_true", help="read gh pr list JSON from stdin"
    )
    args = parser.parse_args(argv)
    if not args.stdin and not args.since:
        parser.error("--since is required unless --stdin is used")
    prs = json.load(sys.stdin) if args.stdin else fetch(args.since)
    prs = [pr for pr in prs if in_range(pr, args.since, args.until)]
    sys.stdout.write(render(prs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
