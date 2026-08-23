#!/usr/bin/env python3
"""Export canonical Aurora brand data for the press kit."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


THEME_JSON = "theme/kk-aurora/theme.json"
TOKENS_CSS = "theme/kk-aurora/assets/css/02-tokens.css"
STYLE_CSS = "theme/kk-aurora/style.css"
OUTPUT_JSON = "content/source-packs/content-architecture-2026/press-kit/brand-reference.json"
OUTPUT_MARKDOWN = "content/source-packs/content-architecture-2026/press-kit/brand-reference.md"

CSS_DECLARATION = re.compile(r"^\s*(--kk-[a-z0-9-]+)\s*:\s*([^;]+);", re.MULTILINE)
CSS_REFERENCE = re.compile(r"^var\((--[a-z0-9-]+)\)$")


class ExportError(ValueError):
    pass


@dataclass(frozen=True)
class ExportPaths:
    repo_root: Path
    theme_json: Path
    tokens_css: Path
    style_css: Path
    output_json: Path
    output_markdown: Path

    @classmethod
    def from_root(cls, repo_root: Path) -> "ExportPaths":
        root = repo_root.resolve()
        return cls(
            repo_root=root,
            theme_json=root / THEME_JSON,
            tokens_css=root / TOKENS_CSS,
            style_css=root / STYLE_CSS,
            output_json=root / OUTPUT_JSON,
            output_markdown=root / OUTPUT_MARKDOWN,
        )


@dataclass(frozen=True)
class Sources:
    paths: ExportPaths
    theme: dict[str, Any]
    tokens_text: str
    style_text: str
    css_tokens: dict[str, str]
    theme_name: str
    theme_version: str
    registry: dict[str, dict[str, Any]]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ExportError(f"cannot read {path}: {exc}") from exc


def parse_header_value(style_text: str, field: str) -> str:
    match = re.search(rf"^\s*{re.escape(field)}:\s*(.+?)\s*$", style_text, re.MULTILINE)
    if not match:
        raise ExportError(f"style.css has no {field} header")
    return match.group(1)


def parse_css_tokens(tokens_text: str) -> dict[str, str]:
    return {name: value.strip() for name, value in CSS_DECLARATION.findall(tokens_text)}


def kebab_case(name: str) -> str:
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", name)
    value = re.sub(r"([A-Za-z])(\d+)", r"\1-\2", value)
    value = re.sub(r"(\d+)([A-Za-z])", r"\1-\2", value)
    return value.lower()


def source(path: str, token: str, location: str | None = None) -> dict[str, str]:
    result = {"path": path, "token": token}
    if location:
        result["location"] = location
    return result


def build_registry(theme: dict[str, Any]) -> dict[str, dict[str, Any]]:
    settings = theme.get("settings", {})
    registry: dict[str, dict[str, Any]] = {}

    preset_specs = (
        (settings.get("color", {}).get("palette", []), "color", "color", "settings.color.palette"),
        (
            settings.get("typography", {}).get("fontFamilies", []),
            "font-family",
            "fontFamily",
            "settings.typography.fontFamilies",
        ),
        (
            settings.get("typography", {}).get("fontSizes", []),
            "font-size",
            "size",
            "settings.typography.fontSizes",
        ),
        (
            settings.get("spacing", {}).get("spacingSizes", []),
            "spacing",
            "size",
            "settings.spacing.spacingSizes",
        ),
        (
            settings.get("shadow", {}).get("presets", []),
            "shadow",
            "shadow",
            "settings.shadow.presets",
        ),
    )
    for entries, preset_type, value_key, location in preset_specs:
        for entry in entries:
            slug = entry["slug"]
            token = f"--wp--preset--{preset_type}--{slug}"
            registry[token] = {
                "value": entry[value_key],
                "source": source(THEME_JSON, token, f"{location}[slug={slug}]"),
            }

    def walk_custom(value: Any, key_parts: list[str], json_parts: list[str]) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                walk_custom(child, [*key_parts, kebab_case(key)], [*json_parts, key])
            return
        token = "--wp--custom--" + "--".join(key_parts)
        registry[token] = {
            "value": value,
            "source": source(THEME_JSON, token, ".".join(json_parts)),
        }

    walk_custom(settings.get("custom", {}), [], ["settings", "custom"])
    return registry


def load_sources(paths: ExportPaths) -> Sources:
    theme_text = read_text(paths.theme_json)
    tokens_text = read_text(paths.tokens_css)
    style_text = read_text(paths.style_css)
    try:
        theme = json.loads(theme_text)
    except json.JSONDecodeError as exc:
        raise ExportError(f"invalid JSON in {paths.theme_json}: {exc}") from exc

    css_tokens = parse_css_tokens(tokens_text)
    if not css_tokens:
        raise ExportError(f"no --kk-* tokens found in {paths.tokens_css}")
    return Sources(
        paths=paths,
        theme=theme,
        tokens_text=tokens_text,
        style_text=style_text,
        css_tokens=css_tokens,
        theme_name=parse_header_value(style_text, "Theme Name"),
        theme_version=parse_header_value(style_text, "Version"),
        registry=build_registry(theme),
    )


def resolve_value(raw_value: Any, registry: dict[str, dict[str, Any]]) -> tuple[Any, list[dict[str, str]]]:
    value = raw_value
    provenance: list[dict[str, str]] = []
    visited: set[str] = set()
    while isinstance(value, str):
        match = CSS_REFERENCE.fullmatch(value.strip())
        if not match:
            break
        token = match.group(1)
        if token in visited:
            raise ExportError(f"circular token reference: {token}")
        visited.add(token)
        if token not in registry:
            raise ExportError(f"unresolved canonical token: {token}")
        definition = registry[token]
        provenance.append(definition["source"])
        value = definition["value"]
    return value, provenance


def item(item_id: str, name: str, value: Any, provenance: list[dict[str, str]]) -> dict[str, Any]:
    if not provenance:
        raise ExportError(f"{item_id} has no canonical provenance")
    return {"id": item_id, "name": name, "value": value, "provenance": provenance}


def semantic_item(sources: Sources, item_id: str, name: str, alias: str) -> dict[str, Any]:
    if alias not in sources.css_tokens:
        raise ExportError(f"missing semantic token: {alias}")
    value, resolved_sources = resolve_value(sources.css_tokens[alias], sources.registry)
    return item(
        item_id,
        name,
        value,
        [source(TOKENS_CSS, alias), *resolved_sources],
    )


def preset_item(
    sources: Sources,
    preset_type: str,
    entry: dict[str, Any],
    value: Any,
) -> dict[str, Any]:
    token = f"--wp--preset--{preset_type}--{entry['slug']}"
    if token not in sources.registry:
        raise ExportError(f"missing preset token: {token}")
    return item(entry["slug"], entry["name"], value, [sources.registry[token]["source"]])


def css_literal_item(sources: Sources, item_id: str, name: str, token: str) -> dict[str, Any]:
    if token not in sources.css_tokens:
        raise ExportError(f"missing canonical token: {token}")
    value, resolved_sources = resolve_value(sources.css_tokens[token], sources.registry)
    return item(item_id, name, value, [source(TOKENS_CSS, token), *resolved_sources])


def nested_value(data: dict[str, Any], keys: tuple[str, ...]) -> Any | None:
    value: Any = data
    for key in keys:
        if not isinstance(value, dict) or key not in value:
            return None
        value = value[key]
    return value


def direct_theme_item(
    sources: Sources,
    item_id: str,
    name: str,
    keys: tuple[str, ...],
) -> dict[str, Any] | None:
    raw_value = nested_value(sources.theme, keys)
    if raw_value is None:
        return None
    token = ".".join(keys)
    value, resolved_sources = resolve_value(raw_value, sources.registry)
    return item(
        item_id,
        name,
        value,
        [source(THEME_JSON, token, token), *resolved_sources],
    )


def custom_item(
    sources: Sources,
    item_id: str,
    name: str,
    key_parts: tuple[str, ...],
) -> dict[str, Any] | None:
    keys = ("settings", "custom", *key_parts)
    raw_value = nested_value(sources.theme, keys)
    if raw_value is None:
        return None
    token = ".".join(keys)
    value, resolved_sources = resolve_value(raw_value, sources.registry)
    return item(
        item_id,
        name,
        value,
        [source(THEME_JSON, token, token), *resolved_sources],
    )


def compact(items: list[dict[str, Any] | None]) -> list[dict[str, Any]]:
    return [entry for entry in items if entry is not None]


def missing_categories(theme: dict[str, Any]) -> list[dict[str, Any]]:
    color = theme.get("settings", {}).get("color", {})
    gradients = color.get("gradients", [])
    duotones = color.get("duotone", [])
    return [
        {
            "concept": "icon_system",
            "status": "missing",
            "reason": "The canonical Aurora sources do not define an icon family or usage rules.",
            "checked_sources": [THEME_JSON, TOKENS_CSS],
        },
        {
            "concept": "logo_usage_rules",
            "status": "missing",
            "reason": "Logo files, clear-space rules, and lockups belong to the rights-cleared asset manifest.",
            "checked_sources": [THEME_JSON, TOKENS_CSS],
        },
        {
            "concept": "photography_treatment",
            "status": "missing",
            "reason": "The canonical Aurora token sources do not define editorial photography rules.",
            "checked_sources": [THEME_JSON, TOKENS_CSS],
        },
        {
            "concept": "brand_gradients",
            "status": "noncanonical_for_press_kit" if gradients else "missing",
            "reason": (
                "Gradient presets exist in theme.json but have no current --kk-* semantic role; "
                "they are intentionally omitted from press-kit guidance."
                if gradients
                else "No canonical brand-gradient system is defined."
            ),
            "checked_sources": [THEME_JSON, TOKENS_CSS],
        },
        {
            "concept": "duotone_treatments",
            "status": "noncanonical_for_press_kit" if duotones else "missing",
            "reason": (
                "Duotone presets exist in theme.json but have no current --kk-* semantic role; "
                "they are intentionally omitted from press-kit guidance."
                if duotones
                else "No canonical duotone treatment is defined."
            ),
            "checked_sources": [THEME_JSON, TOKENS_CSS],
        },
    ]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_reference(sources: Sources, generated_at: str) -> dict[str, Any]:
    settings = sources.theme.get("settings", {})
    color = settings.get("color", {})
    typography = settings.get("typography", {})

    font_families = [
        preset_item(sources, "font-family", entry, entry["fontFamily"])
        for entry in typography.get("fontFamilies", [])
    ]
    type_scale = []
    for entry in typography.get("fontSizes", []):
        value: dict[str, Any] = {"default": entry["size"]}
        if isinstance(entry.get("fluid"), dict):
            value["fluid_min"] = entry["fluid"].get("min")
            value["fluid_max"] = entry["fluid"].get("max")
        type_scale.append(preset_item(sources, "font-size", entry, value))

    layout = compact(
        [
            direct_theme_item(sources, "content_width", "Content width", ("settings", "layout", "contentSize")),
            direct_theme_item(sources, "wide_width", "Wide width", ("settings", "layout", "wideSize")),
            css_literal_item(sources, "measure", "Reading measure", "--kk-measure"),
        ]
    )
    breakpoints = [
        css_literal_item(sources, "small", "Small", "--kk-bp-sm"),
        css_literal_item(sources, "medium", "Medium", "--kk-bp-md"),
        css_literal_item(sources, "large", "Large", "--kk-bp-lg"),
    ]

    spacing = [
        preset_item(sources, "spacing", entry, entry["size"])
        for entry in settings.get("spacing", {}).get("spacingSizes", [])
    ]
    radius_names = {
        "radiusSm": "Small",
        "radiusMd": "Medium",
        "radiusLg": "Large",
        "radiusXl": "Extra Large",
        "radius2xl": "2X Large",
        "radiusFull": "Full / pill",
    }
    radii = compact(
        [custom_item(sources, kebab_case(key), radius_names.get(key, key), ("border", key)) for key in settings.get("custom", {}).get("border", {})]
    )
    shadows = [
        preset_item(sources, "shadow", entry, entry["shadow"])
        for entry in settings.get("shadow", {}).get("presets", [])
    ]

    button_style_specs = (
        ("background", "Background", ("styles", "elements", "button", "color", "background")),
        ("text", "Text", ("styles", "elements", "button", "color", "text")),
        ("font_family", "Font family", ("styles", "elements", "button", "typography", "fontFamily")),
        ("font_size", "Font size", ("styles", "elements", "button", "typography", "fontSize")),
        ("font_weight", "Font weight", ("styles", "elements", "button", "typography", "fontWeight")),
        ("letter_spacing", "Letter spacing", ("styles", "elements", "button", "typography", "letterSpacing")),
    )
    button_custom_names = {
        "paddingInline": "Inline padding",
        "paddingBlock": "Block padding",
        "radius": "Radius",
        "radiusPill": "Pill radius",
        "minHeight": "Minimum height",
        "mobileMinHeight": "Mobile minimum height",
        "iconSize": "Icon size",
    }
    buttons = compact(
        [direct_theme_item(sources, item_id, name, keys) for item_id, name, keys in button_style_specs]
        + [
            custom_item(sources, kebab_case(key), button_custom_names.get(key, key), ("button", key))
            for key in settings.get("custom", {}).get("button", {})
        ]
    )

    theme_name = item(
        "theme_name",
        "Theme name",
        sources.theme_name,
        [source(STYLE_CSS, "Theme Name")],
    )
    theme_version = item(
        "theme_version",
        "Theme version",
        sources.theme_version,
        [source(STYLE_CSS, "Version")],
    )

    return {
        "schema_version": 1,
        "metadata": {
            "generated_at_utc": generated_at,
            "timestamp_policy": "--check reuses the committed timestamp so clock time never creates drift.",
            "theme": {"name": theme_name, "version": theme_version},
            "source_files": [
                {"path": THEME_JSON, "sha256": sha256(sources.paths.theme_json)},
                {"path": TOKENS_CSS, "sha256": sha256(sources.paths.tokens_css)},
                {"path": STYLE_CSS, "sha256": sha256(sources.paths.style_css)},
            ],
            "publication_gate": (
                "This exporter reads repository sources only. Before publication, run make status-readonly "
                "and verify that live and repository Aurora versions agree."
            ),
        },
        "colors": {
            "surfaces": [
                semantic_item(sources, "surface", "Primary surface", "--kk-surface"),
                semantic_item(sources, "surface_sunk", "Sunk surface", "--kk-surface-sunk"),
                semantic_item(sources, "surface_raised", "Raised surface", "--kk-surface-raised"),
            ],
            "ink_text": [
                semantic_item(sources, "ink", "Primary ink", "--kk-ink"),
                semantic_item(sources, "ink_secondary", "Secondary ink", "--kk-ink-secondary"),
                semantic_item(sources, "ink_muted", "Muted ink", "--kk-ink-muted"),
            ],
            "accent_action": [
                semantic_item(sources, "accent", "Primary accent", "--kk-accent"),
                semantic_item(sources, "accent_ink", "Accent text", "--kk-accent-ink"),
            ],
            "semantic": [
                semantic_item(sources, "line", "Structure / line", "--kk-line"),
                *[
                    preset_item(sources, "color", entry, entry["color"])
                    for entry in color.get("palette", [])
                    if entry.get("slug") in {"success", "warning", "error"}
                ],
            ],
        },
        "typography": {"font_families": font_families, "type_scale": type_scale},
        "layout": {"widths": layout, "breakpoints": breakpoints},
        "foundations": {"spacing": spacing, "radii": radii, "shadows": shadows},
        "buttons": buttons,
        "missing_or_noncanonical": missing_categories(sources.theme),
    }


def flatten_json_tokens(value: Any, parts: tuple[str, ...] = ()) -> set[str]:
    tokens: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            tokens.update(flatten_json_tokens(child, (*parts, key)))
    elif not isinstance(value, list) and parts:
        tokens.add(".".join(parts))
    return tokens


def available_source_tokens(sources: Sources) -> set[tuple[str, str]]:
    available = {(TOKENS_CSS, token) for token in sources.css_tokens}
    available.update((THEME_JSON, token) for token in flatten_json_tokens(sources.theme))
    available.update((THEME_JSON, token) for token in sources.registry)
    available.update({(STYLE_CSS, "Theme Name"), (STYLE_CSS, "Version")})
    return available


def source_label(entry: dict[str, str]) -> str:
    aliases = {THEME_JSON: "theme.json", TOKENS_CSS: "02-tokens.css", STYLE_CSS: "style.css"}
    return f"{aliases[entry['path']]} `{entry['token']}`"


def display_value(value: Any) -> str:
    if isinstance(value, dict):
        default = value.get("default", "")
        minimum = value.get("fluid_min")
        maximum = value.get("fluid_max")
        if minimum and maximum:
            return f"{default} (fluid {minimum}–{maximum})"
        return str(default)
    return str(value)


def render_table(items: list[dict[str, Any]]) -> str:
    if not items:
        return "_No canonical values found._\n"
    lines = ["| Role | Value | Source |", "|---|---|---|"]
    for entry in items:
        provenance = " → ".join(source_label(value) for value in entry["provenance"])
        lines.append(f"| {entry['name']} | `{display_value(entry['value'])}` | {provenance} |")
    return "\n".join(lines) + "\n"


def render_markdown(reference: dict[str, Any]) -> str:
    metadata = reference["metadata"]
    theme = metadata["theme"]
    lines = [
        "# Aurora Brand Reference",
        "",
        (
            f"Generated {metadata['generated_at_utc']} from "
            f"{theme['name']['value']} {theme['version']['value']}."
        ),
        "",
        "This is a repository-derived reference, not proof of the live theme. "
        "Before publication, run `make status-readonly` and confirm live/repo Aurora version agreement.",
        "",
        "Source aliases:",
        "",
        f"- `theme.json`: `{THEME_JSON}`",
        f"- `02-tokens.css`: `{TOKENS_CSS}`",
        f"- `style.css`: `{STYLE_CSS}`",
        "",
    ]

    sections = (
        ("Surfaces", reference["colors"]["surfaces"]),
        ("Ink and text", reference["colors"]["ink_text"]),
        ("Accent and action", reference["colors"]["accent_action"]),
        ("Semantic colors", reference["colors"]["semantic"]),
        ("Font families", reference["typography"]["font_families"]),
        ("Type scale", reference["typography"]["type_scale"]),
        ("Layout widths", reference["layout"]["widths"]),
        ("Breakpoints", reference["layout"]["breakpoints"]),
        ("Spacing", reference["foundations"]["spacing"]),
        ("Radii", reference["foundations"]["radii"]),
        ("Shadows", reference["foundations"]["shadows"]),
        ("Buttons", reference["buttons"]),
    )
    for heading, entries in sections:
        lines.extend([f"## {heading}", "", render_table(entries).rstrip(), ""])

    lines.extend(
        [
            "## Missing or noncanonical",
            "",
            "| Concept | Status | Why |",
            "|---|---|---|",
        ]
    )
    for entry in reference["missing_or_noncanonical"]:
        lines.append(f"| {entry['concept']} | {entry['status']} | {entry['reason']} |")
    lines.append("")
    return "\n".join(lines)


def render_json(reference: dict[str, Any]) -> str:
    return json.dumps(reference, indent=2, ensure_ascii=False) + "\n"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rendered_export(paths: ExportPaths, generated_at: str) -> tuple[str, str]:
    reference = build_reference(load_sources(paths), generated_at)
    return render_json(reference), render_markdown(reference)


def write_export(paths: ExportPaths, generated_at: str | None = None) -> None:
    json_text, markdown_text = rendered_export(paths, generated_at or utc_now())
    paths.output_json.parent.mkdir(parents=True, exist_ok=True)
    paths.output_json.write_text(json_text, encoding="utf-8")
    paths.output_markdown.write_text(markdown_text, encoding="utf-8")


def committed_timestamp(path: Path) -> str:
    try:
        reference = json.loads(path.read_text(encoding="utf-8"))
        value = reference["metadata"]["generated_at_utc"]
    except (OSError, json.JSONDecodeError, KeyError, TypeError):
        return "1970-01-01T00:00:00Z"
    return value if isinstance(value, str) else "1970-01-01T00:00:00Z"


def check_export(paths: ExportPaths) -> list[Path]:
    generated_at = committed_timestamp(paths.output_json)
    expected_json, expected_markdown = rendered_export(paths, generated_at)
    expected = {
        paths.output_json: expected_json,
        paths.output_markdown: expected_markdown,
    }
    drifted = []
    for path, content in expected.items():
        try:
            current = path.read_text(encoding="utf-8")
        except OSError:
            current = None
        if current != content:
            drifted.append(path)
    return drifted


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if generated references are stale")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help=argparse.SUPPRESS,
    )
    parser.add_argument("--generated-at", help=argparse.SUPPRESS)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    paths = ExportPaths.from_root(args.repo_root)
    try:
        if args.check:
            drifted = check_export(paths)
            if drifted:
                for path in drifted:
                    print(f"DRIFT: {path.relative_to(paths.repo_root)}", file=sys.stderr)
                return 1
            print("PASS: press-kit brand references match canonical Aurora sources")
            return 0
        write_export(paths, generated_at=args.generated_at)
    except ExportError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(f"WROTE: {OUTPUT_JSON}")
    print(f"WROTE: {OUTPUT_MARKDOWN}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
