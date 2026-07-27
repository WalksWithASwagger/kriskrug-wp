"""CI-safe unit tests for the #546 live-vs-repo theme parity check.

All live HTTP is mocked via fetch_live_style / read_repo_version, so these run
offline with no network. Cases covered: match (exit 0), mismatch (exit 1),
and offline degrade (exit 0 + warning).
"""

import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import check_live_theme_parity as parity  # noqa: E402

LIVE_STYLE = """/*
Theme Name: KK Aurora
Version: 1.5.0
*/
"""


def run_main(repo_version, fetch_result):
    """Run parity.main() with mocked repo + live reads; return (code, stdout)."""
    buf = io.StringIO()
    with (
        mock.patch.object(parity, "read_repo_version", return_value=repo_version),
        mock.patch.object(parity, "fetch_live_style", return_value=fetch_result),
        mock.patch.object(sys, "argv", ["check_live_theme_parity.py"]),
    ):
        with redirect_stdout(buf):
            code = parity.main()
    return code, buf.getvalue()


class ParseVersionTests(unittest.TestCase):
    def test_parses_version_header(self):
        self.assertEqual(parity.parse_version(LIVE_STYLE), "1.5.0")

    def test_none_when_absent(self):
        self.assertIsNone(parity.parse_version("/* no version here */"))


class ParityMainTests(unittest.TestCase):
    def test_match_exits_zero(self):
        code, out = run_main("1.5.0", (200, LIVE_STYLE))
        self.assertEqual(code, 0)
        self.assertIn("PASS", out)
        self.assertIn("1.5.0", out)

    def test_mismatch_exits_nonzero(self):
        code, out = run_main("1.4.9", (200, LIVE_STYLE))
        self.assertEqual(code, 1)
        self.assertIn("FAIL", out)
        self.assertIn("1.5.0", out)  # live
        self.assertIn("1.4.9", out)  # repo

    def test_offline_degrades_soft_skip(self):
        code, out = run_main("1.4.9", (0, "timed out"))
        self.assertEqual(code, 0)
        self.assertIn("WARN", out)
        self.assertIn("SKIP", out)

    def test_bad_repo_version_exits_two(self):
        code, out = run_main(None, (200, LIVE_STYLE))
        self.assertEqual(code, 2)
        self.assertIn("ERROR", out)

    def test_live_http_error_exits_two(self):
        code, out = run_main("1.5.0", (503, ""))
        self.assertEqual(code, 2)
        self.assertIn("HTTP 503", out)

    def test_live_missing_version_exits_two(self):
        code, out = run_main("1.5.0", (200, "/* no version */"))
        self.assertEqual(code, 2)
        self.assertIn("no parseable Version", out)


if __name__ == "__main__":
    unittest.main()
