import contextlib
import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import check_large_files  # noqa: E402


SIX_MB = 6 * 1024 * 1024
HUNDRED_KB = 100 * 1024


class LargeFileCheckTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        self._git("init", "-b", "main")
        self._git("config", "user.name", "Test User")
        self._git("config", "user.email", "test@example.com")
        self._write("README.md", b"base\n")
        self._write("all-in-2026/existing.mov", b"\0" * SIX_MB)
        self._write("content/old.jpg", b"old image")
        self._commit("base")
        self._git("switch", "-c", "feature")

    def tearDown(self):
        self._tmp.cleanup()

    def test_new_six_mb_jpg_fails(self):
        self._write("content/drafts/post/hero.jpg", b"\xff" * SIX_MB)
        self._commit("add hero")

        violations = self._violations()

        self.assertEqual(
            violations,
            [
                check_large_files.Violation(
                    "content/drafts/post/hero.jpg", SIX_MB, "over the 5 MB limit"
                )
            ],
        )

    def test_six_mb_file_fails_even_inside_the_media_allowlist(self):
        self._write("theme/kk-aurora/assets/img/huge.webp", b"\1" * SIX_MB)
        self._commit("add huge theme image")

        self.assertEqual(
            [v.reason for v in self._violations()], ["over the 5 MB limit"]
        )

    def test_large_non_media_file_fails(self):
        self._write("docs/dump.json", b"{" + b" " * SIX_MB + b"}")
        self._commit("add dump")

        self.assertEqual([v.path for v in self._violations()], ["docs/dump.json"])

    def test_small_svg_in_the_allowlist_passes(self):
        self._write(
            "theme/kk-aurora/assets/icons/mark.svg", b"<svg/>" * (HUNDRED_KB // 6)
        )
        self._commit("add theme icon")

        self.assertEqual(self._violations(), [])

    def test_small_media_outside_the_allowlist_fails(self):
        self._write("content/drafts/post/diagram.SVG", b"<svg/>" * (HUNDRED_KB // 6))
        self._commit("add draft diagram")

        self.assertEqual(
            [(v.path, v.reason) for v in self._violations()],
            [("content/drafts/post/diagram.SVG", "media outside the allowlist")],
        )

    def test_small_non_media_file_passes(self):
        self._write("scripts/new_tool.py", b"print('hi')\n")
        self._commit("add tool")

        self.assertEqual(self._violations(), [])

    def test_deleted_large_file_does_not_fail(self):
        self._git("rm", "-q", "all-in-2026/existing.mov")
        self._commit("remove video")

        self.assertEqual(self._violations(), [])

    def test_existing_large_file_on_base_is_not_flagged(self):
        self._write("README.md", b"edited\n")
        self._commit("unrelated edit")

        self.assertEqual(self._violations(), [])

    def test_moving_an_existing_large_file_is_not_flagged(self):
        (self.repo / "archive").mkdir()
        self._git("mv", "all-in-2026/existing.mov", "archive/existing.mov")
        self._commit("move video")

        self.assertEqual(self._violations(), [])

    def test_growing_an_existing_file_past_the_limit_fails(self):
        self._write("content/old.jpg", b"\2" * SIX_MB)
        self._commit("replace image")

        self.assertEqual([v.path for v in self._violations()], ["content/old.jpg"])

    def test_branch_behind_main_is_not_blamed_for_main_changes(self):
        # Diffing against main's tip would show content/old.jpg reverting to
        # the base blob, which is not in main's tree any more.
        self._write("README.md", b"feature edit\n")
        self._commit("feature edit")
        self._git("switch", "-q", "main")
        self._write("content/old.jpg", b"main replaced the image")
        self._commit("main moves on")
        self._git("switch", "-q", "feature")

        self.assertEqual(self._violations("main"), [])

    def test_report_prints_path_and_size_and_fails(self):
        violations = [
            check_large_files.Violation("a/b.mov", SIX_MB, "over the 5 MB limit")
        ]
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            status = check_large_files.report(violations, "origin/main")

        self.assertEqual(status, 1)
        self.assertIn("  a/b.mov  6.0 MB  over the 5 MB limit", out.getvalue())

    def test_report_passes_when_clean(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(check_large_files.report([], "origin/main"), 0)

    def _violations(self, base_ref="main"):
        return check_large_files.find_violations(self.repo, base_ref)

    def _write(self, relative, data):
        path = self.repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def _commit(self, message):
        self._git("add", "-A")
        self._git("commit", "-q", "-m", message)

    def _git(self, *args):
        return subprocess.run(
            ["git", *args],
            cwd=self.repo,
            check=True,
            capture_output=True,
            text=True,
        )


if __name__ == "__main__":
    unittest.main()
