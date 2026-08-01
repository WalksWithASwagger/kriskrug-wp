#!/usr/bin/env python3
"""Snapshot / dry-run / apply helper for Publications page 1895 (Aurora paper tear-sheet).

Default is dry-run. Never uploads media or PATCHes without explicit flags.
Requires WP_USER + WP_APP_PASSWORD (prefer: varlock run --inject vars -- …).
"""

from __future__ import annotations

import argparse
import base64
import difflib
import hashlib
import json
import mimetypes
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import requests


PAGE_ID = 1895
PAGE_SLUG = "publications"
PAGE_TITLE = "Publications"
REPO_ROOT = Path(__file__).resolve().parents[1]
PAYLOAD_PATH = (
    REPO_ROOT
    / "content"
    / "source-packs"
    / "keynotes-2026"
    / "wp-payloads"
    / "publications.html"
)
ASSETS_DIR = REPO_ROOT / "content" / "source-packs" / "keynotes-2026" / "assets"
DEFAULT_SNAPSHOT_DIR = Path("backup") / "publications-tearsheet"
MEDIA_KEYS = [
    "press-2026-07-31-biv-ecosystem-context.jpg",
    "press-2026-07-24-the-tyee-context.jpg",
    "press-2026-06-15-biv-context.jpg",
    "press-2026-05-20-storyhive.jpg",
    "press-2026-02-09-tela-viva-context.jpg",
    "press-2025-07-09-e-channelnews-context.jpg",
    "press-2025-05-01-portfolio-yvr-context.jpg",
]
FORBIDDEN_AFTER = ("kk-publications", "#00e5ff", "#ff6a6a", "--press-night")


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
    return urlunsplit(
        (parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment)
    )


def auth_session() -> tuple[requests.Session, str]:
    base_url = os.getenv("WP_BASE_URL", "https://kriskrug.co").rstrip("/")
    user = os.getenv("WP_USER") or os.getenv("WP_API_USERNAME")
    password = os.getenv("WP_APP_PASSWORD") or os.getenv("WP_API_PASSWORD")
    if not user or not password:
        raise SystemExit(
            "[ABORT] WordPress credentials unresolved. "
            "Run: varlock run --path .env.schema --inject vars -- "
            "python3 scripts/deploy_publications_tearsheet.py --dry-run"
        )
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
        raise SystemExit(
            f"[ABORT] expected slug {PAGE_SLUG!r}, got {page.get('slug')!r}"
        )
    if title != PAGE_TITLE:
        raise SystemExit(f"[ABORT] expected title {PAGE_TITLE!r}, got {title!r}")
    if page.get("status") != "publish":
        raise SystemExit(
            f"[ABORT] expected published status, got {page.get('status')!r}"
        )
    if not page.get("content", {}).get("raw"):
        raise SystemExit("[ABORT] authenticated response did not include content.raw")
    return page


def write_snapshot(page: dict, snapshot_dir: Path, label: str) -> tuple[Path, Path]:
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    json_path = snapshot_dir / f"page-{PAGE_ID}-{label}-{stamp}.json"
    html_path = snapshot_dir / f"page-{PAGE_ID}-{label}-{stamp}.html"
    json_path.write_text(
        json.dumps(page, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    html_path.write_text(page["content"]["raw"], encoding="utf-8")
    json_path.chmod(0o600)
    html_path.chmod(0o600)
    return json_path, html_path


def load_payload() -> str:
    if not PAYLOAD_PATH.exists():
        raise SystemExit(f"[ABORT] missing payload {PAYLOAD_PATH}")
    return PAYLOAD_PATH.read_text(encoding="utf-8")


def assert_local_media() -> None:
    missing = [name for name in MEDIA_KEYS if not (ASSETS_DIR / name).exists()]
    if missing:
        raise SystemExit(f"[ABORT] missing local press assets: {missing}")


def rewrite_media_paths(html: str, media_map: dict[str, str]) -> str:
    out = html
    for key, url in media_map.items():
        out = out.replace(f"../assets/{key}", url)
    residual = re.findall(r'src="(\.\./assets/[^"]+)"', out)
    if residual:
        raise SystemExit(f"[ABORT] residual relative image srcs: {residual}")
    return out


def load_media_map(path: Path | None) -> dict[str, str]:
    if path is None:
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not data:
        raise SystemExit(
            "[ABORT] media map must be a non-empty JSON object filename→url"
        )
    for key in MEDIA_KEYS:
        if key not in data or not str(data[key]).startswith("http"):
            raise SystemExit(f"[ABORT] media map missing http URL for {key}")
    return {k: str(data[k]) for k in MEDIA_KEYS}


def upload_media(
    session: requests.Session, base_url: str, snapshot_dir: Path
) -> dict[str, str]:
    assert_local_media()
    mapping: dict[str, str] = {}
    for name in MEDIA_KEYS:
        path = ASSETS_DIR / name
        mime = mimetypes.guess_type(name)[0] or "image/jpeg"
        with path.open("rb") as handle:
            response = session.post(
                f"{base_url}/wp-json/wp/v2/media",
                headers={
                    "Content-Disposition": f'attachment; filename="{name}"',
                    "Content-Type": mime,
                },
                data=handle.read(),
                timeout=120,
            )
        response.raise_for_status()
        body = response.json()
        source = body.get("source_url")
        if not source:
            raise SystemExit(f"[ABORT] upload for {name} returned no source_url")
        mapping[name] = source
        print(f"[UPLOAD] {name} -> {source} (id={body.get('id')})")
    map_path = snapshot_dir / "media-url-map.json"
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    map_path.write_text(json.dumps(mapping, indent=2) + "\n", encoding="utf-8")
    print(f"[MAP] wrote {map_path}")
    return mapping


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
    html = response.text
    for marker in FORBIDDEN_AFTER:
        if marker in html:
            raise SystemExit(
                f"[ABORT] public HTML still contains forbidden marker: {marker}"
            )
    if "kk-press-display" not in html:
        raise SystemExit("[ABORT] public HTML missing kk-press-display marker")
    if html.count("data-media-key=") < 7:
        raise SystemExit("[ABORT] public HTML expected >=7 data-media-key images")
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
    manifest = {
        "page_id": PAGE_ID,
        "slug": PAGE_SLUG,
        "snapshot_json": snapshot_json,
        "snapshot_html": repo_relative(before_html),
        "before_sha256": before_sha,
        "after_sha256": after_sha,
        "public_verification_url": public_url,
        "restore_command": (
            "varlock run --path .env.schema --inject vars -- "
            "python3 scripts/deploy_publications_tearsheet.py "
            f"--restore {snapshot_json} --apply"
        ),
        "cache_note": "Cache-bypass verified. Purge Pagely PressCACHE manually if canonical HTML remains stale.",
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest_path


def diff_text(before: str, after: str) -> str:
    return "".join(
        difflib.unified_diff(
            before.splitlines(keepends=True),
            after.splitlines(keepends=True),
            fromfile="page-1895-before.html",
            tofile="page-1895-after.html",
        )
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Deploy Aurora paper tear-sheet to Publications page 1895"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="snapshot intent + print diff only (default)",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="perform the WordPress content write (requires KK approval)",
    )
    parser.add_argument(
        "--upload-media",
        action="store_true",
        help="upload the seven local press assets (requires --apply)",
    )
    parser.add_argument(
        "--media-map",
        type=Path,
        help="JSON map of filename→WordPress source_url for path rewrite",
    )
    parser.add_argument(
        "--restore", type=Path, help="restore content.raw from snapshot JSON"
    )
    parser.add_argument(
        "--snapshot-dir",
        type=Path,
        default=DEFAULT_SNAPSHOT_DIR,
    )
    parser.add_argument(
        "--local-only",
        action="store_true",
        help="validate payload + local media without WordPress credentials",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    assert_local_media()
    payload = load_payload()
    if any(marker in payload for marker in FORBIDDEN_AFTER):
        raise SystemExit("[ABORT] payload still contains forbidden dark-skin markers")

    if args.local_only:
        print(
            f"[OK] local payload {repo_relative(PAYLOAD_PATH)} sha256={sha256(payload)}"
        )
        print(
            f"[OK] {len(MEDIA_KEYS)} press assets present under {repo_relative(ASSETS_DIR)}"
        )
        print(
            "[LOCAL ONLY] no WordPress call; dry-run against live requires credentials"
        )
        return 0

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

    media_map = load_media_map(args.media_map)
    desired = payload
    if args.upload_media:
        if not args.apply:
            raise SystemExit(
                "[ABORT] --upload-media requires --apply (refusing silent uploads)"
            )
        media_map = upload_media(session, base_url, args.snapshot_dir)
    if media_map:
        desired = rewrite_media_paths(payload, media_map)
    elif "../assets/" in payload:
        print(
            "[WARN] payload still uses ../assets/ relative image paths. "
            "Provide --media-map after upload, or use --upload-media --apply."
        )

    print(f"target page={PAGE_ID} slug={PAGE_SLUG} status={current['status']}")
    print(f"before_sha256={sha256(current_raw)}")
    print(f"after_sha256={sha256(desired)}")
    print(f"modified_gmt_live={current.get('modified_gmt')}")
    print(diff_text(current_raw, desired))

    if not args.apply:
        before_json, before_html = write_snapshot(
            current, args.snapshot_dir, "dry-run-before"
        )
        print(f"[DRY RUN] snapshot written: {before_json}")
        print("[DRY RUN] no WordPress write; pass --apply only after KK approval")
        return 0

    if "../assets/" in desired:
        raise SystemExit(
            "[ABORT] refusing apply while relative ../assets/ image paths remain"
        )

    before_json, before_html = write_snapshot(
        current, args.snapshot_dir, "before-tearsheet"
    )
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
