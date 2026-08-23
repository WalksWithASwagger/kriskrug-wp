#!/usr/bin/env python3
"""One-shot environment check for agents landing in this repo.

Answers the four questions every session opens with: can I authenticate to
WordPress, is the Python toolchain usable, can I talk to GitHub, and is the
working tree safe to commit into. Read-only. Never prints a secret value.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

OK, WARN, FAIL = "ok", "warn", "fail"
MARK = {OK: "PASS", WARN: "WARN", FAIL: "FAIL"}


def run(cmd: list[str], timeout: int = 20) -> tuple[int, str]:
    try:
        p = subprocess.run(
            cmd, cwd=REPO_ROOT, capture_output=True, text=True, timeout=timeout
        )
        return p.returncode, (p.stdout or p.stderr).strip()
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as exc:
        return 1, str(exc)


def check_wp_credentials() -> tuple[str, str]:
    try:
        from common import wp_process_credentials
    except Exception as exc:
        return FAIL, f"cannot import scripts/common.py: {exc}"
    user, password = wp_process_credentials()
    if user and password:
        return OK, f"resolved (user length {len(user)}; never printed)"
    env_file = REPO_ROOT / "scripts/notion-to-wp/.env"
    if env_file.exists():
        return WARN, f"not in process env; {env_file.name} exists and may supply them"
    return FAIL, (
        "unresolved. Run through Varlock: make varlock-run CMD='...'. "
        "Accepts WP_USER/WP_APP_PASSWORD or WP_API_USERNAME/WP_API_PASSWORD."
    )


def check_varlock() -> tuple[str, str]:
    if not shutil.which("varlock"):
        return WARN, "not on PATH; credential-free targets still work"
    code, _ = run(["varlock", "load", "--agent"], timeout=30)
    return (OK, "installed; schema resolves") if code == 0 else (
        WARN, "installed but schema did not fully resolve (see: make env-check)"
    )


def check_venv() -> tuple[str, str]:
    venv = REPO_ROOT / "scripts/notion-to-wp/.venv/bin/python"
    if not venv.exists():
        return FAIL, "missing scripts/notion-to-wp/.venv (5 Makefile targets call it directly)"
    code, out = run([str(venv), "--version"])
    return (OK, out) if code == 0 else (FAIL, f"present but not runnable: {out}")


def check_gh() -> tuple[str, str]:
    if not shutil.which("gh"):
        return FAIL, "gh CLI not installed"
    code, out = run(["gh", "auth", "status"], timeout=25)
    if code != 0:
        return FAIL, "gh not authenticated"
    m = re.search(r"Logged in to \S+ account (\S+)", out)
    if m:
        return OK, f"authenticated as {m.group(1)}"
    return OK, "authenticated"


def check_git_tree() -> tuple[str, str]:
    code, out = run(["git", "status", "--porcelain"])
    if code != 0:
        return FAIL, "not a git repo"
    branch_code, branch = run(["git", "branch", "--show-current"])
    dirty = len([l for l in out.splitlines() if l.strip()])
    label = f"on {branch or 'DETACHED'}"
    if dirty:
        return WARN, f"{label}; {dirty} uncommitted change(s)"
    return OK, f"{label}; clean"


def check_worktrees() -> tuple[str, str]:
    code, out = run(["git", "worktree", "list"])
    if code != 0:
        return WARN, "could not list worktrees"
    extra = [l for l in out.splitlines() if "/.worktrees/" in l]
    if not extra:
        return OK, "no extra worktrees"
    return WARN, f"{len(extra)} extra worktree(s); other sessions may be live here"


def check_live_site() -> tuple[str, str]:
    code, out = run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
         "https://kriskrug.co/wp-content/themes/kk-aurora/style.css"], timeout=25)
    if code != 0 or out != "200":
        return WARN, f"live style.css readback returned {out or 'no response'}"
    return OK, "live style.css reachable (authoritative for theme version)"


CHECKS = [
    ("WordPress credentials", check_wp_credentials),
    ("Varlock", check_varlock),
    ("Python venv", check_venv),
    ("GitHub CLI", check_gh),
    ("Git working tree", check_git_tree),
    ("Worktrees", check_worktrees),
    ("Live site", check_live_site),
]


def main() -> int:
    print("kriskrug-wp doctor\n")
    worst = OK
    order = {OK: 0, WARN: 1, FAIL: 2}
    for name, fn in CHECKS:
        try:
            status, detail = fn()
        except Exception as exc:
            status, detail = FAIL, f"check raised: {exc}"
        if order[status] > order[worst]:
            worst = status
        print(f"  [{MARK[status]}] {name:22} {detail}")
    print()
    if worst == FAIL:
        print("Result: FAIL. Fix the items above before authenticated or write work.")
        return 1
    if worst == WARN:
        print("Result: OK with warnings. Read-only work is safe.")
        return 0
    print("Result: OK. Everything this repo needs is working.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
