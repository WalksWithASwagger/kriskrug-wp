#!/usr/bin/env python3
"""Update an EXISTING WordPress draft in place from a local draft package.

Companion to `create_local_wp_draft.py`, which is create-only. This one targets
an existing post by id and reuses the same build pipeline (post.html is the
canonical Gutenberg body, frontmatter `images:` uploaded or reused from
publish.log, body <img src> rewritten to the uploaded media URLs), then calls
`wp.update_post(id)` instead of `create_post`.

Guards: the target must exist, be status `draft`, and own the package slug. The
slug is never changed on update. Dry-run by default; pass --execute to write.

Usage:
  python update_local_wp_draft.py <post_md> --wp-id <ID> [--execute]

Note: Jetpack SEO post-meta (jetpack_seo_html_title / advanced_seo_description)
500s when the value contains a combining-diacritic sequence (e.g. "Ethọ́s").
Keep SEO meta in the package frontmatter precomposed/ASCII; the visible title
and body can keep the diacritics.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from create_local_wp_draft import (  # noqa: E402
    build_payload,
    ensure_terms,
    image_entries,
    load_package,
    load_wp_config,
    log_line,
    quality_issues,
    rewrite_uploaded_images,
    upload_images,
)
from kk_notion_to_wp import WordPress  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("post_md", type=Path)
    parser.add_argument("--wp-id", type=int, required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", dest="dry_run", action="store_true", default=True)
    mode.add_argument("--execute", dest="dry_run", action="store_false")
    args = parser.parse_args()

    pkg = load_package(args.post_md)
    issues = quality_issues(pkg)
    if issues:
        raise SystemExit("quality gate failed: " + "; ".join(issues))

    cfg = load_wp_config()
    wp = WordPress(cfg.base_url, cfg.user, cfg.app_password)

    existing = wp.get_post(args.wp_id)
    if existing.get("slug") != pkg.slug:
        raise SystemExit(f"slug mismatch: WP={existing.get('slug')!r} local={pkg.slug!r}")
    if existing.get("status") != "draft":
        raise SystemExit(
            f"refusing to update non-draft post {args.wp_id}: status={existing.get('status')!r}"
        )

    if args.dry_run:
        print(
            f"DRY RUN: would update {args.wp_id} ({pkg.slug}); "
            f"images={[p.name for p, _ in image_entries(pkg)]}"
        )
        return 0

    uploaded = upload_images(wp, pkg)
    content = rewrite_uploaded_images(pkg.body_html, pkg.draft_dir, uploaded)
    if re.search(r'src="(?:/Users/|content/drafts/|images/)', content):
        raise SystemExit("rewritten HTML still contains local image paths")

    payload = build_payload(pkg, cfg, content, uploaded)
    categories = payload.pop("_local_categories", [])
    tags = payload.pop("_local_tags", [])
    if categories:
        payload["categories"] = ensure_terms(wp, "categories", categories)
    if tags:
        payload["tags"] = ensure_terms(wp, "tags", tags)
    payload.pop("slug", None)  # never change the slug on update

    result = wp.update_post(args.wp_id, payload)
    readback = wp.get_post(int(result["id"]))
    if readback.get("status") != "draft" or readback.get("slug") != pkg.slug:
        raise SystemExit(
            f"unexpected readback: id={readback.get('id')} "
            f"status={readback.get('status')!r} slug={readback.get('slug')!r}"
        )
    log_line(
        pkg,
        f"updated WP draft id={readback.get('id')} status={readback.get('status')} "
        f"link={readback.get('link')}",
    )
    print(
        f"UPDATED: {readback.get('id')} status={readback.get('status')} "
        f"featured_media={readback.get('featured_media')} "
        f"edit={cfg.base_url}/wp-admin/post.php?post={readback.get('id')}&action=edit"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
