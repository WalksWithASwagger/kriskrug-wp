"""WP_API_* must satisfy every WP_USER/WP_APP_PASSWORD gate.

Regression guard for 2026-08-23: the Varlock vault only supplies the WP_API_*
names, so any code path that gates on WP_USER alone silently degrades to
unauthenticated. That broke `make status-readonly` and `make morning-truth`.
"""

from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import common  # noqa: E402

CRED_KEYS = ("WP_USER", "WP_APP_PASSWORD", "WP_API_USERNAME", "WP_API_PASSWORD")


def _env(**overrides: str) -> dict[str, str]:
    base = {k: v for k, v in os.environ.items() if k not in CRED_KEYS}
    base.update(overrides)
    return base


class CredentialAliasTests(unittest.TestCase):
    def test_api_names_alone_satisfy_the_process_gate(self):
        with mock.patch.dict(
            os.environ,
            _env(WP_API_USERNAME="someone", WP_API_PASSWORD="a b c d"),
            clear=True,
        ):
            self.assertTrue(common.has_wp_process_credentials())
            user, password = common.wp_process_credentials()
            self.assertEqual(user, "someone")
            self.assertEqual(password, "abcd", "spaces must be stripped")

    def test_legacy_names_alone_still_work(self):
        with mock.patch.dict(
            os.environ, _env(WP_USER="legacy", WP_APP_PASSWORD="pw"), clear=True
        ):
            self.assertTrue(common.has_wp_process_credentials())
            self.assertEqual(common.wp_process_credentials()[0], "legacy")

    def test_legacy_names_win_when_both_present(self):
        with mock.patch.dict(
            os.environ,
            _env(
                WP_USER="legacy",
                WP_APP_PASSWORD="pw",
                WP_API_USERNAME="api",
                WP_API_PASSWORD="apipw",
            ),
            clear=True,
        ):
            self.assertEqual(common.wp_process_credentials()[0], "legacy")

    def test_no_credentials_reports_false(self):
        with mock.patch.dict(os.environ, _env(), clear=True):
            self.assertFalse(common.has_wp_process_credentials())
            self.assertEqual(common.wp_process_credentials(), ("", ""))

    def test_partial_credentials_report_false(self):
        with mock.patch.dict(os.environ, _env(WP_API_USERNAME="only-user"), clear=True):
            self.assertFalse(common.has_wp_process_credentials())

    def test_no_script_gates_on_the_legacy_names_alone(self):
        """Every script touching WP creds must also accept the WP_API_* names."""
        offenders = []
        for path in sorted((REPO_ROOT / "scripts").glob("*.py")):
            text = path.read_text(encoding="utf-8", errors="ignore")
            if "WP_APP_PASSWORD" not in text and "WP_USER" not in text:
                continue
            if "WP_API_PASSWORD" in text or "WP_API_USERNAME" in text:
                continue
            if "has_wp_process_credentials" in text or "wp_process_credentials" in text:
                continue
            offenders.append(path.name)
        self.assertEqual(
            offenders, [], f"these gate on the unresolvable names only: {offenders}"
        )


if __name__ == "__main__":
    unittest.main()
