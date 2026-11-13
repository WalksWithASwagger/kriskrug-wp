from __future__ import annotations

from typing import Callable

from content_derivation import derive_social_message
from cp1252_text import derived_meta_text, plain_meta_text


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
    warn: Callable[[str], None] = print,
) -> dict:
    # run() folds the seo_title and meta_desc it derives before it writes the
    # draft package, so a value that still needs folding here was not derived
    # and is refused. The Publicize message is derived here, so it folds here.
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
            "jetpack_seo_html_title": plain_meta_text(seo_title, "SEO title"),
            "advanced_seo_description": plain_meta_text(meta_desc, "SEO description"),
            "jetpack_publicize_message": derived_meta_text(
                derive_social_message(excerpt, max_chars=240), "jetpack_publicize_message", warn
            ),
        },
    }
