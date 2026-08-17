import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import docs_truth_check  # noqa: E402


class EphemeralMorningTruthGuidanceTests(unittest.TestCase):
    def test_active_guidance_rejects_routine_report_commit_flow(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            work_plan = repo_root / "docs/current-state/WORK-PLAN-2026-08-17.md"
            work_plan.parent.mkdir(parents=True)
            work_plan.write_text(
                "1. `make morning-truth` while online.\n"
                "2. Commit the fresh report.\n",
                encoding="utf-8",
            )

            findings = docs_truth_check.scan_file(repo_root, work_plan)

        self.assertTrue(
            any("morning-truth-checkpoint" in finding.message for finding in findings)
        )

    def test_active_guidance_rejects_commit_first_routine_report_flow(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            master_plan = repo_root / "docs/current-state/MASTER-PLAN-2026-07-30.md"
            master_plan.parent.mkdir(parents=True)
            master_plan.write_text(
                "- Commit fresh `make morning-truth` report\n",
                encoding="utf-8",
            )

            findings = docs_truth_check.scan_file(repo_root, master_plan)

        self.assertTrue(
            any("morning-truth-checkpoint" in finding.message for finding in findings)
        )

    def test_active_guidance_allows_ephemeral_and_checkpoint_modes(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            readme = repo_root / "docs/current-state/README.md"
            readme.parent.mkdir(parents=True)
            readme.write_text(
                "Run `make status-readonly` for routine startup.\n"
                "Use `make morning-truth` only for an ignored local copy.\n"
                "Use `make morning-truth-checkpoint` and commit it for a durable handoff.\n",
                encoding="utf-8",
            )

            findings = docs_truth_check.scan_file(repo_root, readme)

        self.assertFalse(
            any("morning-truth-checkpoint" in finding.message for finding in findings)
        )

    def test_active_guidance_allows_negated_commit_safety_language(self):
        samples = [
            "Use `make morning-truth` for an ignored local copy; do not commit it.\n",
            "Do not commit output from `make morning-truth`; it is ephemeral.\n",
        ]

        for sample in samples:
            with self.subTest(sample=sample), tempfile.TemporaryDirectory() as tmp:
                repo_root = Path(tmp)
                readme = repo_root / "docs/current-state/README.md"
                readme.parent.mkdir(parents=True)
                readme.write_text(sample, encoding="utf-8")

                findings = docs_truth_check.scan_file(repo_root, readme)

            self.assertFalse(
                any("morning-truth-checkpoint" in finding.message for finding in findings)
            )


if __name__ == "__main__":
    unittest.main()
