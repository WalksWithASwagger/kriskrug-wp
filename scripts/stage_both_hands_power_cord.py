#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
WP_HELPERS = REPO_ROOT / "scripts" / "notion-to-wp"

import sys

sys.path.insert(0, str(WP_HELPERS))
from wp_blocks import heading, inline, separator  # noqa: E402


DEFAULT_OUTPUT = REPO_ROOT / "content" / "drafts" / "2026-07-31-both-hands-on-the-power-cord"
SOURCE_OF_TRUTH = "kk-kb:content/sources/kriskrug-co/articles/both-hands-on-the-power-cord/article.md"
YOUTUBE_URL = "https://www.youtube.com/watch?v=n_aGBFGnPzo"
EXCERPT = (
    "I marched through Vancouver in a crowd chanting ‘Fuck AI.’ Then I went home and used AI "
    "to organize my notes. That contradiction is the work."
)
SEO_TITLE = "Canada's AI Energy Fight: Power, Protest and Sovereignty"
SEO_DESCRIPTION = (
    "Kris Krüg connects Canada's AI energy race, data-centre protests, Indigenous sovereignty, "
    "and a both-hands-full plan for building what comes next."
)


def split_frontmatter(text: str) -> tuple[dict, str]:
    match = re.match(r"\A---\n(.*?)\n---\n?(.*)\Z", text, flags=re.S)
    if not match:
        raise ValueError("source article has no YAML frontmatter")
    return yaml.safe_load(match.group(1)) or {}, match.group(2).strip()


def paragraph(text: str, *, class_name: str = "") -> str:
    class_attr = f' class="{class_name}"' if class_name else ""
    block_attr = f' {{"className":"{class_name}"}}' if class_name else ""
    return (
        f"<!-- wp:paragraph{block_attr} -->\n"
        f"<p{class_attr}>{inline(text)}</p>\n"
        "<!-- /wp:paragraph -->"
    )


def youtube_embed(url: str) -> str:
    return (
        '<!-- wp:embed {"url":"'
        + url
        + '","type":"video","providerNameSlug":"youtube","responsive":true,'
        '"className":"wp-embed-aspect-16-9 wp-has-aspect-ratio"} -->\n'
        '<figure class="wp-block-embed is-type-video is-provider-youtube wp-block-embed-youtube '
        'wp-embed-aspect-16-9 wp-has-aspect-ratio"><div class="wp-block-embed__wrapper">\n'
        + url
        + "\n</div></figure>\n<!-- /wp:embed -->"
    )


def ordered_list(items: list[str]) -> str:
    body = "\n".join(f"<li>{inline(item)}</li>" for item in items)
    return (
        '<!-- wp:list {"ordered":true} -->\n'
        f'<ol class="wp-block-list">\n{body}\n</ol>\n'
        "<!-- /wp:list -->"
    )


def render_gutenberg(body: str, subtitle: str) -> str:
    source_blocks = [block.strip() for block in re.split(r"\n\s*\n", body) if block.strip()]
    rendered: list[str] = []
    list_items: list[str] = []
    skipped_title = False

    def flush_list() -> None:
        nonlocal list_items
        if list_items:
            rendered.append(ordered_list(list_items))
            list_items = []

    for block in source_blocks:
        item = re.fullmatch(r"\d+\.\s+(.+)", block, flags=re.S)
        if item:
            list_items.append(item.group(1).replace("\n", " "))
            continue
        flush_list()

        if block.startswith("# ") and not skipped_title:
            skipped_title = True
            continue
        if block == f"## {subtitle}":
            rendered.append(paragraph(f"*{subtitle}*", class_name="both-hands-deck"))
            continue
        if block.startswith("## "):
            rendered.append(heading(inline(block[3:].strip()), level=2))
            continue
        if block.startswith("### "):
            rendered.append(heading(inline(block[4:].strip()), level=3))
            continue
        if block == "---":
            rendered.append(separator())
            continue
        if block == YOUTUBE_URL:
            rendered.append(youtube_embed(block))
            continue
        rendered.append(paragraph(block.replace("\n", " ")))

    flush_list()
    return "\n\n".join(rendered) + "\n"


def deployment_markdown(source: Path, source_meta: dict, body: str) -> str:
    frontmatter = {
        "title": source_meta["title"],
        "slug": "both-hands-on-the-power-cord",
        "status": "draft",
        "excerpt": EXCERPT,
        "source_of_truth": SOURCE_OF_TRUTH,
        "categories": ["Responsible AI & Policy", "AI Ethics & Philosophy"],
        "seo": {"meta_title": SEO_TITLE, "meta_description": SEO_DESCRIPTION},
    }
    return "---\n" + yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=True) + "---\n\n" + body + "\n"


def validate(post_md: str, post_html: str) -> None:
    checks = {
        "draft status": "status: draft" in post_md,
        "one video embed": post_html.count('providerNameSlug":"youtube"') == 1,
        "one ordered list": post_html.count('<!-- wp:list {"ordered":true} -->') == 1,
        "six policy items": post_html.count("<li>") == 6,
        "no local path in public HTML": "/Users/" not in post_html,
        "no em dash": "—" not in post_html,
        "Gutenberg blocks": post_html.count("<!-- wp:") >= 40,
    }
    failures = [name for name, passed in checks.items() if not passed]
    if failures:
        raise ValueError("staging validation failed: " + ", ".join(failures))


def main() -> int:
    parser = argparse.ArgumentParser(description="Stage the Both Hands article as a Gutenberg draft package")
    parser.add_argument("source", type=Path, help="canonical article.md from kk-kb")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--write", action="store_true", help="write post.md and post.html")
    args = parser.parse_args()

    source = args.source.resolve()
    source_meta, body = split_frontmatter(source.read_text(encoding="utf-8"))
    post_md = deployment_markdown(source, source_meta, body)
    post_html = render_gutenberg(body, str(source_meta["subtitle"]))
    validate(post_md, post_html)

    print(
        f"title={source_meta['title']!r} blocks={post_html.count('<!-- wp:')} "
        f"links={post_html.count('<a href=')} bytes={len(post_html)}"
    )
    if not args.write:
        print("[DRY RUN] no files written; pass --write to stage the package")
        return 0

    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "post.md").write_text(post_md, encoding="utf-8")
    (args.output / "post.html").write_text(post_html, encoding="utf-8")
    print(f"[STAGED] {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
