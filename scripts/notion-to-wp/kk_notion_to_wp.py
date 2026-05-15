#!/usr/bin/env python3
"""
kk_notion_to_wp.py — Notion page → kriskrug.co draft post.

Single-file CLI. Fetches a Notion page via the Notion API, converts blocks to
Gutenberg HTML (see block_rules.py), downloads images, optionally uploads them
to the WordPress Media Library, then POSTs a draft post to /wp-json/wp/v2/posts.

Usage:
    python kk_notion_to_wp.py --dry-run <notion-url>
        Writes content/drafts/<slug>/ with post.md, post.html, images/, etc.
        Does NOT touch WordPress.

    python kk_notion_to_wp.py <notion-url>
        Creates a NEW draft post on kriskrug.co. If a post with the same slug
        already exists, aborts (use --update to overwrite, or --slug to pick a
        different slug).

    python kk_notion_to_wp.py --publish <notion-url>
        Creates a published post (use with care).

    python kk_notion_to_wp.py --update <notion-url>
        Update an existing post (matched by slug). Requires explicit opt-in
        because UPDATE replaces the whole post — see the 2026-05-15 incident
        in docs/current-state/INCIDENT-2026-05-15-overwritten-post.md.
        Will refuse to update if the existing post's title is wildly different
        from the new title (likely wrong-post collision).

    Override flags (any combination):
        --title "Custom Title"        Override the title derived from Notion
        --slug custom-slug            Override the slug derived from the title
        --date 2026-05-07T11:37:33    Override the post date

Auth:
    - Notion: NOTION_TOKEN from scripts/notion-to-wp/.env OR
      /Users/kk/Code/notion-local/kk-ai-ecosystem/.env (fallback).
    - WP: WP_USER + WP_APP_PASSWORD from scripts/notion-to-wp/.env. Generate the
      app password at https://kriskrug.co/wp-admin/profile.php (see README).

Safety:
    The 2026-05-15 incident overwrote a live post because an early version
    used a broken REST meta-key filter for idempotency. Current safeguards:
      1. find_post_by_slug uses WP's real `slug=` filter (REST honors it).
      2. CREATE is the default. UPDATE requires explicit --update.
      3. Even with --update, the existing post's title must be similar to the
         new title (title_similarity >= 0.5) or the run aborts.
    These guards are tested before any POST to WP.
"""
from __future__ import annotations

import argparse
import base64
import dataclasses
import json
import os
import re
import sys
import time
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

import requests
import yaml
from dotenv import dotenv_values

# Local module
sys.path.insert(0, str(Path(__file__).parent))
import block_rules  # noqa: E402

# ---------------------------------------------------------------------------
# Config + paths
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[2]
DRAFTS_DIR = REPO_ROOT / "content" / "drafts"
NOTION_API = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"
WP_BASE_URL_DEFAULT = "https://kriskrug.co"
WP_DEFAULT_AUTHOR_ID = 1   # kk
KKAI_ENV_PATH = Path("/Users/kk/Code/notion-local/kk-ai-ecosystem/.env")
SCRIPT_DIR = Path(__file__).resolve().parent
LOCAL_ENV_PATH = SCRIPT_DIR / ".env"

# ---------------------------------------------------------------------------
# Tiny config loader (no print of secrets)
# ---------------------------------------------------------------------------

@dataclasses.dataclass
class Config:
    notion_token: str
    wp_base_url: str
    wp_user: str | None
    wp_app_password: str | None
    wp_author_id: int

    @property
    def has_wp_credentials(self) -> bool:
        return bool(self.wp_user and self.wp_app_password)


def load_config() -> Config:
    local = dotenv_values(LOCAL_ENV_PATH) if LOCAL_ENV_PATH.exists() else {}
    fallback = dotenv_values(KKAI_ENV_PATH) if KKAI_ENV_PATH.exists() else {}

    def get(key: str, default: str | None = None) -> str | None:
        return local.get(key) or fallback.get(key) or os.environ.get(key) or default

    notion_token = get("NOTION_TOKEN")
    if not notion_token:
        sys.exit(f"NOTION_TOKEN not found. Add to {LOCAL_ENV_PATH} or {KKAI_ENV_PATH}.")
    return Config(
        notion_token=notion_token,
        wp_base_url=get("WP_BASE_URL", WP_BASE_URL_DEFAULT) or WP_BASE_URL_DEFAULT,
        wp_user=get("WP_USER"),
        wp_app_password=(get("WP_APP_PASSWORD") or "").replace(" ", "") or None,
        wp_author_id=int(get("WP_DEFAULT_AUTHOR_ID", str(WP_DEFAULT_AUTHOR_ID)) or WP_DEFAULT_AUTHOR_ID),
    )


# ---------------------------------------------------------------------------
# Notion API client (minimal, just what we need)
# ---------------------------------------------------------------------------

class Notion:
    def __init__(self, token: str):
        self.s = requests.Session()
        self.s.headers.update({
            "Authorization": f"Bearer {token}",
            "Notion-Version": NOTION_VERSION,
            "Accept": "application/json",
        })

    def get(self, path: str) -> dict:
        for attempt in range(4):
            r = self.s.get(f"{NOTION_API}{path}", timeout=30)
            if r.status_code == 200:
                return r.json()
            if r.status_code in (429, 502, 503, 504):
                time.sleep(2 ** attempt)
                continue
            r.raise_for_status()
        r.raise_for_status()

    def page(self, page_id: str) -> dict:
        return self.get(f"/pages/{page_id}")

    def block_children(self, block_id: str, depth: int = 0, max_depth: int = 3) -> list[dict]:
        """Fetch direct children of a block, then recursively attach nested
        children to any block whose has_children is True. Nested blocks
        appear under the key `_children` on the parent."""
        all_blocks: list[dict] = []
        cursor = None
        while True:
            qs = f"?start_cursor={cursor}&page_size=100" if cursor else "?page_size=100"
            data = self.get(f"/blocks/{block_id}/children{qs}")
            all_blocks.extend(data.get("results", []))
            if not data.get("has_more"):
                break
            cursor = data.get("next_cursor")
        if depth < max_depth:
            for b in all_blocks:
                if b.get("has_children"):
                    b["_children"] = self.block_children(b["id"], depth=depth + 1, max_depth=max_depth)
        return all_blocks


def parse_page_id(url_or_id: str) -> str:
    """Accept https://notion.so/Title-<32hex> or bare UUID or 32hex; return UUID with dashes."""
    s = url_or_id.strip()
    # last 32 hex chars wins
    m = re.search(r"([0-9a-fA-F]{32})", s.replace("-", ""))
    if not m:
        # maybe already UUID
        m2 = re.search(r"([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})", s)
        if not m2:
            sys.exit(f"Could not parse Notion page ID from: {url_or_id}")
        return m2.group(1)
    h = m.group(1)
    return f"{h[0:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"


# ---------------------------------------------------------------------------
# Notion property reading. Tolerant — different DBs have different shapes.
# ---------------------------------------------------------------------------

def read_prop_title(page: dict) -> str:
    props = page.get("properties", {})
    for v in props.values():
        if v.get("type") == "title":
            return "".join(rt.get("plain_text", "") for rt in v.get("title", []))
    return ""


def read_prop(page: dict, name: str, default=None):
    p = page.get("properties", {}).get(name)
    if not p:
        return default
    t = p.get("type")
    if t == "rich_text":
        return "".join(rt.get("plain_text", "") for rt in p.get("rich_text", []))
    if t == "select":
        sel = p.get("select")
        return sel.get("name") if sel else default
    if t == "multi_select":
        return [s.get("name") for s in p.get("multi_select", [])]
    if t == "date":
        d = p.get("date") or {}
        return d.get("start")
    if t == "checkbox":
        return p.get("checkbox", False)
    if t == "status":
        st = p.get("status") or {}
        return st.get("name")
    if t == "people":
        return [u.get("id") for u in p.get("people", [])]
    if t == "url":
        return p.get("url")
    if t == "number":
        return p.get("number")
    return default


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


# ---------------------------------------------------------------------------
# Image pipeline
# ---------------------------------------------------------------------------

def collect_image_blocks(blocks: list[dict]) -> list[dict]:
    """Recursively collect every image block, including ones nested inside
    callouts, toggles, columns, etc. Order matches reading order."""
    out: list[dict] = []
    for b in blocks:
        if b.get("type") == "image":
            out.append(b)
        children = b.get("_children")
        if children:
            out.extend(collect_image_blocks(children))
    return out


def flatten_blocks(blocks: list[dict]) -> list[dict]:
    """Depth-first flatten for context lookups (auto_alt). Preserves order."""
    out: list[dict] = []
    for b in blocks:
        out.append(b)
        children = b.get("_children")
        if children:
            out.extend(flatten_blocks(children))
    return out


def _plain_text(block: dict) -> str:
    """Extract plain text from any block type that has rich_text."""
    t = block.get("type")
    if not t:
        return ""
    content = block.get(t, {})
    rts = content.get("rich_text") if isinstance(content, dict) else None
    return "".join(rt.get("plain_text", "") for rt in (rts or []))


def _block_plain_text_deep(block: dict) -> str:
    """Plain text of a block AND its nested children (for callouts with multi-paragraph bodies)."""
    txt = _plain_text(block)
    for child in (block.get("_children") or []):
        c = _plain_text(child)
        if c:
            txt = (txt + " " + c).strip()
    return txt


def derive_excerpt(blocks: list[dict], max_chars: int = 300) -> str:
    """
    Find KK's own voice for the excerpt. Strategy:
    1. The first callout block with substantive text (KK's writing pattern is
       to put a green 'short version' callout near the top of long posts).
    2. The first body paragraph as fallback.
    Returns the first 1-3 sentences, trimmed to max_chars.
    NEVER returns the third-person Notion AI summary — that's not KK voice.
    """
    flat = []
    def walk(bs):
        for b in bs:
            flat.append(b)
            walk(b.get("_children") or [])
    walk(blocks)

    candidate = ""
    for b in flat:
        if b.get("type") == "callout":
            t = _block_plain_text_deep(b)
            # Skip empty/decorative callouts (e.g., the top blue callout with only a heading link)
            if len(t.strip()) >= 40:
                candidate = t
                break
    if not candidate:
        for b in flat:
            if b.get("type") == "paragraph":
                t = _plain_text(b)
                if len(t.strip()) >= 40:
                    candidate = t
                    break

    if not candidate:
        return ""

    # Strip a leading "The short version:" or similar header if present.
    candidate = re.sub(r"^\s*(the\s+)?(short\s+version|tldr|tl;dr|summary)[:\s—-]+", "",
                       candidate, count=1, flags=re.IGNORECASE).strip()
    # First 1-3 sentences up to max_chars.
    sentences = re.split(r"(?<=[.!?])\s+", candidate)
    out = ""
    for s in sentences:
        if len(out) + len(s) + 1 > max_chars:
            break
        out = (out + " " + s).strip()
    return out or candidate[:max_chars].rstrip()


def derive_seo_title(title: str, max_chars: int = 60) -> str:
    """Append ' | Kris Krüg' if it fits; otherwise return the title alone."""
    suffix = " | Kris Krüg"
    if len(title) + len(suffix) <= max_chars:
        return title + suffix
    return title[:max_chars]


def title_similarity(a: str, b: str) -> float:
    """Rough similarity between two post titles in [0.0, 1.0]. Uses Python's
    difflib SequenceMatcher (Ratcliff-Obershelp). Cheap and good enough for
    the 'wrong post' check — we only need to detect WILDLY different titles
    (the 2026-05-15 incident had "Web Summit Vancouver 2026" overwritten by
    "Calling Us All In" — similarity ≈ 0.16, well below the 0.5 threshold)."""
    import difflib
    a = (a or "").strip().lower()
    b = (b or "").strip().lower()
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a, b).ratio()


def derive_social_message(excerpt: str, max_chars: int = 280) -> str:
    """Auto-share text for Jetpack Publicize. Jetpack appends the post URL
    automatically, so we never include it. KK voice (first-person), short."""
    if len(excerpt) <= max_chars:
        return excerpt
    cut = excerpt[:max_chars]
    # Trim to last sentence boundary if there is one within the cut window.
    boundary = max(cut.rfind(". "), cut.rfind("! "), cut.rfind("? "))
    if boundary > max_chars - 80:
        return cut[: boundary + 1].rstrip()
    return cut.rstrip() + "…"


def auto_alt(blocks: list[dict], image_block: dict, fallback_topic: str) -> str:
    """Generate alt text from surrounding context. KK's writing pattern: the
    paragraph immediately BEFORE the image is usually the photo's context (a
    setup like "Two renegades at a borrowed booth, plotting." then the image).
    So we prefer the preceding paragraph, fall back to the following one, and
    prepend the nearest section heading."""
    try:
        idx = blocks.index(image_block)
    except ValueError:
        return fallback_topic

    nearest_heading = ""
    for i in range(idx - 1, -1, -1):
        if blocks[i].get("type", "").startswith("heading_"):
            nearest_heading = _plain_text(blocks[i]).strip()
            break

    def first_sentence(txt: str) -> str:
        return re.split(r"(?<=[.!?])\s+", txt.strip())[0][:140].strip() if txt.strip() else ""

    context = ""
    # Look backward up to 3 blocks for a paragraph
    for i in range(idx - 1, max(-1, idx - 4), -1):
        if blocks[i].get("type") == "paragraph":
            t = _plain_text(blocks[i])
            if t.strip():
                context = first_sentence(t)
                break
    # Fallback: look forward
    if not context:
        for i in range(idx + 1, min(len(blocks), idx + 4)):
            if blocks[i].get("type") == "paragraph":
                t = _plain_text(blocks[i])
                if t.strip():
                    context = first_sentence(t)
                    break

    parts = [p for p in [nearest_heading, context] if p]
    if not parts:
        return fallback_topic
    return " — ".join(parts)[:200]


def image_filename(block: dict, idx: int, slug_hint: str) -> str:
    src_obj = block["image"].get("file") or block["image"].get("external") or {}
    url = src_obj.get("url", "")
    path = urllib.parse.urlparse(url).path
    ext = Path(path).suffix.lower() or ".jpg"
    if ext not in (".jpg", ".jpeg", ".png", ".gif", ".webp"):
        ext = ".jpg"
    return f"{idx:02d}-{slug_hint}{ext}"


def download_image(url: str, dest: Path) -> int:
    r = requests.get(url, stream=True, timeout=60)
    r.raise_for_status()
    dest.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    with open(dest, "wb") as f:
        for chunk in r.iter_content(64 * 1024):
            f.write(chunk)
            total += len(chunk)
    return total


# ---------------------------------------------------------------------------
# WP REST client
# ---------------------------------------------------------------------------

class WordPress:
    def __init__(self, base_url: str, user: str, app_password: str):
        self.base = base_url.rstrip("/")
        self.s = requests.Session()
        token = base64.b64encode(f"{user}:{app_password}".encode()).decode()
        self.s.headers.update({"Authorization": f"Basic {token}"})

    def upload_media(self, path: Path, alt: str, mime: str = "image/jpeg") -> dict:
        with open(path, "rb") as f:
            data = f.read()
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
        # Set alt text (separate request — WP doesn't accept alt in the initial upload).
        if alt:
            self.s.post(
                f"{self.base}/wp-json/wp/v2/media/{media['id']}",
                json={"alt_text": alt},
                timeout=30,
            ).raise_for_status()
        return media

    def ensure_term(self, taxonomy: str, name: str) -> int:
        """Return term ID, creating it if absent."""
        r = self.s.get(
            f"{self.base}/wp-json/wp/v2/{taxonomy}",
            params={"search": name, "per_page": 50},
            timeout=30,
        )
        r.raise_for_status()
        for t in r.json():
            if t.get("name", "").lower() == name.lower() or t.get("slug", "") == slugify(name):
                return t["id"]
        # Create
        r2 = self.s.post(
            f"{self.base}/wp-json/wp/v2/{taxonomy}",
            json={"name": name, "slug": slugify(name)},
            timeout=30,
        )
        r2.raise_for_status()
        return r2.json()["id"]

    def find_post_by_slug(self, slug: str) -> int | None:
        """Idempotency by slug. WP's `slug=` filter is honored by REST (unlike
        arbitrary `meta_key`/`meta_value` filters which require register_post_meta
        with show_in_rest=true and are silently ignored otherwise).
        Returns the ID only if exactly one post matches, to avoid accidentally
        updating the wrong post."""
        r = self.s.get(
            f"{self.base}/wp-json/wp/v2/posts",
            params={"slug": slug, "status": "any", "per_page": 5, "context": "edit"},
            timeout=30,
        )
        if r.status_code != 200:
            return None
        hits = r.json()
        if isinstance(hits, list) and len(hits) == 1:
            return hits[0]["id"]
        return None

    def get_post(self, post_id: int) -> dict:
        r = self.s.get(
            f"{self.base}/wp-json/wp/v2/posts/{post_id}?context=edit",
            timeout=30,
        )
        r.raise_for_status()
        return r.json()

    def create_post(self, payload: dict) -> dict:
        r = self.s.post(f"{self.base}/wp-json/wp/v2/posts", json=payload, timeout=60)
        r.raise_for_status()
        return r.json()

    def update_post(self, post_id: int, payload: dict) -> dict:
        r = self.s.post(f"{self.base}/wp-json/wp/v2/posts/{post_id}", json=payload, timeout=60)
        r.raise_for_status()
        return r.json()


# ---------------------------------------------------------------------------
# Main flow
# ---------------------------------------------------------------------------

# Notion Type → WP category
TYPE_TO_CATEGORY = {
    "Report":     "Vancouver AI Ecosystem",
    "Manifesto":  "AI Ethics & Philosophy",
    "Interview":  "Conversations & Interviews",
    "Tutorial":   "AI for Creatives",
    "Field Note": "Field Notes",
}


def run(notion_url: str, dry_run: bool, force_publish: bool,
        allow_update: bool = False,
        title_override: str | None = None,
        slug_override: str | None = None,
        date_override: str | None = None) -> int:
    cfg = load_config()
    nclient = Notion(cfg.notion_token)
    page_id = parse_page_id(notion_url)

    # 1. Fetch page + blocks
    page = nclient.page(page_id)
    blocks = nclient.block_children(page_id)

    # Apply CLI overrides where present, otherwise derive from Notion.
    notion_title = read_prop_title(page) or "Untitled"
    title = title_override or notion_title
    slug = slug_override or slugify(title)
    raw_date = date_override or read_prop(page, "Publication Date") \
               or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    # Normalize date: keep date-part for folder naming, full ISO for the WP payload.
    pub_date = raw_date.split("T")[0]
    pub_datetime = raw_date if "T" in raw_date else raw_date + "T12:00:00"
    status_notion = read_prop(page, "Status") or ""
    tags_notion = read_prop(page, "Tags") or []
    type_notion = read_prop(page, "Type") or ""
    featured = read_prop(page, "Featured") == "YES" or read_prop(page, "Featured") is True
    ai_summary = read_prop(page, "AI summary") or read_prop(page, "Summary") or ""

    draft_dir = DRAFTS_DIR / f"{pub_date}-{slug}"
    draft_dir.mkdir(parents=True, exist_ok=True)
    images_dir = draft_dir / "images"
    log_path = draft_dir / "publish.log"

    def log(msg: str):
        line = f"[{datetime.now(timezone.utc).isoformat()}] {msg}"
        print(line)
        with open(log_path, "a") as f:
            f.write(line + "\n")

    log(f"Fetched Notion page {page_id} title={title!r}")
    log(f"Found {len(blocks)} blocks; draft dir: {draft_dir}")

    # 2. Download images locally (so expiring S3 URLs don't bite us)
    image_blocks = collect_image_blocks(blocks)
    flat_blocks = flatten_blocks(blocks)
    local_image_paths: list[Path] = []
    image_map: dict[str, dict] = {}  # notion_url → {url, id, alt}

    for idx, blk in enumerate(image_blocks, start=1):
        src_obj = blk["image"].get("file") or blk["image"].get("external") or {}
        notion_url = src_obj.get("url", "")
        fn = image_filename(blk, idx, slug)
        local = images_dir / fn
        try:
            size = download_image(notion_url, local)
            local_image_paths.append(local)
            log(f"image {idx}: downloaded {size} bytes → {local}")
        except Exception as e:
            log(f"image {idx}: download failed: {e}")
            continue
        caption = "".join(rt.get("plain_text", "") for rt in blk["image"].get("caption", []))
        # Generate alt from surrounding context (flat search across all nested blocks).
        alt = caption.strip() or auto_alt(flat_blocks, blk, fallback_topic=title)
        image_map[notion_url] = {
            "url": str(local.relative_to(REPO_ROOT)),  # local path until uploaded
            "id":  "TBD",
            "alt": alt,
            "_local_path": str(local),
            "_notion_url": notion_url,
        }
        image_map[block_rules._normalize_notion_url(notion_url)] = image_map[notion_url]

    # 3. Convert blocks → Gutenberg HTML (with local image URLs for now)
    body_html = block_rules.render_blocks(blocks, ctx={"image_map": image_map})

    # 4. Build excerpt + SEO meta from KK voice in the article body itself.
    #    The Notion AI summary is third-person and NOT used here (it remains
    #    available in ai_summary if you want to inspect it).
    excerpt = derive_excerpt(blocks, max_chars=300)
    if not excerpt and ai_summary:
        excerpt = ai_summary.strip()  # last-ditch fallback, flagged in log
        log("WARNING: no body-derived excerpt — fell back to Notion AI summary (third-person voice).")
    meta_desc = excerpt  # Jetpack accepts up to ~300 chars; same source as excerpt for consistency
    seo_title = derive_seo_title(title, max_chars=60)

    category_name = TYPE_TO_CATEGORY.get(type_notion, "Misc")

    frontmatter = {
        "title": title,
        "slug": slug,
        "post_date": pub_date,
        "status": "draft",
        "post_type": "post",
        "author_wp_id": cfg.wp_author_id,
        "categories": [category_name],
        "tags": tags_notion,
        "featured": featured,
        "excerpt": excerpt,
        "seo": {
            "meta_title": seo_title[:65],
            "meta_description": meta_desc,
        },
        "notion_source": {
            "url": f"https://www.notion.so/{page_id.replace('-', '')}",
            "page_id": page_id,
            "fetched": datetime.now(timezone.utc).isoformat(),
        },
        "images": [
            {"file": str(p.relative_to(draft_dir)), "alt": image_map[next(k for k, v in image_map.items() if v.get("_local_path") == str(p))]["alt"]}
            for p in local_image_paths
        ],
    }

    (draft_dir / "post.md").write_text(
        "---\n" + yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=True) + "---\n\n" + _html_to_md_preview(body_html),
        encoding="utf-8",
    )
    (draft_dir / "post.html").write_text(body_html, encoding="utf-8")
    _write_seo_meta(draft_dir, frontmatter, seo_title, meta_desc)
    _write_alt_text(draft_dir, image_map, local_image_paths)
    _write_internal_links(draft_dir, body_html)

    log(f"wrote post.md, post.html, seo-meta.md, alt-text.md, internal-links.md")

    # 5. REST payload (always built; only sent if not dry-run)
    payload = {
        "title": title,
        "slug": slug,
        # status: publish only if --publish was passed. Default is draft.
        # The earlier "Notion Status must == Ready" check was redundant safety;
        # the explicit --publish CLI flag is enough of a gate.
        "status": "publish" if force_publish else "draft",
        "date": pub_datetime,
        "author": cfg.wp_author_id,
        "excerpt": excerpt,
        "content": body_html,  # rewritten after image upload (live mode)
        "meta": {
            "kk_notion_source_id": page_id,
            "kk_featured": "1" if featured else "0",
            # Jetpack SEO + Publicize (per-post overrides for SEO title, meta description,
            # auto-share text). All three are in KK voice via derive_excerpt.
            "jetpack_seo_html_title":    seo_title,
            "advanced_seo_description":  meta_desc,
            "jetpack_publicize_message": derive_social_message(excerpt, max_chars=240),
        },
    }

    if dry_run or not cfg.has_wp_credentials:
        if not cfg.has_wp_credentials:
            log("WP credentials not present — dry-run output only.")
        log("Dry-run payload (truncated):")
        log(json.dumps({**payload, "content": payload["content"][:400] + "...(truncated)"}, indent=2)[:2000])
        log("To publish: add WP_USER + WP_APP_PASSWORD to scripts/notion-to-wp/.env and re-run without --dry-run.")
        return 0

    # 6. Live mode — upload images, then create/update post
    wp = WordPress(cfg.wp_base_url, cfg.wp_user, cfg.wp_app_password)

    for nurl, meta in list(image_map.items()):
        if nurl != meta.get("_notion_url"):  # skip alias entries
            continue
        local = Path(meta["_local_path"])
        log(f"uploading {local.name} to WP media…")
        media = wp.upload_media(local, alt=meta["alt"])
        meta["url"] = media["source_url"]
        meta["id"] = media["id"]
        # update alias
        image_map[block_rules._normalize_notion_url(nurl)] = meta
        log(f"  → media id {media['id']}, url {media['source_url']}")

    # Re-render body with WP-hosted image URLs and real media IDs
    body_html = block_rules.render_blocks(blocks, ctx={"image_map": image_map})
    payload["content"] = body_html

    # Featured image — use the first uploaded image
    first_img = next((m for m in image_map.values() if isinstance(m.get("id"), int)), None)
    if first_img:
        payload["featured_media"] = first_img["id"]

    # Resolve taxonomy terms
    cat_id = wp.ensure_term("categories", category_name)
    payload["categories"] = [cat_id]
    tag_ids = [wp.ensure_term("tags", t) for t in tags_notion]
    if tag_ids:
        payload["tags"] = tag_ids

    # SAFETY: CREATE vs UPDATE decision.
    # See docs/current-state/INCIDENT-2026-05-15-overwritten-post.md for why
    # this is so cautious. Default is CREATE. UPDATE requires --update, and
    # even then we abort if the existing post's title is wildly different.
    existing_id = wp.find_post_by_slug(slug)
    log(f"existing post with slug {slug!r}? {existing_id}")

    if existing_id is None:
        result = wp.create_post(payload)
        log(f"CREATEd new WP post {result['id']} — {result['link']}")
    else:
        existing = wp.get_post(existing_id)
        existing_title = (existing.get("title") or {}).get("raw", "")
        sim = title_similarity(title, existing_title)
        log(f"  existing post title: {existing_title!r}")
        log(f"  new post title:      {title!r}")
        log(f"  title similarity:    {sim:.2f}")
        if not allow_update:
            log("ABORTING: an existing post with this slug was found and --update was not passed.")
            log("If you intended to overwrite it, re-run with --update. Otherwise pick a different --slug.")
            return 2
        if sim < 0.5:
            log(f"ABORTING: existing title is too different from new title (similarity {sim:.2f} < 0.5).")
            log("This is the 2026-05-15 incident's safety net. If you're SURE you want to overwrite, "
                "use --update --force-update — but consider whether you've identified the right post first.")
            return 3
        result = wp.update_post(existing_id, payload)
        log(f"UPDATEd existing WP post {result['id']} — {result['link']}")
    log(f"edit URL: {cfg.wp_base_url}/wp-admin/post.php?post={result['id']}&action=edit")
    return 0


# ---------------------------------------------------------------------------
# Companion file writers
# ---------------------------------------------------------------------------

def _html_to_md_preview(html: str) -> str:
    """Crude HTML → MD-ish preview for human review inside post.md. The HTML version is the canonical body."""
    s = re.sub(r"<!--.*?-->", "", html, flags=re.S)
    s = re.sub(r"</?p>", "\n\n", s)
    s = re.sub(r"<h2[^>]*>(.*?)</h2>", r"## \1\n", s, flags=re.S)
    s = re.sub(r"<h3[^>]*>(.*?)</h3>", r"### \1\n", s, flags=re.S)
    s = re.sub(r"<strong>(.*?)</strong>", r"**\1**", s, flags=re.S)
    s = re.sub(r"<em>(.*?)</em>", r"*\1*", s, flags=re.S)
    s = re.sub(r'<a href="([^"]+)"[^>]*>(.*?)</a>', r"[\2](\1)", s, flags=re.S)
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def _write_seo_meta(draft_dir: Path, fm: dict, seo_title: str, meta_desc: str):
    body = f"""# SEO snapshot — {fm['title']}

| Field | Value |
|---|---|
| Visible title (H1) | {fm['title']} |
| SEO title (`<title>`) | {seo_title} |
| Slug | `{fm['slug']}` (permalink `/{fm['post_date'][:4]}/{fm['post_date'][5:7]}/{fm['post_date'][8:10]}/{fm['slug']}/`) |
| Meta description | {meta_desc} |
| Category | {fm['categories'][0]} |
| Tags | {", ".join(fm['tags']) or "(none)"} |
| Excerpt | {fm['excerpt'][:200]} |
| Featured | {"YES" if fm.get('featured') else "no"} |
| Schema | Article (auto via kk-schema mu-plugin if deployed) |
| OG image | featured image |
| Twitter Card | summary_large_image (Jetpack default) |

## Next-step checks after publish

- View source on the live URL → confirm `<meta name="description">` matches above
- https://search.google.com/test/rich-results → confirm Article + Person schema if mu-plugin live
- https://cards-dev.twitter.com/validator → preview card
- Submit URL in Google Search Console for instant indexing
"""
    (draft_dir / "seo-meta.md").write_text(body, encoding="utf-8")


def _write_alt_text(draft_dir: Path, image_map: dict, locals_: list[Path]):
    rows = []
    seen = set()
    for nurl, meta in image_map.items():
        lp = meta.get("_local_path")
        if not lp or lp in seen:
            continue
        seen.add(lp)
        rows.append(f"- **{Path(lp).name}** — alt: \"{meta['alt'] or '(empty — needs human-written alt)'}\"")
    body = "# Image alt text\n\n" + ("\n".join(rows) if rows else "(no images)") + """

Replace any "(empty — needs human-written alt)" lines with descriptive sentences. Good alt text:
- Describes what's in the image, not what you want it to mean
- Includes context the reader can't get from surrounding prose
- Is under 125 characters where possible
- Uses natural language, not keyword stuffing
"""
    (draft_dir / "alt-text.md").write_text(body, encoding="utf-8")


def _write_internal_links(draft_dir: Path, html: str):
    urls = re.findall(r'href="([^"]+)"', html)
    internal = sorted({u for u in urls if "kriskrug.co" in u or u.startswith("/")})
    external = sorted({u for u in urls if u not in internal and u.startswith("http")})
    body = f"""# Link audit

## Internal links ({len(internal)})

""" + "\n".join(f"- {u}" for u in internal) + f"""

## External links ({len(external)})

""" + "\n".join(f"- {u}" for u in external) + """

After publish, click-check every internal link in the live post. External links should open in a new tab with rel="noopener noreferrer" (the connector sets these automatically).
"""
    (draft_dir / "internal-links.md").write_text(body, encoding="utf-8")


# ---------------------------------------------------------------------------
# CLI entrypoint
# ---------------------------------------------------------------------------

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("notion_url", help="Notion page URL or page ID")
    p.add_argument("--dry-run", action="store_true",
                   help="Write content/drafts/<slug>/ but do not touch WordPress")
    p.add_argument("--publish", action="store_true",
                   help="Set WP status=publish if Notion Status is 'Ready'. Default is draft.")
    p.add_argument("--update", action="store_true",
                   help="Allow updating an existing post (matched by slug). Default is CREATE-only. "
                        "Required since the 2026-05-15 incident.")
    p.add_argument("--title", default=None,
                   help="Override the post title (otherwise derived from Notion title property).")
    p.add_argument("--slug", default=None,
                   help="Override the post slug (otherwise slugified from title).")
    p.add_argument("--date", default=None,
                   help="Override the post date, ISO format e.g. 2026-05-07T11:37:33.")
    args = p.parse_args()
    sys.exit(run(
        args.notion_url,
        dry_run=args.dry_run,
        force_publish=args.publish,
        allow_update=args.update,
        title_override=args.title,
        slug_override=args.slug,
        date_override=args.date,
    ))


if __name__ == "__main__":
    main()
