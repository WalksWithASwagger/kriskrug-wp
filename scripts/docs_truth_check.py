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
    Path(".env.schema"),
    Path(".claude/context/project-context.md"),
    Path(".claude/agents-vibe.md"),
    Path(".github/ISSUE_TEMPLATE/accessibility.yml"),
    Path(".github/ISSUE_TEMPLATE/bug_report.yml"),
    Path(".github/ISSUE_TEMPLATE/content.yml"),
    Path(".github/ISSUE_TEMPLATE/feature_request.yml"),
    Path(".github/ISSUE_TEMPLATE/performance.yml"),
    Path(".github/agent-state/README.md"),
    Path(".github/agents/doc-swarm/README.md"),
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
        re.compile(r"Aurora\s*\**\s*`?1\.5\.0`?\s*\**\s*\(?\s*live\s*==?\s*repo", re.I),
        "Aurora live==repo parity at 1.5.0 is stale; rerun `make status-readonly`, read the public style.css, and name the measured versions.",
    ),
    (
        re.compile(r"Current live queue count is 43", re.I),
        "Draft queue count is stale; rerun or cite `make draft-queue-audit`.",
    ),
    (
        re.compile(r"WordPress has `?42`? draft posts", re.I),
        "Draft queue count is stale; rerun or cite `make draft-queue-audit`.",
    ),
    (
        re.compile(r"Open issues:\s*`?(?:61|69)`?", re.I),
        "Open issue count is stale; rerun or cite `make status-readonly`.",
    ),
    (
        re.compile(r"Open issues\s*\|\s*(?:61|64|69)\s*\|", re.I),
        "Open issue table count is stale; rerun or cite `make status-readonly`.",
    ),
    (
        re.compile(r"Open PRs\s*\|\s*2\s*\|", re.I),
        "Open PR table count is stale; rerun or cite `make status-readonly`.",
    ),
    (
        re.compile(r"auto-implement`?\s*(?:issues)?\s*[:|]\s*`?(?:45|47|62)`?", re.I),
        "Historical `auto-implement` count is stale; query the current label inventory.",
    ),
    (
        re.compile(r"GitHub shows 64 open issues", re.I),
        "Open issue count is stale; rerun or cite `make status-readonly`.",
    ),
    (
        re.compile(r"Draft posts\s*\|\s*32\s*\|", re.I),
        "Draft-post table count is stale; rerun or cite `make draft-queue-audit`.",
    ),
    (
        re.compile(r"Draft pages\s*\|\s*3\s*\|", re.I),
        "Draft-page table count is stale; rerun or cite `make draft-queue-audit`.",
    ),
    (
        re.compile(r"authenticated WordPress (?:currently|now) has 32 draft posts", re.I),
        "Draft queue wording is stale; rerun or cite `make draft-queue-audit`.",
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

ACTIVE_GUIDANCE_PATHS = {
    Path("AGENTS.md"),
    Path("README.md"),
    Path("docs/INDEX.md"),
    Path("docs/current-state/README.md"),
    Path("docs/current-state/CURRENT-STATE-2026-07-30.md"),
    Path("docs/current-state/WORK-PLAN-2026-08-25.md"),
    Path("docs/current-state/MASTER-PLAN-2026-07-30.md"),
}

PERSONAL_SITE_IDENTITY_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (
        re.compile(r"Kris Krug is a grassroots ecosystem initiative", re.I),
        "Agent context must preserve Kris Krug's personal-site identity, not describe him as an organization.",
    ),
    (
        re.compile(r"(?:This is community infrastructure|platform for building BC's inclusive AI future)", re.I),
        "Agent context must preserve kriskrug.co's personal-site identity, not present it as BC + AI infrastructure.",
    ),
]

ISSUE_TEMPLATE_IDENTITY_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (
        re.compile(r"\bkk\.ca\b", re.I),
        "Issue templates must use the canonical kriskrug.co domain.",
    ),
    (
        re.compile(r"BC\s*\+\s*AI(?:'s)?\s+(?:website|mission)", re.I),
        "Issue templates must describe kriskrug.co as Kris Krug's personal site, not a BC + AI property.",
    ),
]

PATH_SCOPED_STALE_PATTERNS: dict[Path, list[tuple[re.Pattern[str], str]]] = {
    Path("README.md"): [
        (
            re.compile(r"(?m)^\s*skills/\s+#"),
            "The repository-local skill path is `.agents/skills/`, not a top-level `skills/` directory.",
        ),
        (
            re.compile(r"(?m)^-\s+Active backlog:.*(?:FIX_QUEUE|SITE-AUDIT)", re.I),
            "The active backlog is the open GitHub issue list; archived audit files are evidence only.",
        ),
    ],
    Path("docs/INDEX.md"): [
        (
            re.compile(r"\[\s*`?\.\./skills/`?\s*\]\(\.\./skills/\)"),
            "The documentation index must link repository-local skills at `../.agents/skills/`.",
        ),
        (
            re.compile(r"WORK-PLAN-2026-08-24\.md.*(?:active|current).*runbook", re.I),
            "The active documentation index must point to `WORK-PLAN-2026-08-25.md`.",
        ),
        (
            re.compile(r"correct the remaining issue #4 media identity", re.I),
            "The audited current-state sequence must record issue #4's mapped media gate as complete.",
        ),
    ],
    Path("docs/current-state/ACCESS_CHANNELS.md"): [
        (
            re.compile(
                r"(?:agent swarm in `.github/` can be triggered|"
                r"71 draft posts|5 draft pages|gitignored local `\.env`)",
                re.I,
            ),
            "The audited current-state access guide must use Varlock, live counts by command, and the retired-swarm status.",
        ),
    ],
    Path("docs/current-state/CURRENT-STATE-2026-07-30.md"): [
        (
            re.compile(r"(?:Latest dated runbook|front door)[^\n]*WORK-PLAN-2026-08-24\.md", re.I),
            "The declared snapshot must point to `WORK-PLAN-2026-08-25.md`.",
        ),
        (
            re.compile(r"Open PRs:\s*`1`[^\n]*#710", re.I),
            "The parked PR #710 counter is stale; rerun `make status-readonly`.",
        ),
        (
            re.compile(r"Three `/private/tmp` worktree registrations were prunable", re.I),
            "The approved #738 cleanup is complete; do not describe its stale registrations as pending.",
        ),
        (
            re.compile(r"WordPress draft queue:[^\n]*`65`\s*draft posts", re.I),
            "The 65-draft snapshot is stale; rerun `make status-readonly`.",
        ),
    ],
    Path("docs/current-state/MASTER-PLAN-2026-07-30.md"): [
        (
            re.compile(r"Day runbook:[^\n]*WORK-PLAN-2026-08-24\.md", re.I),
            "The master plan must point to `WORK-PLAN-2026-08-25.md`.",
        ),
    ],
    Path("docs/current-state/README.md"): [
        (
            re.compile(r"AGENT-MERGE-PATH-2026-07-26\.md[^\n]*Cloud merge / review path", re.I),
            "The deleted agent-safe-merge workflow is historical, not an active merge path.",
        ),
        (
            re.compile(r"two wrong duplicate-media writes and five corrected targets await", re.I),
            "The issue #4 front door predates the partial identity-repair execution; use the current three-target state.",
        ),
    ],
    Path("AGENTS.md"): [
        (
            re.compile(r"PHP is\s+\*\*\d+\.\d+\*\*\s+here", re.I),
            "Do not pin the installed local PHP minor version; tell agents to inspect the runtime.",
        ),
        (
            re.compile(r"repair two wrong duplicate-media writes and five corrected targets", re.I),
            "The issue #4 orientation predates the partial identity-repair execution; use the current three-target state.",
        ),
    ],
    Path(".claude/context/project-context.md"): PERSONAL_SITE_IDENTITY_PATTERNS,
    Path(".claude/agents-vibe.md"): PERSONAL_SITE_IDENTITY_PATTERNS,
    Path(".github/ISSUE_TEMPLATE/accessibility.yml"): ISSUE_TEMPLATE_IDENTITY_PATTERNS,
    Path(".github/ISSUE_TEMPLATE/bug_report.yml"): ISSUE_TEMPLATE_IDENTITY_PATTERNS,
    Path(".github/ISSUE_TEMPLATE/content.yml"): ISSUE_TEMPLATE_IDENTITY_PATTERNS,
    Path(".github/ISSUE_TEMPLATE/feature_request.yml"): ISSUE_TEMPLATE_IDENTITY_PATTERNS,
    Path(".github/ISSUE_TEMPLATE/performance.yml"): ISSUE_TEMPLATE_IDENTITY_PATTERNS,
}

REQUIRED_PATH_PATTERNS: dict[Path, list[tuple[re.Pattern[str], str]]] = {
    Path(".github/agent-state/README.md"): [
        (
            re.compile(r"STATUS:\s*Historical", re.I),
            "Retired swarm documentation must carry a `STATUS: Historical` banner.",
        ),
    ],
    Path(".github/agents/doc-swarm/README.md"): [
        (
            re.compile(r"STATUS:\s*Historical", re.I),
            "Retired swarm documentation must carry a `STATUS: Historical` banner.",
        ),
    ],
}

MERGE_POLICY_GUIDANCE_PATHS = {
    Path("AGENTS.md"),
    Path("CONTRIBUTING.md"),
    Path(".env.schema"),
    Path("docs/current-state/MASTER-PLAN-2026-07-30.md"),
}

STALE_MERGE_POLICY_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (
        re.compile(r"(?:only working path|KK merge)[^\n]*(?:admin override|--admin)", re.I),
        "Merge policy must use the normal protected path, not a routine admin override.",
    ),
    (
        re.compile(r"`?main`?[^\n]*requires?\s+(?:1|one)\s+approving review", re.I),
        "Merge policy contains the retired one-review requirement.",
    ),
    (
        re.compile(
            r"(?:second[- ]account token|not the PR author)[^\n]*(?:merge|approve|unblock|fail)",
            re.I,
        ),
        "Merge policy contains the retired second-account token requirement.",
    ),
    (
        re.compile(r"classic PAT[^\n]*(?:approve|merge)", re.I),
        "Merge policy contains the retired second-account token requirement.",
    ),
    (
        re.compile(
            r"(?:human maintainer[^\n]*(?:reviews?|approves?)|"
            r"maintainers still do human review/approval)",
            re.I,
        ),
        "Merge policy incorrectly makes human approval universal.",
    ),
]

REQUIRED_AGENT_MERGE_POLICY_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (
        re.compile(r"\b0 approving reviews\b", re.I),
        "Merge policy must state that `main` requires 0 approving reviews.",
    ),
    (
        re.compile(r"(?:Test PR / )?summary`?[^\n]*green", re.I),
        "Merge policy must require the green `summary` check.",
    ),
    (
        re.compile(r"up to date with\s+`?main`?", re.I),
        "Merge policy must require the branch to be up to date with `main`.",
    ),
    (
        re.compile(r"gh pr merge <n> --squash --delete-branch", re.I),
        "Merge policy must name the normal protected merge command.",
    ),
    (
        re.compile(r"no\s+`?--admin`?", re.I),
        "Merge policy must forbid routine `--admin` use.",
    ),
    (
        re.compile(r"Theme\s*/\s*plugins[^\n]*inc[^\n]*ask KK before merging", re.I),
        "Merge policy must preserve KK approval for theme, plugin, and `inc/` merges.",
    ),
]

STALE_MORNING_TRUTH_FLOW_PATTERNS: list[re.Pattern[str]] = [
    re.compile(
        r"\bmake\s+morning-truth(?!-checkpoint)\b[^\n]*"
        r"(?:\n\s*(?:[-*]|\d+[.)])?\s*)?(?<!not )\bcommit\b",
        re.I,
    ),
    re.compile(
        r"(?<!not )\bcommit\b[^\n]*\bmake\s+morning-truth(?!-checkpoint)\b",
        re.I,
    ),
]

CURRENT_LANGUAGE_PATTERNS = [
    re.compile(r"\bcurrent (?:front door|execution truth|startup context|startup truth)\b", re.I),
    re.compile(r"\blatest startup truth\b", re.I),
]

ANCHOR_PATTERN = re.compile(
    r"2026-\d\d-\d\d|morning-truth|status-readonly|reports/|HANDOFF-2026-05-24|TRACK-A-MORNING-TRUTH|AURORA-V3-QA",
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
        explicit_file = resolved.is_file()
        candidates = [resolved] if explicit_file else resolved.rglob("*.md")
        for candidate in candidates:
            if not explicit_file and candidate.suffix.lower() != ".md":
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

    for pattern, message in PATH_SCOPED_STALE_PATTERNS.get(relative_path, []):
        for match in pattern.finditer(text):
            findings.append(
                Finding(
                    relative_path,
                    text.count("\n", 0, match.start()) + 1,
                    message,
                    match.group(0).strip(),
                )
            )

    for pattern, message in REQUIRED_PATH_PATTERNS.get(relative_path, []):
        if not pattern.search(text):
            findings.append(Finding(relative_path, 1, message, ""))

    if relative_path in ACTIVE_GUIDANCE_PATHS:
        for pattern in STALE_MORNING_TRUTH_FLOW_PATTERNS:
            for match in pattern.finditer(text):
                findings.append(
                    Finding(
                        relative_path,
                        text.count("\n", 0, match.start()) + 1,
                        "Routine `make morning-truth` output must not be committed; use `make morning-truth-checkpoint` for durable evidence.",
                        match.group(0).replace("\n", " ").strip(),
                    )
                )

    if relative_path in MERGE_POLICY_GUIDANCE_PATHS:
        for pattern, message in STALE_MERGE_POLICY_PATTERNS:
            for match in pattern.finditer(text):
                findings.append(
                    Finding(
                        relative_path,
                        text.count("\n", 0, match.start()) + 1,
                        message,
                        match.group(0).strip(),
                    )
                )

    if relative_path == Path("AGENTS.md"):
        for pattern, message in REQUIRED_AGENT_MERGE_POLICY_PATTERNS:
            if not pattern.search(text):
                findings.append(Finding(relative_path, 1, message, ""))

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
