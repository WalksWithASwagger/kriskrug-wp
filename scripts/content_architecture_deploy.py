#!/usr/bin/env python3
"""Snapshot-gated WordPress page deploy for the content architecture source pack."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
import urllib.request
from pathlib import Path
from typing import Any

from common import REPO_ROOT, WPClient


PACK_DIR = REPO_ROOT / "content/source-packs/content-architecture-2026"
PAYLOAD_DIR = PACK_DIR / "wp-payloads"
PAGE_MAP_PATH = PAYLOAD_DIR / "page-map.json"
SNAPSHOT_FIELDS = "id,slug,status,title,content,excerpt,meta,modified,link"


def load_page_map() -> dict[str, dict[str, Any]]:
    return json.loads(PAGE_MAP_PATH.read_text(encoding="utf-8"))


def read_payload(page: dict[str, Any]) -> str:
    return (PAYLOAD_DIR / page["payload"]).read_text(encoding="utf-8").strip() + "\n"


def safe_name(value: str) -> str:
    return re.sub(r"[^a-z0-9-]+", "-", value.lower()).strip("-")


def fetch_public_html(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "kriskrug-content-architecture/1.0"})
    with urllib.request.urlopen(req, timeout=40) as resp:
        return resp.read().decode("utf-8", errors="replace")


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def verify_target(actual: dict[str, Any], expected: dict[str, Any]) -> None:
    failures = []
    for field in ("id", "slug"):
        if actual.get(field) != expected[field]:
            failures.append(f"{field}: expected {expected[field]!r}, got {actual.get(field)!r}")
    if actual.get("status") != "publish":
        failures.append(f"status: expected 'publish', got {actual.get('status')!r}")
    if failures:
        raise RuntimeError("; ".join(failures))


def verify_markers(raw: str, markers: list[str]) -> list[str]:
    return [marker for marker in markers if marker not in raw]


def snapshot_page(
    wp: WPClient,
    page_key: str,
    page: dict[str, Any],
    snapshot_dir: Path,
    suffix: str,
) -> dict[str, str]:
    slug = safe_name(page["slug"])
    page_json = wp.get(
        f"pages/{page['id']}",
        params={"context": "edit", "_fields": SNAPSHOT_FIELDS},
    )
    verify_target(page_json, page)
    public_html = fetch_public_html(page["url"])

    json_path = snapshot_dir / f"page-{page['id']}-{slug}-{suffix}.json"
    html_path = snapshot_dir / f"page-{page['id']}-{slug}-{suffix}.html"
    write_json(json_path, page_json)
    write_text(html_path, public_html)
    return {
        "page": page_key,
        "json": str(json_path.relative_to(REPO_ROOT)),
        "html": str(html_path.relative_to(REPO_ROOT)),
        "json_sha256": sha256_text(json.dumps(page_json, sort_keys=True, ensure_ascii=False)),
        "html_sha256": sha256_text(public_html),
    }


def write_sha_file(snapshot_dir: Path, records: list[dict[str, str]]) -> None:
    lines = []
    for record in records:
        lines.append(f"{record['json_sha256']}  {record['json']}")
        lines.append(f"{record['html_sha256']}  {record['html']}")
    write_text(snapshot_dir / "sha256sums.txt", "\n".join(lines).rstrip() + "\n")


def selected_page_items(page_map: dict[str, dict[str, Any]], names: list[str]) -> list[tuple[str, dict[str, Any]]]:
    if not names:
        return list(page_map.items())
    unknown = [name for name in names if name not in page_map]
    if unknown:
        raise SystemExit(f"Unknown page key(s): {', '.join(unknown)}")
    return [(name, page_map[name]) for name in names]


def restore_page(wp: WPClient, page_key: str, page: dict[str, Any], snapshot_dir: Path) -> None:
    slug = safe_name(page["slug"])
    snapshot_path = snapshot_dir / f"page-{page['id']}-{slug}-before.json"
    if not snapshot_path.exists():
        raise SystemExit(f"Missing snapshot: {snapshot_path}")
    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    verify_target(snapshot, page)
    raw = snapshot.get("content", {}).get("raw", "")
    if not raw:
        raise SystemExit(f"Snapshot has no content.raw: {snapshot_path}")
    wp.post(f"pages/{page['id']}", {"content": raw})
    readback = wp.get(f"pages/{page['id']}", params={"context": "edit", "_fields": SNAPSHOT_FIELDS})
    verify_target(readback, page)
    print(f"restored {page_key} page_id={page['id']} from {snapshot_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true", help="Apply payloads to live WordPress.")
    parser.add_argument("--page", action="append", default=[], help="Page key from page-map.json; repeatable.")
    parser.add_argument("--snapshot-dir", default="", help="Override snapshot output directory.")
    parser.add_argument("--restore", action="store_true", help="Restore selected page(s) from --snapshot-dir before snapshots.")
    args = parser.parse_args()

    page_map = load_page_map()
    items = selected_page_items(page_map, args.page)
    wp = WPClient.from_env()

    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    snapshot_dir = (
        Path(args.snapshot_dir)
        if args.snapshot_dir
        else REPO_ROOT / "backup" / f"{ts}-content-architecture" / "page-snapshots"
    )
    if not snapshot_dir.is_absolute():
        snapshot_dir = REPO_ROOT / snapshot_dir

    if args.restore:
        if not args.snapshot_dir:
            raise SystemExit("--restore requires --snapshot-dir")
        for page_key, page in items:
            restore_page(wp, page_key, page, snapshot_dir)
        return

    records: list[dict[str, str]] = []
    report: dict[str, Any] = {"snapshot_dir": str(snapshot_dir.relative_to(REPO_ROOT)), "pages": []}

    for page_key, page in items:
        payload = read_payload(page)
        current = wp.get(
            f"pages/{page['id']}",
            params={"context": "edit", "_fields": SNAPSHOT_FIELDS},
        )
        verify_target(current, page)
        payload_missing = verify_markers(payload, page["markers"])
        if payload_missing:
            raise SystemExit(f"{page_key} payload missing markers: {payload_missing}")

        print(f"target ok: {page_key} id={page['id']} slug={page['slug']} payload={page['payload']}")
        if not args.execute:
            report["pages"].append({"page": page_key, "id": page["id"], "action": "dry-run"})
            continue

        before = snapshot_page(wp, page_key, page, snapshot_dir, "before")
        records.append(before)

        wp.post(f"pages/{page['id']}", {"content": payload})
        readback = wp.get(
            f"pages/{page['id']}",
            params={"context": "edit", "_fields": SNAPSHOT_FIELDS},
        )
        verify_target(readback, page)
        raw = readback.get("content", {}).get("raw", "")
        missing = verify_markers(raw, page["markers"])
        if missing:
            restore_page(wp, page_key, page, snapshot_dir)
            raise SystemExit(f"{page_key} readback missing markers after write; restored: {missing}")

        after = snapshot_page(wp, page_key, page, snapshot_dir, "after")
        records.append(after)
        report["pages"].append(
            {
                "page": page_key,
                "id": page["id"],
                "slug": page["slug"],
                "url": page["url"],
                "payload": page["payload"],
                "before": before,
                "after": after,
                "modified": readback.get("modified"),
            }
        )
        print(f"updated: {page_key} id={page['id']} url={page['url']}")

    if args.execute:
        write_sha_file(snapshot_dir, records)
        report_path = snapshot_dir.parent / "deploy-report.json"
        write_json(report_path, report)
        print(f"snapshot_dir={snapshot_dir.relative_to(REPO_ROOT)}")
        print(f"deploy_report={report_path.relative_to(REPO_ROOT)}")
    else:
        print(f"[dry-run] planned pages={len(items)}; no snapshots or writes created")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise
