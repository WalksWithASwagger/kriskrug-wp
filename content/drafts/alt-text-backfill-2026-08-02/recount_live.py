#!/usr/bin/env python3
"""Re-verify the alt-text inventory headline against live kriskrug.co HTML.

Read-only. Issues GET requests only, never writes to the site.

The original crawler that produced inventory.csv was not committed. This script
rebuilds the checkable half of it: it takes the route list straight out of the
delivered CSV, re-fetches every route, re-classifies every rendered <img> with
the shared helpers in scripts/public_image_audit.py, and reports two different
totals that the first pass conflated:

  occurrences        every <img> element in the delivered HTML
  unique (page, src) what inventory.csv actually stores, one row each

Usage:
  python3 recount_live.py                      # all 216 routes from inventory.csv
  python3 recount_live.py --top-routes-only    # just the 10 tier-1 routes
  python3 recount_live.py --json out.json      # machine-readable totals
"""

from __future__ import annotations

import argparse
import collections
import csv
import json
import sys
import time
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from public_image_audit import ImageParser, RenderedImage  # noqa: E402

CSV_PATH = HERE / "inventory.csv"
TRACKING_PIXEL_MARKER = "facebook.com/tr"
USER_AGENT = "KrisKrugAltInventoryRecount/1.0 (read-only)"


def routes_from_csv(csv_path: Path, top_only: bool) -> list[str]:
    seen: dict[str, str] = {}
    with csv_path.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            seen.setdefault(row["page_url"], row["tier"])
    if top_only:
        return [u for u, tier in seen.items() if tier == "1-top-route"]
    return list(seen)


def csv_row_counts(csv_path: Path) -> collections.Counter:
    with csv_path.open(newline="", encoding="utf-8") as fh:
        return collections.Counter(row["page_url"] for row in csv.DictReader(fh))


def classify(url: str, attrs: dict[str, str]) -> str:
    src = attrs.get("src", "")
    if TRACKING_PIXEL_MARKER in src:
        return "decorative-tracking-pixel"
    rendered = RenderedImage(
        page_url=url,
        page_kind="",
        page_id=None,
        page_slug="",
        src=src,
        alt=attrs.get("alt"),
        media_id=None,
        loading=attrs.get("loading", ""),
        has_srcset=bool(attrs.get("srcset")),
        classes=attrs.get("class", ""),
        role=attrs.get("role", ""),
        width=attrs.get("width", ""),
        height=attrs.get("height", ""),
    )
    state = rendered.alt_state
    return {
        "empty": "empty-alt-content-VIOLATION",
        "missing-attr": "missing-alt-attr-VIOLATION",
        "filename-style": "filename-style-alt-VIOLATION",
        "decorative-empty": "decorative-empty-correct",
        "ok": "has-alt",
    }[state]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--top-routes-only", action="store_true")
    ap.add_argument("--delay", type=float, default=0.25)
    ap.add_argument("--json", type=Path)
    args = ap.parse_args()

    routes = routes_from_csv(CSV_PATH, args.top_routes_only)
    expected = csv_row_counts(CSV_PATH)
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    occ_class: collections.Counter = collections.Counter()
    uniq_class: collections.Counter = collections.Counter()
    total_occ = 0
    total_uniq = 0
    collapsed: list[tuple[str, str, int]] = []
    fetch_errors: list[tuple[str, str]] = []

    for i, url in enumerate(routes, 1):
        try:
            resp = session.get(url, timeout=20)
            resp.raise_for_status()
        except requests.RequestException as exc:  # network truth, not a silent skip
            fetch_errors.append((url, str(exc)))
            continue
        parser = ImageParser(url)
        parser.feed(resp.text)
        per_src: dict[str, list[dict[str, str]]] = collections.defaultdict(list)
        for attrs in parser.images:
            per_src[attrs.get("src", "")].append(attrs)
        for src, group in per_src.items():
            klass = classify(url, group[0])
            occ_class[klass] += len(group)
            uniq_class[klass] += 1
            total_occ += len(group)
            total_uniq += 1
            if len(group) > 1:
                collapsed.append((url, src, len(group)))
        print(
            f"[{i}/{len(routes)}] {url} occ={sum(len(g) for g in per_src.values())} "
            f"uniq={len(per_src)} csv={expected[url]}",
            file=sys.stderr,
        )
        time.sleep(args.delay)

    result = {
        "routes_fetched": len(routes) - len(fetch_errors),
        "routes_requested": len(routes),
        "fetch_errors": fetch_errors,
        "occurrences_total": total_occ,
        "unique_page_src_total": total_uniq,
        "csv_rows_for_these_routes": sum(expected[u] for u in routes),
        "by_classification_occurrences": dict(occ_class),
        "by_classification_unique": dict(uniq_class),
        "collapsed_duplicate_src": [
            {"page_url": u, "src": s, "occurrences": n} for u, s, n in collapsed
        ],
        "violation_occurrences": sum(
            v for k, v in occ_class.items() if k.endswith("VIOLATION")
        ),
        "violation_unique": sum(
            v for k, v in uniq_class.items() if k.endswith("VIOLATION")
        ),
    }
    print(json.dumps(result, indent=2))
    if args.json:
        args.json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
