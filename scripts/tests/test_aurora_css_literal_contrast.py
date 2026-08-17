"""Contrast coverage for colours that live *inside component rules*.

`test_aurora_contrast_tokens.py` checks named tokens in `theme.json`. That is
necessary but not sufficient: issue #470 was filed against a foreground colour
hardcoded in a component rule, and #464 before it hit rules whose foreground
token was fine but whose *surface* had flipped from dark to cream in the 1.4.0
port. Neither class is visible to a palette-only test.

This module closes that gap with two mechanisms:

1. `REGISTERED_LITERALS` — every literal `color:` declaration in the theme's
   front-end CSS must be registered here together with the surface it actually
   renders against, and must clear its floor. A literal added anywhere in the
   theme with no registry entry fails `test_no_unregistered_foreground_literals`
   until somebody states, in this file, what it sits on and measures it. That
   is the check that would have caught #470 as filed.

2. `RESOLVED_COMPONENT_COLORS` — component rules whose foreground is a *token*
   are resolved through the `:root` blocks and measured against their real
   surface, so a token that is fine in the abstract but wrong in context (the
   #464 failure mode) is still caught.

A caveat this module cannot remove: it reads declarations, not the cascade.
A rule can be correct here and still lose to a later rule of equal
specificity. Confirming a *live* value needs the concatenated stylesheet the
site actually serves, matched against real markup.

Closed by #485 (theme 1.4.6), and now asserted rather than merely noted:

* `.aurora-writing-card` kept a pre-cream near-black background (`#050708`)
  while its text used cream-palette tokens, putting blog-index titles at
  1.00–1.06:1 and meta at 1.00–1.03:1. All six declaration sites were converted
  to `--aurora-panel-solid` together with the component's borders, gradients,
  `::after` wash and `::before` placeholder tiles. Pinned by
  `test_writing_card_is_a_cream_surface` and
  `test_blog_index_card_text_meets_aa_on_the_cream_card`.
* `.aurora-featured-media`'s dark panel (`rgba(21, 24, 33, 0.76)`) is cream, so
  the caption declaration that actually wins the cascade (revive-port.css's
  `--revive-ink-soft`) is 7.62:1 rather than 2.06:1. The losing pre-cream
  literal was deleted rather than retuned. Pinned by
  `test_featured_media_caption_winner_is_legible`.
* `--aurora-ink-muted` was rgba(23, 19, 16, 0.55) — 3.84:1 on cream — while
  theme.json's `text-muted` (#5c5044), the value it is supposed to mirror, is
  6.30:1. Both `:root` blocks now carry #5c5044. Pinned by
  `test_ink_muted_matches_the_palette_entry_it_aliases`.

Known open finding, deliberately not asserted here because fixing it is a
design decision rather than a value correction:

* `.aurora-work-card-num` renders on bare photography with no scrim.
"""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
THEME_DIR = ROOT / "theme/kk-aurora"

# Front-end sheets only. editor.css is not served to visitors.
# Includes Aurora 1.5.0 scaffold sheets (#474): tokens + late (empty at scaffold).
CSS_FILES = (
    "style.css",
    "assets/css/02-tokens.css",
    "assets/css/revive-port.css",
    "assets/css/typography-refined.css",
    "assets/css/bleeding-edge.css",
    "assets/css/animations.css",
    "assets/css/09-late.css",
)

AA_TEXT = 4.5
# SC 1.4.11: graphical objects / decorative separators.
AA_NON_TEXT = 3.0
# Sentinel floors for declarations that cannot be given an honest ratio.
# Both are exempt from the ratio assertion but must still carry a note, so they
# stay visible in the registry instead of silently reading as "fine".
#
#   NOT_STATIC — renders over user-supplied photography with no scrim
#                guaranteeing a surface.
#   OVERRIDDEN — loses the cascade to a later rule, so measuring this value
#                would describe something the browser never paints. The note
#                must record the winning rule and its real ratio.
NOT_STATIC = "not-statically-determinable"
OVERRIDDEN = "overridden-in-the-cascade"
EXEMPT_FLOORS = {NOT_STATIC, OVERRIDDEN}


# --------------------------------------------------------------------------
# colour maths
# --------------------------------------------------------------------------


def _linearize(channel):
    channel = channel / 255
    if channel <= 0.03928:
        return channel / 12.92
    return ((channel + 0.055) / 1.055) ** 2.4


def relative_luminance(rgb):
    red, green, blue = (_linearize(channel) for channel in rgb)
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def contrast_ratio(foreground, background):
    first = relative_luminance(foreground)
    second = relative_luminance(background)
    lighter, darker = max(first, second), min(first, second)
    return (lighter + 0.05) / (darker + 0.05)


def parse_color(value):
    """Parse `#rgb`, `#rrggbb`, `rgb()`, `rgba()` into (r, g, b, alpha)."""
    value = value.replace("!important", "").strip()

    hex_match = re.fullmatch(r"#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})", value)
    if hex_match:
        digits = hex_match.group(1)
        if len(digits) == 3:
            digits = "".join(channel * 2 for channel in digits)
        return (
            int(digits[0:2], 16),
            int(digits[2:4], 16),
            int(digits[4:6], 16),
            1.0,
        )

    func_match = re.fullmatch(r"rgba?\(([^)]*)\)", value)
    if func_match:
        parts = [part for part in re.split(r"[,\s/]+", func_match.group(1)) if part]
        red, green, blue = (int(float(part)) for part in parts[:3])
        alpha = float(parts[3]) if len(parts) > 3 else 1.0
        return (red, green, blue, alpha)

    raise ValueError(f"unparseable colour: {value!r}")


def composite(foreground, background):
    """Flatten a possibly-translucent foreground onto an opaque background."""
    red, green, blue, alpha = foreground
    if alpha >= 1.0:
        return (red, green, blue)
    return tuple(
        round(alpha * channel + (1 - alpha) * base)
        for channel, base in zip((red, green, blue), background)
    )


# --------------------------------------------------------------------------
# a very small CSS reader (selector + declaration pairs, at-rule aware)
# --------------------------------------------------------------------------


def iter_rules(css_text):
    """Yield (at_rule_context, selector, declarations, line_number)."""
    css_text = re.sub(r"/\*.*?\*/", "", css_text, flags=re.S)
    stack = []
    buffer = ""
    index = 0
    line = 1
    while index < len(css_text):
        char = css_text[index]
        if char == "{":
            prelude = " ".join(buffer.split())
            if prelude.startswith("@"):
                stack.append((prelude, None))
                buffer = ""
                index += 1
                continue
            # find the matching close brace for this declaration block
            depth = 1
            end = index + 1
            while end < len(css_text) and depth:
                if css_text[end] == "{":
                    depth += 1
                elif css_text[end] == "}":
                    depth -= 1
                end += 1
            body = css_text[index + 1 : end - 1]
            context = " ".join(entry[0] for entry in stack)
            yield context, prelude, body, line
            line += css_text[index:end].count("\n")
            index = end
            buffer = ""
            continue
        if char == "}":
            if stack:
                stack.pop()
            buffer = ""
        else:
            buffer += char
        if char == "\n":
            line += 1
        index += 1


def root_custom_properties():
    """Collect `--*` declarations from every `:root` block, later files winning."""
    properties = {}
    for name in CSS_FILES:
        for _context, selector, body, _line in iter_rules(
            (THEME_DIR / name).read_text(encoding="utf-8")
        ):
            if selector != ":root":
                continue
            for declaration in body.split(";"):
                match = re.match(r"\s*(--[\w-]+)\s*:\s*(.+)", declaration, flags=re.S)
                if match:
                    properties[match.group(1)] = " ".join(match.group(2).split())
    return properties


def resolve(value, properties, _depth=0):
    """Resolve `var(--token, fallback)` chains down to a literal colour string."""
    value = value.strip()
    if _depth > 10:
        raise ValueError(f"var() cycle resolving {value!r}")
    match = re.fullmatch(r"var\(\s*(--[\w-]+)\s*(?:,\s*(.+?)\s*)?\)", value)
    if not match:
        return value
    token, fallback = match.group(1), match.group(2)
    if token in properties:
        return resolve(properties[token], properties, _depth + 1)
    if fallback is not None:
        return resolve(fallback, properties, _depth + 1)
    raise ValueError(f"unresolvable token: {token}")


def literal_color_declarations():
    """Every literal (non-`var()`) `color:` declaration in front-end CSS.

    Returns {(file, selector, value)} — print-only rules are excluded because
    they never render against a screen surface.
    """
    found = set()
    for name in CSS_FILES:
        text = (THEME_DIR / name).read_text(encoding="utf-8")
        for context, selector, body, _line in iter_rules(text):
            if "print" in context:
                continue
            for declaration in body.split(";"):
                match = re.match(
                    r"\s*(?:-webkit-text-fill-)?color\s*:\s*(.+)",
                    declaration,
                    flags=re.S,
                )
                if not match:
                    continue
                value = " ".join(match.group(1).split())
                bare = value.replace("!important", "").strip()
                if bare.startswith("var(") or bare in {
                    "inherit",
                    "currentColor",
                    "transparent",
                    "unset",
                    "initial",
                    "revert",
                }:
                    continue
                found.add((name, " ".join(selector.split()), bare))
    return found


# --------------------------------------------------------------------------
# the registry
# --------------------------------------------------------------------------

# Opaque surfaces these rules actually render against, all measured from the
# CSS rather than assumed. Keys are referenced by the tables below.
SURFACES = {
    # body.aurora-theme background: var(--revive-surface)
    "cream": (0xEF, 0xE6, 0xD2),
    # --revive-surface-2 / --aurora-panel-solid
    "cream-2": (0xE6, 0xDC, 0xC2),
    # theme.json `muted`, the darkest cream in the palette
    "cream-muted": (0xD9, 0xCD, 0xB0),
    # .aurora-services-band background: var(--revive-ink)
    "ink": (0x17, 0x13, 0x10),
    # .aurora-signal / --wp--preset--color--signal solid fill
    "signal": (0x9A, 0x2F, 0x14),
    # .aurora-signal-control solid fill
    "signal-control": (0xC0, 0x3F, 0x18),
    # .aurora-work-card-media::after — rgba(23,19,16,.72) scrim over a
    # grayscaled photo. Worst case is the scrim over a pure-white photo
    # region: 0.72*(23,19,16) + 0.28*(255,255,255).
    "work-card-scrim": (88, 85, 83),
    # .aurora-hero-scrim (#618 hero) — two stacked gradients of rgb(3,4,5):
    # 90deg 0.82→0.05 and 180deg 0.12→0.5. Worst case inside the copy box is
    # its right/top edge (~40% viewport, top of copy): combined alpha
    # 1-(1-.515)(1-.12)=0.573 over a pure-white photo. Left edge, where the
    # copy actually anchors, measures (35, 36, 36).
    "hero-2026-scrim-copy-edge": (111, 111, 112),
    # .aurora-writing-card / .aurora-featured-media after the #485 cream port:
    # both are flat var(--aurora-panel-solid). The card's ::after wash sits
    # under the card body (z-index 2 vs 3), so it is part of the backdrop; at
    # its darkest (hover, opacity .26) the surface is (227, 215, 189), which is
    # what "writing-card-hover" measures.
    "writing-card": (0xE6, 0xDC, 0xC2),
    "writing-card-hover": (227, 215, 189),
    # .aurora-writing-card ::before placeholder tile, darkest cream + a tint.
    "writing-card-placeholder": (0xD9, 0xCD, 0xB0),
}

# (file, selector, literal) -> (surface key, floor, note)
REGISTERED_LITERALS = {
    (
        "style.css",
        ".aurora-writing-archive .aurora-writing-archive-dek",
        "rgba(247, 247, 242, 0.72)",
    ): (
        "cream",
        OVERRIDDEN,
        "revive-port.css sets this dek to --revive-ink-soft !important, and it "
        "renders in the archive header on cream, not on a card: 8.11:1 live. "
        "The literal here is dead pre-cream residue.",
    ),
    (
        "assets/css/revive-port.css",
        ".aurora-proof-outlets span",
        "rgba(23, 19, 16, 0.62)",
    ): ("cream", AA_TEXT, "outlet names on cream"),
    (
        "assets/css/revive-port.css",
        ".aurora-work-card-num",
        "rgba(239, 230, 210, 0.72)",
    ): (
        "work-card-scrim",
        NOT_STATIC,
        "#411 retired the oversized accent drop-numeral. The quiet mono index "
        "still sits top-left on bare photography (scrim is transparent there), "
        "so the ratio is not statically determinable. Markup now marks it "
        "aria-hidden.",
    ),
    (
        "assets/css/revive-port.css",
        ".aurora-work-card-body",
        "#efe6d2",
    ): ("work-card-scrim", AA_TEXT, "card body text over the ink scrim"),
    (
        "assets/css/revive-port.css",
        "body.aurora-theme #aurora-main .aurora-hero-2026 "
        ":where( #aurora-home-title, .aurora-hero-copy h1 )",
        "#f7f7f2",
    ): (
        "hero-2026-scrim-copy-edge",
        AA_TEXT,
        "hero display heading over the #618 gradient scrim: 4.67:1 at the "
        "geometric worst case (white photo, lightest copy-zone scrim), "
        "14.5:1 at the left edge where the title actually renders.",
    ),
    (
        "assets/css/revive-port.css",
        "body.aurora-theme #aurora-main .aurora-hero-2026 .aurora-button-secondary",
        "#f7f7f2",
    ): (
        "hero-2026-scrim-copy-edge",
        AA_TEXT,
        "ghost-button label in the hero action row; the rgba(247,247,242,.08) "
        "fill is negligible, so the scrim floor governs: 4.67:1 worst case.",
    ),
    (
        "assets/css/revive-port.css",
        "body.aurora-theme #aurora-main .aurora-hero-2026 "
        ":where( .aurora-hero-dek, .aurora-hero-copy p:not(.aurora-kicker) )",
        "#c8cac8",
    ): (
        "hero-2026-scrim-copy-edge",
        NOT_STATIC,
        "3.04:1 at the white-photo worst case, 9.4:1 over the real krug-1 "
        "left field where the dek renders. The gradient alone cannot "
        "guarantee AA at the copy-box edge; it holds because the portrait's "
        "left region is near-black. Re-measure if the hero photo changes.",
    ),
    (
        "assets/css/revive-port.css",
        "body.aurora-theme #aurora-main .aurora-hero-2026 .aurora-kicker",
        "#e8b53a",
    ): (
        "hero-2026-scrim-copy-edge",
        NOT_STATIC,
        "2.65:1 white-photo worst case, 8.2:1 over the real photo's left "
        "field. Amber micro-label (0.72rem uppercase); needs a design call "
        "(darker plate or guaranteed scrim floor) if the hero art lightens.",
    ),
    (
        "assets/css/revive-port.css",
        ".aurora-work-card-body h3",
        "#efe6d2",
    ): ("work-card-scrim", AA_TEXT, "card heading over the ink scrim"),
    (
        "assets/css/revive-port.css",
        ".aurora-work-card-body p",
        "rgba(239, 230, 210, 0.84)",
    ): ("work-card-scrim", AA_TEXT, "card copy over the ink scrim"),
    (
        "assets/css/revive-port.css",
        ".aurora-services-band .aurora-kicker",
        "rgba(239, 230, 210, 0.55)",
    ): ("ink", AA_TEXT, "kicker on the ink services band"),
    (
        "assets/css/revive-port.css",
        ".aurora-services-band .aurora-section-lede",
        "rgba(239, 230, 210, 0.72)",
    ): ("ink", AA_TEXT, "lede on the ink services band"),
    (
        "assets/css/revive-port.css",
        ".aurora-service-card p",
        "rgba(239, 230, 210, 0.75)",
    ): ("ink", AA_TEXT, "service copy on the ink services band"),
    (
        "assets/css/revive-port.css",
        ".aurora-service-card .aurora-service-meta",
        "rgba(239, 230, 210, 0.55)",
    ): ("ink", AA_TEXT, "service meta on the ink services band"),
    (
        "assets/css/revive-port.css",
        "body.aurora-theme #aurora-main .aurora-service-card :where(.aurora-kicker)",
        "rgba(239, 230, 210, 0.55)",
    ): (
        "ink",
        AA_TEXT,
        "service-card roman-numeral kickers on the ink band; outranks the "
        "#aurora-main accent-kicker override that painted them #9a2f14 (2.45:1, "
        "#708 / audit F19)",
    ),
}

# Component rules whose foreground is a token. (file, selector) -> declaration
# is read from the CSS, resolved through :root, and measured against every
# listed surface. This is the #464 failure mode: right token, wrong surface.
RESOLVED_COMPONENT_COLORS = (
    # The #470 defect as filed: the two homepage band links.
    (
        "assets/css/revive-port.css",
        ".aurora-section-head a",
        ("cream", "cream-2"),
        AA_TEXT,
    ),
    (
        "assets/css/revive-port.css",
        ".aurora-section-head h2",
        ("cream", "cream-2"),
        AA_TEXT,
    ),
    (
        "assets/css/revive-port.css",
        ".aurora-section-head h2 .accent",
        ("cream", "cream-2", "cream-muted"),
        AA_TEXT,
    ),
    (
        "assets/css/revive-port.css",
        ".aurora-service-card a",
        ("ink",),
        AA_TEXT,
    ),
    (
        "style.css",
        ".aurora-single-2026 .aurora-article-dek",
        ("cream", "cream-2"),
        AA_TEXT,
    ),
    # #485: every foreground inside the ported writing card, measured against
    # the card surface *and* the darkest point of its ::after wash.
    (
        "style.css",
        ".aurora-writing-card-title a",
        ("writing-card", "writing-card-hover"),
        AA_TEXT,
    ),
    (
        "style.css",
        ".aurora-writing-card-category, .aurora-writing-card-meta",
        ("writing-card", "writing-card-hover"),
        AA_TEXT,
    ),
    (
        "style.css",
        ".aurora-writing-card-meta time, .aurora-writing-card-meta span",
        ("writing-card", "writing-card-hover"),
        AA_TEXT,
    ),
    (
        "style.css",
        ".aurora-writing-archive .aurora-writing-card-excerpt, "
        ".aurora-writing-archive .aurora-writing-card-excerpt p",
        ("writing-card", "writing-card-hover"),
        AA_TEXT,
    ),
    (
        "style.css",
        ".aurora-writing-card-excerpt, .aurora-writing-card-excerpt p",
        ("writing-card", "writing-card-hover"),
        AA_TEXT,
    ),
    # The category pill draws its own rgba(23,19,16,.05) fill on the card.
    (
        "style.css",
        ".aurora-writing-card-category a, .aurora-article-category a, .aurora-post-tags a",
        ("writing-card", "cream", "cream-muted"),
        AA_TEXT,
    ),
    # Pagination and RSS chips on the same template.
    (
        "style.css",
        ".aurora-writing-pagination a, "
        ".aurora-writing-pagination .page-numbers, "
        ".aurora-writing-pagination .wp-block-query-pagination-previous, "
        ".aurora-writing-pagination .wp-block-query-pagination-next",
        ("cream-2",),
        AA_TEXT,
    ),
    ("style.css", ".aurora-feed-link-grid a", ("cream-2",), AA_TEXT),
    (
        "style.css",
        ".aurora-writing-pagination",
        ("cream", "cream-2"),
        AA_TEXT,
    ),
    ("style.css", ".aurora-meta-divider", ("cream", "cream-2"), AA_NON_TEXT),
    (
        "style.css",
        ".aurora-search-form .wp-block-search__button, "
        ".aurora-theme .wp-block-search__button, "
        ".aurora-form button, "
        ".aurora-theme :where(.gform_wrapper, .wp-block-jetpack-contact-form) button",
        ("signal",),
        AA_TEXT,
    ),
    (
        "style.css",
        ".aurora-button-primary, "
        ".wp-block-button.is-style-aurora-primary .wp-block-button__link",
        ("signal-control",),
        AA_TEXT,
    ),
)


def declared_color(css_name, selector):
    """The last `color:` declared for an exact selector in one file."""
    text = (THEME_DIR / css_name).read_text(encoding="utf-8")
    wanted = " ".join(selector.split())
    value = None
    for context, found_selector, body, _line in iter_rules(text):
        if "print" in context or " ".join(found_selector.split()) != wanted:
            continue
        for declaration in body.split(";"):
            match = re.match(r"\s*color\s*:\s*(.+)", declaration, flags=re.S)
            if match:
                value = (
                    " ".join(match.group(1).split()).replace("!important", "").strip()
                )
    return value


class AuroraCssLiteralContrastTests(unittest.TestCase):
    def setUp(self):
        self.properties = root_custom_properties()

    # -- mechanism 1: no unjustified literals ------------------------------

    def test_no_unregistered_foreground_literals(self):
        """A new hardcoded foreground colour must declare what it sits on.

        This is the check that was missing when #470 was filed: nothing forced
        a literal `color:` inside a component rule to be measured at all.
        """
        found = literal_color_declarations()
        unregistered = sorted(
            entry for entry in found if entry not in REGISTERED_LITERALS
        )
        self.assertEqual(
            unregistered,
            [],
            "Hardcoded foreground colour(s) with no registered surface. Either use "
            "a semantic token, or add an entry to REGISTERED_LITERALS naming the "
            "surface it renders against:\n"
            + "\n".join(
                f"  {name}  {selector}  ->  {value}"
                for name, selector, value in unregistered
            ),
        )

    def test_registry_has_no_stale_entries(self):
        """Registry entries must still exist in the CSS, so it cannot rot."""
        found = literal_color_declarations()
        stale = sorted(entry for entry in REGISTERED_LITERALS if entry not in found)
        self.assertEqual(
            stale, [], f"REGISTERED_LITERALS entries no longer in the CSS: {stale}"
        )

    def test_registered_literals_meet_their_floor(self):
        failures = []
        for (name, selector, value), (surface_key, floor, note) in sorted(
            REGISTERED_LITERALS.items()
        ):
            if floor in EXEMPT_FLOORS:
                self.assertTrue(
                    note, f"{name} {selector} needs a note explaining the exemption"
                )
                continue
            surface = SURFACES[surface_key]
            ratio = contrast_ratio(composite(parse_color(value), surface), surface)
            if ratio < floor:
                failures.append(
                    f"{name} {selector}: {value} on {surface_key} = {ratio:.2f}:1 "
                    f"(needs {floor}:1) — {note}"
                )
        self.assertEqual(failures, [])

    # -- mechanism 2: tokens measured in context ---------------------------

    def test_component_token_colors_meet_aa_on_their_real_surfaces(self):
        """Right token, wrong surface — the #464/#470 root-cause family."""
        failures = []
        for name, selector, surface_keys, floor in RESOLVED_COMPONENT_COLORS:
            declaration = declared_color(name, selector)
            self.assertIsNotNone(
                declaration,
                f"expected a color declaration for {selector!r} in {name}",
            )
            literal = resolve(declaration, self.properties)
            for surface_key in surface_keys:
                surface = SURFACES[surface_key]
                ratio = contrast_ratio(
                    composite(parse_color(literal), surface), surface
                )
                if ratio < floor:
                    failures.append(
                        f"{name} {selector} -> {declaration} ({literal}) "
                        f"on {surface_key} = {ratio:.2f}:1 (needs {floor}:1)"
                    )
        self.assertEqual(failures, [])

    # -- the specific #470 regression --------------------------------------

    def test_section_head_links_are_legible_on_cream(self):
        """#470: 'Photography →' and 'Full index →' on the homepage.

        The archive and work bands inherit the cream body surface, so a
        cream-family foreground here is invisible. Pinned explicitly because
        this rule is the one the issue was filed against.
        """
        declaration = declared_color(
            "assets/css/revive-port.css", ".aurora-section-head a"
        )
        self.assertIsNotNone(declaration)
        self.assertTrue(
            declaration.startswith("var("),
            f"section-head links must use a semantic token, got {declaration!r}",
        )
        literal = resolve(declaration, self.properties)
        for surface_key in ("cream", "cream-2"):
            surface = SURFACES[surface_key]
            ratio = contrast_ratio(composite(parse_color(literal), surface), surface)
            self.assertGreaterEqual(
                ratio,
                AA_TEXT,
                f".aurora-section-head a ({literal}) on {surface_key} is {ratio:.2f}:1",
            )

    def test_front_page_still_renders_the_section_head_links(self):
        """Guard the selector itself — a renamed class would silence the test."""
        front_page = (THEME_DIR / "templates/front-page.html").read_text(
            encoding="utf-8"
        )
        self.assertIn("aurora-section-head", front_page)
        self.assertIn("Photography", front_page)
        self.assertIn("Full index", front_page)

    # -- the specific #485 regression --------------------------------------

    def test_ink_muted_matches_the_palette_entry_it_aliases(self):
        """#485: the CSS alias had drifted from theme.json's `text-muted`.

        rgba(23, 19, 16, 0.55) is not #5c5044 — it is a *different colour* that
        happens to sit in the same family, and it was 3.84:1 on cream against
        the palette value's 6.30:1, across ~30 foreground uses.
        """
        palette = json.loads((THEME_DIR / "theme.json").read_text(encoding="utf-8"))
        text_muted = next(
            entry["color"]
            for entry in palette["settings"]["color"]["palette"]
            if entry["slug"] == "text-muted"
        )
        for token in ("--aurora-ink-muted", "--revive-ink-muted"):
            self.assertEqual(
                self.properties[token].lower(),
                text_muted.lower(),
                f"{token} must mirror theme.json text-muted ({text_muted})",
            )
        # ...and it has to actually clear AA on every cream surface it lands on.
        for surface_key in ("cream", "cream-2", "cream-muted"):
            surface = SURFACES[surface_key]
            ratio = contrast_ratio(composite(parse_color(text_muted), surface), surface)
            self.assertGreaterEqual(
                ratio, AA_TEXT, f"text-muted on {surface_key} is {ratio:.2f}:1"
            )

    def test_writing_card_is_a_cream_surface(self):
        """#485: no `.aurora-writing-card` rule may repaint a dark surface.

        The component is declared in six places. The archive override at
        (0,2,0) is the one that wins on /blog/, so a fix applied only to the
        base rule would have changed nothing live — this walks every rule whose
        selector mentions the component and fails on any dark background,
        whichever site it came from.
        """
        text = (THEME_DIR / "style.css").read_text(encoding="utf-8")
        offenders = []
        for context, selector, body, line in iter_rules(text):
            if "print" in context or "aurora-writing-card" not in selector:
                continue
            for declaration in body.split(";"):
                match = re.match(
                    r"\s*(background|background-color)\s*:\s*(.+)",
                    declaration,
                    flags=re.S,
                )
                if not match:
                    continue
                value = " ".join(match.group(2).split())
                for literal in re.findall(r"#[0-9a-fA-F]{3,6}\b|rgba?\([^)]*\)", value):
                    parsed = parse_color(literal)
                    if parsed[3] < 0.5:
                        # A translucent tint reads as a wash over whatever is
                        # beneath it, not as the surface itself.
                        continue
                    if relative_luminance(parsed[:3]) < 0.18:
                        offenders.append(f"style.css:{line} {selector} -> {literal}")
        self.assertEqual(
            offenders,
            [],
            "dark surface(s) still painted inside the cream writing card:\n"
            + "\n".join(f"  {entry}" for entry in offenders),
        )

    def test_blog_index_card_text_meets_aa_on_the_cream_card(self):
        """#485 as filed: titles and meta on the blog index.

        Measured against the darkest backdrop the text can get — the card
        surface with the hover ::after wash on top of it, since that wash
        paints below `.aurora-writing-card-body` (z-index 2 vs 3).
        """
        surface = SURFACES["writing-card-hover"]
        for selector in (
            ".aurora-writing-card-title a",
            ".aurora-writing-card-category, .aurora-writing-card-meta",
        ):
            declaration = declared_color("style.css", selector)
            self.assertIsNotNone(declaration, f"no color declared for {selector}")
            self.assertTrue(
                declaration.startswith("var("),
                f"{selector} must use a semantic token, got {declaration!r}",
            )
            literal = resolve(declaration, self.properties)
            ratio = contrast_ratio(composite(parse_color(literal), surface), surface)
            self.assertGreaterEqual(
                ratio, AA_TEXT, f"{selector} ({literal}) is {ratio:.2f}:1 on the card"
            )

    def test_blog_index_template_still_renders_the_probed_classes(self):
        """Guard the selectors — a renamed class would silence the tests above."""
        home = (THEME_DIR / "templates/home.html").read_text(encoding="utf-8")
        for class_name in (
            "aurora-writing-archive",
            "aurora-writing-card",
            "aurora-writing-card-title",
            "aurora-writing-card-meta",
            "aurora-writing-pagination",
        ):
            self.assertIn(class_name, home)

    def test_featured_media_caption_winner_is_legible(self):
        """#485: fix the surface, not the declaration that never paints.

        `.aurora-featured-media :where(figcaption, ...)` and revive-port.css's
        `.aurora-theme :where(p, li, figcaption)` are both (0,1,0); the later
        file wins. So the caption's real colour is --revive-ink-soft, and the
        only thing that can move its ratio is the panel underneath.
        """
        panel_rule = None
        for _context, selector, body, _line in iter_rules(
            (THEME_DIR / "style.css").read_text(encoding="utf-8")
        ):
            if " ".join(selector.split()) == ".aurora-featured-media":
                for declaration in body.split(";"):
                    match = re.match(
                        r"\s*background\s*:\s*(.+)", declaration, flags=re.S
                    )
                    if match:
                        panel_rule = " ".join(match.group(1).split())
        self.assertIsNotNone(
            panel_rule, "no background declared for .aurora-featured-media"
        )
        panel = parse_color(resolve(panel_rule, self.properties))
        self.assertEqual(panel[3], 1.0, "the featured-media panel must be opaque")

        # The losing pre-cream literal must be gone, not retuned in place.
        self.assertIsNone(
            declared_color(
                "style.css",
                ".aurora-featured-media :where(figcaption, .wp-element-caption)",
            ),
            "this rule's color never paints; it must not declare one",
        )

        winner = resolve(self.properties["--revive-ink-soft"], self.properties)
        ratio = contrast_ratio(composite(parse_color(winner), panel[:3]), panel[:3])
        self.assertGreaterEqual(
            ratio, AA_TEXT, f"featured-media caption is {ratio:.2f}:1 on its panel"
        )

    # -- sanity check on the maths ----------------------------------------

    def test_contrast_maths_matches_known_values(self):
        self.assertAlmostEqual(
            contrast_ratio((0, 0, 0), (255, 255, 255)), 21.0, places=2
        )
        self.assertAlmostEqual(
            contrast_ratio((255, 255, 255), (255, 255, 255)), 1.0, places=2
        )
        # #9a2f14 on cream #efe6d2, the accent-text value from #465.
        self.assertAlmostEqual(
            contrast_ratio((0x9A, 0x2F, 0x14), (0xEF, 0xE6, 0xD2)), 6.06, places=2
        )
        # A translucent cream on cream is the #470 failure shape.
        self.assertLess(
            contrast_ratio(
                composite(parse_color("rgba(239, 230, 210, 0.78)"), SURFACES["cream"]),
                SURFACES["cream"],
            ),
            1.1,
        )


if __name__ == "__main__":
    unittest.main()
