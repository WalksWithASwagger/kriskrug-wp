"""Static safety contract for the production-adjacent issue #706 runbook."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNBOOK = (ROOT / "fixes/issue-706-script-diet.md").read_text(encoding="utf-8")


def section(start: str, end: str) -> str:
    return RUNBOOK.split(start, 1)[1].split(end, 1)[0]


class ScriptDietRunbookTests(unittest.TestCase):
    def test_snapshot_command_fails_closed_and_creates_private_valid_json(self):
        snapshot = section("# Full Code Snippets snapshot", "PSI baseline")

        self.assertIn("mkdir -p", snapshot)
        self.assertIn("umask 077", snapshot)
        self.assertIn("curl --fail-with-body --silent --show-error", snapshot)
        self.assertIn(".tmp", snapshot)
        self.assertIn("jq -e", snapshot)
        self.assertIn("chmod 600", snapshot)
        self.assertIn('ln "$tmp_path" "$snapshot_path"', snapshot)

    def test_pixel_lives_in_wpcode_not_code_snippets(self):
        self.assertIn("WPCode Lite", RUNBOOK)
        self.assertIn("insert-headers-and-footers/ihaf", RUNBOOK)
        self.assertIn("Do not invent one", RUNBOOK)
        self.assertIn("### 2. Remove the pixel, then purge", RUNBOOK)
        self.assertNotIn("### 2. Deactivate the pixel", RUNBOOK)
        pixel_write = section(
            "### 2. Remove the pixel, then purge", "### 3. Install the gtag delay"
        )
        self.assertNotIn("code-snippets/v1/snippets", pixel_write)
        self.assertIn("WPCode", pixel_write)

    def test_varlock_injected_credentials_are_expanded_inside_child_shell(self):
        snapshot = section("# Full Code Snippets snapshot", "PSI baseline")
        self.assertIn("varlock run --inject vars -- sh -eu -c", snapshot)
        self.assertNotIn("varlock run --inject vars -- curl", snapshot)
        self.assertNotIn("'$WP_USER", snapshot)

    def test_idle_timing_contract_is_explicit(self):
        self.assertIn("no earlier than 3 seconds after `load`", RUNBOOK)
        self.assertIn("one-second ceiling", RUNBOOK)


if __name__ == "__main__":
    unittest.main()
