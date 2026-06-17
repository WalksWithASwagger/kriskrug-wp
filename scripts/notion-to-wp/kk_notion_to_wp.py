#!/usr/bin/env python3
"""
kk_notion_to_wp.py — Notion page → kriskrug.co draft post.

CLI wrapper. Fetches a Notion page via the Notion API, converts blocks to
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

    python kk_notion_to_wp.py --diff <notion-url>
        Fetch the existing post matched by slug, enforce the same title guard,
        print a unified diff of selected WP fields vs. the proposed payload,
        and exit before any WordPress write request.

    Override flags (any combination):
        --title "Custom Title"        Override the title derived from Notion
        --slug custom-slug            Override the slug derived from the title
        --date 2026-05-07T11:37:33    Override the post date
        --category "AI Ethics & Philosophy"
                                      Override Notion Type → WP category routing

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
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

# Local modules
sys.path.insert(0, str(Path(__file__).parent))
import block_rules  # noqa: E402
import text_polish  # noqa: E402
from category_routing import (  # noqa: E402
    CATEGORY_REVIEW_REQUIRED,
    FEATURE_CATEGORY_TAG_HINTS,
    TYPE_TO_CATEGORY,
    category_requires_review,
    resolve_category,
)
from connector_config import (  # noqa: E402
    DRAFTS_DIR,
    KKAI_ENV_PATH,
    LOCAL_ENV_PATH,
    REPO_ROOT,
    SCRIPT_DIR,
    WP_BASE_URL_DEFAULT,
    WP_DEFAULT_AUTHOR_ID,
    Config,
    load_config,
)
from connector_payload import build_wp_payload  # noqa: E402
from content_derivation import (  # noqa: E402
    _block_plain_text_deep,
    _plain_text,
    derive_excerpt,
    derive_seo_title,
    derive_social_message,
)
from draft_writers import (  # noqa: E402
    html_to_md_preview as _html_to_md_preview,
    write_alt_text as _write_alt_text,
    write_internal_links as _write_internal_links,
    write_seo_meta as _write_seo_meta,
)
from media_pipeline import (  # noqa: E402
    auto_alt,
    collect_image_blocks,
    download_image,
    flatten_blocks,
    image_filename,
)
from notion_client import (  # noqa: E402
    Notion,
    parse_page_id,
    read_prop,
    read_prop_title,
    slugify,
)
from update_safety import (  # noqa: E402
    TITLE_SIMILARITY_UPDATE_THRESHOLD,
    _wp_text_field,
    emit_update_diff_review,
    title_similarity,
    update_diff,
    update_title_guard,
)
from wp_client import WordPress  # noqa: E402


# ---------------------------------------------------------------------------
# Main flow
# ---------------------------------------------------------------------------


def run(notion_url: str, dry_run: bool, force_publish: bool,
        allow_update: bool = False,
        title_override: str | None = None,
        slug_override: str | None = None,
        date_override: str | None = None,
        category_override: str | None = None,
        diff_update: bool = False) -> int:
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

    # 3a. Polish pass — em-dash purge + auto-link first occurrence of proper nouns.
    #     See scripts/notion-to-wp/text_polish.py for the rules. Self-link guard
    #     uses the canonical URL the post will live at.
    canonical_url = f"{cfg.wp_base_url.rstrip('/')}/{pub_date.replace('-', '/')}/{slug}/"
    body_html, polish_report = text_polish.polish_html(body_html, self_url=canonical_url)
    if polish_report["links_added"]:
        log(f"auto-linked {len(polish_report['links_added'])} proper nouns: " +
            ", ".join(x["text"] for x in polish_report["links_added"]))

    # 4. Build excerpt + SEO meta from KK voice in the article body itself.
    #    The Notion AI summary is third-person and NOT used here (it remains
    #    available in ai_summary if you want to inspect it).
    excerpt = text_polish.polish_text(derive_excerpt(blocks, max_chars=300))
    if not excerpt and ai_summary:
        excerpt = ai_summary.strip()  # last-ditch fallback, flagged in log
        log("WARNING: no body-derived excerpt — fell back to Notion AI summary (third-person voice).")
    meta_desc = excerpt  # Jetpack accepts up to ~300 chars; same source as excerpt for consistency
    seo_title = text_polish.polish_text(derive_seo_title(title, max_chars=60))

    category_name, category_route = resolve_category(type_notion, tags_notion, category_override)
    log(
        f"category route: Type={type_notion!r}, tags={tags_notion!r} "
        f"→ {category_name!r} ({category_route})"
    )

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
    payload = build_wp_payload(
        title=title,
        slug=slug,
        force_publish=force_publish,
        pub_datetime=pub_datetime,
        author_id=cfg.wp_author_id,
        excerpt=excerpt,
        body_html=body_html,
        page_id=page_id,
        featured=featured,
        seo_title=seo_title,
        meta_desc=meta_desc,
    )

    if (dry_run and not diff_update) or not cfg.has_wp_credentials:
        if diff_update and not cfg.has_wp_credentials:
            log("ABORTING: --diff requires WP credentials to fetch the existing post by slug.")
            log("No WP write was attempted.")
            return 5
        if not cfg.has_wp_credentials:
            log("WP credentials not present — dry-run output only.")
        log("Dry-run payload (truncated):")
        log(json.dumps({**payload, "content": payload["content"][:400] + "...(truncated)"}, indent=2)[:2000])
        log("To publish: add WP_USER + WP_APP_PASSWORD to scripts/notion-to-wp/.env and re-run without --dry-run.")
        return 0

    if category_requires_review(category_name):
        log("ABORTING: Notion Type=Feature needs an explicit category decision before a live WP write.")
        log(
            'Re-run with --category "AI Ethics & Philosophy", '
            '--category "Vancouver AI Ecosystem", or another intentional category.'
        )
        return 4

    # 6. Live mode — upload images, then create/update post
    wp = WordPress(cfg.wp_base_url, cfg.wp_user, cfg.wp_app_password)

    if diff_update:
        return emit_update_diff_review(wp, slug, title, payload, log)

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
    body_html, _ = text_polish.polish_html(body_html, self_url=canonical_url)
    payload["content"] = body_html
    payload["meta"]["jetpack_publicize_message"] = text_polish.polish_text(
        payload["meta"]["jetpack_publicize_message"]
    )

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
        title_match, sim = update_title_guard(title, existing_title)
        log(f"  existing post title: {existing_title!r}")
        log(f"  new post title:      {title!r}")
        log(f"  title similarity:    {sim:.2f}")
        if not allow_update:
            log("ABORTING: an existing post with this slug was found and --update was not passed.")
            log("If you intended to overwrite it, re-run with --update. Otherwise pick a different --slug.")
            return 2
        if not title_match:
            log(f"ABORTING: existing title is too different from new title "
                f"(similarity {sim:.2f} < {TITLE_SIMILARITY_UPDATE_THRESHOLD}).")
            log("This is the 2026-05-15 incident's safety net. If you're SURE you want to overwrite, "
                "stop and verify the slug, WP ID, and intended target before changing the connector.")
            return 3
        result = wp.update_post(existing_id, payload)
        log(f"UPDATEd existing WP post {result['id']} — {result['link']}")
    log(f"edit URL: {cfg.wp_base_url}/wp-admin/post.php?post={result['id']}&action=edit")
    try:
        verified = wp.get_post(result["id"])
        log("verified WP readback: "
            f"id={verified.get('id')} "
            f"status={verified.get('status')!r} "
            f"slug={verified.get('slug')!r} "
            f"link={verified.get('link')!r}")
    except Exception as e:
        log(f"WARNING: post-write verification GET failed: {e}")
    return 0


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
    p.add_argument("--diff", action="store_true",
                   help="Print a no-write diff against the existing slug target and exit. "
                        "Requires WP credentials but never creates, updates, uploads media, or creates terms.")
    p.add_argument("--title", default=None,
                   help="Override the post title (otherwise derived from Notion title property).")
    p.add_argument("--slug", default=None,
                   help="Override the post slug (otherwise slugified from title).")
    p.add_argument("--date", default=None,
                   help="Override the post date, ISO format e.g. 2026-05-07T11:37:33.")
    p.add_argument(
        "--category",
        default=None,
        help="Override Notion Type → WP category routing. Required for Feature posts when tags are ambiguous.",
    )
    args = p.parse_args()
    sys.exit(run(
        args.notion_url,
        dry_run=args.dry_run,
        force_publish=args.publish,
        allow_update=args.update,
        title_override=args.title,
        slug_override=args.slug,
        date_override=args.date,
        category_override=args.category,
        diff_update=args.diff,
    ))


if __name__ == "__main__":
    main()
