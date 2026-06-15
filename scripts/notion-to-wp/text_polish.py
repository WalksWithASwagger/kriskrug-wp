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

    # KK's pillar pages — internal hub links (topic cluster spokes point here)
    # Longer phrases first so "Vancouver AI Ecosystem" wins over bare "Vancouver AI".
    (r"\bVancouver\s+AI\s+Ecosystem\b",          "https://kriskrug.co/vancouver-ai/",           "Vancouver AI Ecosystem"),
    (r"\bVancouver\s+AI\s+community\b",          "https://kriskrug.co/vancouver-ai/",           "Vancouver AI community"),
    (r"\bAI\s+for\s+Creatives\b",               "https://kriskrug.co/ai-for-creatives/",       "AI for Creatives"),
    (r"\bcreative\s+AI\b",                       "https://kriskrug.co/ai-for-creatives/",       "AI for Creatives"),
    (r"\bAI\s+for\s+Journalism\s+(?:and|&)\s+Media\b", "https://kriskrug.co/ai-for-journalists/", "AI for Journalism and Media"),
    (r"\bAI\s+for\s+journalists?\b",             "https://kriskrug.co/ai-for-journalists/",     "AI for journalists"),
    (r"\bAI\s+journalism\b",                     "https://kriskrug.co/ai-for-journalists/",     "AI journalism"),
    (r"\bIndigenous\s+(?:and|&)\s+Reconciliation\s+in\s+Tech\b", "https://kriskrug.co/indigenous-ai/", "Indigenous and Reconciliation in Tech"),
    (r"\bIndigenous\s+AI\b",                     "https://kriskrug.co/indigenous-ai/",          "Indigenous AI"),
    (r"\breconciliation\s+in\s+tech\b",          "https://kriskrug.co/indigenous-ai/",          "reconciliation in tech"),
    (r"\bAI\s+Ethics\s+(?:and|&)\s+Philosophy\b","https://kriskrug.co/ai-ethics/",             "AI Ethics and Philosophy"),
    (r"\bethical\s+AI\b",                        "https://kriskrug.co/ai-ethics/",              "ethical AI"),
    (r"\bAI\s+ethics\b",                         "https://kriskrug.co/ai-ethics/",              "AI ethics"),
    (r"\bGenerative\s+AI\s+Tools?\b",            "https://kriskrug.co/ai-tools/",               "Generative AI Tools"),
    (r"\bgenerative\s+AI\s+tools?\b",            "https://kriskrug.co/ai-tools/",               "generative AI tools"),
    (r"\bConversations?\s+(?:and|&)\s+Interviews?\b", "https://kriskrug.co/ai-conversations/",  "Conversations and Interviews"),
    (r"\bAI\s+conversations?\b",                 "https://kriskrug.co/ai-conversations/",       "AI conversations"),
    (r"\bAI\s+events?\b",                        "https://kriskrug.co/ai-events/",              "AI events"),
    # Bare "Vancouver AI" is intentionally lower priority than the ecosystem phrase above.
    (r"\bVancouver\s+AI\b",                      "https://kriskrug.co/vancouver-ai/",           "Vancouver AI"),

    # KK's own pillar posts — internal cross-links to keep traffic on kriskrug.co
    (r"\bPunk\s+Rock\s+AI\b",                    "https://kriskrug.co/2026/05/04/punk-rock-ai/", "Punk Rock AI"),
    (r"\bBoth\s+Hands\s+Full\b",                 "https://kriskrug.co/2026/05/16/make-culture-not-content/", "Both Hands Full — Make Culture, Not Content"),  # TODO(KK): confirm canonical target
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
# _SKIP_COMMENTS: Gutenberg block-comment delimiters (including JSON attrs inside <!-- -->).
#   Masking prevents injecting into e.g. <!-- wp:quote {"citation":"OpenAI employee"} -->.
# _SKIP_TAGS: existing <a> + block-level wrappers that must not gain nested/extra links.
_SKIP_COMMENTS = re.compile(r"<!--.*?-->", re.DOTALL)
_SKIP_TAGS = re.compile(
    r"<(a|h[1-6]|figcaption|cite|code|pre|script|style)\b[^>]*>.*?</\1>",
    re.IGNORECASE | re.DOTALL,
)


def auto_link_first_occurrence(html: str, self_url: str | None = None) -> tuple[str, list[dict]]:
    """Hyperlink the first occurrence of each LINK_MAP term that isn't already a
    link, inside a Gutenberg block comment, or inside a heading/figcaption/cite.
    Returns (new_html, applied) where applied is a list of dicts describing each
    substitution (for the publish log).

    self_url: optional URL of the post being polished. If a LINK_MAP entry's url
    equals self_url, that term is skipped (don't self-link a post to itself).

    Masking strategy (two-pass, mask → sub → re-mask → restore):
    1. Mask HTML comments first (protects Gutenberg block-comment JSON attributes).
    2. Mask skip-zone tags (<a>, headings, etc.) so patterns can't reach inside them.
    3. After each successful injection, re-mask newly created <a> tags so subsequent
       patterns cannot produce nested anchors (e.g. 'Vancouver AI' matching inside
       an already-injected 'Vancouver AI community' anchor)."""
    if not html:
        return html, []

    # Mask skip-zones so .sub() can't reach inside them. Mask → restore.
    masks: list[str] = []
    def mask(m: re.Match) -> str:
        masks.append(m.group(0))
        return f"\x00MASK{len(masks)-1}\x00"

    masked = _SKIP_COMMENTS.sub(mask, html)
    masked = _SKIP_TAGS.sub(mask, masked)

    applied: list[dict] = []
    for regex, url, title in _COMPILED:
        if self_url and url.rstrip("/") == self_url.rstrip("/"):
            continue
        replaced = {"done": False}
        def repl(m: re.Match, _replaced: dict = replaced, _url: str = url, _title: str | None = title) -> str:
            if _replaced["done"]:
                return m.group(0)
            _replaced["done"] = True
            anchor_text = m.group(0)
            title_attr = f' title="{_title}"' if _title else ""
            applied.append({"text": anchor_text, "url": _url})
            return f'<a href="{_url}"{title_attr}>{anchor_text}</a>'
        new_masked = regex.sub(repl, masked, count=1)
        if replaced["done"]:
            # Re-mask the newly inserted <a> so subsequent patterns cannot nest
            # inside it (e.g. bare 'Vancouver AI' re-matching inside
            # 'Vancouver AI community' anchor text or title attribute).
            masked = _SKIP_TAGS.sub(mask, new_masked)
        else:
            masked = new_masked

    # Restore skip-zones
    def unmask(m: re.Match) -> str:
        return masks[int(m.group(1))]
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
