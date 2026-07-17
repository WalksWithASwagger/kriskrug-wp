"""Offline contract tests for scripts/mcp-wordpress-remote.sh (issue #378).

Static checks parse the launcher text; behavioral checks run it with stub
binaries and throwaway HOME/PATH. Nothing here invokes the real npx, varlock,
or WordPress, and no network action can occur.
"""

import re
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LAUNCHER = ROOT / "scripts" / "mcp-wordpress-remote.sh"

# Reviewed pin. Bump together with MCP_WP_REMOTE_VERSION in the launcher
# (upgrade procedure documented in the launcher header).
PINNED_VERSION = "0.3.5"
PINNED_PACKAGE = f"@automattic/mcp-wordpress-remote@{PINNED_VERSION}"

STUB_TEMPLATE = """#!/bin/bash
printf '%s\\n' "$@" > "$STUB_LOG_DIR/{name}.args"
env > "$STUB_LOG_DIR/{name}.env"
exit 0
"""


class LauncherStaticContract(unittest.TestCase):
    def setUp(self):
        self.text = LAUNCHER.read_text()

    def test_package_version_is_pinned_not_latest(self):
        self.assertNotIn("@latest", self.text)
        pins = re.findall(r'^MCP_WP_REMOTE_VERSION="([^"]+)"$', self.text, re.M)
        self.assertEqual(pins, [PINNED_VERSION])
        self.assertRegex(pins[0], r"^\d+\.\d+\.\d+$")
        self.assertIn(
            'MCP_WP_REMOTE_PKG="@automattic/mcp-wordpress-remote@${MCP_WP_REMOTE_VERSION}"',
            self.text,
        )

    def test_every_exec_path_uses_the_pinned_package(self):
        exec_lines = [
            line
            for line in self.text.splitlines()
            if re.match(r"\s*exec\s", line)
        ]
        self.assertEqual(len(exec_lines), 2)
        launch_blob = self.text[self.text.index("exec "):]
        self.assertEqual(launch_blob.count('"$MCP_WP_REMOTE_PKG"'), 2)

    def test_upgrade_procedure_is_documented(self):
        self.assertIn("Upgrade procedure", self.text)
        self.assertIn("npm view @automattic/mcp-wordpress-remote version", self.text)
        self.assertIn("test_mcp_wordpress_remote.py", self.text)

    def test_varlock_contract_takes_precedence_over_env_file(self):
        self.assertIn(
            'AGENTS_WP_ENV="${WP_MCP_AGENTS_ENV:-$HOME/.agents/env/wordpress}"',
            self.text,
        )
        self.assertIn(
            'ENV_FILE="${WP_MCP_ENV_FILE:-$SCRIPT_DIR/notion-to-wp/.env}"',
            self.text,
        )
        varlock_branch = self.text.index('[[ -f "$AGENTS_WP_ENV/.env.local" ]]')
        env_file_source = self.text.index('source "$ENV_FILE"')
        self.assertLess(varlock_branch, env_file_source)

    def test_ambient_credentials_are_scrubbed_before_varlock_injection(self):
        self.assertIn(
            "env -u WP_API_USERNAME -u WP_API_PASSWORD -u WP_USER -u WP_APP_PASSWORD",
            self.text,
        )

    def test_env_file_fallback_exports_sourced_values(self):
        self.assertRegex(
            self.text, r'set -a\n(?:# shellcheck[^\n]*\n)?source "\$ENV_FILE"\nset \+a'
        )

    def test_fails_closed_naming_both_missing_sources_without_values(self):
        self.assertIn('missing $ENV_FILE', self.text)
        self.assertIn('no $AGENTS_WP_ENV/.env.local', self.text)
        self.assertIn("set -euo pipefail", self.text)

    def test_no_hardcoded_credentials(self):
        for line in self.text.splitlines():
            match = re.search(
                r"(\w*(?:PASSWORD|SECRET|TOKEN|API_KEY)\w*)=(.*)", line
            )
            if match:
                value = match.group(2).strip()
                self.assertRegex(
                    value,
                    r'^"\$',
                    f"credential-looking assignment must expand a variable: {line!r}",
                )
        self.assertNotRegex(self.text, r"://[^/\s]+:[^/\s]+@")
        self.assertNotRegex(self.text, r"[A-Za-z0-9+/]{32,}")


class LauncherBehavior(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        base = Path(self.tmp.name)
        self.home = base / "home"
        self.stub_bin = base / "bin"
        self.stub_log = base / "log"
        self.agents_env = base / "agents-env"
        for d in (self.home, self.stub_bin, self.stub_log, self.agents_env):
            d.mkdir()

    def add_stub(self, name):
        stub = self.stub_bin / name
        stub.write_text(STUB_TEMPLATE.format(name=name))
        stub.chmod(0o755)
        return stub

    def run_launcher(self, env_file, extra_env=None):
        env = {
            "HOME": str(self.home),
            "PATH": f"{self.stub_bin}:/usr/bin:/bin",
            "STUB_LOG_DIR": str(self.stub_log),
            "WP_MCP_AGENTS_ENV": str(self.agents_env),
            "WP_MCP_ENV_FILE": str(env_file),
        }
        if extra_env:
            env.update(extra_env)
        return subprocess.run(
            ["/bin/bash", str(LAUNCHER)],
            env=env,
            capture_output=True,
            text=True,
            timeout=30,
        )

    def stub_args(self, name):
        return (self.stub_log / f"{name}.args").read_text().splitlines()

    def test_fails_closed_before_launch_when_no_credential_source_exists(self):
        self.add_stub("npx")
        missing_env = Path(self.tmp.name) / "does-not-exist.env"
        result = self.run_launcher(
            missing_env, extra_env={"WP_APP_PASSWORD": "ambient-sekrit-value"}
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn(str(missing_env), result.stderr)
        self.assertIn(f"{self.agents_env}/.env.local", result.stderr)
        self.assertNotIn("ambient-sekrit-value", result.stdout + result.stderr)
        self.assertFalse((self.stub_log / "npx.args").exists(), "npx must not launch")
        self.assertFalse((self.stub_log / "varlock.args").exists())

    def test_varlock_contract_wins_and_ambient_credentials_are_scrubbed(self):
        npx_stub = self.add_stub("npx")
        self.add_stub("varlock")
        (self.agents_env / ".env.local").write_text("# stub contract\n")
        env_file = Path(self.tmp.name) / "fallback.env"
        env_file.write_text("FALLBACK_MARKER=used\n")
        result = self.run_launcher(
            env_file, extra_env={"WP_APP_PASSWORD": "ambient-sekrit-value"}
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        args = self.stub_args("varlock")
        self.assertEqual(args[:4], ["run", "--path", str(self.agents_env), "--inject"])
        self.assertEqual(args[4:6], ["vars", "--"])
        self.assertEqual(args[6:], [str(npx_stub), "-y", PINNED_PACKAGE])
        varlock_env = (self.stub_log / "varlock.env").read_text()
        self.assertNotIn("ambient-sekrit-value", varlock_env)
        self.assertIn(
            f"LOG_FILE={self.home}/.agents/logs/mcp-wordpress.log", varlock_env
        )
        self.assertNotIn("FALLBACK_MARKER", varlock_env, ".env must not be sourced")
        self.assertFalse(
            (self.stub_log / "npx.args").exists(),
            "varlock stub owns the launch; npx must not run directly",
        )

    def test_env_file_fallback_exports_credentials_and_launches_pinned_package(self):
        self.add_stub("npx")
        env_file = Path(self.tmp.name) / "fallback.env"
        env_file.write_text("WP_USER=stub-user\nWP_APP_PASSWORD=stub-pass\n")
        result = self.run_launcher(env_file)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.stub_args("npx"), ["-y", PINNED_PACKAGE])
        npx_env = (self.stub_log / "npx.env").read_text()
        self.assertIn("WP_API_USERNAME=stub-user", npx_env)
        self.assertIn("WP_API_PASSWORD=stub-pass", npx_env)
        self.assertIn(
            "WP_API_URL=https://kriskrug.co/wp-json/mcp/mcp-adapter-default-server",
            npx_env,
        )
        self.assertIn(f"LOG_FILE={self.home}/.cursor/logs/mcp-wordpress.log", npx_env)
        self.assertFalse((self.stub_log / "varlock.args").exists())


if __name__ == "__main__":
    unittest.main()
