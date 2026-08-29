#!/usr/bin/env python3
"""Run Ruff only on Python files changed from a base ref."""

from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path


def changed_python_files(
    repo_root: Path, base_ref: str, head_ref: str = "HEAD"
) -> list[str]:
    result = subprocess.run(
        [
            "git",
            "diff",
            "--name-only",
            "--diff-filter=ACMR",
            "-z",
            f"{base_ref}...{head_ref}",
            "--",
            "*.py",
        ],
        cwd=repo_root,
        check=True,
        capture_output=True,
    )
    return sorted(os.fsdecode(path) for path in result.stdout.split(b"\0") if path)


def run_ruff(repo_root: Path, files: list[str], ruff: str = "ruff") -> int:
    if not files:
        print("ruff changed-file check: no Python files changed")
        return 0

    print("ruff changed-file check:", flush=True)
    for path in files:
        print(f"  {path}", flush=True)

    result = subprocess.run([ruff, "check", "--", *files], cwd=repo_root)
    return result.returncode


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-ref", required=True)
    parser.add_argument("--head-ref", default="HEAD")
    parser.add_argument("--ruff", default="ruff")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    files = changed_python_files(repo_root, args.base_ref, args.head_ref)
    return run_ruff(repo_root, files, args.ruff)


if __name__ == "__main__":
    raise SystemExit(main())
