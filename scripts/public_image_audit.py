#!/usr/bin/env python3
"""Audit public-rendered images on kriskrug.co posts/pages.

Default mode is read-only. Live media alt writes require --execute plus an exact
media-alt JSON file; crawl findings are never auto-applied.
"""

from __future__ import annotations

import argparse
import base64
import csv
import dataclasses
import html
import json
import os
import re
import sys
import time
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import requests


REPO_ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = REPO_ROOT / "scripts" / "notion-to-wp" / ".env"
DEFAULT_BASE_URL = "https://kriskrug.co"
DEFAULT_URLS = (
    "/",
    "/blog/",
    "/home/",
    "/speaking/",
    "/generative-ai-services/",
    "/contact/",
    "/photography/",
    "/flickr-photographr-badge/",
)
IMAGE_EXT_RE = re.compile(r"\.(?:avif|gif|jpe?g|png|svg|webp)(?:$|[?#])", re.I)
MEDIA_ID_RE = re.compile(r"\bwp-image-(\d+)\b")


@dataclasses.dataclass
class RenderedImage:
    page_url: str
    page_kind: str
    page_id: int | None
    page_slug: str
    src: str
    alt: str | None
    media_id: int | None
    loading: str
    has_srcset: bool
    classes: str
    role: str
    width: str
    height: str
    status: int | None = None
    content_length: int | None = None

    @property
    def alt_state(self) -> str:
        if self.is_decorative:
            return "decorative-empty"
        if self.alt is None:
            return "missing-attr"
        if self.alt.strip() == "":
            return "empty"
        if is_filename_style_alt(self.alt, self.src):
            return "filename-style"
        return "ok"

    @property
    def is_decorative(self) -> bool:
        if self.alt is None or self.alt.strip() != "":
            return False
        haystack = f"{self.classes} {self.role} {self.src}".lower()
        decorative_markers = (
            "aurora-brand-logo",
            "custom-logo",
            "site-logo",
            "pixel",
            "tracking",
            "transparent",
            "spacer",
        )
        return any(marker in haystack for marker in decorative_markers)

    @property
    def oversize(self) -> bool:
        return bool(self.content_length and self.content_length > 500_000)


class ImageParser(HTMLParser):
    def __init__(self, page_url: str):
        super().__init__()
        self.page_url = page_url
        self.images: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "img":
            return
        data = {k.lower(): (v or "") for k, v in attrs}
        if data.get("src"):
            self.images.append(data)


def parse_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def auth_session(base_url: str) -> requests.Session:
    env = parse_env(ENV_PATH)
    user = env.get("WP_USER") or os.environ.get("WP_USER")
    password = (env.get("WP_APP_PASSWORD") or os.environ.get("WP_APP_PASSWORD") or "").replace(" ", "")
    if not user or not password:
        raise SystemExit(f"Missing WP credentials in {ENV_PATH} or environment")
    session = requests.Session()
    token = base64.b64encode(f"{user}:{password}".encode("utf-8")).decode("utf-8")
    session.headers.update({"Authorization": f"Basic {token}"})
    session.headers.update({"User-Agent": "KrisKrugPublicImageAudit/1.0"})
    session.base_url = base_url.rstrip("/")  # type: ignore[attr-defined]
    return session


def public_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"User-Agent": "KrisKrugPublicImageAudit/1.0"})
    return session


def normalize_filenameish(value: str) -> str:
    value = html.unescape(value).lower()
    value = re.sub(r"\.[a-z0-9]{2,5}$", "", value)
    return re.sub(r"[^a-z0-9]+", "", value)


def image_basename(src: str) -> str:
    path = urlsplit(html.unescape(src)).path.rstrip("/")
    return Path(path).name


def is_filename_style_alt(alt: str, src: str) -> bool:
    alt_raw = html.unescape(alt).strip()
    if not IMAGE_EXT_RE.search(alt_raw) and "-" not in alt_raw and "_" not in alt_raw:
        return False
    alt_norm = normalize_filenameish(alt)
    base_norm = normalize_filenameish(image_basename(src))
    if not alt_norm or not base_norm or len(alt_norm) < 8:
        return False
    return alt_norm == base_norm or alt_norm in base_norm or base_norm in alt_norm


def cachebust_url(url: str) -> str:
    split = urlsplit(url)
    query = dict(parse_qsl(split.query, keep_blank_values=True))
    query["cachebust"] = str(int(time.time()))
    return urlunsplit((split.scheme, split.netloc, split.path, urlencode(query), split.fragment))


def fetch_html(session: requests.Session, url: str, timeout: int, max_bytes: int = 2_000_000) -> str:
    response = session.get(url, stream=True, timeout=(timeout, timeout))
    response.raise_for_status()
    chunks: list[bytes] = []
    total = 0
    for chunk in response.iter_content(chunk_size=65536):
        if not chunk:
            continue
        chunks.append(chunk)
        total += len(chunk)
        if total >= max_bytes:
            break
    encoding = response.encoding or "utf-8"
    return b"".join(chunks).decode(encoding, "replace")


def absolute_url(base_url: str, url: str) -> str:
    if url.startswith("http://") or url.startswith("https://"):
        return url
    if url.startswith("//"):
        return "https:" + url
    return base_url.rstrip("/") + "/" + url.lstrip("/")


def media_id_from_class(classes: str) -> int | None:
    match = MEDIA_ID_RE.search(classes)
    return int(match.group(1)) if match else None


def image_probe(session: requests.Session, src: str, timeout: int) -> tuple[int | None, int | None]:
    try:
        response = session.head(src, allow_redirects=True, timeout=timeout)
        if response.status_code in (405, 429) or response.status_code >= 500:
            response = session.get(src, stream=True, timeout=timeout)
        length_raw = response.headers.get("content-length")
        length = int(length_raw) if length_raw and length_raw.isdigit() else None
        return response.status_code, length
    except requests.RequestException:
        return None, None


def fetch_public_items(base_url: str, kinds: list[str], ids: list[int], limit: int, since: str) -> list[dict[str, Any]]:
    session = public_session()
    items: list[dict[str, Any]] = []
    for kind in kinds:
        endpoint = "posts" if kind == "post" else "pages"
        if ids:
            for item_id in ids:
                response = session.get(
                    f"{base_url}/wp-json/wp/v2/{endpoint}/{item_id}",
                    params={"_fields": "id,slug,link,title,type,date"},
                    timeout=30,
                )
                if response.status_code == 200:
                    items.append(response.json())
            continue

        page = 1
        while len([i for i in items if i.get("type") == kind]) < limit:
            params: dict[str, Any] = {
                "status": "publish",
                "per_page": min(100, limit),
                "page": page,
                "_fields": "id,slug,link,title,type,date",
            }
            if kind == "post" and since:
                params["after"] = f"{since}T00:00:00"
            response = session.get(f"{base_url}/wp-json/wp/v2/{endpoint}", params=params, timeout=30)
            if response.status_code != 200:
                break
            batch = response.json()
            if not batch:
                break
            items.extend(batch)
            if page >= int(response.headers.get("X-WP-TotalPages", "1")):
                break
            page += 1
    return items[: limit * max(1, len(kinds))]


def item_title(item: dict[str, Any]) -> str:
    title = item.get("title") or {}
    if isinstance(title, dict):
        return re.sub(r"\s+", " ", html.unescape(title.get("rendered", ""))).strip()
    return str(title)


def collect_urls(args: argparse.Namespace) -> list[dict[str, Any]]:
    base_url = args.base_url.rstrip("/")
    if args.urls:
        return [
            {
                "id": None,
                "slug": urlsplit(url).path.strip("/") or "home",
                "link": absolute_url(base_url, url),
                "type": "url",
                "title": {"rendered": url},
            }
            for url in args.urls
        ]
    if not args.ids and args.default_urls:
        return [
            {
                "id": None,
                "slug": path.strip("/") or "home",
                "link": absolute_url(base_url, path),
                "type": "url",
                "title": {"rendered": path},
            }
            for path in DEFAULT_URLS
        ]
    return fetch_public_items(base_url, args.kind, args.ids, args.limit, args.since)


def audit_images(args: argparse.Namespace) -> list[RenderedImage]:
    session = public_session()
    rows: list[RenderedImage] = []
    for item in collect_urls(args):
        page_url = str(item["link"])
        try:
            html_text = fetch_html(session, cachebust_url(page_url), args.timeout)
        except requests.RequestException:
            continue
        parser = ImageParser(page_url)
        parser.feed(html_text)
        for attrs in parser.images:
            src = absolute_url(args.base_url, attrs.get("src", ""))
            status = None
            content_length = None
            if args.check_urls and IMAGE_EXT_RE.search(src):
                status, content_length = image_probe(session, src, args.timeout)
            rows.append(
                RenderedImage(
                    page_url=page_url,
                    page_kind=str(item.get("type") or "url"),
                    page_id=item.get("id"),
                    page_slug=str(item.get("slug") or ""),
                    src=src,
                    alt=attrs.get("alt") if "alt" in attrs else None,
                    media_id=media_id_from_class(attrs.get("class", "")),
                    loading=attrs.get("loading", ""),
                    has_srcset=bool(attrs.get("srcset")),
                    classes=attrs.get("class", ""),
                    role=attrs.get("role", ""),
                    width=attrs.get("width", ""),
                    height=attrs.get("height", ""),
                    status=status,
                    content_length=content_length,
                )
            )
    return rows


def summarize(rows: list[RenderedImage]) -> dict[str, int]:
    return {
        "pages": len({r.page_url for r in rows}),
        "images": len(rows),
        "missing_attr": sum(1 for r in rows if r.alt_state == "missing-attr"),
        "empty_alt": sum(1 for r in rows if r.alt_state == "empty"),
        "decorative_empty": sum(1 for r in rows if r.alt_state == "decorative-empty"),
        "filename_style": sum(1 for r in rows if r.alt_state == "filename-style"),
        "srcset": sum(1 for r in rows if r.has_srcset),
        "lazy": sum(1 for r in rows if r.loading.lower() == "lazy"),
        "broken": sum(1 for r in rows if r.status is not None and r.status >= 400),
        "oversize": sum(1 for r in rows if r.oversize),
    }


def row_dict(row: RenderedImage) -> dict[str, Any]:
    return {
        "page_url": row.page_url,
        "page_kind": row.page_kind,
        "page_id": row.page_id,
        "page_slug": row.page_slug,
        "media_id": row.media_id,
        "alt_state": row.alt_state,
        "alt": row.alt or "",
        "src": row.src,
        "loading": row.loading,
        "has_srcset": row.has_srcset,
        "status": row.status,
        "content_length": row.content_length,
        "oversize": row.oversize,
    }


def render_markdown(rows: list[RenderedImage]) -> str:
    stats = summarize(rows)
    flagged = [r for r in rows if r.alt_state not in ("ok", "decorative-empty") or r.oversize or (r.status and r.status >= 400)]
    lines = [
        "# Public Image Audit",
        "",
        f"- Pages scanned: {stats['pages']}",
        f"- Images found: {stats['images']}",
        f"- Missing alt attribute: {stats['missing_attr']}",
        f"- Empty non-decorative alt: {stats['empty_alt']}",
        f"- Decorative empty alt: {stats['decorative_empty']}",
        f"- Filename-style alt: {stats['filename_style']}",
        f"- Images with srcset: {stats['srcset']}",
        f"- Lazy-loaded images: {stats['lazy']}",
        f"- Broken checked image URLs: {stats['broken']}",
        f"- Checked images over 500 KB response size: {stats['oversize']}",
        "",
        "## Flagged Images",
        "",
        "| Page | Media ID | State | Status | Bytes | Alt | Source |",
        "|---|---:|---|---:|---:|---|---|",
    ]
    for row in flagged[:200]:
        alt = (row.alt or "").replace("|", "\\|")[:80]
        src = row.src.replace("|", "%7C")[:120]
        lines.append(
            f"| {row.page_url} | {row.media_id or ''} | {row.alt_state}{' oversize' if row.oversize else ''} | "
            f"{row.status or ''} | {row.content_length or ''} | {alt} | {src} |"
        )
    if not flagged:
        lines.append("| - | - | - | - | - | - | - |")
    return "\n".join(lines) + "\n"


def write_output(args: argparse.Namespace, rows: list[RenderedImage]) -> None:
    if args.format == "json":
        output = json.dumps({"summary": summarize(rows), "images": [row_dict(r) for r in rows]}, indent=2)
    elif args.format == "csv":
        import io

        buffer = io.StringIO()
        writer = csv.DictWriter(buffer, fieldnames=list(row_dict(rows[0]).keys()) if rows else ["page_url"])
        writer.writeheader()
        for row in rows:
            writer.writerow(row_dict(row))
        output = buffer.getvalue()
    else:
        output = render_markdown(rows)

    if args.output:
        path = Path(args.output)
        if not path.is_absolute():
            path = REPO_ROOT / path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(output, encoding="utf-8")
        print(f"report={path}")
    else:
        print(output)


def execute_media_alt_file(args: argparse.Namespace) -> None:
    if not args.media_alt_file:
        raise SystemExit("--execute requires --media-alt-file with exact media_id/alt_text entries")
    data = json.loads(Path(args.media_alt_file).read_text(encoding="utf-8"))
    entries = data.get("items", data)
    if not isinstance(entries, list):
        raise SystemExit("media alt file must be a list or {'items': [...]}")
    session = auth_session(args.base_url)
    updates = []
    for entry in entries:
        media_id = int(entry["media_id"])
        alt_text = str(entry["alt_text"]).strip()
        if not alt_text:
            raise SystemExit(f"media {media_id} alt_text is empty")
        before = session.get(f"{session.base_url}/wp-json/wp/v2/media/{media_id}", params={"context": "edit", "_fields": "id,alt_text"}, timeout=30)  # type: ignore[attr-defined]
        before.raise_for_status()
        old_alt = before.json().get("alt_text", "")
        response = session.post(f"{session.base_url}/wp-json/wp/v2/media/{media_id}", json={"alt_text": alt_text}, timeout=60)  # type: ignore[attr-defined]
        response.raise_for_status()
        after = session.get(f"{session.base_url}/wp-json/wp/v2/media/{media_id}", params={"context": "edit", "_fields": "id,alt_text"}, timeout=30)  # type: ignore[attr-defined]
        after.raise_for_status()
        new_alt = after.json().get("alt_text", "")
        if new_alt != alt_text:
            raise SystemExit(f"media {media_id} readback mismatch")
        updates.append({"media_id": media_id, "old_alt": old_alt, "new_alt": new_alt})
    print(json.dumps({"updated": updates}, indent=2))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--kind", default="post,page", type=lambda value: [v.strip() for v in value.split(",") if v.strip()])
    parser.add_argument("--ids", default="", type=lambda value: [int(v) for v in value.split(",") if v.strip()])
    parser.add_argument("--urls", default="", type=lambda value: [v.strip() for v in value.split(",") if v.strip()])
    parser.add_argument("--default-urls", action="store_true", help="Scan the high-visibility default URL set.")
    parser.add_argument("--since", default="2025-01-01")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--check-urls", action="store_true")
    parser.add_argument("--format", choices=("markdown", "json", "csv"), default="markdown")
    parser.add_argument("--output", default="")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--media-alt-file", default="")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.execute:
        execute_media_alt_file(args)
        return
    rows = audit_images(args)
    write_output(args, rows)


if __name__ == "__main__":
    main()
