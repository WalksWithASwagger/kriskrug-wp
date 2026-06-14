"""Pure derivation + decision logic for the SEO metadata backfill.

No network, no WordPress imports — unit-testable in isolation. The only job
here is: given a WP REST item (context=edit, with meta/excerpt/content/title),
decide which of the three Jetpack SEO meta keys are EMPTY and derive a value
for each. Emptiness is decided by the *same* function the seo-audit uses, so
backfill and audit can never disagree.
"""

from __future__ import annotations

import html
import re
from dataclasses import dataclass, field

# Single source of truth for the three keys we are allowed to touch.
# Mirrors scripts/seo-audit/inventory_lib.py.
SEO_TITLE_KEYS = ("jetpack_seo_html_title",)
META_DESC_KEYS = ("advanced_seo_description",)
SOCIAL_KEYS = ("jetpack_publicize_message",)

ALLOWED_META_KEYS = frozenset(SEO_TITLE_KEYS + META_DESC_KEYS + SOCIAL_KEYS)

FIELD_TO_KEY = {
    "seo_title": SEO_TITLE_KEYS[0],
    "meta_desc": META_DESC_KEYS[0],
    "social": SOCIAL_KEYS[0],
}

_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")


def meta_value(meta: dict, keys: tuple[str, ...]) -> str:
    """A meta field counts as set only if it is a non-empty, non-whitespace str.
    Identical semantics to inventory_lib.meta_value."""
    for key in keys:
        value = meta.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def strip_html(value: str) -> str:
    return _WS_RE.sub(" ", html.unescape(_TAG_RE.sub(" ", value or ""))).strip()


def title_text(item: dict) -> str:
    """Prefer the raw title (context=edit), fall back to unescaped rendered."""
    t = item.get("title") or {}
    if isinstance(t, dict):
        raw = (t.get("raw") or "").strip()
        if raw:
            return raw
        return html.unescape((t.get("rendered") or "").strip())
    return str(t or "").strip()


def _rendered(item: dict, key: str) -> str:
    v = item.get(key) or {}
    if isinstance(v, dict):
        return v.get("rendered") or v.get("raw") or ""
    return str(v or "")


def derive_seo_title(title: str, max_chars: int = 60) -> str:
    """Append ' | Kris Krüg' if it fits; otherwise the title alone (truncated).
    Same rule as the Notion publisher's derive_seo_title."""
    suffix = " | Kris Krüg"
    if len(title) + len(suffix) <= max_chars:
        return title + suffix
    return title[:max_chars]


def _trim_to_sentence(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    cut = text[:max_chars]
    boundary = max(cut.rfind(". "), cut.rfind("! "), cut.rfind("? "))
    if boundary > max_chars - 80:
        return cut[: boundary + 1].rstrip()
    return cut.rstrip() + "…"


def derive_meta_description(item: dict, max_chars: int = 200) -> tuple[str, str]:
    """Return (description, source). source is 'excerpt', 'first_paragraph', or
    'none'. Prefer the authored excerpt; fall back to the first real paragraph
    of the content. Returns ('', 'none') when nothing usable exists."""
    excerpt = strip_html(_rendered(item, "excerpt"))
    if excerpt:
        return _trim_to_sentence(excerpt, max_chars), "excerpt"
    content_html = _rendered(item, "content")
    for chunk in re.split(r"</p>|<br\s*/?>|\n", content_html):
        text = strip_html(chunk)
        if len(text) >= 40:  # skip headings, captions, single links
            return _trim_to_sentence(text, max_chars), "first_paragraph"
    return "", "none"


def derive_social_message(text: str, max_chars: int = 280) -> str:
    """Same trimming as the publisher's derive_social_message."""
    return _trim_to_sentence(text or "", max_chars)


_CAPTION_RE = re.compile(r"^(photo|image|figure|fig\.|caption|credit)\b", re.I)


@dataclass
class MetaPlan:
    planned: dict = field(default_factory=dict)  # only EMPTY + derivable keys
    flags: list[str] = field(default_factory=list)
    note: str = ""  # why nothing/partial was planned

    @property
    def is_empty(self) -> bool:
        return not self.planned


def plan_meta_for_item(item: dict, kind: str, fields=("seo_title", "meta_desc", "social")) -> MetaPlan:
    """Build the additive-only plan: include a key ONLY if it is currently empty
    and we can derive a value. Never includes a non-empty field. Social message
    applies to posts only."""
    meta = item.get("meta") or {}
    plan = MetaPlan()

    if "seo_title" in fields and not meta_value(meta, SEO_TITLE_KEYS):
        title = title_text(item)
        if not title:
            plan.flags.append("seo_title:no-source")
        else:
            value = derive_seo_title(title)
            # Only backfill when the ' | Kris Krüg' suffix fits — that's a pure
            # branding gain. When the title is too long, derive_seo_title would
            # TRUNCATE it; but an empty jetpack_seo_html_title already falls back
            # to the full post title in WP, so a truncated value is worse than
            # empty. Skip those and leave the WP default intact.
            if value.endswith("Kris Krüg"):
                plan.planned[SEO_TITLE_KEYS[0]] = value
            else:
                plan.flags.append("seo_title:skipped-too-long")

    desc = ""
    desc_source = "none"
    if "meta_desc" in fields and not meta_value(meta, META_DESC_KEYS):
        desc, desc_source = derive_meta_description(item)
        if desc:
            plan.planned[META_DESC_KEYS[0]] = desc
            if desc_source == "first_paragraph":
                plan.flags.append("desc:first-paragraph-fallback")
            if len(desc) < 50:
                plan.flags.append("desc:short")
            if _CAPTION_RE.match(desc):
                plan.flags.append("desc:looks-like-caption")
        else:
            plan.flags.append("desc:no-source")

    if "social" in fields and kind == "post" and not meta_value(meta, SOCIAL_KEYS):
        # Reuse the excerpt/first-paragraph text we already derived.
        source_text = desc or strip_html(_rendered(item, "excerpt"))
        if source_text:
            plan.planned[SOCIAL_KEYS[0]] = derive_social_message(source_text)
            if desc_source == "first_paragraph" or (not desc and not strip_html(_rendered(item, "excerpt"))):
                plan.flags.append("social:derived-from-body")
        else:
            plan.flags.append("social:no-source")

    if plan.is_empty:
        plan.note = "nothing empty to fill" if meta else "no meta/derivable source"
    return plan


def build_meta_payload(planned: dict) -> dict:
    """Hard enforcement of additive-only / meta-only. Raises if any planned key
    is outside the 3-key allowlist. The returned payload has exactly one
    top-level key, `meta`, so a WP REST partial update can touch nothing else."""
    if not planned:
        raise ValueError("empty plan — nothing to write")
    bad = set(planned) - ALLOWED_META_KEYS
    if bad:
        raise ValueError(f"refusing to write non-allowlisted meta keys: {sorted(bad)}")
    return {"meta": dict(planned)}
