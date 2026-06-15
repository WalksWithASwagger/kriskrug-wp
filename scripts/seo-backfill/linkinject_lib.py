"""Pure logic for the internal-link spoke-injection engine.

No network, no WordPress imports — unit-testable in isolation. The only job
here is: given a post's raw Gutenberg content, figure out which contextual
anchors to insert (via text_polish.auto_link_first_occurrence) and whether to
append a "Part of the …collection" footer block.

SAFETY MODEL: assert_minimal_diff is the load-bearing guard. It reconstructs
the original body from the proposed new body by reversing every anchor insertion
and stripping the footer block, then diffs the result against the original.
Any unexplained character — a deleted word, a reordered paragraph, a replaced
em-dash — causes a MinimalDiffError and prevents the write from reaching the
CLI caller. The 2026-05-15 incident class (full-body overwrite) is impossible
to slip past this check.
"""

from __future__ import annotations

import difflib
import html as _html_mod
import random
import re
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Pillar page map
# ---------------------------------------------------------------------------

# category_term_id -> (pillar_url, anchor_vocabulary)
# Vocabulary lists are longest-to-shortest so the most specific anchor wins.
PILLAR_BY_CATEGORY: dict[int, tuple[str, list[str]]] = {
    1662: (
        "https://kriskrug.co/vancouver-ai/",
        [
            "Vancouver AI Ecosystem",
            "Vancouver AI community",
            "Vancouver AI",
        ],
    ),
    1665: (
        "https://kriskrug.co/ai-for-creatives/",
        [
            "AI for Creatives",
            "creative AI",
            "AI creativity",
        ],
    ),
    1676: (
        "https://kriskrug.co/ai-events/",
        [
            "Events and Reports",
            "AI events",
            "event coverage",
        ],
    ),
    1678: (
        "https://kriskrug.co/ai-ethics/",
        [
            "AI Ethics and Philosophy",
            "AI ethics",
            "ethical AI",
        ],
    ),
    1677: (
        "https://kriskrug.co/ai-conversations/",
        [
            "Conversations and Interviews",
            "AI conversations",
            "AI interviews",
        ],
    ),
    1679: (
        "https://kriskrug.co/ai-for-journalists/",
        [
            "AI for Journalism and Media",
            "AI for journalists",
            "AI journalism",
        ],
    ),
    1680: (
        "https://kriskrug.co/ai-tools/",
        [
            "Generative AI Tools",
            "generative AI tools",
            "AI tools",
        ],
    ),
    1675: (
        "https://kriskrug.co/indigenous-ai/",
        [
            "Indigenous and Reconciliation in Tech",
            "Indigenous AI",
            "reconciliation in tech",
        ],
    ),
    # Folded categories (no dedicated pillar) -> nearest topical pillar.
    1754: (  # Responsible AI & Policy -> AI Ethics
        "https://kriskrug.co/ai-ethics/",
        ["responsible AI", "AI ethics", "AI policy"],
    ),
    1755: (  # Creative Technology & Making -> AI for Creatives
        "https://kriskrug.co/ai-for-creatives/",
        ["creative technology", "AI for Creatives", "making with AI"],
    ),
    1753: (  # Keynotes & Speaking -> AI Events & Recaps
        "https://kriskrug.co/ai-events/",
        ["AI keynotes and talks", "AI events", "keynote recaps"],
    ),
    1681: (  # Field Notes (KK's AI essays/observations) -> AI for Creatives
        "https://kriskrug.co/ai-for-creatives/",
        ["AI for Creatives", "creative AI", "AI field notes"],
    ),
}

FOOTER_SENTINEL = "kk-collection-footer"

# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class MinimalDiffError(Exception):
    """Raised when the proposed new content has unexplained differences from
    the original (i.e., more than just inserted anchors + the footer block)."""


# ---------------------------------------------------------------------------
# Footer block
# ---------------------------------------------------------------------------

def _purge_em_dashes(s: str) -> str:
    """Inline copy of text_polish.purge_em_dashes — avoids a circular import
    and keeps linkinject_lib fully standalone (pure, no side effects)."""
    if not s:
        return s
    s = re.sub(r"\s*—\s*", ", ", s)
    s = re.sub(r"(?<!\d)\s*–\s*(?!\d)", "-", s)
    return s


def _pick_anchor(vocabulary: list[str], wave: str, seed: int | None = None) -> str:
    """Pick an anchor text from the pillar vocabulary.

    Wave A: rotate through the list deterministically via hash-based pick so
    repeated runs on different posts vary the anchor without randomness.
    Wave B: same strategy — the wave distinction lives at the sibling cap level.
    seed: used in tests for determinism."""
    if not vocabulary:
        return "pillar"
    if seed is not None:
        idx = seed % len(vocabulary)
    else:
        idx = 0
    return _purge_em_dashes(vocabulary[idx % len(vocabulary)])


def build_footer_block(
    pillar: tuple[str, list[str]],
    siblings: list[dict],
    wave: str,
    *,
    _anchor_seed: int | None = None,
) -> str:
    """Build the Gutenberg paragraph block that closes a spoke post.

    pillar: (url, vocabulary) tuple from PILLAR_BY_CATEGORY.
    siblings: list of {title, url} dicts (already ranked, already capped).
    wave: 'A' or 'B'. Wave B gets at most 1 sibling.
    _anchor_seed: optional int for deterministic anchor selection in tests.

    Returns the exact block string (no trailing newline — caller joins with \\n\\n).
    """
    pillar_url, vocabulary = pillar
    anchor = _pick_anchor(vocabulary, wave, seed=_anchor_seed)

    # Wave B: cap siblings to 1.
    if wave == "B":
        siblings = siblings[:1]
    else:
        siblings = siblings[:2]

    sib_titles = [_purge_em_dashes(_html_mod.unescape(s["title"])) for s in siblings]
    sib_urls = [s["url"] for s in siblings]

    if not siblings:
        body = f'Part of the <a href="{pillar_url}">{anchor}</a> collection.'
    elif len(siblings) == 1:
        body = (
            f'Part of the <a href="{pillar_url}">{anchor}</a> collection. '
            f'See also: <a href="{sib_urls[0]}">{sib_titles[0]}</a>.'
        )
    else:
        body = (
            f'Part of the <a href="{pillar_url}">{anchor}</a> collection. '
            f'See also: <a href="{sib_urls[0]}">{sib_titles[0]}</a> and '
            f'<a href="{sib_urls[1]}">{sib_titles[1]}</a>.'
        )

    return (
        f'<!-- wp:paragraph {{"className":"{FOOTER_SENTINEL}"}} -->\n'
        f'<p class="{FOOTER_SENTINEL}">{body}</p>\n'
        f'<!-- /wp:paragraph -->'
    )


# ---------------------------------------------------------------------------
# Idempotence guards
# ---------------------------------------------------------------------------

def has_footer(content: str) -> bool:
    """Return True if the content already contains our footer sentinel."""
    return FOOTER_SENTINEL in content


def remove_existing_footer(content: str) -> str:
    """Strip our footer block from content (idempotence on re-run).

    Matches the opening wp:paragraph comment through the closing /wp:paragraph
    comment when the className contains our sentinel. Handles optional trailing
    newline after the block."""
    pattern = re.compile(
        r"\n*<!-- wp:paragraph \{[^}]*" + re.escape(FOOTER_SENTINEL) + r'[^}]*\} -->'
        r".*?"
        r"<!-- /wp:paragraph -->",
        re.DOTALL,
    )
    return pattern.sub("", content)


# ---------------------------------------------------------------------------
# Minimal-diff guard
# ---------------------------------------------------------------------------

def strip_inserted_anchors(html: str, applied: list[dict]) -> str:
    """Reverse exactly the anchors that auto_link_first_occurrence inserted.

    For each {text, url} in applied (in the order they were applied), collapse
    <a href="URL"[^>]*>TEXT</a> -> TEXT, count=1. This is the inverse operation
    used by assert_minimal_diff to reconstruct the original content."""
    out = html
    for entry in applied:
        text = re.escape(entry["text"])
        url = re.escape(entry["url"])
        pattern = re.compile(
            r'<a\s+href="' + url + r'"[^>]*>' + text + r'</a>',
            re.IGNORECASE,
        )
        out = pattern.sub(entry["text"], out, count=1)
    return out


def assert_minimal_diff(
    old: str,
    new: str,
    applied: list[dict],
    footer_block: str | None,
) -> None:
    """Assert that new == old after reversing every anchor insertion and the
    footer block. Raises MinimalDiffError with a unified diff on mismatch.

    Steps:
    1. If footer_block provided, assert new ends with it (preceded by \\n\\n)
       and strip it from the working copy.
    2. Reverse each anchor insertion (strip_inserted_anchors).
    3. Compare reconstructed.rstrip("\\n") == old.rstrip("\\n").
    """
    work = new

    if footer_block:
        # Footer must be a suffix, separated from body by exactly \n\n.
        expected_suffix = "\n\n" + footer_block
        if not work.endswith(expected_suffix):
            raise MinimalDiffError(
                f"footer block not found as suffix of new content. "
                f"Last 200 chars of new: {work[-200:]!r}"
            )
        work = work[: -len(expected_suffix)]

    reconstructed = strip_inserted_anchors(work, applied)

    lhs = old.rstrip("\n")
    rhs = reconstructed.rstrip("\n")
    if lhs != rhs:
        diff = "\n".join(
            difflib.unified_diff(
                lhs.splitlines(),
                rhs.splitlines(),
                fromfile="original",
                tofile="reconstructed",
                lineterm="",
            )
        )
        raise MinimalDiffError(
            f"reconstructed content differs from original:\n{diff}"
        )


# ---------------------------------------------------------------------------
# Sibling ranking
# ---------------------------------------------------------------------------

_LEGACY_CUTOFF_YEAR = 2014


def _post_year(post: dict) -> int:
    """Extract year from post date string (ISO 8601). Returns 0 on parse failure."""
    date = post.get("date") or post.get("date_gmt") or ""
    try:
        return int(date[:4])
    except (ValueError, TypeError):
        return 0


def _title_tokens(title: str) -> set[str]:
    """Lowercased word tokens from a post title, for shared-token boost."""
    return set(re.findall(r"\b\w+\b", title.lower()))


def rank_siblings(
    post: dict,
    candidates: list[dict],
    n: int,
) -> list[dict]:
    """Select and rank up to n sibling posts for the footer "See also" links.

    Exclusions:
    - self (matched by id)
    - legacy stubs: empty/short title (< 5 chars) or published before 2014

    Scoring (descending priority):
    1. Shared title-token boost (posts sharing >= 2 tokens with subject post)
    2. Recency (year desc, then id desc as tiebreak)

    Returns list of {title, url} with titles HTML-unescaped and em-dash-purged.
    """
    self_id = post.get("id")
    self_title_tokens = _title_tokens(
        _html_mod.unescape((post.get("title") or {}).get("raw") or "")
    )

    scored: list[tuple[int, int, dict]] = []
    for c in candidates:
        # Exclude self
        if c.get("id") == self_id:
            continue
        # Exclude legacy stubs
        raw_title = (c.get("title") or {}).get("raw") or (c.get("title") or {}).get("rendered") or ""
        clean_title = _html_mod.unescape(raw_title).strip()
        if len(clean_title) < 5:
            continue
        year = _post_year(c)
        if year and year < _LEGACY_CUTOFF_YEAR:
            continue

        # Shared token boost: +10000 per shared non-trivial token
        shared = _title_tokens(clean_title) & self_title_tokens
        # Filter out very short tokens (stop-word-like)
        meaningful_shared = {t for t in shared if len(t) > 3}
        boost = len(meaningful_shared) * 10000

        cid = int(c.get("id") or 0)
        scored.append((boost + year * 100 + cid, cid, c))

    scored.sort(key=lambda x: x[0], reverse=True)

    result = []
    for _, _, c in scored[:n]:
        raw_title = (c.get("title") or {}).get("raw") or (c.get("title") or {}).get("rendered") or ""
        title = _purge_em_dashes(_html_mod.unescape(raw_title).strip())
        url = c.get("link") or ""
        result.append({"title": title, "url": url})
    return result


# ---------------------------------------------------------------------------
# Link planning
# ---------------------------------------------------------------------------

# How many existing internal kriskrug.co links count toward the cap.
# Exclude media/system paths: Gutenberg image blocks with linkDestination=media
# produce <a href="https://kriskrug.co/wp-content/uploads/...img"> wrappers that
# are NOT navigational internal links and must not inflate the cap (they caused
# image-heavy posts to be falsely skipped as cap-met).
_INTERNAL_RE = re.compile(
    r'href="https://kriskrug\.co/(?!wp-content/|wp-includes/|wp-admin/|feed/|wp-json/)',
    re.IGNORECASE,
)


def _validate_contextual(original: str, new_content: str, applied: list[dict]) -> None:
    """Run assert_minimal_diff on only the contextual portion (no footer).

    Raises MinimalDiffError if the contextual anchors alone are malformed —
    used by plan_links_for_post to decide whether to fall back to footer-only."""
    assert_minimal_diff(original, new_content, applied, footer_block=None)


def _count_internal_links(content: str) -> int:
    return len(_INTERNAL_RE.findall(content))


def _pillar_already_linked(content: str, pillar_url: str) -> bool:
    escaped = re.escape(pillar_url.rstrip("/"))
    return bool(re.search(r'href="' + escaped, content, re.IGNORECASE))


def plan_links_for_post(
    content_raw: str,
    self_url: str,
    pillar: tuple[str, list[str]] | None,
    siblings: list[dict],
    wave: str,
    *,
    _anchor_seed: int | None = None,
) -> tuple[str, list[dict], str | None, list[str]]:
    """Plan all link insertions for a single post.

    Returns (new_content, applied, footer_block, flags).
    - new_content: the modified Gutenberg content string.
    - applied: list of {text, url} dicts from auto_link_first_occurrence.
    - footer_block: the rendered footer block string, or None if skipped.
    - flags: list of string flags explaining any decisions made.

    Idempotence: if the content already contains our footer sentinel, skip
    and return the original content unchanged with flag 'already-done'.

    Cap logic (2-5 internal links across contextual + footer):
    - Count existing kriskrug.co links.
    - After auto_link_first_occurrence adds contextual anchors, trim applied
      to keep total internal links <= 5.
    - If pillar is already contextually linked, skip the footer pillar sentence
      (set flag 'pillar-contextually-linked').
    - If pillar + >= 2 siblings are already linked, skip footer entirely
      (flag 'cap-met').
    """
    import sys
    from pathlib import Path
    # Import auto_link_first_occurrence from text_polish (same repo).
    _repo_root = Path(__file__).resolve().parent.parent.parent
    _polish_path = str(_repo_root / "scripts" / "notion-to-wp")
    if _polish_path not in sys.path:
        sys.path.insert(0, _polish_path)
    from text_polish import auto_link_first_occurrence  # type: ignore[import]

    flags: list[str] = []

    # Idempotence check
    if has_footer(content_raw):
        flags.append("already-done")
        return content_raw, [], None, flags

    if pillar is None:
        flags.append("no-pillar")
        # Still run auto_link_first_occurrence for contextual anchors from LINK_MAP.
        new_content, applied = auto_link_first_occurrence(content_raw, self_url)
        return new_content, applied, None, flags

    pillar_url, vocabulary = pillar

    # Run contextual auto-linking — wrapped in a try/except so a malformed
    # anchor in the contextual layer never hard-fails the whole post.  If the
    # resulting new_content would fail assert_minimal_diff, we discard the
    # contextual work and fall back to footer-only (the append-only footer is
    # provably safe).  The post gets the flag 'contextual-dropped' when this
    # happens so dry-run reports make the degradation visible.
    try:
        new_content, applied = auto_link_first_occurrence(content_raw, self_url)
        # Validate the contextual changes immediately — if they'd fail the
        # minimal-diff guard later, catch it now before building the footer.
        _validate_contextual(content_raw, new_content, applied)
    except MinimalDiffError:
        # Contextual layer produced a malformed anchor; fall back to footer-only.
        flags.append("contextual-dropped")
        new_content = content_raw
        applied = []

    # Count how many internal links exist after contextual linking.
    existing_before = _count_internal_links(content_raw)
    added_by_auto = len(applied)
    total_after_auto = existing_before + added_by_auto

    # Trim applied if over cap (keep the first ones — they appear earlier in body).
    CAP = 5
    if total_after_auto > CAP:
        # How many new links are we allowed to add?
        allowed_new = max(0, CAP - existing_before)
        if allowed_new < added_by_auto:
            flags.append(f"auto-link-trimmed-to-{allowed_new}")
            # We need to rebuild new_content without the trimmed anchors.
            # Re-run with the trimmed applied list is complex; instead, we
            # strip the excess anchors from new_content using strip_inserted_anchors.
            trimmed_applied = applied[:allowed_new]
            excess = applied[allowed_new:]
            new_content = strip_inserted_anchors(new_content, excess)
            applied = trimmed_applied
            total_after_auto = existing_before + len(applied)

    # Check cap-met: if pillar + >=2 siblings already linked, skip footer.
    pillar_linked_contextually = _pillar_already_linked(new_content, pillar_url)
    sib_linked_count = sum(
        1 for s in siblings
        if s.get("url") and _pillar_already_linked(new_content, s["url"])
    )

    if pillar_linked_contextually and sib_linked_count >= 2:
        flags.append("cap-met")
        return new_content, applied, None, flags

    # Determine footer sibling budget.
    remaining_budget = CAP - total_after_auto
    if pillar_linked_contextually:
        flags.append("pillar-contextually-linked")
        # Footer will omit the pillar sentence; each sibling = 1 link.
        # But build_footer_block always includes the pillar link. So we
        # note this and let the block include it anyway (it's a pillar page —
        # the link is editorial, not spam). We just note the flag.

    # Cap siblings for the footer: wave B = 1, wave A = 2; also respect budget.
    wave_sib_cap = 1 if wave == "B" else 2
    # Footer adds 1 (pillar) + len(siblings) links.
    # Budget for footer links:
    if remaining_budget <= 0:
        # No room for footer at all.
        flags.append("cap-met-no-footer-room")
        return new_content, applied, None, flags

    # Footer always links pillar (1 link) + siblings.
    sib_budget = min(wave_sib_cap, remaining_budget - 1)  # -1 for the pillar link
    sib_budget = max(0, sib_budget)

    footer_siblings = siblings[:sib_budget]

    footer_block = build_footer_block(
        pillar, footer_siblings, wave, _anchor_seed=_anchor_seed
    )
    new_content = new_content + "\n\n" + footer_block

    return new_content, applied, footer_block, flags


# ---------------------------------------------------------------------------
# Payload builder
# ---------------------------------------------------------------------------

_CONTENT_PAYLOAD_ALLOWLIST = frozenset({"content"})


def build_content_payload(new_content: str) -> dict:
    """Build the WP REST partial-update payload for a content write.

    Raises ValueError if called with any key other than 'content' (hard guard
    against accidentally including title, slug, status, meta, etc.)."""
    payload = {"content": new_content}
    # Hard allowlist check — if this function is ever extended to accept a dict,
    # reject anything outside the single allowed key.
    bad = set(payload) - _CONTENT_PAYLOAD_ALLOWLIST
    if bad:
        raise ValueError(f"build_content_payload: disallowed keys {sorted(bad)}")
    return payload
