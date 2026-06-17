from __future__ import annotations

import difflib
import json
import re


TITLE_SIMILARITY_UPDATE_THRESHOLD = 0.5


def title_similarity(a: str, b: str) -> float:
    """Detect wild title mismatches before updating an existing slug target."""
    a = (a or "").strip().lower()
    b = (b or "").strip().lower()
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a, b).ratio()


def update_title_guard(new_title: str, existing_title: str) -> tuple[bool, float]:
    sim = title_similarity(new_title, existing_title)
    return sim >= TITLE_SIMILARITY_UPDATE_THRESHOLD, sim


def _wp_text_field(value) -> str:
    if isinstance(value, dict):
        raw = value.get("raw")
        if raw:
            return raw
        rendered = value.get("rendered") or ""
        return re.sub(r"<[^>]+>", "", rendered).strip()
    return value or ""


def update_diff(existing_post: dict, proposed_payload: dict) -> str:
    existing = {
        "title": _wp_text_field(existing_post.get("title")),
        "slug": existing_post.get("slug") or "",
        "status": existing_post.get("status") or "",
        "date": existing_post.get("date") or "",
        "excerpt": _wp_text_field(existing_post.get("excerpt")),
        "content": _wp_text_field(existing_post.get("content")),
        "meta": existing_post.get("meta") or {},
    }
    proposed = {
        "title": proposed_payload.get("title") or "",
        "slug": proposed_payload.get("slug") or "",
        "status": proposed_payload.get("status") or "",
        "date": proposed_payload.get("date") or "",
        "excerpt": proposed_payload.get("excerpt") or "",
        "content": proposed_payload.get("content") or "",
        "meta": proposed_payload.get("meta") or {},
    }
    before = json.dumps(existing, indent=2, ensure_ascii=False, sort_keys=True).splitlines(keepends=True)
    after = json.dumps(proposed, indent=2, ensure_ascii=False, sort_keys=True).splitlines(keepends=True)
    return "".join(difflib.unified_diff(
        before,
        after,
        fromfile="existing-wp-post",
        tofile="proposed-notion-payload",
    ))


def emit_update_diff_review(wp, slug: str, title: str, payload: dict, log, emit=print) -> int:
    existing_id = wp.find_post_by_slug(slug)
    log(f"existing post with slug {slug!r}? {existing_id}")
    if existing_id is None:
        log("ABORTING: --diff needs an existing post with this slug; no WP write was attempted.")
        return 6

    existing = wp.get_post(existing_id)
    existing_title = (existing.get("title") or {}).get("raw", "")
    title_match, sim = update_title_guard(title, existing_title)
    log(f"  existing post title: {existing_title!r}")
    log(f"  new post title:      {title!r}")
    log(f"  title similarity:    {sim:.2f}")
    if not title_match:
        log(f"ABORTING: existing title is too different from new title "
            f"(similarity {sim:.2f} < {TITLE_SIMILARITY_UPDATE_THRESHOLD}).")
        log("No diff was emitted and no WP write was attempted.")
        return 3

    diff_text = update_diff(existing, payload)
    if diff_text:
        emit(diff_text)
    else:
        emit("No update diff: selected existing WP fields match the proposed payload.")
    log("Diff-only run complete; no WP create, update, taxonomy, or media write request was sent.")
    log("Review the diff, then re-run with --update only after explicit operator approval.")
    return 0
