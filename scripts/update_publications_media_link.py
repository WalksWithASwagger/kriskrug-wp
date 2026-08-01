#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import difflib
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import requests


PAGE_ID = 1895
PAGE_SLUG = "publications"
PAGE_TITLE = "Publications"
MEDIA_PATH = "/2026/07/02/ai-media-appearances-podcast-guesting/"
DEFAULT_SNAPSHOT_DIR = Path("backup/20260731-publications-media-appearances-link")
REPO_ROOT = Path(__file__).resolve().parents[1]
ANCHOR = (
    'For current projects and AI work, start with <a href="/recent-projects-include/">Work</a>, '
    '<a href="/speaking/">Speaking</a>, or '
    '<a href="/generative-ai-services/">Services</a>.'
)
INSERTION = (
    ANCHOR
    + ' For a curated set of recent video interviews, broadcasts, and playable appearances, '
    + f'visit <a href="{MEDIA_PATH}">Media Appearances</a>.'
)


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def repo_relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def cache_bypass(url: str) -> str:
    parts = urlsplit(url)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query["cb"] = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def auth_session() -> tuple[requests.Session, str]:
    base_url = os.getenv("WP_BASE_URL", "https://kriskrug.co").rstrip("/")
    user = os.getenv("WP_USER") or os.getenv("WP_API_USERNAME")
    password = os.getenv("WP_APP_PASSWORD") or os.getenv("WP_API_PASSWORD")
    if not user or not password:
        raise SystemExit("[ABORT] WordPress credentials are unresolved. Run through Varlock.")
    token = base64.b64encode(f"{user}:{password}".encode()).decode()
    session = requests.Session()
    session.headers.update({"Authorization": f"Basic {token}"})
    return session, base_url


def fetch_page(session: requests.Session, base_url: str) -> dict:
    response = session.get(
        f"{base_url}/wp-json/wp/v2/pages/{PAGE_ID}",
        params={"context": "edit"},
        timeout=30,
    )
    response.raise_for_status()
    page = response.json()
    title = page.get("title", {}).get("raw") or page.get("title", {}).get("rendered")
    if page.get("id") != PAGE_ID:
        raise SystemExit(f"[ABORT] expected page id {PAGE_ID}, got {page.get('id')!r}")
    if page.get("slug") != PAGE_SLUG:
        raise SystemExit(f"[ABORT] expected slug {PAGE_SLUG!r}, got {page.get('slug')!r}")
    if title != PAGE_TITLE:
        raise SystemExit(f"[ABORT] expected title {PAGE_TITLE!r}, got {title!r}")
    if page.get("status") != "publish":
        raise SystemExit(f"[ABORT] expected published status, got {page.get('status')!r}")
    if not page.get("content", {}).get("raw"):
        raise SystemExit("[ABORT] authenticated response did not include content.raw")
    return page


def build_updated(raw: str) -> tuple[str, bool]:
    target_count = raw.count(MEDIA_PATH)
    if target_count:
        if target_count == 1 and raw.count("Media Appearances") == 1:
            return raw, True
        raise SystemExit(
            f"[ABORT] partial or duplicate target state: path={target_count}, "
            f"label={raw.count('Media Appearances')}"
        )
    anchor_count = raw.count(ANCHOR)
    if anchor_count != 1:
        raise SystemExit(f"[ABORT] expected one publications footer anchor, found {anchor_count}")
    return raw.replace(ANCHOR, INSERTION, 1), False


def diff_text(before: str, after: str) -> str:
    return "".join(
        difflib.unified_diff(
            before.splitlines(keepends=True),
            after.splitlines(keepends=True),
            fromfile="page-1895-before.html",
            tofile="page-1895-after.html",
        )
    )


def write_snapshot(page: dict, snapshot_dir: Path, label: str) -> tuple[Path, Path]:
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    json_path = snapshot_dir / f"page-{PAGE_ID}-{label}-{stamp}.json"
    html_path = snapshot_dir / f"page-{PAGE_ID}-{label}-{stamp}.html"
    json_path.write_text(json.dumps(page, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    html_path.write_text(page["content"]["raw"], encoding="utf-8")
    json_path.chmod(0o600)
    html_path.chmod(0o600)
    return json_path, html_path


def update_content(session: requests.Session, base_url: str, content: str) -> dict:
    response = session.post(
        f"{base_url}/wp-json/wp/v2/pages/{PAGE_ID}",
        json={"content": content},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def verify_public(page_url: str) -> str:
    url = cache_bypass(page_url)
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    if response.text.count(MEDIA_PATH) != 1 or response.text.count("Media Appearances") != 1:
        raise SystemExit("[ABORT] public cache-bypass verification failed")
    return url


def write_manifest(
    snapshot_dir: Path,
    before_json: Path,
    before_html: Path,
    before_sha: str,
    after_sha: str,
    public_url: str,
) -> Path:
    manifest_path = snapshot_dir / "rollback-manifest.json"
    snapshot_json = repo_relative(before_json)
    snapshot_html = repo_relative(before_html)
    manifest = {
        "page_id": PAGE_ID,
        "slug": PAGE_SLUG,
        "snapshot_json": snapshot_json,
        "snapshot_html": snapshot_html,
        "before_sha256": before_sha,
        "after_sha256": after_sha,
        "public_verification_url": public_url,
        "restore_command": (
            "varlock run --path .env.schema --inject vars -- python3 scripts/update_publications_media_link.py "
            f"--restore {snapshot_json} --apply"
        ),
        "cache_note": "Cache-bypass verified. Purge Pagely PressCACHE manually if canonical HTML remains stale.",
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Safely add the media collection link to Publications")
    parser.add_argument("--apply", action="store_true", help="perform the WordPress write")
    parser.add_argument("--restore", type=Path, help="restore content.raw from a saved page snapshot")
    parser.add_argument("--snapshot-dir", type=Path, default=DEFAULT_SNAPSHOT_DIR)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    session, base_url = auth_session()
    current = fetch_page(session, base_url)
    current_raw = current["content"]["raw"]

    if args.restore:
        snapshot = json.loads(args.restore.read_text(encoding="utf-8"))
        if snapshot.get("id") != PAGE_ID:
            raise SystemExit(f"[ABORT] restore snapshot is not page {PAGE_ID}")
        desired = snapshot.get("content", {}).get("raw")
        if not desired:
            raise SystemExit("[ABORT] restore snapshot has no content.raw")
        print(diff_text(current_raw, desired))
        if not args.apply:
            print("[DRY RUN] restore diff only; pass --apply to write")
            return 0
        write_snapshot(current, args.snapshot_dir, "before-restore")
        update_content(session, base_url, desired)
        readback = fetch_page(session, base_url)["content"]["raw"]
        if sha256(readback) != sha256(desired):
            raise SystemExit("[ABORT] restore readback hash mismatch")
        print(f"[RESTORED] page={PAGE_ID} sha256={sha256(readback)}")
        return 0

    desired, already_applied = build_updated(current_raw)
    if already_applied:
        print(f"[NOOP] page={PAGE_ID} already contains the verified Media Appearances link")
        return 0

    print(f"target page={PAGE_ID} slug={PAGE_SLUG} status={current['status']}")
    print(f"before_sha256={sha256(current_raw)}")
    print(f"after_sha256={sha256(desired)}")
    print(diff_text(current_raw, desired))
    if not args.apply:
        print("[DRY RUN] no WordPress write; pass --apply to write")
        return 0

    before_json, before_html = write_snapshot(current, args.snapshot_dir, "before-media-link")
    result = update_content(session, base_url, desired)
    if result.get("id") != PAGE_ID:
        raise SystemExit("[ABORT] update response returned the wrong page id")
    readback = fetch_page(session, base_url)
    readback_raw = readback["content"]["raw"]
    if sha256(readback_raw) != sha256(desired):
        raise SystemExit("[ABORT] authenticated readback hash mismatch")
    public_url = verify_public(readback["link"])
    manifest = write_manifest(
        args.snapshot_dir,
        before_json,
        before_html,
        sha256(current_raw),
        sha256(readback_raw),
        public_url,
    )
    print(f"[APPLIED] page={PAGE_ID} modified={readback.get('modified_gmt')}")
    print(f"snapshot={before_json}")
    print(f"rollback={manifest}")
    print(f"verified={public_url}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
