#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
from pathlib import Path

import requests


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def auth_session() -> tuple[requests.Session, str]:
    base_url = os.getenv("WP_BASE_URL", "https://kriskrug.co").rstrip("/")
    user = os.getenv("WP_USER") or os.getenv("WP_API_USERNAME")
    password = (os.getenv("WP_APP_PASSWORD") or os.getenv("WP_API_PASSWORD") or "").replace(" ", "")
    if not user or not password:
        raise SystemExit("[ABORT] WordPress credentials are unresolved. Run through Varlock.")
    token = base64.b64encode(f"{user}:{password}".encode()).decode()
    session = requests.Session()
    session.headers.update({"Authorization": f"Basic {token}"})
    return session, base_url


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify a WordPress post remains an exact private draft")
    parser.add_argument("post_id", type=int)
    parser.add_argument("expected_html", type=Path)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--youtube-id")
    parser.add_argument("--list-items", type=int)
    parser.add_argument("--blocks", type=int)
    parser.add_argument("--category-id", type=int, action="append")
    parser.add_argument("--seo-title")
    parser.add_argument("--seo-description")
    args = parser.parse_args()

    expected = args.expected_html.read_text(encoding="utf-8")
    session, base_url = auth_session()
    response = session.get(
        f"{base_url}/wp-json/wp/v2/posts/{args.post_id}",
        params={"context": "edit"},
        timeout=30,
    )
    response.raise_for_status()
    post = response.json()
    raw = post.get("content", {}).get("raw", "")
    title = post.get("title", {}).get("raw") or post.get("title", {}).get("rendered")
    checks = {
        "id": post.get("id") == args.post_id,
        "status_draft": post.get("status") == "draft",
        "slug": post.get("slug") == args.slug,
        "title": title == args.title,
        "content_sha_match": sha256(raw) == sha256(expected),
        "featured_media_unset": post.get("featured_media") == 0,
    }
    if args.youtube_id:
        checks["youtube_embed_once"] = (
            raw.count('providerNameSlug":"youtube"') == 1
            and raw.count(args.youtube_id) == 2
        )
    if args.list_items is not None:
        checks["list_items"] = raw.count("<li>") == args.list_items
    if args.blocks is not None:
        checks["gutenberg_blocks"] = raw.count("<!-- wp:") == args.blocks
    if args.category_id:
        checks["categories"] = sorted(post.get("categories") or []) == sorted(set(args.category_id))
    meta = post.get("meta") or {}
    if args.seo_title:
        checks["seo_title"] = meta.get("jetpack_seo_html_title") == args.seo_title
    if args.seo_description:
        checks["seo_description"] = meta.get("advanced_seo_description") == args.seo_description

    result = {
        "checks": checks,
        "content_sha256": sha256(raw),
        "modified_gmt": post.get("modified_gmt"),
        "edit_url": f"{base_url}/wp-admin/post.php?post={args.post_id}&action=edit",
        "seo_meta": {
            "jetpack_seo_html_title": meta.get("jetpack_seo_html_title"),
            "advanced_seo_description": meta.get("advanced_seo_description"),
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if all(checks.values()) else 2


if __name__ == "__main__":
    raise SystemExit(main())
