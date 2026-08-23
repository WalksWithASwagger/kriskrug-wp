"""`make doctor` must always render a flat (status, detail) pair.

Regression guard for 2026-08-23: check_gh() used
`return OK, f"..." if m else (OK, "...")`, which binds as
`(OK, (OK, "..."))` when the regex misses, so the report printed a tuple
where the detail line belongs.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import doctor  # noqa: E402


class ReturnShapeTests(unittest.TestCase):
    def _assert_pair(self, result, label):
        self.assertIsInstance(result, tuple, f"{label} must return a tuple")
        self.assertEqual(len(result), 2, f"{label} must return exactly 2 values")
        status, detail = result
        self.assertIn(status, (doctor.OK, doctor.WARN, doctor.FAIL), label)
        self.assertIsInstance(detail, str, f"{label} detail must be a plain string")

    def test_every_registered_check_returns_a_flat_pair(self):
        for name, fn in doctor.CHECKS:
            self._assert_pair(fn(), name)

    def test_gh_check_handles_unrecognised_status_output(self):
        """The branch that produced the nested tuple."""
        with mock.patch.object(doctor.shutil, "which", return_value="/usr/bin/gh"), \
             mock.patch.object(doctor, "run", return_value=(0, "some other wording")):
            self._assert_pair(doctor.check_gh(), "check_gh/no-regex-match")
            self.assertEqual(doctor.check_gh()[1], "authenticated")

    def test_gh_check_extracts_the_login(self):
        out = "github.com\n  ✓ Logged in to github.com account someuser (GH_TOKEN)"
        with mock.patch.object(doctor.shutil, "which", return_value="/usr/bin/gh"), \
             mock.patch.object(doctor, "run", return_value=(0, out)):
            self.assertEqual(doctor.check_gh(), (doctor.OK, "authenticated as someuser"))

    def test_gh_check_reports_fail_when_unauthenticated(self):
        with mock.patch.object(doctor.shutil, "which", return_value="/usr/bin/gh"), \
             mock.patch.object(doctor, "run", return_value=(1, "not logged in")):
            self.assertEqual(doctor.check_gh()[0], doctor.FAIL)

    def test_credentials_check_never_prints_a_secret(self):
        secret = "super-secret-password-value"
        with mock.patch.object(
            doctor, "wp_process_credentials", create=True
        ), mock.patch.dict(
            "os.environ",
            {"WP_API_USERNAME": "someuser", "WP_API_PASSWORD": secret},
            clear=True,
        ):
            status, detail = doctor.check_wp_credentials()
            self.assertEqual(status, doctor.OK)
            self.assertNotIn(secret, detail)
            self.assertNotIn("someuser", detail)

    def test_a_raising_check_is_reported_not_crashed(self):
        with mock.patch.object(doctor, "CHECKS", [("boom", lambda: 1 / 0)]):
            self.assertEqual(doctor.main(), 1)


if __name__ == "__main__":
    unittest.main()
