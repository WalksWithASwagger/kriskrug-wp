#!/usr/bin/env python3
"""Read-only parity check: tracked page payloads vs live WordPress content.raw (#1222).

For every page in the canonical content-architecture maps, GET the live page
with context=edit, run the deploy's slug/ID/status check, normalize both sides
the way scripts/content_architecture_deploy.py does, and compare SHA-256.
It prints IDs, slugs, hashes and a verdict, never page content.

GET requests only; it never writes to WordPress and writes no files unless
--json PATH is given. context=edit needs credentials, so run it through Varlock:

    make varlock-run CMD='make payload-parity'

Exit codes:
    0  every page matches (drift without --fail-on-drift also exits 0)
    1  drift found and --fail-on-drift was given
    2  could not verify: missing credentials, unreadable map, HTTP error,
       or a page that failed the slug/ID/status check
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError

from common import REPO_ROOT, WPClient
from content_architecture_deploy import (
    PACK_DIR,
    PAYLOAD_DIR,
    describe_verdict,
    load_page_map,
    parity_verdict,
    read_payload,
    repo_path,
    verify_target,
)

DEFAULT_MAPS = (
    PAYLOAD_DIR / "page-map.json",
    PAYLOAD_DIR / "topic-hubs" / "page-map.json",
)
SUPERSEDED_PACK = PACK_DIR / "issue-480-retire-inline-css"
PAGE_FIELDS = "id,slug,status,modified,content"
VARLOCK_HINT = "make varlock-run CMD='make payload-parity'"
NOT_COVERED = (
    "publications 1895 (scripts/deploy_publications_tearsheet.py)",
    "events 2250 (scripts/deploy_events_page.py)",
)


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT.resolve()))
    except ValueError:
        return str(path)


EXCLUDED_NOTE = (
    f"{rel(SUPERSEDED_PACK)}/ (superseded #480 pack; never checked under "
    "page-map.json or page-map.superseded.json, see #1223)"
)


def is_superseded(map_path: Path) -> bool:
    return SUPERSEDED_PACK.resolve() in map_path.resolve().parents


def payload_commit_date(path: Path) -> str:
    result = subprocess.run(
        ["git", "log", "-1", "--format=%cI", "--", str(path)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode:
        return "unknown"
    return result.stdout.strip() or "uncommitted"


def describe_error(exc: Exception) -> str:
    if isinstance(exc, HTTPError):
        return f"HTTP {exc.code} {exc.reason}"
    return f"{type(exc).__name__}: {exc}"


def is_auth_failure(exc: Exception) -> bool:
    # WPClient raises RuntimeError only when the login-mode handshake fails.
    return isinstance(exc, RuntimeError) or (
        isinstance(exc, HTTPError) and exc.code in (401, 403)
    )


def check_page(
    wp: Any,
    map_path: Path,
    page_key: str,
    page: dict[str, Any],
    commit_date: Callable[[Path], str],
) -> dict[str, Any]:
    payload_path = map_path.parent / page["payload"]
    row: dict[str, Any] = {
        "page": page_key,
        "map": rel(map_path),
        "id": page["id"],
        "slug": page["slug"],
        "payload": rel(payload_path),
        "payload_last_commit": commit_date(payload_path),
        "live_modified": None,
    }
    try:
        payload = read_payload(page, map_path.parent)
        live = wp.get(
            f"pages/{page['id']}",
            params={"context": "edit", "_fields": PAGE_FIELDS},
        )
    except (OSError, ValueError, RuntimeError) as exc:
        return {
            **row,
            "verdict": "ERROR",
            "error": describe_error(exc),
            "auth_failed": is_auth_failure(exc),
        }
    row["live_modified"] = live.get("modified")
    try:
        verify_target(live, page)
    except RuntimeError as exc:
        return {**row, "verdict": "ERROR", "error": f"target check failed: {exc}"}
    raw = (live.get("content") or {}).get("raw")
    if not isinstance(raw, str):
        return {
            **row,
            "verdict": "ERROR",
            "error": "no content.raw in response; needs an authenticated context=edit read",
        }
    return {**row, **parity_verdict(raw, payload)}


def check_pages(
    wp: Any,
    maps: list[tuple[Path, dict[str, dict[str, Any]]]],
    commit_date: Callable[[Path], str],
) -> tuple[list[dict[str, Any]], bool]:
    """Return (rows, stopped). Stops at the first auth failure so a bad
    credential is not retried against every page."""
    rows: list[dict[str, Any]] = []
    for map_path, page_map in maps:
        for page_key, page in page_map.items():
            row = check_page(wp, map_path, page_key, page, commit_date)
            auth_failed = row.pop("auth_failed", False)
            rows.append(row)
            if auth_failed:
                return rows, True
    return rows, False


def result_text(row: dict[str, Any]) -> str:
    if row["verdict"] == "ERROR":
        return f"ERROR {row['error']}"
    return describe_verdict(row)


def render_table(rows: list[dict[str, Any]]) -> str:
    header = ("page", "id", "slug", "live_modified", "payload_last_commit", "result")
    body = [
        (
            row["page"],
            str(row["id"]),
            row["slug"],
            row["live_modified"] or "-",
            row["payload_last_commit"],
            result_text(row),
        )
        for row in rows
    ]
    widths = [max(len(line[i]) for line in [header, *body]) for i in range(5)]
    lines = []
    for line in [header, *body]:
        cells = [cell.ljust(width) for cell, width in zip(line[:5], widths)]
        lines.append("  ".join([*cells, line[5]]).rstrip())
    return "\n".join(lines)


def summarize(
    rows: list[dict[str, Any]], expected: int, stopped: bool
) -> dict[str, Any]:
    counts = {
        verdict: sum(1 for row in rows if row["verdict"] == verdict)
        for verdict in ("match", "DRIFT", "ERROR")
    }
    return {
        "expected": expected,
        "checked": len(rows),
        "match": counts["match"],
        "drift": counts["DRIFT"],
        "error": counts["ERROR"],
        "stopped_after_auth_failure": stopped,
    }


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read-only live-vs-repo parity check for mapped page payloads."
    )
    parser.add_argument(
        "--map",
        action="append",
        default=[],
        help="Page map JSON (repo-relative or absolute); repeatable. "
        "Default: the two canonical wp-payloads maps.",
    )
    parser.add_argument(
        "--json",
        nargs="?",
        const="-",
        metavar="PATH",
        help="Machine output. Bare --json prints JSON instead of the table; "
        "--json PATH writes it to PATH.",
    )
    parser.add_argument(
        "--fail-on-drift", action="store_true", help="Exit 1 when any page drifts."
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    requested = [repo_path(value) for value in args.map] or list(DEFAULT_MAPS)
    for path in requested:
        if is_superseded(path):
            print(f"excluded --map {rel(path)}: {EXCLUDED_NOTE}", file=sys.stderr)
    active = [path for path in requested if not is_superseded(path)]
    if not active:
        print("error: no active page map to check", file=sys.stderr)
        return 2
    try:
        maps = [(path, load_page_map(path)) for path in active]
    except (OSError, ValueError) as exc:
        print(f"error: cannot read page map: {describe_error(exc)}", file=sys.stderr)
        return 2
    try:
        wp = WPClient.from_env()
    except (RuntimeError, ValueError) as exc:
        print(
            f"error: cannot verify without WordPress credentials ({exc}); run: {VARLOCK_HINT}",
            file=sys.stderr,
        )
        return 2

    rows, stopped = check_pages(wp, maps, payload_commit_date)
    summary = summarize(rows, sum(len(page_map) for _, page_map in maps), stopped)
    report = {
        "maps": [rel(path) for path in active],
        "excluded": [EXCLUDED_NOTE],
        "not_covered": list(NOT_COVERED),
        "pages": rows,
        "summary": summary,
    }

    if args.json == "-":
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print("Page payload parity (read-only: live content.raw vs tracked payload)")
        print(f"maps: {', '.join(report['maps'])}")
        print(f"excluded: {EXCLUDED_NOTE}")
        print(f"not covered: {'; '.join(NOT_COVERED)}")
        print()
        print(render_table(rows))
        print()
        if stopped:
            print(
                "stopped after an authentication failure; remaining pages not checked"
            )
        print(
            "summary: "
            + " ".join(
                f"{key}={value}"
                for key, value in summary.items()
                if key != "stopped_after_auth_failure"
            )
        )
        if args.json:
            Path(args.json).write_text(
                json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            print(f"json: {args.json}")

    if summary["error"] or stopped:
        return 2
    if summary["drift"] and args.fail_on_drift:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
