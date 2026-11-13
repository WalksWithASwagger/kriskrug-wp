from __future__ import annotations

import difflib
import html
import json
import re
from datetime import datetime, timezone

from wp_client import SlugVerificationFailed


TITLE_SIMILARITY_UPDATE_THRESHOLD = 0.5


def title_similarity(a: str, b: str) -> float:
    """Detect wild title mismatches before updating an existing slug target.

    Stored titles can hold character references for text the database cannot
    store raw, so both sides are compared unescaped.
    """
    a = html.unescape(a or "").strip().lower()
    b = html.unescape(b or "").strip().lower()
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a, b).ratio()


def update_title_guard(new_title: str, existing_title: str) -> tuple[bool, float]:
    sim = title_similarity(new_title, existing_title)
    return sim >= TITLE_SIMILARITY_UPDATE_THRESHOLD, sim


def update_payload(payload: dict, *, force_publish: bool, send_date: bool) -> dict:
    """The body an update sends, as a new dict.

    Without --publish it carries no status and without --date no date, so
    WordPress keeps the post's own. The connector used to send "draft" and the
    Notion date here. The first unpublished live posts. The second let
    wp_insert_post publish a scheduled post once the sent date had passed.
    """
    dropped = set()
    if not force_publish:
        dropped.add("status")
    if not send_date:
        dropped.add("date")
    return {key: value for key, value in payload.items() if key not in dropped}


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
        "status": proposed_payload.get("status", existing["status"]),
        "date": proposed_payload.get("date", existing["date"]),
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
    try:
        existing_id = wp.find_post_by_slug(slug)
    except SlugVerificationFailed as e:
        log(f"ABORTING: {e}")
        log("No diff was emitted and no WP write was attempted.")
        return 8
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


# WordPress turns a publish request whose date is in the future into a scheduled post.
_READBACK_STATUS_ALIASES = {"publish": {"publish", "future"}}


def _same_post_date(sent: str, readback: dict) -> bool:
    sent_dt = datetime.fromisoformat(sent)
    if sent_dt.tzinfo is None:
        stored = readback.get("date")
    else:
        # WordPress converts an offset date to site time, so compare in UTC.
        stored = readback.get("date_gmt")
        sent_dt = sent_dt.astimezone(timezone.utc).replace(tzinfo=None)
    return bool(stored) and datetime.fromisoformat(stored) == sent_dt


def _comparable_title(title: str) -> str:
    # The raw title can hold the same text as character references (kses turns
    # & into &amp;, and the cp1252 database keeps other characters only as
    # numeric references), and WordPress trims titles on save (title_save_pre).
    return html.unescape(title).strip()


def readback_mismatches(
    payload: dict, readback: dict, *, before: dict | None = None
) -> dict[str, tuple]:
    """Return {field: (sent, stored)} for identity fields WordPress did not store as sent.

    `before` is the post as an update found it. An update that sends no status
    must find that status exactly. A sent publish may read back as future only
    when the post was not already live, because scheduling a live post takes it
    down until the date.
    """
    mismatches: dict[str, tuple] = {}
    # Only title.raw (context=edit) is the stored value; title.rendered is texturized.
    sent_title = payload.get("title") or ""
    stored_title = (readback.get("title") or {}).get("raw")
    if stored_title is None or _comparable_title(stored_title) != _comparable_title(sent_title):
        mismatches["title"] = (sent_title, stored_title)
    if readback.get("slug") != payload.get("slug"):
        mismatches["slug"] = (payload.get("slug"), readback.get("slug"))
    before_status = (before or {}).get("status")
    if "status" not in payload:
        sent_status = before_status
        allowed = {before_status}
    elif before_status == "publish":
        sent_status = payload["status"]
        allowed = {sent_status}
    else:
        sent_status = payload["status"]
        allowed = _READBACK_STATUS_ALIASES.get(sent_status, {sent_status})
    if readback.get("status") not in allowed:
        mismatches["status"] = (sent_status, readback.get("status"))
    # An update without --date sends none, and WordPress may still move a draft's
    # floating date, so there is nothing of ours to compare.
    if "date" in payload and not _same_post_date(payload["date"], readback):
        mismatches["date"] = (payload["date"], readback.get("date"))
    return mismatches
