import io
import json
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
import check_current_state_drift  # noqa: E402


def _http_error(code: int) -> HTTPError:
    err = HTTPError("http://x", code, f"err{code}", hdrs=None, fp=io.BytesIO(b""))
    err.close()
    return err


def _clear_wp_process_creds():
    """Started patcher that removes injected WP credentials for deterministic tests."""
    patcher = mock.patch.dict(os.environ)
    patcher.start()
    # Both name pairs must go: the credential gate accepts either, so leaving the
    # WP_API_* pair set makes this test pass a bare shell but fail under Varlock.
    for key in ("WP_USER", "WP_APP_PASSWORD", "WP_API_USERNAME", "WP_API_PASSWORD"):
        os.environ.pop(key, None)
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
        self.assertIn(
            "WP_USER/WP_APP_PASSWORD (or WP_API_USERNAME/WP_API_PASSWORD) "
            "not set in process env",
            error,
        )


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

    def test_exit_one_smoke_preserves_version_and_failure_details(self):
        smoke = {
            "observed_wordpress_version": "7.0.6",
            "checks": [{"path": "(version gate)", "status": "fail",
                        "failures": ["expected WordPress 7.0.5, observed 7.0.6"]}],
        }
        completed = subprocess.CompletedProcess([], 1, json.dumps(smoke), "")
        with mock.patch.object(morning_truth_report.subprocess, "run", return_value=completed):
            result, payload = morning_truth_report.run_json_command(
                "Smoke", ["smoke"], Path("."), accepted_returncodes=(0, 1)
            )
        self.assertEqual(result.returncode, 1)
        self.assertEqual(payload, smoke)
        self.assertNotIn("observed_wordpress_version\":", result.stdout)
        summary = morning_truth_report.summarize_smoke(payload)
        self.assertEqual(summary["observed_version"], "7.0.6")
        self.assertEqual(summary["failures"], 1)
        self.assertEqual(summary["failure_details"], [
            "(version gate): expected WordPress 7.0.5, observed 7.0.6"
        ])

    def test_failed_github_query_with_valid_json_stays_unavailable(self):
        completed = subprocess.CompletedProcess([], 1, "[]", "authentication failed")
        with mock.patch.object(morning_truth_report.subprocess, "run", return_value=completed):
            _, payload = morning_truth_report.run_json_command("PRs", ["gh"], Path("."))
        self.assertIsNone(payload)

    def test_smoke_empty_malformed_or_unexpected_exit_stays_unavailable(self):
        for code, output in [(1, ""), (1, "invalid JSON"), (124, '{"checks": []}')]:
            with self.subTest(code=code, output=output):
                completed = subprocess.CompletedProcess([], code, output, "")
                with mock.patch.object(morning_truth_report.subprocess, "run", return_value=completed):
                    _, payload = morning_truth_report.run_json_command(
                        "Smoke", ["smoke"], Path("."), accepted_returncodes=(0, 1)
                    )
                self.assertIsNone(payload)

    def test_error_object_is_not_a_healthy_smoke_result(self):
        for payload in [{"message": "error"}, {"checks": []}, {"checks": "error"},
                        {"checks": ["error"]}, {"checks": [{"status": "unknown"}]}]:
            with self.subTest(payload=payload):
                self.assertFalse(morning_truth_report.summarize_smoke(payload)["available"])

    def test_report_surfaces_smoke_failure_and_fails_opt_in_gate(self):
        smoke = {"observed_wordpress_version": "7.0.6", "checks": [
            {"path": "(version gate)", "status": "fail", "failures": ["version mismatch"]}
        ]}
        def command(title, command, cwd, **kwargs):
            if title == "WP7 Public Smoke (JSON)":
                self.assertEqual(command[command.index("--expect-version") + 1], "7.0.5")
            if title == "Current-State Drift Check (JSON)":
                self.assertEqual(command[command.index("--work-plan") + 1],
                                 "docs/current-state/CURRENT-STATE-2026-09-21.md")
            output = json.dumps(smoke) if title == "WP7 Public Smoke (JSON)" else (
                "[]" if title in ("Issue JSON", "PR JSON") else '{"checks": []}'
            )
            return morning_truth_report.CommandResult(
                title, command, 1 if title == "WP7 Public Smoke (JSON)" else 0, output, ""
            )
        output = io.StringIO()
        with mock.patch.object(sys, "argv", ["report", "--stdout", "--skip-fetch", "--fail-on-error"]), \
             mock.patch.object(morning_truth_report, "run_command", side_effect=command), \
             mock.patch.object(morning_truth_report, "fetch_wp_queue_counts", return_value=(
                 {"future_posts": 0, "draft_posts": 1, "draft_pages": 1}, None)), \
             mock.patch("sys.stdout", output), mock.patch("sys.stderr", io.StringIO()):
            code = morning_truth_report.main()
        self.assertEqual(code, 1)
        self.assertIn("WordPress version (smoke): `7.0.6`", output.getvalue())
        self.assertIn("(version gate): version mismatch", output.getvalue())
        self.assertNotIn("public smoke result unavailable", output.getvalue())

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


class StartupBaselineTests(unittest.TestCase):
    def test_make_defaults_match_declared_snapshot_and_preserve_overrides(self):
        root = Path(__file__).resolve().parents[2]
        for target in ("status-readonly", "morning-truth", "morning-truth-checkpoint",
                       "current-state-drift-check"):
            with self.subTest(target=target):
                result = subprocess.run(["make", "-n", target], cwd=root,
                                        capture_output=True, text=True, check=True)
                self.assertIn("WORK_PLAN:-docs/current-state/CURRENT-STATE-2026-09-21.md",
                              result.stdout)
                if target != "current-state-drift-check":
                    self.assertIn("EXPECT_VERSION:-7.0.5", result.stdout)
        self.assertIn("CURRENT-STATE-2026-09-21.md", (root / "AGENTS.md").read_text())

    def test_direct_drift_script_uses_september_snapshot(self):
        with mock.patch.object(sys, "argv", ["drift"]):
            args = check_current_state_drift.parse_args()
        self.assertEqual(args.work_plan, Path("docs/current-state/CURRENT-STATE-2026-09-21.md"))


class MorningTruthOutputPathTests(unittest.TestCase):
    def test_default_report_uses_generated_state_directory(self):
        repo_root = Path("/workspace/kriskrug-wp")

        output = morning_truth_report.resolve_output_path(
            repo_root, "20260813-120000Z"
        )

        self.assertEqual(
            output,
            repo_root
            / ".generated/current-state"
            / "morning-truth-20260813-120000Z.md",
        )

    def test_checkpoint_report_uses_durable_reports_directory(self):
        repo_root = Path("/workspace/kriskrug-wp")

        output = morning_truth_report.resolve_output_path(
            repo_root, "20260813-120000Z", checkpoint=True
        )

        self.assertEqual(
            output,
            repo_root
            / "docs/current-state/reports"
            / "morning-truth-20260813-120000Z.md",
        )

    def test_stdout_has_no_output_path(self):
        output = morning_truth_report.resolve_output_path(
            Path("/workspace/kriskrug-wp"), "20260813-120000Z", stdout=True
        )

        self.assertIsNone(output)

    def test_output_modes_are_mutually_exclusive(self):
        with self.assertRaisesRegex(ValueError, "only one output mode"):
            morning_truth_report.resolve_output_path(
                Path("/workspace/kriskrug-wp"),
                "20260813-120000Z",
                stdout=True,
                checkpoint=True,
            )


if __name__ == "__main__":
    unittest.main()


class ThemeParityLineTests(unittest.TestCase):
    """Live-vs-repo Aurora drift reporting (#546 detector, wired into the report)."""

    @staticmethod
    def _result(returncode, stdout="", stderr=""):
        return morning_truth_report.CommandResult(
            title="Live vs Repo Aurora Version",
            command=["python3", "scripts/check_live_theme_parity.py"],
            returncode=returncode,
            stdout=stdout,
            stderr=stderr,
        )

    def test_drift_is_reported_as_drift(self):
        line = morning_truth_report.render_theme_parity_line(
            self._result(1, "FAIL theme version drift detected:\n  live: 1.5.7\n  repo: 1.5.8")
        )
        self.assertIn("DRIFT", line)
        self.assertIn("1.5.7", line)
        self.assertIn("1.5.8", line)

    def test_match_is_reported_as_in_sync(self):
        line = morning_truth_report.render_theme_parity_line(
            self._result(0, "PASS live and repo agree on Version: 1.5.8")
        )
        self.assertIn("in sync", line)
        self.assertNotIn("DRIFT", line)

    def test_unreachable_live_is_not_reported_as_a_pass(self):
        # The detector exits 0 for both a real match and a soft skip. A skip
        # must not read as "in sync" or the report would launder a
        # non-measurement into a green check.
        line = morning_truth_report.render_theme_parity_line(
            self._result(0, "WARN live theme unreachable (...)\nSKIP parity check (repo declares Version: 1.5.8)")
        )
        self.assertIn("not measured", line)
        self.assertNotIn("in sync", line)

    def test_repo_read_failure_is_reported_as_unmeasurable(self):
        line = morning_truth_report.render_theme_parity_line(
            self._result(2, "ERROR could not read repo Version from theme/kk-aurora/style.css")
        )
        self.assertIn("could not measure", line)
        self.assertNotIn("in sync", line)
