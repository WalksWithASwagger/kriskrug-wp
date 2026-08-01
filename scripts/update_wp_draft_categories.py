#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import html
import json
import os

import requests


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


def fetch_post(session: requests.Session, base_url: str, post_id: int) -> dict:
    response = session.get(
        f"{base_url}/wp-json/wp/v2/posts/{post_id}",
        params={"context": "edit"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def main() -> int:
    parser = argparse.ArgumentParser(description="Assign existing categories to a guarded WordPress draft")
    parser.add_argument("post_id", type=int)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--category", type=int, action="append", required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    desired = sorted(set(args.category))
    session, base_url = auth_session()
    post = fetch_post(session, base_url, args.post_id)
    title = post.get("title", {}).get("raw") or post.get("title", {}).get("rendered")
    if post.get("id") != args.post_id:
        raise SystemExit("[ABORT] readback returned the wrong post id")
    if post.get("status") != "draft":
        raise SystemExit(f"[ABORT] post is not a draft: {post.get('status')!r}")
    if post.get("slug") != args.slug:
        raise SystemExit(f"[ABORT] slug mismatch: {post.get('slug')!r}")
    if title != args.title:
        raise SystemExit(f"[ABORT] title mismatch: {title!r}")

    categories: dict[int, str] = {}
    for category_id in desired:
        response = session.get(
            f"{base_url}/wp-json/wp/v2/categories/{category_id}",
            timeout=30,
        )
        response.raise_for_status()
        category = response.json()
        categories[category_id] = html.unescape(str(category.get("name", "")))
    if any(not name for name in categories.values()):
        raise SystemExit("[ABORT] one or more category ids did not resolve to a name")

    before = sorted(post.get("categories") or [])
    print(json.dumps({"post_id": args.post_id, "before": before, "after": desired, "names": categories}, indent=2))
    if before == desired:
        print("[NOOP] draft already has the requested categories")
        return 0
    if not args.apply:
        print("[DRY RUN] no WordPress write; pass --apply to update the draft")
        return 0

    response = session.post(
        f"{base_url}/wp-json/wp/v2/posts/{args.post_id}",
        json={"categories": desired},
        timeout=30,
    )
    response.raise_for_status()
    readback = fetch_post(session, base_url, args.post_id)
    if readback.get("status") != "draft" or sorted(readback.get("categories") or []) != desired:
        raise SystemExit("[ABORT] category update readback failed")
    print(f"[APPLIED] post={args.post_id} status=draft categories={desired}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
