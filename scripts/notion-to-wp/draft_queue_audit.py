#!/usr/bin/env python3
"""Audit local draft packages and the live WordPress draft queue.

The script is read-only. It gathers enough evidence to decide which drafts are
ready for editorial rescue without treating "a WordPress draft exists" as a win.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from common import WPClient  # noqa: E402


STATUSES = ("future", "draft", "pending", "private")


@dataclass
class LocalDraft:
    path: str
    title: str
    slug: str
    status: str
    words: int
    markdown_links: int
    html_links: int
    markdown_images: int
    html_images: int
    image_files: int
    blocks: int
    todos: int
    files: list[str]


@dataclass
class WPDraft:
    kind: str
    wp_id: int
    status: str
    slug: str
    title: str
    date: str
    modified: str
    words: int
    links: int
    images: int
    blocks: int
    featured_media: int
    categories: list[int]
    tags: list[int]


@dataclass
class WPMatch:
    kind: str
    wp_id: int
    status: str
    title: str
    link: str


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    match = re.match(r"\A---\n(.*?)\n---\n?(.*)\Z", text, flags=re.S)
    if not match:
        return {}, text
    frontmatter_text = match.group(1)
    try:
        return yaml.safe_load(frontmatter_text) or {}, match.group(2)
    except yaml.YAMLError:
        parsed: dict[str, Any] = {}
        for line in frontmatter_text.splitlines():
            if line.startswith(("title:", "slug:", "status:")):
                key, value = line.split(":", 1)
                parsed[key.strip()] = value.strip().strip("\"'")
        return parsed, match.group(2)


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'’-]+\b", re.sub(r"<[^>]+>", " ", text)))


def local_draft_metrics(draft_dir: Path) -> LocalDraft:
    post_md = draft_dir / "post.md"
    post_html = draft_dir / "post.html"
    body = ""
    frontmatter: dict[str, Any] = {}
    if post_md.exists():
        frontmatter, body = split_frontmatter(post_md.read_text(encoding="utf-8", errors="replace"))
    html_body = post_html.read_text(encoding="utf-8", errors="replace") if post_html.exists() else ""
    images_dir = draft_dir / "images"
    image_files = len([path for path in images_dir.rglob("*") if path.is_file()]) if images_dir.exists() else 0
    expected_files = [
        "post.md",
        "post.html",
        "seo-meta.md",
        "alt-text.md",
        "internal-links.md",
        "publish-gate.md",
    ]
    scan = f"{body}\n{html_body}"
    return LocalDraft(
        path=str(draft_dir),
        title=str(frontmatter.get("title", "")).strip(),
        slug=str(frontmatter.get("slug", "")).strip(),
        status=str(frontmatter.get("status", "")).strip(),
        words=word_count(body),
        markdown_links=len(re.findall(r"\[[^\]]+\]\((?:https?://|/|\.\.?/)[^)]+\)", body)),
        html_links=len(re.findall(r"<a\b", html_body)),
        markdown_images=len(re.findall(r"!\[[^\]]*\]\([^)]+\)", body)),
        html_images=len(re.findall(r"<img\b", html_body)),
        image_files=image_files,
        blocks=len(re.findall(r"<!--\s*wp:", html_body)),
        todos=len(re.findall(r"\b(TODO|TK|FIXME|\?\?\?)\b", scan, flags=re.I)),
        files=[name for name in expected_files if (draft_dir / name).exists()],
    )


def collect_local_drafts(repo_root: Path) -> list[LocalDraft]:
    drafts_root = repo_root / "content" / "drafts"
    if not drafts_root.exists():
        return []
    return [local_draft_metrics(path) for path in sorted(drafts_root.iterdir()) if path.is_dir()]


def collect_wp_items(wp: WPClient, kind: str, status: str) -> list[dict[str, Any]]:
    return wp.get_all(kind, params={"status": status, "context": "edit"}, per_page=100)


def wp_draft_metrics(kind: str, post: dict[str, Any]) -> WPDraft:
    content = post.get("content") or {}
    raw = content.get("raw") or ""
    html_body = raw or content.get("rendered") or ""
    title = post.get("title") or {}
    return WPDraft(
        kind=kind[:-1],
        wp_id=int(post.get("id") or 0),
        status=str(post.get("status") or ""),
        slug=str(post.get("slug") or ""),
        title=str(title.get("raw") or title.get("rendered") or ""),
        date=str(post.get("date") or ""),
        modified=str(post.get("modified") or ""),
        words=word_count(html_body),
        links=len(re.findall(r"<a\b", html_body)),
        images=len(re.findall(r"<img\b", html_body)),
        blocks=len(re.findall(r"<!--\s*wp:", raw)),
        featured_media=int(post.get("featured_media") or 0),
        categories=[int(value) for value in post.get("categories") or []],
        tags=[int(value) for value in post.get("tags") or []],
    )


def collect_slug_matches(wp: WPClient, slugs: list[str]) -> dict[str, list[WPMatch]]:
    matches: dict[str, list[WPMatch]] = {slug: [] for slug in slugs}
    for slug in slugs:
        for kind in ("posts", "pages"):
            items = wp.get(
                kind,
                params={"slug": slug, "status": "any", "per_page": 100, "context": "edit"},
            )
            for item in items or []:
                title = item.get("title") or {}
                matches[slug].append(
                    WPMatch(
                        kind=kind[:-1],
                        wp_id=int(item.get("id") or 0),
                        status=str(item.get("status") or ""),
                        title=str(title.get("raw") or title.get("rendered") or ""),
                        link=str(item.get("link") or ""),
                    )
                )
    return matches


def collect_wp_audit(slugs: list[str] | None = None) -> tuple[list[dict[str, Any]], list[WPDraft], dict[str, list[WPMatch]]]:
    wp = WPClient.from_env(timeout=30)
    summary: list[dict[str, Any]] = []
    drafts: list[WPDraft] = []
    for kind in ("posts", "pages"):
        for status in STATUSES:
            items = collect_wp_items(wp, kind, status)
            summary.append({"kind": kind, "status": status, "count": len(items)})
            if status == "draft":
                drafts.extend(wp_draft_metrics(kind, item) for item in items)
    slug_matches = collect_slug_matches(wp, slugs or [])
    return summary, sorted(drafts, key=lambda item: (item.kind, item.date), reverse=True), slug_matches


def match_state(local: LocalDraft, slug_matches: dict[str, list[WPMatch]]) -> str:
    if not local.slug:
        return "no local slug"
    matches = slug_matches.get(local.slug, [])
    if matches:
        labels = ", ".join(f"{match.kind} {match.wp_id} ({match.status})" for match in matches)
        return labels
    return "no WP slug match"


def quality_state(local: LocalDraft, match: str) -> str:
    if "(publish)" in match:
        return "published; do not duplicate"
    if local.words == 0 and not local.files:
        return "empty local artifact"
    image_count = max(local.markdown_images, local.html_images, local.image_files)
    if "post " in match and local.blocks >= 50 and image_count >= 1:
        return "reviewable draft"
    if local.words >= 2500 and image_count >= 1:
        return "strong local candidate"
    if local.words >= 1200:
        return "needs media/taxonomy pass"
    if local.words > 0:
        return "thin source draft"
    return "admin gate only"


def render_markdown(
    local_drafts: list[LocalDraft],
    wp_summary: list[dict[str, Any]],
    wp_drafts: list[WPDraft],
    slug_matches: dict[str, list[WPMatch]] | None = None,
) -> str:
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines = [
        f"# Draft Queue Audit Snapshot - {generated}",
        "",
        "This is a read-only inventory. It does not create, update, schedule, or publish WordPress content.",
        "",
        "## WordPress Queue Counts",
        "",
    ]
    if wp_summary:
        lines.extend(["| Surface | Future | Draft | Pending | Private |", "|---|---:|---:|---:|---:|"])
        for kind in ("posts", "pages"):
            counts = {row["status"]: row["count"] for row in wp_summary if row["kind"] == kind}
            lines.append(
                f"| {kind.title()} | {counts.get('future', 0)} | {counts.get('draft', 0)} | "
                f"{counts.get('pending', 0)} | {counts.get('private', 0)} |"
            )
    else:
        lines.append("WordPress REST checks skipped.")
    lines.extend(
        [
            "",
            "## Local Draft Packages",
            "",
            "| Local package | WP match | Quality state | Words | Links | Images | Blocks | TODOs | Files |",
            "|---|---|---|---:|---:|---:|---:|---:|---|",
        ]
    )
    for local in local_drafts:
        match = match_state(local, slug_matches or {})
        images = max(local.markdown_images, local.html_images, local.image_files)
        links = max(local.markdown_links, local.html_links)
        files = ", ".join(local.files) if local.files else "-"
        label = local.slug or Path(local.path).name
        lines.append(
            f"| `{label}` | {match} | {quality_state(local, match)} | {local.words} | {links} | "
            f"{images} | {local.blocks} | {local.todos} | {files} |"
        )
    lines.extend(
        [
            "",
            "## WordPress Drafts",
            "",
            "| Kind | WP ID | Slug/title | Words | Links | Images | Blocks | Featured | Notes |",
            "|---|---:|---|---:|---:|---:|---:|---:|---|",
        ]
    )
    for draft in wp_drafts:
        label = draft.slug or draft.title or "(untitled)"
        notes = []
        if not draft.slug:
            notes.append("empty REST slug")
        if not draft.featured_media:
            notes.append("no featured image")
        if draft.blocks == 0:
            notes.append("no block comments")
        if draft.kind == "post" and draft.categories == [1]:
            notes.append("Misc category")
        lines.append(
            f"| {draft.kind} | {draft.wp_id} | `{label}` | {draft.words} | {draft.links} | "
            f"{draft.images} | {draft.blocks} | {draft.featured_media} | {', '.join(notes) or 'review needed'} |"
        )
    lines.extend(
        [
            "",
            "## Required Promotion Gate",
            "",
            "- Editorial voice pass: strong KK opening, no recap filler, clear first-screen argument.",
            "- Formatting pass: block-clean WordPress body, no markdown artifacts, skimmable headings.",
            "- Link pass: intentional internal links, checked external links, no local/private URLs.",
            "- Image/media pass: featured image or explicit text-only decision, alt text, source/credit note.",
            "- Taxonomy/meta pass: deliberate title, slug, excerpt, category, tags, and no accidental `Misc`.",
            "- Preview pass: wp-admin preview on desktop and mobile before any schedule decision.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--local-only", action="store_true", help="Skip WordPress REST checks.")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    local_drafts = collect_local_drafts(repo_root)
    wp_summary: list[dict[str, Any]] = []
    wp_drafts: list[WPDraft] = []
    slug_matches: dict[str, list[WPMatch]] = {}
    if not args.local_only:
        slugs = [local.slug for local in local_drafts if local.slug]
        wp_summary, wp_drafts, slug_matches = collect_wp_audit(slugs)

    if args.format == "json":
        print(
            json.dumps(
                {
                    "local_drafts": [asdict(item) for item in local_drafts],
                    "wp_summary": wp_summary,
                    "wp_drafts": [asdict(item) for item in wp_drafts],
                    "slug_matches": {
                        slug: [asdict(item) for item in matches] for slug, matches in slug_matches.items()
                    },
                },
                indent=2,
            )
        )
        return 0
    print(render_markdown(local_drafts, wp_summary, wp_drafts, slug_matches))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
