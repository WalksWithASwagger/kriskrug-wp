#!/usr/bin/env python3
"""Resolve hero art candidates for /events cards. Dry-run default, GET-only.

Resolution order per event (#587):

  1. repo-asset  tracked path already on the record (repo:, kk_kb:, absolute)
  2. youtube     maxresdefault thumbnail when youtube_id is present or the
                 event url is a YouTube link
  3. og-image    og:image from a local HTML snapshot (og_html_path) or from
                 the live event_url / url page (page fetch only on --execute)
  4. rafiki      gap marker, only with --allow-rafiki (never generates)

Candidates land under scripts/events_page/heroes/_engine_cache/ (gitignored).
Prints a JSON report of {id, source, local_path} rows to stdout; summary goes
to stderr. This script has no WordPress client and never writes media IDs
back into the catalog. Wave 3 ship owns that sync.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

from lib import (
    CATALOG_PATH,
    HERE,
    load_catalog,
    resolve_image_path,
    resolve_path_roots,
)

CACHE_DIR = HERE / "heroes" / "_engine_cache"
UA = "kk-events-hero-engine/1.0 (+https://kriskrug.co)"
TIMEOUT = 30

YOUTUBE_URL_RE = re.compile(
    r"(?:youtube\.com/(?:watch\?(?:[^#\s]*&)?v=|embed/|shorts/|live/)|youtu\.be/)"
    r"([A-Za-z0-9_-]{6,})"
)
OG_IMAGE_TAG_RE = re.compile(
    r"<meta\b[^>]*(?:property|name)=[\"']og:image(?::secure_url)?[\"'][^>]*>",
    re.IGNORECASE,
)
CONTENT_ATTR_RE = re.compile(r"content=[\"']([^\"']+)[\"']", re.IGNORECASE)
IMG_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


def youtube_thumb_url(video_id: str, name: str = "maxresdefault") -> str:
    return f"https://img.youtube.com/vi/{video_id}/{name}.jpg"


def youtube_id_from_url(url: str | None) -> str | None:
    if not url:
        return None
    match = YOUTUBE_URL_RE.search(str(url))
    return match.group(1) if match else None


def extract_og_image(html: str) -> str | None:
    for tag in OG_IMAGE_TAG_RE.finditer(html):
        content = CONTENT_ATTR_RE.search(tag.group(0))
        if content and content.group(1).strip():
            return content.group(1).strip()
    return None


def resolve_prefixed_path(text: str, roots: dict[str, Path]) -> Path:
    value = str(text)
    if value.startswith("kk_kb:"):
        return (roots["kk_kb"] / value[len("kk_kb:") :]).resolve()
    if value.startswith("repo:"):
        return (roots["repo"] / value[len("repo:") :]).resolve()
    path = Path(value).expanduser()
    return path if path.is_absolute() else (HERE / path).resolve()


def ext_for(url: str | None, content_type: str | None = None) -> str:
    if content_type:
        mapped = {
            "image/jpeg": ".jpg",
            "image/png": ".png",
            "image/webp": ".webp",
            "image/gif": ".gif",
        }.get(content_type.split(";")[0].strip().lower())
        if mapped:
            return mapped
    if url:
        suffix = Path(url.split("?")[0].split("#")[0]).suffix.lower()
        if suffix in IMG_EXTS:
            return suffix
    return ".jpg"


def _add_note(row: dict[str, Any], note: str) -> None:
    row["note"] = f"{row['note']}; {note}" if row.get("note") else note


def _absolute_og_url(og_url: str, base_url: str | None) -> str | None:
    if og_url.startswith("//"):
        return f"https:{og_url}"
    if og_url.startswith(("http://", "https://")):
        return og_url
    if base_url:
        joined = urljoin(base_url, og_url)
        if joined.startswith(("http://", "https://")):
            return joined
    return None


def plan_event(
    event: dict[str, Any],
    roots: dict[str, Path],
    cache_dir: Path,
    allow_rafiki: bool = False,
) -> dict[str, Any]:
    """Pure planning step: pick a source for one event. No network, no writes."""
    eid = event.get("id")
    row: dict[str, Any] = {
        "id": eid,
        "source": "none",
        "local_path": None,
        "remote_url": None,
        "fetched": False,
    }
    image = event.get("image") or {}
    if not isinstance(image, dict):
        image = {"path": image}

    if image.get("media_id"):
        row["source"] = "wp-media"
        _add_note(row, f"already WP media {image['media_id']}; nothing to fetch")
        return row

    notes: list[str] = []

    asset = resolve_image_path(image, roots)
    if asset is not None:
        if asset.exists() and asset.is_file():
            row["source"] = "repo-asset"
            row["local_path"] = str(asset)
            return row
        notes.append(f"on-record image path missing on disk: {asset}")

    page_url = event.get("event_url") or event.get("url")
    video_id = event.get("youtube_id") or youtube_id_from_url(page_url)
    if video_id:
        row["source"] = "youtube"
        row["youtube_id"] = video_id
        row["remote_url"] = youtube_thumb_url(video_id)
        row["local_path"] = str(cache_dir / f"{eid}-youtube.jpg")
        for note in notes:
            _add_note(row, note)
        return row

    og_html = event.get("og_html_path")
    if og_html:
        snapshot = resolve_prefixed_path(og_html, roots)
        if snapshot.exists() and snapshot.is_file():
            og_url = extract_og_image(
                snapshot.read_text(encoding="utf-8", errors="replace")
            )
            og_url = _absolute_og_url(og_url, page_url) if og_url else None
            if og_url:
                row["source"] = "og-image"
                row["og_from"] = "snapshot"
                row["remote_url"] = og_url
                row["local_path"] = str(cache_dir / f"{eid}-og{ext_for(og_url)}")
                for note in notes:
                    _add_note(row, note)
                return row
            notes.append(f"no absolute og:image in snapshot: {snapshot}")
        else:
            notes.append(f"og_html_path missing on disk: {snapshot}")

    if page_url:
        row["source"] = "og-image"
        row["og_from"] = "page"
        row["page_url"] = page_url
        _add_note(row, "og:image resolved from live page only on --execute")
        for note in notes:
            _add_note(row, note)
        return row

    if allow_rafiki:
        row["source"] = "rafiki"
        _add_note(
            row,
            "gap eligible for a Rafiki branded tile; generation happens "
            "outside this script",
        )
        for note in notes:
            _add_note(row, note)
        return row

    for note in notes:
        _add_note(row, note)
    if not row.get("note"):
        _add_note(row, "MISSING hero_hint: no image path, youtube id, or event url")
    return row


def resolve_events(
    events: list[dict[str, Any]],
    roots: dict[str, Path],
    cache_dir: Path,
    allow_rafiki: bool = False,
) -> tuple[list[dict[str, Any]], int]:
    rows: list[dict[str, Any]] = []
    skipped_no_id = 0
    for event in events:
        if not isinstance(event, dict) or not event.get("id"):
            skipped_no_id += 1
            continue
        rows.append(plan_event(event, roots, cache_dir, allow_rafiki=allow_rafiki))
    return rows, skipped_no_id


def _download(url: str, dest: Path) -> Any | None:
    """GET url to dest. Returns the response, or None on HTTP 404."""
    import requests

    resp = requests.get(url, headers={"User-Agent": UA}, timeout=TIMEOUT)
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(resp.content)
    return resp


def _execute_youtube(row: dict[str, Any]) -> None:
    dest = Path(row["local_path"])
    if dest.exists():
        row["fetched"] = True
        _add_note(row, "cache hit; not re-downloaded")
        return
    if _download(row["remote_url"], dest) is None:
        fallback = youtube_thumb_url(row["youtube_id"], "hqdefault")
        if _download(fallback, dest) is None:
            _add_note(row, "maxresdefault and hqdefault both 404")
            return
        row["remote_url"] = fallback
        _add_note(row, "maxresdefault 404; used hqdefault")
    row["fetched"] = True


def _execute_og(row: dict[str, Any], cache_dir: Path, allow_rafiki: bool) -> None:
    import requests

    if row.get("og_from") == "page":
        page = requests.get(
            row["page_url"], headers={"User-Agent": UA}, timeout=TIMEOUT
        )
        page.raise_for_status()
        og_url = extract_og_image(page.text)
        og_url = _absolute_og_url(og_url, row["page_url"]) if og_url else None
        if not og_url:
            row["source"] = "rafiki" if allow_rafiki else "none"
            row["local_path"] = None
            _add_note(row, "no og:image found on page")
            return
        row["remote_url"] = og_url
        row["local_path"] = str(cache_dir / f"{row['id']}-og{ext_for(og_url)}")
    dest = Path(row["local_path"])
    if dest.exists():
        row["fetched"] = True
        _add_note(row, "cache hit; not re-downloaded")
        return
    if _download(row["remote_url"], dest) is None:
        _add_note(row, "og:image URL returned 404")
        return
    row["fetched"] = True


def execute_rows(
    rows: list[dict[str, Any]], cache_dir: Path, allow_rafiki: bool
) -> int:
    errors = 0
    for row in rows:
        try:
            if row["source"] == "youtube":
                _execute_youtube(row)
            elif row["source"] == "og-image":
                _execute_og(row, cache_dir, allow_rafiki)
        except Exception as exc:  # keep going; one bad row must not kill the run
            errors += 1
            _add_note(row, f"fetch error: {exc}")
    return errors


def load_events_json(path: Path) -> list[dict[str, Any]]:
    doc = json.loads(path.read_text(encoding="utf-8"))
    events = doc.get("events") if isinstance(doc, dict) else doc
    if not isinstance(events, list):
        raise SystemExit(
            f'--events-json must hold a list of event dicts or {{"events": [...]}}: {path}'
        )
    return events


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--catalog", type=Path, default=CATALOG_PATH)
    parser.add_argument(
        "--events-json",
        type=Path,
        help="JSON file with a list of event dicts (overrides --catalog)",
    )
    parser.add_argument(
        "--ids",
        nargs="+",
        help="only process these event ids (space or comma separated)",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--dry-run",
        action="store_true",
        help="plan only, zero network (default)",
    )
    mode.add_argument(
        "--execute",
        action="store_true",
        help="download candidates into heroes/_engine_cache/ (GET-only)",
    )
    parser.add_argument(
        "--allow-rafiki",
        action="store_true",
        help="mark remaining gaps as Rafiki-tile eligible (off by default; "
        "never generates)",
    )
    parser.add_argument(
        "--report", type=Path, help="also write the JSON report to this path"
    )
    parser.add_argument("--cache-dir", type=Path, default=CACHE_DIR)
    args = parser.parse_args(argv)

    if args.events_json:
        events = load_events_json(args.events_json)
        roots = resolve_path_roots({})
    else:
        catalog = load_catalog(args.catalog)
        events = catalog["events"]
        roots = resolve_path_roots(catalog)

    if args.ids:
        wanted = {part for token in args.ids for part in token.split(",") if part}
        events = [e for e in events if isinstance(e, dict) and e.get("id") in wanted]
        missing = wanted - {e.get("id") for e in events}
        if missing:
            print(f"WARNING: ids not in catalog: {sorted(missing)}", file=sys.stderr)

    rows, skipped_no_id = resolve_events(
        events, roots, args.cache_dir, allow_rafiki=args.allow_rafiki
    )

    errors = 0
    if args.execute:
        args.cache_dir.mkdir(parents=True, exist_ok=True)
        errors = execute_rows(rows, args.cache_dir, args.allow_rafiki)

    report = json.dumps(rows, indent=2)
    print(report)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(report + "\n", encoding="utf-8")

    counts: dict[str, int] = {}
    for row in rows:
        counts[row["source"]] = counts.get(row["source"], 0) + 1
    fetched = sum(1 for row in rows if row["fetched"])
    summary = " ".join(f"{key}={counts[key]}" for key in sorted(counts))
    print(
        f"Mode: {'EXECUTE' if args.execute else 'DRY-RUN'} | events={len(rows)} "
        f"{summary} fetched={fetched} errors={errors} skipped_no_id={skipped_no_id}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
