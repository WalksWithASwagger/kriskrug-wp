"""WP_API_* must satisfy every WP_USER/WP_APP_PASSWORD gate.

Regression guard for 2026-08-23: the Varlock vault only supplies the WP_API_*
names, so any code path that gates on WP_USER alone silently degrades to
unauthenticated. That broke `make status-readonly` and `make morning-truth`.
"""

from __future__ import annotations

import itertools
import os
import sys
import tempfile
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


class LoadEnvPrecedenceTests(unittest.TestCase):
    """load_env: process env beats the file across both name families, then the file, then nothing.

    Every value is a fake label naming its own source, family and field, so a
    failure shows which source won and nothing real is loaded or printed.
    """

    FAMILIES = ("legacy", "alias")
    NAMES = {
        "user": {"legacy": "WP_USER", "alias": "WP_API_USERNAME"},
        "password": {"legacy": "WP_APP_PASSWORD", "alias": "WP_API_PASSWORD"},
    }
    FAMILY_SETS = ((), ("legacy",), ("alias",), ("legacy", "alias"))

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.env_file = Path(tmp.name) / "connector.env"

    def layer(self, source: str, families) -> dict[str, str]:
        return {
            names[family]: f"{source}-{family}-{field}"
            for field, names in self.NAMES.items()
            for family in families
        }

    def process_env(self, process: dict[str, str]):
        isolated = {
            k: v for k, v in os.environ.items() if k not in common._OVERRIDE_KEYS
        }
        return mock.patch.dict(os.environ, {**isolated, **process}, clear=True)

    def load(self, process: dict[str, str], file_values: dict[str, str], **kwargs):
        lines = [f"{key}={value}" for key, value in file_values.items()]
        # Every case reads a real file, even one that holds no credentials.
        lines.append("WP_BASE_URL=https://file.example.test")
        self.env_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
        with self.process_env(process):
            return common.load_env(self.env_file, **kwargs)

    def winner(self, process_families, file_families) -> str | None:
        ranked = [("process", f) for f in self.FAMILIES if f in process_families]
        ranked += [("file", f) for f in self.FAMILIES if f in file_families]
        return "-".join(ranked[0]) if ranked else None

    def test_every_source_and_name_family_combination(self):
        for process_families, file_families in itertools.product(
            self.FAMILY_SETS, repeat=2
        ):
            with self.subTest(process=process_families, file=file_families):
                values = self.load(
                    self.layer("process", process_families),
                    self.layer("file", file_families),
                )
                winner = self.winner(process_families, file_families)
                if winner is None:
                    self.assertNotIn("WP_USER", values)
                    self.assertNotIn("WP_APP_PASSWORD", values)
                    with self.assertRaises(RuntimeError):
                        common.wp_credentials(values)
                    continue
                self.assertEqual(values["WP_USER"], f"{winner}-user")
                self.assertEqual(values["WP_APP_PASSWORD"], f"{winner}-password")
                self.assertEqual(
                    common.wp_credentials(values)[1:],
                    (f"{winner}-user", f"{winner}-password"),
                )

    def test_process_alias_pair_beats_file_legacy_pair_through_from_env(self):
        """The reported bug: a file WP_USER used to beat a Varlock WP_API_USERNAME."""
        self.env_file.write_text(
            "WP_USER=file-legacy-user\nWP_APP_PASSWORD=file-legacy-password\n",
            encoding="utf-8",
        )
        with self.process_env(self.layer("process", ("alias",))):
            client = common.WPClient.from_env(self.env_file)
        self.assertEqual(
            (client.user, client.app_password),
            ("process-alias-user", "process-alias-password"),
        )

    def test_empty_process_values_do_not_shadow_the_file(self):
        empty = {name: "" for names in self.NAMES.values() for name in names.values()}
        values = self.load(empty, self.layer("file", ("alias",)))
        self.assertEqual(values["WP_USER"], "file-alias-user")
        self.assertEqual(values["WP_APP_PASSWORD"], "file-alias-password")

    def test_overlay_disabled_ignores_the_process_env(self):
        for file_families in self.FAMILY_SETS:
            with self.subTest(file=file_families):
                values = self.load(
                    self.layer("process", self.FAMILIES),
                    self.layer("file", file_families),
                    overlay_os=False,
                )
                winner = self.winner((), file_families)
                expected = f"{winner}-user" if winner else None
                self.assertEqual(values.get("WP_USER"), expected)


if __name__ == "__main__":
    unittest.main()
