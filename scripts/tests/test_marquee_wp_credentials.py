"""Marquee sync resolves WP credentials through common.load_env.

wp_sync used to parse scripts/notion-to-wp/.env itself and let the file beat the
process env, and it only knew the WP_USER names. Values here are fake and
injected through the process environment. The no-file cases refuse every file
open, so they prove credentials resolve without reading a .env.
"""

from __future__ import annotations

import builtins
import contextlib
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts/marquee"))

import common  # noqa: E402
import sync  # noqa: E402
import wp_sync  # noqa: E402

ISOLATED_KEYS = (*common._OVERRIDE_KEYS, "KKAI_ENV_PATH", "NOTION_ENV_PATH")


def process_env(**values: str):
    env = {k: v for k, v in os.environ.items() if k not in ISOLATED_KEYS}
    env.update(values)
    return mock.patch.dict(os.environ, env, clear=True)


@contextlib.contextmanager
def refuse_file_reads():
    blocked = AssertionError("credential loading opened a file")
    with (
        mock.patch.object(builtins, "open", side_effect=blocked),
        mock.patch.object(io, "open", side_effect=blocked),
        mock.patch.object(common, "parse_simple_env", side_effect=blocked),
        mock.patch.object(common, "dotenv_values", side_effect=blocked),
    ):
        yield


class _TempEnvPath(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.env_file = Path(tmp.name) / "connector.env"
        patcher = mock.patch.object(wp_sync, "ENV_PATH", self.env_file)
        patcher.start()
        self.addCleanup(patcher.stop)


class LoadWpCredentialsTests(_TempEnvPath):
    def test_varlock_names_resolve_with_no_env_file_and_no_file_read(self):
        with (
            process_env(WP_API_USERNAME="fake-user", WP_API_PASSWORD="fake app pass"),
            refuse_file_reads(),
        ):
            creds = wp_sync.load_wp_credentials()
        self.assertEqual(
            creds,
            {
                "base": "https://kriskrug.co",
                "user": "fake-user",
                "app_password": "fakeapppass",
            },
        )

    def test_process_env_wins_over_the_env_file_under_either_name_pair(self):
        self.env_file.write_text(
            "WP_USER=file-user\nWP_APP_PASSWORD=file-pass\n"
            "WP_BASE_URL=https://file.example.test/\n",
            encoding="utf-8",
        )
        for user_key, password_key in (
            ("WP_USER", "WP_APP_PASSWORD"),
            ("WP_API_USERNAME", "WP_API_PASSWORD"),
        ):
            with (
                self.subTest(names=(user_key, password_key)),
                process_env(**{user_key: "env-user", password_key: "env-pass"}),
            ):
                creds = wp_sync.load_wp_credentials()
                self.assertEqual(
                    (creds["user"], creds["app_password"]), ("env-user", "env-pass")
                )
                self.assertEqual(creds["base"], "https://file.example.test")

    def test_env_file_alone_still_works(self):
        self.env_file.write_text(
            "WP_API_USERNAME=file-user\nWP_API_PASSWORD=file pass\n", encoding="utf-8"
        )
        with process_env():
            creds = wp_sync.load_wp_credentials()
        self.assertEqual(
            (creds["user"], creds["app_password"]), ("file-user", "filepass")
        )

    def test_nothing_anywhere_resolves_to_none(self):
        with process_env(), refuse_file_reads():
            creds = wp_sync.load_wp_credentials()
        self.assertEqual(
            creds, {"base": "https://kriskrug.co", "user": None, "app_password": None}
        )


class SyncCliTests(_TempEnvPath):
    """sync.py keeps its flags and exit codes; output is captured, never printed."""

    def run_cli(self, *argv: str):
        output = io.StringIO()
        with (
            mock.patch.object(sys, "argv", ["sync.py", *argv]),
            mock.patch.object(sync, "load", return_value={"boards": []}),
            mock.patch.object(wp_sync, "MarqueeWP") as client,
            contextlib.redirect_stdout(output),
        ):
            code = sync.main()
        return code, client, output.getvalue()

    def test_execute_without_credentials_exits_1_before_building_a_client(self):
        with process_env(), refuse_file_reads():
            code, client, output = self.run_cli("--execute")
        self.assertEqual(code, 1)
        client.assert_not_called()
        self.assertIn("make varlock-run", output)

    def test_execute_builds_the_client_from_injected_credentials(self):
        with (
            process_env(WP_API_USERNAME="fake-user", WP_API_PASSWORD="fake-pass"),
            refuse_file_reads(),
        ):
            code, client, _ = self.run_cli("--execute")
        self.assertEqual(code, 0)
        client.assert_called_once_with("https://kriskrug.co", "fake-user", "fake-pass")

    def test_dry_run_never_loads_credentials(self):
        with mock.patch.object(wp_sync, "load_wp_credentials") as loader:
            code, client, _ = self.run_cli()
        self.assertEqual(code, 0)
        loader.assert_not_called()
        client.assert_not_called()


if __name__ == "__main__":
    unittest.main()
