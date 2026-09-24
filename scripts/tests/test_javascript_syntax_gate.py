"""Regression for `make javascript-syntax` exit status (#1037).

The recipe used to report only the last file's `node --check` status, so a
broken earlier file still passed. Uses temporary files only.
"""

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
VALID = "const ok = 1;\nconsole.log(ok);\n"
INVALID = "const = ;\n"


@unittest.skipUnless(
    shutil.which("make") and shutil.which("node"), "make and node are required"
)
class JavascriptSyntaxGateTests(unittest.TestCase):
    def _run(self, contents: list[str]) -> subprocess.CompletedProcess:
        with tempfile.TemporaryDirectory() as tmp:
            files = []
            for i, body in enumerate(contents):
                path = Path(tmp) / f"f{i}.js"
                path.write_text(body, encoding="utf-8")
                files.append(str(path))
            return subprocess.run(
                [
                    "make",
                    "--no-print-directory",
                    "-C",
                    str(REPO_ROOT),
                    "javascript-syntax",
                    f"JAVASCRIPT_FILES={' '.join(files)}",
                ],
                capture_output=True,
                text=True,
                timeout=120,
            )

    def test_invalid_first_file_fails(self):
        result = self._run([INVALID, VALID])
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("SyntaxError", result.stderr)

    def test_invalid_middle_file_fails(self):
        result = self._run([VALID, INVALID, VALID])
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_invalid_last_file_fails(self):
        result = self._run([VALID, INVALID])
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_all_valid_passes_and_runs_harness(self):
        result = self._run([VALID, VALID])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
