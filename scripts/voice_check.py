#!/usr/bin/env python3
"""Gate mechanically decidable voice rules in payload and Aurora copy (#747).

The default scan covers publishable draft payloads plus user-visible Aurora
templates, parts, patterns, and the theme-owned document-title source in
``theme/kk-aurora/functions.php`` (#756). Comments are excluded.

Waivers in ``.voice-waivers.json`` are pinned to an exact file SHA-256. A file
edit invalidates its waiver, so new violations fail. Removing all violations
passes without requiring a coordinated waiver edit in another PR.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
WAIVER_PATH = REPO_ROOT / ".voice-waivers.json"
EM_DASH = "\u2014"
PAYLOAD_ROOT = Path("content/drafts")
PAYLOAD_NAMES = {"post.md", "post.html", "post-body.html", "copy.md"}
THEME_FILES = (Path("theme/kk-aurora/functions.php"),)
THEME_DIRS = tuple(
    Path("theme/kk-aurora") / name for name in ("templates", "parts", "patterns")
)
RULES = (
    ("em-dash", re.compile(re.escape(EM_DASH)), "em dash; rewrite as a colon, period, or comma"),
    ("slop:delve", re.compile(r"\bdelv(?:e|es|ed|ing)\b", re.I), "slop lexicon: delve"),
    ("slop:tapestry", re.compile(r"\btapestr(?:y|ies)\b", re.I), "slop lexicon: tapestry"),
    ("slop:testament", re.compile(r"\ba testament to\b", re.I), "slop lexicon: a testament to"),
    ("slop:nestled", re.compile(r"\bnestled\b", re.I), "slop lexicon: nestled"),
    (
        "slop:in-a-world",
        re.compile(r"(?:\A|\n)[ \t>#*_]*In a world\b"),
        'slop lexicon: "In a world" opener',
    ),
)
BLOCK_COMMENTS = (re.compile(r"<!--.*?-->", re.S), re.compile(r"/\*.*?\*/", re.S))
PHP_LINE_COMMENT = re.compile(r"(?<!:)//[^\n]*")


def blank_comments(text: str, suffix: str) -> str:
    def blank(match: re.Match) -> str:
        return "".join("\n" if char == "\n" else " " for char in match.group(0))

    for pattern in BLOCK_COMMENTS:
        text = pattern.sub(blank, text)
    return PHP_LINE_COMMENT.sub(blank, text) if suffix == ".php" else text


def scan_text(text: str, suffix: str) -> list[tuple[str, int, int, str, str]]:
    scannable = blank_comments(text, suffix)
    lines = text.split("\n")
    found = []
    for rule_id, pattern, message in RULES:
        for match in pattern.finditer(scannable):
            line = scannable.count("\n", 0, match.start()) + 1
            col = match.start() - scannable.rfind("\n", 0, match.start())
            found.append((rule_id, line, col, message, lines[line - 1].strip()[:100]))
    return sorted(found, key=lambda hit: (hit[1], hit[2]))


def default_targets() -> list[Path]:
    targets = [
        path.relative_to(REPO_ROOT)
        for path in (REPO_ROOT / PAYLOAD_ROOT).rglob("*")
        if path.name in PAYLOAD_NAMES
    ]
    targets.extend(path for path in THEME_FILES if (REPO_ROOT / path).is_file())
    for directory in THEME_DIRS:
        targets.extend(
            path.relative_to(REPO_ROOT)
            for path in (REPO_ROOT / directory).rglob("*")
            if path.is_file()
        )
    return sorted(targets)


def load_waivers() -> dict[str, dict]:
    if not WAIVER_PATH.exists():
        return {}
    data = json.loads(WAIVER_PATH.read_text(encoding="utf-8"))
    return {entry["path"]: entry for entry in data.get("waivers", [])}


def waiver_applies(waiver: dict | None, rule_id: str, digest: str) -> bool:
    if not waiver or waiver.get("sha256") != digest:
        return False
    rules = waiver.get("rules", ["*"])
    return "*" in rules or rule_id in rules


def target_key(target: Path, absolute: Path) -> str:
    try:
        return str(absolute.relative_to(REPO_ROOT))
    except ValueError:
        return str(target)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("paths", nargs="*", help="Files to scan; '-' reads stdin")
    args = parser.parse_args(argv)
    waivers = load_waivers()
    violations = []
    waived_count = 0

    if args.paths == ["-"]:
        targets = []
        violations.extend(
            ("<stdin>", *hit) for hit in scan_text(sys.stdin.read(), ".txt")
        )
    else:
        targets = [Path(path) for path in args.paths] if args.paths else default_targets()

    for target in targets:
        absolute = target if target.is_absolute() else REPO_ROOT / target
        if not absolute.is_file():
            continue
        data = absolute.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        key = target_key(target, absolute)
        waiver = waivers.get(key)
        for hit in scan_text(data.decode("utf-8", errors="replace"), absolute.suffix):
            if waiver_applies(waiver, hit[0], digest):
                waived_count += 1
            else:
                violations.append((key, *hit))

    for path, rule_id, line, col, message, excerpt in violations:
        print(f"{path}:{line}:{col}: [{rule_id}] {message}\n    {excerpt}")
    print(
        f"\nvoice-check: {len(targets) or 1} file(s) scanned, "
        f"{len(violations)} violation(s), {waived_count} baseline-waived."
    )
    print(
        "Hard rules only. Full local pass (optional):\n"
        "  python3 ~/Code/kk-voice/scripts/voicecheck.py <file>"
    )
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
