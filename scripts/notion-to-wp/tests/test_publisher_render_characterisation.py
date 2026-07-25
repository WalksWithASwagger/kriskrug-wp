"""Characterisation tests for the one-off publish_*.py block loops (issue #254).

These pin the CURRENT rendering behaviour of the marker -> Gutenberg loops that
each `publish_*.py` script carries inline, so the #254 consolidation can be shown
to be behaviour-preserving.

The `legacy_*` functions below are transcribed verbatim from the scripts as they
stood before the #254 refactor:

  * `legacy_render_dc_protest`       <- publish_dc_protest_draft.py
  * `legacy_render_you_cant_drink`   <- publish_you_cant_drink_data.py
  * `legacy_render_context_creators` <- publish_context_creators.py
  * `legacy_render_text_post`        <- publish_common.render_text_post (proximity)

Do NOT "fix" a legacy function. They are the reference. If a shared helper stops
matching one of them, the helper changed behaviour and that is the bug.
"""
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import publish_common  # noqa: E402
from wp_blocks import (  # noqa: E402
    gallery,
    heading,
    hero_image,
    image,
    inline,
    inline_image,
    pullquote,
    separator,
)

MEDIA_RE = re.compile(r"^!\[(.*?)\]\(media:(\d+)\)$")
PHOTO_RE = re.compile(r"^!\[(.*?)\]\(photo:(\d+)\)$")
POSTER_RE = re.compile(r"^!\[(.*?)\]\(poster:(\d+)\)$")
SCREENSHOT_RE = re.compile(r"^!\[(.*?)\]\(screenshot:([a-z-]+)\)$")


# --------------------------------------------------------------------------
# Legacy reference implementations (verbatim, pre-#254)
# --------------------------------------------------------------------------
def legacy_render_dc_protest(body: str, uploaded: dict) -> list[str]:
    out = []
    seen_title = False
    for b in publish_common.split_body_blocks(body):
        if b.startswith("# ") and not seen_title:
            seen_title = True
            continue
        m = publish_common.MARKDOWN_IMG_IMAGES_RE.match(b)
        if m:
            fn, alt = m.group(2), m.group(1)
            u = uploaded[fn]
            out.append(image(u["id"], u["url"], alt, caption=alt, width=None, align=None, lightbox=True))
        elif b.startswith("## "):
            out.append(heading(inline(b[3:].strip())))
        elif b == "---":
            out.append(separator())
        else:
            out.append(f"<!-- wp:paragraph -->\n<p>{inline(b)}</p>\n<!-- /wp:paragraph -->")
    return out


def legacy_render_you_cant_drink(
    body: str,
    *,
    ai_signs: dict,
    ai_gallery: list,
    ai_cap: dict,
    inbody_ai: dict,
    inbody_photo: dict,
    best_photos: list,
    photos_rest: list,
    inbody_photos: dict,
) -> list[str]:
    out = []
    seen_title = False
    for b in publish_common.split_body_blocks(body):
        b = b.strip()
        if b.startswith("# ") and not seen_title:
            seen_title = True
            continue
        if b == "---":
            out.append(separator())
        elif b.startswith("## "):
            out.append(heading(inline(b[3:].strip())))
        elif b.startswith(">>> "):
            out.append(pullquote(inline(b[4:].strip())))
        elif b == "[[GALLERY-BEST]]":
            out.append(gallery([(i, u, a, c) for i, u, a, c, _ in best_photos], columns=3))
        elif b == "[[GALLERY-AI]]":
            out.append(
                gallery(
                    [(mid, ai_signs[mid][0], ai_signs[mid][1], ai_cap[mid]) for mid in ai_gallery],
                    columns=3,
                )
            )
        elif b == "[[GALLERY-PHOTOS]]":
            if photos_rest:
                out.append(gallery([(i, u, a, c) for i, u, a, c, _ in photos_rest], columns=3))
        else:
            m = MEDIA_RE.match(b)
            mp = PHOTO_RE.match(b)
            if m:
                mid = int(m.group(2))
                url, alt = ai_signs[mid]
                cap, align, width = inbody_ai.get(mid, (None, "center", 320))
                out.append(image(mid, url, alt, caption=cap, width=width, align=align))
            elif mp:
                key = mp.group(2)
                if key in inbody_photos:
                    mid, url, alt, cap = inbody_photos[key]
                    align, width = inbody_photo.get(key, ("center", 660))
                    out.append(image(mid, url, alt, caption=cap, width=width, align=align))
            else:
                out.append(publish_common.render_paragraph_from_markdown(b))
    return out


def legacy_render_context_creators(body: str, *, poster_media: dict, shot_media: dict) -> list[str]:
    out = []
    seen_title = False
    for b in publish_common.split_body_blocks(body):
        if b.startswith("# ") and not seen_title:
            seen_title = True
            continue
        if b == "---":
            out.append(separator())
        elif b.startswith("## "):
            out.append(heading(inline(b[3:].strip())))
        elif b.startswith(">>> "):
            out.append(pullquote(inline(b[4:].strip())))
        else:
            mp = POSTER_RE.match(b)
            ms = SCREENSHOT_RE.match(b)
            if mp:
                n = int(mp.group(2))
                mid, url, alt = poster_media[n]
                out.append(hero_image(mid, url, alt))
            elif ms:
                mid, url, alt, caption = shot_media[ms.group(2)]
                out.append(inline_image(mid, url, alt, caption=caption))
            else:
                out.append(publish_common.render_paragraph_from_markdown(b))
    return out


def legacy_render_text_post(body: str) -> str:
    out: list[str] = []
    seen_title = False
    for block in publish_common.split_body_blocks(body):
        if block.startswith("# ") and not seen_title:
            seen_title = True
            continue
        if block == "---":
            out.append(separator())
        elif block.startswith("## "):
            out.append(heading(inline(block[3:].strip()), level=2))
        elif block.startswith("### "):
            out.append(heading(inline(block[4:].strip()), level=3))
        else:
            out.append(publish_common.render_paragraph_from_markdown(block))
    return "\n\n".join(out)


# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------
DC_BODY = """# Dropped Title

Intro paragraph with an [internal link](https://kriskrug.co/x/) and **bold**.

## A Heading

![a sign that says water the servers last](images/04-water.png)

---

A multi-line paragraph
that spans two source lines.

![second sign](images/06-thirsty.png)
"""

DC_UPLOADED = {
    "04-water.png": {"id": 11918, "url": "https://kriskrug.co/wp-content/uploads/2026/05/04-water.png"},
    "06-thirsty.png": {"id": 11919, "url": "https://kriskrug.co/wp-content/uploads/2026/05/06-thirsty.png"},
}

YCDD_BODY = """# Dropped Title

Opening paragraph.

## Section One

>>> A punchy pullquote line.

---

![we are the training data](media:11920)

![march photo](photo:7674)

![missing photo key](photo:9999)

[[GALLERY-BEST]]

[[GALLERY-AI]]

[[GALLERY-PHOTOS]]

Closing paragraph
with a second line.
"""

YCDD_AI_SIGNS = {
    11920: ("https://kriskrug.co/u/we-are-the-training-data.jpg", "WE ARE THE TRAINING DATA, datamosh glitch type"),
    11918: ("https://kriskrug.co/u/water-the-servers-last.png", "WATER THE SERVERS LAST, block-stack type"),
}
YCDD_AI_GALLERY = [11918, 11920]
YCDD_AI_CAP = {mid: YCDD_AI_SIGNS[mid][1].split(",")[0] for mid in YCDD_AI_GALLERY}
YCDD_INBODY_AI = {11920: ("One of mine.", "right", 300)}
YCDD_INBODY_PHOTO = {"7674": ("center", 680)}
YCDD_BEST = [(1, "https://kriskrug.co/u/best-1.jpg", "best one", "cap one", "01-best.jpg")]
YCDD_INBODY_PHOTOS = {"7674": (2, "https://kriskrug.co/u/7674.jpg", "alt 7674", "cap 7674")}

CC_BODY = """# Dropped Title

Lead paragraph.

## What I Actually Did

>>> A deck line.

---

![poster hero](poster:2)

![the recipe slide](screenshot:persona)

Trailing paragraph
over two lines.
"""

CC_POSTER_MEDIA = {2: (900, "https://kriskrug.co/u/poster-2.png", "Both Hands Full poster")}
CC_SHOT_MEDIA = {"persona": (901, "https://kriskrug.co/u/slide-persona.png", "Persona slide", "The recipe.")}

TEXT_BODY = """# Dropped Title

Opening with an [external link](https://example.com/a).

## H2 Section

### H3 Section

---

Two line
paragraph here.
"""


def block_kinds(blocks: list[str]) -> list[str]:
    """First-line block-comment name for each rendered block."""
    return [b.split("\n", 1)[0].split(" ")[1].rstrip(">").strip() for b in blocks]


class DcProtestCharacterisationTests(unittest.TestCase):
    def test_block_sequence_is_stable(self):
        out = legacy_render_dc_protest(DC_BODY, DC_UPLOADED)
        self.assertEqual(
            block_kinds(out),
            ["wp:paragraph", "wp:heading", "wp:image", "wp:separator", "wp:paragraph", "wp:image"],
        )

    def test_first_h1_is_dropped(self):
        out = legacy_render_dc_protest(DC_BODY, DC_UPLOADED)
        self.assertNotIn("Dropped Title", "\n".join(out))

    def test_image_block_uses_alt_as_caption_and_no_align(self):
        out = legacy_render_dc_protest(DC_BODY, DC_UPLOADED)
        img_block = out[2]
        self.assertIn('"id":11918', img_block)
        self.assertIn('"lightbox":{"enabled":true}', img_block)
        self.assertNotIn('"align"', img_block)
        self.assertIn(
            '<figcaption class="wp-element-caption">a sign that says water the servers last</figcaption>',
            img_block,
        )

    def test_multiline_paragraph_keeps_newline_and_does_not_insert_br(self):
        """dc_protest is the ONLY script that does not <br>-join paragraph lines."""
        out = legacy_render_dc_protest(DC_BODY, DC_UPLOADED)
        para = out[4]
        self.assertIn("A multi-line paragraph\nthat spans two source lines.", para)
        self.assertNotIn("<br>", para)


class YouCantDrinkDataCharacterisationTests(unittest.TestCase):
    def render(self, *, photos_rest):
        return legacy_render_you_cant_drink(
            YCDD_BODY,
            ai_signs=YCDD_AI_SIGNS,
            ai_gallery=YCDD_AI_GALLERY,
            ai_cap=YCDD_AI_CAP,
            inbody_ai=YCDD_INBODY_AI,
            inbody_photo=YCDD_INBODY_PHOTO,
            best_photos=YCDD_BEST,
            photos_rest=photos_rest,
            inbody_photos=YCDD_INBODY_PHOTOS,
        )

    def test_block_sequence_is_stable(self):
        out = self.render(photos_rest=[])
        self.assertEqual(
            block_kinds(out),
            [
                "wp:paragraph",
                "wp:heading",
                "wp:pullquote",
                "wp:separator",
                "wp:image",
                "wp:image",
                "wp:gallery",
                "wp:gallery",
                "wp:paragraph",
            ],
        )

    def test_unknown_photo_key_emits_nothing(self):
        """`![x](photo:9999)` with no matching upload is silently dropped."""
        out = self.render(photos_rest=[])
        self.assertNotIn("9999", "\n".join(out))

    def test_empty_gallery_photos_emits_nothing(self):
        without = self.render(photos_rest=[])
        with_rest = self.render(
            photos_rest=[(3, "https://kriskrug.co/u/rest.jpg", "rest alt", "rest cap", "05-rest.jpg")]
        )
        self.assertEqual(len(with_rest), len(without) + 1)

    def test_inbody_ai_uses_declared_align_and_width(self):
        out = self.render(photos_rest=[])
        block = out[4]
        self.assertIn('"width":"300px"', block)
        self.assertIn('"align":"right"', block)
        self.assertIn("One of mine.", block)

    def test_multiline_paragraph_is_br_joined(self):
        out = self.render(photos_rest=[])
        self.assertIn("Closing paragraph<br>with a second line.", out[-1])


class ContextCreatorsCharacterisationTests(unittest.TestCase):
    def render(self):
        return legacy_render_context_creators(
            CC_BODY, poster_media=CC_POSTER_MEDIA, shot_media=CC_SHOT_MEDIA
        )

    def test_block_sequence_is_stable(self):
        self.assertEqual(
            block_kinds(self.render()),
            [
                "wp:paragraph",
                "wp:heading",
                "wp:pullquote",
                "wp:separator",
                "wp:image",
                "wp:image",
                "wp:paragraph",
            ],
        )

    def test_poster_is_full_width_and_screenshot_is_460(self):
        out = self.render()
        self.assertNotIn('"width"', out[4])
        self.assertIn('"width":"460px"', out[5])

    def test_screenshot_caption_comes_from_declaration_not_markdown_alt(self):
        out = self.render()
        self.assertIn("The recipe.", out[5])
        self.assertIn('alt="Persona slide"', out[5])


class TextPostCharacterisationTests(unittest.TestCase):
    def test_matches_shipped_render_text_post(self):
        self.assertEqual(
            publish_common.render_text_post(TEXT_BODY), legacy_render_text_post(TEXT_BODY)
        )

    def test_h3_level_attr_and_external_link_target(self):
        out = publish_common.render_text_post(TEXT_BODY)
        self.assertIn('{"level":3}', out)
        self.assertIn('target="_blank" rel="noopener noreferrer"', out)
        self.assertNotIn("<h1", out)


# --------------------------------------------------------------------------
# Equivalence: the consolidated dispatcher must reproduce every legacy loop
# byte for byte. These are the proof that #254 is behaviour-preserving.
# --------------------------------------------------------------------------
def shared_render_dc_protest(body: str, uploaded: dict) -> list[str]:
    """publish_dc_protest_draft.py, post-#254."""
    def staged_image(block, match):
        alt, filename = match.group(1), match.group(2)
        media = uploaded[filename]
        return image(media["id"], media["url"], alt, caption=alt, width=None, align=None, lightbox=True)

    return publish_common.render_marker_blocks(
        body,
        [(publish_common.MARKDOWN_IMG_IMAGES_RE, staged_image)]
        + publish_common.standard_text_handlers(h3=False),
        paragraph=publish_common.raw_paragraph,
    )


def shared_render_you_cant_drink(
    body: str,
    *,
    ai_signs: dict,
    ai_gallery: list,
    ai_cap: dict,
    inbody_ai: dict,
    inbody_photo: dict,
    best_photos: list,
    photos_rest: list,
    inbody_photos: dict,
) -> list[str]:
    """publish_you_cant_drink_data.py, post-#254."""
    def ai_sign(block, match):
        mid = int(match.group(2))
        url, alt = ai_signs[mid]
        cap, align, width = inbody_ai.get(mid, (None, "center", 320))
        return image(mid, url, alt, caption=cap, width=width, align=align)

    def march_photo(block, match):
        key = match.group(2)
        if key not in inbody_photos:
            return None
        mid, url, alt, cap = inbody_photos[key]
        align, width = inbody_photo.get(key, ("center", 660))
        return image(mid, url, alt, caption=cap, width=width, align=align)

    return publish_common.render_marker_blocks(
        body,
        publish_common.standard_text_handlers(h3=False, pullquote_marker=True)
        + [
            (publish_common.exact("[[GALLERY-BEST]]"),
             lambda b, m: gallery([(i, u, a, c) for i, u, a, c, _ in best_photos], columns=3)),
            (publish_common.exact("[[GALLERY-AI]]"),
             lambda b, m: gallery(
                 [(mid, ai_signs[mid][0], ai_signs[mid][1], ai_cap[mid]) for mid in ai_gallery],
                 columns=3,
             )),
            (publish_common.exact("[[GALLERY-PHOTOS]]"),
             lambda b, m: gallery([(i, u, a, c) for i, u, a, c, _ in photos_rest], columns=3)
             if photos_rest else None),
            (MEDIA_RE, ai_sign),
            (PHOTO_RE, march_photo),
        ],
    )


def shared_render_context_creators(body: str, *, poster_media: dict, shot_media: dict) -> list[str]:
    """publish_context_creators.py, post-#254."""
    def poster(block, match):
        mid, url, alt = poster_media[int(match.group(2))]
        return hero_image(mid, url, alt)

    def screenshot(block, match):
        mid, url, alt, caption = shot_media[match.group(2)]
        return inline_image(mid, url, alt, caption=caption)

    return publish_common.render_marker_blocks(
        body,
        publish_common.standard_text_handlers(h3=False, pullquote_marker=True)
        + [(POSTER_RE, poster), (SCREENSHOT_RE, screenshot)],
    )


class DispatcherEquivalenceTests(unittest.TestCase):
    def test_dc_protest_identical(self):
        self.assertEqual(
            shared_render_dc_protest(DC_BODY, DC_UPLOADED),
            legacy_render_dc_protest(DC_BODY, DC_UPLOADED),
        )

    def test_you_cant_drink_identical(self):
        for photos_rest in ([], [(3, "https://kriskrug.co/u/r.jpg", "r alt", "r cap", "05-r.jpg")]):
            kwargs = dict(
                ai_signs=YCDD_AI_SIGNS,
                ai_gallery=YCDD_AI_GALLERY,
                ai_cap=YCDD_AI_CAP,
                inbody_ai=YCDD_INBODY_AI,
                inbody_photo=YCDD_INBODY_PHOTO,
                best_photos=YCDD_BEST,
                photos_rest=photos_rest,
                inbody_photos=YCDD_INBODY_PHOTOS,
            )
            with self.subTest(photos_rest=bool(photos_rest)):
                self.assertEqual(
                    shared_render_you_cant_drink(YCDD_BODY, **kwargs),
                    legacy_render_you_cant_drink(YCDD_BODY, **kwargs),
                )

    def test_context_creators_identical(self):
        self.assertEqual(
            shared_render_context_creators(
                CC_BODY, poster_media=CC_POSTER_MEDIA, shot_media=CC_SHOT_MEDIA
            ),
            legacy_render_context_creators(
                CC_BODY, poster_media=CC_POSTER_MEDIA, shot_media=CC_SHOT_MEDIA
            ),
        )

    def test_text_post_identical(self):
        self.assertEqual(
            publish_common.render_text_post(TEXT_BODY), legacy_render_text_post(TEXT_BODY)
        )

    def test_cross_fed_bodies_stay_identical(self):
        """Every corpus body through every renderer: legacy and shared must agree.

        Cross-feeding catches marker-precedence drift that a script's own body
        would never exercise (e.g. a `>>> ` line reaching the dc_protest loop).
        """
        bodies = {"dc": DC_BODY, "ycdd": YCDD_BODY, "cc": CC_BODY, "text": TEXT_BODY}
        ycdd_kwargs = dict(
            ai_signs=YCDD_AI_SIGNS,
            ai_gallery=YCDD_AI_GALLERY,
            ai_cap=YCDD_AI_CAP,
            inbody_ai=YCDD_INBODY_AI,
            inbody_photo=YCDD_INBODY_PHOTO,
            best_photos=YCDD_BEST,
            photos_rest=[],
            inbody_photos=YCDD_INBODY_PHOTOS,
        )
        for name, body in bodies.items():
            with self.subTest(body=name, loop="you_cant_drink"):
                self.assertEqual(
                    shared_render_you_cant_drink(body, **ycdd_kwargs),
                    legacy_render_you_cant_drink(body, **ycdd_kwargs),
                )
            with self.subTest(body=name, loop="context_creators"):
                self.assertEqual(
                    shared_render_context_creators(
                        body, poster_media=CC_POSTER_MEDIA, shot_media=CC_SHOT_MEDIA
                    ),
                    legacy_render_context_creators(
                        body, poster_media=CC_POSTER_MEDIA, shot_media=CC_SHOT_MEDIA
                    ),
                )
            with self.subTest(body=name, loop="text_post"):
                self.assertEqual(
                    "\n\n".join(
                        publish_common.render_marker_blocks(
                            body, publish_common.standard_text_handlers()
                        )
                    ),
                    legacy_render_text_post(body),
                )

    def test_dc_protest_cross_fed_bodies_stay_identical(self):
        """dc_protest's loop only resolves `images/` markers, so feed it safe bodies."""
        for name, body in (("dc", DC_BODY), ("text", TEXT_BODY)):
            with self.subTest(body=name):
                self.assertEqual(
                    shared_render_dc_protest(body, DC_UPLOADED),
                    legacy_render_dc_protest(body, DC_UPLOADED),
                )


class RenderMarkerBlocksUnitTests(unittest.TestCase):
    def test_first_matching_handler_wins(self):
        handlers = [
            (publish_common.prefix("## "), lambda b, m: "FIRST"),
            (publish_common.prefix("## "), lambda b, m: "SECOND"),
        ]
        self.assertEqual(publish_common.render_marker_blocks("## x", handlers), ["FIRST"])

    def test_handler_returning_none_emits_nothing(self):
        handlers = [(publish_common.exact("SKIP"), lambda b, m: None)]
        self.assertEqual(publish_common.render_marker_blocks("SKIP\n\nkeep", handlers)[0].count("keep"), 1)
        self.assertEqual(len(publish_common.render_marker_blocks("SKIP\n\nkeep", handlers)), 1)

    def test_regex_matcher_receives_the_match_object(self):
        seen = []
        handlers = [(re.compile(r"^X(\d+)$"), lambda b, m: seen.append(m.group(1)) or "ok")]
        publish_common.render_marker_blocks("X42", handlers)
        self.assertEqual(seen, ["42"])

    def test_h3_never_collides_with_h2_prefix(self):
        out = publish_common.render_marker_blocks("### Sub", publish_common.standard_text_handlers())
        self.assertIn('{"level":3}', out[0])

    def test_skip_first_h1_only_drops_the_first(self):
        out = publish_common.render_marker_blocks("# One\n\n# Two", [])
        self.assertEqual(len(out), 1)
        self.assertIn("# Two", out[0])

    def test_skip_first_h1_can_be_disabled(self):
        out = publish_common.render_marker_blocks("# One", [], skip_first_h1=False)
        self.assertEqual(len(out), 1)


class StripFrontmatterTests(unittest.TestCase):
    def test_matches_the_inline_index_walk_it_replaces(self):
        raw = "---\ntitle: T\nslug: s\n---\n\nBody line.\n"
        fm_end = raw.index("\n---", raw.index("---") + 3)
        self.assertEqual(publish_common.strip_frontmatter(raw), raw[fm_end + 4:])

    def test_body_survives_a_horizontal_rule(self):
        raw = "---\ntitle: T\n---\n\nOne.\n\n---\n\nTwo.\n"
        body = publish_common.strip_frontmatter(raw)
        self.assertEqual(publish_common.split_body_blocks(body), ["One.", "---", "Two."])

    def test_missing_fences_raise(self):
        with self.assertRaises(ValueError):
            publish_common.strip_frontmatter("no front matter here")


if __name__ == "__main__":
    unittest.main()
