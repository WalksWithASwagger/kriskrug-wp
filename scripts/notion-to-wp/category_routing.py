from __future__ import annotations


TYPE_TO_CATEGORY = {
    "Report": "Vancouver AI Ecosystem",
    "Manifesto": "AI Ethics & Philosophy",
    "Interview": "Conversations & Interviews",
    "Tutorial": "AI for Creatives",
    "Field Note": "Field Notes",
}

CATEGORY_REVIEW_REQUIRED = "NEEDS CATEGORY REVIEW"

FEATURE_CATEGORY_TAG_HINTS = (
    ("Vancouver AI Ecosystem", (
        "bc + ai",
        "comox",
        "community spotlight",
        "industry",
        "recap",
        "vancouver ai",
        "web summit",
    )),
    ("AI Ethics & Philosophy", (
        "ai ethics",
        "certification",
        "responsible ai",
        "sovereign ai",
        "values",
    )),
    ("AI for Creatives", (
        "artist",
        "creative",
        "creatives",
        "tools",
        "workflow",
    )),
    ("Conversations & Interviews", (
        "appearance",
        "interview",
        "media",
        "podcast",
    )),
)


def resolve_category(
    type_notion: str,
    tags_notion: list[str],
    category_override: str | None = None,
) -> tuple[str, str]:
    override = (category_override or "").strip()
    if override:
        return override, "override"

    notion_type = (type_notion or "").strip()
    if notion_type in TYPE_TO_CATEGORY:
        return TYPE_TO_CATEGORY[notion_type], f"type:{notion_type}"

    if notion_type.lower() == "feature":
        tags_text = " ".join(str(tag).lower() for tag in (tags_notion or []))
        for category, hints in FEATURE_CATEGORY_TAG_HINTS:
            if any(hint in tags_text for hint in hints):
                return category, "feature-tags"
        return CATEGORY_REVIEW_REQUIRED, "feature-needs-category"

    return "Misc", "fallback"


def category_requires_review(category_name: str) -> bool:
    return category_name == CATEGORY_REVIEW_REQUIRED
