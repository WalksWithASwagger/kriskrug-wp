from __future__ import annotations

from content_derivation import derive_social_message


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
            "jetpack_seo_html_title": seo_title,
            "advanced_seo_description": meta_desc,
            "jetpack_publicize_message": derive_social_message(excerpt, max_chars=240),
        },
    }
