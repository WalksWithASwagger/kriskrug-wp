import io
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

    def test_missing_env_file_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            result, error = morning_truth_report.fetch_wp_queue_counts(Path(tmp))

        self.assertIsNone(result)
        self.assertIn("missing env file", error)


if __name__ == "__main__":
    unittest.main()
