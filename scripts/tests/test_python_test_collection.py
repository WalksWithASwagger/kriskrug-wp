"""Guard for #1216: `make python-test` must collect every Python test directory.

`unittest discover` never collected module-level pytest functions, and a tests
directory outside every discovery path never ran at all, so a failing test sat
behind a green CI check. Every suite now runs through pytest, which collects
both styles. This fails when a tracked `scripts/**/tests/` directory is not
passed to pytest by the `python-test` recipe.
"""

import re
import subprocess
import unittest
from pathlib import Path, PurePosixPath

REPO_ROOT = Path(__file__).resolve().parents[2]


def tracked_test_dirs() -> set[str]:
    listing = subprocess.run(
        ["git", "ls-files", "--", "scripts"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    dirs = set()
    for name in listing.splitlines():
        path = PurePosixPath(name)
        if (
            path.parent.name == "tests"
            and path.name.startswith("test_")
            and path.suffix == ".py"
        ):
            dirs.add(str(path.parent))
    return dirs


def python_test_pytest_targets() -> set[str]:
    makefile = (REPO_ROOT / "Makefile").read_text(encoding="utf-8")
    recipe = re.search(r"^python-test:.*\n((?:\t.*\n)+)", makefile, re.MULTILINE)
    assert recipe, "Makefile has no python-test recipe"
    targets = set()
    for line in recipe.group(1).splitlines():
        command = re.search(r"-m pytest\s+(.*)", line)
        if command:
            targets.update(
                arg.rstrip("/")
                for arg in command.group(1).split()
                if not arg.startswith("-")
            )
    return targets


class PythonTestCollectionTests(unittest.TestCase):
    def test_finds_the_known_suites(self):
        self.assertIn("scripts/tests", tracked_test_dirs())
        self.assertIn("scripts/photo-library/tests", tracked_test_dirs())

    def test_every_tracked_tests_dir_is_collected_by_pytest(self):
        missing = sorted(tracked_test_dirs() - python_test_pytest_targets())
        self.assertEqual(
            missing,
            [],
            "Add these to the pytest commands in the Makefile python-test recipe",
        )


if __name__ == "__main__":
    unittest.main()
