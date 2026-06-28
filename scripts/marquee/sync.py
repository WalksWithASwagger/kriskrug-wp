#!/usr/bin/env python3
"""SYNC — push marquee boards from marquee.json into the WordPress `marquee_board` CPT.

Dry-run by default (prints payloads, writes nothing). Live writes require BOTH `--execute`
and WP credentials in scripts/notion-to-wp/.env. CREATE-by-default; `--update` is guarded by a
title-similarity check. The OG card (dist/<slug>/og.png) is uploaded as the featured image.

Usage:
  python3 scripts/marquee/sync.py                 # dry-run all boards
  python3 scripts/marquee/sync.py --execute       # live create (KK approval)
  python3 scripts/marquee/sync.py --execute --update   # allow guarded updates
"""
from __future__ import annotations
import argparse
import sys

from marquee_lib import load, DIST_DIR, slugify
import wp_sync


def main() -> int:
    ap = argparse.ArgumentParser(description="Sync marquee boards to WordPress (default: dry-run)")
    ap.add_argument("--execute", action="store_true", help="perform live writes (default is dry-run)")
    ap.add_argument("--update", action="store_true", help="allow updating existing boards (title-guarded)")
    ap.add_argument("--limit", type=int, default=0, help="max boards to process (0 = all)")
    args = ap.parse_args()

    data = load()
    boards = data.get("boards", [])
    if args.limit:
        boards = boards[: args.limit]
    print(f"Marquee sync — {len(boards)} board(s) — mode: {'LIVE' if args.execute else 'dry-run'}\n")

    wp = None
    if args.execute:
        creds = wp_sync.load_wp_credentials()
        if not (creds["user"] and creds["app_password"]):
            print("ERROR: WP_USER and WP_APP_PASSWORD required in scripts/notion-to-wp/.env for --execute")
            return 1
        try:
            wp = wp_sync.MarqueeWP(creds["base"], creds["user"], creds["app_password"])
        except ImportError:
            print("ERROR: the 'requests' package is required for live writes")
            return 1
        print(f"Target: {creds['base']}  user: {creds['user']}\n")

    results = []
    for b in boards:
        slug = b.get("seo", {}).get("slug") or slugify(" ".join(b["board"]))
        og = DIST_DIR / slug / "og.png"
        results.append(
            wp_sync.sync_board(wp, b, og if og.exists() else None,
                               execute=args.execute, allow_update=args.update)
        )

    counts = {}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    print("\nSummary: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    if not args.execute:
        print("Dry run only. Re-run with --execute (and creds) to write — see plugins/kk-marquee-board/DEPLOYMENT.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
