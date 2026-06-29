"""
Notion block → Gutenberg block converters for kriskrug.co.

Each function takes a Notion block dict (Notion API response shape) and returns
a string of WP Gutenberg-block HTML. Functions are pure — no I/O, no globals
except a small image-URL rewrite map passed in by the caller.

Block types covered:
    paragraph, heading_1/2/3, bulleted_list_item, numbered_list_item,
    quote, callout, divider, code, image, bookmark, embed, toggle,
    column_list, column, to_do.

Inline rich text formatting preserved:
    bold, italic, underline, strikethrough, code, link, color (yellow → <mark>).

If a block type isn't recognized, render_block emits an HTML comment so the
unrendered block is visible in source but doesn't break the page.
"""

from __future__ import annotations
from html import escape
from typing import Callable

import wp_blocks


# ---------------------------------------------------------------------------
# Inline rich-text rendering.
# ---------------------------------------------------------------------------

def render_rich_text(rts: list) -> str:
    """Convert Notion rich_text array to inline HTML."""
    out = []
    for rt in rts or []:
        out.append(_render_one_rich_text(rt))
    return "".join(out)


def _render_one_rich_text(rt: dict) -> str:
    plain = rt.get("plain_text", "")
    if not plain:
        return ""
    text = escape(plain)
    ann = rt.get("annotations", {}) or {}

    # Yellow highlight → semantic <mark>. Theme CSS can style it.
    color = ann.get("color", "default")
    if color == "yellow" or color == "yellow_background":
        text = f"<mark>{text}</mark>"

    if ann.get("code"):
        text = f"<code>{text}</code>"
    if ann.get("bold"):
        text = f"<strong>{text}</strong>"
    if ann.get("italic"):
        text = f"<em>{text}</em>"
    if ann.get("underline"):
        text = f"<u>{text}</u>"
    if ann.get("strikethrough"):
        text = f"<s>{text}</s>"

    href = rt.get("href")
    if href:
        rel = _link_rel(href)
        target = ' target="_blank"' if rel else ""
        rel_attr = f' rel="{rel}"' if rel else ""
        text = f'<a href="{escape(href, quote=True)}"{rel_attr}{target}>{text}</a>'
    return text


def _link_rel(href: str) -> str:
    """External links get rel='noopener noreferrer'; internal kriskrug.co links stay clean."""
    if href.startswith("/") or "kriskrug.co" in href:
        return ""
    return "noopener noreferrer"


# ---------------------------------------------------------------------------
# Block-level renderers. Each returns Gutenberg-flavoured HTML.
# ---------------------------------------------------------------------------

def render_paragraph(block: dict, _ctx: dict | None = None) -> str:
    txt = render_rich_text(block["paragraph"]["rich_text"])
    if not txt.strip():
        return ""  # skip empty paragraphs (Notion sometimes emits these)
    return f'<!-- wp:paragraph -->\n<p>{txt}</p>\n<!-- /wp:paragraph -->'


def render_heading(block: dict, level: int, _ctx: dict | None = None) -> str:
    txt = render_rich_text(block[f"heading_{level}"]["rich_text"])
    # Page H1 is the title; first body heading should be H2.
    # Notion h1 → WP h2, h2 → h2, h3 → h3.
    wp_level = 2 if level == 1 else (2 if level == 2 else 3)
    return wp_blocks.heading(txt, wp_level)


def render_heading_1(block, ctx=None): return render_heading(block, 1, ctx)
def render_heading_2(block, ctx=None): return render_heading(block, 2, ctx)
def render_heading_3(block, ctx=None): return render_heading(block, 3, ctx)


def render_bulleted_list_item(block: dict, _ctx: dict | None = None) -> str:
    # Notion gives each list item as a standalone block; we batch in render_blocks.
    return _LIST_ITEM_SENTINEL + render_rich_text(block["bulleted_list_item"]["rich_text"])


def render_numbered_list_item(block: dict, _ctx: dict | None = None) -> str:
    return _OLIST_ITEM_SENTINEL + render_rich_text(block["numbered_list_item"]["rich_text"])


def render_quote(block: dict, _ctx: dict | None = None) -> str:
    txt = render_rich_text(block["quote"]["rich_text"])
    return (
        '<!-- wp:quote -->\n'
        f'<blockquote class="wp-block-quote"><p>{txt}</p></blockquote>\n'
        '<!-- /wp:quote -->'
    )


def render_callout(block: dict, ctx: dict | None = None) -> str:
    c = block["callout"]
    color = c.get("color", "default")  # gray_background, blue_background, etc.
    style_class = _callout_style_class(color)
    icon_html = _callout_icon_html(c.get("icon"))
    txt = render_rich_text(c["rich_text"])

    # Render any nested child blocks (Notion callouts can contain headings,
    # additional paragraphs, lists, images, etc.).
    children = block.get("_children") or []
    children_html = render_blocks(children, ctx=ctx) if children else ""

    pieces = []
    if icon_html:
        pieces.append(icon_html)
    if txt.strip():
        pieces.append(f"<p>{txt}</p>")
    if children_html:
        pieces.append(children_html)
    inner = "".join(pieces) or "<p></p>"
    return (
        f'<!-- wp:quote {{"className":"{style_class}"}} -->\n'
        f'<blockquote class="wp-block-quote {style_class}">{inner}</blockquote>\n'
        f'<!-- /wp:quote -->'
    )


def _callout_style_class(notion_color: str) -> str:
    """Map Notion callout colours to CSS classes the theme can style."""
    mapping = {
        "green_background": "is-style-callout-green",
        "blue_background":  "is-style-callout-blue",
        "yellow_background":"is-style-callout-yellow",
        "red_background":   "is-style-callout-red",
        "gray_background":  "is-style-callout-gray",
        "orange_background":"is-style-callout-orange",
        "pink_background":  "is-style-callout-pink",
        "purple_background":"is-style-callout-purple",
        "brown_background": "is-style-callout-brown",
    }
    return mapping.get(notion_color, "is-style-callout")


def _callout_icon_html(icon: dict | None) -> str:
    if not icon:
        return ""
    if icon.get("type") == "emoji":
        return f'<span class="callout-icon" aria-hidden="true">{escape(icon.get("emoji", ""))}</span>'
    # Custom emojis & external icons skipped — would require asset hosting.
    return ""


def render_divider(_block: dict, _ctx: dict | None = None) -> str:
    return wp_blocks.separator()


def render_code(block: dict, _ctx: dict | None = None) -> str:
    c = block["code"]
    lang = c.get("language", "plaintext")
    txt = escape("".join(rt.get("plain_text", "") for rt in c.get("rich_text", [])))
    return (
        '<!-- wp:code -->\n'
        f'<pre class="wp-block-code"><code class="language-{escape(lang, quote=True)}">{txt}</code></pre>\n'
        '<!-- /wp:code -->'
    )


def render_image(block: dict, ctx: dict | None = None) -> str:
    """
    Render an image block.

    ctx['image_map'] maps Notion file URLs → {'url': wp_media_url, 'id': wp_media_id, 'alt': alt_text}.
    If not in the map (dry-run, image not yet uploaded), emit a placeholder with alt + comment.
    """
    img = block["image"]
    src_obj = img.get("file") or img.get("external") or {}
    notion_url = src_obj.get("url", "")
    caption_rts = img.get("caption", [])
    caption_text = render_rich_text(caption_rts)

    image_map = (ctx or {}).get("image_map", {})
    entry = image_map.get(notion_url) or image_map.get(_normalize_notion_url(notion_url))
    if entry:
        wp_url = entry["url"]
        wp_id = entry["id"]
        alt = escape(entry.get("alt", caption_text or ""), quote=True)
    else:
        wp_url = notion_url  # placeholder; expires
        wp_id = "TBD"
        alt = escape(caption_text or "", quote=True)

    return wp_blocks.image(
        wp_id, escape(wp_url, quote=True), alt,
        caption=caption_text or None, width=None, align=None, lightbox=True,
    )


def _normalize_notion_url(url: str) -> str:
    """Strip query/signature so the same Notion image can be matched across runs."""
    return url.split("?")[0] if url else ""


def render_bookmark(block: dict, _ctx: dict | None = None) -> str:
    url = block.get("bookmark", {}).get("url", "")
    if not url:
        return ""
    rel = _link_rel(url)
    rel_attr = f' rel="{rel}"' if rel else ""
    target = ' target="_blank"' if rel else ""
    return (
        '<!-- wp:paragraph {"className":"is-style-bookmark"} -->\n'
        f'<p class="is-style-bookmark">'
        f'<a href="{escape(url, quote=True)}"{rel_attr}{target}>{escape(url)}</a>'
        '</p>\n<!-- /wp:paragraph -->'
    )


def render_embed(block: dict, _ctx: dict | None = None) -> str:
    # Catch Responsive doesn't ship great embed blocks; fall back to a link paragraph.
    url = block.get("embed", {}).get("url", "")
    if not url:
        return ""
    rel = _link_rel(url)
    rel_attr = f' rel="{rel}"' if rel else ""
    target = ' target="_blank"' if rel else ""
    return (
        '<!-- wp:paragraph -->\n'
        f'<p><a href="{escape(url, quote=True)}"{rel_attr}{target}>{escape(url)}</a></p>\n'
        '<!-- /wp:paragraph -->'
    )


def render_toggle(block: dict, ctx: dict | None = None) -> str:
    summary = render_rich_text(block["toggle"]["rich_text"])
    children = block.get("_children") or []
    children_html = render_blocks(children, ctx=ctx) if children else ""
    return (
        '<!-- wp:details -->\n'
        f'<details class="wp-block-details"><summary>{summary}</summary>{children_html}</details>\n'
        '<!-- /wp:details -->'
    )


def render_to_do(block: dict, _ctx: dict | None = None) -> str:
    td = block["to_do"]
    checked = td.get("checked", False)
    txt = render_rich_text(td["rich_text"])
    box = "☑" if checked else "☐"
    return (
        '<!-- wp:paragraph {"className":"is-style-todo"} -->\n'
        f'<p class="is-style-todo">{box} {txt}</p>\n'
        '<!-- /wp:paragraph -->'
    )


# Sentinel markers used during list-item batching in render_blocks().
_LIST_ITEM_SENTINEL  = "\x00LISTITEM\x00"
_OLIST_ITEM_SENTINEL = "\x00OLISTITEM\x00"


REGISTRY: dict[str, Callable] = {
    "paragraph":            render_paragraph,
    "heading_1":            render_heading_1,
    "heading_2":            render_heading_2,
    "heading_3":            render_heading_3,
    "bulleted_list_item":   render_bulleted_list_item,
    "numbered_list_item":   render_numbered_list_item,
    "quote":                render_quote,
    "callout":              render_callout,
    "divider":              render_divider,
    "code":                 render_code,
    "image":                render_image,
    "bookmark":             render_bookmark,
    "embed":                render_embed,
    "toggle":               render_toggle,
    "to_do":                render_to_do,
    # column_list/column flattened: caller will pass through child blocks.
}


def render_blocks(blocks: list, ctx: dict | None = None) -> str:
    """Render a flat list of Notion blocks into Gutenberg HTML.
    Adjacent list items are batched into a single <ul>/<ol>."""
    out = []
    pending_ul: list[str] = []
    pending_ol: list[str] = []

    def flush_lists():
        if pending_ul:
            items = "".join(f"<li>{i}</li>" for i in pending_ul)
            out.append(f'<!-- wp:list -->\n<ul class="wp-block-list">{items}</ul>\n<!-- /wp:list -->')
            pending_ul.clear()
        if pending_ol:
            items = "".join(f"<li>{i}</li>" for i in pending_ol)
            out.append(f'<!-- wp:list {{"ordered":true}} -->\n<ol class="wp-block-list">{items}</ol>\n<!-- /wp:list -->')
            pending_ol.clear()

    for b in blocks:
        btype = b.get("type", "")
        renderer = REGISTRY.get(btype)
        if renderer is None:
            flush_lists()
            out.append(f"<!-- skipped unsupported block: {escape(btype)} -->")
            continue

        rendered = renderer(b, ctx)
        if not rendered:
            continue

        if rendered.startswith(_LIST_ITEM_SENTINEL):
            pending_ul.append(rendered[len(_LIST_ITEM_SENTINEL):])
            if pending_ol:
                flush_lists()  # only ul or ol queued at a time
            continue
        if rendered.startswith(_OLIST_ITEM_SENTINEL):
            pending_ol.append(rendered[len(_OLIST_ITEM_SENTINEL):])
            if pending_ul:
                flush_lists()
            continue

        flush_lists()
        out.append(rendered)

    flush_lists()
    return "\n\n".join(out)
