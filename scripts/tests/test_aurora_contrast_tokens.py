import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
THEME_DIR = ROOT / "theme/kk-aurora"


def contrast_ratio(foreground, background):
    def relative_luminance(hex_color):
        color = hex_color.lstrip("#")
        channels = [int(color[index : index + 2], 16) / 255 for index in (0, 2, 4)]

        def linearize(channel):
            if channel <= 0.03928:
                return channel / 12.92
            return ((channel + 0.055) / 1.055) ** 2.4

        red, green, blue = [linearize(channel) for channel in channels]
        return 0.2126 * red + 0.7152 * green + 0.0722 * blue

    lighter, darker = sorted(
        [relative_luminance(foreground), relative_luminance(background)],
        reverse=True,
    )
    return (lighter + 0.05) / (darker + 0.05)


class AuroraContrastTokenTests(unittest.TestCase):
    def setUp(self):
        theme = json.loads((THEME_DIR / "theme.json").read_text(encoding="utf-8"))
        palette = theme["settings"]["color"]["palette"]
        self.colors = {entry["slug"]: entry["color"] for entry in palette}

    def test_text_tokens_meet_wcag_aa_on_dark_surfaces(self):
        foregrounds = ("text-primary", "text-secondary", "text-muted", "signal")
        backgrounds = ("deep", "surface", "elevated", "muted")

        failures = []
        for foreground in foregrounds:
            for background in backgrounds:
                ratio = contrast_ratio(self.colors[foreground], self.colors[background])
                if ratio < 4.5:
                    failures.append(f"{foreground} on {background}: {ratio:.2f}:1")

        self.assertEqual(failures, [])

    def test_css_signal_token_matches_theme_palette(self):
        css = (THEME_DIR / "style.css").read_text(encoding="utf-8")
        match = re.search(r"--aurora-signal:\s*(#[0-9a-fA-F]{6});", css)

        self.assertIsNotNone(match)
        self.assertEqual(match.group(1).upper(), self.colors["signal"].upper())

    def test_primary_cta_control_colors_meet_wcag_aa(self):
        css = (THEME_DIR / "style.css").read_text(encoding="utf-8")
        control_colors = re.findall(r"--aurora-signal-control(?:-hover)?:\s*(#[0-9a-fA-F]{6});", css)

        self.assertEqual(len(control_colors), 2)
        for color in control_colors:
            self.assertGreaterEqual(contrast_ratio("#FFFAF6", color), 4.5)


if __name__ == "__main__":
    unittest.main()
