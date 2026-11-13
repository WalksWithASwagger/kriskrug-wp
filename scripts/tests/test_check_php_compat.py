import contextlib
import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import check_php_compat  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[2]


class RequiresPhpTests(unittest.TestCase):
    def test_reads_theme_stylesheet_header(self):
        text = "/*\nTheme Name: Aurora\nRequires at least: 6.4\nRequires PHP: 8.0\n*/\n"
        self.assertEqual(check_php_compat.requires_php(text), "8.0")

    def test_reads_plugin_docblock_header(self):
        text = "<?php\n/**\n * Plugin Name: Board\n * Requires PHP:      7.4\n */\n"
        self.assertEqual(check_php_compat.requires_php(text), "7.4")

    def test_no_header_is_none(self):
        self.assertIsNone(check_php_compat.requires_php("<?php\n// helper\n"))


class ComponentsTests(unittest.TestCase):
    def test_finds_theme_and_plugins_that_declare_a_floor(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write(root / "theme/aurora/style.css", "Requires PHP: 8.0\n")
            self._write(root / "plugins/board/board.php", " * Requires PHP: 7.4\n")
            self._write(root / "plugins/board/helpers.php", "<?php\n")
            self._write(root / "plugins/loose/loose.php", "<?php\n")

            found = check_php_compat.components(root)

        self.assertEqual(
            [(path.relative_to(root).as_posix(), version) for path, version in found],
            [("theme/aurora", "8.0"), ("plugins/board", "7.4")],
        )

    def test_repository_headers_are_all_found(self):
        found = {
            path.relative_to(REPO_ROOT).as_posix(): version
            for path, version in check_php_compat.components(REPO_ROOT)
        }

        self.assertEqual(
            set(found),
            {
                "theme/kk-aurora",
                "plugins/kk-marquee-board",
                "plugins/kk-practice",
                "plugins/kk-sidebar-promos",
            },
        )
        for version in found.values():
            self.assertRegex(version, r"^\d+\.\d+$")

    def _write(self, path, text):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


class CheckTests(unittest.TestCase):
    def test_each_component_is_checked_at_its_own_floor(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "theme/aurora").mkdir(parents=True)
            (root / "theme/aurora/style.css").write_text("Requires PHP: 8.0\n")
            (root / "plugins/board").mkdir(parents=True)
            (root / "plugins/board/board.php").write_text(" * Requires PHP: 7.4\n")

            status, calls, output = self._run_check(root, returncodes=[0, 0])

        self.assertEqual(status, 0)
        floors = [(call[-1], call[call.index("testVersion") + 1]) for call in calls]
        self.assertEqual(floors, [("theme/aurora", "8.0-"), ("plugins/board", "7.4-")])
        self.assertIn("ok   plugins/board (Requires PHP 7.4)", output)

    def test_a_component_below_its_floor_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "plugins/board").mkdir(parents=True)
            (root / "plugins/board/board.php").write_text(" * Requires PHP: 7.4\n")

            status, _, output = self._run_check(root, returncodes=[1])

        self.assertEqual(status, 1)
        self.assertIn("FAIL plugins/board (Requires PHP 7.4)", output)

    def test_no_headers_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            status, calls, _ = self._run_check(Path(tmp), returncodes=[])

        self.assertEqual(status, 1)
        self.assertEqual(calls, [])

    def _run_check(self, root, returncodes):
        results = iter(subprocess.CompletedProcess([], code) for code in returncodes)
        out = io.StringIO()
        with (
            mock.patch.object(check_php_compat.shutil, "which", return_value="phpcs"),
            mock.patch.object(
                check_php_compat.subprocess,
                "run",
                side_effect=lambda *a, **k: next(results),
            ) as run,
            contextlib.redirect_stdout(out),
        ):
            status = check_php_compat.check(root, "phpcs")
        return status, [call.args[0] for call in run.call_args_list], out.getvalue()


if __name__ == "__main__":
    unittest.main()
