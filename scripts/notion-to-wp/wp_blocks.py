"""Canonical Gutenberg block markup for kriskrug.co (kk-aurora theme).

ONE place every notion-to-wp script emits in-body blocks from, so we stop
reinventing the markup per script. Replaces the old image_blocks.py and the
copy-pasted image/gallery/heading/separator/pullquote strings.

kk-aurora facts that shape these helpers:
- Prose column is 720px. A small inline image must set an explicit width well
  under 720 (inline_image defaults to 460); a hero fills the column (width=None).
- The theme has NO float CSS (.alignleft/.alignright do not wrap text), so the
  supported inline placement is centered. `align` is a param but defaults center.
- The theme supports the native WP 6.4+ lightbox (theme.json core/image.lightbox).
  Click-to-zoom is enabled per image via "lightbox":{"enabled":true} with NO <a>
  wrapper. See theme/kk-aurora/patterns/photo-gallery.php.

Escaping: callers pass ready strings. wp_blocks does NOT escape (text helpers and
block_rules already produce safe HTML; the publish scripts pass controlled copy).
"""
from __future__ import annotations

import re

_SEPARATOR = ('<!-- wp:separator -->\n'
              '<hr class="wp-block-separator has-alpha-channel-opacity"/>\n'
              '<!-- /wp:separator -->')


def inline(s: str) -> str:
    """Markdown-ish inline formatting -> HTML. Links, bold, italic. External
    links get target=_blank rel=noopener noreferrer; kriskrug.co/internal stay clean."""
    def link(m: re.Match) -> str:
        text, url = m.group(1), m.group(2)
        extra = '' if url.startswith(("https://kriskrug.co", "/")) else ' target="_blank" rel="noopener noreferrer"'
        return f'<a href="{url}"{extra}>{text}</a>'
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    return s


def separator() -> str:
    return _SEPARATOR


def heading(text: str, level: int = 2) -> str:
    """Canonical core heading. text is ready HTML. Omits the level attr for the
    default h2 (matches Gutenberg); always sets the wp-block-heading class."""
    attr = "" if level == 2 else f' {{"level":{level}}}'
    return (f'<!-- wp:heading{attr} -->\n'
            f'<h{level} class="wp-block-heading">{text}</h{level}>\n'
            f'<!-- /wp:heading -->')


def pullquote(text: str) -> str:
    """Callout-style pullquote (deck). text is ready HTML."""
    return ('<!-- wp:pullquote -->\n'
            f'<figure class="wp-block-pullquote"><blockquote><p>{text}</p></blockquote></figure>\n'
            '<!-- /wp:pullquote -->')


def image(media_id, url, alt, *, caption=None, width=None, align="center",
          lightbox=True, size_slug="large") -> str:
    """Core image block. media_id may be int (emits "id":N + wp-image-N class),
    the string "TBD" (dry-run: class only, no id), or None (no id, no wp-image class).
    lightbox=True -> native click-to-zoom, no <a> wrapper; lightbox=False ->
    linkDestination none (plain). width in px constrains + adds is-resized."""
    attrs = []
    if isinstance(media_id, int):
        attrs.append(f'"id":{media_id}')
    if width:
        attrs.append(f'"width":"{width}px"')
    if size_slug:
        attrs.append(f'"sizeSlug":"{size_slug}"')
    attrs.append('"lightbox":{"enabled":true}' if lightbox else '"linkDestination":"none"')
    if align:
        attrs.append(f'"align":"{align}"')

    figcls = "wp-block-image"
    if align:
        figcls += f" align{align}"
    if size_slug:
        figcls += f" size-{size_slug}"
    style = ""
    if width:
        figcls += " is-resized"
        style = f' style="width:{width}px"'

    cls = f' class="wp-image-{media_id}"' if media_id is not None else ""
    img = f'<img src="{url}" alt="{alt}"{cls}{style}/>'
    cap = f'<figcaption class="wp-element-caption">{caption}</figcaption>' if caption else ""
    return (f'<!-- wp:image {{{",".join(attrs)}}} -->\n'
            f'<figure class="{figcls}">{img}{cap}</figure>\n<!-- /wp:image -->')


def inline_image(media_id, url, alt, caption=None, width=460, align="center") -> str:
    """Small, centered, click-to-zoom in-body image (screenshots / receipts).
    Default 460px (~64% of the 720px prose column)."""
    return image(media_id, url, alt, caption=caption, width=width, align=align)


def hero_image(media_id, url, alt, caption=None, align="center") -> str:
    """Full-width section hero (e.g. posters); fills the column, click-to-zoom on."""
    return image(media_id, url, alt, caption=caption, width=None, align=align)


def gallery(items, columns: int = 3) -> str:
    """wp:gallery of click-to-zoom images. items: (id, url, alt[, caption])."""
    inner = "\n".join(
        image(it[0], it[1], it[2],
              caption=(it[3] if len(it) > 3 and it[3] else None),
              width=None, align=None, lightbox=True)
        for it in items
    )
    return (f'<!-- wp:gallery {{"columns":{columns},"imageCrop":false}} -->\n'
            f'<figure class="wp-block-gallery has-nested-images columns-{columns}">\n'
            f'{inner}\n</figure>\n<!-- /wp:gallery -->')
