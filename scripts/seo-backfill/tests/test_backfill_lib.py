"""Unit tests for backfill_lib — pure, no network."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backfill_lib import (  # noqa: E402
    ALLOWED_META_KEYS,
    build_meta_payload,
    derive_meta_description,
    derive_seo_title,
    parse_approved_entry,
    plan_meta_for_item,
    reconcile_with_fresh_meta,
    title_text,
)


def item(meta=None, title="Hello World", excerpt="", content=""):
    return {
        "id": 1,
        "slug": "hello-world",
        "title": {"raw": title, "rendered": title},
        "meta": meta or {},
        "excerpt": {"rendered": excerpt},
        "content": {"rendered": content},
    }


# --- additive-only: never touch non-empty fields ---

def test_plan_skips_already_set_fields():
    it = item(meta={
        "jetpack_seo_html_title": "Existing | Kris Krüg",
        "advanced_seo_description": "Already has a description here.",
        "jetpack_publicize_message": "already social",
    }, excerpt="An excerpt.")
    plan = plan_meta_for_item(it, "post")
    assert plan.is_empty
    assert "nothing empty" in plan.note


def test_plan_fills_only_empty_fields():
    it = item(meta={"jetpack_seo_html_title": "Set | Kris Krüg"}, excerpt="A real authored excerpt.")
    plan = plan_meta_for_item(it, "post")
    assert "jetpack_seo_html_title" not in plan.planned  # already set -> untouched
    assert plan.planned["advanced_seo_description"] == "A real authored excerpt."
    assert plan.planned["jetpack_publicize_message"] == "A real authored excerpt."


def test_whitespace_only_counts_as_empty():
    it = item(meta={"advanced_seo_description": "   "}, excerpt="Fill me.")
    plan = plan_meta_for_item(it, "post")
    assert plan.planned["advanced_seo_description"] == "Fill me."


# --- derivation ---

def test_seo_title_suffix_when_fits():
    assert derive_seo_title("Short") == "Short | Kris Krüg"


def test_seo_title_truncates_when_too_long():
    long = "x" * 80
    assert derive_seo_title(long) == "x" * 60
    assert not derive_seo_title(long).endswith("Kris Krüg")


def test_meta_desc_prefers_excerpt():
    desc, source = derive_meta_description(item(excerpt="The excerpt.", content="<p>Body paragraph here.</p>"))
    assert desc == "The excerpt."
    assert source == "excerpt"


def test_meta_desc_falls_back_to_first_real_paragraph():
    it = item(excerpt="", content="<h2>Heading</h2><p>This is the first substantial paragraph of the body.</p>")
    desc, source = derive_meta_description(it)
    assert source == "first_paragraph"
    assert "first substantial paragraph" in desc


def test_meta_desc_none_when_no_source():
    desc, source = derive_meta_description(item(excerpt="", content="<h2>Just a heading</h2>"))
    assert desc == ""
    assert source == "none"


def test_first_paragraph_fallback_is_flagged():
    it = item(excerpt="", content="<p>" + "A long enough body paragraph to qualify as a description. " * 2 + "</p>")
    plan = plan_meta_for_item(it, "post")
    assert "desc:first-paragraph-fallback" in plan.flags


def test_seo_title_backfilled_when_suffix_fits():
    plan = plan_meta_for_item(item(meta={}, title="Short Title", excerpt="x"), "post")
    assert plan.planned["jetpack_seo_html_title"] == "Short Title | Kris Krüg"


def test_seo_title_skipped_when_too_long_to_brand():
    # A long title would truncate; empty already falls back to full title in WP,
    # so we must NOT write a worse, truncated value.
    long_title = "A Very Long Title That Cannot Possibly Fit The Branding Suffix Within Sixty Chars"
    plan = plan_meta_for_item(item(meta={}, title=long_title, excerpt="x"), "post")
    assert "jetpack_seo_html_title" not in plan.planned
    assert "seo_title:skipped-too-long" in plan.flags


def test_social_only_for_posts_not_pages():
    it = item(excerpt="Excerpt text.")
    assert "jetpack_publicize_message" in plan_meta_for_item(it, "post").planned
    assert "jetpack_publicize_message" not in plan_meta_for_item(it, "page").planned


def test_title_text_prefers_raw():
    assert title_text({"title": {"raw": "Raw & Co", "rendered": "Raw &amp; Co"}}) == "Raw & Co"


# --- the hard allowlist guarantee ---

def test_build_payload_is_meta_only():
    payload = build_meta_payload({"jetpack_seo_html_title": "x"})
    assert list(payload) == ["meta"]


def test_build_payload_rejects_non_allowlisted_key():
    with pytest.raises(ValueError, match="non-allowlisted"):
        build_meta_payload({"title": "HACK", "jetpack_seo_html_title": "x"})


def test_build_payload_rejects_empty():
    with pytest.raises(ValueError, match="empty plan"):
        build_meta_payload({})


def test_allowlist_is_exactly_the_three_keys():
    assert ALLOWED_META_KEYS == {
        "jetpack_seo_html_title",
        "advanced_seo_description",
        "jetpack_publicize_message",
    }


def test_reconcile_preserves_derived_values_not_in_fresh_meta():
    # Regression: the pre-write readback omits excerpt/content, so we must keep
    # the values derived from the original item — never drop desc/social just
    # because they aren't re-derivable from the readback.
    planned = {
        "jetpack_seo_html_title": "T | Kris Krüg",
        "advanced_seo_description": "A real description.",
        "jetpack_publicize_message": "A real social message.",
    }
    fresh_meta = {}  # nothing filled since enumeration
    result = reconcile_with_fresh_meta(planned, fresh_meta)
    assert result == planned  # all three survive


def test_reconcile_drops_keys_filled_since_enumeration():
    planned = {"advanced_seo_description": "x", "jetpack_publicize_message": "y"}
    fresh_meta = {"advanced_seo_description": "someone set this already"}
    result = reconcile_with_fresh_meta(planned, fresh_meta)
    assert result == {"jetpack_publicize_message": "y"}


def test_parse_approved_entry_valid():
    pid, slug, meta = parse_approved_entry({
        "id": 42, "slug": "hello", "meta": {"advanced_seo_description": "A crafted description."}
    })
    assert pid == 42 and slug == "hello"
    assert meta == {"advanced_seo_description": "A crafted description."}


def test_parse_approved_entry_requires_slug_guard():
    with pytest.raises(ValueError, match="slug"):
        parse_approved_entry({"id": 42, "meta": {"advanced_seo_description": "x"}})


def test_parse_approved_entry_rejects_non_allowlisted():
    with pytest.raises(ValueError, match="non-allowlisted"):
        parse_approved_entry({"id": 42, "slug": "h", "meta": {"content": "HACK"}})


def test_parse_approved_entry_rejects_empty_value():
    with pytest.raises(ValueError, match="empty"):
        parse_approved_entry({"id": 42, "slug": "h", "meta": {"advanced_seo_description": "  "}})


def test_fields_filter_limits_scope():
    it = item(excerpt="Excerpt.")
    plan = plan_meta_for_item(it, "post", fields=("seo_title",))
    assert set(plan.planned) == {"jetpack_seo_html_title"}
