#!/usr/bin/env python3
"""Read-only Jetpack SEO metadata inventory for posts and pages."""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any

from inventory_lib import (
    SEORecord,
    meta_keys_registered,
    record_from_item,
    record_from_rendered,
    render_markdown,
    summarize,
    write_csv,
)

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


UNREGISTERED_META_HELP = """\
ERROR: the Jetpack SEO meta keys are not exposed by REST on this site.

Every published item came back with those keys absent from `meta`, which this
audit cannot distinguish from "no SEO title set". Reporting the inventory now
would claim every item is missing its SEO metadata, which is false: the values
are still in wp_postmeta and still rendering, because
theme/kk-aurora/inc/seo-title.php reads them with get_post_meta().

Cause: Jetpack registers these keys for REST, and Jetpack is deactivated.

Consequence beyond this audit: REST *writes* to these keys silently no-op too.
WordPress drops unregistered meta without erroring, so any script that PATCHes
jetpack_seo_html_title appears to succeed and changes nothing.

To measure what crawlers actually see, run with --source rendered.\
"""


def collect_inventory(wp: WordPress, items_by_kind: dict) -> list[SEORecord]:
    records: list[SEORecord] = []
    for kind, items in items_by_kind.items():
        for item in items:
            records.append(record_from_item(kind, item))
    return records


def collect_rendered_inventory(wp: WordPress, items_by_kind: dict) -> list[SEORecord]:
    records: list[SEORecord] = []
    for kind, items in items_by_kind.items():
        for item in items:
            link = str(item.get("link") or "")
            if not link:
                continue
            separator = "&" if "?" in link else "?"
            response = wp.s.get(
                f"{link}{separator}cachebust={int(time.time())}", timeout=60
            )
            response.raise_for_status()
            records.append(record_from_rendered(kind, item, response.text))
    return records


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read-only Jetpack SEO metadata inventory"
    )
    parser.add_argument(
        "--format", choices=("markdown", "json", "csv"), default="markdown"
    )
    parser.add_argument("--output", type=Path, help="Write CSV/JSON to this path")
    parser.add_argument(
        "--source",
        choices=("meta", "rendered"),
        default="meta",
        help="meta reads REST post meta; rendered reads delivered HTML",
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Audit at most this many items per kind (sampling, --source rendered)",
    )
    args = parser.parse_args()

    cfg = load_config()
    if not cfg.has_wp_credentials:
        print(
            "WP_USER and WP_APP_PASSWORD required in scripts/notion-to-wp/.env",
            file=sys.stderr,
        )
        return 1

    wp = WordPress(cfg.wp_base_url, cfg.wp_user, cfg.wp_app_password)
    items_by_kind = {kind: fetch_published(wp, kind) for kind in ("post", "page")}
    if args.limit:
        items_by_kind = {k: v[: args.limit] for k, v in items_by_kind.items()}

    if args.source == "rendered":
        records = collect_rendered_inventory(wp, items_by_kind)
    else:
        all_items = [item for items in items_by_kind.values() for item in items]
        if all_items and not meta_keys_registered(all_items):
            print(UNREGISTERED_META_HELP, file=sys.stderr)
            return 2
        records = collect_inventory(wp, items_by_kind)

    if args.format == "json":
        payload = {
            "source": args.source,
            "summary": summarize(records),
            "records": [asdict(r) for r in records],
        }
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
        print(render_markdown(records, args.source))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
