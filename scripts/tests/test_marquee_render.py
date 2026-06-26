"""Marquee Tier 1 guarantees: geometry, no-JS-safe cells, on-brand tokens, external animation.

Mirrors the plan's verification: board fits the geometry, cells are pre-rendered (work without
JS, no CLS), the LED skin uses Aurora tokens (not the old off-brand hex), and the hero animation
is the deferred theme asset — not inline in the hero.
"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
THEME = ROOT / "theme/kk-aurora"
sys.path.insert(0, str(ROOT / "scripts/marquee"))

import render  # noqa: E402
from marquee_lib import wrap_board, MAX_LINE_CHARS, MAX_LINES  # noqa: E402

OFF_BRAND = ("#ff3b3b", "#ffb000", "#00e0c6", "#ff5a5a")  # the v1 invented palette


class WrapBoardTests(unittest.TestCase):
    def test_fits_geometry_and_uppercases(self):
        rows = wrap_board("the model is the message")
        self.assertIsNotNone(rows)
        self.assertLessEqual(len(rows), MAX_LINES)
        for r in rows:
            self.assertLessEqual(len(r), MAX_LINE_CHARS)
            self.assertEqual(r, r.upper())

    def test_rejects_unwrappable(self):
        self.assertIsNone(wrap_board("supercalifragilisticexpialidocious"))  # word > line
        self.assertIsNone(wrap_board("one two three four five six seven eight nine ten"))  # > MAX_LINES


class RenderTests(unittest.TestCase):
    def test_cells_prerendered_no_js_safe(self):
        section = render.board_section(["THE MODEL", "IS THE", "MESSAGE"], "now showing", "led")
        # letters present in markup (visible without JS), with a final-value hook for the flip
        self.assertIn('data-final="T"', section)
        self.assertIn(">T</div>", section)
        self.assertIn('role="img"', section)
        self.assertIn('aria-label="THE MODEL IS THE MESSAGE"', section)

    def test_animation_is_single_source_and_motion_safe(self):
        js = render.theme_js()
        self.assertIn("kkmHydrate", js)
        self.assertIn("prefers-reduced-motion", js)

    def test_on_brand_tokens_not_invented_hex(self):
        css = render.BOARD_RULES + render.TOKENS_WP + render.TOKENS_DIST
        self.assertIn("--wp--preset--color--signal", render.TOKENS_WP)
        self.assertIn("var(--kkm-signal)", render.BOARD_RULES)
        for hexv in OFF_BRAND:
            self.assertNotIn(hexv, css)


class ThemeIntegrationTests(unittest.TestCase):
    def test_generated_partial_is_loop_output(self):
        partial = (THEME / "parts/marquee-current.html").read_text(encoding="utf-8")
        self.assertIn("kkm-board", partial)
        self.assertIn("data-final=", partial)                 # pre-rendered
        self.assertIn("--wp--preset--color--signal", partial)  # on-brand tokens
        self.assertNotIn("<script", partial)                   # animation is external/deferred
        for hexv in OFF_BRAND:
            self.assertNotIn(hexv, partial)

    def test_hero_pattern_is_thin_wrapper(self):
        pattern = (THEME / "patterns/marquee-hero.php").read_text(encoding="utf-8")
        self.assertIn("marquee-current.html", pattern)         # includes the generated partial
        self.assertNotIn("setInterval", pattern)               # no inline animation in the hero


if __name__ == "__main__":
    unittest.main()
