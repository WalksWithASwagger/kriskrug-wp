"""Pure helpers for SEO inventory (no WordPress imports)."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

SEO_TITLE_KEYS = ("jetpack_seo_html_title",)
META_DESC_KEYS = ("advanced_seo_description",)
SOCIAL_KEYS = ("jetpack_publicize_message",)


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
        "missing_meta_description": sum(1 for r in records if not r.has_meta_description),
        "missing_social_message": sum(1 for r in records if r.kind == "post" and not r.has_social_message),
    }


def render_markdown(records: list[SEORecord]) -> str:
    stats = summarize(records)
    lines = [
        "# Jetpack SEO Metadata Inventory",
        "",
        "Read-only snapshot. `transcript` CPT excluded (not deployed).",
        "",
        "## Summary",
        "",
        f"- Total: {stats['total']} ({stats['posts']} posts, {stats['pages']} pages)",
        f"- Missing SEO title: {stats['missing_seo_title']}",
        f"- Missing meta description: {stats['missing_meta_description']}",
        f"- Posts missing social message: {stats['missing_social_message']}",
        "",
    ]
    return "\n".join(lines)


def write_csv(path, records: list[SEORecord]) -> None:  # noqa: ANN001
    import csv
    from pathlib import Path

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(records[0]).keys()) if records else [])
        if records:
            writer.writeheader()
            for record in records:
                writer.writerow(asdict(record))
