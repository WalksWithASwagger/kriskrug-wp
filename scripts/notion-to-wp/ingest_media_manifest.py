#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlparse

import requests

from wp_client import WordPress


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]
DEFAULT_MANIFEST = REPO_ROOT / "content" / "source-packs" / "site-photography-2026" / "media-manifest.json"
MEDIA_FIELDS = "id,slug,source_url,title,caption,description,alt_text,date"
WORDPRESS_FIELDS = ("title", "alt_text", "caption", "description")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    return value.strip()


def validate_manifest(manifest_path: Path) -> tuple[dict, list[dict]]:
    data = json.loads(manifest_path.read_text())
    if data.get("schema_version") != 1:
        raise ValueError("schema_version must be 1")
    assets = data.get("assets")
    if not isinstance(assets, list) or not assets:
        raise ValueError("assets must be a non-empty list")

    validated: list[dict] = []
    seen_files: set[str] = set()
    for index, asset in enumerate(assets):
        if not isinstance(asset, dict):
            raise ValueError(f"assets[{index}] must be an object")
        relative_file = require_text(asset.get("file"), f"assets[{index}].file")
        if relative_file in seen_files:
            raise ValueError(f"duplicate asset file: {relative_file}")
        seen_files.add(relative_file)
        path = (manifest_path.parent / relative_file).resolve()
        if not path.is_file():
            raise ValueError(f"asset file not found: {relative_file}")
        expected_hash = require_text(asset.get("sha256"), f"assets[{index}].sha256")
        actual_hash = sha256(path)
        if actual_hash != expected_hash:
            raise ValueError(f"sha256 mismatch for {relative_file}")

        credit = require_text(asset.get("credit"), f"assets[{index}].credit")
        wordpress = asset.get("wordpress")
        if not isinstance(wordpress, dict):
            raise ValueError(f"assets[{index}].wordpress must be an object")
        metadata = {
            field: require_text(wordpress.get(field), f"assets[{index}].wordpress.{field}")
            for field in WORDPRESS_FIELDS
        }
        if credit not in metadata["caption"] or credit not in metadata["description"]:
            raise ValueError(f"caption and description must preserve credit for {relative_file}")

        mime = mimetypes.guess_type(path.name)[0]
        if mime not in {"image/jpeg", "image/png", "image/webp"}:
            raise ValueError(f"unsupported media type for {relative_file}: {mime}")
        validated.append(
            {
                **asset,
                "path": path,
                "mime": mime,
                "wordpress": metadata,
            }
        )
    return data, validated


def source_filename(media: dict) -> str:
    return unquote(Path(urlparse(str(media.get("source_url", ""))).path).name)


def exact_media_matches(items: object, filename: str) -> list[dict]:
    if not isinstance(items, list):
        return []
    target = Path(filename)
    allowed_stems = {target.stem, f"{target.stem}-scaled"}
    numbered = re.compile(rf"^{re.escape(target.stem)}-\d+$")
    matches: list[dict] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        current = Path(source_filename(item))
        if current.suffix.lower() != target.suffix.lower():
            continue
        if current.stem in allowed_stems or numbered.fullmatch(current.stem):
            matches.append(item)
    return matches


def search_media(session: requests.Session, base_url: str, filename: str, *, edit: bool) -> list[dict]:
    params = {
        "search": Path(filename).stem,
        "per_page": 100,
        "_fields": MEDIA_FIELDS,
    }
    if edit:
        params["context"] = "edit"
    response = session.get(
        f"{base_url.rstrip('/')}/wp-json/wp/v2/media",
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    return exact_media_matches(response.json(), filename)


def raw_field(value: object) -> str:
    if isinstance(value, dict):
        raw = value.get("raw")
        return raw if isinstance(raw, str) else ""
    return value if isinstance(value, str) else ""


def media_metadata(media: dict) -> dict[str, str]:
    return {
        "title": raw_field(media.get("title")),
        "alt_text": raw_field(media.get("alt_text")),
        "caption": raw_field(media.get("caption")),
        "description": raw_field(media.get("description")),
    }


def build_result(manifest_path: Path, base_url: str, mode: str) -> dict:
    try:
        manifest_label = str(manifest_path.relative_to(REPO_ROOT))
    except ValueError:
        manifest_label = str(manifest_path)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": mode,
        "manifest": manifest_label,
        "base_url": base_url,
        "assets": [],
        "summary": {},
        "rollback": {
            "created_media_ids": [],
            "admin_urls": [],
            "method": "Remove only the listed unattached items through wp-admin after confirming no page references them.",
        },
    }


def write_report(result: dict, report_path: Path | None) -> None:
    payload = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if report_path:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(payload)
    print(payload, end="")


def abort_execute(result: dict, report_path: Path | None, message: str) -> None:
    result["summary"] = {
        "assets_completed": len(result["assets"]),
        "created_media_ids": len(result["rollback"]["created_media_ids"]),
        "live_write": bool(result["rollback"]["created_media_ids"]),
        "error": message,
    }
    write_report(result, report_path)
    raise SystemExit(message)


def dry_run(manifest_path: Path, base_url: str, assets: list[dict], report_path: Path | None) -> int:
    result = build_result(manifest_path, base_url, "dry-run")
    with requests.Session() as session:
        for asset in assets:
            matches = search_media(session, base_url, asset["path"].name, edit=False)
            result["assets"].append(
                {
                    "file": asset["file"],
                    "sha256": asset["sha256"],
                    "existing_media_ids": [item["id"] for item in matches],
                    "action": "upload" if not matches else "review-existing",
                    "wordpress": asset["wordpress"],
                }
            )
    uploads = sum(item["action"] == "upload" for item in result["assets"])
    result["summary"] = {
        "assets": len(assets),
        "planned_uploads": uploads,
        "existing_matches": len(assets) - uploads,
        "live_write": False,
    }
    write_report(result, report_path)
    return 0


def execute(manifest_path: Path, base_url: str, assets: list[dict], report_path: Path | None) -> int:
    user = os.environ.get("WP_USER")
    password = (os.environ.get("WP_APP_PASSWORD") or "").replace(" ", "")
    if not user or not password:
        raise SystemExit("--execute requires Varlock-injected WP_USER and WP_APP_PASSWORD")

    wp = WordPress(base_url, user, password)
    result = build_result(manifest_path, base_url, "execute")
    try:
        for asset in assets:
            matches = search_media(wp.s, base_url, asset["path"].name, edit=True)
            if len(matches) > 1:
                abort_execute(
                    result,
                    report_path,
                    f"multiple exact media matches for {asset['file']}; aborting",
                )
            if matches:
                current = media_metadata(matches[0])
                if current != asset["wordpress"]:
                    abort_execute(
                        result,
                        report_path,
                        f"existing media metadata differs for {asset['file']}; no update applied",
                    )
                result["assets"].append(
                    {
                        "file": asset["file"],
                        "media_id": matches[0]["id"],
                        "source_url": matches[0]["source_url"],
                        "action": "reused",
                        "verified": True,
                    }
                )
                continue

            media = wp.upload_media_file(asset["path"], mime=asset["mime"])
            media_id = int(media["id"])
            result["rollback"]["created_media_ids"].append(media_id)
            result["rollback"]["admin_urls"].append(
                f"{base_url.rstrip('/')}/wp-admin/post.php?post={media_id}&action=edit"
            )
            entry = {
                "file": asset["file"],
                "media_id": media_id,
                "source_url": media.get("source_url", ""),
                "action": "uploaded-pending-metadata",
                "verified": False,
            }
            result["assets"].append(entry)
            wp.update_media(media_id, asset["wordpress"])
            verified = wp.get_media(media_id, context="edit")
            if media_metadata(verified) != asset["wordpress"]:
                abort_execute(
                    result,
                    report_path,
                    f"metadata verification failed for media id {media_id}",
                )
            entry.update(
                {
                    "source_url": verified["source_url"],
                    "action": "uploaded",
                    "verified": True,
                }
            )
    except (requests.RequestException, KeyError, ValueError) as exc:
        abort_execute(result, report_path, f"WordPress media ingestion failed: {exc}")

    result["summary"] = {
        "assets": len(assets),
        "uploaded": sum(item["action"] == "uploaded" for item in result["assets"]),
        "reused": sum(item["action"] == "reused" for item in result["assets"]),
        "live_write": True,
    }
    write_report(result, report_path)
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate and ingest a WordPress media metadata manifest.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--base-url", default=os.environ.get("WP_BASE_URL", "https://kriskrug.co"))
    parser.add_argument("--report", type=Path)
    parser.add_argument("--execute", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    manifest_path = args.manifest.resolve()
    _, assets = validate_manifest(manifest_path)
    if args.execute:
        return execute(manifest_path, args.base_url, assets, args.report)
    return dry_run(manifest_path, args.base_url, assets, args.report)


if __name__ == "__main__":
    sys.exit(main())
