#!/usr/bin/env python3
"""Upload local event hero images to WordPress media; write IDs back to catalog.

Dry-run by default. Pass --execute to upload.
Credentials: scripts/notion-to-wp/.env (WP_USER / WP_APP_PASSWORD) or process env.
Never prints secret values.
"""

from __future__ import annotations

import argparse
import base64
import sys
from pathlib import Path
from typing import Any

import requests
import yaml

from lib import (
    CATALOG_PATH,
    dump_yaml,
    guess_mime,
    load_catalog,
    load_wp_credentials,
    resolve_image_path,
    resolve_path_roots,
)


class WPMedia:
    def __init__(self, base: str, user: str, app_password: str):
        self.base = base.rstrip("/")
        self.s = requests.Session()
        token = base64.b64encode(f"{user}:{app_password}".encode()).decode()
        self.s.headers.update({"Authorization": f"Basic {token}"})

    def get_media(self, media_id: int) -> dict:
        r = self.s.get(f"{self.base}/wp-json/wp/v2/media/{media_id}", timeout=30)
        r.raise_for_status()
        return r.json()

    def upload(self, path: Path, alt: str, mime: str) -> dict:
        data = path.read_bytes()
        r = self.s.post(
            f"{self.base}/wp-json/wp/v2/media",
            headers={
                "Content-Disposition": f'attachment; filename="{path.name}"',
                "Content-Type": mime,
            },
            data=data,
            timeout=120,
        )
        r.raise_for_status()
        media = r.json()
        if alt:
            self.s.post(
                f"{self.base}/wp-json/wp/v2/media/{media['id']}",
                json={"alt_text": alt},
                timeout=30,
            ).raise_for_status()
        return media


def needs_upload(image: dict[str, Any], roots: dict[str, Path]) -> Path | None:
    if not image:
        return None
    if image.get("media_id") and image.get("url"):
        return None
    if image.get("media_id") and not image.get("url"):
        return None
    path = resolve_image_path(image, roots)
    if path and path.exists() and path.is_file():
        return path
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=CATALOG_PATH)
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually upload media and write catalog (default is dry-run)",
    )
    parser.add_argument(
        "--resolve-urls",
        action="store_true",
        help="Fetch source_url for rows that already have media_id but lack url",
    )
    args = parser.parse_args()

    raw = yaml.safe_load(args.catalog.read_text(encoding="utf-8"))
    if not raw or "events" not in raw:
        print(f"ERROR: invalid catalog {args.catalog}", file=sys.stderr)
        return 1

    catalog = load_catalog(args.catalog)
    roots = resolve_path_roots(catalog)
    creds = load_wp_credentials()
    has_creds = bool(creds.get("user") and creds.get("app_password"))
    print(
        f"WP auth: {'present' if has_creds else 'MISSING'} "
        f"(user length={len(creds.get('user') or '')})"
    )
    print(f"Mode: {'EXECUTE' if args.execute else 'DRY-RUN'}")

    wp = None
    if (args.execute or args.resolve_urls) and has_creds:
        wp = WPMedia(creds["base"], creds["user"], creds["app_password"])  # type: ignore[arg-type]
    elif args.execute and not has_creds:
        print("ERROR: --execute requires WP_USER + WP_APP_PASSWORD", file=sys.stderr)
        return 1

    raw_by_id = {e["id"]: e for e in raw["events"] if e.get("id")}
    materialized: list[str] = []

    planned = 0
    uploaded = 0
    resolved = 0
    missing_files = 0

    for event in catalog["events"]:
        eid = event.get("id")
        if not eid:
            continue
        if eid not in raw_by_id:
            # Persist harvest-merged row so media_id can be written back.
            raw_by_id[eid] = {
                k: event.get(k)
                for k in (
                    "id",
                    "title",
                    "date",
                    "end",
                    "bucket_hint",
                    "kind",
                    "edition",
                    "role",
                    "url",
                    "blurb",
                    "label",
                    "tags",
                    "status",
                    "cta_past",
                    "cta_upcoming",
                    "image_layout",
                )
                if event.get(k) not in (None, "", [])
            }
            raw_by_id[eid]["image"] = dict(event.get("image") or {})
            materialized.append(eid)

        image = dict(event.get("image") or {})
        raw_image = dict(raw_by_id[eid].get("image") or {})
        path = resolve_image_path(image, roots)

        if (
            image.get("media_id")
            and not image.get("url")
            and (args.resolve_urls or args.execute)
        ):
            if wp is None:
                print(f"  would resolve media_id={image['media_id']} for {eid}")
            else:
                media = wp.get_media(int(image["media_id"]))
                url = media.get("source_url")
                raw_image["media_id"] = int(image["media_id"])
                raw_image["url"] = url
                raw_by_id[eid]["image"] = raw_image
                resolved += 1
                print(f"  resolved {eid} -> media {image['media_id']}")

        if image.get("media_id"):
            continue
        if not path:
            continue
        if not path.exists():
            print(f"  MISSING file for {eid}: {path}")
            missing_files += 1
            continue

        planned += 1
        alt = image.get("alt") or event.get("title") or eid
        photographer = image.get("photographer")
        if photographer:
            alt = f"{alt} (photo: {photographer})"
        mime = guess_mime(path)
        size_kb = path.stat().st_size // 1024

        if not args.execute:
            print(f"  would upload {eid}: {path.name} ({size_kb} KB, {mime})")
            continue

        assert wp is not None
        media = wp.upload(path, alt=alt, mime=mime)
        raw_image["path"] = image.get("path")
        raw_image["media_id"] = media["id"]
        raw_image["url"] = media.get("source_url")
        if photographer:
            raw_image["photographer"] = photographer
        if image.get("alt"):
            raw_image["alt"] = image.get("alt")
        raw_by_id[eid]["image"] = raw_image
        uploaded += 1
        print(f"  uploaded {eid} -> media_id={media['id']}")

    if args.execute or (args.resolve_urls and resolved):
        ordered: list[dict] = []
        seen: set[str] = set()
        for e in raw["events"]:
            eid = e.get("id")
            if eid and eid in raw_by_id:
                ordered.append(raw_by_id[eid])
                seen.add(eid)
            else:
                ordered.append(e)
        for eid in materialized:
            if eid not in seen:
                ordered.append(raw_by_id[eid])
                seen.add(eid)
        raw["events"] = ordered
        dump_yaml(raw, args.catalog)
        print(f"Wrote catalog {args.catalog}")
    elif materialized and not args.execute:
        print(
            f"Note: {len(materialized)} harvest-only rows would be "
            "materialized into the catalog on --execute"
        )

    print(
        f"Summary: planned_uploads={planned} uploaded={uploaded} "
        f"urls_resolved={resolved} missing_files={missing_files}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
