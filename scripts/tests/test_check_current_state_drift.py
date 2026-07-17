import io
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from urllib.error import HTTPError

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import check_current_state_drift  # noqa: E402


def _http_error(code: int) -> HTTPError:
    err = HTTPError("http://x", code, f"err{code}", hdrs=None, fp=io.BytesIO(b""))
    err.close()
    return err


def _clear_wp_process_creds():
    """Context manager that removes injected WP credentials for deterministic tests."""
    patcher = mock.patch.dict(os.environ)
    patcher.start()
    os.environ.pop("WP_USER", None)
    os.environ.pop("WP_APP_PASSWORD", None)
    return patcher


class CurrentStateDriftQueueCountsTests(unittest.TestCase):
    def test_fetch_wp_queue_counts_uses_shared_wpclient(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            env_path = repo_root / "scripts" / "notion-to-wp" / ".env"
            env_path.parent.mkdir(parents=True)
            env_path.write_text("WP_USER=u\nWP_APP_PASSWORD=p a s s\n", encoding="utf-8")
            client = object()
            counts = {"future_posts": 1, "draft_posts": 2, "draft_pages": 3}

            with mock.patch.object(check_current_state_drift.WPClient, "from_env", return_value=client) as from_env, \
                 mock.patch.object(check_current_state_drift, "wp_queue_counts", return_value=counts) as queue_counts:
                result, error = check_current_state_drift.fetch_wp_queue_counts(repo_root)

        self.assertEqual(result, counts)
        self.assertIsNone(error)
        from_env.assert_called_once_with(env_path, timeout=30)
        queue_counts.assert_called_once_with(client)

    def test_fetch_wp_queue_counts_reports_http_400_instead_of_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            env_path = repo_root / "scripts" / "notion-to-wp" / ".env"
            env_path.parent.mkdir(parents=True)
            env_path.write_text("WP_USER=u\nWP_APP_PASSWORD=p\n", encoding="utf-8")

            with mock.patch.object(check_current_state_drift.WPClient, "from_env", return_value=object()), \
                 mock.patch.object(check_current_state_drift, "wp_queue_counts", side_effect=_http_error(400)):
                result, error = check_current_state_drift.fetch_wp_queue_counts(repo_root)

        self.assertIsNone(result)
        self.assertIn("failed to fetch live draft queue counts", error)
        self.assertIn("HTTP Error 400", error)

    def test_process_env_credentials_work_without_env_file(self):
        client = object()
        counts = {"future_posts": 4, "draft_posts": 5, "draft_pages": 6}
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict(os.environ, {"WP_USER": "u", "WP_APP_PASSWORD": "p"}), \
                 mock.patch.object(check_current_state_drift.WPClient, "from_env", return_value=client) as from_env, \
                 mock.patch.object(check_current_state_drift, "wp_queue_counts", return_value=counts):
                result, error = check_current_state_drift.fetch_wp_queue_counts(Path(tmp))

        self.assertEqual(result, counts)
        self.assertIsNone(error)
        from_env.assert_called_once_with(None, timeout=30)

    def test_missing_env_file_and_process_env_is_reported(self):
        patcher = _clear_wp_process_creds()
        try:
            with tempfile.TemporaryDirectory() as tmp:
                result, error = check_current_state_drift.fetch_wp_queue_counts(Path(tmp))
        finally:
            patcher.stop()

        self.assertIsNone(result)
        self.assertIn("missing env file", error)
        self.assertIn("WP_USER/WP_APP_PASSWORD not set in process env", error)


class CurrentStateDriftJsonSourceTests(unittest.TestCase):
    def test_failed_gh_command_returns_none_with_error(self):
        failed = check_current_state_drift.CommandResult(
            command=["gh", "pr", "list"], returncode=1, stdout="", stderr="gh: auth required"
        )
        with mock.patch.object(check_current_state_drift, "run_command", return_value=failed):
            payload, error = check_current_state_drift.load_json_result(["gh", "pr", "list"], Path("."))

        self.assertIsNone(payload)
        self.assertIn("command failed (1)", error)
        self.assertIn("gh: auth required", error)

    def test_invalid_json_returns_none_with_error(self):
        garbled = check_current_state_drift.CommandResult(
            command=["gh", "issue", "list"], returncode=0, stdout="not json at all", stderr=""
        )
        with mock.patch.object(check_current_state_drift, "run_command", return_value=garbled):
            payload, error = check_current_state_drift.load_json_result(["gh", "issue", "list"], Path("."))

        self.assertIsNone(payload)
        self.assertIn("invalid JSON", error)

    def test_build_observed_keeps_failed_sources_unavailable_not_zero(self):
        observed = check_current_state_drift.build_observed(None, None, None, None)
        self.assertIsNone(observed["open_prs"])
        self.assertIsNone(observed["open_issues"])
        self.assertIsNone(observed["wp_version"])
        self.assertIsNone(observed["future_posts"])
        self.assertIsNone(observed["draft_posts"])
        self.assertIsNone(observed["draft_pages"])

    def test_build_observed_counts_successful_sources(self):
        observed = check_current_state_drift.build_observed(
            [{"number": 1}],
            [{"number": 2}, {"number": 3}],
            {"future_posts": 7, "draft_posts": 8, "draft_pages": 9},
            {"observed_wordpress_version": "7.0.1"},
        )
        self.assertEqual(observed["open_prs"], 1)
        self.assertEqual(observed["open_issues"], 2)
        self.assertEqual(observed["wp_version"], "7.0.1")
        self.assertEqual(observed["future_posts"], 7)


class CurrentStateDriftEvaluationTests(unittest.TestCase):
    def test_evaluate_drift_distinguishes_no_drift_from_not_evaluated(self):
        declared = {"open_prs": 3, "open_issues": 5}
        observed = {"open_prs": 3, "open_issues": None}
        checks = {check["key"]: check for check in check_current_state_drift.evaluate_drift(declared, observed)}

        self.assertTrue(checks["open_prs"]["evaluated"])
        self.assertFalse(checks["open_prs"]["drift"])
        self.assertEqual(checks["open_prs"]["status"], "no drift")

        self.assertFalse(checks["open_issues"]["evaluated"])
        self.assertFalse(checks["open_issues"]["drift"])
        self.assertEqual(checks["open_issues"]["status"], "not evaluated")

    def test_evaluate_drift_flags_real_drift(self):
        checks = {
            check["key"]: check
            for check in check_current_state_drift.evaluate_drift({"open_prs": 3}, {"open_prs": 4})
        }
        self.assertEqual(checks["open_prs"]["status"], "drift")
        self.assertTrue(checks["open_prs"]["drift"])

    def test_render_human_shows_unavailable_and_not_evaluated(self):
        checks = check_current_state_drift.evaluate_drift({"open_prs": 3}, {"open_prs": None})
        report = {
            "work_plan": "docs/current-state/WORK-PLAN.md",
            "base_url": "https://example.test",
            "checks": checks,
            "errors": ["command failed (1): gh pr list"],
        }
        rendered = check_current_state_drift.render_human(report)

        self.assertIn("| Open PRs | 3 | unavailable | not evaluated |", rendered)
        self.assertNotIn("| Open PRs | 3 | 0 |", rendered)
        self.assertIn("command failed (1): gh pr list", rendered)


if __name__ == "__main__":
    unittest.main()
