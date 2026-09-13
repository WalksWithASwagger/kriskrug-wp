#!/usr/bin/env python3
"""Deploy the generated /events/ artifact to WP page 2250.

Snapshot-first and dry-run by default. Content-only write: title, slug, status,
template, featured media and meta are never sent. Reads the page back after the
write and restores from the snapshot if the readback does not match.

    python3 scripts/deploy_events_page.py              # dry-run, writes a snapshot
    python3 scripts/deploy_events_page.py --execute    # live write to page 2250
    python3 scripts/deploy_events_page.py --restore <snapshot.json>
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import REPO_ROOT, WPClient  # noqa: E402

PAGE_ID = 2250
EXPECTED = {"id": PAGE_ID, "slug": "events", "type": "page", "status": "publish"}
ARTIFACT = REPO_ROOT / "scripts/events_page/out/events-2250.generated.html"
BACKUP_DIR = REPO_ROOT / "backup/page-snapshots"
FIELDS = "id,slug,status,type,title,modified_gmt,content,template,featured_media"

# A preview-local artifact carries relative paths that are not public URLs.
FORBIDDEN = ("file://", "/Users/", 'src=""', 'src="heroes/', "_pending", "#media-")


class DeployError(RuntimeError):
    pass


def guard_artifact(html: str) -> None:
    for bad in FORBIDDEN:
        if bad in html:
            raise DeployError(f"artifact contains {bad!r}; refusing to deploy")
    for required in ('data-events-grid="sheet"', 'data-events-grid="upcoming"', "kk-ev-record-grid"):
        if required not in html:
            raise DeployError(f"artifact is missing {required!r}; wrong file?")


def check_identity(page: dict) -> None:
    for key, value in EXPECTED.items():
        if page.get(key) != value:
            raise DeployError(f"page {key}={page.get(key)!r}, expected {value!r}")
    if not isinstance(page.get("content", {}).get("raw"), str):
        raise DeployError("authenticated content.raw required; check credentials")


def snapshot(page: dict) -> Path:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = BACKUP_DIR / f"page-{PAGE_ID}-events-{stamp}.json"
    path.write_text(json.dumps(page, indent=1), encoding="utf-8")
    return path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--execute", action="store_true", help="send the live write")
    ap.add_argument("--restore", type=Path, help="restore content from a snapshot file")
    args = ap.parse_args()

    wp = WPClient.from_env()

    if args.restore:
        saved = json.loads(args.restore.read_text(encoding="utf-8"))
        if saved.get("id") != PAGE_ID:
            raise DeployError(f"snapshot is for page {saved.get('id')}, not {PAGE_ID}")
        wp.post(f"/pages/{PAGE_ID}", {"content": saved["content"]["raw"]})
        print(f"restored page {PAGE_ID} from {args.restore}")
        return 0

    html = ARTIFACT.read_text(encoding="utf-8")
    guard_artifact(html)

    page = wp.get(f"/pages/{PAGE_ID}?context=edit&_fields={FIELDS}")
    check_identity(page)
    before = page["content"]["raw"]

    snap = snapshot(page)
    print(f"page          : {PAGE_ID} /{page['slug']}/ status={page['status']}")
    print(f"modified_gmt  : {page['modified_gmt']}")
    print(f"snapshot      : {snap}")
    print(f"artifact      : {ARTIFACT.name} ({len(html)} bytes, was {len(before)})")

    if before == html:
        print("page already matches the artifact; nothing to do")
        return 0
    if not args.execute:
        print("DRY-RUN. No write sent. Re-run with --execute to deploy.")
        return 0

    wp.post(f"/pages/{PAGE_ID}", {"content": html})

    after = wp.get(f"/pages/{PAGE_ID}?context=edit&_fields={FIELDS}")
    if after["content"]["raw"] != html:
        print("READBACK MISMATCH. Restoring from snapshot.", file=sys.stderr)
        wp.post(f"/pages/{PAGE_ID}", {"content": before})
        raise DeployError(f"write did not round-trip; restored. snapshot: {snap}")

    print(f"deployed. readback matches. rollback: --restore {snap}")
    print("Next: purge the Pagely page cache and verify /events/ logged out.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except DeployError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
