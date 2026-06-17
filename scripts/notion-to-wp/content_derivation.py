from __future__ import annotations

import re


def _plain_text(block: dict) -> str:
    t = block.get("type")
    if not t:
        return ""
    content = block.get(t, {})
    rts = content.get("rich_text") if isinstance(content, dict) else None
    return "".join(rt.get("plain_text", "") for rt in (rts or []))


def _block_plain_text_deep(block: dict) -> str:
    txt = _plain_text(block)
    for child in (block.get("_children") or []):
        c = _plain_text(child)
        if c:
            txt = (txt + " " + c).strip()
    return txt


def derive_excerpt(blocks: list[dict], max_chars: int = 300) -> str:
    """
    Find KK's own voice for the excerpt. Prefer a substantive early callout,
    then the first substantive paragraph. Never returns third-person AI summary.
    """
    flat = []

    def walk(bs):
        for b in bs:
            flat.append(b)
            walk(b.get("_children") or [])

    walk(blocks)

    candidate = ""
    for b in flat:
        if b.get("type") == "callout":
            t = _block_plain_text_deep(b)
            if len(t.strip()) >= 40:
                candidate = t
                break
    if not candidate:
        for b in flat:
            if b.get("type") == "paragraph":
                t = _plain_text(b)
                if len(t.strip()) >= 40:
                    candidate = t
                    break

    if not candidate:
        return ""

    candidate = re.sub(
        r"^\s*(the\s+)?(short\s+version|tldr|tl;dr|summary)[:\s—-]+",
        "",
        candidate,
        count=1,
        flags=re.IGNORECASE,
    ).strip()
    sentences = re.split(r"(?<=[.!?])\s+", candidate)
    out = ""
    for s in sentences:
        if len(out) + len(s) + 1 > max_chars:
            break
        out = (out + " " + s).strip()
    return out or candidate[:max_chars].rstrip()


def derive_seo_title(title: str, max_chars: int = 60) -> str:
    suffix = " | Kris Krüg"
    if len(title) + len(suffix) <= max_chars:
        return title + suffix
    return title[:max_chars]


def derive_social_message(excerpt: str, max_chars: int = 280) -> str:
    if len(excerpt) <= max_chars:
        return excerpt
    cut = excerpt[:max_chars]
    boundary = max(cut.rfind(". "), cut.rfind("! "), cut.rfind("? "))
    if boundary > max_chars - 80:
        return cut[: boundary + 1].rstrip()
    return cut.rstrip() + "…"
