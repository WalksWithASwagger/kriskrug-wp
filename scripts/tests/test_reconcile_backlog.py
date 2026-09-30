import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import reconcile_backlog as rb  # noqa: E402

REPO = "WalksWithASwagger/kriskrug-wp"
ORIGIN_URL = f"git@github.com:{REPO}.git"
MAIN_SHA = "b" * 40
SQUASH_SHA = "a" * 40
MERGE_SHA = "c" * 40
POST_SHA = "d" * 40
OPEN_SHA = "e" * 40
OTHER_SHA = "f" * 40


def _pr(
    number: int,
    ref: str,
    sha: str,
    *,
    repo: str | None = REPO,
    merged: str | None = None,
    state: str | None = None,
    title: str = "t",
    body: str = "",
) -> dict:
    if merged:
        state = "closed"
    elif state is None:
        state = "open"
    head_repo = None if repo is None else {"full_name": repo}
    return {
        "number": number,
        "title": title,
        "body": body,
        "state": state,
        "merged_at": merged,
        "head": {"ref": ref, "sha": sha, "repo": head_repo},
    }


class FakeWorld:
    """Offline git + GitHub API. Records every argv for destructive-command checks."""

    def __init__(self):
        self.calls: list[list[str]] = []
        self.refs = {"origin/main": MAIN_SHA}
        self.ancestors: set[str] = set()
        self.worktrees = [
            {"path": "/repo", "head": MAIN_SHA, "branch": "main", "dirty": False},
        ]
        self.issue_pages: list[list[dict]] = [[]]
        self.pull_pages: list[list[dict]] = [[]]
        self.issue_error_page = None
        self.pull_error_page = None
        self.graphql_error = False
        self.graphql_nodes: list[dict] = []
        self.graphql_total = 0
        self.issue_list_error = True
        self.issue_list_items: list[dict] = []
        self.fetch_error = False
        self.ref_error = False
        self.ancestor_error_refs: set[str] = set()
        self.worktree_list_error = False
        self.status_error_paths: set[str] = set()

    def run(self, argv, **kwargs):
        self.calls.append(list(argv))
        if argv[:1] == ["git"]:
            return self._git(argv)
        if argv[:3] == ["gh", "api", "graphql"]:
            return self._graphql(argv)
        if argv[:2] == ["gh", "api"]:
            return self._gh(argv)
        if argv[:3] == ["gh", "issue", "list"]:
            return self._issue_list(argv)
        raise AssertionError(f"unexpected command: {argv!r}")

    def _completed(self, stdout="", stderr="", returncode=0):
        return subprocess.CompletedProcess(
            args=[], returncode=returncode, stdout=stdout, stderr=stderr
        )

    def _git(self, argv):
        args = rb._git_argv_after_global_flags(argv)
        if args[:2] == ["remote", "get-url"]:
            return self._completed(ORIGIN_URL + "\n")
        if args[:1] == ["fetch"]:
            if self.fetch_error:
                raise subprocess.CalledProcessError(1, argv, "", "fetch failed")
            return self._completed()
        if args[:1] == ["for-each-ref"]:
            if self.ref_error:
                raise subprocess.CalledProcessError(1, argv, "", "for-each-ref failed")
            lines = [f"{ref} {sha}" for ref, sha in self.refs.items()]
            return self._completed("\n".join(lines) + "\n")
        if args[:2] == ["merge-base", "--is-ancestor"]:
            ref = args[2]
            if ref in self.ancestor_error_refs:
                return self._completed(stderr="not a valid object", returncode=128)
            return self._completed(returncode=0 if ref in self.ancestors else 1)
        if args[:2] == ["worktree", "list"]:
            if self.worktree_list_error:
                raise subprocess.CalledProcessError(1, argv, "", "worktree list failed")
            chunks = []
            for tree in self.worktrees:
                chunks.append(
                    f"worktree {tree['path']}\nHEAD {tree['head']}\n"
                    f"branch refs/heads/{tree['branch']}\n"
                )
            return self._completed("\n".join(chunks) + "\n")
        if args[:1] == ["status"]:
            path = None
            raw = argv[1:]
            if raw[:1] == ["-C"]:
                path = raw[1]
            if path in self.status_error_paths:
                raise subprocess.CalledProcessError(1, argv, "", "status failed")
            dirty = False
            for tree in self.worktrees:
                if tree["path"] == path:
                    dirty = bool(tree.get("dirty"))
            return self._completed(" M file\n" if dirty else "")
        raise AssertionError(f"unhandled git command: {argv!r}")

    def _gh(self, argv):
        path = argv[2]
        parsed = urlparse("https://api.github.example/" + path)
        page = int(parse_qs(parsed.query).get("page", ["1"])[0])
        if "/issues" in parsed.path:
            if self.issue_error_page == page or self.issue_error_page == "all":
                raise subprocess.CalledProcessError(1, argv, "", "issues api failed")
            pages = self.issue_pages
        elif "/pulls" in parsed.path:
            if self.pull_error_page == page or self.pull_error_page == "all":
                raise subprocess.CalledProcessError(1, argv, "", "pulls api failed")
            pages = self.pull_pages
        else:
            raise AssertionError(f"unhandled gh api path: {path!r}")
        payload = pages[page - 1] if page <= len(pages) else []
        return self._completed(json.dumps(payload))

    def _graphql(self, argv):
        if self.graphql_error:
            raise subprocess.CalledProcessError(1, argv, "", "graphql failed")
        nodes = self.graphql_nodes
        total = self.graphql_total if self.graphql_total is not None else len(nodes)
        return self._completed(json.dumps({
            "data": {
                "repository": {
                    "issues": {
                        "totalCount": total,
                        "pageInfo": {"hasNextPage": False, "endCursor": None},
                        "nodes": nodes,
                    }
                }
            }
        }))

    def _issue_list(self, argv):
        if self.issue_list_error:
            raise subprocess.CalledProcessError(1, argv, "", "issue list failed")
        return self._completed(json.dumps(self.issue_list_items))


def _rest_pr(number: int) -> dict:
    return {
        "number": number,
        "title": f"PR {number}",
        "labels": [],
        "updated_at": "2026-09-30T00:00:00Z",
        "created_at": "2026-09-30T00:00:00Z",
        "pull_request": {"url": f"https://api.github.example/pulls/{number}"},
    }


def _gql_issue(number: int, title: str, labels: list[str] | None = None) -> dict:
    return {
        "number": number,
        "title": title,
        "updatedAt": "2026-09-30T00:00:00Z",
        "createdAt": "2026-09-30T00:00:00Z",
        "labels": {"nodes": [{"name": name} for name in (labels or [])]},
    }


def _section(report: str, heading: str) -> str:
    marker = f"## {heading}"
    start = report.index(marker)
    rest = report[start:]
    nxt = rest.find("\n## ", 1)
    return rest if nxt < 0 else rest[:nxt]


def _report(world: FakeWorld) -> str:
    with patch.object(rb, "run_cmd", side_effect=world.run):
        return rb.build_report(stale_days=90)


class RefMatchingTests(unittest.TestCase):
    def setUp(self):
        self.issues = [
            {"number": 14, "title": "Indigenomics CTO", "labels": [], "updatedAt": "2026-01-02T00:00:00Z"},
            {"number": 222, "title": "EPIC hardening", "labels": [], "updatedAt": "2026-06-13T00:00:00Z"},
            {"number": 255, "title": "CI tests", "labels": [], "updatedAt": "2026-06-24T00:00:00Z"},
        ]

    def test_closing_keyword_flags_open_issue(self):
        prs = [{"number": 99, "title": "fix", "body": "Fixes #14", "headRefName": "x", "mergedAt": "2026-06-01T00:00:00Z"}]
        closing, mention = rb.issues_referenced_by_merged_prs(self.issues, prs)
        self.assertIn(14, closing)
        self.assertNotIn(14, mention)

    def test_bare_mention_is_weak_not_closing(self):
        prs = [{"number": 100, "title": "work", "body": "part of #222 epic", "headRefName": "y", "mergedAt": "2026-06-02T00:00:00Z"}]
        closing, mention = rb.issues_referenced_by_merged_prs(self.issues, prs)
        self.assertEqual(closing, {})
        self.assertIn(222, mention)

    def test_closing_wins_over_mention_for_same_issue(self):
        prs = [{"number": 101, "title": "t", "body": "refs #255 and closes #255", "headRefName": "z", "mergedAt": "2026-06-03T00:00:00Z"}]
        closing, mention = rb.issues_referenced_by_merged_prs(self.issues, prs)
        self.assertIn(255, closing)
        self.assertNotIn(255, mention)

    def test_negated_closing_keywords_remain_weak_mentions(self):
        phrases = (
            "Did not close #14",
            "Does not auto-close #14",
            "Does **not** close #14",
            "Cloud regeneration cannot close #14",
            "This doesn't close #14",
            "This will not resolve #14",
        )
        for body in phrases:
            with self.subTest(body=body):
                prs = [{
                    "number": 103,
                    "title": "status",
                    "body": body,
                    "headRefName": "status-only",
                    "mergedAt": "2026-06-04T00:00:00Z",
                }]
                closing, mention = rb.issues_referenced_by_merged_prs(self.issues, prs)
                self.assertEqual(closing, {})
                self.assertIn(14, mention)

    def test_positive_closing_reference_survives_negated_reference(self):
        prs = [{
            "number": 104,
            "title": "finish",
            "body": "The prep did not close #14. This final change fixes #14.",
            "headRefName": "finish-14",
            "mergedAt": "2026-06-05T00:00:00Z",
        }]
        closing, mention = rb.issues_referenced_by_merged_prs(self.issues, prs)
        self.assertIn(14, closing)
        self.assertNotIn(14, mention)

    def test_reference_to_unknown_issue_ignored(self):
        prs = [{"number": 102, "title": "t", "body": "Fixes #9999", "headRefName": "z", "mergedAt": "2026-06-03T00:00:00Z"}]
        closing, mention = rb.issues_referenced_by_merged_prs(self.issues, prs)
        self.assertEqual(closing, {})


class StaleWishlistTests(unittest.TestCase):
    def test_old_enhancement_flagged_recent_kept(self):
        issues = [
            {"number": 7, "title": "old idea", "labels": [{"name": "enhancement"}], "updatedAt": "2026-01-02T00:00:00Z"},
            {"number": 8, "title": "fresh idea", "labels": [{"name": "enhancement"}], "updatedAt": "2026-06-20T00:00:00Z"},
            {"number": 9, "title": "old bug", "labels": [{"name": "bug"}], "updatedAt": "2026-01-02T00:00:00Z"},
        ]
        # huge stale window → nothing stale; tiny window handled by _now-relative logic
        stale_all = {n for n, *_ in rb.stale_wishlist(issues, stale_days=1)}
        self.assertIn(7, stale_all)       # old + enhancement
        self.assertNotIn(9, stale_all)    # old but not enhancement
        # 8 is recent relative to now; with a 1-day window it depends on run date,
        # so only assert the label/type filter via the very-old #7 vs bug #9 above.

    def test_huge_window_flags_nothing(self):
        issues = [{"number": 7, "title": "x", "labels": [{"name": "enhancement"}], "updatedAt": "2026-01-02T00:00:00Z"}]
        self.assertEqual(rb.stale_wishlist(issues, stale_days=100000), [])


class RepoSlugTests(unittest.TestCase):
    def test_parses_ssh_and_https(self):
        for url, want in [
            ("git@github.com:Owner/repo.git", "Owner/repo"),
            ("https://github.com/Owner/repo.git", "Owner/repo"),
            ("https://github.com/Owner/repo", "Owner/repo"),
        ]:
            self.assertEqual(rb.parse_repo_slug(url), want)


class MergedBranchEvidenceTests(unittest.TestCase):
    def test_squash_merge_exact_sha_is_confirmed_without_ancestry(self):
        world = FakeWorld()
        world.refs["origin/codex/1041-squash-demo"] = SQUASH_SHA
        world.pull_pages = [[
            _pr(8801, "codex/1041-squash-demo", SQUASH_SHA, merged="2026-09-30T00:00:00Z"),
        ]]
        report = _report(world)
        section = _section(report, "3. Merged remote branches not pruned")
        self.assertIn("### Confirmed matches", section)
        self.assertIn("`origin/codex/1041-squash-demo` @ `" + SQUASH_SHA + "`", section)
        self.assertIn("PR #8801 head `" + SQUASH_SHA + "`", section)
        self.assertIn(rb.METHOD_SQUASH, section)
        self.assertNotIn(rb.METHOD_ANCESTRY, section)
        self.assertNotIn(rb.NONE_MARK, section)
        self.assertIn("not permission to delete", section)
        self.assertNotIn("git push origin --delete", section)

    def test_ancestry_merge_keeps_ancestry_evidence(self):
        world = FakeWorld()
        world.refs["origin/codex/1041-merge-demo"] = MERGE_SHA
        world.ancestors.add("origin/codex/1041-merge-demo")
        world.pull_pages = [[
            _pr(8802, "codex/1041-merge-demo", MERGE_SHA, merged="2026-09-29T00:00:00Z"),
        ]]
        report = _report(world)
        section = _section(report, "3. Merged remote branches not pruned")
        self.assertIn("### Confirmed matches", section)
        self.assertIn("`origin/codex/1041-merge-demo` @ `" + MERGE_SHA + "`", section)
        self.assertIn("PR #8802 head `" + MERGE_SHA + "`", section)
        self.assertIn(rb.METHOD_ANCESTRY, section)
        self.assertIn(rb.METHOD_SQUASH, section)

    def test_name_alone_is_not_confirmed_when_sha_differs(self):
        world = FakeWorld()
        world.refs["origin/codex/1041-post-merge"] = POST_SHA
        world.pull_pages = [[
            _pr(8803, "codex/1041-post-merge", SQUASH_SHA, merged="2026-09-28T00:00:00Z"),
        ]]
        report = _report(world)
        section = _section(report, "3. Merged remote branches not pruned")
        self.assertNotIn("### Confirmed matches", section)
        self.assertIn("### Post-merge commits", section)
        self.assertIn("`origin/codex/1041-post-merge` @ `" + POST_SHA + "`", section)
        self.assertIn("PR #8803 head `" + SQUASH_SHA + "`", section)
        self.assertIn(rb.METHOD_POST_MERGE, section)

    def test_reused_name_with_open_pr_is_not_confirmed(self):
        world = FakeWorld()
        world.refs["origin/codex/1041-reused"] = OPEN_SHA
        world.pull_pages = [[
            _pr(8804, "codex/1041-reused", SQUASH_SHA, merged="2026-09-20T00:00:00Z"),
            _pr(8805, "codex/1041-reused", OPEN_SHA, state="open"),
        ]]
        report = _report(world)
        section = _section(report, "3. Merged remote branches not pruned")
        self.assertNotIn("### Confirmed matches", section)
        self.assertIn("### Reused branch names or open PRs", section)
        self.assertIn("`origin/codex/1041-reused` @ `" + OPEN_SHA + "`", section)
        self.assertIn("PR #8805 head `" + OPEN_SHA + "`", section)
        self.assertIn(rb.METHOD_REUSED, section)
        self.assertNotIn("### Post-merge commits", section)

    def test_cross_repo_sha_match_is_mismatch_not_confirmed(self):
        world = FakeWorld()
        world.refs["origin/codex/1041-fork"] = SQUASH_SHA
        world.pull_pages = [[
            _pr(
                8806,
                "codex/1041-fork",
                SQUASH_SHA,
                repo="other/fork",
                merged="2026-09-21T00:00:00Z",
            ),
        ]]
        report = _report(world)
        section = _section(report, "3. Merged remote branches not pruned")
        self.assertNotIn("### Confirmed matches", section)
        self.assertIn("### Repository mismatches", section)
        self.assertIn("`origin/codex/1041-fork` @ `" + SQUASH_SHA + "`", section)
        self.assertIn("PR #8806 head `" + SQUASH_SHA + "` from `other/fork`", section)
        self.assertIn(rb.METHOD_REPO_MISMATCH, section)

    def test_pagination_follows_full_pages_then_short_page(self):
        world = FakeWorld()
        page1 = [
            _pr(9000 + i, f"codex/page1-{i}", OTHER_SHA, merged="2026-09-01T00:00:00Z")
            for i in range(2)
        ]
        page2 = [_pr(9100, "codex/page2", OTHER_SHA, merged="2026-09-02T00:00:00Z")]
        world.pull_pages = [page1, page2]
        with patch.object(rb, "run_cmd", side_effect=world.run):
            result = rb.gh_api(f"repos/{REPO}/pulls?state=all&per_page=2")
        self.assertTrue(result.complete)
        self.assertEqual(result.pages, 2)
        self.assertEqual(len(result.items), 3)
        self.assertEqual([
            c[2] for c in world.calls
            if c[:2] == ["gh", "api"] and c[2] != "graphql"
        ], [
            f"repos/{REPO}/pulls?state=all&per_page=2&page=1",
            f"repos/{REPO}/pulls?state=all&per_page=2&page=2",
        ])

    def test_partial_page_then_api_error_is_incomplete_not_none(self):
        world = FakeWorld()
        world.pull_pages = [[
            _pr(9200 + i, f"codex/partial-{i}", OTHER_SHA, merged="2026-09-03T00:00:00Z")
            for i in range(rb.DEFAULT_PER_PAGE)
        ]]
        world.pull_error_page = 2
        report = _report(world)
        section = _section(report, "3. Merged remote branches not pruned")
        self.assertIn("### Incomplete / unknown API or Git state", section)
        self.assertIn("incomplete", section.lower())
        self.assertNotIn(rb.NONE_MARK, section)
        one = _section(report, "1. Open issues a merged PR said it would CLOSE")
        self.assertIn("incomplete", one)
        self.assertNotIn(rb.NONE_MARK, one)

    def test_api_failure_is_incomplete_never_none(self):
        world = FakeWorld()
        world.pull_error_page = 1
        report = _report(world)
        section = _section(report, "3. Merged remote branches not pruned")
        self.assertIn("### Incomplete / unknown API or Git state", section)
        self.assertIn("failed", section)
        self.assertNotIn(rb.NONE_MARK, section)

    def test_git_ref_failure_is_incomplete_never_none(self):
        world = FakeWorld()
        world.ref_error = True
        report = _report(world)
        section = _section(report, "3. Merged remote branches not pruned")
        self.assertIn("### Incomplete / unknown API or Git state", section)
        self.assertIn("for-each-ref failed", section)
        self.assertNotIn(rb.NONE_MARK, section)

    def test_merge_base_failure_marks_branch_unknown(self):
        world = FakeWorld()
        world.refs["origin/codex/1041-unknown"] = OTHER_SHA
        world.ancestor_error_refs.add("origin/codex/1041-unknown")
        world.pull_pages = [[
            _pr(8807, "codex/1041-unknown", SQUASH_SHA, merged="2026-09-22T00:00:00Z"),
        ]]
        report = _report(world)
        section = _section(report, "3. Merged remote branches not pruned")
        self.assertIn("`origin/codex/1041-unknown` @ `" + OTHER_SHA + "`", section)
        self.assertIn(rb.METHOD_UNKNOWN, section)
        self.assertNotIn("### Confirmed matches", section)
        self.assertNotIn(rb.NONE_MARK, section)

    def test_checked_out_dirty_worktree_is_caution(self):
        world = FakeWorld()
        world.refs["origin/codex/1041-dirty"] = SQUASH_SHA
        world.worktrees.append({
            "path": "/worktrees/1041-dirty",
            "head": SQUASH_SHA,
            "branch": "codex/1041-dirty",
            "dirty": True,
        })
        world.pull_pages = [[
            _pr(8808, "codex/1041-dirty", SQUASH_SHA, merged="2026-09-23T00:00:00Z"),
        ]]
        report = _report(world)
        section = _section(report, "3. Merged remote branches not pruned")
        self.assertIn("### Confirmed matches", section)
        self.assertIn("caution: checked out at /worktrees/1041-dirty", section)
        self.assertIn("caution: dirty work at /worktrees/1041-dirty", section)

    def test_unavailable_worktree_state_is_caution(self):
        world = FakeWorld()
        world.refs["origin/codex/1041-occupied"] = SQUASH_SHA
        world.worktrees.append({
            "path": "/worktrees/1041-occupied",
            "head": SQUASH_SHA,
            "branch": "codex/1041-occupied",
            "dirty": False,
        })
        world.status_error_paths.add("/worktrees/1041-occupied")
        world.pull_pages = [[
            _pr(8809, "codex/1041-occupied", SQUASH_SHA, merged="2026-09-24T00:00:00Z"),
        ]]
        report = _report(world)
        section = _section(report, "3. Merged remote branches not pruned")
        self.assertIn("caution: checked out at /worktrees/1041-occupied", section)
        self.assertIn("caution: worktree state unavailable at /worktrees/1041-occupied", section)
        self.assertIn("### Incomplete / unknown API or Git state", section)

    def test_complete_empty_scan_still_reports_none(self):
        world = FakeWorld()
        report = _report(world)
        section = _section(report, "3. Merged remote branches not pruned")
        self.assertIn(rb.NONE_MARK, section)
        self.assertNotIn("### Confirmed matches", section)
        self.assertNotIn("### Incomplete / unknown API or Git state", section)

    def test_no_destructive_git_or_gh_commands_run(self):
        world = FakeWorld()
        world.refs["origin/codex/1041-squash-demo"] = SQUASH_SHA
        world.refs["origin/codex/1041-dirty"] = POST_SHA
        world.ancestors.add("origin/codex/1041-merge-demo")
        world.refs["origin/codex/1041-merge-demo"] = MERGE_SHA
        world.worktrees.append({
            "path": "/worktrees/1041-dirty",
            "head": POST_SHA,
            "branch": "codex/1041-dirty",
            "dirty": True,
        })
        world.pull_pages = [[
            _pr(8801, "codex/1041-squash-demo", SQUASH_SHA, merged="2026-09-30T00:00:00Z"),
            _pr(8802, "codex/1041-merge-demo", MERGE_SHA, merged="2026-09-29T00:00:00Z"),
            _pr(8803, "codex/1041-dirty", SQUASH_SHA, merged="2026-09-28T00:00:00Z"),
        ]]
        _report(world)
        self.assertTrue(world.calls)
        for argv in world.calls:
            if argv[:1] == ["git"]:
                self.assertTrue(rb._is_allowed_git(argv), argv)
                joined = " ".join(argv)
                self.assertNotIn(" push ", f" {joined} ")
                self.assertNotRegex(joined, r"branch\s+-[dD]")
                self.assertNotIn("worktree remove", joined)
                self.assertNotIn("worktree prune", joined)
                self.assertNotIn("update-ref -d", joined)
                self.assertNotRegex(joined, r"\breset\b")
                self.assertNotRegex(joined, r"\bclean\b")
            elif argv[:1] == ["gh"]:
                self.assertTrue(rb._is_allowed_gh(argv), argv)
                self.assertIn(argv[1], ("api", "issue"))
                self.assertNotIn("-X", argv)
                self.assertNotIn("close", argv)
            else:
                self.fail(f"unexpected command {argv!r}")

    def test_rest_pr_only_page_is_incomplete_not_zero_none(self):
        """Live bug: REST /issues returned 5 PRs, no Link, and the report said 0 / none."""
        world = FakeWorld()
        world.graphql_error = True
        world.issue_list_error = True
        world.issue_pages = [[_rest_pr(n) for n in (1113, 1112, 1111, 1110, 1109)]]
        report = _report(world)
        self.assertIn("open issues: **0** (incomplete)", report)
        one = _section(report, "1. Open issues a merged PR said it would CLOSE")
        four = _section(report, "4. Stale `enhancement` issues")
        self.assertIn("incomplete", one)
        self.assertNotIn(rb.NONE_MARK, one)
        self.assertIn("incomplete", four)
        self.assertNotIn(rb.NONE_MARK, four)
        self.assertIn("only pull requests", report)

    def test_graphql_issue_count_wins_over_rest_pr_only_page(self):
        world = FakeWorld()
        world.issue_pages = [[_rest_pr(n) for n in (1113, 1112, 1111, 1110, 1109)]]
        world.graphql_nodes = [
            _gql_issue(1041, "squash evidence"),
            _gql_issue(14, "Indigenomics CTO"),
        ]
        world.graphql_total = 2
        report = _report(world)
        self.assertIn("open issues: **2**", report)
        self.assertNotIn("open issues: **0**", report)
        self.assertNotIn("(incomplete)", report.split("merged PRs scanned")[0])


if __name__ == "__main__":
    unittest.main()
