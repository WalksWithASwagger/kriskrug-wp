#!/usr/bin/env python3
"""Deploy the generated /events/ artifact to WP page 2250.

Snapshot-first and dry-run by default. Content-only write: title, slug, status,
template, featured media and meta are never sent. Reads the page back after the
write. On a readback mismatch it only auto-restores when the stored content is
exactly WordPress's own filtered version of our write; any other difference is
treated as a possible concurrent edit and left alone for a human (#1035).

    python3 scripts/deploy_events_page.py              # dry-run, writes a snapshot
    python3 scripts/deploy_events_page.py --execute    # live write to page 2250

Restore is preview-first and refuses to overwrite edits it has not seen:

    python3 scripts/deploy_events_page.py --restore <snapshot.json>
        # preview: verifies identity, prints the live content sha256, no write
    python3 scripts/deploy_events_page.py --restore <snapshot.json> --execute \
        --expect-current-sha256 <sha256 printed by the preview>
        # live: aborts if the page changed since the preview, snapshots the
        # current page first, then verifies the restored content exactly
"""

from __future__ import annotations

import argparse
import hashlib
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
    for required in (
        'data-events-grid="sheet"',
        'data-events-grid="upcoming"',
        "kk-ev-record-grid",
    ):
        if required not in html:
            raise DeployError(f"artifact is missing {required!r}; wrong file?")


def check_identity(page: dict) -> None:
    for key, value in EXPECTED.items():
        if page.get(key) != value:
            raise DeployError(f"page {key}={page.get(key)!r}, expected {value!r}")
    if not isinstance(page.get("content", {}).get("raw"), str):
        raise DeployError("authenticated content.raw required; check credentials")


def snapshot(page: dict, label: str = "") -> Path:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    suffix = f"-{label}" if label else ""
    path = BACKUP_DIR / f"page-{PAGE_ID}-events-{stamp}{suffix}.json"
    path.write_text(json.dumps(page, indent=1), encoding="utf-8")
    return path


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_snapshot(path: Path) -> str:
    """Validate a snapshot's structure and identity; return its content.raw."""
    try:
        saved = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise DeployError(f"cannot read snapshot {path}: {exc}") from exc
    if not isinstance(saved, dict):
        raise DeployError(f"snapshot {path} is not a page object")
    for key, value in EXPECTED.items():
        # id and slug are mandatory; older snapshots may omit type/status,
        # but a present value must still match.
        if key in ("type", "status") and saved.get(key) is None:
            continue
        if saved.get(key) != value:
            raise DeployError(
                f"snapshot {key}={saved.get(key)!r}, expected {value!r}; wrong file?"
            )
    raw = (saved.get("content") or {}).get("raw")
    if not isinstance(raw, str) or not raw.strip():
        raise DeployError(f"snapshot {path} has no content.raw to restore")
    return raw


def fetch(wp: WPClient) -> dict:
    return wp.get(f"/pages/{PAGE_ID}?context=edit&_fields={FIELDS}")


def restore(wp: WPClient, path: Path, execute: bool, expect_sha: str | None) -> int:
    target = load_snapshot(path)
    page = fetch(wp)
    check_identity(page)
    current = page["content"]["raw"]
    current_sha = sha256(current)
    print(f"page          : {PAGE_ID} /{page['slug']}/ status={page['status']}")
    print(f"modified_gmt  : {page['modified_gmt']}")
    print(f"live sha256   : {current_sha} ({len(current)} bytes)")
    print(f"snapshot      : {path} sha256={sha256(target)} ({len(target)} bytes)")

    if current == target:
        print("page already matches the snapshot; nothing to do")
        return 0
    if not execute:
        print("RESTORE PREVIEW. No write sent. To restore exactly this state run:")
        print(f"  --restore {path} --execute --expect-current-sha256 {current_sha}")
        return 0
    if not expect_sha:
        raise DeployError(
            "live restore needs --expect-current-sha256 from a preview run"
        )
    if expect_sha != current_sha:
        raise DeployError(
            "page content changed since the preview "
            f"(expected {expect_sha}, live {current_sha}); re-run the preview"
        )

    pre = snapshot(page, "pre-restore")
    print(f"pre-restore   : {pre}")
    wp.post(f"/pages/{PAGE_ID}", {"content": target})
    after = fetch(wp)
    if after.get("content", {}).get("raw") != target:
        raise DeployError(
            f"restore readback does not match the snapshot; no further write "
            f"sent. pre-restore snapshot: {pre}"
        )
    print(f"restored page {PAGE_ID} from {path}; readback matches")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--execute", action="store_true", help="send the live write")
    ap.add_argument(
        "--restore", type=Path, help="preview (or with --execute, run) a restore"
    )
    ap.add_argument(
        "--expect-current-sha256",
        help="live content sha256 from the restore preview; required to restore",
    )
    args = ap.parse_args()

    if args.restore:
        load_snapshot(args.restore)  # fail on a bad file before any request
        wp = WPClient.from_env()
        return restore(wp, args.restore, args.execute, args.expect_current_sha256)

    wp = WPClient.from_env()

    html = ARTIFACT.read_text(encoding="utf-8")
    guard_artifact(html)

    page = fetch(wp)
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

    try:
        resp = wp.post(f"/pages/{PAGE_ID}", {"content": html})
    except Exception as exc:
        raise DeployError(
            f"write outcome unknown ({exc}); no retry sent. Preview a restore "
            f"to inspect the live page: --restore {snap}"
        ) from exc

    try:
        after = fetch(wp)
    except Exception as exc:
        raise DeployError(
            f"write sent but readback failed ({exc}); no restore attempted. "
            f"Preview: --restore {snap}"
        ) from exc
    stored = after.get("content", {}).get("raw")
    if stored != html:
        written = resp.get("content", {}).get("raw") if isinstance(resp, dict) else None
        if isinstance(written, str) and stored == written:
            # Content is exactly what WordPress stored for our own write
            # (filtered), so restoring cannot clobber anyone else's edit.
            print(
                "READBACK MISMATCH: WordPress filtered the artifact. Restoring.",
                file=sys.stderr,
            )
            wp.post(f"/pages/{PAGE_ID}", {"content": before})
            check = fetch(wp).get("content", {}).get("raw")
            state = "restored" if check == before else "RESTORE DID NOT VERIFY"
            raise DeployError(
                f"artifact was filtered by WordPress; {state}. snapshot: {snap}"
            )
        raise DeployError(
            "readback differs from both the artifact and WordPress's write "
            "response: possible concurrent edit. No restore sent. Preview: "
            f"--restore {snap}"
        )

    print(f"deployed. readback matches. rollback: --restore {snap}")
    print("Next: purge the Pagely page cache and verify /events/ logged out.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except DeployError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
