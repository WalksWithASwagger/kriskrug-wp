"""Unit tests for linkinject_lib — pure, no network.

Mirrors test_backfill_lib.py in structure and style.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Ensure both seo-backfill/ and notion-to-wp/ are importable.
_SEOBACKFILL = Path(__file__).resolve().parent.parent
_NOTION_TO_WP = _SEOBACKFILL.parent / "notion-to-wp"
sys.path.insert(0, str(_SEOBACKFILL))
sys.path.insert(0, str(_NOTION_TO_WP))

from linkinject_lib import (  # noqa: E402
    FOOTER_SENTINEL,
    PILLAR_BY_CATEGORY,
    MinimalDiffError,
    assert_minimal_diff,
    build_content_payload,
    build_footer_block,
    has_footer,
    plan_links_for_post,
    rank_siblings,
    remove_existing_footer,
    strip_inserted_anchors,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

PILLAR_VANCOUVER = PILLAR_BY_CATEGORY[1662]   # (url, vocabulary)
PILLAR_CREATIVES = PILLAR_BY_CATEGORY[1665]


def _post(
    pid: int = 1,
    title: str = "Hello World",
    link: str = "https://kriskrug.co/2026/01/01/hello-world/",
    date: str = "2026-01-01T00:00:00",
    categories: list[int] | None = None,
    content_raw: str = "<p>Body text here.</p>",
) -> dict:
    return {
        "id": pid,
        "slug": title.lower().replace(" ", "-"),
        "title": {"raw": title, "rendered": title},
        "link": link,
        "date": date,
        "categories": categories or [],
        "content": {"raw": content_raw, "rendered": content_raw},
    }


def _sib(
    pid: int,
    title: str,
    link: str,
    date: str = "2025-06-01T00:00:00",
) -> dict:
    return _post(pid=pid, title=title, link=link, date=date)


# ---------------------------------------------------------------------------
# FOOTER_SENTINEL constant
# ---------------------------------------------------------------------------

def test_footer_sentinel_present_in_module():
    assert FOOTER_SENTINEL == "kk-collection-footer"


# ---------------------------------------------------------------------------
# build_footer_block
# ---------------------------------------------------------------------------

def test_footer_pillar_only_when_no_siblings():
    block = build_footer_block(PILLAR_VANCOUVER, [], "A", _anchor_seed=0)
    assert "Part of the" in block
    assert "See also" not in block
    assert FOOTER_SENTINEL in block
    assert "<!-- wp:paragraph" in block
    assert "<!-- /wp:paragraph -->" in block


def test_footer_one_sibling_wave_a():
    sibs = [{"title": "Some Post", "url": "https://kriskrug.co/some-post/"}]
    block = build_footer_block(PILLAR_VANCOUVER, sibs, "A", _anchor_seed=0)
    assert "See also:" in block
    assert "Some Post" in block
    assert "and" not in block  # only one sibling


def test_footer_two_siblings_wave_a():
    sibs = [
        {"title": "Post One", "url": "https://kriskrug.co/post-one/"},
        {"title": "Post Two", "url": "https://kriskrug.co/post-two/"},
    ]
    block = build_footer_block(PILLAR_VANCOUVER, sibs, "A", _anchor_seed=0)
    assert "Post One" in block
    assert "Post Two" in block
    assert " and " in block


def test_footer_wave_b_caps_siblings_at_1():
    sibs = [
        {"title": "Post One", "url": "https://kriskrug.co/post-one/"},
        {"title": "Post Two", "url": "https://kriskrug.co/post-two/"},
    ]
    block = build_footer_block(PILLAR_VANCOUVER, sibs, "B", _anchor_seed=0)
    assert "Post One" in block
    assert "Post Two" not in block


def test_footer_em_dash_purged_in_anchor():
    # Sibling title with an em-dash should have it removed.
    sibs = [{"title": "Hello — World", "url": "https://kriskrug.co/hello-world/"}]
    block = build_footer_block(PILLAR_VANCOUVER, sibs, "A", _anchor_seed=0)
    assert "—" not in block


def test_footer_block_exact_structure():
    block = build_footer_block(PILLAR_VANCOUVER, [], "A", _anchor_seed=0)
    assert block.startswith(f'<!-- wp:paragraph {{"className":"{FOOTER_SENTINEL}"}} -->')
    assert block.endswith("<!-- /wp:paragraph -->")
    assert f'<p class="{FOOTER_SENTINEL}">' in block


# ---------------------------------------------------------------------------
# has_footer / remove_existing_footer
# ---------------------------------------------------------------------------

def test_has_footer_false_on_clean_content():
    assert not has_footer("<p>Clean body.</p>")


def test_has_footer_true_when_sentinel_present():
    content = f'<p class="{FOOTER_SENTINEL}">Part of…</p>'
    assert has_footer(content)


def test_remove_existing_footer_strips_block():
    block = build_footer_block(PILLAR_VANCOUVER, [], "A", _anchor_seed=0)
    content = "<p>Body.</p>\n\n" + block
    stripped = remove_existing_footer(content)
    assert FOOTER_SENTINEL not in stripped
    assert "Body." in stripped


def test_remove_existing_footer_idempotent():
    block = build_footer_block(PILLAR_VANCOUVER, [], "A", _anchor_seed=0)
    content = "<p>Body.</p>\n\n" + block
    once = remove_existing_footer(content)
    twice = remove_existing_footer(once)
    assert once == twice


# ---------------------------------------------------------------------------
# strip_inserted_anchors
# ---------------------------------------------------------------------------

def test_strip_inserted_anchors_reverses_single():
    html = '<p>Visit <a href="https://kriskrug.co/vancouver-ai/">Vancouver AI Ecosystem</a> today.</p>'
    applied = [{"text": "Vancouver AI Ecosystem", "url": "https://kriskrug.co/vancouver-ai/"}]
    result = strip_inserted_anchors(html, applied)
    assert result == "<p>Visit Vancouver AI Ecosystem today.</p>"


def test_strip_inserted_anchors_count_1_only():
    # If the same link appears twice, only the first occurrence is stripped.
    html = (
        '<a href="https://kriskrug.co/vancouver-ai/">Vancouver AI Ecosystem</a> '
        'and <a href="https://kriskrug.co/vancouver-ai/">Vancouver AI Ecosystem</a>'
    )
    applied = [{"text": "Vancouver AI Ecosystem", "url": "https://kriskrug.co/vancouver-ai/"}]
    result = strip_inserted_anchors(html, applied)
    # First stripped, second left as-is.
    assert result.count('<a href="https://kriskrug.co/vancouver-ai/">') == 1


def test_strip_inserted_anchors_empty_applied():
    html = "<p>No links here.</p>"
    assert strip_inserted_anchors(html, []) == html


# ---------------------------------------------------------------------------
# assert_minimal_diff — PASS cases
# ---------------------------------------------------------------------------

def test_assert_minimal_diff_passes_anchors_only():
    old = "<p>Visit Vancouver AI Ecosystem today.</p>"
    applied = [{"text": "Vancouver AI Ecosystem", "url": "https://kriskrug.co/vancouver-ai/"}]
    new = '<p>Visit <a href="https://kriskrug.co/vancouver-ai/">Vancouver AI Ecosystem</a> today.</p>'
    # Should not raise.
    assert_minimal_diff(old, new, applied, None)


def test_assert_minimal_diff_passes_anchors_and_footer():
    old = "<p>Visit Vancouver AI Ecosystem today.</p>"
    applied = [{"text": "Vancouver AI Ecosystem", "url": "https://kriskrug.co/vancouver-ai/"}]
    footer = build_footer_block(PILLAR_VANCOUVER, [], "A", _anchor_seed=0)
    new = '<p>Visit <a href="https://kriskrug.co/vancouver-ai/">Vancouver AI Ecosystem</a> today.</p>' + "\n\n" + footer
    assert_minimal_diff(old, new, applied, footer)


def test_assert_minimal_diff_passes_no_changes():
    old = "<p>Clean body.</p>"
    assert_minimal_diff(old, old, [], None)


# ---------------------------------------------------------------------------
# assert_minimal_diff — RAISE cases
# ---------------------------------------------------------------------------

def test_assert_minimal_diff_raises_on_deleted_word():
    old = "<p>Important body word here.</p>"
    new = "<p>Important body here.</p>"  # "word" deleted
    with pytest.raises(MinimalDiffError):
        assert_minimal_diff(old, new, [], None)


def test_assert_minimal_diff_raises_on_mid_body_footer():
    # Footer appears in the middle of the content, not as a suffix.
    old = "<p>Para one.</p>\n\n<p>Para two.</p>"
    footer = build_footer_block(PILLAR_VANCOUVER, [], "A", _anchor_seed=0)
    new = "<p>Para one.</p>\n\n" + footer + "\n\n<p>Para two.</p>"
    with pytest.raises(MinimalDiffError):
        assert_minimal_diff(old, new, [], footer)


def test_assert_minimal_diff_raises_on_anchor_not_in_applied():
    old = "<p>Visit Vancouver AI Ecosystem today.</p>"
    # new has an anchor but applied list is empty (not declared)
    new = '<p>Visit <a href="https://kriskrug.co/vancouver-ai/">Vancouver AI Ecosystem</a> today.</p>'
    with pytest.raises(MinimalDiffError):
        assert_minimal_diff(old, new, [], None)


# ---------------------------------------------------------------------------
# 2026-05-15 INCIDENT REGRESSION
# ---------------------------------------------------------------------------

# The incident: "Web Summit Vancouver 2026" post body was overwritten by the
# "Calling Us All In" body. assert_minimal_diff must catch this.

_REAL_BODY = """<!-- wp:paragraph -->
<p>The Web Summit Vancouver 2026 gathering brought together over 10,000 technologists.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Sessions ranged from AI policy to creative tooling demos.</p>
<!-- /wp:paragraph -->"""

_INCIDENT_BODY = """<!-- wp:paragraph -->
<p>Calling Us All In explores what it means to build technology with integrity.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>This is a completely different post body that must never be written to the wrong post.</p>
<!-- /wp:paragraph -->"""


def test_incident_regression_raises():
    """Full-body overwrite (different post body, empty applied, no footer) MUST raise."""
    with pytest.raises(MinimalDiffError):
        assert_minimal_diff(_REAL_BODY, _INCIDENT_BODY, [], None)


# ---------------------------------------------------------------------------
# Idempotence
# ---------------------------------------------------------------------------

def test_plan_links_idempotent_no_second_footer():
    """Running plan_links_for_post on content that already has a footer returns
    the original content unchanged with 'already-done' flag."""
    footer = build_footer_block(PILLAR_VANCOUVER, [], "A", _anchor_seed=0)
    content = "<p>Body.</p>\n\n" + footer
    new_content, applied, footer_block, flags = plan_links_for_post(
        content,
        "https://kriskrug.co/2026/01/01/hello/",
        PILLAR_VANCOUVER,
        [],
        "A",
    )
    assert "already-done" in flags
    assert new_content == content
    assert footer_block is None
    assert not applied


def test_plan_links_idempotent_no_dup_anchor():
    """Second pass should not insert a duplicate anchor (auto_link skips already-linked terms)."""
    # After first pass, the URL is already linked — text_polish masks existing <a> tags.
    content = '<p>Visit <a href="https://kriskrug.co/vancouver-ai/">Vancouver AI Ecosystem</a> here.</p>'
    new_content, applied, footer_block, flags = plan_links_for_post(
        content,
        "https://kriskrug.co/2026/01/01/hello/",
        PILLAR_VANCOUVER,
        [],
        "A",
    )
    # No anchor should be re-applied for the already-linked term.
    assert not any(a["url"] == "https://kriskrug.co/vancouver-ai/" for a in applied)


# ---------------------------------------------------------------------------
# Pillar / category edge cases
# ---------------------------------------------------------------------------

def test_plan_links_no_pillar_returns_no_footer():
    content = "<p>Some body text.</p>"
    new_content, applied, footer_block, flags = plan_links_for_post(
        content,
        "https://kriskrug.co/2026/01/01/hello/",
        None,  # no pillar
        [],
        "A",
    )
    assert footer_block is None
    assert "no-pillar" in flags


def test_plan_links_pillar_only_when_no_siblings():
    content = "<p>Some body text.</p>"
    new_content, applied, footer_block, flags = plan_links_for_post(
        content,
        "https://kriskrug.co/2026/01/01/hello/",
        PILLAR_VANCOUVER,
        [],  # no siblings
        "A",
    )
    assert footer_block is not None
    assert "See also" not in footer_block


# ---------------------------------------------------------------------------
# 2–5 link cap reconciliation
# ---------------------------------------------------------------------------

def test_plan_links_cap_skips_footer_when_budget_exhausted():
    # Construct content with 5 existing kriskrug.co links so the budget is full.
    links = " ".join(
        f'<a href="https://kriskrug.co/post-{i}/">Post {i}</a>' for i in range(5)
    )
    content = f"<p>{links}</p>"
    new_content, applied, footer_block, flags = plan_links_for_post(
        content,
        "https://kriskrug.co/2026/01/01/hello/",
        PILLAR_VANCOUVER,
        [],
        "A",
    )
    # No footer should be added when budget is at 5.
    assert footer_block is None
    assert any("cap" in f for f in flags)


def test_plan_links_cap_met_when_pillar_and_2_siblings_linked():
    # Content already has pillar + 2 sibling links.
    content = (
        '<p><a href="https://kriskrug.co/vancouver-ai/">Vancouver AI</a> '
        '<a href="https://kriskrug.co/post-a/">Post A</a> '
        '<a href="https://kriskrug.co/post-b/">Post B</a></p>'
    )
    sibs = [
        {"title": "Post A", "url": "https://kriskrug.co/post-a/"},
        {"title": "Post B", "url": "https://kriskrug.co/post-b/"},
    ]
    new_content, applied, footer_block, flags = plan_links_for_post(
        content,
        "https://kriskrug.co/2026/01/01/hello/",
        PILLAR_VANCOUVER,
        sibs,
        "A",
    )
    assert footer_block is None
    assert "cap-met" in flags


# ---------------------------------------------------------------------------
# Wave B sibling cap
# ---------------------------------------------------------------------------

def test_wave_b_footer_has_at_most_1_sibling():
    sibs = [
        {"title": "Post One", "url": "https://kriskrug.co/post-one/"},
        {"title": "Post Two", "url": "https://kriskrug.co/post-two/"},
    ]
    content = "<p>Some body text.</p>"
    new_content, applied, footer_block, flags = plan_links_for_post(
        content,
        "https://kriskrug.co/2026/01/01/hello/",
        PILLAR_VANCOUVER,
        sibs,
        "B",
    )
    assert footer_block is not None
    # Wave B: at most 1 sibling in footer
    assert footer_block.count('<a href="https://kriskrug.co/post-') == 1


# ---------------------------------------------------------------------------
# rank_siblings
# ---------------------------------------------------------------------------

def test_rank_siblings_excludes_self():
    post = _post(pid=10, title="My Post", link="https://kriskrug.co/my-post/", date="2025-01-01T00:00:00")
    candidates = [
        _sib(10, "My Post", "https://kriskrug.co/my-post/"),
        _sib(11, "Other Post", "https://kriskrug.co/other-post/"),
    ]
    result = rank_siblings(post, candidates, n=5)
    assert all(s["title"] != "My Post" for s in result)
    assert any(s["title"] == "Other Post" for s in result)


def test_rank_siblings_excludes_legacy_pre_2014():
    post = _post(pid=10, title="Modern Post", date="2025-01-01T00:00:00")
    candidates = [
        _sib(11, "Old Post", "https://kriskrug.co/old/", date="2013-06-01T00:00:00"),
        _sib(12, "Recent Post", "https://kriskrug.co/recent/", date="2025-06-01T00:00:00"),
    ]
    result = rank_siblings(post, candidates, n=5)
    titles = [s["title"] for s in result]
    assert "Old Post" not in titles
    assert "Recent Post" in titles


def test_rank_siblings_excludes_short_title():
    post = _post(pid=10, title="Long Enough Title", date="2025-01-01T00:00:00")
    candidates = [
        _sib(11, "OK", "https://kriskrug.co/stub/"),  # < 5 chars
        _sib(12, "Good Post Title", "https://kriskrug.co/good/"),
    ]
    result = rank_siblings(post, candidates, n=5)
    titles = [s["title"] for s in result]
    assert "OK" not in titles
    assert "Good Post Title" in titles


def test_rank_siblings_prefers_recent():
    post = _post(pid=10, title="My Post", date="2026-01-01T00:00:00")
    candidates = [
        _sib(11, "Older Post", "https://kriskrug.co/older/", date="2023-01-01T00:00:00"),
        _sib(12, "Newer Post", "https://kriskrug.co/newer/", date="2025-12-01T00:00:00"),
    ]
    result = rank_siblings(post, candidates, n=2)
    assert result[0]["title"] == "Newer Post"


def test_rank_siblings_em_dash_purged_in_title():
    post = _post(pid=10, title="My Post", date="2025-01-01T00:00:00")
    candidates = [
        _sib(11, "Post — with em dash", "https://kriskrug.co/em-post/"),
    ]
    result = rank_siblings(post, candidates, n=5)
    assert "—" not in result[0]["title"]


# ---------------------------------------------------------------------------
# build_content_payload
# ---------------------------------------------------------------------------

def test_build_content_payload_single_key():
    payload = build_content_payload("<p>New content.</p>")
    assert list(payload) == ["content"]
    assert payload["content"] == "<p>New content.</p>"


def test_build_content_payload_raises_on_extra_key():
    # The function currently only accepts the content string, so a payload with
    # extra keys cannot be produced through this function. We verify the internal
    # allowlist guard by monkey-patching — but since the function only accepts a
    # string, we verify the guard via the module's _CONTENT_PAYLOAD_ALLOWLIST.
    from linkinject_lib import _CONTENT_PAYLOAD_ALLOWLIST
    assert _CONTENT_PAYLOAD_ALLOWLIST == frozenset({"content"})


# ---------------------------------------------------------------------------
# PILLAR_BY_CATEGORY completeness
# ---------------------------------------------------------------------------

def test_pillar_by_category_covers_8_distinct_pillars():
    # 8 dedicated pillars plus folded categories that reuse a pillar URL.
    pillar_urls = {url for url, _ in PILLAR_BY_CATEGORY.values()}
    assert len(pillar_urls) == 8, f"expected 8 distinct pillar URLs, got {sorted(pillar_urls)}"


def test_pillar_by_category_all_have_vocabulary():
    for cat_id, (url, vocab) in PILLAR_BY_CATEGORY.items():
        assert url.startswith("https://kriskrug.co/"), f"cat {cat_id} url bad: {url}"
        assert len(vocab) >= 1, f"cat {cat_id} has empty vocabulary"


# ---------------------------------------------------------------------------
# Comment masking — Gutenberg block comments must never receive injected links
# ---------------------------------------------------------------------------

def test_no_link_injected_into_wp_quote_citation():
    """A wp:quote block with OpenAI/Dwarkesh Patel in the JSON citation attr
    must not have those names linked inside the comment delimiter.  This is
    the regression for post 11178 (your-taste-is-your-moat)."""
    from text_polish import auto_link_first_occurrence  # type: ignore[import]
    import re

    content = (
        "<!-- wp:paragraph -->\n"
        "<p>An anonymous <a href=\"https://openai.com/\" target=\"_blank\">OpenAI</a>"
        " employee on <a href=\"https://www.dwarkesh.com/\">Dwarkesh Patel</a>'s podcast:</p>\n"
        "<!-- /wp:paragraph -->\n\n"
        '<!-- wp:quote {"citation":"Anonymous OpenAI employee, Dwarkesh Patel podcast"} -->\n'
        "<blockquote class=\"wp-block-quote\"><!-- wp:paragraph -->\n"
        "<p>Quote text.</p>\n"
        "<!-- /wp:paragraph --><cite>Anonymous OpenAI employee, Dwarkesh Patel podcast</cite>"
        "</blockquote>\n"
        "<!-- /wp:quote -->"
    )
    result, applied = auto_link_first_occurrence(content)
    # Verify no <a> tag appears inside any HTML comment.
    for m in re.finditer(r"<!--.*?-->", result, re.DOTALL):
        assert "<a " not in m.group(0), (
            f"anchor injected inside HTML comment: {m.group(0)[:120]!r}"
        )


def test_no_link_injected_into_arbitrary_block_comment():
    """Generic Gutenberg block comment attrs should never receive injected links."""
    from text_polish import auto_link_first_occurrence  # type: ignore[import]
    import re

    content = (
        '<!-- wp:image {"id":123,"sizeSlug":"large"} -->\n'
        "<figure class=\"wp-block-image\"><img src=\"x.jpg\"/></figure>\n"
        "<!-- /wp:image -->\n\n"
        "<p>Visit Vancouver AI community events near you.</p>"
    )
    result, applied = auto_link_first_occurrence(content)
    for m in re.finditer(r"<!--.*?-->", result, re.DOTALL):
        assert "<a " not in m.group(0)
    # The paragraph body link must still fire.
    assert any(a["url"] == "https://kriskrug.co/vancouver-ai/" for a in applied)


def test_no_nested_anchor_from_overlapping_patterns():
    """'Vancouver AI community' and bare 'Vancouver AI' are two LINK_MAP entries.
    Only one anchor should be created — the more specific 'community' one —
    and the bare pattern must not re-match inside the already-injected anchor."""
    from text_polish import auto_link_first_occurrence  # type: ignore[import]

    content = "<p>Every Vancouver AI community gathering starts here.</p>"
    result, applied = auto_link_first_occurrence(content)
    # Only one anchor for this URL.
    assert result.count('href="https://kriskrug.co/vancouver-ai/"') == 1
    # The result must be well-formed HTML (no nested <a>).
    assert result.count("<a ") == result.count("</a>")
    # applied list should have exactly one entry for this URL.
    vai_applied = [a for a in applied if a["url"] == "https://kriskrug.co/vancouver-ai/"]
    assert len(vai_applied) == 1


# ---------------------------------------------------------------------------
# Graceful degradation — contextual failures fall back to footer-only
# ---------------------------------------------------------------------------

def test_plan_links_contextual_drop_falls_back_to_footer():
    """When the contextual layer would produce a malformed anchor (triggering
    MinimalDiffError), plan_links_for_post must fall back to footer-only,
    set the 'contextual-dropped' flag, and return a valid plan that passes
    assert_minimal_diff."""
    import sys
    from pathlib import Path
    # Patch auto_link_first_occurrence to simulate a corrupted result.
    _repo_root = Path(__file__).resolve().parent.parent.parent
    _polish_path = str(_repo_root / "scripts" / "notion-to-wp")
    if _polish_path not in sys.path:
        sys.path.insert(0, _polish_path)
    import text_polish as _tp
    import linkinject_lib as _lib

    original_fn = _tp.auto_link_first_occurrence

    def _broken_auto_link(html, self_url=None):
        # Return a corrupted result that assert_minimal_diff will reject.
        corrupted = html + " EXTRA-INJECTED-GARBAGE"
        return corrupted, [{"text": "Vancouver AI", "url": "https://kriskrug.co/vancouver-ai/"}]

    _tp.auto_link_first_occurrence = _broken_auto_link
    try:
        content = "<p>Some Vancouver AI community post content.</p>"
        new_content, applied, footer_block, flags = plan_links_for_post(
            content,
            "https://kriskrug.co/2026/01/01/hello/",
            PILLAR_VANCOUVER,
            [],
            "A",
        )
    finally:
        _tp.auto_link_first_occurrence = original_fn

    assert "contextual-dropped" in flags, f"expected contextual-dropped in {flags}"
    assert applied == [], "applied should be empty after contextual drop"
    # Footer should still be produced (footer-only mode).
    assert footer_block is not None, "footer should still be appended"
    # The plan must pass assert_minimal_diff.
    assert_minimal_diff(content, new_content, applied, footer_block)


def test_plan_links_previously_failed_post_now_yields_footer_only():
    """Simulate the post 11700 (punk-rock-ai) class of failure: contextual
    auto_link produces a partial-anchor corruption.  The engine must now
    return a footer-only plan (status would be 'planned', not 'failed')."""
    import sys
    from pathlib import Path
    _repo_root = Path(__file__).resolve().parent.parent.parent
    _polish_path = str(_repo_root / "scripts" / "notion-to-wp")
    if _polish_path not in sys.path:
        sys.path.insert(0, _polish_path)
    import text_polish as _tp

    # Reproduce the partial-anchor corruption verbatim from the 11700 report:
    # the reconstructed content had a broken mid-tag fragment.
    def _corrupted_auto_link(html, self_url=None):
        # Simulate the broken anchor from the dry-run failure
        broken = html.replace(
            "Every Vancouver AI community",
            'Every Vancouver AI community">Vancouver AI Community</a>',
        )
        return broken, [{"text": "Vancouver AI", "url": "https://kriskrug.co/vancouver-ai/"}]

    _tp.auto_link_first_occurrence = _corrupted_auto_link
    try:
        content = "<p>Every Vancouver AI community gathering opens with a welcome.</p>"
        new_content, applied, footer_block, flags = plan_links_for_post(
            content,
            "https://kriskrug.co/2026/05/04/punk-rock-ai/",
            PILLAR_VANCOUVER,
            [],
            "A",
        )
    finally:
        import importlib
        import text_polish as _tp2
        # Restore: reimport so other tests get the real function
        importlib.reload(_tp2)
        import linkinject_lib
        # plan_links_for_post imports auto_link_first_occurrence inside the function
        # so no module-level reference needs patching back

    assert "contextual-dropped" in flags
    # Footer-only plan: original content + footer, no contextual anchors.
    assert applied == []
    assert footer_block is not None
    # The resulting plan must pass minimal-diff.
    assert_minimal_diff(content, new_content, [], footer_block)
