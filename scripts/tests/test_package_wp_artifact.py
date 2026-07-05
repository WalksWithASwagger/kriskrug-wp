import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import package_wp_artifact as package  # noqa: E402


class PackageWpArtifactTests(unittest.TestCase):
    def test_theme_version_requires_matching_cache_bust_define(self):
        style = "/*\nTheme Name: Demo\nVersion: 1.2.3\n*/"
        functions = "<?php\ndefine('KK_AURORA_VERSION', '1.2.4');\n"

        with self.assertRaisesRegex(ValueError, "does not match"):
            package.theme_version_from_files(style, functions)

    def test_plugin_version_reads_root_plugin_header(self):
        version, notes = package.plugin_version_from_files(
            "demo-plugin",
            {
                "demo-plugin.php": "<?php\n/**\n * Plugin Name: Demo Plugin\n * Version: 0.3.0\n */\n",
            },
        )

        self.assertEqual(version, "0.3.0")
        self.assertEqual(notes, [])

    def test_zip_directory_uses_slug_root_and_skips_local_cruft(self):
        with tempfile.TemporaryDirectory() as tempdir:
            temp = Path(tempdir)
            source = temp / "theme"
            source.mkdir()
            (source / "style.css").write_text("/*\nTheme Name: Demo\nVersion: 1.2.3\n*/", encoding="utf-8")
            (source / "functions.php").write_text("<?php\ndefine('KK_AURORA_VERSION', '1.2.3');\n", encoding="utf-8")
            (source / ".DS_Store").write_text("cruft", encoding="utf-8")
            (source / "__pycache__").mkdir()
            (source / "__pycache__" / "x.pyc").write_bytes(b"cruft")
            destination = temp / "demo.zip"

            package.zip_directory(source, destination, "demo-theme")

            with zipfile.ZipFile(destination) as archive:
                self.assertEqual(archive.testzip(), None)
                self.assertIn("demo-theme/style.css", archive.namelist())
                self.assertIn("demo-theme/functions.php", archive.namelist())
                self.assertNotIn("demo-theme/.DS_Store", archive.namelist())
                self.assertNotIn("demo-theme/__pycache__/x.pyc", archive.namelist())

    def test_main_refuses_dirty_source_without_override(self):
        with mock.patch.object(package, "parse_args") as parse_args, \
             mock.patch.object(package, "ensure_clean_source", side_effect=SystemExit("dirty")), \
             tempfile.TemporaryDirectory() as tempdir:
            source = Path(tempdir) / "kk-aurora"
            source.mkdir()
            parse_args.return_value = mock.Mock(
                source=str(source),
                kind="theme",
                slug="kk-aurora",
                label="release",
                output_dir=tempdir,
                date="20260705",
                base_url="https://example.com",
                rollback_ref="",
                rollback_label="rollback",
                allow_dirty=False,
                copy_path=False,
                open_admin=False,
                report="",
            )
            with mock.patch.object(package, "REPO_ROOT", Path(tempdir)):
                with self.assertRaises(SystemExit):
                    package.main()


if __name__ == "__main__":
    unittest.main()
