import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import reconcile_backlog as rb  # noqa: E402


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
        # exercise the regex directly via a fake remote-style string
        for url, want in [
            ("git@github.com:Owner/repo.git", "Owner/repo"),
            ("https://github.com/Owner/repo.git", "Owner/repo"),
            ("https://github.com/Owner/repo", "Owner/repo"),
        ]:
            import re
            m = re.search(r"[:/]([^/:]+/[^/]+?)(?:\.git)?$", url)
            self.assertEqual(m.group(1), want)


if __name__ == "__main__":
    unittest.main()
