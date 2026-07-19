#!/usr/bin/env python3
"""Audit and remediate post IA/media requirements for published posts."""

from __future__ import annotations

import argparse
import base64
import dataclasses
import datetime as dt
import html
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import requests

try:
    from dotenv import dotenv_values
except Exception:  # pragma: no cover - local fallback
    dotenv_values = None


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_ENV_PATH = REPO_ROOT / "scripts" / "notion-to-wp" / ".env"
DEFAULT_BASE_URL = "https://kriskrug.co"
DEFAULT_SINCE = "2025-01-01"


def _fallback_env_paths() -> list[Path]:
    """Optional extra .env locations (env override, then ~/Code/... if present)."""
    paths: list[Path] = []
    for key in ("KKAI_ENV_PATH", "NOTION_ENV_PATH"):
        raw = os.environ.get(key)
        if raw:
            paths.append(Path(raw).expanduser())
    paths.append(Path.home() / "Code" / "notion-local" / "kk-ai-ecosystem" / ".env")
    return paths


def parse_simple_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def load_env(path: Path) -> dict[str, str]:
    if dotenv_values is not None and path.exists():
        return {
            str(k): str(v)
            for k, v in dotenv_values(path).items()
            if k and v is not None
        }
    return parse_simple_env(path)


@dataclasses.dataclass
class Config:
    base_url: str
    wp_user: str
    wp_app_password: str


@dataclasses.dataclass
class PostAudit:
    post_id: int
    slug: str
    link: str
    title: str
    featured_media: int
    featured_alt: str
    has_excerpt: bool
    has_featured: bool
    has_featured_alt: bool
    missing_excerpt: bool
    missing_featured: bool
    missing_featured_alt: bool


class WordPressClient:
    def __init__(self, config: Config, timeout: int = 30):
        token = base64.b64encode(
            f"{config.wp_user}:{config.wp_app_password}".encode("utf-8")
        ).decode("utf-8")
        self.base_url = config.base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Basic {token}"})

    def get(self, endpoint: str, params: dict[str, Any] | None = None) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response

    def post(self, endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        response = self.session.post(url, json=payload, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def paged_get(self, endpoint: str, params: dict[str, Any]) -> list[dict[str, Any]]:
        page = 1
        output: list[dict[str, Any]] = []
        while True:
            page_params = dict(params)
            page_params["page"] = page
            response = self.get(endpoint, page_params)
            batch = response.json()
            if not isinstance(batch, list):
                break
            output.extend(batch)
            total_pages = int(response.headers.get("X-WP-TotalPages", "1"))
            if page >= total_pages:
                break
            page += 1
        return output


def load_config() -> Config:
    sources = [load_env(SCRIPT_ENV_PATH)]
    sources.extend(load_env(path) for path in _fallback_env_paths())

    def value(key: str, default: str | None = None) -> str | None:
        if os.environ.get(key):
            return os.environ[key]
        for source in sources:
            if source.get(key):
                return source.get(key)
        return default

    base_url = value("WP_BASE_URL", DEFAULT_BASE_URL) or DEFAULT_BASE_URL
    wp_user = value("WP_USER")
    wp_app_password = (value("WP_APP_PASSWORD") or "").replace(" ", "")

    if not wp_user or not wp_app_password:
        sys.exit(
            f"Missing WP credentials. Set WP_USER and WP_APP_PASSWORD in {SCRIPT_ENV_PATH} "
            "or environment variables."
        )

    return Config(base_url=base_url, wp_user=wp_user, wp_app_password=wp_app_password)


def strip_html(value: str) -> str:
    text = re.sub(r"<!--.*?-->", " ", value, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def derive_excerpt(content_raw: str, max_chars: int = 220) -> str:
    text = strip_html(content_raw)
    if not text:
        return ""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    chosen = ""
    for sentence in sentences:
        candidate = f"{chosen} {sentence}".strip()
        if len(candidate) > max_chars:
            break
        chosen = candidate
        if len(chosen) >= max_chars * 0.72:
            break
    if not chosen:
        chosen = text[:max_chars].rstrip()
    return chosen


def default_alt_text(title: str) -> str:
    return f'Featured image for "{title}"'


def title_text(post: dict[str, Any]) -> str:
    title_obj = post.get("title", {})
    if isinstance(title_obj, dict):
        return strip_html(str(title_obj.get("rendered", "")))
    return strip_html(str(title_obj))


def excerpt_text(post: dict[str, Any]) -> str:
    excerpt_obj = post.get("excerpt", {})
    if isinstance(excerpt_obj, dict):
        raw = str(excerpt_obj.get("raw", "")).strip()
        if raw:
            return raw
        return strip_html(str(excerpt_obj.get("rendered", "")))
    return strip_html(str(excerpt_obj))


def load_text_only_slugs(args: argparse.Namespace) -> set[str]:
    slugs = {slug.strip() for slug in args.text_only_slug if slug.strip()}
    if args.text_only_slugs_file:
        file_path = Path(args.text_only_slugs_file)
        if not file_path.is_absolute():
            file_path = REPO_ROOT / file_path
        if file_path.exists():
            for raw in file_path.read_text(encoding="utf-8").splitlines():
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                slugs.add(line)
    return slugs


def fetch_posts(
    wp: WordPressClient,
    since_date: str,
) -> list[dict[str, Any]]:
    after_iso = f"{since_date}T00:00:00"
    params = {
        "status": "publish",
        "after": after_iso,
        "orderby": "date",
        "order": "asc",
        "per_page": 100,
        "context": "edit",
        "_fields": "id,slug,link,date,title,excerpt,featured_media",
    }
    return wp.paged_get("/wp-json/wp/v2/posts", params)


def fetch_media(wp: WordPressClient, media_id: int, cache: dict[int, dict[str, Any]]) -> dict[str, Any]:
    if media_id in cache:
        return cache[media_id]
    media = wp.get(
        f"/wp-json/wp/v2/media/{media_id}",
        params={"context": "edit", "_fields": "id,alt_text,source_url"},
    ).json()
    cache[media_id] = media
    return media


def audit_posts(
    wp: WordPressClient,
    posts: list[dict[str, Any]],
    text_only_slugs: set[str],
) -> list[PostAudit]:
    media_cache: dict[int, dict[str, Any]] = {}
    audits: list[PostAudit] = []

    for post in posts:
        post_id = int(post["id"])
        slug = str(post["slug"])
        link = str(post.get("link", ""))
        title = title_text(post)
        excerpt = excerpt_text(post)
        featured_media = int(post.get("featured_media") or 0)
        has_excerpt = bool(excerpt)
        has_featured = featured_media > 0
        featured_alt = ""

        if has_featured:
            media = fetch_media(wp, featured_media, media_cache)
            featured_alt = str(media.get("alt_text", "")).strip()

        has_featured_alt = bool(featured_alt) if has_featured else False
        missing_excerpt = not has_excerpt
        missing_featured = (not has_featured) and (slug not in text_only_slugs)
        missing_featured_alt = has_featured and (not has_featured_alt)

        audits.append(
            PostAudit(
                post_id=post_id,
                slug=slug,
                link=link,
                title=title,
                featured_media=featured_media,
                featured_alt=featured_alt,
                has_excerpt=has_excerpt,
                has_featured=has_featured,
                has_featured_alt=has_featured_alt,
                missing_excerpt=missing_excerpt,
                missing_featured=missing_featured,
                missing_featured_alt=missing_featured_alt,
            )
        )
    return audits


def summarize(audits: list[PostAudit]) -> dict[str, int]:
    return {
        "total": len(audits),
        "missing_excerpt": sum(1 for a in audits if a.missing_excerpt),
        "missing_featured": sum(1 for a in audits if a.missing_featured),
        "missing_featured_alt": sum(1 for a in audits if a.missing_featured_alt),
    }


def find_by_slug(audits: list[PostAudit], slug: str) -> PostAudit | None:
    for audit in audits:
        if audit.slug == slug:
            return audit
    return None


def post_content(wp: WordPressClient, post_id: int) -> str:
    payload = wp.get(
        f"/wp-json/wp/v2/posts/{post_id}",
        params={"context": "edit", "_fields": "content"},
    ).json()
    content = payload.get("content", {})
    if isinstance(content, dict):
        raw = str(content.get("raw", "")).strip()
        if raw:
            return raw
        return str(content.get("rendered", ""))
    return str(content)


def public_page_probe(url: str, timeout: int = 30) -> dict[str, Any]:
    split = urlsplit(url)
    query = dict(parse_qsl(split.query, keep_blank_values=True))
    query["cachebust"] = str(int(time.time()))
    probe_url = urlunsplit((split.scheme, split.netloc, split.path, urlencode(query), split.fragment))
    headers = {"User-Agent": "KKAuroraIAProbe/1.0 (+https://kriskrug.co)"}
    html_text = requests.get(probe_url, headers=headers, timeout=timeout).text
    body_start = html_text.find("<body")
    body_html = html_text[body_start:] if body_start != -1 else html_text

    featured_match = re.search(
        r'<figure[^>]*class="[^"]*wp-block-post-featured-image[^"]*"[^>]*>.*?<img[^>]*alt="([^"]*)"',
        body_html,
        flags=re.S,
    )
    featured_alt = featured_match.group(1).strip() if featured_match else ""

    og_alt_match = re.search(
        r'<meta[^>]+property="og:image:alt"[^>]+content="([^"]*)"',
        html_text,
        flags=re.I,
    )
    og_alt = og_alt_match.group(1).strip() if og_alt_match else ""

    h1_pos = body_html.find('<h1 class="aurora-single-title')
    dek_pos = body_html.find("aurora-article-dek")
    content_pos = body_html.find("aurora-prose")
    hierarchy_ok = h1_pos != -1 and dek_pos != -1 and content_pos != -1 and h1_pos < dek_pos < content_pos

    hardcoded_field_note = "Field note" in body_html
    schema_has_image = '"@type":"Article"' in html_text and '"image"' in html_text

    return {
        "featured_alt": featured_alt,
        "og_alt": og_alt,
        "hierarchy_ok": hierarchy_ok,
        "hardcoded_field_note": hardcoded_field_note,
        "schema_has_image": schema_has_image,
    }


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        out.append("| " + " | ".join(row) + " |")
    return "\n".join(out)


def write_report(
    report_path: Path,
    args: argparse.Namespace,
    before_summary: dict[str, int],
    after_summary: dict[str, int],
    audits_after: list[PostAudit],
    pilot_slug: str,
    pilot_probe: dict[str, Any] | None,
    media_updates: list[dict[str, Any]],
    excerpt_updates: list[dict[str, Any]],
    manual_featured: list[PostAudit],
    spot_checks: list[dict[str, Any]],
) -> None:
    generated = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")
    pilot = find_by_slug(audits_after, pilot_slug)

    before_after_table = markdown_table(
        ["Metric", "Before", "After"],
        [
            ["Published posts audited", str(before_summary["total"]), str(after_summary["total"])],
            ["Missing manual excerpt", str(before_summary["missing_excerpt"]), str(after_summary["missing_excerpt"])],
            ["Missing featured image", str(before_summary["missing_featured"]), str(after_summary["missing_featured"])],
            ["Missing featured-image alt", str(before_summary["missing_featured_alt"]), str(after_summary["missing_featured_alt"])],
        ],
    )

    pilot_rows = [["Status", "N/A"]]
    if pilot is not None:
        pilot_rows = [
            ["Post ID", str(pilot.post_id)],
            ["Slug", pilot.slug],
            ["Has excerpt", "yes" if pilot.has_excerpt else "no"],
            ["Featured media ID", str(pilot.featured_media or 0)],
            ["Featured alt non-empty", "yes" if pilot.has_featured_alt else "no"],
        ]
        if pilot_probe:
            pilot_rows.extend(
                [
                    ["Live featured img alt non-empty", "yes" if bool(pilot_probe["featured_alt"]) else "no"],
                    ["Live OG image alt non-empty", "yes" if bool(pilot_probe["og_alt"]) else "no"],
                    ["Live H1 -> dek -> content order", "yes" if pilot_probe["hierarchy_ok"] else "no"],
                    ["Live hardcoded Field note present", "yes" if pilot_probe["hardcoded_field_note"] else "no"],
                    ["Live Article schema includes image", "yes" if pilot_probe["schema_has_image"] else "no"],
                ]
            )

    pilot_table = markdown_table(["Pilot check", "Result"], pilot_rows)

    media_rows = [
        [
            str(item["post_id"]),
            item["slug"],
            str(item["media_id"]),
            item["reason"],
            item["new_alt"],
        ]
        for item in media_updates
    ]
    excerpt_rows = [
        [
            str(item["post_id"]),
            item["slug"],
            item["excerpt"][:120].replace("|", "\\|"),
        ]
        for item in excerpt_updates
    ]
    manual_rows = [[str(post.post_id), post.slug, post.link] for post in manual_featured]
    spot_rows = [
        [
            str(item["post_id"]),
            item["slug"],
            "yes" if item["featured_alt_non_empty"] else "no",
            "yes" if item["hierarchy_ok"] else "no",
            "yes" if item["field_note_absent"] else "no",
        ]
        for item in spot_checks
    ]

    sections: list[str] = [
        f"# Single-Post IA + Media Rollout Report ({dt.date.today().isoformat()})",
        "",
        f"- Generated: {generated}",
        f"- Cohort: published posts since `{args.since}`",
        f"- Mode: {'execute' if args.execute else 'dry-run'}",
        f"- Pilot slug: `{pilot_slug}`",
        f"- Pilot media ID: `{args.pilot_media_id}`",
        "",
        "## Before/After Counts",
        "",
        before_after_table,
        "",
        "## Pilot Status",
        "",
        pilot_table,
        "",
        "## Remediations Applied",
        "",
        f"- Featured-image alt updates: **{len(media_updates)}**",
        f"- Manual excerpt updates: **{len(excerpt_updates)}**",
        f"- Posts still needing manual featured image decision: **{len(manual_featured)}**",
        "",
    ]

    if media_rows:
        sections.extend(
            [
                "### Featured-image Alt Updates",
                "",
                markdown_table(["Post ID", "Slug", "Media ID", "Reason", "New alt text"], media_rows),
                "",
            ]
        )

    if excerpt_rows:
        sections.extend(
            [
                "### Excerpt Updates",
                "",
                markdown_table(["Post ID", "Slug", "Excerpt preview"], excerpt_rows),
                "",
            ]
        )

    if manual_rows:
        sections.extend(
            [
                "### Manual Featured-image Queue",
                "",
                markdown_table(["Post ID", "Slug", "URL"], manual_rows),
                "",
            ]
        )

    if spot_rows:
        sections.extend(
            [
                "## Spot-check (5 remediated posts)",
                "",
                markdown_table(
                    ["Post ID", "Slug", "Featured alt non-empty", "Hierarchy ok", "No hardcoded Field note"],
                    spot_rows,
                ),
                "",
            ]
        )

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(sections).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--since", default=DEFAULT_SINCE, help="Start date (YYYY-MM-DD).")
    parser.add_argument("--execute", action="store_true", help="Apply updates to live WordPress.")
    parser.add_argument("--report", default="", help="Write markdown report to this path.")
    parser.add_argument("--pilot-slug", default="make-culture-not-content")
    parser.add_argument("--pilot-media-id", type=int, default=11264)
    parser.add_argument(
        "--pilot-media-alt",
        default="Cover image for Make Culture, Not Content, highlighting Kris Krug's culture-first AI message.",
    )
    parser.add_argument("--text-only-slug", action="append", default=[], help="Slug allowed without featured image.")
    parser.add_argument("--text-only-slugs-file", default="", help="Path to newline-delimited text-only slugs.")
    parser.add_argument("--spot-check-count", type=int, default=5)
    return parser.parse_args()


def snapshot_targets(
    wp: WordPressClient,
    media_updates: list[dict[str, Any]],
    excerpt_updates: list[dict[str, Any]],
) -> Path:
    """Capture live current values of every write target before mutating, for rollback."""
    snap: dict[str, Any] = {"media": [], "posts": []}
    for item in media_updates:
        cur = wp.get(
            f"/wp-json/wp/v2/media/{item['media_id']}",
            {"context": "edit", "_fields": "id,alt_text"},
        ).json()
        snap["media"].append(
            {"media_id": item["media_id"], "alt_text": str(cur.get("alt_text", ""))}
        )
    for item in excerpt_updates:
        cur = wp.get(
            f"/wp-json/wp/v2/posts/{item['post_id']}",
            {"context": "edit", "_fields": "id,excerpt"},
        ).json()
        excerpt_obj = cur.get("excerpt", {})
        raw = excerpt_obj.get("raw", "") if isinstance(excerpt_obj, dict) else str(excerpt_obj)
        snap["posts"].append({"post_id": item["post_id"], "excerpt": raw})
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d-%H%M%SZ")
    path = REPO_ROOT / "backup" / f"{ts}-wp-post-ia-rollout" / "pre-write-snapshot.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(snap, indent=2, ensure_ascii=False))
    return path


def main() -> None:
    args = parse_args()
    config = load_config()
    wp = WordPressClient(config)
    text_only_slugs = load_text_only_slugs(args)

    posts = fetch_posts(wp, args.since)
    audits_before = audit_posts(wp, posts, text_only_slugs)
    before_summary = summarize(audits_before)

    media_updates: list[dict[str, Any]] = []
    excerpt_updates: list[dict[str, Any]] = []
    manual_featured = [a for a in audits_before if a.missing_featured]

    # Build the write plan from reads only; this runs in BOTH dry-run and execute
    # so dry-run can preview exactly what --execute would change.
    media_cache: dict[int, dict[str, Any]] = {}
    updated_media_ids: set[int] = set()

    pilot = find_by_slug(audits_before, args.pilot_slug)
    if pilot and pilot.featured_media == args.pilot_media_id:
        current = fetch_media(wp, pilot.featured_media, media_cache)
        current_alt = str(current.get("alt_text", "")).strip()
        if current_alt != args.pilot_media_alt:
            media_updates.append(
                {
                    "post_id": pilot.post_id,
                    "slug": pilot.slug,
                    "media_id": pilot.featured_media,
                    "reason": "pilot override",
                    "old_alt": current_alt,
                    "new_alt": args.pilot_media_alt,
                }
            )
            updated_media_ids.add(pilot.featured_media)

    for audit in audits_before:
        if audit.missing_featured_alt and audit.featured_media not in updated_media_ids:
            alt = default_alt_text(audit.title)
            media_updates.append(
                {
                    "post_id": audit.post_id,
                    "slug": audit.slug,
                    "media_id": audit.featured_media,
                    "reason": "cohort missing alt",
                    "old_alt": "",
                    "new_alt": alt,
                }
            )
            updated_media_ids.add(audit.featured_media)

        if audit.missing_excerpt:
            content_raw = post_content(wp, audit.post_id)
            excerpt = derive_excerpt(content_raw)
            if excerpt:
                excerpt_updates.append(
                    {
                        "post_id": audit.post_id,
                        "slug": audit.slug,
                        "excerpt": excerpt,
                    }
                )

    if args.execute:
        snapshot_path = snapshot_targets(wp, media_updates, excerpt_updates)
        print(f"pre-write snapshot={snapshot_path}")
        for item in media_updates:
            wp.post(
                f"/wp-json/wp/v2/media/{item['media_id']}", {"alt_text": item["new_alt"]}
            )
        for item in excerpt_updates:
            wp.post(
                f"/wp-json/wp/v2/posts/{item['post_id']}", {"excerpt": item["excerpt"]}
            )
    else:
        print(
            f"[dry-run] planned writes: media={len(media_updates)} "
            f"excerpt={len(excerpt_updates)} (no changes made; pass --execute to apply)"
        )
        for item in media_updates:
            print(
                f"  [plan] media {item['media_id']} ({item['slug']}) "
                f"alt: {item.get('old_alt', '')!r} -> {item['new_alt']!r}"
            )
        for item in excerpt_updates:
            print(
                f"  [plan] post {item['post_id']} ({item['slug']}) "
                f"excerpt -> {item['excerpt'][:60]!r}"
            )

    posts_after = fetch_posts(wp, args.since)
    audits_after = audit_posts(wp, posts_after, text_only_slugs)
    after_summary = summarize(audits_after)
    manual_featured_after = [a for a in audits_after if a.missing_featured]

    print(
        f"audited={before_summary['total']} "
        f"missing_excerpt(before={before_summary['missing_excerpt']} after={after_summary['missing_excerpt']}) "
        f"missing_featured(before={before_summary['missing_featured']} after={after_summary['missing_featured']}) "
        f"missing_featured_alt(before={before_summary['missing_featured_alt']} after={after_summary['missing_featured_alt']})"
    )
    print(f"media_updates={len(media_updates)} excerpt_updates={len(excerpt_updates)}")
    print(f"manual_featured_after={len(manual_featured_after)}")

    pilot_probe: dict[str, Any] | None = None
    pilot_after = find_by_slug(audits_after, args.pilot_slug)
    if pilot_after and pilot_after.link:
        pilot_probe = public_page_probe(pilot_after.link)
        print(
            "pilot_probe "
            f"featured_alt_non_empty={bool(pilot_probe['featured_alt'])} "
            f"og_alt_non_empty={bool(pilot_probe['og_alt'])} "
            f"hierarchy_ok={pilot_probe['hierarchy_ok']} "
            f"field_note_present={pilot_probe['hardcoded_field_note']} "
            f"schema_has_image={pilot_probe['schema_has_image']}"
        )

    spot_checks: list[dict[str, Any]] = []
    changed_ids = [item["post_id"] for item in media_updates + excerpt_updates]
    seen: set[int] = set()
    for post_id in changed_ids:
        if post_id in seen:
            continue
        seen.add(post_id)
        if len(spot_checks) >= args.spot_check_count:
            break
        post = next((a for a in audits_after if a.post_id == post_id), None)
        if not post or not post.link:
            continue
        probe = public_page_probe(post.link)
        spot_checks.append(
            {
                "post_id": post.post_id,
                "slug": post.slug,
                "featured_alt_non_empty": bool(probe["featured_alt"]),
                "hierarchy_ok": bool(probe["hierarchy_ok"]),
                "field_note_absent": not bool(probe["hardcoded_field_note"]),
            }
        )

    report_arg = args.report.strip()
    if not report_arg:
        report_name = f"SINGLE-POST-IA-MEDIA-ROLL-OUT-{dt.date.today().isoformat()}.md"
        report_path = REPO_ROOT / "docs" / "current-state" / report_name
    else:
        report_path = Path(report_arg)
        if not report_path.is_absolute():
            report_path = REPO_ROOT / report_path

    write_report(
        report_path=report_path,
        args=args,
        before_summary=before_summary,
        after_summary=after_summary,
        audits_after=audits_after,
        pilot_slug=args.pilot_slug,
        pilot_probe=pilot_probe,
        media_updates=media_updates,
        excerpt_updates=excerpt_updates,
        manual_featured=manual_featured_after,
        spot_checks=spot_checks,
    )
    print(f"report={report_path}")


if __name__ == "__main__":
    main()
