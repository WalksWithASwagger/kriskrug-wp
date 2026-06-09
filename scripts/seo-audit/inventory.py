#!/usr/bin/env python3
"""Read-only Jetpack SEO metadata inventory for posts and pages."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

from inventory_lib import SEORecord, record_from_item, render_markdown, summarize, write_csv

SCRIPT_DIR = Path(__file__).resolve().parent
NOTION_DIR = SCRIPT_DIR.parent / "notion-to-wp"
sys.path.insert(0, str(NOTION_DIR))

from kk_notion_to_wp import WordPress, load_config  # noqa: E402


def fetch_published(wp: WordPress, kind: str) -> list[dict[str, Any]]:
    endpoint = "posts" if kind == "post" else "pages"
    page = 1
    items: list[dict[str, Any]] = []
    while True:
        response = wp.s.get(
            f"{wp.base}/wp-json/wp/v2/{endpoint}",
            params={
                "status": "publish",
                "per_page": 100,
                "page": page,
                "context": "edit",
                "_fields": "id,slug,title,link,meta",
            },
            timeout=60,
        )
        response.raise_for_status()
        batch = response.json()
        if not batch:
            break
        items.extend(batch)
        total_pages = int(response.headers.get("X-WP-TotalPages", "1"))
        if page >= total_pages:
            break
        page += 1
    return items


def collect_inventory(wp: WordPress) -> list[SEORecord]:
    records: list[SEORecord] = []
    for kind in ("post", "page"):
        for item in fetch_published(wp, kind):
            records.append(record_from_item(kind, item))
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only Jetpack SEO metadata inventory")
    parser.add_argument("--format", choices=("markdown", "json", "csv"), default="markdown")
    parser.add_argument("--output", type=Path, help="Write CSV/JSON to this path")
    args = parser.parse_args()

    cfg = load_config()
    if not cfg.has_wp_credentials:
        print("WP_USER and WP_APP_PASSWORD required in scripts/notion-to-wp/.env", file=sys.stderr)
        return 1

    wp = WordPress(cfg.wp_base_url, cfg.wp_user, cfg.wp_app_password)
    records = collect_inventory(wp)

    if args.format == "json":
        payload = {"summary": summarize(records), "records": [asdict(r) for r in records]}
        text = json.dumps(payload, indent=2)
        if args.output:
            args.output.write_text(text + "\n", encoding="utf-8")
        else:
            print(text)
    elif args.format == "csv":
        out = args.output or Path("content/seo-audit-inventory.csv")
        write_csv(out, records)
        print(f"Wrote {len(records)} rows to {out}")
    else:
        print(render_markdown(records))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
