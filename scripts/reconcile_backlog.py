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
2. Merged remote branches not yet pruned, including squash-merged heads whose
   tip SHA exactly matches a merged PR head (ancestry-only misses those).
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
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import parse_qsl, urlencode

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "docs/current-state/reports"
# "Fixes #12" / "closed #12" — should have auto-closed on merge to default branch
CLOSING_REF = re.compile(r"\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#(\d+)", re.IGNORECASE)
NEGATED_CLOSING_PREFIX = re.compile(
    r"\b(?:(?:do(?:es)?|did|will|would|should|must|can|could|is|are|was|were)\s+not|"
    r"cannot|can't|won't|doesn't|didn't|shouldn't|mustn't|wouldn't|couldn't)"
    r"\s+(?:auto-)?$",
    re.IGNORECASE,
)
# bare "#12" mention — weak signal (epic refs, progress notes)
MENTION_REF = re.compile(r"#(\d+)")
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
NONE_MARK = "- none ✅"
DEFAULT_PER_PAGE = 100
MAX_PAGES = 50

METHOD_ANCESTRY = "ancestry (tip is ancestor of origin/main)"
METHOD_SQUASH = "exact squash-head SHA (same repo, same branch)"
METHOD_POST_MERGE = (
    "post-merge commits (branch name matches merged PR; tip SHA differs)"
)
METHOD_REUSED = "reused branch name or open PR (name alone is not merge proof)"
METHOD_REPO_MISMATCH = "repository mismatch (PR head repo differs from origin)"
METHOD_UNKNOWN = "unknown API or Git state"


@dataclass
class ApiResult:
    """One paginated GitHub REST retrieval."""

    items: list = field(default_factory=list)
    complete: bool = True
    error: str | None = None
    pages: int = 0


@dataclass
class WorktreeState:
    path: str
    head: str = ""
    branch: str = ""
    dirty: bool | None = None


@dataclass
class BranchRecord:
    ref: str
    name: str
    sha: str
    kind: str
    method: str
    pr_number: int | None = None
    pr_head_sha: str | None = None
    pr_head_repo: str | None = None
    cautions: list[str] = field(default_factory=list)


@dataclass
class BranchScan:
    confirmed: list[BranchRecord] = field(default_factory=list)
    post_merge: list[BranchRecord] = field(default_factory=list)
    reused: list[BranchRecord] = field(default_factory=list)
    repo_mismatch: list[BranchRecord] = field(default_factory=list)
    unknown: list[BranchRecord] = field(default_factory=list)
    complete: bool = True
    notes: list[str] = field(default_factory=list)

    def has_rows(self) -> bool:
        return bool(
            self.confirmed
            or self.post_merge
            or self.reused
            or self.repo_mismatch
            or self.unknown
            or self.notes
        )


def parse_repo_slug(url: str) -> str:
    """Return owner/name from an SSH or HTTPS GitHub remote URL."""
    m = re.search(r"[:/]([^/:]+/[^/]+?)(?:\.git)?$", url)
    if not m:
        raise RuntimeError(f"cannot parse repo from remote: {url!r}")
    return m.group(1)


def _git_argv_after_global_flags(argv: list[str]) -> list[str]:
    rest = list(argv[1:])
    while rest:
        if rest[0] == "-C" and len(rest) >= 2:
            rest = rest[2:]
            continue
        if rest[0] == "--git-dir" and len(rest) >= 2:
            rest = rest[2:]
            continue
        break
    return rest


def _is_allowed_git(argv: list[str]) -> bool:
    """Report-only allowlist. fetch --prune refreshes tracking refs; it is not a delete."""
    if not argv or argv[0] != "git":
        return False
    args = _git_argv_after_global_flags(argv)
    if not args:
        return False
    if args[0] == "remote":
        return True
    if args[0] == "fetch":
        return True
    if args[0] == "for-each-ref":
        return True
    if args[0] == "merge-base":
        return True
    if args[0] == "rev-parse":
        return True
    if args[0] == "worktree" and args[1:2] == ["list"]:
        return True
    if args[0] == "status":
        return True
    return False


def _is_allowed_gh(argv: list[str]) -> bool:
    if len(argv) < 2 or argv[0] != "gh":
        return False
    if argv[1:3] == ["issue", "list"]:
        return "close" not in argv and "edit" not in argv and "delete" not in argv
    if argv[1] != "api":
        return False
    if "-X" in argv or "--method" in argv:
        flag = "-X" if "-X" in argv else "--method"
        idx = argv.index(flag)
        method = argv[idx + 1].upper() if idx + 1 < len(argv) else ""
        return method in ("", "GET")
    return True


def _reject_destructive(argv: list[str]) -> None:
    """Refuse mutating git/gh. This script reports only and deletes nothing."""
    if not argv:
        return
    if argv[0] == "git" and not _is_allowed_git(argv):
        raise RuntimeError(f"refusing destructive or unlisted git command: {argv!r}")
    if argv[0] == "gh" and not _is_allowed_gh(argv):
        raise RuntimeError(f"refusing mutating gh command: {argv!r}")


def run_cmd(
    argv: list[str],
    *,
    timeout: int = 30,
    check: bool = False,
) -> subprocess.CompletedProcess:
    """Run a read-only subprocess. Tests patch this to inspect every call."""
    _reject_destructive(argv)
    return subprocess.run(
        argv,
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=check,
    )


def repo_slug() -> str:
    """owner/name from the git origin remote (no API call, no rate limit)."""
    url = run_cmd(["git", "remote", "get-url", "origin"], timeout=15).stdout.strip()
    return parse_repo_slug(url)


def _with_page(path: str, page: int, per_page: int) -> str:
    if "?" in path:
        base, qs = path.split("?", 1)
    else:
        base, qs = path, ""
    params = dict(parse_qsl(qs, keep_blank_values=True))
    params["page"] = str(page)
    params["per_page"] = str(per_page)
    return f"{base}?{urlencode(params)}"


def _path_per_page(path: str) -> int:
    if "?" not in path:
        return DEFAULT_PER_PAGE
    params = dict(parse_qsl(path.split("?", 1)[1], keep_blank_values=True))
    raw = params.get("per_page")
    if not raw:
        return DEFAULT_PER_PAGE
    try:
        value = int(raw)
    except ValueError:
        return DEFAULT_PER_PAGE
    return max(1, min(value, DEFAULT_PER_PAGE))


def gh_api(path: str, *, per_page: int | None = None) -> ApiResult:
    """Call the GitHub REST API via `gh api`, following pages until a short page.

    A full-sized last page without a successful follow-up request is incomplete.
    API errors after a partial retrieval stay incomplete; they never become [].
    """
    page_size = per_page if per_page is not None else _path_per_page(path)
    items: list = []
    page = 1
    while page <= MAX_PAGES:
        page_path = _with_page(path, page, page_size)
        try:
            proc = run_cmd(["gh", "api", page_path], timeout=90, check=True)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            detail = getattr(e, "stderr", "") or str(e)
            print(f"  ! gh api {page_path} failed: {detail}", file=sys.stderr)
            return ApiResult(
                items=items,
                complete=False,
                error=f"gh api {page_path} failed: {e}",
                pages=page - 1,
            )
        try:
            data = json.loads(proc.stdout) if proc.stdout.strip() else []
        except json.JSONDecodeError as e:
            print(f"  ! gh api {page_path} failed: {e}", file=sys.stderr)
            return ApiResult(
                items=items,
                complete=False,
                error=f"gh api {page_path} returned invalid JSON: {e}",
                pages=page - 1,
            )
        if isinstance(data, dict):
            data = [data]
        if not isinstance(data, list):
            return ApiResult(
                items=items,
                complete=False,
                error=f"gh api {page_path} returned a non-list payload",
                pages=page - 1,
            )
        items.extend(data)
        if len(data) < page_size:
            return ApiResult(items=items, complete=True, pages=page)
        page += 1
    return ApiResult(
        items=items,
        complete=False,
        error=f"gh api {path} stopped at {MAX_PAGES} pages (incomplete)",
        pages=MAX_PAGES,
    )


def _normalize_pr(raw: dict) -> dict:
    head = raw.get("head") or {}
    repo = head.get("repo") or {}
    return {
        "number": raw.get("number"),
        "title": raw.get("title", "") or "",
        "body": raw.get("body", "") or "",
        "headRefName": head.get("ref", "") or "",
        "headSha": (head.get("sha") or "").lower(),
        "headRepo": repo.get("full_name") or "",
        "mergedAt": raw.get("merged_at") or "",
        "state": raw.get("state") or "",
    }


def list_pulls() -> ApiResult:
    """All open and closed PRs, mapped to the report shape. Paginated."""
    repo = repo_slug()
    raw = gh_api(f"repos/{repo}/pulls?state=all&sort=updated&direction=desc")
    mapped = [_normalize_pr(p) for p in raw.items if isinstance(p, dict)]
    return ApiResult(
        items=mapped,
        complete=raw.complete,
        error=raw.error,
        pages=raw.pages,
    )


OPEN_ISSUES_GQL = (
    "query($owner: String!, $name: String!, $cursor: String) {"
    " repository(owner: $owner, name: $name) {"
    "  issues(states: OPEN, first: 100, after: $cursor) {"
    "   totalCount pageInfo { hasNextPage endCursor }"
    "   nodes { number title updatedAt createdAt labels(first: 50) { nodes { name } } }"
    "  }"
    " }"
    "}"
)
ISSUE_LIST_LIMIT = 200
REST_PR_ONLY_ERROR = (
    "REST /issues returned only pull requests with no further pages; "
    "that is not a proven empty issue list (PRs share the issues API)"
)


def _issue_record(number, title, labels, updated, created) -> dict:
    return {
        "number": number,
        "title": title or "",
        "labels": labels or [],
        "updatedAt": updated or "",
        "createdAt": created or "",
    }


def _issue_from_rest(raw: dict) -> dict:
    return _issue_record(
        raw.get("number"),
        raw.get("title", ""),
        raw.get("labels", []),
        raw.get("updated_at", ""),
        raw.get("created_at", ""),
    )


def _issue_from_graphql(node: dict) -> dict:
    labels = [
        {"name": lab.get("name", "")}
        for lab in ((node.get("labels") or {}).get("nodes") or [])
        if isinstance(lab, dict)
    ]
    return _issue_record(
        node.get("number"),
        node.get("title", ""),
        labels,
        node.get("updatedAt", ""),
        node.get("createdAt", ""),
    )


def _open_issues_graphql(repo: str) -> ApiResult:
    """GraphQL repository.issues — REST /issues can be installation-filtered and PR-only."""
    if "/" not in repo:
        return ApiResult(complete=False, error=f"cannot parse owner/name from {repo!r}")
    owner, name = repo.split("/", 1)
    items: list[dict] = []
    cursor = None
    total = None
    pages = 0
    while pages < MAX_PAGES:
        argv = [
            "gh", "api", "graphql",
            "-f", f"query={OPEN_ISSUES_GQL}",
            "-F", f"owner={owner}",
            "-F", f"name={name}",
        ]
        if cursor:
            argv.extend(["-F", f"cursor={cursor}"])
        try:
            proc = run_cmd(argv, timeout=90, check=True)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            return ApiResult(
                items=items,
                complete=False,
                error=f"gh api graphql issues failed: {e}",
                pages=pages,
            )
        try:
            payload = json.loads(proc.stdout) if proc.stdout.strip() else {}
        except json.JSONDecodeError as e:
            return ApiResult(
                items=items,
                complete=False,
                error=f"gh api graphql issues returned invalid JSON: {e}",
                pages=pages,
            )
        if not isinstance(payload, dict):
            return ApiResult(
                items=items,
                complete=False,
                error="gh api graphql issues returned a non-object payload",
                pages=pages,
            )
        if payload.get("errors"):
            return ApiResult(
                items=items,
                complete=False,
                error=f"gh api graphql issues errors: {payload['errors']}",
                pages=pages,
            )
        conn = ((payload.get("data") or {}).get("repository") or {}).get("issues")
        if not isinstance(conn, dict):
            return ApiResult(
                items=items,
                complete=False,
                error="gh api graphql issues: repository.issues missing",
                pages=pages,
            )
        pages += 1
        total = conn.get("totalCount")
        for node in conn.get("nodes") or []:
            if isinstance(node, dict):
                items.append(_issue_from_graphql(node))
        page_info = conn.get("pageInfo") or {}
        if not page_info.get("hasNextPage"):
            if isinstance(total, int) and len(items) != total:
                return ApiResult(
                    items=items,
                    complete=False,
                    error=f"GraphQL issues totalCount={total} but retrieved {len(items)}",
                    pages=pages,
                )
            return ApiResult(items=items, complete=True, pages=pages)
        cursor = page_info.get("endCursor")
        if not cursor:
            return ApiResult(
                items=items,
                complete=False,
                error="GraphQL issues hasNextPage without endCursor",
                pages=pages,
            )
    return ApiResult(
        items=items,
        complete=False,
        error=f"GraphQL issues stopped at {MAX_PAGES} pages (incomplete)",
        pages=pages,
    )


def _open_issues_cli() -> ApiResult:
    """Same catalog `gh issue list` uses. Limit hit means we did not prove completeness."""
    argv = [
        "gh", "issue", "list",
        "--state", "open",
        "--limit", str(ISSUE_LIST_LIMIT),
        "--json", "number,title,labels,updatedAt,createdAt",
    ]
    try:
        proc = run_cmd(argv, timeout=90, check=True)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        return ApiResult(complete=False, error=f"gh issue list failed: {e}")
    try:
        raw = json.loads(proc.stdout) if proc.stdout.strip() else []
    except json.JSONDecodeError as e:
        return ApiResult(complete=False, error=f"gh issue list returned invalid JSON: {e}")
    if not isinstance(raw, list):
        return ApiResult(complete=False, error="gh issue list returned a non-list payload")
    items = [
        _issue_record(
            row.get("number"),
            row.get("title", ""),
            row.get("labels", []),
            row.get("updatedAt", ""),
            row.get("createdAt", ""),
        )
        for row in raw
        if isinstance(row, dict)
    ]
    if len(items) >= ISSUE_LIST_LIMIT:
        return ApiResult(
            items=items,
            complete=False,
            error=f"gh issue list hit --limit {ISSUE_LIST_LIMIT}",
            pages=1,
        )
    return ApiResult(items=items, complete=True, pages=1)


def _open_issues_rest(repo: str) -> ApiResult:
    raw = gh_api(f"repos/{repo}/issues?state=open")
    mapped = [
        _issue_from_rest(i)
        for i in raw.items
        if isinstance(i, dict) and not i.get("pull_request")
    ]
    pr_only = bool(raw.items) and all(
        isinstance(i, dict) and i.get("pull_request") for i in raw.items
    )
    if pr_only:
        return ApiResult(
            items=mapped,
            complete=False,
            error=REST_PR_ONLY_ERROR,
            pages=raw.pages,
        )
    return ApiResult(
        items=mapped,
        complete=raw.complete,
        error=raw.error,
        pages=raw.pages,
    )


def open_issues() -> tuple[list[dict], ApiResult]:
    """Open issues, excluding PRs. Prefer GraphQL; never treat a PR-only REST page as none."""
    repo = repo_slug()
    gql = _open_issues_graphql(repo)
    if gql.complete:
        return list(gql.items), gql
    listed = _open_issues_cli()
    if listed.complete:
        return list(listed.items), listed
    rest = _open_issues_rest(repo)
    if rest.complete:
        return list(rest.items), rest
    items = gql.items or listed.items or rest.items
    error = "; ".join(part for part in (gql.error, listed.error, rest.error) if part)
    return list(items), ApiResult(
        items=list(items),
        complete=False,
        error=error or "open-issue retrieval did not finish",
        pages=max(gql.pages, listed.pages, rest.pages),
    )


def merged_prs(limit: int | None = None) -> list[dict]:
    """Merged PRs for issue-reference scanning. Prefer list_pulls() in build_report."""
    raw = list_pulls()
    out = [p for p in raw.items if p.get("mergedAt")]
    if limit is not None:
        return out[:limit]
    return out


def _full_sha(value: str) -> str | None:
    sha = (value or "").strip().lower()
    return sha if FULL_SHA.match(sha) else None


def _parse_worktree_porcelain(text: str) -> list[WorktreeState]:
    blocks = []
    current: dict[str, str] = {}
    for line in text.splitlines():
        if line == "":
            if current.get("path"):
                blocks.append(
                    WorktreeState(
                        path=current.get("path", ""),
                        head=(current.get("head") or "").lower(),
                        branch=current.get("branch", ""),
                    )
                )
            current = {}
            continue
        if line.startswith("worktree "):
            current["path"] = line[len("worktree "):]
        elif line.startswith("HEAD "):
            current["head"] = line[len("HEAD "):]
        elif line.startswith("branch "):
            ref = line[len("branch "):]
            current["branch"] = ref.removeprefix("refs/heads/")
    if current.get("path"):
        blocks.append(
            WorktreeState(
                path=current.get("path", ""),
                head=(current.get("head") or "").lower(),
                branch=current.get("branch", ""),
            )
        )
    return blocks


def list_worktree_states() -> tuple[list[WorktreeState], bool, str | None]:
    try:
        proc = run_cmd(["git", "worktree", "list", "--porcelain"], timeout=30, check=True)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        return [], False, f"git worktree list failed: {e}"
    trees = _parse_worktree_porcelain(proc.stdout)
    complete = True
    error = None
    for tree in trees:
        try:
            status = run_cmd(
                ["git", "-C", tree.path, "status", "--porcelain"],
                timeout=30,
                check=True,
            )
            tree.dirty = bool(status.stdout.strip())
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            tree.dirty = None
            complete = False
            error = f"git status failed for worktree {tree.path}: {e}"
    return trees, complete, error


def worktree_cautions(
    name: str,
    sha: str,
    trees: list[WorktreeState],
    trees_complete: bool,
    trees_error: str | None,
) -> list[str]:
    cautions: list[str] = []
    if not trees_complete and trees_error and not trees:
        cautions.append(f"worktree state unavailable ({trees_error})")
        return cautions
    tip = _full_sha(sha)
    for tree in trees:
        occupied = tree.branch == name or (tip and tree.head == tip)
        if not occupied:
            continue
        cautions.append(f"checked out at {tree.path}")
        if tree.dirty is True:
            cautions.append(f"dirty work at {tree.path}")
        elif tree.dirty is None:
            cautions.append(f"worktree state unavailable at {tree.path}")
    if not trees_complete and trees_error and not any("unavailable" in c for c in cautions):
        cautions.append(f"worktree state unavailable ({trees_error})")
    return cautions


def _is_ancestor(ref: str) -> tuple[bool | None, str | None]:
    """True/False when merge-base answers; None when git state is unknown."""
    try:
        proc = run_cmd(["git", "merge-base", "--is-ancestor", ref, "origin/main"], timeout=30)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        return None, f"git merge-base --is-ancestor {ref} origin/main failed: {e}"
    if proc.returncode == 0:
        return True, None
    if proc.returncode == 1:
        return False, None
    detail = (proc.stderr or proc.stdout or "").strip() or f"exit {proc.returncode}"
    return None, f"git merge-base --is-ancestor {ref} origin/main failed: {detail}"


def _prs_for_branch(name: str, pulls: list[dict]) -> tuple[list[dict], list[dict]]:
    merged, opened = [], []
    for pr in pulls:
        if (pr.get("headRefName") or "") != name:
            continue
        if pr.get("mergedAt"):
            merged.append(pr)
        if pr.get("state") == "open":
            opened.append(pr)
    return merged, opened


def _same_repo(pr: dict, origin: str) -> bool | None:
    head_repo = pr.get("headRepo") or ""
    if not head_repo:
        return None
    return head_repo == origin


def _exact_sha_matches(merged: list[dict], sha: str, origin: str) -> list[dict]:
    tip = _full_sha(sha)
    if not tip:
        return []
    out = []
    for pr in merged:
        if _full_sha(pr.get("headSha", "") or "") != tip:
            continue
        if _same_repo(pr, origin) is True:
            out.append(pr)
    return out


def _repo_mismatches(merged: list[dict], sha: str, origin: str) -> list[dict]:
    tip = _full_sha(sha)
    if not tip:
        return []
    out = []
    for pr in merged:
        if _full_sha(pr.get("headSha", "") or "") != tip:
            continue
        if _same_repo(pr, origin) is False:
            out.append(pr)
    return out


def _pick_pr(candidates: list[dict]) -> dict | None:
    if not candidates:
        return None
    return sorted(candidates, key=lambda p: p.get("number") or 0)[-1]


def _record(
    ref: str,
    name: str,
    sha: str,
    kind: str,
    method: str,
    pr: dict | None,
    cautions: list[str],
) -> BranchRecord:
    return BranchRecord(
        ref=ref,
        name=name,
        sha=sha,
        kind=kind,
        method=method,
        pr_number=(pr or {}).get("number"),
        pr_head_sha=_full_sha((pr or {}).get("headSha", "") or "") or (pr or {}).get("headSha") or None,
        pr_head_repo=(pr or {}).get("headRepo") or None,
        cautions=cautions,
    )


def _refresh_remote_refs() -> tuple[bool, str | None]:
    try:
        run_cmd(["git", "fetch", "origin", "--prune"], timeout=60, check=True)
        return True, None
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        return False, f"git fetch origin --prune failed: {e}"


def _remote_branch_tips() -> tuple[list[tuple[str, str]], bool, str | None]:
    try:
        proc = run_cmd(
            ["git", "for-each-ref", "--format=%(refname:short) %(objectname)", "refs/remotes/origin/"],
            timeout=30,
            check=True,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        return [], False, f"git for-each-ref failed: {e}"
    out = []
    for line in proc.stdout.splitlines():
        parts = line.split()
        if len(parts) != 2:
            continue
        ref, sha = parts
        if ref in ("origin", "origin/HEAD", "origin/main"):
            continue
        out.append((ref, sha.lower()))
    return out, True, None


def classify_remote_branch(
    ref: str,
    sha: str,
    origin: str,
    pulls: list[dict],
    pulls_complete: bool,
    cautions: list[str],
) -> BranchRecord | None:
    """Classify one remote-tracking branch. Name alone is never merge proof."""
    name = ref.removeprefix("origin/")
    merged, opened = _prs_for_branch(name, pulls)
    ancestor, ancestor_error = _is_ancestor(ref)
    exact = _exact_sha_matches(merged, sha, origin)
    mismatched = _repo_mismatches(merged, sha, origin)
    missing_repo_exact = []
    tip = _full_sha(sha)
    if tip:
        for pr in merged:
            if _full_sha(pr.get("headSha", "") or "") == tip and _same_repo(pr, origin) is None:
                missing_repo_exact.append(pr)

    if ancestor is None:
        return _record(ref, name, sha, "unknown", METHOD_UNKNOWN, _pick_pr(merged or opened), cautions)

    methods = []
    if ancestor:
        methods.append(METHOD_ANCESTRY)
    if exact:
        methods.append(METHOD_SQUASH)
    if methods:
        pr = _pick_pr(exact) or _pick_pr(merged)
        if opened:
            for pr_open in opened:
                cautions.append(
                    f"open PR #{pr_open.get('number')} shares this branch name (reused name)"
                )
        return _record(ref, name, sha, "confirmed", "; ".join(methods), pr, cautions)

    if mismatched:
        return _record(ref, name, sha, "repo-mismatch", METHOD_REPO_MISMATCH, _pick_pr(mismatched), cautions)

    if missing_repo_exact:
        extra = list(cautions)
        extra.append("PR head repository identity is missing; SHA match is not proof")
        return _record(ref, name, sha, "unknown", METHOD_UNKNOWN, _pick_pr(missing_repo_exact), extra)

    if opened and merged:
        return _record(ref, name, sha, "reused", METHOD_REUSED, _pick_pr(opened), cautions)

    if opened and not pulls_complete:
        return _record(ref, name, sha, "unknown", METHOD_UNKNOWN, _pick_pr(opened), cautions)

    if merged:
        return _record(ref, name, sha, "post-merge", METHOD_POST_MERGE, _pick_pr(merged), cautions)

    if not pulls_complete:
        extra = list(cautions)
        extra.append("PR list incomplete; cannot rule out a squash-head match")
        return _record(ref, name, sha, "unknown", METHOD_UNKNOWN, None, extra)
    return None


def merged_unpruned_branches(
    pulls: list[dict] | None = None,
    pulls_complete: bool = True,
    pulls_error: str | None = None,
) -> BranchScan:
    """Remote branches whose tip is merged — ancestry and/or exact squash-head SHA."""
    scan = BranchScan()
    origin = repo_slug()
    fetched, fetch_error = _refresh_remote_refs()
    if not fetched:
        scan.complete = False
        scan.notes.append(fetch_error or "git fetch failed")

    if pulls is None:
        raw = list_pulls()
        pulls = raw.items
        pulls_complete = raw.complete
        pulls_error = raw.error

    if not pulls_complete:
        scan.complete = False
        scan.notes.append(pulls_error or "GitHub pulls retrieval is incomplete")

    refs, refs_complete, refs_error = _remote_branch_tips()
    if not refs_complete:
        scan.complete = False
        scan.notes.append(refs_error or "git for-each-ref failed")
        if not refs:
            return scan

    trees, trees_complete, trees_error = list_worktree_states()
    if not trees_complete:
        scan.complete = False
        if trees_error:
            scan.notes.append(trees_error)

    for ref, sha in refs:
        cautions = worktree_cautions(ref.removeprefix("origin/"), sha, trees, trees_complete, trees_error)
        record = classify_remote_branch(
            ref, sha, origin, pulls, pulls_complete, cautions
        )
        if record is None:
            continue
        if record.kind == "confirmed":
            scan.confirmed.append(record)
        elif record.kind == "post-merge":
            scan.post_merge.append(record)
        elif record.kind == "reused":
            scan.reused.append(record)
        elif record.kind == "repo-mismatch":
            scan.repo_mismatch.append(record)
        else:
            scan.unknown.append(record)
    return scan


def closing_refs(text: str) -> set[int]:
    """Return affirmative closing references, excluding explicit negations."""
    refs = set()
    for match in CLOSING_REF.finditer(text):
        prefix = re.sub(r"[*_`~]", "", text[max(0, match.start() - 64) : match.start()])
        if NEGATED_CLOSING_PREFIX.search(prefix):
            continue
        refs.add(int(match.group(1)))
    return refs


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
        closes = closing_refs(text)
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
        labels = {label["name"] for label in i.get("labels", [])}
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


def _format_branch_record(rec: BranchRecord) -> list[str]:
    lines = [f"- [ ] `{rec.ref}` @ `{rec.sha}`"]
    if rec.pr_number:
        head = rec.pr_head_sha or "unknown"
        repo = f" from `{rec.pr_head_repo}`" if rec.pr_head_repo else ""
        lines.append(f"  - PR #{rec.pr_number} head `{head}`{repo}")
    else:
        lines.append("  - PR: none found")
    lines.append(f"  - matched via {rec.method}")
    for caution in rec.cautions:
        lines.append(f"  - caution: {caution}")
    return lines


def _append_bucket(lines: list[str], title: str, rows: list[BranchRecord]) -> None:
    if not rows:
        return
    lines.append(f"### {title}")
    for rec in rows:
        lines.extend(_format_branch_record(rec))
    lines.append("")


def _section_or_incomplete(
    lines: list[str],
    rows: list,
    *,
    complete: bool,
    incomplete_line: str,
    render,
) -> None:
    if not complete:
        lines.append(f"- [ ] incomplete: {incomplete_line}")
        if rows:
            for row in rows:
                render(row)
    elif rows:
        for row in rows:
            render(row)
    else:
        lines.append(NONE_MARK)


def build_report(stale_days: int) -> str:
    issues, issues_result = open_issues()
    by_num = {i["number"]: i for i in issues}
    pulls_result = list_pulls()
    pulls = pulls_result.items
    merged = [p for p in pulls if p.get("mergedAt")]
    closing, mention = issues_referenced_by_merged_prs(issues, merged)
    scan = merged_unpruned_branches(
        pulls=pulls,
        pulls_complete=pulls_result.complete,
        pulls_error=pulls_result.error,
    )
    stale = stale_wishlist(issues, stale_days)

    def _prs(refs):
        return ", ".join(f"#{p} ({w})" for p, w in sorted(set(refs)))

    scanned = f"{len(merged)}"
    if not pulls_result.complete:
        scanned += " (incomplete)"

    lines = ["# Backlog reconcile (report-only)", "",
             f"- open issues: **{len(issues)}**"
             + ("" if issues_result.complete else " (incomplete)"),
             f"- merged PRs scanned: {scanned}", ""]

    lines.append("## 1. Open issues a merged PR said it would CLOSE (high precision — auto-close missed)")
    def _closing_line(num):
        lines.append(f"- [ ] #{num} — {by_num[num]['title']}  _(closing PR(s): {_prs(closing[num])})_")
    _section_or_incomplete(
        lines,
        list(sorted(closing)),
        complete=issues_result.complete and pulls_result.complete,
        incomplete_line=issues_result.error or pulls_result.error or "issue or PR retrieval did not finish",
        render=_closing_line,
    )
    lines.append("")

    lines.append("## 2. Open issues merely MENTIONED by a merged PR (weak — verify, may be epic/progress refs)")
    def _mention_line(num):
        lines.append(f"- [ ] #{num} — {by_num[num]['title']}  _(PR(s): {_prs(mention[num])})_")
    _section_or_incomplete(
        lines,
        list(sorted(mention)),
        complete=issues_result.complete and pulls_result.complete,
        incomplete_line=issues_result.error or pulls_result.error or "issue or PR retrieval did not finish",
        render=_mention_line,
    )
    lines.append("")

    lines.append("## 3. Merged remote branches not pruned")
    lines.append("")
    lines.append(
        "Report-only. Matches are evidence, not permission to delete branches or worktrees."
    )
    lines.append("")
    if not scan.complete or scan.notes or scan.unknown:
        lines.append("### Incomplete / unknown API or Git state")
        for note in scan.notes:
            lines.append(f"- [ ] {note}")
        for rec in scan.unknown:
            lines.extend(_format_branch_record(rec))
        if not scan.notes and not scan.unknown:
            lines.append("- [ ] retrieval incomplete; do not treat this section as empty-success")
        lines.append("")
    _append_bucket(lines, "Confirmed matches", scan.confirmed)
    _append_bucket(lines, "Post-merge commits", scan.post_merge)
    _append_bucket(lines, "Reused branch names or open PRs", scan.reused)
    _append_bucket(lines, "Repository mismatches", scan.repo_mismatch)
    if scan.complete and not scan.has_rows():
        lines.append(NONE_MARK)
        lines.append("")

    lines.append(f"## 4. Stale `enhancement` issues (no activity > {stale_days}d)")
    def _stale_line(row):
        num, title, when = row
        lines.append(f"- [ ] #{num} — {title}  _(last activity {when})_")
    _section_or_incomplete(
        lines,
        stale,
        complete=issues_result.complete,
        incomplete_line=issues_result.error or "open-issue retrieval did not finish",
        render=_stale_line,
    )
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
