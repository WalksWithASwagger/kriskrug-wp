import io
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from urllib.error import HTTPError

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import morning_truth_report  # noqa: E402


def _http_error(code: int) -> HTTPError:
    err = HTTPError("http://x", code, f"err{code}", hdrs=None, fp=io.BytesIO(b""))
    err.close()
    return err


def _clear_wp_process_creds():
    """Started patcher that removes injected WP credentials for deterministic tests."""
    patcher = mock.patch.dict(os.environ)
    patcher.start()
    os.environ.pop("WP_USER", None)
    os.environ.pop("WP_APP_PASSWORD", None)
    return patcher


class MorningTruthQueueCountsTests(unittest.TestCase):
    def test_fetch_wp_queue_counts_uses_shared_wpclient(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            env_path = repo_root / "scripts" / "notion-to-wp" / ".env"
            env_path.parent.mkdir(parents=True)
            env_path.write_text("WP_USER=u\nWP_APP_PASSWORD=p a s s\n", encoding="utf-8")
            client = object()
            counts = {"future_posts": 1, "draft_posts": 2, "draft_pages": 3}

            with mock.patch.object(morning_truth_report.WPClient, "from_env", return_value=client) as from_env, \
                 mock.patch.object(morning_truth_report, "wp_queue_counts", return_value=counts) as queue_counts:
                result, error = morning_truth_report.fetch_wp_queue_counts(repo_root)

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

            with mock.patch.object(morning_truth_report.WPClient, "from_env", return_value=object()), \
                 mock.patch.object(morning_truth_report, "wp_queue_counts", side_effect=_http_error(400)):
                result, error = morning_truth_report.fetch_wp_queue_counts(repo_root)

        self.assertIsNone(result)
        self.assertIn("failed to fetch live draft queue counts", error)
        self.assertIn("HTTP Error 400", error)

    def test_process_env_credentials_work_without_env_file(self):
        client = object()
        counts = {"future_posts": 4, "draft_posts": 5, "draft_pages": 6}
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.dict(os.environ, {"WP_USER": "u", "WP_APP_PASSWORD": "p"}), \
                 mock.patch.object(morning_truth_report.WPClient, "from_env", return_value=client) as from_env, \
                 mock.patch.object(morning_truth_report, "wp_queue_counts", return_value=counts):
                result, error = morning_truth_report.fetch_wp_queue_counts(Path(tmp))

        self.assertEqual(result, counts)
        self.assertIsNone(error)
        from_env.assert_called_once_with(None, timeout=30)

    def test_missing_env_file_and_process_env_is_reported(self):
        patcher = _clear_wp_process_creds()
        try:
            with tempfile.TemporaryDirectory() as tmp:
                result, error = morning_truth_report.fetch_wp_queue_counts(Path(tmp))
        finally:
            patcher.stop()

        self.assertIsNone(result)
        self.assertIn("missing env file", error)
        self.assertIn("WP_USER/WP_APP_PASSWORD not set in process env", error)


class MorningTruthAvailabilityTests(unittest.TestCase):
    def test_format_json_count_never_renders_failed_query_as_zero(self):
        self.assertEqual(morning_truth_report.format_json_count(None), "unavailable")
        self.assertEqual(morning_truth_report.format_json_count("gh error text"), "unavailable")
        self.assertEqual(morning_truth_report.format_json_count([]), "0")
        self.assertEqual(morning_truth_report.format_json_count([{"number": 1}]), "1")

    def test_summarize_smoke_unavailable_is_not_zero_failures(self):
        summary = morning_truth_report.summarize_smoke(None)
        self.assertFalse(summary["available"])
        self.assertIsNone(summary["failures"])
        self.assertIsNone(summary["warnings"])
        self.assertIsNone(summary["observed_version"])

    def test_summarize_smoke_counts_failures_and_warnings(self):
        summary = morning_truth_report.summarize_smoke(
            {
                "observed_wordpress_version": "7.0.1",
                "checks": [
                    {"status": "fail"},
                    {"status": "warn"},
                    {"status": "pass"},
                    {"status": "fail"},
                ],
            }
        )
        self.assertTrue(summary["available"])
        self.assertEqual(summary["failures"], 2)
        self.assertEqual(summary["warnings"], 1)
        self.assertEqual(summary["observed_version"], "7.0.1")

    def test_run_json_command_failure_yields_none_payload(self):
        completed = subprocess.CompletedProcess(
            args=["gh", "pr", "list"], returncode=1, stdout="", stderr="gh: auth required"
        )
        with mock.patch.object(morning_truth_report.subprocess, "run", return_value=completed):
            result, payload = morning_truth_report.run_json_command("PR JSON", ["gh", "pr", "list"], Path("."))

        self.assertEqual(result.returncode, 1)
        self.assertIsNone(payload)

    def test_run_json_command_invalid_json_yields_none_payload(self):
        completed = subprocess.CompletedProcess(
            args=["gh", "issue", "list"], returncode=0, stdout="definitely not json", stderr=""
        )
        with mock.patch.object(morning_truth_report.subprocess, "run", return_value=completed):
            result, payload = morning_truth_report.run_json_command("Issue JSON", ["gh", "issue", "list"], Path("."))

        self.assertEqual(result.returncode, 0)
        self.assertIsNone(payload)

    def test_collect_truth_errors_lists_every_unavailable_source(self):
        errors = morning_truth_report.collect_truth_errors(
            prs_json=None,
            issues_json=None,
            queue_error="missing env file",
            smoke_available=False,
            drift_json=None,
        )
        self.assertEqual(len(errors), 5)
        joined = "\n".join(errors)
        self.assertIn("open PR list unavailable", joined)
        self.assertIn("open issue list unavailable", joined)
        self.assertIn("draft queue counts unavailable", joined)
        self.assertIn("public smoke result unavailable", joined)
        self.assertIn("drift report unavailable", joined)

    def test_collect_truth_errors_empty_when_all_sources_resolved(self):
        errors = morning_truth_report.collect_truth_errors(
            prs_json=[],
            issues_json=[{"number": 1, "labels": []}],
            queue_error=None,
            smoke_available=True,
            drift_json={"checks": []},
        )
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
