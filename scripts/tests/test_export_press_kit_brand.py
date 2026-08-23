import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import export_press_kit_brand as exporter  # noqa: E402


GENERATED_AT = "2026-08-23T01:00:00Z"


def fixture_theme() -> dict:
    return {
        "settings": {
            "layout": {"contentSize": "40rem", "wideSize": "64rem"},
            "color": {
                "palette": [
                    {"slug": "paper", "name": "Paper", "color": "#f5f0e6"},
                    {"slug": "surface", "name": "Panel", "color": "#e9e0cf"},
                    {"slug": "elevated", "name": "Raised", "color": "#eee5d5"},
                    {"slug": "text-primary", "name": "Ink", "color": "#191512"},
                    {"slug": "text-secondary", "name": "Ink Secondary", "color": "#40372f"},
                    {"slug": "text-muted", "name": "Ink Muted", "color": "#61564b"},
                    {"slug": "signal", "name": "Signal", "color": "#a4381e"},
                    {"slug": "signal-text", "name": "Signal Text", "color": "#8c2d18"},
                    {"slug": "muted", "name": "Line", "color": "#d8ccb6"},
                    {"slug": "deep", "name": "Button Ink", "color": "#f5f0e6"},
                    {"slug": "success", "name": "Success", "color": "#267e76"},
                    {"slug": "warning", "name": "Warning", "color": "#dba52e"},
                    {"slug": "error", "name": "Error", "color": "#c94321"},
                ],
                "gradients": [
                    {
                        "slug": "legacy-neon",
                        "name": "Legacy Neon",
                        "gradient": "linear-gradient(#00E5FF, #0D0D12)",
                    }
                ],
                "duotone": [
                    {"slug": "legacy-duo", "name": "Legacy Duo", "colors": ["#0D0D12", "#00E5FF"]}
                ],
            },
            "typography": {
                "fontFamilies": [
                    {"slug": "display", "name": "Display", "fontFamily": "Example Display, sans-serif"},
                    {"slug": "body", "name": "Body", "fontFamily": "Example Body, sans-serif"},
                ],
                "fontSizes": [
                    {
                        "slug": "base",
                        "name": "Base",
                        "size": "1rem",
                        "fluid": {"min": "1rem", "max": "1.125rem"},
                    },
                    {"slug": "xl", "name": "Extra Large", "size": "1.25rem"},
                ],
            },
            "spacing": {
                "spacingSizes": [
                    {"slug": "20", "name": "2", "size": "0.5rem"},
                    {"slug": "60", "name": "6", "size": "1.5rem"},
                ]
            },
            "shadow": {
                "presets": [
                    {"slug": "sm", "name": "Small", "shadow": "0 1px 2px rgb(0 0 0 / 20%)"}
                ]
            },
            "custom": {
                "border": {"radiusSm": "0.25rem", "radiusMd": "0.5rem"},
                "button": {
                    "paddingInline": "var(--wp--preset--spacing--60)",
                    "paddingBlock": "var(--wp--preset--spacing--20)",
                    "radius": "var(--wp--custom--border--radius-md)",
                    "minHeight": "44px",
                },
            },
        },
        "styles": {
            "elements": {
                "button": {
                    "color": {
                        "background": "var(--wp--preset--color--signal)",
                        "text": "var(--wp--preset--color--deep)",
                    },
                    "typography": {"fontWeight": "600"},
                }
            }
        },
    }


TOKENS_CSS = """@layer tokens {
  :root {
    --kk-surface: var(--wp--preset--color--paper);
    --kk-surface-sunk: var(--wp--preset--color--surface);
    --kk-surface-raised: var(--wp--preset--color--elevated);
    --kk-ink: var(--wp--preset--color--text-primary);
    --kk-ink-secondary: var(--wp--preset--color--text-secondary);
    --kk-ink-muted: var(--wp--preset--color--text-muted);
    --kk-accent: var(--wp--preset--color--signal);
    --kk-accent-ink: var(--wp--preset--color--signal-text);
    --kk-line: var(--wp--preset--color--muted);
    --kk-measure: 66ch;
    --kk-bp-sm: 480px;
    --kk-bp-md: 768px;
    --kk-bp-lg: 1200px;
  }
}
"""


def write_fixture(repo_root: Path) -> exporter.ExportPaths:
    paths = exporter.ExportPaths.from_root(repo_root)
    paths.theme_json.parent.mkdir(parents=True)
    paths.tokens_css.parent.mkdir(parents=True)
    paths.output_json.parent.mkdir(parents=True)
    paths.theme_json.write_text(json.dumps(fixture_theme()), encoding="utf-8")
    paths.tokens_css.write_text(TOKENS_CSS, encoding="utf-8")
    paths.style_css.write_text("/*\nTheme Name: Fixture Aurora\nVersion: 9.8.7\n*/\n", encoding="utf-8")
    return paths


def guidance_items(value):
    if isinstance(value, dict):
        if "value" in value and "provenance" in value:
            yield value
            return
        for child in value.values():
            yield from guidance_items(child)
    elif isinstance(value, list):
        for child in value:
            yield from guidance_items(child)


class SourceLoadingTests(unittest.TestCase):
    def test_loads_theme_version_and_semantic_aliases(self):
        with tempfile.TemporaryDirectory() as tmp:
            sources = exporter.load_sources(write_fixture(Path(tmp)))

        self.assertEqual(sources.theme_name, "Fixture Aurora")
        self.assertEqual(sources.theme_version, "9.8.7")
        self.assertEqual(
            sources.css_tokens["--kk-surface"],
            "var(--wp--preset--color--paper)",
        )


class ReferenceBuildTests(unittest.TestCase):
    def test_output_order_and_role_mapping_are_stable(self):
        with tempfile.TemporaryDirectory() as tmp:
            sources = exporter.load_sources(write_fixture(Path(tmp)))
            first = exporter.build_reference(sources, GENERATED_AT)
            second = exporter.build_reference(sources, GENERATED_AT)

        self.assertEqual(
            [item["id"] for item in first["colors"]["surfaces"]],
            ["surface", "surface_sunk", "surface_raised"],
        )
        self.assertEqual(first, second)
        self.assertEqual(first["colors"]["surfaces"][0]["value"], "#f5f0e6")
        self.assertEqual(
            [source["token"] for source in first["colors"]["surfaces"][0]["provenance"]],
            ["--kk-surface", "--wp--preset--color--paper"],
        )

    def test_every_guidance_item_points_to_an_existing_source_token(self):
        with tempfile.TemporaryDirectory() as tmp:
            sources = exporter.load_sources(write_fixture(Path(tmp)))
            reference = exporter.build_reference(sources, GENERATED_AT)
            available = exporter.available_source_tokens(sources)

        items = list(guidance_items(reference))
        self.assertGreater(len(items), 20)
        for item in items:
            with self.subTest(item=item["id"]):
                self.assertTrue(item["provenance"])
                for source in item["provenance"]:
                    self.assertIn((source["path"], source["token"]), available)

    def test_committed_sources_support_every_exported_provenance(self):
        repo_root = Path(__file__).resolve().parents[2]
        sources = exporter.load_sources(exporter.ExportPaths.from_root(repo_root))
        reference = exporter.build_reference(sources, GENERATED_AT)
        available = exporter.available_source_tokens(sources)

        for item in guidance_items(reference):
            with self.subTest(item=item["id"]):
                for source in item["provenance"]:
                    self.assertIn((source["path"], source["token"]), available)

    def test_missing_categories_are_reported_without_exporting_old_neon_values(self):
        with tempfile.TemporaryDirectory() as tmp:
            sources = exporter.load_sources(write_fixture(Path(tmp)))
            reference = exporter.build_reference(sources, GENERATED_AT)

        missing = {item["concept"]: item["status"] for item in reference["missing_or_noncanonical"]}
        serialized = json.dumps(reference)
        self.assertEqual(missing["icon_system"], "missing")
        self.assertEqual(missing["brand_gradients"], "noncanonical_for_press_kit")
        self.assertEqual(missing["duotone_treatments"], "noncanonical_for_press_kit")
        self.assertNotIn("#00E5FF", serialized)
        self.assertNotIn("#0D0D12", serialized)


class CheckModeTests(unittest.TestCase):
    def test_check_passes_then_fails_when_a_source_token_drifts(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp)
            paths = write_fixture(repo_root)
            exporter.write_export(paths, generated_at=GENERATED_AT)

            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                self.assertEqual(exporter.main(["--repo-root", str(repo_root), "--check"]), 0)

            theme = json.loads(paths.theme_json.read_text(encoding="utf-8"))
            theme["settings"]["color"]["palette"][0]["color"] = "#ffffff"
            paths.theme_json.write_text(json.dumps(theme), encoding="utf-8")
            committed_json = paths.output_json.read_text(encoding="utf-8")
            committed_markdown = paths.output_markdown.read_text(encoding="utf-8")

            stderr = io.StringIO()
            with redirect_stdout(io.StringIO()), redirect_stderr(stderr):
                result = exporter.main(["--repo-root", str(repo_root), "--check"])
            checked_json = paths.output_json.read_text(encoding="utf-8")
            checked_markdown = paths.output_markdown.read_text(encoding="utf-8")

        self.assertEqual(result, 1)
        self.assertIn("brand-reference.json", stderr.getvalue())
        self.assertIn("brand-reference.md", stderr.getvalue())
        self.assertEqual(checked_json, committed_json)
        self.assertEqual(checked_markdown, committed_markdown)


if __name__ == "__main__":
    unittest.main()
