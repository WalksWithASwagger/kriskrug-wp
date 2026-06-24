from __future__ import annotations

import unicodedata

from content_derivation import derive_social_message


def normalize_seo_meta(text: str) -> str:
    """Make a value safe for Jetpack's SEO post-meta REST fields.

    Jetpack's ``jetpack_seo_html_title`` / ``advanced_seo_description`` REST
    writes return HTTP 500 when the value carries combining diacritics
    (Unicode category Mn) that NFC cannot precompose — e.g. "Ethọ́s"
    (o + combining dot-below + combining acute). Precompose with NFC, then drop
    any leftover combining marks. Precomposed accents (ü, é, ñ) are single
    NFC codepoints and survive untouched; the visible post title, excerpt, and
    body are never routed through this.
    """
    nfc = unicodedata.normalize("NFC", text)
    return "".join(ch for ch in nfc if not unicodedata.combining(ch))


def build_wp_payload(
    *,
    title: str,
    slug: str,
    force_publish: bool,
    pub_datetime: str,
    author_id: int,
    excerpt: str,
    body_html: str,
    page_id: str,
    featured: bool,
    seo_title: str,
    meta_desc: str,
) -> dict:
    return {
        "title": title,
        "slug": slug,
        "status": "publish" if force_publish else "draft",
        "date": pub_datetime,
        "author": author_id,
        "excerpt": excerpt,
        "content": body_html,
        "meta": {
            "kk_notion_source_id": page_id,
            "kk_featured": "1" if featured else "0",
            "jetpack_seo_html_title": normalize_seo_meta(seo_title),
            "advanced_seo_description": normalize_seo_meta(meta_desc),
            "jetpack_publicize_message": derive_social_message(excerpt, max_chars=240),
        },
    }
