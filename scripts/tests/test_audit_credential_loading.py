"""The two credentialed audit targets load WP credentials through common.load_env (#1226).

Values are fake and injected through the process environment. The no-file cases
block every file open, so they prove credentials resolve without reading a .env.
"""

from __future__ import annotations

import builtins
import importlib.util
import io
import os
import re
import sys
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest import mock

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = SCRIPTS_DIR.parent
sys.path.insert(0, str(SCRIPTS_DIR))

import common  # noqa: E402


def _load(module_name: str, filename: str):
    spec = importlib.util.spec_from_file_location(module_name, SCRIPTS_DIR / filename)
    module = importlib.util.module_from_spec(spec)
    # Both scripts define dataclasses, which look their module up in sys.modules.
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


TARGETS = (
    (
        "jetpack-feedback-audit",
        _load("jetpack_feedback_audit", "jetpack_feedback_audit.py"),
    ),
    ("wp7-admin-readiness", _load("wp7_admin_readiness", "wp7-admin-readiness.py")),
)
CREDENTIAL_KEYS = (
    "WP_USER",
    "WP_APP_PASSWORD",
    "WP_API_USERNAME",
    "WP_API_PASSWORD",
    "WP_BASE_URL",
    "WP_AUTH_MODE",
    "KKAI_ENV_PATH",
    "NOTION_ENV_PATH",
)


def process_env(**values: str):
    env = {k: v for k, v in os.environ.items() if k not in CREDENTIAL_KEYS}
    env.update(values)
    return mock.patch.dict(os.environ, env, clear=True)


@contextmanager
def refuse_file_reads():
    blocked = AssertionError("credential loading opened a file")
    with (
        mock.patch.object(builtins, "open", side_effect=blocked),
        mock.patch.object(io, "open", side_effect=blocked),
        mock.patch.object(common, "parse_simple_env", side_effect=blocked),
        mock.patch.object(common, "dotenv_values", side_effect=blocked),
    ):
        yield


class _Stop(Exception):
    pass


class AuditCredentialLoadingTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tmp = Path(tmp.name)
        defaults = mock.patch.object(
            common, "DEFAULT_ENV_PATHS", (self.tmp / "absent.env",)
        )
        defaults.start()
        self.addCleanup(defaults.stop)

    def resolve(self, target, module, *argv):
        """Run main() with the target's argv and return the Config it built."""
        seen = []

        def capture(config, timeout):
            seen.append(config)
            raise _Stop

        with (
            mock.patch.object(sys, "argv", [target, *argv]),
            mock.patch.object(module, "collect", side_effect=capture),
            self.assertRaises(_Stop),
        ):
            module.main()
        return seen[0]

    def test_varlock_names_resolve_with_no_env_file_and_no_file_read(self):
        missing = str(self.tmp / "missing.env")
        for target, module in TARGETS:
            for argv in ((), ("--env-file", missing)):
                with (
                    self.subTest(target=target, argv=argv),
                    process_env(
                        WP_API_USERNAME="fake-user", WP_API_PASSWORD="fake app pass"
                    ),
                    refuse_file_reads(),
                ):
                    config = self.resolve(target, module, *argv)
                    self.assertEqual(config.user, "fake-user")
                    self.assertEqual(config.app_password, "fakeapppass")
                    self.assertEqual(config.base_url, "https://kriskrug.co")

    def test_process_env_wins_over_env_file(self):
        env_file = self.tmp / "connector.env"
        env_file.write_text(
            "WP_USER=file-user\nWP_APP_PASSWORD=file-pass\nWP_BASE_URL=https://file.example.test\n",
            encoding="utf-8",
        )
        for target, module in TARGETS:
            with (
                self.subTest(target=target),
                process_env(WP_USER="env-user", WP_APP_PASSWORD="env-pass"),
            ):
                config = self.resolve(target, module, "--env-file", str(env_file))
                self.assertEqual(
                    (config.user, config.app_password), ("env-user", "env-pass")
                )
                self.assertEqual(config.base_url, "https://file.example.test")

    def test_missing_credentials_exit_with_varlock_hint(self):
        for target, module in TARGETS:
            with (
                self.subTest(target=target),
                process_env(),
                refuse_file_reads(),
                mock.patch.object(sys, "argv", [target]),
                self.assertRaises(SystemExit) as caught,
            ):
                module.main()
            self.assertIn("make varlock-run", str(caught.exception.code))

    def test_makefile_targets_pass_env_file_only_when_set(self):
        makefile = (REPO_ROOT / "Makefile").read_text(encoding="utf-8")
        for target, _ in TARGETS:
            with self.subTest(target=target):
                recipe = re.search(
                    rf"^{re.escape(target)}:.*?(?=^\S)", makefile, re.M | re.S
                ).group(0)
                self.assertNotIn("notion-to-wp/.env", recipe)
                self.assertIn('$${ENV_FILE:+--env-file "$$ENV_FILE"}', recipe)


if __name__ == "__main__":
    unittest.main()
