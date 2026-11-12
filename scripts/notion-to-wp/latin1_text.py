"""Keep text sent to kriskrug.co storable in its latin1 database.

The database stores any character above U+00FF that arrives raw as "?" (#606,
#1225). Fields WordPress keeps as HTML (post title, content and excerpt, media
alt text, caption and description, term names) carry those characters as
numeric character references instead, which render identically.

Plain-text meta is different. Jetpack's SEO title and description and the
Publicize message are escaped or posted as text, so a reference would show up
literally, and combining marks in the SEO fields make the REST write fail with
HTTP 500. Those values must already be latin1 before they are sent.

No dependencies beyond the standard library, so the marquee and events writers
can import this without pulling in requests.
"""
from __future__ import annotations

import unicodedata

LATIN1_MAX = 0xFF

HTML_TEXT_FIELDS = frozenset(
    {"title", "content", "excerpt", "alt_text", "caption", "description", "name"}
)

# Typographic punctuation that has an exact plain-text stand-in. Excerpts and
# SEO copy are full of curly quotes, and derive_social_message ends a cut
# Publicize message with an ellipsis, so refusing these would stop ordinary posts.
_PLAIN_TEXT_FOLDS = str.maketrans({
    "\u2018": "'",
    "\u2019": "'",
    "\u201c": '"',
    "\u201d": '"',
    "\u2013": "-",
    "\u2026": "...",
})


class NonLatin1Text(ValueError):
    pass


def to_ncr(text: str) -> str:
    """Replace each character above U+00FF with a decimal numeric reference.

    Latin1 characters and existing entities pass through untouched, so running
    it twice changes nothing.
    """
    return text.encode("latin-1", "xmlcharrefreplace").decode("latin-1")


def _above_latin1(text: str) -> list[str]:
    return [ch for ch in dict.fromkeys(text) if ord(ch) > LATIN1_MAX]


def _describe(chars: list[str]) -> str:
    return ", ".join(f"U+{ord(ch):04X} {unicodedata.name(ch, 'UNNAMED')}" for ch in chars)


def plain_meta_text(text: str, field: str) -> str:
    """Return `text` as latin1 plain text for a meta field, or raise.

    Composes accents (NFC) and folds curly quotes, the en dash and the
    ellipsis to ASCII. Anything else above U+00FF, combining marks included,
    raises NonLatin1Text so the copy gets fixed instead of stored as "?".
    """
    folded = unicodedata.normalize("NFC", text).translate(_PLAIN_TEXT_FOLDS)
    bad = _above_latin1(folded)
    if bad:
        combining = any(unicodedata.combining(ch) for ch in bad)
        reason = "Combining marks make Jetpack's SEO meta write fail with HTTP 500. " if combining else ""
        raise NonLatin1Text(
            f"{field} has characters the latin1 database cannot store: {_describe(bad)}. "
            f"{reason}Use precomposed latin1 or ASCII text in this field "
            f"(for example 'Ethos' rather than 'Eth\u1ecd\u0301s')."
        )
    return folded


def assert_latin1(value, path: str = "payload") -> None:
    """Raise NonLatin1Text naming the first field that holds a raw character above U+00FF."""
    if isinstance(value, str):
        bad = _above_latin1(value)
        if bad:
            raise NonLatin1Text(
                f"{path} has raw characters above U+00FF that WordPress would store as '?': "
                f"{_describe(bad)}"
            )
    elif isinstance(value, dict):
        for key, item in value.items():
            assert_latin1(item, f"{path}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            assert_latin1(item, f"{path}[{index}]")


def latin1_payload(payload: dict) -> dict:
    """The REST body to send: HTML text fields encoded, then the whole body checked.

    Returns a new dict, so the caller's payload keeps the text it started with.
    """
    encoded = {
        key: to_ncr(value) if key in HTML_TEXT_FIELDS and isinstance(value, str) else value
        for key, value in payload.items()
    }
    assert_latin1(encoded)
    return encoded
