#!/usr/bin/env python3
"""Prepare a local markdown draft for WordPress review.

This is intentionally narrow: it takes a `content/drafts/.../post.md` file,
generates Gutenberg-friendly `post.html`, runs a small quality gate, and can
optionally update an existing WordPress draft after verifying the target.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import yaml

from kk_notion_to_wp import WordPress, load_config, update_title_guard


MIN_WORDS = 900
MIN_LINKS = 4
BANNED_BODY_PATTERNS = [
    "/Users/",
    "content/source-packs/",
    "Source note:",
    "this draft is based on",
    "wp-admin/",
]
BANNED_WEAK_PHRASES = [
    "in today's fast-paced",
    "delve into",
    "navigate the landscape",
    "unlock the potential",
    "game-changer",
]


@dataclass
class DraftPackage:
    path: Path
    frontmatter: dict
    body: str

    @property
    def draft_dir(self) -> Path:
        return self.path.parent

    @property
    def title(self) -> str:
        return str(self.frontmatter.get("title", "")).strip()

    @property
    def slug(self) -> str:
        return str(self.frontmatter.get("slug", "")).strip()

    @property
    def excerpt(self) -> str:
        return str(self.frontmatter.get("excerpt", "")).strip()


def split_frontmatter(text: str) -> tuple[dict, str]:
    match = re.match(r"\A---\n(.*?)\n---\n?(.*)\Z", text, flags=re.S)
    if not match:
        return {}, text
    return yaml.safe_load(match.group(1)) or {}, match.group(2).strip()


def load_draft(path: Path) -> DraftPackage:
    frontmatter, body = split_frontmatter(path.read_text(encoding="utf-8"))
    return DraftPackage(path=path, frontmatter=frontmatter, body=body.strip())


def inline_markdown(value: str) -> str:
    escaped = html.escape(value, quote=False)
    escaped = re.sub(
        r"\[([^\]]+)\]\((https?://[^)]+|/[^)]+|\.\.?/[^)]+)\)",
        lambda m: f'<a href="{html.escape(m.group(2), quote=True)}">{m.group(1)}</a>',
        escaped,
    )
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)
    return escaped


def paragraph_block(lines: list[str]) -> str:
    text = " ".join(line.strip() for line in lines).strip()
    return (
        "<!-- wp:paragraph -->\n"
        f"<p>{inline_markdown(text)}</p>\n"
        "<!-- /wp:paragraph -->"
    )


def heading_block(line: str) -> str:
    level = len(line) - len(line.lstrip("#"))
    level = max(2, min(level, 4))
    text = line[level:].strip()
    attrs = "" if level == 2 else f' {{"level":{level}}}'
    return (
        f"<!-- wp:heading{attrs} -->\n"
        f'<h{level} class="wp-block-heading">{inline_markdown(text)}</h{level}>\n'
        "<!-- /wp:heading -->"
    )


def list_block(items: list[str], ordered: bool = False) -> str:
    tag = "ol" if ordered else "ul"
    attrs = ' {"ordered":true}' if ordered else ""
    rendered = [f"<!-- wp:list{attrs} -->", f'<{tag} class="wp-block-list">']
    for item in items:
        rendered.extend(
            [
                "<!-- wp:list-item -->",
                f"<li>{inline_markdown(item)}</li>",
                "<!-- /wp:list-item -->",
            ]
        )
    rendered.extend([f"</{tag}>", "<!-- /wp:list -->"])
    return "\n".join(rendered)


def quote_block(lines: list[str]) -> str:
    text = " ".join(line.lstrip("> ").strip() for line in lines).strip()
    return (
        "<!-- wp:quote -->\n"
        '<blockquote class="wp-block-quote">'
        f"<!-- wp:paragraph -->\n<p>{inline_markdown(text)}</p>\n<!-- /wp:paragraph -->"
        "</blockquote>\n"
        "<!-- /wp:quote -->"
    )


def image_block(src: str, alt: str = "") -> str:
    return (
        "<!-- wp:image -->\n"
        "<figure class=\"wp-block-image\">"
        f'<img src="{html.escape(src, quote=True)}" alt="{html.escape(alt, quote=True)}"/>'
        "</figure>\n"
        "<!-- /wp:image -->"
    )


def nextpage_block() -> str:
    return "<!-- wp:nextpage -->\n<!--nextpage-->\n<!-- /wp:nextpage -->"


def markdown_to_blocks(markdown: str) -> str:
    blocks: list[str] = []
    paragraph: list[str] = []
    list_items: list[str] = []
    ordered_items: list[str] = []
    quote_lines: list[str] = []

    def flush_paragraph():
        if paragraph:
            blocks.append(paragraph_block(paragraph))
            paragraph.clear()

    def flush_lists():
        if list_items:
            blocks.append(list_block(list_items))
            list_items.clear()
        if ordered_items:
            blocks.append(list_block(ordered_items, ordered=True))
            ordered_items.clear()

    def flush_quote():
        if quote_lines:
            blocks.append(quote_block(quote_lines))
            quote_lines.clear()

    for raw_line in markdown.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            flush_paragraph()
            flush_lists()
            flush_quote()
            continue
        if line.strip() == "<!--nextpage-->":
            flush_paragraph()
            flush_lists()
            flush_quote()
            blocks.append(nextpage_block())
            continue
        image_match = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", line.strip())
        if image_match:
            flush_paragraph()
            flush_lists()
            flush_quote()
            blocks.append(image_block(image_match.group(2), image_match.group(1)))
            continue
        if line.startswith("#"):
            flush_paragraph()
            flush_lists()
            flush_quote()
            blocks.append(heading_block(line))
            continue
        unordered = re.match(r"^\s*[-*]\s+(.+)$", line)
        if unordered:
            flush_paragraph()
            flush_quote()
            list_items.append(unordered.group(1).strip())
            continue
        ordered = re.match(r"^\s*\d+[.)]\s+(.+)$", line)
        if ordered:
            flush_paragraph()
            flush_quote()
            ordered_items.append(ordered.group(1).strip())
            continue
        if line.startswith(">"):
            flush_paragraph()
            flush_lists()
            quote_lines.append(line)
            continue
        flush_lists()
        flush_quote()
        paragraph.append(line)

    flush_paragraph()
    flush_lists()
    flush_quote()
    return "\n\n".join(blocks).strip() + "\n"


def count_words(markdown: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", re.sub(r"`[^`]+`", " ", markdown)))


def count_links(markdown: str) -> int:
    return len(re.findall(r"\[[^\]]+\]\((https?://[^)]+|/[^)]+|\.\.?/[^)]+)\)", markdown))


def count_images(markdown: str) -> int:
    return len(re.findall(r"!\[[^\]]*\]\([^)]+\)", markdown))


def quality_issues(pkg: DraftPackage, html_body: str) -> list[str]:
    issues: list[str] = []
    body = pkg.body
    frontmatter_text = yaml.safe_dump(pkg.frontmatter, sort_keys=False)
    if not pkg.title:
        issues.append("missing frontmatter title")
    if not pkg.slug:
        issues.append("missing frontmatter slug")
    if count_words(body) < MIN_WORDS:
        issues.append(f"body is under {MIN_WORDS} words")
    if count_links(body) < MIN_LINKS:
        issues.append(f"body has fewer than {MIN_LINKS} markdown links")
    if count_images(body) == 0 and not pkg.frontmatter.get("featured_media_id"):
        issues.append("no markdown image and no featured_media_id")
    if re.search(r"\]\(\.\.?/", body):
        issues.append("public body contains a draft-local relative link")
    if "/Users/" in frontmatter_text:
        issues.append("frontmatter contains an absolute local path")
    for pattern in BANNED_BODY_PATTERNS:
        if pattern in body:
            issues.append(f"public body contains private/source marker: {pattern}")
    lower_body = body.lower()
    for phrase in BANNED_WEAK_PHRASES:
        if phrase in lower_body:
            issues.append(f"weak AI-copy phrase present: {phrase}")
    if "<!-- wp:" not in html_body:
        issues.append("generated HTML has no WordPress blocks")
    return issues


def ensure_terms(wp: WordPress, taxonomy: str, values: Iterable[str]) -> list[int]:
    ids: list[int] = []
    for value in values:
        if value:
            ids.append(wp.ensure_term(taxonomy, value))
    return ids


def update_wp_draft(pkg: DraftPackage, html_body: str, wp_id: int) -> dict:
    cfg = load_config()
    wp = WordPress(cfg.wp_base_url, cfg.wp_user, cfg.wp_app_password)
    existing = wp.get_post(wp_id)
    existing_slug = existing.get("slug", "")
    existing_status = existing.get("status", "")
    existing_title = (existing.get("title") or {}).get("raw", "")
    if existing_slug != pkg.slug:
        raise RuntimeError(f"slug mismatch: WP has {existing_slug!r}, local has {pkg.slug!r}")
    if existing_status != "draft":
        raise RuntimeError(f"refusing to update non-draft post {wp_id}: status {existing_status!r}")
    title_match, similarity = update_title_guard(pkg.title, existing_title)
    if not title_match:
        raise RuntimeError(
            f"title mismatch: WP={existing_title!r}, local={pkg.title!r}, similarity={similarity:.2f}"
        )

    payload: dict = {
        "title": pkg.title,
        "slug": pkg.slug,
        "status": "draft",
        "excerpt": pkg.excerpt,
        "content": html_body,
    }
    categories = pkg.frontmatter.get("categories") or []
    tags = pkg.frontmatter.get("tags") or []
    if categories:
        payload["categories"] = ensure_terms(wp, "categories", categories)
    if tags:
        payload["tags"] = ensure_terms(wp, "tags", tags)
    if pkg.frontmatter.get("featured_media_id"):
        payload["featured_media"] = int(pkg.frontmatter["featured_media_id"])
    seo = pkg.frontmatter.get("seo") or {}
    if seo:
        payload["meta"] = {
            "jetpack_seo_html_title": str(seo.get("meta_title", "")),
            "advanced_seo_description": str(seo.get("meta_description", "")),
        }

    result = wp.update_post(wp_id, payload)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("post_md", type=Path)
    parser.add_argument("--wp-id", type=int, default=None)
    parser.add_argument("--no-write", action="store_true", help="Validate only; do not write post.html")
    parser.add_argument("--fail-on-warning", action="store_true")
    args = parser.parse_args()

    pkg = load_draft(args.post_md)
    html_body = markdown_to_blocks(pkg.body)
    issues = quality_issues(pkg, html_body)
    if not args.no_write:
        (pkg.draft_dir / "post.html").write_text(html_body, encoding="utf-8")
    if issues:
        for issue in issues:
            print(f"WARN: {issue}")
        if args.fail_on_warning:
            return 3
    print(
        f"OK: {pkg.slug} words={count_words(pkg.body)} links={count_links(pkg.body)} "
        f"images={count_images(pkg.body)} blocks={html_body.count('<!-- wp:')}"
    )
    if args.wp_id is not None:
        result = update_wp_draft(pkg, html_body, args.wp_id)
        print(f"UPDATED: WP draft {result['id']} {result.get('link')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
