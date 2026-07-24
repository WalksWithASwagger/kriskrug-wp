#!/usr/bin/env python3
"""Build a private, deduplicated review catalog from a photo archive."""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import io
import json
import mimetypes
import os
import shutil
import subprocess
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import BinaryIO, Iterator


IMAGE_EXTENSIONS = {".avif", ".gif", ".heic", ".heif", ".jpeg", ".jpg", ".png", ".tif", ".tiff", ".webp"}
VIDEO_EXTENSIONS = {".3gp", ".avi", ".m4v", ".mkv", ".mov", ".mp4", ".webm"}
MEDIA_EXTENSIONS = IMAGE_EXTENSIONS | VIDEO_EXTENSIONS
EXIF_FIELDS = (
    "ImageWidth",
    "ImageHeight",
    "Orientation",
    "DateTimeOriginal",
    "CreateDate",
    "ModifyDate",
    "Make",
    "Model",
    "LensModel",
    "Artist",
    "Creator",
    "Credit",
    "Copyright",
    "GPSLatitude",
    "GPSLongitude",
    "Title",
    "Description",
    "Caption-Abstract",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_stream(stream: BinaryIO) -> str:
    digest = hashlib.sha256()
    for chunk in iter(lambda: stream.read(1024 * 1024), b""):
        digest.update(chunk)
    return digest.hexdigest()


def sha256_file(path: Path) -> str:
    with path.open("rb") as stream:
        return sha256_stream(stream)


def media_kind(name: str) -> str | None:
    suffix = Path(name).suffix.lower()
    if suffix in IMAGE_EXTENSIONS:
        return "image"
    if suffix in VIDEO_EXTENSIONS:
        return "video"
    return None


def parse_exif_datetime(value: object) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    normalized = value.strip()
    if len(normalized) >= 19 and normalized[4] == ":" and normalized[7] == ":":
        normalized = f"{normalized[:4]}-{normalized[5:7]}-{normalized[8:]}"
    try:
        return datetime.fromisoformat(normalized).isoformat()
    except ValueError:
        return None


def sidecar_datetime(sidecar: dict[str, object]) -> str | None:
    for field in ("photoTakenTime", "creationTime"):
        value = sidecar.get(field)
        if not isinstance(value, dict):
            continue
        timestamp = value.get("timestamp")
        if isinstance(timestamp, str) and timestamp.isdigit():
            return datetime.fromtimestamp(int(timestamp), tz=timezone.utc).isoformat().replace("+00:00", "Z")
    return None


def captured_at(
    metadata: dict[str, object],
    fallback: datetime | None,
    sidecar: dict[str, object] | None = None,
) -> tuple[str | None, str]:
    for field in ("DateTimeOriginal", "CreateDate", "ModifyDate"):
        parsed = parse_exif_datetime(metadata.get(field))
        if parsed:
            return parsed, f"exif:{field}"
    parsed_sidecar = sidecar_datetime(sidecar or {})
    if parsed_sidecar:
        return parsed_sidecar, "google-sidecar"
    if fallback:
        return fallback.replace(microsecond=0).isoformat(), "archive-mtime"
    return None, "unknown"


def run_exiftool(path: Path) -> dict[str, object]:
    if not shutil.which("exiftool"):
        return {}
    command = ["exiftool", "-j", "-n"] + [f"-{field}" for field in EXIF_FIELDS] + [str(path)]
    try:
        result = subprocess.run(command, check=False, capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        return {}
    if result.returncode != 0:
        return {}
    try:
        rows = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {}
    if not rows:
        return {}
    return {key: value for key, value in rows[0].items() if key != "SourceFile"}


def make_thumbnail(source: Path, destination: Path, max_size: int = 640) -> bool:
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        from PIL import Image, ImageOps

        with Image.open(source) as image:
            image = ImageOps.exif_transpose(image)
            image.thumbnail((max_size, max_size))
            if image.mode not in ("RGB", "L"):
                image = image.convert("RGB")
            image.save(destination, "JPEG", quality=84, optimize=True)
        return True
    except (ImportError, OSError, ValueError):
        pass

    if not shutil.which("sips"):
        return False
    try:
        result = subprocess.run(
            ["sips", "-s", "format", "jpeg", "-Z", str(max_size), str(source), "--out", str(destination)],
            check=False,
            capture_output=True,
            text=True,
            timeout=60,
        )
    except subprocess.TimeoutExpired:
        return False
    return result.returncode == 0 and destination.exists()


def run_ocr(source: Path, fallback_thumbnail: Path | None = None) -> str:
    if not shutil.which("tesseract"):
        return ""
    targets = [source]
    if fallback_thumbnail and fallback_thumbnail.exists():
        targets.append(fallback_thumbnail)
    for target in targets:
        try:
            result = subprocess.run(
                ["tesseract", str(target), "stdout", "--psm", "11", "tsv"],
                check=False,
                capture_output=True,
                text=True,
                timeout=90,
            )
        except subprocess.TimeoutExpired:
            continue
        cleaned = parse_tesseract_tsv(result.stdout)
        if result.returncode == 0 and cleaned:
            return cleaned[:4000]
    return ""


def parse_tesseract_tsv(value: str, minimum_confidence: float = 60.0) -> str:
    lines: dict[tuple[str, str, str], list[str]] = {}
    try:
        rows = csv.DictReader(io.StringIO(value), delimiter="\t")
        for row in rows:
            text = (row.get("text") or "").strip()
            try:
                confidence = float(row.get("conf") or -1)
            except ValueError:
                continue
            short_signal = text.upper() in {"AI", "BC", "CBC", "SFU", "TED"}
            if confidence < minimum_confidence or (len(text) < 3 and not short_signal) or not any(character.isalnum() for character in text):
                continue
            key = (row.get("block_num") or "", row.get("par_num") or "", row.get("line_num") or "")
            lines.setdefault(key, []).append(text)
    except csv.Error:
        return ""
    return "\n".join(" ".join(words) for words in lines.values())


def zip_timestamp(info: zipfile.ZipInfo) -> datetime | None:
    try:
        return datetime(*info.date_time)
    except (TypeError, ValueError):
        return None


def iter_zip_media(archive: zipfile.ZipFile) -> Iterator[zipfile.ZipInfo]:
    for info in archive.infolist():
        if info.is_dir() or info.filename.startswith("__MACOSX/"):
            continue
        if media_kind(info.filename):
            yield info


def google_sidecar(
    archive: zipfile.ZipFile,
    member: str,
    names: set[str] | None = None,
) -> dict[str, object]:
    names = names if names is not None else set(archive.namelist())
    candidates = (f"{member}.json", str(Path(member).with_suffix(".json")))
    for candidate in candidates:
        if candidate not in names:
            continue
        try:
            value = json.loads(archive.read(candidate))
        except (KeyError, UnicodeDecodeError, json.JSONDecodeError):
            continue
        if isinstance(value, dict):
            return value
    return {}


def load_jsonl(path: Path) -> dict[str, dict[str, object]]:
    if not path.exists():
        return {}
    records: dict[str, dict[str, object]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            record = json.loads(line)
            records[str(record["asset_id"])] = record
    return records


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(f"{path.suffix}.tmp")
    temporary.write_text(content, encoding="utf-8")
    os.replace(temporary, path)


def review_record(record: dict[str, object]) -> dict[str, object]:
    metadata = dict(record.get("metadata") or {})
    metadata.pop("GPSLatitude", None)
    metadata.pop("GPSLongitude", None)
    return {
        "asset_id": record["asset_id"],
        "filename": record["filename"],
        "media_kind": record["media_kind"],
        "mime_type": record.get("mime_type"),
        "size_bytes": record["size_bytes"],
        "captured_at": record.get("captured_at"),
        "captured_at_source": record.get("captured_at_source"),
        "event_group": record.get("event_group"),
        "metadata": metadata,
        "ocr_text": record.get("ocr_text", ""),
        "thumbnail": record.get("thumbnail"),
        "review_status": record.get("review_status", "unreviewed"),
        "caption_draft": record.get("caption_draft"),
        "identity_clues": record.get("identity_clues", []),
        "site_uses": record.get("site_uses", []),
        "source_title": record.get("source_title"),
        "source_description": record.get("source_description"),
        "event_name": record.get("event_name"),
    }


def render_review_html(records: list[dict[str, object]], title: str) -> str:
    cards: list[str] = []
    for record in records:
        asset_id = str(record["asset_id"])
        raw_filename = str(record["filename"])
        raw_event_group = str(record.get("event_group") or "unclustered")
        raw_ocr = str(record.get("ocr_text") or "")
        filename = html.escape(raw_filename)
        captured = html.escape(str(record.get("captured_at") or "date unknown"))
        event_group = html.escape(raw_event_group)
        ocr = html.escape(raw_ocr)
        data_search = html.escape(f"{raw_filename.lower()} {raw_event_group.lower()} {raw_ocr.lower()}", quote=True)
        thumb = record.get("thumbnail")
        image = f'<img loading="lazy" src="{html.escape(str(thumb))}" alt="Private review thumbnail for {filename}">' if thumb else '<div class="missing">No thumbnail</div>'
        cards.append(
            f'<article data-search="{data_search}">'
            f'{image}<div class="details"><code>{asset_id[:12]}</code><h2>{filename}</h2>'
            f'<p>{captured}<br>{event_group}</p><pre>{ocr or "No OCR text"}</pre></div></article>'
        )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} — private photo review</title>
<style>
:root{{color-scheme:dark}}body{{margin:0;background:#101015;color:#eee;font:15px/1.45 system-ui,sans-serif}}
header{{position:sticky;top:0;z-index:2;padding:18px 24px;background:#101015ee;border-bottom:1px solid #333}}
h1{{margin:0 0 10px;font-size:22px}}header p{{margin:0 0 10px;color:#aaa}}input{{width:min(720px,90%);padding:10px;border:1px solid #555;border-radius:8px;background:#191920;color:#fff}}
main{{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:16px;padding:20px}}
article{{overflow:hidden;border:1px solid #30303a;border-radius:10px;background:#17171d}}article img,.missing{{width:100%;height:220px;object-fit:cover;background:#08080a;display:grid;place-items:center}}
.details{{padding:12px}}h2{{margin:6px 0;font-size:15px;overflow-wrap:anywhere}}p{{color:#aaa}}code{{color:#55d6be}}pre{{max-height:90px;overflow:auto;white-space:pre-wrap;color:#d5c58a;font:12px/1.35 ui-monospace,monospace}}
</style></head><body><header><h1>{html.escape(title)}</h1><p>Private working catalog. Identity clues are unverified until evidence is reviewed; nothing here is approved for publication.</p><input id="q" type="search" placeholder="Filter filename, date/event group, or OCR text"></header>
<main>{''.join(cards)}</main><script>const q=document.querySelector('#q');q.addEventListener('input',()=>{{const v=q.value.toLowerCase();document.querySelectorAll('article').forEach(c=>c.hidden=!c.dataset.search.includes(v));}});</script>
</body></html>"""


def write_contact_sheets(records: list[dict[str, object]], review_root: Path) -> int:
    try:
        from PIL import Image, ImageDraw, ImageOps
    except ImportError:
        return 0

    sheets_root = review_root / "sheets"
    sheets_root.mkdir(parents=True, exist_ok=True)
    usable = [record for record in records if record.get("thumbnail")]
    per_sheet = 24
    columns, card_width, card_height = 4, 300, 245
    count = 0
    for start in range(0, len(usable), per_sheet):
        batch = usable[start : start + per_sheet]
        rows = (len(batch) + columns - 1) // columns
        sheet = Image.new("RGB", (columns * card_width, rows * card_height), "#101015")
        draw = ImageDraw.Draw(sheet)
        for index, record in enumerate(batch):
            row, column = divmod(index, columns)
            left, top = column * card_width, row * card_height
            source = review_root / str(record["thumbnail"])
            try:
                with Image.open(source) as thumb:
                    thumb = ImageOps.exif_transpose(thumb).convert("RGB")
                    thumb.thumbnail((card_width - 12, 190))
                    x = left + (card_width - thumb.width) // 2
                    sheet.paste(thumb, (x, top + 6))
            except OSError:
                pass
            label = f"{str(record['asset_id'])[:10]}  {str(record['filename'])[:34]}"
            draw.text((left + 8, top + 204), label, fill="#f1f1f1")
            draw.text((left + 8, top + 222), str(record.get("captured_at") or "date unknown")[:19], fill="#a9a9b2")
        destination = sheets_root / f"sheet-{start // per_sheet + 1:04d}.jpg"
        sheet.save(destination, "JPEG", quality=88, optimize=True)
        count += 1
    return count


def write_catalog_outputs(
    library_root: Path,
    records: dict[str, dict[str, object]],
    manifest: dict[str, object],
    title: str,
) -> None:
    private_root = library_root / "private"
    review_root = library_root / "review"
    ordered = sorted(records.values(), key=lambda item: (str(item.get("captured_at") or ""), str(item["filename"])), reverse=True)
    atomic_write(private_root / "catalog.jsonl", "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in ordered))
    atomic_write(private_root / "manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n")

    annotation_path = review_root / "annotations.jsonl"
    prior_annotations = load_jsonl(annotation_path)
    review = []
    for row in ordered:
        item = review_record(row)
        annotation = prior_annotations.get(str(row["asset_id"]), {})
        for field in ("caption_draft", "identity_clues", "site_uses", "review_status"):
            if field in annotation:
                item[field] = annotation[field]
        if annotation.get("event_name"):
            item["event_name"] = annotation["event_name"]
            item["event_group"] = annotation["event_name"]
        review.append(item)
    atomic_write(review_root / "catalog.json", json.dumps(review, ensure_ascii=False, indent=2) + "\n")
    atomic_write(review_root / "index.html", render_review_html(review, title))

    csv_path = review_root / "catalog.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=("asset_id", "filename", "captured_at", "event_group", "review_status", "ocr_text"))
        writer.writeheader()
        for row in review:
            writer.writerow({key: row.get(key) for key in writer.fieldnames})

    annotations = [
        {
            "asset_id": row["asset_id"],
            "caption_draft": row.get("caption_draft"),
            "event_name": row.get("event_name"),
            "identity_clues": row.get("identity_clues", []),
            "site_uses": row.get("site_uses", []),
            "review_status": row.get("review_status", "unreviewed"),
        }
        for row in review
    ]
    atomic_write(annotation_path, "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in annotations))
    manifest["contact_sheet_count"] = write_contact_sheets(review, review_root)
    atomic_write(private_root / "manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def ingest_zip(archive_path: Path, library_root: Path, title: str, run_ocr_enabled: bool) -> dict[str, object]:
    archive_path = archive_path.expanduser().resolve()
    library_root = library_root.expanduser().resolve()
    private_root = library_root / "private"
    thumbnails_root = library_root / "review" / "thumbnails"
    private_root.mkdir(parents=True, exist_ok=True)
    thumbnails_root.mkdir(parents=True, exist_ok=True)

    catalog_path = private_root / "catalog.jsonl"
    records = load_jsonl(catalog_path)
    archive_hash = sha256_file(archive_path)
    started_at = utc_now()
    processed = duplicates = 0

    with zipfile.ZipFile(archive_path) as archive, tempfile.TemporaryDirectory(prefix="kk-photo-catalog-") as temporary:
        media = list(iter_zip_media(archive))
        archive_names = set(archive.namelist())
        for info in media:
            with archive.open(info) as stream:
                asset_id = sha256_stream(stream)
            occurrence = {"archive_sha256": archive_hash, "member": info.filename}
            if asset_id in records:
                sources = records[asset_id].setdefault("sources", [])
                if occurrence not in sources:
                    sources.append(occurrence)
                duplicates += 1
                continue

            suffix = Path(info.filename).suffix.lower()
            temporary_path = Path(temporary) / f"asset{suffix}"
            with archive.open(info) as source, temporary_path.open("wb") as destination:
                shutil.copyfileobj(source, destination, length=1024 * 1024)

            kind = media_kind(info.filename)
            metadata = run_exiftool(temporary_path)
            sidecar = google_sidecar(archive, info.filename, archive_names)
            captured, captured_source = captured_at(metadata, zip_timestamp(info), sidecar)
            thumbnail_relative: str | None = None
            thumbnail_path: Path | None = None
            if kind == "image":
                thumbnail_relative = f"thumbnails/{asset_id[:20]}.jpg"
                thumbnail_path = library_root / "review" / thumbnail_relative
                if not make_thumbnail(temporary_path, thumbnail_path):
                    thumbnail_relative = None
                    thumbnail_path = None

            ocr_text = run_ocr(temporary_path, thumbnail_path) if run_ocr_enabled and kind == "image" else ""
            mime_type = mimetypes.guess_type(info.filename)[0] or "application/octet-stream"
            event_group = captured[:10] if captured else "date-unknown"
            records[asset_id] = {
                "asset_id": asset_id,
                "filename": Path(info.filename).name,
                "archive_member": info.filename,
                "media_kind": kind,
                "mime_type": mime_type,
                "size_bytes": info.file_size,
                "captured_at": captured,
                "captured_at_source": captured_source,
                "event_group": event_group,
                "metadata": metadata,
                "google_sidecar": sidecar,
                "source_title": sidecar.get("title") if sidecar else None,
                "source_description": sidecar.get("description") if sidecar else None,
                "ocr_text": ocr_text,
                "thumbnail": thumbnail_relative,
                "sources": [occurrence],
                "review_status": "unreviewed",
                "caption_draft": None,
                "identity_clues": [],
                "site_uses": [],
            }
            processed += 1
            temporary_path.unlink(missing_ok=True)

    manifest = {
        "schema_version": 1,
        "title": title,
        "privacy": "private-master",
        "publication_gate": "explicit asset approval required",
        "archive": {
            "path": str(archive_path),
            "sha256": archive_hash,
            "size_bytes": archive_path.stat().st_size,
        },
        "started_at": started_at,
        "completed_at": utc_now(),
        "unique_asset_count": len(records),
        "new_asset_count": processed,
        "duplicate_occurrence_count": duplicates,
        "ocr_enabled": run_ocr_enabled,
    }
    write_catalog_outputs(library_root, records, manifest, title)
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path, help="Google Photos album ZIP")
    parser.add_argument("--library-root", type=Path, required=True, help="Private output directory outside Git")
    parser.add_argument("--title", default="KK Photos", help="Album label for the review catalog")
    parser.add_argument("--ocr", action="store_true", help="Run local Tesseract OCR on every image")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if not args.archive.is_file():
        raise SystemExit(f"Archive not found: {args.archive}")
    if not zipfile.is_zipfile(args.archive):
        raise SystemExit(f"Not a ZIP archive: {args.archive}")
    manifest = ingest_zip(args.archive, args.library_root, args.title, args.ocr)
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
