import os
import subprocess
from pathlib import Path

import pytest


MAKEFILE = Path(__file__).resolve().parents[2] / "Makefile"


@pytest.mark.parametrize(
    ("target", "switches"),
    [
        ("seo-backfill", {"EXECUTE": "--execute"}),
        ("wp-package", {"OPEN_ADMIN": "--open-admin", "COPY_PATH": "--copy-path", "ALLOW_DIRTY": "--allow-dirty"}),
        ("public-image-audit", {"DEFAULT_URLS": "--default-urls", "CHECK_URLS": "--check-urls"}),
        ("css-coverage", {"RECORD": "--record"}),
    ],
)
@pytest.mark.parametrize("value", [None, "0", "false", "1 extra", "1"])
def test_operational_flags_require_explicit_one(tmp_path, target, switches, value):
    # Capture the arguments without loading credentials or running the underlying tool.
    capture = tmp_path / "python3"
    capture.write_text('#!/bin/sh\nprintf "%s\\n" "$@"\n')
    capture.chmod(0o755)
    interpreter = tmp_path / "scripts/notion-to-wp/.venv/bin/python"
    interpreter.parent.mkdir(parents=True)
    interpreter.symlink_to(capture)

    env = {key: val for key, val in os.environ.items() if key not in switches}
    env["PATH"] = os.pathsep.join([str(tmp_path), env["PATH"]])
    settings = [f"{name}={value}" for name in switches] if value is not None else []
    result = subprocess.run(
        ["make", "-s", "-f", str(MAKEFILE), target, "PYTHON=python3", *settings],
        cwd=tmp_path, env=env, check=True, capture_output=True, text=True,
    )
    args = result.stdout.splitlines()
    assert args[0].startswith("scripts/")
    for flag in switches.values():
        assert (flag in args) == (value == "1")
