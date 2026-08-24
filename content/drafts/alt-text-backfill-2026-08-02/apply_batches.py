#!/usr/bin/env python3
"""Apply the approved alt-text backfill batches for issue #4.

Two batches, applied separately, from inventory.csv in this directory:

  --batch media    Batch 0: media library ``alt_text`` writes. Selects every
                   violation row with ``fix_surface=media-library-alt_text``
                   that carries a ``proposed_alt`` string, dedupes by media ID.
                   Rows on that surface WITHOUT a drafted string are reported
                   as needs-review and never written (a script must not invent
                   alt text).
  --batch content  Batch 1: the 34 ``post-content-block`` rows across seven
                   site pages. Inserts each row's ``proposed_alt`` into the
                   empty ``alt=""`` of the matching image block in the page's
                   raw ``post_content``, then PATCHes the page.

Safety contract (docs/current-state/INCIDENT-2026-05-15-overwritten-post.md):

  * Default is DRY-RUN. Nothing is written without ``--apply``.
  * Every write is preceded by a live slug+ID verification: the target is
    fetched by ID and its slug/URL/file must match what inventory.csv says.
    Mismatch = the item is refused, never "fixed up".
  * Before any write the full live JSON record is snapshotted to a local
    gitignored directory (.generated/alt-text-backfill/<run>/).
  * An existing non-empty value that differs from the proposed string is a
    CONFLICT and is skipped, never overwritten.
  * Every write is read back and verified; a per-item report is printed and
    saved next to the snapshots.

Without WP_USER/WP_APP_PASSWORD the dry run still works read-only: it
verifies slug+ID and current live state over the public REST API and reports
exactly what an authenticated run would do (raw post_content diffs need auth,
so content-batch matching is then done against ``content.rendered``).

Usage:
  python3 apply_batches.py --batch media              # dry-run (default)
  python3 apply_batches.py --batch media --apply      # live writes
  python3 apply_batches.py --batch content            # dry-run
  python3 apply_batches.py --batch content --apply    # live writes
  python3 apply_batches.py --batch content --only-page-id 3899 --apply
  python3 apply_batches.py --batch content --restore <snapshot.json>
  python3 apply_batches.py --batch content --restore <snapshot.json> --apply
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import re
import stat
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from common import WPClient, load_env  # noqa: E402

CSV_PATH = HERE / "inventory.csv"
SNAPSHOT_ROOT = REPO_ROOT / ".generated" / "alt-text-backfill"
BASE_URL = "https://kriskrug.co"
USER_AGENT = "KrisKrugAltBackfill/1.0 (issue #4)"


# ---------------------------------------------------------------------------
# CSV selection


def load_rows() -> list[dict[str, str]]:
    with CSV_PATH.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def media_targets(rows: list[dict[str, str]]) -> tuple[list[dict], list[dict]]:
    """(apply-ready one-per-media targets, needs-review rows without a string)."""
    surface = [
        r
        for r in rows
        if r["fix_surface"] == "media-library-alt_text"
        and r["classification"].endswith("VIOLATION")
    ]
    ready_rows = [r for r in surface if r["proposed_alt"].strip()]
    needs_review = [r for r in surface if not r["proposed_alt"].strip()]
    by_media: dict[str, dict] = {}
    for r in ready_rows:
        mid = r["media_id"]
        prev = by_media.get(mid)
        if prev and prev["proposed_alt"] != r["proposed_alt"]:
            raise SystemExit(
                f"inventory.csv holds two different proposed strings for media {mid}"
            )
        by_media.setdefault(mid, r)
    return list(by_media.values()), needs_review


def content_targets(rows: list[dict[str, str]]) -> dict[str, list[dict]]:
    """Batch-1 rows grouped by page ID. All are pages (tier 2-page)."""
    batch1 = [r for r in rows if r["batch"] == "batch-1"]
    for r in batch1:
        if r["fix_surface"] != "post-content-block" or not r["proposed_alt"].strip():
            raise SystemExit(
                f"unexpected batch-1 row shape for media {r['media_id']} on "
                f"{r['page_url']} (fix_surface={r['fix_surface']!r})"
            )
    pages: dict[str, list[dict]] = {}
    for r in batch1:
        pages.setdefault(r["page_id"], []).append(r)
    return pages


# ---------------------------------------------------------------------------
# HTTP


def public_get(path: str) -> dict:
    url = path if path.startswith("http") else f"{BASE_URL}/wp-json/wp/v2/{path}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def make_client() -> WPClient | None:
    env = load_env()
    if (env.get("WP_USER") or "").strip() and (env.get("WP_APP_PASSWORD") or "").strip():
        return WPClient.from_env()
    return None


# ---------------------------------------------------------------------------
# Matching helpers


def file_stem(name_or_url: str) -> str:
    """Comparable stem: basename, query stripped, size/edit suffixes removed."""
    base = name_or_url.split("?")[0].rsplit("/", 1)[-1]
    stem = base.rsplit(".", 1)[0]
    stem = re.sub(r"-\d+x\d+$", "", stem)
    stem = re.sub(r"-e\d{10,}$", "", stem)
    stem = re.sub(r"-scaled$", "", stem)
    return stem.lower()


IMG_TAG_RE = re.compile(r"<img\b[^>]*/?>", re.IGNORECASE)


def tag_matches_media(tag: str, media_id: str, image_src: str) -> bool:
    if re.search(rf"\bwp-image-{re.escape(media_id)}\b", tag):
        return True
    src_m = re.search(r"""\bsrc\s*=\s*["']([^"']+)["']""", tag)
    return bool(src_m and file_stem(src_m.group(1)) == file_stem(image_src))


def tag_alt(tag: str) -> str | None:
    m = re.search(r"""\balt\s*=\s*(["'])(.*?)\1""", tag, re.DOTALL)
    return m.group(2) if m else None


def set_tag_alt(tag: str, alt: str) -> str:
    if '"' in alt:
        raise SystemExit(f"proposed alt contains a double quote, refusing: {alt!r}")
    if "<" in alt or ">" in alt:
        raise SystemExit(f"proposed alt contains HTML markup, refusing: {alt!r}")
    if re.search(r"""\balt\s*=\s*(["']).*?\1""", tag, re.DOTALL):
        return re.sub(
            r"""\balt\s*=\s*(["']).*?\1""", f'alt="{alt}"', tag, count=1, flags=re.DOTALL
        )
    return tag.replace("<img", f'<img alt="{alt}"', 1)


def apply_rows_to_html(
    html: str, page_rows: list[dict]
) -> tuple[str, list[dict]]:
    """Insert each row's proposed alt into its matching img tag(s).

    Returns (new_html, per-row results). A row that matches nothing, or whose
    matched tag carries a different non-empty alt, is reported and skipped.
    """
    results = []
    new_html = html
    for row in page_rows:
        proposed = row["proposed_alt"]
        matched = 0
        changed = 0
        already = 0
        conflict: str | None = None

        def repl(m: re.Match) -> str:
            nonlocal matched, changed, already, conflict
            tag = m.group(0)
            if not tag_matches_media(tag, row["media_id"], row["image_src"]):
                return tag
            matched += 1
            current = tag_alt(tag)
            if current == proposed:
                already += 1
                return tag
            if current not in (None, ""):
                conflict = current
                return tag
            changed += 1
            return set_tag_alt(tag, proposed)

        new_html = IMG_TAG_RE.sub(repl, new_html)
        if matched == 0:
            status = "no-match"
        elif conflict:
            status = "conflict"
        elif changed == 0:
            status = "already-applied"
        else:
            status = "would-change"
        results.append(
            {
                "media_id": row["media_id"],
                "image_file": row["image_file"],
                "proposed_alt": proposed,
                "tags_matched": matched,
                "tags_changed": changed,
                "tags_already_correct": already,
                "conflict_alt": conflict,
                "status": status,
            }
        )
    return new_html, results


# ---------------------------------------------------------------------------
# Snapshots + reporting


def snapshot(run_dir: Path, name: str, payload: dict) -> Path:
    run_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
    run_dir.chmod(0o700)
    path = run_dir / f"{name}.json"
    serialized = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
        handle.write(serialized)
        handle.flush()
        os.fsync(handle.fileno())
    path.chmod(0o600)
    if json.loads(path.read_text(encoding="utf-8")) != payload:
        raise RuntimeError(f"snapshot readback differs from source: {path}")
    return path


# ---------------------------------------------------------------------------
# Batch: media


def run_media(client: WPClient | None, apply: bool, run_dir: Path, only_id: str | None):
    targets, needs_review = media_targets(load_rows())
    if only_id:
        targets = [t for t in targets if t["media_id"] == only_id]
        if not targets:
            raise SystemExit(f"media {only_id!r} is not in the approved media batch")
    report = {
        "batch": "media (batch 0)",
        "mode": "APPLY" if apply else "DRY-RUN",
        "authenticated": client is not None,
        "apply_ready_media_ids": sorted(t["media_id"] for t in targets),
        "needs_review_rows_without_string": len(needs_review),
        "items": [],
    }
    for t in targets:
        mid = t["media_id"]
        item = {"media_id": mid, "proposed_alt": t["proposed_alt"]}
        live = public_get(f"media/{mid}")
        # slug+ID verification: right record, right file
        ok_id = str(live.get("id")) == mid
        ok_file = file_stem(live.get("source_url", "")) == file_stem(t["image_file"])
        item["verified_id"] = ok_id
        item["verified_file"] = ok_file
        item["live_alt_text"] = live.get("alt_text", "")
        if not (ok_id and ok_file):
            item["status"] = "REFUSED-identity-mismatch"
        elif live.get("alt_text") == t["proposed_alt"]:
            item["status"] = "already-applied"
        elif live.get("alt_text"):
            item["status"] = "CONFLICT-existing-different-alt"
        elif not apply:
            item["status"] = "would-write"
        else:
            assert client is not None
            snap = snapshot(run_dir, f"media-{mid}-before", live)
            item["snapshot"] = str(snap)
            client.post(f"media/{mid}", {"alt_text": t["proposed_alt"]})
            readback = public_get(f"media/{mid}")
            item["readback_alt_text"] = readback.get("alt_text", "")
            item["status"] = (
                "written-verified"
                if readback.get("alt_text") == t["proposed_alt"]
                else "WRITTEN-READBACK-MISMATCH"
            )
        report["items"].append(item)
    return report


# ---------------------------------------------------------------------------
# Batch: content


def run_content(
    client: WPClient | None, apply: bool, run_dir: Path, only_page: str | None
):
    pages = content_targets(load_rows())
    if only_page:
        pages = {k: v for k, v in pages.items() if k == only_page}
        if not pages:
            raise SystemExit(f"page {only_page!r} is not in the approved content batch")
    report = {
        "batch": "content (batch 1)",
        "mode": "APPLY" if apply else "DRY-RUN",
        "authenticated": client is not None,
        "pages": [],
    }
    for page_id, page_rows in sorted(pages.items(), key=lambda kv: int(kv[0])):
        expect_slug = page_rows[0]["page_slug"]
        expect_url = page_rows[0]["page_url"].rstrip("/")
        entry = {
            "page_id": page_id,
            "expected_slug": expect_slug,
            "page_url": page_rows[0]["page_url"],
            "rows": len(page_rows),
        }
        if client:
            live = client.get(f"pages/{page_id}", params={"context": "edit"})
            html = live.get("content", {}).get("raw", "")
            surface = "content.raw"
        else:
            live = public_get(f"pages/{page_id}")
            html = live.get("content", {}).get("rendered", "")
            surface = "content.rendered (unauthenticated fallback; apply needs raw)"
        live_slug = live.get("slug", "")
        live_link = (live.get("link") or "").rstrip("/")
        ok = (
            str(live.get("id")) == page_id
            and live_slug == expect_slug
            and live_link.endswith("/" + expect_slug)
            and live_link == expect_url
        )
        entry["verified_slug_id"] = ok
        entry["live_slug"] = live_slug
        entry["live_status"] = live.get("status", "")
        entry["match_surface"] = surface
        if not ok:
            entry["status"] = "REFUSED-slug-id-mismatch"
            report["pages"].append(entry)
            continue
        new_html, results = apply_rows_to_html(html, page_rows)
        entry["items"] = results
        changed = sum(r["tags_changed"] for r in results)
        blocked = [r for r in results if r["status"] in ("no-match", "conflict")]
        entry["tags_to_change"] = changed
        if blocked:
            entry["blocked_rows"] = len(blocked)
            entry["status"] = "REFUSED-blocked-rows"
        elif not apply:
            entry["status"] = "dry-run"
        elif client is None:
            entry["status"] = "REFUSED-apply-needs-credentials"
        elif changed == 0:
            entry["status"] = "no-op"
        else:
            snap = snapshot(run_dir, f"page-{page_id}-before", live)
            entry["snapshot"] = str(snap)
            client.post(f"pages/{page_id}", {"content": new_html})
            readback = client.get(f"pages/{page_id}", params={"context": "edit"})
            raw = readback.get("content", {}).get("raw", "")
            _, readback_results = apply_rows_to_html(raw, page_rows)
            missing = [
                r["media_id"]
                for r in readback_results
                if r["status"] != "already-applied"
            ]
            entry["readback_items"] = readback_results
            entry["readback_missing_media_ids"] = missing
            entry["status"] = "written-verified" if not missing else "WRITTEN-READBACK-MISSING"
        report["pages"].append(entry)
    return report


# ---------------------------------------------------------------------------


def run_restore(
    batch: str,
    source: Path,
    client: WPClient,
    apply: bool,
    run_dir: Path,
) -> dict:
    try:
        source = source.resolve(strict=True)
        source.relative_to(SNAPSHOT_ROOT.resolve())
    except (OSError, ValueError):
        raise SystemExit(
            f"restore source must be a file in the private generated snapshot directory: {SNAPSHOT_ROOT}"
        ) from None
    if not source.is_file() or stat.S_IMODE(source.stat().st_mode) & 0o077:
        raise SystemExit(f"restore source must be a private mode-0600 snapshot: {source}")

    saved = json.loads(source.read_text(encoding="utf-8"))
    saved_id = str(saved.get("id", ""))
    item = {"snapshot": str(source), "target_id": saved_id}

    if batch == "media":
        targets, _ = media_targets(load_rows())
        by_id = {row["media_id"]: row for row in targets}
        target = by_id.get(saved_id)
        if target is None:
            raise SystemExit(
                f"snapshot media {saved_id!r} is not in the approved media batch"
            )
        if file_stem(saved.get("source_url", "")) != file_stem(target["image_file"]):
            raise SystemExit(f"snapshot media {saved_id} file does not match inventory.csv")
        restore_value = saved.get("alt_text")
        if not isinstance(restore_value, str):
            raise SystemExit(f"snapshot media {saved_id} has no string alt_text")
        live = client.get(f"media/{saved_id}", params={"context": "edit"})
        if str(live.get("id")) != saved_id or file_stem(
            live.get("source_url", "")
        ) != file_stem(target["image_file"]):
            raise SystemExit(f"live media {saved_id} identity does not match inventory.csv")
        current_value = live.get("alt_text")
        expected_applied_value = target["proposed_alt"]
        endpoint = f"media/{saved_id}"
        payload = {"alt_text": restore_value}
        snapshot_name = f"media-{saved_id}-before-restore"
    else:
        pages = content_targets(load_rows())
        page_rows = pages.get(saved_id)
        if page_rows is None:
            raise SystemExit(
                f"snapshot page {saved_id!r} is not in the approved content batch"
            )
        expected_slug = page_rows[0]["page_slug"]
        expected_url = page_rows[0]["page_url"].rstrip("/")
        saved_link = (saved.get("link") or "").rstrip("/")
        if saved.get("slug") != expected_slug or saved_link != expected_url:
            raise SystemExit(f"snapshot page {saved_id} identity does not match inventory.csv")
        restore_value = saved.get("content", {}).get("raw")
        if not isinstance(restore_value, str):
            raise SystemExit(f"snapshot page {saved_id} has no content.raw")
        live = client.get(f"pages/{saved_id}", params={"context": "edit"})
        live_link = (live.get("link") or "").rstrip("/")
        if (
            str(live.get("id")) != saved_id
            or live.get("slug") != expected_slug
            or live_link != expected_url
        ):
            raise SystemExit(f"live page {saved_id} identity does not match inventory.csv")
        current_value = live.get("content", {}).get("raw")
        expected_applied_value, expected_results = apply_rows_to_html(
            restore_value, page_rows
        )
        if any(r["status"] in ("no-match", "conflict") for r in expected_results):
            raise SystemExit(
                f"snapshot page {saved_id} cannot reproduce the approved applied state"
            )
        endpoint = f"pages/{saved_id}"
        payload = {"content": restore_value}
        snapshot_name = f"page-{saved_id}-before-restore"

    if current_value == restore_value:
        item["status"] = "already-restored"
    elif current_value != expected_applied_value:
        raise SystemExit(
            f"live {batch} {saved_id} drifted from the expected applied state; refusing restore"
        )
    elif not apply:
        item["status"] = "would-restore"
    else:
        recovery = snapshot(run_dir, snapshot_name, live)
        item["pre_restore_snapshot"] = str(recovery)
        client.post(endpoint, payload)
        readback = client.get(endpoint, params={"context": "edit"})
        actual = (
            readback.get("alt_text")
            if batch == "media"
            else readback.get("content", {}).get("raw")
        )
        item["status"] = (
            "restored-verified"
            if actual == restore_value
            else "WRITTEN-RESTORE-READBACK-MISMATCH"
        )

    return {
        "batch": f"{batch} restore",
        "mode": "APPLY" if apply else "DRY-RUN",
        "authenticated": True,
        "items": [item],
    }


# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--batch", choices=["media", "content"], required=True)
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="default")
    mode.add_argument("--apply", action="store_true", help="perform live writes")
    ap.add_argument("--only-media-id", help="restrict media batch to one attachment")
    ap.add_argument("--only-page-id", help="restrict content batch to one page")
    ap.add_argument("--restore", type=Path, help="restore one pre-write snapshot")
    ap.add_argument("--json", type=Path, help="also write the report to this path")
    args = ap.parse_args()

    if args.batch == "media" and args.only_page_id:
        raise SystemExit("--only-page-id is a content selector, not a media selector")
    if args.batch == "content" and args.only_media_id:
        raise SystemExit("--only-media-id is a media selector, not a content selector")
    if args.restore and (args.only_media_id or args.only_page_id):
        raise SystemExit("--restore cannot be combined with --only-media-id/--only-page-id")

    client = make_client()
    if args.restore and client is None:
        raise SystemExit("--restore requires WordPress credentials, even in dry-run mode")
    if args.apply and client is None:
        raise SystemExit(
            "--apply requires WP_USER/WP_APP_PASSWORD in the environment "
            "(presence checked by name only). Refusing to continue."
        )

    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    operation = "restore" if args.restore else args.batch
    run_dir = SNAPSHOT_ROOT / f"{stamp}-{operation}-{'apply' if args.apply else 'dry'}"

    if args.restore:
        assert client is not None
        report = run_restore(args.batch, args.restore, client, args.apply, run_dir)
    elif args.batch == "media":
        report = run_media(client, args.apply, run_dir, args.only_media_id)
    else:
        report = run_content(client, args.apply, run_dir, args.only_page_id)

    out = json.dumps(report, indent=2, ensure_ascii=False)
    print(out)
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "report.json").write_text(out + "\n", "utf-8")
    if args.json:
        args.json.write_text(out + "\n", "utf-8")
    print(f"\nreport saved: {run_dir / 'report.json'}", file=sys.stderr)

    bad = json.loads(out)
    problems = []
    for item in bad.get("items", []) + [
        i for p in bad.get("pages", []) for i in p.get("items", [])
    ]:
        status = str(item.get("status", ""))
        if status in ("no-match", "conflict") or status.startswith(
            ("REFUSED", "CONFLICT", "WRITTEN-")
        ):
            problems.append(item)
    for p in bad.get("pages", []):
        if str(p.get("status", "")).startswith(("REFUSED", "WRITTEN-")):
            problems.append(p)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
