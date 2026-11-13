"""Keep text sent to kriskrug.co storable in its database.

The posts and postmeta tables use MySQL's "latin1", which is really Windows-1252
(cp1252): ISO-8859-1 plus curly quotes, en and em dashes, the ellipsis, the
bullet, the euro and trademark signs and a few more. The edit-context snapshots
under backup/ hold those raw in title, content, excerpt and meta fields, and no
other character above U+00FF. Anything outside cp1252 sent raw is stored as "?"
(#606, #1225).

Fields WordPress keeps as HTML (post title, content and excerpt, media alt text,
caption and description, term names) carry such characters as numeric character
references, which render identically. Plain-text meta (Jetpack's SEO title and
description, the Publicize message) cannot: a reference would show literally,
and combining marks in the SEO fields make the REST write fail with HTTP 500.
Meta a writer derives itself is folded to plain letters (derived_meta_text);
meta the operator wrote is refused (plain_meta_text).

No dependencies beyond the standard library, so the marquee and events writers
can import this without pulling in requests.
"""
from __future__ import annotations

import re
import unicodedata
from typing import Callable

DB_CODEC = "cp1252"

# Latin letters NFKD cannot split into base letter plus accent. WordPress's
# remove_accents() folds them the same way.
UNDECOMPOSABLE_LATIN = str.maketrans({
    "Ø": "O", "ø": "o", "Æ": "AE", "æ": "ae", "ß": "ss", "Đ": "D", "đ": "d",
    "Ð": "D", "ð": "d", "Ł": "L", "ł": "l", "Þ": "TH", "þ": "th", "Œ": "OE",
    "œ": "oe",
})

HTML_TEXT_FIELDS = frozenset(
    {"title", "content", "excerpt", "alt_text", "caption", "description", "name"}
)

# Browsers do not decode character references inside these elements.
_RAW_TEXT_ELEMENT = re.compile(
    r"(<(style|script)\b[^>]*>)(.*?)(?=</\2\s*>|\Z)", re.IGNORECASE | re.DOTALL
)
_RAW_TEXT_ESCAPE = {"style": "a CSS escape such as \\2192", "script": "a JavaScript escape such as \\u2192"}


class UnstorableText(ValueError):
    pass


def is_storable(ch: str) -> bool:
    """True when the database keeps `ch` as sent.

    Python's cp1252 codec has no mapping for the C1 controls U+0080 to U+009F,
    including the five bytes cp1252 leaves undefined (0x81, 0x8D, 0x8F, 0x90,
    0x9D), so none of them counts as storable.
    """
    try:
        ch.encode(DB_CODEC)
    except UnicodeEncodeError:
        return False
    return True


def fold_latin(text: str) -> str:
    """Latin letters folded to their base letters, as WordPress's remove_accents() does.

    "Krüg" becomes "Krug" and "Łódź" becomes "Lodz". Slugs go through this so
    they match the slug WordPress stores (#1257).
    """
    text = unicodedata.normalize("NFKD", text.translate(UNDECOMPOSABLE_LATIN))
    return "".join(ch for ch in text if not unicodedata.combining(ch))


def _unstorable(text: str) -> list[str]:
    return [ch for ch in dict.fromkeys(text) if not is_storable(ch)]


def _describe(chars: list[str]) -> str:
    return ", ".join(f"U+{ord(ch):04X} {unicodedata.name(ch, 'UNNAMED')}" for ch in chars)


def to_ncr(text: str) -> str:
    """Replace each character outside cp1252 with a decimal numeric reference.

    cp1252 text and existing entities pass through untouched, so running it twice
    changes nothing. A C1 control raises instead: browsers read &#128; to &#159;
    as cp1252 punctuation, so it has no faithful reference.
    """
    controls = [ch for ch in dict.fromkeys(text) if 0x80 <= ord(ch) <= 0x9F]
    if controls:
        raise UnstorableText(
            f"text has C1 control characters, usually a sign of mis-decoded "
            f"cp1252: {_describe(controls)}. Fix the source text."
        )
    return text.encode(DB_CODEC, "xmlcharrefreplace").decode(DB_CODEC)


def encode_html(text: str) -> str:
    """to_ncr for HTML, leaving <style> and <script> bodies as written.

    Raises UnstorableText when such a body holds a character outside cp1252,
    since a reference there would reach the CSS or JavaScript literally.
    """
    parts: list[str] = []
    pos = 0
    for match in _RAW_TEXT_ELEMENT.finditer(text):
        parts.append(to_ncr(text[pos:match.start(3)]))
        body, element = match.group(3), match.group(2).lower()
        bad = _unstorable(body)
        if bad:
            raise UnstorableText(
                f"<{element}> holds characters the database cannot store and a "
                f"character reference cannot stand in for there: {_describe(bad)}. "
                f"Use {_RAW_TEXT_ESCAPE[element]} instead."
            )
        parts.append(body)
        pos = match.end(3)
    parts.append(to_ncr(text[pos:]))
    return "".join(parts)


def plain_meta_text(text: str, field: str) -> str:
    """Return `text` composed (NFC) for a plain-text meta field, or raise.

    Raises UnstorableText for any character outside cp1252, combining marks
    included, so the copy gets fixed instead of stored as "?".
    """
    composed = unicodedata.normalize("NFC", text)
    bad = _unstorable(composed)
    if bad:
        combining = any(unicodedata.combining(ch) for ch in bad)
        reason = "Combining marks make Jetpack's SEO meta write fail with HTTP 500. " if combining else ""
        raise UnstorableText(
            f"{field} has characters the database cannot store: {_describe(bad)}. "
            f"{reason}Use text that cp1252 covers in this field "
            f"(for example 'Ethos' rather than 'Eth\u1ecd\u0301s')."
        )
    return composed


def _plain_letters(ch: str) -> str:
    base = fold_latin(ch)
    return "" if _unstorable(base) else base


def derived_meta_text(text: str, field: str, warn: Callable[[str], None]) -> str:
    """plain_meta_text for meta a writer derives itself: folds instead of refusing.

    KK's ruling of 2026-11-12. Each character cp1252 cannot store becomes its
    base letter when it has one cp1252 can store ("Ethọ́s" becomes "Ethos", "Ł"
    becomes "L") and is dropped otherwise (arrows, emoji), then doubled spaces
    collapse. cp1252 text is never touched. `warn` gets one line when anything
    is folded, so the operator sees what WordPress will store.
    """
    composed = unicodedata.normalize("NFC", text)
    if not _unstorable(composed):
        return composed
    folded = "".join(ch if is_storable(ch) else _plain_letters(ch) for ch in composed)
    folded = re.sub(r" {2,}", " ", folded).strip()
    warn(f'seo: folded {field}: "{text}" -> "{folded}"')
    return folded


def assert_storable(value, path: str = "payload") -> None:
    """Raise UnstorableText naming the first field that holds a character outside cp1252."""
    if isinstance(value, str):
        bad = _unstorable(value)
        if bad:
            raise UnstorableText(
                f"{path} has raw characters outside cp1252 that WordPress would store as '?': "
                f"{_describe(bad)}"
            )
    elif isinstance(value, dict):
        for key, item in value.items():
            assert_storable(item, f"{path}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            assert_storable(item, f"{path}[{index}]")


def storable_payload(payload: dict) -> dict:
    """The REST body to send: HTML text fields encoded, then the whole body checked.

    Returns a new dict, so the caller's payload keeps the text it started with.
    """
    encoded = {}
    for key, value in payload.items():
        if key in HTML_TEXT_FIELDS and isinstance(value, str):
            try:
                value = encode_html(value)
            except UnstorableText as exc:
                raise UnstorableText(f"{key}: {exc}") from None
        encoded[key] = value
    assert_storable(encoded)
    return encoded


def assert_sendable(payload: dict, *, alt_texts=(), term_names=()) -> None:
    """Raise UnstorableText if any request a run will make cannot be sent.

    The client checks each request as it sends it, which is after the media
    uploads and term writes that come first. Media trash is off on this site,
    so writers call this before their first upload or term write.
    """
    storable_payload(payload)
    for alt in alt_texts:
        storable_payload({"alt_text": alt})
    for name in term_names:
        storable_payload({"name": name})
