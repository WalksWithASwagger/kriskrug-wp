"""Shared helpers for one-off publish_*.py scripts.

Orchestration only: front matter, marker -> block dispatch, image manifests,
declared ID lookup, term/media ID validation, and SEO meta shaping. Gutenberg
markup stays in wp_blocks.py.
"""
from __future__ import annotations

import functools
import html
import json
import pathlib
import re
import sys
from dataclasses import dataclass
from typing import Any, Callable, Sequence

from connector_payload import normalize_seo_meta
from kk_notion_to_wp import slugify
from wp_blocks import heading, inline, separator

MARKDOWN_IMG_IMAGES_RE = re.compile(r"^!\[(.+?)\]\(images/(.+?)\)$")
PUBLISHER_IDS_PATH = pathlib.Path(__file__).resolve().parent / "publisher-ids.json"


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


def strip_frontmatter(raw: str) -> str:
    """Return the post body with a leading `---` YAML front matter block removed.

    Exactly the index-walk the one-off scripts each carried inline: find the
    closing `\\n---` after the opening fence and slice past it. Raises ValueError
    (as `str.index` always did) when the fences are missing, so a malformed
    post.md still fails loudly rather than publishing its own front matter.
    """
    fm_end = raw.index("\n---", raw.index("---") + 3)
    return raw[fm_end + 4:]


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


def raw_paragraph(block: str) -> str:
    """Single-line-ish paragraph: inline() the whole block, newlines preserved.

    This is publish_dc_protest_draft.py's paragraph shape. It differs from
    render_paragraph_from_markdown, which joins source lines with <br>. Both are
    kept because the difference is visible in already-shipped post bodies.
    """
    return paragraph_block(inline(block))


# ---------------------------------------------------------------------------
# marker -> block dispatch
# ---------------------------------------------------------------------------
# A handler is (matcher, render).
#   matcher: a compiled regex (matched against the block) or a callable
#            returning truthy for blocks it claims.
#   render:  callable(block, match) -> block markup, or None to emit nothing.
BlockRender = Callable[[str, Any], "str | None"]
BlockHandler = "tuple[Any, BlockRender]"


def exact(literal: str) -> Callable[[str], bool]:
    """Matcher for a block that equals `literal` (e.g. `---`, `[[GALLERY-AI]]`)."""
    return lambda block: block == literal


def prefix(literal: str) -> Callable[[str], bool]:
    """Matcher for a block starting with `literal` (e.g. `## `, `>>> `)."""
    return lambda block: block.startswith(literal)


def render_marker_blocks(
    body: str,
    handlers: Sequence[Any] = (),
    *,
    paragraph: Callable[[str], str] = render_paragraph_from_markdown,
    skip_first_h1: bool = True,
) -> list[str]:
    """Split `body` into blocks and dispatch each through `handlers`.

    The first `# ` block is dropped when `skip_first_h1` (the post title lives in
    the WP title field, not the body). Handlers are tried in order and the first
    match wins; anything unclaimed falls through to `paragraph`. A handler may
    return None to emit nothing for that block.
    """
    out: list[str] = []
    seen_title = False
    for block in split_body_blocks(body):
        if skip_first_h1 and block.startswith("# ") and not seen_title:
            seen_title = True
            continue
        rendered: str | None = None
        claimed = False
        for matcher, render in handlers:
            if hasattr(matcher, "match"):
                match = matcher.match(block)
                if match is None:
                    continue
            else:
                if not matcher(block):
                    continue
                match = None
            claimed = True
            rendered = render(block, match)
            break
        if not claimed:
            rendered = paragraph(block)
        if rendered is not None:
            out.append(rendered)
    return out


def standard_text_handlers(*, h3: bool = True, pullquote_marker: bool = False) -> list[Any]:
    """The `---` / `## ` / `### ` / `>>> ` handlers every one-off script shares.

    `### ` never collides with the `## ` prefix ("###"[0:3] != "## "), so callers
    may reorder or extend this list freely.
    """
    from wp_blocks import pullquote as _pullquote

    handlers: list[Any] = [
        (exact("---"), lambda block, match: separator()),
        (prefix("## "), lambda block, match: heading(inline(block[3:].strip()), level=2)),
    ]
    if h3:
        handlers.append(
            (prefix("### "), lambda block, match: heading(inline(block[4:].strip()), level=3))
        )
    if pullquote_marker:
        handlers.append((prefix(">>> "), lambda block, match: _pullquote(inline(block[4:].strip()))))
    return handlers


def render_text_post(body: str) -> str:
    """Text-only post assembler: skip first H1, map ---/##/###/else via wp_blocks."""
    return "\n\n".join(render_marker_blocks(body, standard_text_handlers()))


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


DEFAULT_MEDIA_EXTENSIONS: tuple[str, ...] = (".jpg", ".jpeg", ".png", ".webp")


def _split_basename(name: str) -> tuple[str, str]:
    """('.../hero-scaled.PNG') -> ('hero-scaled', '.png'). No extension -> ('x', '')."""
    base = name.rsplit("/", 1)[-1]
    head, dot, ext = base.rpartition(".")
    if not dot:
        return base, ""
    return head, f".{ext.lower()}"


def select_media_match(
    results: Any,
    stem: str,
    *,
    extensions: tuple[str, ...] = DEFAULT_MEDIA_EXTENSIONS,
) -> tuple[int, str] | None:
    """Pick the one attachment in `results` whose filename is exactly `stem` + an
    allowed extension. Returns (id, source_url), or None when nothing matches.

    Matching rule (issue #483 — no prefix matching, ever):

      * the `source_url` basename must split to (stem, ext) with ext in
        `extensions` (case-insensitive on the extension only), OR
      * `media_details.original_image` — WordPress's own record of the filename it
        was handed before it produced a `-scaled` variant — must split the same way.

    So `hero.png` matches an attachment served as `hero.png`, and matches a scaled
    attachment whose `original_image` WordPress reports as `hero.png`. It does NOT
    match `hero-2.png`, `hero-scaled.png`, `hero-thumbnail.png`, or
    `hero-1024x768.png` — those are different files, and silently reusing one is
    how the wrong image gets attached to a post.

    Two or more DISTINCT attachment ids matching the same stem is an ambiguity the
    caller cannot resolve safely, so it raises SystemExit rather than picking one.
    That is the 2026-05-15 incident rule applied to media: never bind an operation
    to a target you only half-identified.

    Pure function over the REST payload so both WordPress clients in this repo can
    share one matching rule without sharing a client.
    """
    allowed = tuple(ext.lower() for ext in extensions)
    matches: dict[int, str] = {}
    for media in results or []:
        if not isinstance(media, dict):
            continue
        url = media.get("source_url") or ""
        media_id = media.get("id")
        if not url or media_id is None:
            continue
        original = (media.get("media_details") or {}).get("original_image") or ""
        for name in (url, original):
            if not name:
                continue
            head, ext = _split_basename(name)
            if head == stem and ext in allowed:
                matches[int(media_id)] = str(url)
                break
    if not matches:
        return None
    if len(matches) > 1:
        listed = ", ".join(f"{mid} ({matches[mid]})" for mid in sorted(matches))
        raise SystemExit(
            f"[ABORT] ambiguous media match for {stem!r}: {len(matches)} attachments share "
            f"that filename -> {listed}. Refusing to guess which one the post meant; "
            f"delete or rename the duplicates in the media library, or pass an explicit id."
        )
    media_id, url = next(iter(matches.items()))
    return media_id, url


def find_media_by_stem(
    wp: Any,
    stem: str,
    *,
    extensions: tuple[str, ...] = DEFAULT_MEDIA_EXTENSIONS,
) -> tuple[int, str] | None:
    """Idempotent WP media lookup by exact filename stem + extension allow-list.

    Network failures return None (caller uploads instead — a duplicate upload is
    recoverable, a wrong attachment is not). An ambiguous match raises SystemExit;
    see select_media_match for the rule.
    """
    try:
        result = wp.s.get(
            f"{wp.base}/wp-json/wp/v2/media",
            params={"search": stem, "per_page": 100, "context": "edit"},
            timeout=30,
        ).json()
    except Exception:
        return None
    if not isinstance(result, list):
        return None
    return select_media_match(result, stem, extensions=extensions)


def find_or_upload_media(
    wp: Any,
    path: pathlib.Path,
    alt: str,
    *,
    mime: str,
    write: bool,
    label: str | None = None,
    log: list[str] | None = None,
    extensions: tuple[str, ...] = DEFAULT_MEDIA_EXTENSIONS,
) -> tuple[int, str]:
    """Idempotent single-file media resolve: reuse by stem, else upload.

    Returns (media_id, source_url). In dry-run (`write=False`) returns
    (0, "DRYRUN/<filename>") without touching WordPress. `label` prefixes the log
    line (scripts log either a bare filename or `subdir/filename`).
    """
    name = label or path.name
    if not write:
        return 0, f"DRYRUN/{path.name}"
    found = find_media_by_stem(wp, path.stem, extensions=extensions)
    if found:
        media_id, url = found
        if log is not None:
            log.append(f"{name} -> REUSE id={media_id}")
        return media_id, url
    media = wp.upload_media(path, alt=alt, mime=mime)
    media_id, url = int(media["id"]), media["source_url"]
    if log is not None:
        log.append(f"{name} -> NEW id={media_id} {url}")
    return media_id, url


def find_existing_post_by_slug(wp: Any, slug: str) -> dict[str, Any] | None:
    """Return the first post record matching `slug` in any status, else None.

    The create/update guard every one-off script runs before it writes. Keeping it
    in one place keeps the 2026-05-15 slug-idempotency rule in one place too:
    callers must confirm the returned record is the intended target before PATCH.
    """
    hits = wp.s.get(
        f"{wp.base}/wp-json/wp/v2/posts",
        params={"slug": slug, "status": "any", "context": "edit"},
        timeout=30,
    ).json()
    return hits[0] if isinstance(hits, list) and hits else None


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
        media_id, url = find_or_upload_media(
            wp,
            path,
            alt,
            mime="image/jpeg",
            write=write,
            label=f"{subdir}/{path.name}",
            log=log,
        )
        items.append((media_id, url, alt, caption, path.name))
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
) -> list[int]:
    """Validate numeric IDs when provided; else resolve names via ensure_term_id.

    Name resolution is always create-or-reuse (proximity's behaviour). There used to
    be a `create_missing` flag whose two branches called ensure_term_id identically,
    which read as an opt-in write guard that did not exist (issue #483). Dropped
    rather than implemented: no caller passes names today, and a real read-only mode
    needs a distinct resolver, not a flag on this one.
    """
    if ids:
        return validate_term_ids(wp, "categories", ids)
    return [ensure_term_id(wp, "categories", name) for name in names or []]


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


SEO_META_KEYS = ("jetpack_seo_html_title", "advanced_seo_description")


def verify_seo_meta_landed(
    response_meta: dict[str, Any] | None,
    expected_meta: dict[str, str] | None,
) -> list[str]:
    """Return SEO meta keys that were sent but did not land in the REST response.

    WordPress silently drops unregistered meta keys on write — the POST returns
    200 and the value is never stored. Since Jetpack was deactivated on
    kriskrug.co, ``jetpack_seo_html_title`` and ``advanced_seo_description`` are
    no longer registered, so every connector publish silently loses them.

    Pass the ``meta`` dict from the post-write readback (or the create/update
    response) and the ``meta`` sub-dict from the payload. Any key that was sent
    with a non-empty value but is absent or mismatched in the response is
    listed. An empty list means everything landed (or nothing was sent).
    """
    if not expected_meta:
        return []
    response_meta = response_meta or {}
    dropped: list[str] = []
    for key in SEO_META_KEYS:
        sent = expected_meta.get(key)
        if not sent:
            continue
        if response_meta.get(key) != sent:
            dropped.append(key)
    return dropped


def parse_int_arg(argv: list[str], flag: str, default: int | None = None) -> int | None:
    """Parse `--flag N` from argv; return default when absent."""
    if flag in argv:
        idx = argv.index(flag)
        if idx + 1 >= len(argv):
            raise SystemExit(f"[ABORT] {flag} requires an integer value")
        return int(argv[idx + 1])
    return default


# ---------------------------------------------------------------------------
# declared WordPress IDs (publisher-ids.json)
# ---------------------------------------------------------------------------
@functools.lru_cache(maxsize=None)
def load_publisher_ids(path: pathlib.Path | None = None) -> dict[str, Any]:
    """Load and cache publisher-ids.json (same loader shape as page-map.json)."""
    return json.loads((path or PUBLISHER_IDS_PATH).read_text(encoding="utf-8"))


def _declared(section: str, key: str, ids: dict[str, Any] | None = None) -> dict[str, Any]:
    data = ids if ids is not None else load_publisher_ids()
    entries = data.get(section) or {}
    if key not in entries:
        raise SystemExit(
            f"[ABORT] unknown {section} key {key!r} in publisher-ids.json. "
            f"Known keys: {sorted(entries)}"
        )
    return entries[key]


def category_id(key: str, *, ids: dict[str, Any] | None = None) -> int:
    """Declared category ID by logical key (e.g. 'ai-ethics-philosophy').

    Structural validation only. Live existence is proven separately by
    resolve_category_ids/validate_term_ids at write time.
    """
    entry = _declared("categories", key, ids)
    value = entry.get("id")
    if not isinstance(value, int) or value <= 0:
        raise SystemExit(f"[ABORT] category {key!r} has a non-positive id: {value!r}")
    return value


def media_id(key: str, *, ids: dict[str, Any] | None = None) -> int:
    """Declared media ID by logical key (e.g. 'you-cant-drink-data-featured')."""
    entry = _declared("media", key, ids)
    value = entry.get("id")
    if not isinstance(value, int) or value <= 0:
        raise SystemExit(f"[ABORT] media {key!r} has a non-positive id: {value!r}")
    return value


def media_group(key: str, *, ids: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """Declared, ordered media set by logical key. Returns [{id, url, alt}, ...]."""
    entry = _declared("media_groups", key, ids)
    items = entry.get("items") or []
    for item in items:
        if not isinstance(item.get("id"), int) or item["id"] <= 0:
            raise SystemExit(f"[ABORT] media group {key!r} has an entry with a bad id: {item!r}")
        if not item.get("url") or not item.get("alt"):
            raise SystemExit(f"[ABORT] media group {key!r} entry {item.get('id')} needs url + alt")
    return list(items)


def media_group_index(
    key: str, *, ids: dict[str, Any] | None = None
) -> tuple[dict[int, tuple[str, str]], list[int]]:
    """media_group() as ({id: (url, alt)}, [id, ...]) in declared order."""
    items = media_group(key, ids=ids)
    return {it["id"]: (it["url"], it["alt"]) for it in items}, [it["id"] for it in items]


def media_group_keys(key: str, *, ids: dict[str, Any] | None = None) -> dict[str, int]:
    """media_group() as {declared key: media id}, so scripts can name a sign
    instead of typing its production ID (e.g. SIGN["water-the-servers-last"])."""
    keyed: dict[str, int] = {}
    for item in media_group(key, ids=ids):
        name = item.get("key")
        if not name:
            raise SystemExit(f"[ABORT] media group {key!r} entry {item['id']} has no 'key'")
        if name in keyed:
            raise SystemExit(f"[ABORT] media group {key!r} declares duplicate key {name!r}")
        keyed[name] = item["id"]
    return keyed
