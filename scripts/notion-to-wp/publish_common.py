"""Shared helpers for one-off publish_*.py scripts.

Orchestration only: image manifests, text-post assembly, term/media ID
validation, and SEO meta shaping. Gutenberg markup stays in wp_blocks.py.
"""
from __future__ import annotations

import html
import pathlib
import re
import sys
from dataclasses import dataclass
from typing import Any

from connector_payload import normalize_seo_meta
from kk_notion_to_wp import slugify
from wp_blocks import heading, inline, separator

MARKDOWN_IMG_IMAGES_RE = re.compile(r"^!\[(.+?)\]\(images/(.+?)\)$")


@dataclass(frozen=True)
class PublishFlags:
    execute: bool
    update: bool

    @property
    def write(self) -> bool:
        return self.execute or self.update


def parse_publish_argv(argv: list[str] | None = None) -> PublishFlags:
    """Parse --execute / --update consistently across one-off scripts."""
    args = list(sys.argv[1:] if argv is None else argv)
    return PublishFlags(execute="--execute" in args, update="--update" in args)


def split_body_blocks(body: str) -> list[str]:
    """Split post body on blank lines; return stripped non-empty blocks."""
    return [x.strip() for x in re.split(r"\n\s*\n", body) if x.strip()]


def paragraph_block(html_body: str) -> str:
    """Wrap ready HTML in a canonical wp:paragraph block."""
    return f"<!-- wp:paragraph -->\n<p>{html_body}</p>\n<!-- /wp:paragraph -->"


def render_paragraph_from_markdown(block: str) -> str:
    """Multiline markdown block → wp:paragraph with <br> between lines."""
    para = "<br>".join(inline(line.strip()) for line in block.split("\n"))
    return paragraph_block(para)


def render_text_post(body: str) -> str:
    """Text-only post assembler: skip first H1, map ---/##/###/else via wp_blocks."""
    out: list[str] = []
    seen_title = False
    for block in split_body_blocks(body):
        if block.startswith("# ") and not seen_title:
            seen_title = True
            continue
        if block == "---":
            out.append(separator())
        elif block.startswith("## "):
            out.append(heading(inline(block[3:].strip()), level=2))
        elif block.startswith("### "):
            out.append(heading(inline(block[4:].strip()), level=3))
        else:
            out.append(render_paragraph_from_markdown(block))
    return "\n\n".join(out)


def parse_markdown_image_order(
    body: str,
    pattern: re.Pattern[str] | None = None,
) -> list[tuple[str, str]]:
    """Return [(filename, alt), ...] in document order from markdown image lines."""
    pat = pattern or MARKDOWN_IMG_IMAGES_RE
    order: list[tuple[str, str]] = []
    for block in split_body_blocks(body):
        match = pat.match(block)
        if match:
            order.append((match.group(2), match.group(1)))
    return order


def load_captions(directory: pathlib.Path) -> dict[str, str]:
    """Parse captions.txt lines as filename|alt."""
    caps: dict[str, str] = {}
    path = directory / "captions.txt"
    if not path.exists():
        return caps
    for line in path.read_text().splitlines():
        if "|" in line:
            filename, alt = line.split("|", 1)
            caps[filename.strip()] = alt.strip()
    return caps


def find_media_by_stem(
    wp: Any,
    stem: str,
    *,
    extensions: tuple[str, ...] = (".jpg", ".jpeg", ".png", ".webp"),
) -> tuple[int, str] | None:
    """Idempotent WP media lookup by basename stem (you_cant find_media logic)."""
    try:
        result = wp.s.get(
            f"{wp.base}/wp-json/wp/v2/media",
            params={"search": stem, "per_page": 10, "context": "edit"},
            timeout=30,
        ).json()
    except Exception:
        return None
    if not isinstance(result, list):
        return None
    for media in result:
        base = media.get("source_url", "").rsplit("/", 1)[-1]
        if base == f"{stem}.jpg" or base.startswith(stem):
            return int(media["id"]), media["source_url"]
        for ext in extensions:
            if base == f"{stem}{ext}":
                return int(media["id"]), media["source_url"]
    return None


def upload_image_manifest(
    wp: Any | None,
    items: list[tuple[str, str]],
    src_dir: pathlib.Path,
    *,
    write: bool,
    mime: str = "image/png",
) -> tuple[dict[str, dict[str, Any]], list[str]]:
    """Upload or dry-run stub. Returns {filename: {id, url}} and log lines."""
    uploaded: dict[str, dict[str, Any]] = {}
    log: list[str] = []
    for filename, alt in items:
        if write:
            if wp is None:
                raise SystemExit("[ABORT] write=True requires a WordPress client")
            media = wp.upload_media(src_dir / filename, alt=alt, mime=mime)
            uploaded[filename] = {"id": media["id"], "url": media["source_url"]}
            log.append(f"{filename} -> id={media['id']} {media['source_url']}")
        else:
            uploaded[filename] = {"id": 0, "url": f"DRYRUN/{filename}"}
    return uploaded, log


def load_photos_from_dir(
    wp: Any,
    stage_dir: pathlib.Path,
    subdir: str,
    *,
    write: bool,
    alt_from_slug: bool = False,
    photo_log: list[str] | None = None,
) -> list[tuple[int, str, str, str, str]]:
    """Load/upload photos under stage_dir/subdir.

    Returns (id, url, alt, caption, filename).
    """
    directory = stage_dir / subdir
    files = sorted(p for p in directory.glob("*.jpg") if not p.name.startswith("_"))
    caps = load_captions(directory)
    items: list[tuple[int, str, str, str, str]] = []
    log = photo_log if photo_log is not None else []
    for path in files:
        caption = caps.get(path.name, "")
        if alt_from_slug:
            alt = re.sub(r"^\d+-", "", path.stem).replace("-", " ") + " protest sign"
        else:
            alt = caption or path.stem
        if write:
            found = find_media_by_stem(wp, path.stem)
            if found:
                media_id, url = found
                log.append(f"{subdir}/{path.name} -> REUSE id={media_id}")
            else:
                media = wp.upload_media(path, alt=alt, mime="image/jpeg")
                media_id, url = media["id"], media["source_url"]
                log.append(f"{subdir}/{path.name} -> NEW id={media_id} {url}")
            items.append((media_id, url, alt, caption, path.name))
        else:
            items.append((0, f"DRYRUN/{path.name}", alt, caption, path.name))
    return items


def ensure_term_id(wp: Any, taxonomy: str, name: str) -> int:
    """HTML-unescape-safe term resolve/create (lifted from proximity term_id)."""
    slug = slugify(name)
    response = wp.s.get(
        f"{wp.base}/wp-json/wp/v2/{taxonomy}",
        params={"search": name, "per_page": 100},
        timeout=30,
    )
    response.raise_for_status()
    for term in response.json():
        if html.unescape(term.get("name", "")).lower() == name.lower() or term.get("slug", "") == slug:
            return int(term["id"])
    create = wp.s.post(
        f"{wp.base}/wp-json/wp/v2/{taxonomy}",
        json={"name": name, "slug": slug},
        timeout=30,
    )
    if create.status_code == 400:
        data = (create.json() or {}).get("data") or {}
        if data.get("term_id"):
            return int(data["term_id"])
    create.raise_for_status()
    return int(create.json()["id"])


def validate_term_ids(wp: Any, taxonomy: str, ids: list[int]) -> list[int]:
    """GET each term ID; raise SystemExit if any ID is missing."""
    validated: list[int] = []
    for term_id in ids:
        response = wp.s.get(
            f"{wp.base}/wp-json/wp/v2/{taxonomy}/{term_id}",
            timeout=30,
        )
        if response.status_code != 200:
            raise SystemExit(
                f"[ABORT] {taxonomy} id={term_id} not found "
                f"(HTTP {response.status_code}). Pass a valid --category-id / config id."
            )
        validated.append(int(term_id))
    return validated


def validate_media_id(wp: Any, media_id: int) -> int:
    """GET /media/{id}; raise SystemExit if absent."""
    response = wp.s.get(f"{wp.base}/wp-json/wp/v2/media/{media_id}", timeout=30)
    if response.status_code != 200:
        raise SystemExit(
            f"[ABORT] media id={media_id} not found "
            f"(HTTP {response.status_code}). Pass a valid --featured-media-id."
        )
    return int(media_id)


def resolve_category_ids(
    wp: Any,
    *,
    ids: list[int] | None = None,
    names: list[str] | None = None,
    create_missing: bool = False,
) -> list[int]:
    """Validate numeric IDs when provided; else resolve names via ensure_term_id."""
    if ids:
        return validate_term_ids(wp, "categories", ids)
    resolved: list[int] = []
    for name in names or []:
        if create_missing:
            resolved.append(ensure_term_id(wp, "categories", name))
        else:
            # Read-only resolve: ensure_term_id creates on miss; for names we still
            # need create-or-reuse behavior matching proximity.
            resolved.append(ensure_term_id(wp, "categories", name))
    return resolved


def resolve_featured_media(
    wp: Any,
    *,
    media_id: int | None = None,
    filename: str | None = None,
    uploaded: dict[str, dict[str, Any]] | None = None,
    write: bool,
) -> int | None:
    """Resolve featured from explicit ID (validated on write) or uploaded filename."""
    if media_id is not None:
        if write:
            return validate_media_id(wp, media_id)
        return int(media_id)
    if filename and uploaded and filename in uploaded:
        return int(uploaded[filename]["id"])
    return None


def build_seo_meta(meta_title: str, meta_description: str) -> dict[str, str]:
    """Return Jetpack SEO meta dict with normalize_seo_meta applied to both fields."""
    return {
        "jetpack_seo_html_title": normalize_seo_meta(meta_title),
        "advanced_seo_description": normalize_seo_meta(meta_description),
    }


def parse_int_arg(argv: list[str], flag: str, default: int | None = None) -> int | None:
    """Parse `--flag N` from argv; return default when absent."""
    if flag in argv:
        idx = argv.index(flag)
        if idx + 1 >= len(argv):
            raise SystemExit(f"[ABORT] {flag} requires an integer value")
        return int(argv[idx + 1])
    return default
