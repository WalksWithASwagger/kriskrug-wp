import contextlib
import importlib.util
import io
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def load_script(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    module = importlib.util.module_from_spec(spec)
    scripts_dir = str(ROOT / "scripts")
    sys.modules[name] = module
    sys.path.insert(0, scripts_dir)
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.remove(scripts_dir)
    return module


class MachineLocalDefaultsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gsc_audit = load_script("gsc_404_audit", "gsc-404-audit.py")
        cls.og_deploy = load_script("og_snippet_deploy", "og_snippet_deploy.py")

    def test_gsc_audit_requires_explicit_csv(self):
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as error:
                self.gsc_audit.main([])

        self.assertEqual(error.exception.code, 2)

    def test_gsc_audit_accepts_explicit_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "Table.csv"
            csv_path.write_text(
                "URL,Last crawled\nhttps://kriskrug.co/quote-request/,2026-07-01\n",
                encoding="utf-8",
            )
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                result = self.gsc_audit.main(["--csv", str(csv_path)])

        self.assertEqual(result, 0)
        self.assertIn("URLs audited: 1", output.getvalue())

    def test_og_deploy_env_path_is_repo_relative(self):
        self.assertEqual(
            self.og_deploy.ENV_PATH,
            ROOT / "scripts" / "notion-to-wp" / ".env",
        )


if __name__ == "__main__":
    unittest.main()
