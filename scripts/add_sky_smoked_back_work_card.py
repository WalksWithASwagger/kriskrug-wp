#!/usr/bin/env python3
"""Safely add The Sky Smoked Back to the live Work page."""

from __future__ import annotations

import argparse
import datetime as dt
import difflib
import hashlib
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from common import REPO_ROOT, WPClient


PAGE_ID = 2672
PAGE_SLUG = "work"
PAGE_TITLE = "Work"
PROJECT_URL = "https://lightningstrike.org/"
PROJECT_HREF = f'href="{PROJECT_URL}"'
PROJECT_LABEL = "Explore The Sky Smoked Back"
PHOTOGRAPHY_CARD_ANCHOR = """<article class="aurora-media-card">
      <a href="/photography/" style="text-decoration: none;" aria-label="Explore the photography archive">"""
PROJECT_CARD = """<article class="aurora-media-card">
      <a href="https://lightningstrike.org/" style="text-decoration: none;" aria-label="Explore The Sky Smoked Back">
        <img src="https://lightningstrike.org/__l5e/assets-v1/a6927ff4-8d22-4103-a21e-5a136ae28ef0/the-sky-smoked-back-social-v1.jpg" width="1200" height="630" alt="The Sky Smoked Back title over purple lightning above a Vancouver porch" loading="lazy" decoding="async" />
        <span class="aurora-card-label">Storm film</span>
        <div>
          <h3>The Sky Smoked Back</h3>
          <p>A 56-second film, live browser storm, and public memory map made from one rare Vancouver lightning night.</p>
        </div>
      </a>
    </article>
"""
SNAPSHOT_FIELDS = "id,slug,status,title,content,modified,modified_gmt,link"


def sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def repo_relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path.resolve())


def fetch_page(wp: WPClient) -> dict:
    page = wp.get(
        f"pages/{PAGE_ID}",
        params={"context": "edit", "_fields": SNAPSHOT_FIELDS},
    )
    title = page.get("title", {}).get("raw") or page.get("title", {}).get("rendered")
    expected = {
        "id": PAGE_ID,
        "slug": PAGE_SLUG,
        "status": "publish",
        "title": PAGE_TITLE,
    }
    actual = {
        "id": page.get("id"),
        "slug": page.get("slug"),
        "status": page.get("status"),
        "title": title,
    }
    if actual != expected:
        raise SystemExit(f"[ABORT] wrong Work page identity: expected {expected}, got {actual}")
    if not isinstance(page.get("content", {}).get("raw"), str):
        raise SystemExit("[ABORT] authenticated response did not include content.raw")
    return page


def build_updated(raw: str) -> tuple[str, bool]:
    project_count = raw.count(PROJECT_HREF)
    label_count = raw.count(PROJECT_LABEL)
    if project_count or label_count:
        if project_count == 1 and label_count == 1:
            return raw, True
        raise SystemExit(
            f"[ABORT] partial or duplicate project card: url={project_count}, label={label_count}"
        )

    anchor_count = raw.count(PHOTOGRAPHY_CARD_ANCHOR)
    if anchor_count != 1:
        raise SystemExit(
            f"[ABORT] expected one Photography card anchor, found {anchor_count}"
        )
    return raw.replace(PHOTOGRAPHY_CARD_ANCHOR, PROJECT_CARD + PHOTOGRAPHY_CARD_ANCHOR, 1), False


def remove_project_card(raw: str) -> str:
    href_at = raw.find(PROJECT_HREF)
    if href_at < 0:
        raise SystemExit("[ABORT] project card href is missing")
    card_start = raw.rfind('<article class="aurora-media-card">', 0, href_at)
    card_end = raw.find("</article>", href_at)
    if card_start < 0 or card_end < 0:
        raise SystemExit("[ABORT] project card boundaries are missing")
    card_end += len("</article>")
    if raw[card_end : card_end + 1] == "\n":
        card_end += 1
    return raw[:card_start] + raw[card_end:]


def diff_text(before: str, after: str) -> str:
    return "".join(
        difflib.unified_diff(
            before.splitlines(keepends=True),
            after.splitlines(keepends=True),
            fromfile="page-2672-before.html",
            tofile="page-2672-after.html",
        )
    )


def write_snapshot(page: dict, snapshot_dir: Path, label: str) -> tuple[Path, Path]:
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    json_path = snapshot_dir / f"page-{PAGE_ID}-{label}-{stamp}.json"
    html_path = snapshot_dir / f"page-{PAGE_ID}-{label}-{stamp}.html"
    json_path.write_text(json.dumps(page, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    html_path.write_text(page["content"]["raw"], encoding="utf-8")
    json_path.chmod(0o600)
    html_path.chmod(0o600)
    return json_path, html_path


def public_verification_url(page_url: str) -> str:
    parts = urllib.parse.urlsplit(page_url)
    query = dict(urllib.parse.parse_qsl(parts.query, keep_blank_values=True))
    query["cb"] = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d%H%M%S")
    return urllib.parse.urlunsplit(
        (parts.scheme, parts.netloc, parts.path, urllib.parse.urlencode(query), parts.fragment)
    )


def verify_public(page_url: str) -> str:
    url = public_verification_url(page_url)
    request = urllib.request.Request(url, headers={"User-Agent": "kriskrug-work-card/1.0"})
    with urllib.request.urlopen(request, timeout=40) as response:
        html = response.read().decode("utf-8", errors="replace")
    if html.count(PROJECT_HREF) != 1 or html.count(PROJECT_LABEL) != 1:
        raise SystemExit("[ABORT] public cache-bypass verification failed")
    return url


def write_manifest(
    snapshot_dir: Path,
    before_json: Path,
    before_html: Path,
    before_sha: str,
    after_sha: str,
    verified_url: str,
) -> Path:
    manifest_path = snapshot_dir / "rollback-manifest.json"
    snapshot_json = repo_relative(before_json)
    manifest = {
        "page_id": PAGE_ID,
        "slug": PAGE_SLUG,
        "snapshot_json": snapshot_json,
        "snapshot_html": repo_relative(before_html),
        "before_sha256": before_sha,
        "after_sha256": after_sha,
        "verified_url": verified_url,
        "restore_command": (
            "make varlock-run CMD='python3 scripts/add_sky_smoked_back_work_card.py "
            f"--restore {snapshot_json} --apply'"
        ),
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    manifest_path.chmod(0o600)
    return manifest_path


def default_snapshot_dir() -> Path:
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return REPO_ROOT / "backup" / f"{stamp}-sky-smoked-back-work-card"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="perform the WordPress write")
    parser.add_argument("--restore", type=Path, help="restore content.raw from a saved snapshot")
    parser.add_argument("--snapshot-dir", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    explicit_snapshot_dir = args.snapshot_dir is not None
    snapshot_dir = args.snapshot_dir or default_snapshot_dir()
    if not snapshot_dir.is_absolute():
        snapshot_dir = REPO_ROOT / snapshot_dir

    wp = WPClient.from_env()
    current = fetch_page(wp)
    current_raw = current["content"]["raw"]

    if args.restore:
        snapshot_path = args.restore if args.restore.is_absolute() else REPO_ROOT / args.restore
        snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
        if snapshot.get("id") != PAGE_ID or snapshot.get("slug") != PAGE_SLUG:
            raise SystemExit("[ABORT] restore snapshot is not the Work page")
        desired = snapshot.get("content", {}).get("raw")
        if not desired:
            raise SystemExit("[ABORT] restore snapshot has no content.raw")
        print(diff_text(current_raw, desired))
        if not args.apply:
            print("[DRY RUN] restore diff only; pass --apply to write")
            return 0
        write_snapshot(current, snapshot_dir, "before-restore")
        wp.post(f"pages/{PAGE_ID}", {"content": desired})
        restored = fetch_page(wp)["content"]["raw"]
        if sha256(restored) != sha256(desired):
            raise SystemExit("[ABORT] restore readback hash mismatch")
        print(f"[RESTORED] page={PAGE_ID} sha256={sha256(restored)}")
        return 0

    desired, already_applied = build_updated(current_raw)
    if already_applied:
        verified_url = verify_public(current["link"])
        if explicit_snapshot_dir and not (snapshot_dir / "rollback-manifest.json").exists():
            before_jsons = sorted(snapshot_dir.glob(f"page-{PAGE_ID}-before-project-card-*.json"))
            before_htmls = sorted(snapshot_dir.glob(f"page-{PAGE_ID}-before-project-card-*.html"))
            if len(before_jsons) != 1 or len(before_htmls) != 1:
                raise SystemExit("[ABORT] expected one before snapshot pair for receipt repair")
            before = json.loads(before_jsons[0].read_text(encoding="utf-8"))
            before_raw = before.get("content", {}).get("raw", "")
            if remove_project_card(current_raw) != before_raw:
                raise SystemExit("[ABORT] current page differs from the snapshot beyond the project card")
            manifest = write_manifest(
                snapshot_dir,
                before_jsons[0],
                before_htmls[0],
                sha256(before_raw),
                sha256(current_raw),
                verified_url,
            )
            print(f"rollback={repo_relative(manifest)}")
        print(f"[NOOP] page={PAGE_ID} already has one verified project card")
        print(f"verified={verified_url}")
        return 0

    print(f"target page={PAGE_ID} slug={PAGE_SLUG} status={current['status']}")
    print(f"before_sha256={sha256(current_raw)}")
    print(f"after_sha256={sha256(desired)}")
    print(diff_text(current_raw, desired))
    if not args.apply:
        print("[DRY RUN] no WordPress write; pass --apply to write")
        return 0

    fresh = fetch_page(wp)
    fresh_raw = fresh["content"]["raw"]
    if sha256(fresh_raw) != sha256(current_raw):
        raise SystemExit("[ABORT] Work page changed after preflight; rerun dry-run")

    before_json, before_html = write_snapshot(fresh, snapshot_dir, "before-project-card")
    result = wp.post(f"pages/{PAGE_ID}", {"content": desired})
    if result.get("id") != PAGE_ID:
        raise SystemExit("[ABORT] update response returned the wrong page id")
    readback = fetch_page(wp)
    readback_raw = readback["content"]["raw"]
    _, readback_applied = build_updated(readback_raw)
    if not readback_applied or remove_project_card(readback_raw) != current_raw:
        raise SystemExit("[ABORT] authenticated readback changed content outside the project card")
    verified_url = verify_public(readback["link"])
    manifest = write_manifest(
        snapshot_dir,
        before_json,
        before_html,
        sha256(current_raw),
        sha256(readback_raw),
        verified_url,
    )
    print(f"[APPLIED] page={PAGE_ID} modified={readback.get('modified_gmt')}")
    print(f"snapshot={repo_relative(before_json)}")
    print(f"rollback={repo_relative(manifest)}")
    print(f"verified={verified_url}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
