import argparse
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import visual_baseline  # noqa: E402


class VisualBaselinePruneTests(unittest.TestCase):
    def test_keep_two_preserves_newest_complete_diff_pair(self):
        runs = [
            ("20260811T033217Z", "candidate", "2026-08-11T03:32:17+00:00"),
            ("20260817T044333Z", "baseline", "2026-08-17T04:43:33+00:00"),
            ("20260817T044445Z", "baseline", "2026-08-17T04:44:45+00:00"),
            ("20260817T044820Z", "candidate", "2026-08-17T04:48:20+00:00"),
            ("20260817T045150Z", "candidate", "2026-08-17T04:51:50+00:00"),
        ]

        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            artifact_root = repo_root / "docs/current-state/reports/visual-baseline"
            artifact_root.mkdir(parents=True)
            for run_id, kind, created_at in runs:
                run_dir = artifact_root / run_id
                run_dir.mkdir()
                (run_dir / "capture.png").write_bytes(b"png")
                (artifact_root / f"manifest-{run_id}.json").write_text(
                    json.dumps(
                        {"run_id": run_id, "kind": kind, "created_at": created_at}
                    ),
                    encoding="utf-8",
                )
            for baseline_run, candidate_run, created_at in (
                (
                    "20260817T044333Z",
                    "20260817T044820Z",
                    "2026-08-17T04:50:51+00:00",
                ),
                (
                    "20260817T044445Z",
                    "20260817T045150Z",
                    "2026-08-17T04:54:20+00:00",
                ),
            ):
                (artifact_root / f"diff-{candidate_run}.json").write_text(
                    json.dumps(
                        {
                            "baseline_run": baseline_run,
                            "candidate_run": candidate_run,
                            "created_at": created_at,
                        }
                    ),
                    encoding="utf-8",
                )

            previous_repo_root = visual_baseline.REPO_ROOT
            previous_artifact_root = visual_baseline.ARTIFACT_ROOT
            visual_baseline.REPO_ROOT = repo_root
            visual_baseline.ARTIFACT_ROOT = artifact_root
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    visual_baseline.cmd_prune(argparse.Namespace(keep=2))
            finally:
                visual_baseline.REPO_ROOT = previous_repo_root
                visual_baseline.ARTIFACT_ROOT = previous_artifact_root

            remaining = {path.name for path in artifact_root.iterdir() if path.is_dir()}

        self.assertEqual(
            remaining,
            {"20260817T044445Z", "20260817T045150Z"},
        )

    def test_dry_run_reports_victims_without_deleting_capture_dirs(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            artifact_root = repo_root / "docs/current-state/reports/visual-baseline"
            artifact_root.mkdir(parents=True)
            for run_id, kind, created_at in (
                ("20260811T033217Z", "candidate", "2026-08-11T03:32:17+00:00"),
                ("20260817T044445Z", "baseline", "2026-08-17T04:44:45+00:00"),
                ("20260817T045150Z", "candidate", "2026-08-17T04:51:50+00:00"),
            ):
                run_dir = artifact_root / run_id
                run_dir.mkdir()
                (run_dir / "capture.png").write_bytes(b"png")
                (artifact_root / f"manifest-{run_id}.json").write_text(
                    json.dumps(
                        {"run_id": run_id, "kind": kind, "created_at": created_at}
                    ),
                    encoding="utf-8",
                )
            (artifact_root / "diff-20260817T045150Z.json").write_text(
                json.dumps(
                    {
                        "baseline_run": "20260817T044445Z",
                        "candidate_run": "20260817T045150Z",
                        "created_at": "2026-08-17T04:54:20+00:00",
                    }
                ),
                encoding="utf-8",
            )

            output = io.StringIO()
            with (
                mock.patch.object(visual_baseline, "REPO_ROOT", repo_root),
                mock.patch.object(visual_baseline, "ARTIFACT_ROOT", artifact_root),
                contextlib.redirect_stdout(output),
            ):
                visual_baseline.cmd_prune(
                    argparse.Namespace(keep=2, dry_run=True)
                )

            remaining = {path.name for path in artifact_root.iterdir() if path.is_dir()}

        self.assertEqual(
            remaining,
            {"20260811T033217Z", "20260817T044445Z", "20260817T045150Z"},
        )
        self.assertIn("would remove", output.getvalue())


if __name__ == "__main__":
    unittest.main()
