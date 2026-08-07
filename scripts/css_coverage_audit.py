#!/usr/bin/env python3
"""Read-only CSS coverage / dead-code / overlap audit for the kk-aurora theme.

Answers four questions, all measured, none guessed:

1. Which class selectors in the theme's CSS have no matching token anywhere in
   the repo's markup corpus (templates, parts, patterns, content, fixes)?
2. Which selectors are declared in more than one stylesheet (cascade overlap)?
3. Where are the ``!important`` declarations, per file?
4. Where are inline ``<style>`` blocks in the FSE templates/parts?

The script never writes to the theme and never touches WordPress. It needs no
credentials and no third-party packages -- plain ``python3`` only.

Usage::

    python3 scripts/css_coverage_audit.py                    # markdown summary
    python3 scripts/css_coverage_audit.py --format json      # machine-readable
    python3 scripts/css_coverage_audit.py --section dead     # one section only
    python3 scripts/css_coverage_audit.py --min-confidence high

Most of this site's rendered markup lives in the WordPress database, not in the
repo, so a repo-only grep over-reports dead code. Pass a directory of saved
public HTML to close that gap (fetching is out of scope for this script -- do it
yourself with ``curl`` against the public sitemap, read-only)::

    python3 scripts/css_coverage_audit.py --live-corpus /path/to/saved-html

Confidence model for "dead" findings:

* ``high``   -- class token appears nowhere in markup, PHP, JS, or the supplied
                live-HTML corpus, and is not a WordPress/core-generated shape.
                Safe removal candidate.
* ``medium`` -- token is absent as a whole word but appears as a substring
                somewhere (possible dynamic composition). Needs eyeballs.
* ``low``    -- WordPress-generated (``wp-*``, ``has-*``, ``is-*``), body/state
                class, or referenced from JS/PHP/live HTML. Do not treat as dead.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
THEME_DIR = REPO_ROOT / "theme" / "kk-aurora"

# Stylesheets audited, in the order functions.php enqueues them (later wins on
# equal specificity). Includes Aurora 1.5.0 scaffold sheets (#474): tokens,
# primitives (#476), and the deliberately-unlayered late overrides.
CSS_FILES = [
    THEME_DIR / "style.css",
    THEME_DIR / "assets" / "css" / "02-tokens.css",
    THEME_DIR / "assets" / "css" / "04-primitives.css",
    THEME_DIR / "assets" / "css" / "typography-refined.css",
    THEME_DIR / "assets" / "css" / "animations.css",
    THEME_DIR / "assets" / "css" / "bleeding-edge.css",
    THEME_DIR / "assets" / "css" / "revive-port.css",
    THEME_DIR / "assets" / "css" / "09-late.css",
    THEME_DIR / "assets" / "css" / "editor.css",
]

# Markup that a browser could actually render classes into.
MARKUP_GLOBS = [
    ("theme/kk-aurora/templates", "*.html"),
    ("theme/kk-aurora/parts", "*.html"),
    ("theme/kk-aurora/patterns", "*.php"),
    ("content", "**/*.html"),
    ("content", "**/*.md"),
    ("content", "**/*.json"),
    ("fixes", "**/*.md"),
    ("fixes", "**/*.php"),
    ("fixes", "**/*.html"),
    ("fixes", "**/*.txt"),
]

# PHP that renders markup (theme + repo-side plugins/snippets).
PHP_GLOBS = [
    ("theme/kk-aurora", "functions.php"),
    ("theme/kk-aurora/inc", "*.php"),
    ("plugins", "**/*.php"),
    ("inc", "*.php"),
]

# JS that toggles state classes at runtime.
JS_GLOBS = [
    ("theme/kk-aurora/assets/js", "*.js"),
    ("plugins", "**/*.js"),
]

# Class shapes WordPress core / the block editor generate. Never "dead" from a
# repo grep alone.
WP_GENERATED_PREFIXES = (
    "wp-",
    "has-",
    "is-",
    "editor-",
    "block-editor-",
    "components-",
    "screen-reader",
    "alignwide",
    "alignfull",
    "aligncenter",
    "alignleft",
    "alignright",
    "post-",
    "page-",
    "single-",
    "category-",
    "tag-",
    "admin-bar",
    "logged-in",
    "menu-item",
    "sub-menu",
    "current-menu",
    "entry-",
    "comment-",
    "gallery-",
    "sticky",
    "attachment-",
    "size-",
)

WP_GENERATED_EXACT = {
    "home",
    "blog",
    "archive",
    "search",
    "error404",
    "page",
    "single",
    "post",
    "hentry",
    "rtl",
    "custom-logo",
    "custom-logo-link",
    "site-title",
    "site-logo",
    "widget",
    "sidebar",
    "nav-links",
    "screen-reader-text",
    "skip-link",
}

TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_-]*")
CLASS_IN_SELECTOR_RE = re.compile(r"\.(-?[_a-zA-Z][A-Za-z0-9_-]*)")
COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)
HEX_COLOR_RE = re.compile(r"#(?:[0-9a-fA-F]{3,8})\b")
CUSTOM_PROP_RE = re.compile(r"(--[A-Za-z0-9_-]+)\s*:")


# --------------------------------------------------------------------------
# CSS parsing
# --------------------------------------------------------------------------


@dataclass
class Rule:
    """A single ``selector { ... }`` block."""

    path: Path
    line: int
    selector: str
    body: str
    at_context: str = ""

    @property
    def size(self) -> int:
        return len(self.selector) + len(self.body) + 3  # "{", "}", newline

    @property
    def selector_parts(self) -> list[str]:
        return [p.strip() for p in self.selector.split(",") if p.strip()]


def _blank_comments(text: str) -> str:
    """Replace comments with equal-length whitespace so line numbers survive."""

    def repl(m: re.Match[str]) -> str:
        return re.sub(r"[^\n]", " ", m.group(0))

    return COMMENT_RE.sub(repl, text)


def parse_css(path: Path) -> tuple[list[Rule], str]:
    """Return every style rule in ``path`` plus the comment-stripped source.

    Hand-rolled brace walker: good enough for authored CSS, and it keeps the
    script dependency-free. At-rule blocks (@media/@supports/@layer) are
    descended into; @keyframes/@font-face bodies are recorded as context only.
    """

    raw = path.read_text(encoding="utf-8")
    src = _blank_comments(raw)

    rules: list[Rule] = []
    stack: list[str] = []
    buf: list[str] = []
    line = 1
    buf_start_line = 1
    i = 0
    n = len(src)

    while i < n:
        ch = src[i]
        if ch == "\n":
            line += 1
            buf.append(ch)
            i += 1
            continue
        if ch == "{":
            prelude = "".join(buf).strip()
            prelude = re.sub(r"\s+", " ", prelude)
            # find matching close brace
            depth = 1
            j = i + 1
            while j < n and depth:
                if src[j] == "{":
                    depth += 1
                elif src[j] == "}":
                    depth -= 1
                j += 1
            body = src[i + 1 : j - 1]

            if prelude.startswith("@"):
                at_name = prelude.split()[0].lower()
                if at_name in ("@media", "@supports", "@layer", "@container", "@scope"):
                    stack.append(prelude)
                    inner_rules, _ = _parse_fragment(
                        body, path, line, " ".join(stack)
                    )
                    rules.extend(inner_rules)
                    stack.pop()
                # @keyframes / @font-face / @property: no selectors we care about
            else:
                rules.append(
                    Rule(
                        path=path,
                        line=buf_start_line if prelude else line,
                        selector=prelude,
                        body=body,
                        at_context=" ".join(stack),
                    )
                )
            line += src.count("\n", i, j)
            i = j
            buf = []
            buf_start_line = line
            continue
        if ch == "}":
            buf = []
            buf_start_line = line
            i += 1
            continue
        if not buf and not ch.isspace():
            buf_start_line = line
        buf.append(ch)
        i += 1

    return rules, src


def _parse_fragment(
    fragment: str, path: Path, base_line: int, at_context: str
) -> tuple[list[Rule], str]:
    """Parse the inside of an at-rule block, offsetting line numbers."""
    rules: list[Rule] = []
    buf: list[str] = []
    line = base_line
    buf_start_line = base_line
    i = 0
    n = len(fragment)

    while i < n:
        ch = fragment[i]
        if ch == "\n":
            line += 1
            buf.append(ch)
            i += 1
            continue
        if ch == "{":
            prelude = re.sub(r"\s+", " ", "".join(buf).strip())
            depth = 1
            j = i + 1
            while j < n and depth:
                if fragment[j] == "{":
                    depth += 1
                elif fragment[j] == "}":
                    depth -= 1
                j += 1
            body = fragment[i + 1 : j - 1]
            if prelude.startswith("@"):
                at_name = prelude.split()[0].lower()
                if at_name in ("@media", "@supports", "@layer", "@container", "@scope"):
                    inner, _ = _parse_fragment(
                        body, path, line, (at_context + " " + prelude).strip()
                    )
                    rules.extend(inner)
            elif prelude:
                rules.append(
                    Rule(
                        path=path,
                        line=buf_start_line,
                        selector=prelude,
                        body=body,
                        at_context=at_context,
                    )
                )
            line += fragment.count("\n", i, j)
            i = j
            buf = []
            buf_start_line = line
            continue
        if ch == "}":
            buf = []
            buf_start_line = line
            i += 1
            continue
        if not buf and not ch.isspace():
            buf_start_line = line
        buf.append(ch)
        i += 1

    return rules, fragment


# --------------------------------------------------------------------------
# Corpus
# --------------------------------------------------------------------------


@dataclass
class Corpus:
    tokens: set[str] = field(default_factory=set)
    blob: str = ""
    file_count: int = 0

    def has_token(self, name: str) -> bool:
        return name in self.tokens

    def has_substring(self, name: str) -> bool:
        return name in self.blob


def build_corpus(globs: list[tuple[str, str]]) -> Corpus:
    tokens: set[str] = set()
    chunks: list[str] = []
    count = 0
    for rel, pattern in globs:
        base = REPO_ROOT / rel
        if not base.exists():
            continue
        if base.is_file():
            files = [base]
        elif "**" in pattern:
            files = sorted(base.glob(pattern))
        else:
            files = sorted(base.glob(pattern))
        for f in files:
            if not f.is_file():
                continue
            try:
                text = f.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            count += 1
            chunks.append(text)
            tokens.update(TOKEN_RE.findall(text))
    return Corpus(tokens=tokens, blob="\n".join(chunks), file_count=count)


def is_wp_generated(name: str) -> bool:
    if name in WP_GENERATED_EXACT:
        return True
    return name.startswith(WP_GENERATED_PREFIXES)


# --------------------------------------------------------------------------
# Analysis
# --------------------------------------------------------------------------


@dataclass
class ClassFinding:
    name: str
    confidence: str
    reason: str
    occurrences: list[tuple[str, int, str]]  # (file, line, selector)
    bytes_in_rules: int


def build_live_corpus(directory: Path) -> Corpus:
    """Corpus from saved public HTML. Stylesheet <link>/<style> content is not
    stripped, so a class that only exists inside the CSS itself would register
    as 'used' -- we therefore strip <style> blocks before tokenising."""
    tokens: set[str] = set()
    chunks: list[str] = []
    count = 0
    for f in sorted(directory.rglob("*.html")):
        text = f.read_text(encoding="utf-8", errors="ignore")
        text = re.sub(r"<style[^>]*>.*?</style>", " ", text, flags=re.S | re.I)
        count += 1
        chunks.append(text)
        tokens.update(TOKEN_RE.findall(text))
    return Corpus(tokens=tokens, blob="\n".join(chunks), file_count=count)


def analyse(live_corpus_dir: Path | None = None) -> dict:
    markup = build_corpus(MARKUP_GLOBS)
    php = build_corpus(PHP_GLOBS)
    js = build_corpus(JS_GLOBS)
    live = (
        build_live_corpus(live_corpus_dir)
        if live_corpus_dir and live_corpus_dir.exists()
        else Corpus()
    )

    all_rules: list[Rule] = []
    per_file: dict[str, dict] = {}
    class_sites: dict[str, list[tuple[str, int, str]]] = defaultdict(list)
    class_bytes: dict[str, int] = defaultdict(int)
    selector_index: dict[str, list[tuple[str, int]]] = defaultdict(list)
    important_index: dict[str, list[tuple[int, str]]] = defaultdict(list)
    hex_index: dict[str, list[tuple[str, int]]] = defaultdict(list)
    custom_props: dict[str, list[tuple[str, int]]] = defaultdict(list)

    for css in CSS_FILES:
        if not css.exists():
            continue
        rel = str(css.relative_to(REPO_ROOT))
        rules, src = parse_css(css)
        all_rules.extend(rules)

        lines = src.splitlines()
        raw_lines = css.read_text(encoding="utf-8").splitlines()
        important = [
            (idx + 1, raw_lines[idx].strip())
            for idx, ln in enumerate(lines)
            if "!important" in ln
        ]
        important_index[rel] = important

        for idx, ln in enumerate(raw_lines):
            for m in HEX_COLOR_RE.finditer(ln):
                hex_index[m.group(0).lower()].append((rel, idx + 1))
            for m in CUSTOM_PROP_RE.finditer(ln):
                custom_props[m.group(1)].append((rel, idx + 1))

        per_file[rel] = {
            "lines": len(raw_lines),
            "bytes": css.stat().st_size,
            "rules": len(rules),
            "important_count": len(important),
        }

        for r in rules:
            norm = re.sub(r"\s+", " ", r.selector).strip()
            selector_index[norm].append((rel, r.line))
            for part in r.selector_parts:
                for cls in CLASS_IN_SELECTOR_RE.findall(part):
                    class_sites[cls].append((rel, r.line, part))
            share = r.size // max(1, len(set(CLASS_IN_SELECTOR_RE.findall(r.selector))) or 1)
            for cls in set(CLASS_IN_SELECTOR_RE.findall(r.selector)):
                class_bytes[cls] += share

    findings: list[ClassFinding] = []
    for name, sites in sorted(class_sites.items()):
        if markup.has_token(name) or live.has_token(name):
            continue  # rendered somewhere real, done
        if is_wp_generated(name):
            conf, reason = "low", "WordPress/core-generated class shape"
        elif js.has_token(name):
            conf, reason = "low", "referenced in theme/plugin JS (runtime state class)"
        elif php.has_token(name):
            conf, reason = "low", "referenced in PHP render code"
        elif (
            markup.has_substring(name)
            or php.has_substring(name)
            or js.has_substring(name)
            or live.has_substring(name)
        ):
            conf, reason = "medium", "no whole-token match; substring present (possible dynamic composition)"
        else:
            conf, reason = "high", "no token or substring match in markup, PHP, JS, or live HTML"
        findings.append(
            ClassFinding(
                name=name,
                confidence=conf,
                reason=reason,
                occurrences=sites,
                bytes_in_rules=class_bytes[name],
            )
        )

    duplicates = {
        sel: locs
        for sel, locs in selector_index.items()
        if len({loc[0] for loc in locs}) > 1
    }

    # Whole rules that are removable: every comma-part names at least one
    # high-confidence dead class, and no part is class-free (element/tag rules
    # are never proposed for removal here).
    dead_high = {f.name for f in findings if f.confidence == "high"}
    removable: list[dict] = []
    for r in all_rules:
        parts = r.selector_parts
        if not parts:
            continue
        ok = True
        touched: set[str] = set()
        for part in parts:
            classes = set(CLASS_IN_SELECTOR_RE.findall(part))
            if not classes or not (classes & dead_high):
                ok = False
                break
            touched |= classes & dead_high
        if ok:
            removable.append(
                {
                    "file": str(r.path.relative_to(REPO_ROOT)),
                    "line": r.line,
                    "selector": r.selector,
                    "at_context": r.at_context,
                    "bytes": r.size,
                    "classes": sorted(touched),
                }
            )

    # Inline <style> blocks in FSE markup
    inline_styles = []
    for rel_dir in ("theme/kk-aurora/templates", "theme/kk-aurora/parts", "theme/kk-aurora/patterns"):
        base = REPO_ROOT / rel_dir
        if not base.exists():
            continue
        for f in sorted(base.iterdir()):
            if not f.is_file():
                continue
            text = f.read_text(encoding="utf-8", errors="ignore")
            for m in re.finditer(r"<style[^>]*>(.*?)</style>", text, re.S | re.I):
                start_line = text.count("\n", 0, m.start()) + 1
                block = m.group(1)
                inline_styles.append(
                    {
                        "file": str(f.relative_to(REPO_ROOT)),
                        "start_line": start_line,
                        "lines": block.count("\n") + 1,
                        "bytes": len(m.group(0)),
                        "selectors": sorted(
                            {
                                re.sub(r"\s+", " ", s.strip())
                                for s in re.findall(r"([^{}]+)\{", _blank_comments(block))
                                if s.strip() and not s.strip().startswith("@")
                            }
                        ),
                        "important": block.count("!important"),
                    }
                )

    theme_json = REPO_ROOT / "theme" / "kk-aurora" / "theme.json"
    theme_json_colors: dict[str, str] = {}
    if theme_json.exists():
        tj = json.loads(theme_json.read_text(encoding="utf-8"))
        for pal in tj.get("settings", {}).get("color", {}).get("palette", []):
            theme_json_colors[str(pal.get("color", "")).lower()] = pal.get("slug", "")

    return {
        "per_file": per_file,
        "findings": findings,
        "duplicates": duplicates,
        "removable": removable,
        "important": important_index,
        "inline_styles": inline_styles,
        "hex_index": hex_index,
        "custom_props": custom_props,
        "theme_json_colors": theme_json_colors,
        "corpus": {
            "markup_files": markup.file_count,
            "markup_tokens": len(markup.tokens),
            "php_files": php.file_count,
            "js_files": js.file_count,
            "live_files": live.file_count,
            "live_tokens": len(live.tokens),
        },
        "total_classes": len(class_sites),
    }


# --------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------


def report_markdown(data: dict, section: str, min_conf: str) -> str:
    order = {"high": 3, "medium": 2, "low": 1}
    out: list[str] = []
    w = out.append

    if section in ("all", "summary"):
        w("## Stylesheet inventory\n")
        w("| File | Lines | Bytes | Rules | `!important` |")
        w("|---|---:|---:|---:|---:|")
        tl = tb = tr = ti = 0
        for rel, m in data["per_file"].items():
            w(f"| `{rel}` | {m['lines']} | {m['bytes']:,} | {m['rules']} | {m['important_count']} |")
            tl += m["lines"]
            tb += m["bytes"]
            tr += m["rules"]
            ti += m["important_count"]
        w(f"| **Total** | **{tl}** | **{tb:,}** | **{tr}** | **{ti}** |")
        c = data["corpus"]
        w("")
        w(
            f"Corpus scanned: {c['markup_files']} markup files "
            f"({c['markup_tokens']:,} distinct tokens), {c['php_files']} PHP files, "
            f"{c['js_files']} JS files, {c['live_files']} saved live HTML pages "
            f"({c['live_tokens']:,} distinct tokens). {data['total_classes']} "
            "distinct class selectors found in CSS.\n"
        )

    if section in ("all", "dead"):
        w("## Unmatched class selectors\n")
        buckets: dict[str, list[ClassFinding]] = defaultdict(list)
        for f in data["findings"]:
            buckets[f.confidence].append(f)
        for conf in ("high", "medium", "low"):
            items = buckets.get(conf, [])
            if order[conf] < order[min_conf]:
                continue
            w(f"### Confidence: {conf} ({len(items)} classes)\n")
            if not items:
                w("_none_\n")
                continue
            w("| Class | Bytes | Sites | Reason |")
            w("|---|---:|---|---|")
            for f in sorted(items, key=lambda x: -x.bytes_in_rules):
                sites = "; ".join(
                    f"{Path(p).name}:{ln}" for p, ln, _ in f.occurrences[:4]
                )
                if len(f.occurrences) > 4:
                    sites += f" (+{len(f.occurrences) - 4})"
                w(f"| `.{f.name}` | {f.bytes_in_rules} | {sites} | {f.reason} |")
            w("")

    if section in ("all", "candidates"):
        rem = data["removable"]
        by_file: dict[str, list[dict]] = defaultdict(list)
        for r in rem:
            by_file[r["file"]].append(r)
        total = sum(r["bytes"] for r in rem)
        w(
            f"## Fully-removable rule blocks ({len(rem)} rules, "
            f"{total:,} bytes)\n"
        )
        w("| File | Rules | Bytes |")
        w("|---|---:|---:|")
        for f, items in sorted(by_file.items(), key=lambda kv: -sum(r["bytes"] for r in kv[1])):
            w(f"| `{f}` | {len(items)} | {sum(r['bytes'] for r in items):,} |")
        w("")
        w("| File:line | Selector | Bytes |")
        w("|---|---|---:|")
        for r in sorted(rem, key=lambda x: -x["bytes"])[:60]:
            sel = r["selector"][:110]
            w(f"| `{Path(r['file']).name}:{r['line']}` | `{sel}` | {r['bytes']} |")
        w("")

    if section in ("all", "duplicates"):
        w(f"## Cross-file duplicate selectors ({len(data['duplicates'])})\n")
        w("| Selector | Declared in |")
        w("|---|---|")
        for sel, locs in sorted(
            data["duplicates"].items(), key=lambda kv: -len(kv[1])
        )[:120]:
            where = "; ".join(f"{Path(p).name}:{ln}" for p, ln in locs)
            w(f"| `{sel}` | {where} |")
        w("")

    if section in ("all", "important"):
        w("## `!important` inventory\n")
        for rel, items in data["important"].items():
            w(f"### `{rel}` — {len(items)}\n")
            for ln, txt in items[:200]:
                w(f"- L{ln}: `{txt[:120]}`")
            w("")

    if section in ("all", "inline"):
        w(f"## Inline `<style>` blocks ({len(data['inline_styles'])})\n")
        for b in data["inline_styles"]:
            w(
                f"- `{b['file']}` L{b['start_line']} — {b['lines']} lines, "
                f"{b['bytes']} bytes, {b['important']} `!important`, "
                f"selectors: {', '.join('`' + s + '`' for s in b['selectors']) or '(none)'}"
            )
        w("")

    if section in ("all", "tokens"):
        w("## Repeated hex color literals\n")
        w("| Hex | Count | In theme.json palette | Locations |")
        w("|---|---:|---|---|")
        for hx, locs in sorted(
            data["hex_index"].items(), key=lambda kv: -len(kv[1])
        )[:40]:
            if len(locs) < 2:
                continue
            slug = data["theme_json_colors"].get(hx, "")
            where = "; ".join(sorted({Path(p).name for p, _ in locs}))
            w(f"| `{hx}` | {len(locs)} | {slug or 'no'} | {where} |")
        w("")

    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--format", choices=["markdown", "json"], default="markdown")
    ap.add_argument(
        "--section",
        choices=["all", "summary", "dead", "candidates", "duplicates", "important", "inline", "tokens"],
        default="all",
    )
    ap.add_argument(
        "--min-confidence", choices=["low", "medium", "high"], default="low"
    )
    ap.add_argument(
        "--live-corpus",
        help="directory of saved public HTML pages to count as rendered markup",
    )
    ap.add_argument("--output", help="write report to this path instead of stdout")
    args = ap.parse_args(argv)

    data = analyse(Path(args.live_corpus) if args.live_corpus else None)

    if args.format == "json":
        payload = {
            "per_file": data["per_file"],
            "corpus": data["corpus"],
            "total_classes": data["total_classes"],
            "findings": [
                {
                    "class": f.name,
                    "confidence": f.confidence,
                    "reason": f.reason,
                    "bytes": f.bytes_in_rules,
                    "sites": [
                        {"file": p, "line": ln, "selector": sel}
                        for p, ln, sel in f.occurrences
                    ],
                }
                for f in data["findings"]
            ],
            "duplicates": {
                sel: [{"file": p, "line": ln} for p, ln in locs]
                for sel, locs in data["duplicates"].items()
            },
            "removable": data["removable"],
            "important": {
                rel: [{"line": ln, "text": txt} for ln, txt in items]
                for rel, items in data["important"].items()
            },
            "inline_styles": data["inline_styles"],
        }
        text = json.dumps(payload, indent=2)
    else:
        text = report_markdown(data, args.section, args.min_confidence)

    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
