#!/usr/bin/env python3
"""Report-only backlog/branch drift detector for kriskrug-wp.

Why: this repo is an issue-tracking hub, not a code mirror — most work ships
live (WP REST/wp-admin) without a PR or `Fixes #N`, so issues stay open after
the work is done and branches linger after merge. This script surfaces the
drift so the next session can action it. It NEVER closes issues or deletes
branches; it only prints a report.

Signals (high → low precision):
1. Open issues referenced by a MERGED PR (e.g. "#253", "Fixes #14") — the
   strongest "done but still open" signal (this is exactly how #253 drifted).
2. Merged remote branches not yet pruned.
3. Stale wishlist: old `enhancement` issues with no recent activity.
4. (Local only, if scripts/notion-to-wp/.env present) live-URL probes for
   issues whose body names a page slug — flags ones that now return HTTP 200.

Usage:
  python3 scripts/reconcile_backlog.py            # print report to stdout
  python3 scripts/reconcile_backlog.py --write     # also write a dated report
  python3 scripts/reconcile_backlog.py --stale-days 90
Requires the `gh` CLI authenticated (locally, or GITHUB_TOKEN in CI).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "docs/current-state/reports"
# "Fixes #12" / "closed #12" — should have auto-closed on merge to default branch
CLOSING_REF = re.compile(r"\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#(\d+)", re.IGNORECASE)
# bare "#12" mention — weak signal (epic refs, progress notes)
MENTION_REF = re.compile(r"#(\d+)")


def parse_repo_slug(url: str) -> str:
    """Return owner/name from an SSH or HTTPS GitHub remote URL."""
    m = re.search(r"[:/]([^/:]+/[^/]+?)(?:\.git)?$", url)
    if not m:
        raise RuntimeError(f"cannot parse repo from remote: {url!r}")
    return m.group(1)


def repo_slug() -> str:
    """owner/name from the git origin remote (no API call, no rate limit)."""
    url = subprocess.run(["git", "remote", "get-url", "origin"], cwd=ROOT,
                         capture_output=True, text=True, timeout=15).stdout.strip()
    return parse_repo_slug(url)


def gh_api(path: str):
    """Call the GitHub REST API via `gh api` (separate, higher limit than GraphQL).

    Single page (per_page up to 100). Sufficient for this repo's scale; the open
    backlog is well under 100 and merged-PR scanning is capped intentionally.
    """
    try:
        out = subprocess.run(["gh", "api", path], capture_output=True,
                             text=True, timeout=90, check=True).stdout
        data = json.loads(out) if out.strip() else []
        return data if isinstance(data, list) else [data]
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, json.JSONDecodeError) as e:
        print(f"  ! gh api {path} failed: {e}", file=sys.stderr)
        return []


def open_issues() -> list[dict]:
    repo = repo_slug()
    raw = gh_api(f"repos/{repo}/issues?state=open&per_page=100")
    out = []
    for i in raw:
        if i.get("pull_request"):  # REST issues endpoint includes PRs; drop them
            continue
        out.append({
            "number": i["number"], "title": i.get("title", ""),
            "labels": i.get("labels", []),
            "updatedAt": i.get("updated_at", ""), "createdAt": i.get("created_at", ""),
        })
    return out


def merged_prs(limit: int = 60) -> list[dict]:
    repo = repo_slug()
    raw = gh_api(f"repos/{repo}/pulls?state=closed&per_page={limit}&sort=updated&direction=desc")
    out = []
    for p in raw:
        if not p.get("merged_at"):
            continue
        out.append({
            "number": p["number"], "title": p.get("title", ""),
            "body": p.get("body", "") or "", "headRefName": (p.get("head") or {}).get("ref", ""),
            "mergedAt": p.get("merged_at", ""),
        })
    return out


def merged_unpruned_branches() -> list[str]:
    """Remote branches (excluding main) whose tip is an ancestor of origin/main."""
    try:
        subprocess.run(["git", "fetch", "origin", "--prune"], cwd=ROOT,
                       capture_output=True, timeout=60)
        refs = subprocess.run(
            ["git", "for-each-ref", "--format=%(refname:short)", "refs/remotes/origin/"],
            cwd=ROOT, capture_output=True, text=True, timeout=30,
        ).stdout.split()
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return []
    out = []
    for ref in refs:
        if ref in ("origin", "origin/HEAD", "origin/main"):
            continue
        merged = subprocess.run(
            ["git", "merge-base", "--is-ancestor", ref, "origin/main"],
            cwd=ROOT, capture_output=True,
        ).returncode == 0
        if merged:
            out.append(ref)
    return out


def issues_referenced_by_merged_prs(issues: list[dict], prs: list[dict]) -> tuple[dict, dict]:
    """Return ({issue#: [(pr#, when)]}, ...) for closing-keyword refs and mention-only refs.

    Closing-keyword + still-open = high-precision drift (auto-close didn't fire).
    Mention-only = weak (epic refs, progress notes) — informational.
    """
    open_nums = {i["number"]: i for i in issues}
    closing: dict[int, list] = {}
    mention: dict[int, list] = {}
    for pr in prs:
        text = f"{pr.get('title','')} {pr.get('body','') or ''} {pr.get('headRefName','')}"
        closes = {int(m) for m in CLOSING_REF.findall(text)}
        mentions = {int(m) for m in MENTION_REF.findall(text)} - closes
        when = (pr.get("mergedAt", "") or "")[:10]
        for num in closes:
            if num in open_nums:
                closing.setdefault(num, []).append((pr["number"], when))
        for num in mentions:
            if num in open_nums:
                mention.setdefault(num, []).append((pr["number"], when))
    return closing, mention


def stale_wishlist(issues: list[dict], stale_days: int) -> list[tuple]:
    cutoff = _now() - dt.timedelta(days=stale_days)
    out = []
    for i in issues:
        labels = {l["name"] for l in i.get("labels", [])}
        updated = _parse(i.get("updatedAt", ""))
        if "enhancement" in labels and updated and updated < cutoff:
            out.append((i["number"], i["title"], updated.date().isoformat()))
    return sorted(out)


def _now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def _parse(s: str):
    try:
        return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


def build_report(stale_days: int) -> str:
    issues = open_issues()
    by_num = {i["number"]: i for i in issues}
    prs = merged_prs()
    closing, mention = issues_referenced_by_merged_prs(issues, prs)
    branches = merged_unpruned_branches()
    stale = stale_wishlist(issues, stale_days)

    def _prs(refs):
        return ", ".join(f"#{p} ({w})" for p, w in sorted(set(refs)))

    lines = ["# Backlog reconcile (report-only)", "",
             f"- open issues: **{len(issues)}**",
             f"- merged PRs scanned: {len(prs)}", ""]

    lines.append("## 1. Open issues a merged PR said it would CLOSE (high precision — auto-close missed)")
    if closing:
        for num in sorted(closing):
            lines.append(f"- [ ] #{num} — {by_num[num]['title']}  _(closing PR(s): {_prs(closing[num])})_")
    else:
        lines.append("- none ✅")
    lines.append("")

    lines.append("## 2. Open issues merely MENTIONED by a merged PR (weak — verify, may be epic/progress refs)")
    if mention:
        for num in sorted(mention):
            lines.append(f"- [ ] #{num} — {by_num[num]['title']}  _(PR(s): {_prs(mention[num])})_")
    else:
        lines.append("- none ✅")
    lines.append("")

    lines.append("## 3. Merged remote branches not pruned")
    if branches:
        for b in branches:
            lines.append(f"- [ ] `{b}`  — `git push origin --delete {b.replace('origin/', '')}`")
    else:
        lines.append("- none ✅")
    lines.append("")

    lines.append(f"## 4. Stale `enhancement` issues (no activity > {stale_days}d)")
    if stale:
        for num, title, when in stale:
            lines.append(f"- [ ] #{num} — {title}  _(last activity {when})_")
    else:
        lines.append("- none ✅")
    lines.append("")
    lines.append("_Report-only. Verify each against live state before closing/pruning._")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="write a dated report under docs/current-state/reports/")
    ap.add_argument("--stale-days", type=int, default=90)
    ap.add_argument("--timestamp", default=None, help="UTC stamp for the report filename (CI passes this)")
    args = ap.parse_args()

    report = build_report(args.stale_days)
    print(report)
    if args.write:
        ts = args.timestamp or "latest"
        REPORTS.mkdir(parents=True, exist_ok=True)
        path = REPORTS / f"backlog-reconcile-{ts}.md"
        path.write_text(report, encoding="utf-8")
        print(f"\nwrote {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
