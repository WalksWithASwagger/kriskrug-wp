#!/usr/bin/env python3
"""Classify GSC 404 export URLs and emit redirect recommendations."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse


GOOGLEBOT_UA = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"

SHRINE_TARGET = (
    "https://kriskrug.co/2023/08/25/"
    "burning-man-art-projects-uncle-charlies-red-hot-cock-tyson-ayers-shrine-of-sympathetic-resonance/"
)
FIRE_PODCAST_TARGET = (
    "https://kriskrug.co/2023/07/28/"
    "future-in-review-conference-and-fire-podcast-an-insiders-view/"
)
BRYGHT_PARENT = "/2007/08/07/bryght-world-tour-2007/"
DEAD_CATEGORY_SLUGS = (
    "art",
    "bioblitz",
    "community",
    "friends",
    "web-20",
    "artificial-intelligence",
    "web-design",
    "gastown",
    "communication",
)
DEAD_POST_IDS = ("87", "107", "142", "247", "280")
DEAD_PAGE_IDS = ("504", "843")
TRACKING_QUERY_KEYS = frozenset({"share", "nb", "amp"})


@dataclass(frozen=True)
class AuditRow:
    url: str
    last_crawled: str
    bucket: str
    live_status: str
    recommended_action: str
    redirect_target: str


def classify_url(url: str) -> tuple[str, str, str]:
    parsed = urlparse(url)
    path = parsed.path or "/"
    query = parse_qs(parsed.query, keep_blank_values=True)

    if url.endswith("/]") or url.endswith("/*") or "wp-*.php" in url:
        return "junk", "skip", ""

    if "share" in query:
        clean = f"{parsed.scheme}://{parsed.netloc}{path.rstrip('/')}/"
        return "share_query", "query_param_snippet", clean

    if "amp" in query or parsed.query in ("amp=1", "amp"):
        base_path = path.rstrip("/") + "/"
        if base_path.startswith("/category/"):
            slug = base_path.removeprefix("/category/").strip("/").split("/")[0]
            if slug in DEAD_CATEGORY_SLUGS:
                return "amp_deleted_category", "redirection", "/blog/"
        return "amp_query", "query_param_snippet", f"{parsed.scheme}://{parsed.netloc}{base_path}"

    if path.startswith("/category/"):
        slug = path.removeprefix("/category/").strip("/").split("/")[0]
        if slug in DEAD_CATEGORY_SLUGS:
            return "deleted_category", "redirection", "/blog/"
        if path == "/category/field-notes/page/3/":
            return "pagination_overflow", "redirection", "/category/field-notes/page/2/"
        return "category_other", "review", ""

    if path.startswith(BRYGHT_PARENT.rstrip("/") + "/"):
        return "drupal_bryght_subpath", "redirection", BRYGHT_PARENT

    if path.startswith("/2006/07/07/gnomedex-6/"):
        return "drupal_gnomedex_subpath", "redirection", "/2006/07/07/gnomedex-6/"

    if path.startswith("/2006/03/25/sxsw-wrap-up/"):
        return "drupal_sxsw_subpath", "redirection", "/2006/03/25/sxsw-wrap-up/"

    if path.startswith("/2006/03/30/tech-village-switch-on-event-with-communicopia/"):
        return "drupal_techvillage_subpath", "redirection", "/2006/03/30/tech-village-switch-on-event-with-communicopia/"

    if path == "/node/216":
        return "drupal_node", "redirection", "/blog/"

    if query.get("p") and query["p"][0] in DEAD_POST_IDS:
        return "dead_post_id", "redirection", "/blog/"

    if query.get("page_id") and query["page_id"][0] in DEAD_PAGE_IDS:
        return "dead_page_id", "redirection", "/blog/"

    if path == "/quote-request/":
        return "dead_page", "redirection", "/contact/"

    if path == "/2023/09/28/future-in-review-podcast/":
        return "dead_page", "redirection", FIRE_PODCAST_TARGET

    if path.rstrip("/") == "/shrine":
        return "dead_page", "redirection", SHRINE_TARGET

    if path.rstrip("/") == "/spark/wordpress":
        return "legacy_wp_root", "redirection", "/blog/"

    return "other", "review", ""


def curl_status(url: str) -> str:
    result = subprocess.run(
        [
            "curl",
            "-sI",
            "-o",
            "/dev/null",
            "-w",
            "%{http_code}",
            "-A",
            GOOGLEBOT_UA,
            url,
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    code = result.stdout.strip()
    return code or "error"


def load_rows(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def audit_rows(rows: list[dict[str, str]], check_live: bool) -> list[AuditRow]:
    audited: list[AuditRow] = []
    for row in rows:
        url = row["URL"]
        bucket, action, target = classify_url(url)
        status = curl_status(url) if check_live else ""
        audited.append(
            AuditRow(
                url=url,
                last_crawled=row.get("Last crawled", ""),
                bucket=bucket,
                live_status=status,
                recommended_action=action,
                redirect_target=target,
            )
        )
    return audited


def write_redirect_csv(rows: list[AuditRow], output_path: Path) -> int:
    redirect_rows = [
        row
        for row in rows
        if row.recommended_action == "redirection" and row.redirect_target
    ]
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source_url", "target_url", "bucket"])
        writer.writeheader()
        for row in redirect_rows:
            writer.writerow(
                {
                    "source_url": row.url,
                    "target_url": row.redirect_target,
                    "bucket": row.bucket,
                }
            )
    return len(redirect_rows)


def print_summary(rows: list[AuditRow]) -> None:
    buckets = Counter(row.bucket for row in rows)
    actions = Counter(row.recommended_action for row in rows)
    statuses = Counter(row.live_status for row in rows if row.live_status)

    print(f"URLs audited: {len(rows)}")
    print("\nBuckets:")
    for bucket, count in buckets.most_common():
        print(f"  {bucket}: {count}")

    print("\nRecommended actions:")
    for action, count in actions.most_common():
        print(f"  {action}: {count}")

    if statuses:
        print("\nLive status codes:")
        for status, count in statuses.most_common():
            print(f"  {status}: {count}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--csv",
        type=Path,
        required=True,
        help="Path to GSC Table.csv export (required; no machine-local default)",
    )
    parser.add_argument(
        "--check-live",
        action="store_true",
        help="HEAD-check each URL with a Googlebot user agent",
    )
    parser.add_argument(
        "--redirect-csv",
        type=Path,
        help="Write redirection recommendations to this CSV path",
    )
    parser.add_argument(
        "--json",
        type=Path,
        help="Write full audit rows as JSON",
    )
    args = parser.parse_args(argv)

    if not args.csv.exists():
        print(f"CSV not found: {args.csv}", file=sys.stderr)
        return 1

    source_rows = load_rows(args.csv)
    audited = audit_rows(source_rows, args.check_live)
    print_summary(audited)

    if args.redirect_csv:
        count = write_redirect_csv(audited, args.redirect_csv)
        print(f"\nWrote {count} redirection rows to {args.redirect_csv}")

    if args.json:
        args.json.write_text(
            json.dumps([asdict(row) for row in audited], indent=2),
            encoding="utf-8",
        )
        print(f"Wrote audit JSON to {args.json}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
