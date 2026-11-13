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

    def test_halves_from_two_name_families_report_false(self):
        for halves in (
            {"WP_USER": "legacy-user", "WP_API_PASSWORD": "alias-pw"},
            {"WP_API_USERNAME": "alias-user", "WP_APP_PASSWORD": "legacy-pw"},
            {"WP_USER": "legacy-user", "WP_APP_PASSWORD": "   "},
        ):
            with (
                self.subTest(halves=sorted(halves)),
                mock.patch.dict(os.environ, _env(**halves), clear=True),
            ):
                self.assertFalse(common.has_wp_process_credentials())
                self.assertEqual(common.wp_process_credentials(), ("", ""))

    def test_complete_api_pair_beats_a_legacy_half(self):
        with mock.patch.dict(
            os.environ,
            _env(WP_USER="legacy-half", WP_API_USERNAME="api", WP_API_PASSWORD="apipw"),
            clear=True,
        ):
            self.assertEqual(common.wp_process_credentials(), ("api", "apipw"))

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
    """load_env: the first source and name family holding a whole pair wins.

    Order: process legacy pair, process alias pair, file legacy pair, file alias
    pair, then nothing. Halves never combine across sources or families, and the
    base URL follows the pair. Every value is a fake label naming its own source,
    family and field, so a failure shows which source won and nothing real is
    loaded or printed.
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

    FILE_URL = "https://file.example.test"
    PROCESS_URL = "https://process.example.test"

    def write_file(self, file_values: dict[str, str], file_url: str | None = FILE_URL):
        lines = [f"{key}={value}" for key, value in file_values.items()]
        # Every case reads a real file, even one that holds no credentials.
        lines.append(f"WP_BASE_URL={file_url}" if file_url else "# no base URL")
        self.env_file.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def load(
        self,
        process: dict[str, str],
        file_values: dict[str, str],
        *,
        file_url: str | None = FILE_URL,
        **kwargs,
    ):
        self.write_file(file_values, file_url)
        with self.process_env(process):
            return common.load_env(self.env_file, **kwargs)

    def pair(self, values: dict[str, str]) -> tuple[str | None, str | None]:
        return values.get("WP_USER"), values.get("WP_APP_PASSWORD")

    def halves(self, source: str):
        """Every one-key half pair a source can hold."""
        for names in self.NAMES.values():
            for family, name in names.items():
                yield name, {name: f"{source}-{family}-half"}

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

    def test_half_pairs_never_complete_each_other(self):
        """No half in one place may be finished by a half from anywhere else."""
        for process_name, process_half in self.halves("process"):
            for file_name, file_half in self.halves("file"):
                with self.subTest(process=process_name, file=file_name):
                    values = self.load(process_half, file_half)
                    self.assertEqual(self.pair(values), (None, None))
                    with self.assertRaises(RuntimeError):
                        common.wp_credentials(values)
        whole = ({"WP_USER", "WP_APP_PASSWORD"}, {"WP_API_USERNAME", "WP_API_PASSWORD"})
        for first, first_half in self.halves("process"):
            for second, second_half in self.halves("process"):
                if first == second or {first, second} in whole:
                    continue
                with self.subTest(process=(first, second)):
                    values = self.load({**first_half, **second_half}, {})
                    self.assertEqual(self.pair(values), (None, None))

    def test_process_half_pair_leaves_the_file_pair_whole(self):
        for name, half in self.halves("process"):
            for family in self.FAMILIES:
                with self.subTest(process=name, file=family):
                    values = self.load(half, self.layer("file", (family,)))
                    self.assertEqual(
                        self.pair(values),
                        (f"file-{family}-user", f"file-{family}-password"),
                    )
                    self.assertEqual(values["WP_BASE_URL"], self.FILE_URL)

    def test_whole_alias_pair_beats_a_legacy_half_in_the_same_source(self):
        process = {
            "WP_USER": "process-legacy-half",
            **self.layer("process", ("alias",)),
        }
        values = self.load(process, self.layer("file", ("legacy",)))
        self.assertEqual(
            self.pair(values), ("process-alias-user", "process-alias-password")
        )

    def test_whitespace_only_values_count_as_empty(self):
        blank_pairs = (
            {"WP_USER": " ", "WP_APP_PASSWORD": "\t"},
            {"WP_USER": "process-legacy-user", "WP_APP_PASSWORD": "   "},
            {"WP_API_USERNAME": "  ", "WP_API_PASSWORD": "process-alias-password"},
        )
        for process in blank_pairs:
            with self.subTest(process=sorted(process)):
                values = self.load(process, self.layer("file", ("alias",)))
                self.assertEqual(
                    self.pair(values), ("file-alias-user", "file-alias-password")
                )
        values = self.load(
            {**self.layer("process", ("legacy",)), "WP_BASE_URL": "  "}, {}
        )
        self.assertNotIn("WP_BASE_URL", values)
        self.env_file.write_text(
            'WP_USER="  "\nWP_APP_PASSWORD="file-legacy-password"\n', encoding="utf-8"
        )
        with self.process_env({}):
            self.assertEqual(self.pair(common.load_env(self.env_file)), (None, None))

    def test_base_url_follows_the_chosen_pair(self):
        process_pair = self.layer("process", ("alias",))
        file_pair = self.layer("file", ("legacy",))
        process_url = {"WP_BASE_URL": self.PROCESS_URL}
        cases = (
            # (process, file pair, file URL, expected base URL)
            (process_pair, file_pair, self.FILE_URL, common.DEFAULT_BASE_URL),
            (process_pair, {}, "http://localhost:10003", common.DEFAULT_BASE_URL),
            (
                {**process_pair, **process_url},
                file_pair,
                self.FILE_URL,
                self.PROCESS_URL,
            ),
            (process_url, file_pair, self.FILE_URL, self.FILE_URL),
            (process_url, file_pair, None, common.DEFAULT_BASE_URL),
            ({}, file_pair, self.FILE_URL, self.FILE_URL),
        )
        for index, (process, file_values, file_url, expected) in enumerate(cases):
            with self.subTest(case=index):
                values = self.load(process, file_values, file_url=file_url)
                self.assertEqual(common.wp_credentials(values)[0], expected)
                with self.process_env(process):
                    client = common.WPClient.from_env(self.env_file)
                self.assertEqual(client.base, expected)

    def test_base_url_without_any_pair_is_not_returned(self):
        values = self.load({"WP_BASE_URL": self.PROCESS_URL}, {})
        self.assertNotIn("WP_BASE_URL", values)

    def test_login_mode_takes_the_pair_from_the_source_that_set_it(self):
        process_pair = self.layer("process", ("alias",))
        file_pair = self.layer("file", ("legacy",))
        process_user = ("process-alias-user", "process-alias-password")
        file_user = ("file-legacy-user", "file-legacy-password")
        login = {"WP_AUTH_MODE": "login"}
        basic = {"WP_AUTH_MODE": "basic"}
        cases = (
            # (process, file, expected pair, expected mode)
            (process_pair, {**file_pair, **login}, file_user, "login"),
            (process_pair, {**file_pair, "WP_AUTH_MODE": "LOGIN"}, file_user, "LOGIN"),
            ({**process_pair, **login}, file_pair, process_user, "login"),
            ({**process_pair, **login}, {**file_pair, **login}, process_user, "login"),
            (login, file_pair, (None, None), "login"),
            (login, {**file_pair, **login}, (None, None), "login"),
            (process_pair, login, (None, None), "login"),
            (process_pair, {**file_pair, **basic}, process_user, "basic"),
            ({**process_pair, **basic}, {**file_pair, **login}, process_user, "basic"),
        )
        for index, (process, file_values, expected, mode) in enumerate(cases):
            with self.subTest(case=index):
                values = self.load(process, file_values)
                self.assertEqual(self.pair(values), expected)
                self.assertEqual(values["WP_AUTH_MODE"], mode)
                if expected == (None, None):
                    with self.assertRaisesRegex(RuntimeError, "WP_AUTH_MODE=login"):
                        common.wp_credentials(values)

    def test_login_mode_in_the_file_also_takes_the_file_base_url(self):
        values = self.load(
            {**self.layer("process", ("alias",)), "WP_BASE_URL": self.PROCESS_URL},
            {**self.layer("file", ("legacy",)), "WP_AUTH_MODE": "login"},
        )
        self.assertEqual(values["WP_BASE_URL"], self.FILE_URL)

    def test_other_file_keys_pass_through_and_alias_names_are_not_returned(self):
        values = self.load(
            self.layer("process", ("alias",)),
            {**self.layer("file", ("alias",)), "WP_DEFAULT_AUTHOR_ID": "18"},
        )
        self.assertEqual(values["WP_DEFAULT_AUTHOR_ID"], "18")
        self.assertNotIn("WP_API_USERNAME", values)
        self.assertNotIn("WP_API_PASSWORD", values)

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
