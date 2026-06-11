#!/usr/bin/env python3
"""Read-only category coverage audit for recent WordPress posts."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import asdict, dataclass
from html import unescape
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen


DEFAULT_BASE_URL = "https://kriskrug.co"
DEFAULT_POST_LIMIT = 100


@dataclass(frozen=True)
class Category:
    wp_id: int
    name: str
    slug: str
    live_count: int | None


@dataclass(frozen=True)
class PostRecord:
    wp_id: int
    slug: str
    title: str
    link: str
    date: str
    category_ids: tuple[int, ...]


def strip_html(value: str | None) -> str:
    if not value:
        return ""
    text = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", unescape(text)).strip()


def category_from_item(item: dict[str, Any]) -> Category:
    return Category(
        wp_id=int(item.get("id") or 0),
        name=strip_html(str(item.get("name") or "")),
        slug=str(item.get("slug") or ""),
        live_count=int(item["count"]) if item.get("count") is not None else None,
    )


def post_from_item(item: dict[str, Any]) -> PostRecord:
    title = item.get("title") or {}
    rendered_title = title.get("rendered") if isinstance(title, dict) else title
    return PostRecord(
        wp_id=int(item.get("id") or 0),
        slug=str(item.get("slug") or ""),
        title=strip_html(str(rendered_title or "")),
        link=str(item.get("link") or ""),
        date=str(item.get("date") or ""),
        category_ids=tuple(int(value) for value in item.get("categories") or []),
    )


def is_misc_category(category: Category) -> bool:
    return category.slug.casefold() == "misc" or category.name.casefold() == "misc"


def build_audit(posts: list[PostRecord], categories: dict[int, Category]) -> dict[str, Any]:
    category_counts = Counter(category_id for post in posts for category_id in post.category_ids)
    category_size_counts = Counter(len(post.category_ids) for post in posts)
    misc_ids = {category_id for category_id, category in categories.items() if is_misc_category(category)}
    misc_posts = [post for post in posts if misc_ids.intersection(post.category_ids)]
    unknown_ids = sorted(category_id for category_id in category_counts if category_id not in categories)

    category_rows = []
    for category_id in sorted(set(category_counts) | set(categories)):
        category = categories.get(category_id)
        category_rows.append(
            {
                "id": category_id,
                "name": category.name if category else f"Unknown category {category_id}",
                "slug": category.slug if category else "",
                "recent_post_count": category_counts.get(category_id, 0),
                "live_count": category.live_count if category else None,
                "is_misc": bool(category and is_misc_category(category)),
            }
        )
    category_rows.sort(key=lambda row: (-row["recent_post_count"], row["name"].casefold(), row["id"]))

    return {
        "posts_scanned": len(posts),
        "category_counts": category_rows,
        "misc": {
            "category_ids": sorted(misc_ids),
            "recent_post_count": len(misc_posts),
            "live_count": sum((categories[category_id].live_count or 0) for category_id in misc_ids),
            "recent_posts": [post_summary(post) for post in misc_posts],
            "status": "found" if misc_ids else "not_found",
        },
        "multi_category_distribution": [
            {"categories_per_post": size, "posts": count} for size, count in sorted(category_size_counts.items())
        ],
        "multi_category_posts": [
            post_summary(post) | {"category_ids": list(post.category_ids)}
            for post in posts
            if len(post.category_ids) > 1
        ],
        "empty_categories": [
            asdict(category)
            for category in sorted(categories.values(), key=lambda item: (item.name.casefold(), item.wp_id))
            if category.live_count == 0
        ],
        "unknown_category_ids": unknown_ids,
    }


def post_summary(post: PostRecord) -> dict[str, Any]:
    return {
        "id": post.wp_id,
        "slug": post.slug,
        "title": post.title,
        "link": post.link,
        "date": post.date,
    }


def render_human(report: dict[str, Any]) -> str:
    audit = report["audit"]
    lines = [
        f"Category coverage audit: {report['base_url']}",
        "Read-only: public WordPress REST GET requests only; no create/update/delete calls.",
        "",
        f"Recent posts requested: {report['post_limit']}",
        f"Recent posts scanned: {audit['posts_scanned']}",
        "",
        "Misc usage:",
        misc_line(audit["misc"]),
        "",
        "Multi-category distribution:",
    ]
    for row in audit["multi_category_distribution"]:
        label = "category" if row["categories_per_post"] == 1 else "categories"
        lines.append(f"- {row['categories_per_post']} {label}: {row['posts']} posts")
    if not audit["multi_category_distribution"]:
        lines.append("- No posts scanned.")

    lines.extend(
        [
            "",
            "Category counts for recent posts:",
            "",
            "| Category | Slug | Recent posts | Live count | Flags |",
            "|---|---|---:|---:|---|",
        ]
    )
    for row in audit["category_counts"]:
        flags = []
        if row["is_misc"]:
            flags.append("Misc")
        if row["live_count"] == 0:
            flags.append("empty")
        if row["id"] in audit["unknown_category_ids"]:
            flags.append("unknown")
        live_count = "" if row["live_count"] is None else str(row["live_count"])
        lines.append(
            f"| {row['name']} | `{row['slug'] or '-'}` | {row['recent_post_count']} | "
            f"{live_count} | {', '.join(flags) or '-'} |"
        )

    lines.extend(["", "Empty categories:"])
    if audit["empty_categories"]:
        for category in audit["empty_categories"]:
            lines.append(f"- {category['name']} (`{category['slug']}`)")
    else:
        lines.append("- None found in category REST response.")

    lines.extend(["", "Recent Misc posts:"])
    if audit["misc"]["recent_posts"]:
        for post in audit["misc"]["recent_posts"]:
            label = post["slug"] or post["title"] or f"post-{post['id']}"
            lines.append(f"- {post['date']} `{label}` ({post['link']})")
    else:
        lines.append("- None in the scanned recent posts.")

    return "\n".join(lines) + "\n"


def misc_line(misc: dict[str, Any]) -> str:
    if misc["status"] == "not_found":
        return "- Misc category was not present in the category REST response."
    return (
        f"- {misc['recent_post_count']} scanned posts use Misc "
        f"(category IDs: {', '.join(str(value) for value in misc['category_ids'])}; "
        f"live count: {misc['live_count']})."
    )


def fetch_json_page(base_url: str, path: str, params: dict[str, Any], timeout: int) -> tuple[list[dict[str, Any]], int]:
    url = base_url.rstrip("/") + path + "?" + urlencode(params)
    request = Request(
        url,
        headers={"Accept": "application/json", "User-Agent": "kriskrug-category-coverage-audit/1.0"},
    )
    with urlopen(request, timeout=timeout) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        payload = json.loads(response.read().decode(charset, "replace"))
        if not isinstance(payload, list):
            raise RuntimeError(f"Expected list payload from {path}")
        total_pages = int(response.headers.get("X-WP-TotalPages") or "1")
        return payload, total_pages


def fetch_paginated(
    base_url: str,
    path: str,
    params: dict[str, Any],
    timeout: int,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    page = 1
    while True:
        remaining = None if limit is None else limit - len(items)
        if remaining is not None and remaining <= 0:
            break
        page_params = dict(params)
        page_params["page"] = page
        page_params["per_page"] = min(100, remaining) if remaining is not None else 100
        batch, total_pages = fetch_json_page(base_url, path, page_params, timeout)
        if not batch:
            break
        items.extend(batch)
        if page >= total_pages:
            break
        page += 1
    return items[:limit] if limit is not None else items


def collect_report(base_url: str, post_limit: int, timeout: int) -> dict[str, Any]:
    post_items = fetch_paginated(
        base_url,
        "/wp-json/wp/v2/posts",
        {
            "status": "publish",
            "orderby": "date",
            "order": "desc",
            "_fields": "id,slug,title,link,date,categories",
        },
        timeout,
        limit=post_limit,
    )
    category_items = fetch_paginated(
        base_url,
        "/wp-json/wp/v2/categories",
        {
            "hide_empty": "false",
            "orderby": "name",
            "order": "asc",
            "_fields": "id,name,slug,count",
        },
        timeout,
    )
    posts = [post_from_item(item) for item in post_items]
    categories = {
        category.wp_id: category
        for category in (category_from_item(item) for item in category_items)
    }
    return {
        "base_url": base_url.rstrip("/"),
        "post_limit": post_limit,
        "read_only": True,
        "rest_requests": [
            "GET /wp-json/wp/v2/posts",
            "GET /wp-json/wp/v2/categories",
        ],
        "audit": build_audit(posts, categories),
    }


def minimum_post_limit(value: str) -> int:
    parsed = int(value)
    if parsed < DEFAULT_POST_LIMIT:
        raise argparse.ArgumentTypeError(f"must be at least {DEFAULT_POST_LIMIT}")
    return parsed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument(
        "--limit",
        type=minimum_post_limit,
        default=DEFAULT_POST_LIMIT,
        help="Recent posts to scan; minimum 100.",
    )
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--format", choices=("human", "json"), default="human")
    args = parser.parse_args()

    report = collect_report(args.base_url, args.limit, args.timeout)
    if args.format == "json":
        print(json.dumps(report, indent=2))
    else:
        print(render_human(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
