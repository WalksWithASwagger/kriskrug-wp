"""Pure helpers for SEO inventory (no WordPress imports)."""

from __future__ import annotations

import html
import re
from dataclasses import asdict, dataclass
from typing import Any

SEO_TITLE_KEYS = ("jetpack_seo_html_title",)
META_DESC_KEYS = ("advanced_seo_description",)
SOCIAL_KEYS = ("jetpack_publicize_message",)
SEO_META_KEYS = SEO_TITLE_KEYS + META_DESC_KEYS + SOCIAL_KEYS


@dataclass
class SEORecord:
    kind: str
    wp_id: int
    slug: str
    title: str
    link: str
    has_seo_title: bool
    seo_title_length: int
    has_meta_description: bool
    meta_description_length: int
    has_social_message: bool
    social_message_length: int


def meta_value(meta: dict[str, Any], keys: tuple[str, ...]) -> str:
    for key in keys:
        value = meta.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def meta_keys_registered(items: list[dict[str, Any]]) -> bool:
    """True when REST still exposes the Jetpack SEO meta keys.

    Jetpack is what registers these keys with `show_in_rest`. Once it is
    deactivated the keys drop out of the payload entirely, so every item looks
    like it is missing its SEO title when the values are in fact still in
    wp_postmeta and still rendering (theme/kk-aurora/inc/seo-title.php reads
    them with get_post_meta). An absent key and an empty key are the same shape
    through meta.get(), so the only way to tell a tooling failure from a content
    gap is to look for the key itself.
    """
    return any(
        key in (item.get("meta") or {}) for item in items for key in SEO_META_KEYS
    )


_TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)
_DESC_TAG_RE = re.compile(r"<meta[^>]+name=[\"']description[\"'][^>]*>", re.I)
_CONTENT_RE = re.compile(r"content=[\"'](.*?)[\"']", re.I | re.S)


def extract_rendered_seo(page_html: str) -> tuple[str, str]:
    """Pull the <title> and meta description a crawler would actually see."""
    title_match = _TITLE_RE.search(page_html)
    title = html.unescape(title_match.group(1)).strip() if title_match else ""

    description = ""
    desc_tag = _DESC_TAG_RE.search(page_html)
    if desc_tag:
        content = _CONTENT_RE.search(desc_tag.group(0))
        if content:
            description = html.unescape(content.group(1)).strip()

    return title, description


def record_from_rendered(kind: str, item: dict[str, Any], page_html: str) -> SEORecord:
    """Build a record from delivered HTML instead of REST meta.

    Social message has no rendered equivalent (Publicize never reaches the
    page), so it is reported as absent and excluded from the summary.
    """
    seo_title, meta_desc = extract_rendered_seo(page_html)
    return SEORecord(
        kind=kind,
        wp_id=int(item["id"]),
        slug=str(item.get("slug") or ""),
        title=str(item.get("title", {}).get("rendered") or item.get("title") or ""),
        link=str(item.get("link") or ""),
        has_seo_title=bool(seo_title),
        seo_title_length=len(seo_title),
        has_meta_description=bool(meta_desc),
        meta_description_length=len(meta_desc),
        has_social_message=False,
        social_message_length=0,
    )


def record_from_item(kind: str, item: dict[str, Any]) -> SEORecord:
    meta = item.get("meta") or {}
    seo_title = meta_value(meta, SEO_TITLE_KEYS)
    meta_desc = meta_value(meta, META_DESC_KEYS)
    social = meta_value(meta, SOCIAL_KEYS)
    return SEORecord(
        kind=kind,
        wp_id=int(item["id"]),
        slug=str(item.get("slug") or ""),
        title=str(item.get("title", {}).get("rendered") or item.get("title") or ""),
        link=str(item.get("link") or ""),
        has_seo_title=bool(seo_title),
        seo_title_length=len(seo_title),
        has_meta_description=bool(meta_desc),
        meta_description_length=len(meta_desc),
        has_social_message=bool(social),
        social_message_length=len(social),
    )


def summarize(records: list[SEORecord]) -> dict[str, Any]:
    return {
        "total": len(records),
        "posts": sum(1 for r in records if r.kind == "post"),
        "pages": sum(1 for r in records if r.kind == "page"),
        "missing_seo_title": sum(1 for r in records if not r.has_seo_title),
        "missing_meta_description": sum(
            1 for r in records if not r.has_meta_description
        ),
        "missing_social_message": sum(
            1 for r in records if r.kind == "post" and not r.has_social_message
        ),
    }


def render_markdown(records: list[SEORecord], source: str = "meta") -> str:
    stats = summarize(records)
    heading = (
        "# Rendered SEO Metadata Inventory"
        if source == "rendered"
        else "# Jetpack SEO Metadata Inventory"
    )
    provenance = (
        'Read from delivered HTML (`<title>` and `<meta name="description">`), '
        "which is the surface a crawler sees."
        if source == "rendered"
        else "Read from REST post meta."
    )
    lines = [
        heading,
        "",
        f"Read-only snapshot. `transcript` CPT excluded (not deployed). {provenance}",
        "",
        "## Summary",
        "",
        f"- Total: {stats['total']} ({stats['posts']} posts, {stats['pages']} pages)",
        f"- Missing SEO title: {stats['missing_seo_title']}",
        f"- Missing meta description: {stats['missing_meta_description']}",
    ]
    if source == "rendered":
        lines.append(
            "- Posts missing social message: not measurable from rendered HTML"
        )
    else:
        lines.append(
            f"- Posts missing social message: {stats['missing_social_message']}"
        )
    lines.append("")
    return "\n".join(lines)


def write_csv(path, records: list[SEORecord]) -> None:  # noqa: ANN001
    import csv
    from pathlib import Path

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(asdict(records[0]).keys()) if records else []
        )
        if records:
            writer.writeheader()
            for record in records:
                writer.writerow(asdict(record))
