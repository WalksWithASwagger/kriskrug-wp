"""
text_polish.py — post-render polish applied to body HTML, excerpt, and SEO fields
before they ship to WordPress.

Two passes:

1. purge_em_dashes:   "—" → ", "    "–" → "-"  (range en-dashes preserved if numeric)
   Reason: em-dashes read as AI-generated in 2026. KK's rule, applied site-wide.

2. auto_link_first_occurrence: turn proper-noun mentions into hyperlinks the first
   time they appear in a post. Drives traffic to KK's properties (kriskrug.co
   pillar posts, bc-ai.ca, theupgrade.ai) and to people/projects KK references.

The LINK_MAP below is the single source of truth. Add to it; don't sprinkle
URL-replacement logic elsewhere.
"""
from __future__ import annotations

import re

# ---------------------------------------------------------------------------
# Pass 1 — em-dash purge
# ---------------------------------------------------------------------------

def purge_em_dashes(s: str) -> str:
    if not s:
        return s
    # Em-dash: replace with ", " regardless of surrounding whitespace.
    # Handles "word — word", "word—word", "word —word", "word— word".
    s = re.sub(r"\s*—\s*", ", ", s)
    # En-dash: keep numeric ranges (e.g. "2024–2026", "0–5"), convert prose en-dashes to hyphens.
    s = re.sub(r"(?<!\d)\s*–\s*(?!\d)", "-", s)
    return s


# ---------------------------------------------------------------------------
# Pass 2 — auto-link first occurrence of proper nouns
# ---------------------------------------------------------------------------

# Order matters: longer phrases first so "BC + AI Ecosystem" wins over a bare "BC".
# Each entry: (regex pattern, url, optional title attribute).
LINK_MAP: list[tuple[str, str, str | None]] = [
    # KK's own properties + organizations he runs
    (r"\bBC\s*\+\s*AI\s+Ecosystem\b",            "https://bc-ai.ca/",                  "BC + AI Ecosystem"),
    (r"\bTheUpgrade\.?ai\b",                     "https://www.theupgrade.ai/",         "The Upgrade AI"),
    (r"\bThe\s+Upgrade\s+AI\b",                  "https://www.theupgrade.ai/",         "The Upgrade AI"),
    (r"\bIndigenomics\.?ai\b",                   "https://indigenomics.ai/",           "Indigenomics AI"),

    # KK's own pillar posts — internal cross-links to keep traffic on kriskrug.co
    (r"\bPunk\s+Rock\s+AI\b",                    "https://kriskrug.co/2025/01/14/punk-rock-ai-a-manifesto-for-the-renegade-creators-of-tomorrow/", "Punk Rock AI manifesto"),
    (r"\bBoth\s+Hands\s+Full\b",                 "https://kriskrug.co/2026/05/16/make-culture-not-content/", "Both Hands Full — Make Culture, Not Content"),
    (r"\b(?:your\s+)?taste\s+is\s+your\s+moat\b","https://kriskrug.co/2026/05/15/your-taste-is-your-moat/", "Your Taste Is Your Moat"),
    (r"\bmycelial\s+network\b",                  "https://kriskrug.co/2025/02/16/bcs-ai-ecosystem-a-mycelial-network-of-creation/", "BC's AI Ecosystem: A Mycelial Network"),

    # External — people, events, projects (high-traffic / Wikipedia-quality targets)
    (r"\bWeb\s+Summit\s+Vancouver\b",            "https://vancouver.websummit.com/",   "Web Summit Vancouver"),
    (r"\bOpenAI\b",                              "https://openai.com/",                None),
    (r"\bAnthropic\b",                           "https://www.anthropic.com/",         None),
    (r"\bClaude\b(?!\s+Code)",                   "https://claude.ai/",                 None),
    (r"\bClaude\s+Code\b",                       "https://www.claude.com/product/claude-code", None),
    (r"\bDwarkesh\s+Patel\b",                    "https://www.dwarkesh.com/",          "Dwarkesh Patel"),
    (r"\bLaSalle\s+College\s+Vancouver\b",       "https://www.lasallecollegevancouver.com/", "LaSalle College Vancouver"),
]

# Compile once, anchor to word boundaries when not already in the pattern.
_COMPILED = [(re.compile(p, re.IGNORECASE), url, title) for (p, url, title) in LINK_MAP]

# Skip linking inside these wrappers — they'd either nest <a> tags or visually break things.
_SKIP_INSIDE = re.compile(
    r"<(a|h[1-6]|figcaption|cite|code|pre|script|style)\b[^>]*>.*?</\1>",
    re.IGNORECASE | re.DOTALL,
)


def auto_link_first_occurrence(html: str, self_url: str | None = None) -> tuple[str, list[dict]]:
    """Hyperlink the first occurrence of each LINK_MAP term that isn't already a
    link or inside a heading/figcaption/cite. Returns (new_html, applied) where
    applied is a list of dicts describing each substitution (for the publish log).

    self_url: optional URL of the post being polished. If a LINK_MAP entry's url
    equals self_url, that term is skipped (don't self-link a post to itself)."""
    if not html:
        return html, []

    # Mask skip-zones so .sub() can't reach inside them. Mask → restore.
    masks: list[str] = []
    def mask(m):
        masks.append(m.group(0))
        return f"\x00MASK{len(masks)-1}\x00"
    masked = _SKIP_INSIDE.sub(mask, html)

    applied: list[dict] = []
    for regex, url, title in _COMPILED:
        if self_url and url.rstrip("/") == self_url.rstrip("/"):
            continue
        replaced = {"done": False}
        def repl(m):
            if replaced["done"]:
                return m.group(0)
            replaced["done"] = True
            anchor_text = m.group(0)
            title_attr = f' title="{title}"' if title else ""
            applied.append({"text": anchor_text, "url": url})
            return f'<a href="{url}"{title_attr}>{anchor_text}</a>'
        masked = regex.sub(repl, masked, count=1)

    # Restore skip-zones
    def unmask(m):
        idx = int(m.group(1))
        return masks[idx]
    out = re.sub(r"\x00MASK(\d+)\x00", unmask, masked)
    return out, applied


# ---------------------------------------------------------------------------
# Convenience: apply both passes to a piece of HTML
# ---------------------------------------------------------------------------

def polish_html(html: str, self_url: str | None = None) -> tuple[str, dict]:
    """Apply em-dash purge + auto-link to body HTML. Returns (html, report)."""
    out = purge_em_dashes(html)
    out, links = auto_link_first_occurrence(out, self_url=self_url)
    return out, {"links_added": links}


def polish_text(text: str) -> str:
    """Apply only em-dash purge to plain text (excerpts, SEO titles, social messages)."""
    return purge_em_dashes(text)
