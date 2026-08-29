import contextlib
import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import ruff_changed  # noqa: E402


class ChangedPythonFilesTests(unittest.TestCase):
    def test_selects_only_added_modified_and_renamed_python_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self._git(repo, "init", "-b", "main")
            self._git(repo, "config", "user.name", "Test User")
            self._git(repo, "config", "user.email", "test@example.com")

            (repo / "changed.py").write_text("VALUE = 1\n", encoding="utf-8")
            (repo / "deleted.py").write_text("VALUE = 1\n", encoding="utf-8")
            (repo / "renamed.py").write_text("VALUE = 1\n", encoding="utf-8")
            (repo / "notes.md").write_text("before\n", encoding="utf-8")
            self._git(repo, "add", ".")
            self._git(repo, "commit", "-m", "base")
            base = self._git(repo, "rev-parse", "HEAD").stdout.strip()

            (repo / "changed.py").write_text("VALUE = 2\n", encoding="utf-8")
            (repo / "deleted.py").unlink()
            self._git(repo, "mv", "renamed.py", "moved.py")
            (repo / "new file.py").write_text("VALUE = 1\n", encoding="utf-8")
            (repo / "notes.md").write_text("after\n", encoding="utf-8")
            self._git(repo, "add", "-A")
            self._git(repo, "commit", "-m", "change")

            files = ruff_changed.changed_python_files(repo, base, "HEAD")

        self.assertEqual(files, ["changed.py", "moved.py", "new file.py"])

    def test_run_ruff_preserves_each_filename_as_one_argument(self):
        completed = subprocess.CompletedProcess([], 0)

        with mock.patch.object(ruff_changed.subprocess, "run", return_value=completed) as run:
            with contextlib.redirect_stdout(io.StringIO()):
                result = ruff_changed.run_ruff(
                    Path("/repo"), ["changed.py", "new file.py"], "ruff"
                )

        self.assertEqual(result, 0)
        run.assert_called_once_with(
            [
                "ruff",
                "check",
                "--isolated",
                "--select",
                "E4,E7,E9,F",
                "--",
                "changed.py",
                "new file.py",
            ],
            cwd=Path("/repo"),
            check=False,
        )

    def test_canonical_requirements_make_and_ci_wire_the_changed_file_gate(self):
        repo_root = Path(__file__).resolve().parents[2]
        requirements = (repo_root / "requirements-test.txt").read_text(encoding="utf-8")
        makefile = (repo_root / "Makefile").read_text(encoding="utf-8")
        workflow = (repo_root / ".github/workflows/test-pr.yml").read_text(
            encoding="utf-8"
        )
        python_job = workflow.split("  python-tests:", 1)[1].split(
            "  # CSS regression ratchet", 1
        )[0]

        self.assertIn("ruff>=0.15.16", requirements)
        self.assertIn("ruff-changed", makefile.splitlines()[3])
        self.assertIn("ruff-changed:", makefile)
        self.assertIn("scripts/ruff_changed.py --base-ref", makefile)
        self.assertIn("fetch-depth: 0", python_job)
        self.assertIn("Check changed Python files with Ruff", python_job)
        self.assertIn(
            'python scripts/ruff_changed.py --base-ref "refs/remotes/origin/${BASE_BRANCH}"',
            python_job,
        )

    @staticmethod
    def _git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *args],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        )


if __name__ == "__main__":
    unittest.main()
