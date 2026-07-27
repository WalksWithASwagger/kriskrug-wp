#!/usr/bin/env python3
"""Guard against repo-vs-live Aurora theme version drift (issue #546).

The repo's #1 risk is the live `kk-aurora` theme silently diverging from the
version tracked in `main`. This detector fetches the live theme `style.css`,
parses its `Version:` header, compares it against the repo's declared version,
and exits non-zero on mismatch so the drift is caught the moment it opens.

Read-only: it makes a single GET request and never writes anything.

Usage:
    python3 scripts/check_live_theme_parity.py            # check live vs repo
    python3 scripts/check_live_theme_parity.py --base URL # check another host

Exit codes:
    0  versions match, OR live is unreachable (soft skip / graceful degrade)
    1  live and repo versions differ (drift detected)
    2  could not read repo version, or live returned a bad/empty style.css
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_BASE = "https://kriskrug.co"
THEME_STYLE_PATH = "/wp-content/themes/kk-aurora/style.css"
REPO_STYLE_CSS = (
    Path(__file__).resolve().parents[1] / "theme" / "kk-aurora" / "style.css"
)

VERSION_RE = re.compile(r"^\s*Version:\s*(.+?)\s*$", re.MULTILINE)


def parse_version(style_css: str) -> str | None:
    """Return the value of the `Version:` header from a WP style.css block."""
    match = VERSION_RE.search(style_css)
    return match.group(1) if match else None


def read_repo_version(path: Path = REPO_STYLE_CSS) -> str | None:
    try:
        return parse_version(path.read_text(encoding="utf-8"))
    except OSError:
        return None


def fetch_live_style(base: str, timeout: int = 12) -> tuple[int, str]:
    """GET the live theme style.css. status 0 signals unreachable/offline."""
    url = base.rstrip("/") + THEME_STYLE_PATH
    req = Request(url, headers={"User-Agent": "kk-theme-parity/1.0"})
    try:
        with urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except HTTPError as exc:
        return exc.code, ""
    except (URLError, TimeoutError, OSError) as exc:
        return 0, str(exc)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default=DEFAULT_BASE, help="site base URL")
    parser.add_argument("--timeout", type=int, default=12, help="HTTP timeout (s)")
    args = parser.parse_args()
    base = args.base.rstrip("/")

    repo_version = read_repo_version()
    if repo_version is None:
        print(f"ERROR could not read repo Version from {REPO_STYLE_CSS}")
        return 2

    status, body = fetch_live_style(base, timeout=args.timeout)

    # Graceful degrade: live unreachable/offline is a soft skip, not a crash.
    if status == 0:
        print(f"WARN live theme unreachable ({base}{THEME_STYLE_PATH}): {body}")
        print(f"SKIP parity check (repo declares Version: {repo_version})")
        return 0

    if status != 200:
        print(f"ERROR live {base}{THEME_STYLE_PATH} -> HTTP {status}")
        return 2

    live_version = parse_version(body)
    if live_version is None:
        print(
            f"ERROR live style.css has no parseable Version: header ({base}{THEME_STYLE_PATH})"
        )
        return 2

    if live_version != repo_version:
        print(
            "FAIL theme version drift detected:\n"
            f"  live ({base}{THEME_STYLE_PATH}): {live_version}\n"
            f"  repo (theme/kk-aurora/style.css): {repo_version}"
        )
        return 1

    print(f"PASS live and repo agree on Version: {live_version}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
