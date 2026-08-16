#!/usr/bin/env python3
"""Voice gate: em dashes and a hard-rule slop lexicon in copy that ships (#747).

Scope is deliberately narrow. This is a grep-class gate on the two rules that
are mechanically decidable, not a voice-similarity scorer. The real checker
(``voicecheck.py``, crystal facets, anti-glossary) lives outside this repo in
``~/Code/kk-voice`` and stays a manual local deep pass; see ``--help`` output.

What gets scanned
-----------------

* **Payload copy**: ``content/drafts/**/{post.md,post.html,post-body.html,copy.md}``.
  Narrow on purpose: voice-audit reports, dash ledgers, and remediation READMEs
  in the same tree legitimately *discuss* em dashes and must never be flagged.
  Those files quote the character as the literal token ``{EMDASH}`` (see
  ``content/drafts/2026-08-02-emdash-remediation/dash-ledger.md``); use that
  convention rather than a waiver when you are writing *about* a dash.
* **Theme chrome**: ``theme/kk-aurora/{templates,parts,patterns}``. HTML, CSS,
  and PHP comments are blanked before matching, because a dash inside
  ``<!-- ... -->`` or a PHP docblock never reaches a reader. Getting that
  distinction wrong is the whole difficulty: of the 11 em dashes in the theme on
  2026-08-15, 6 were comments and only 5 rendered (#733).

Chrome copy that lives outside the repo
---------------------------------------

The sitewide ``<title>`` format string (#756) is a Jetpack setting, not a repo
file, so no static scan can see it. Pipe a live readback through the same rules
instead::

    curl -s https://kriskrug.co/ | grep -o '<title>[^<]*</title>' | \
        python3 scripts/voice_check.py -

Waivers
-------

``.voice-waivers.json`` at the repo root records per-file exemptions with an
issue reference and a reason. It is a **ratchet**, not a mute button: a waiver
whose file no longer violates anything is reported as stale and fails the run,
so grandfathered entries get deleted as the backlog is cleaned up rather than
accumulating forever. Same discipline as ``.css-budget.json`` (#472).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
WAIVER_PATH = REPO_ROOT / ".voice-waivers.json"

# Written as an escape and never as a literal, so that this checker, its docs,
# and its own output can be grepped without the character being reintroduced.
EM_DASH = "\u2014"

PAYLOAD_ROOT = Path("content/drafts")
PAYLOAD_NAMES = ("post.md", "post.html", "post-body.html", "copy.md")
THEME_DIRS = (
    Path("theme/kk-aurora/templates"),
    Path("theme/kk-aurora/parts"),
    Path("theme/kk-aurora/patterns"),
)

RULES = (
    (
        "em-dash",
        re.compile(re.escape(EM_DASH)),
        "em dash; rewrite as a colon, period, or comma",
    ),
    ("slop:delve", re.compile(r"\bdelv(?:e|es|ed|ing)\b", re.I), "slop lexicon: delve"),
    (
        "slop:tapestry",
        re.compile(r"\btapestr(?:y|ies)\b", re.I),
        "slop lexicon: tapestry",
    ),
    (
        "slop:testament",
        re.compile(r"\ba testament to\b", re.I),
        "slop lexicon: a testament to",
    ),
    ("slop:nestled", re.compile(r"\bnestled\b", re.I), "slop lexicon: nestled"),
    (
        "slop:in-a-world",
        re.compile(r"(?:\A|\n)[ \t>#*_]*In a world\b"),
        'slop lexicon: "In a world" opener',
    ),
)

# Blanked before matching. `//` is PHP-only and guarded against `https://`.
BLOCK_COMMENTS = (re.compile(r"<!--.*?-->", re.S), re.compile(r"/\*.*?\*/", re.S))
PHP_LINE_COMMENT = re.compile(r"(?<!:)//[^\n]*")


def blank_comments(text: str, suffix: str) -> str:
    """Replace comment bodies with spaces, preserving offsets and line numbers."""

    def blank(match: re.Match) -> str:
        return "".join("\n" if ch == "\n" else " " for ch in match.group(0))

    for pattern in BLOCK_COMMENTS:
        text = pattern.sub(blank, text)
    if suffix == ".php":
        text = PHP_LINE_COMMENT.sub(blank, text)
    return text


def scan_text(text: str, suffix: str) -> list[tuple[str, int, int, str, str]]:
    """Return (rule_id, line, col, message, excerpt) for every violation."""
    scannable = blank_comments(text, suffix)
    found = []
    for rule_id, pattern, message in RULES:
        for match in pattern.finditer(scannable):
            line = scannable.count("\n", 0, match.start()) + 1
            col = match.start() - (scannable.rfind("\n", 0, match.start()) + 1) + 1
            excerpt = text.split("\n")[line - 1].strip()[:100]
            found.append((rule_id, line, col, message, excerpt))
    return sorted(found, key=lambda hit: (hit[1], hit[2]))


def default_targets() -> list[Path]:
    """Every payload and theme file in scope, relative to the repo root."""
    targets = [
        path
        for path in sorted((REPO_ROOT / PAYLOAD_ROOT).rglob("*"))
        if path.name in PAYLOAD_NAMES
    ]
    for theme_dir in THEME_DIRS:
        targets.extend(
            sorted(p for p in (REPO_ROOT / theme_dir).rglob("*") if p.is_file())
        )
    return [path.relative_to(REPO_ROOT) for path in targets]


def load_waivers() -> dict[str, dict]:
    if not WAIVER_PATH.exists():
        return {}
    data = json.loads(WAIVER_PATH.read_text(encoding="utf-8"))
    return {entry["path"]: entry for entry in data.get("waivers", [])}


def is_waived(waiver: dict | None, rule_id: str) -> bool:
    if waiver is None:
        return False
    rules = waiver.get("rules", ["*"])
    return "*" in rules or rule_id in rules


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument(
        "paths",
        nargs="*",
        help="Files to scan; '-' reads stdin. Default: all payload + theme files in scope.",
    )
    args = parser.parse_args(argv)

    waivers = load_waivers()
    violations: list[tuple[str, str, int, int, str, str]] = []
    waived_count = 0
    scanned_waived: set[str] = set()
    hit_waived: set[str] = set()

    if args.paths == ["-"]:
        for rule_id, line, col, message, excerpt in scan_text(sys.stdin.read(), ".txt"):
            violations.append(("<stdin>", rule_id, line, col, message, excerpt))
        targets: list[Path] = []
    else:
        targets = [Path(p) for p in args.paths] if args.paths else default_targets()

    for target in targets:
        absolute = target if target.is_absolute() else REPO_ROOT / target
        if not absolute.is_file():
            continue
        key = str(target)
        waiver = waivers.get(key)
        if waiver is not None:
            scanned_waived.add(key)
        for rule_id, line, col, message, excerpt in scan_text(
            absolute.read_text(encoding="utf-8", errors="replace"), absolute.suffix
        ):
            if is_waived(waiver, rule_id):
                waived_count += 1
                hit_waived.add(key)
                continue
            violations.append((key, rule_id, line, col, message, excerpt))

    stale = sorted(scanned_waived - hit_waived)

    for path, rule_id, line, col, message, excerpt in violations:
        print(f"{path}:{line}:{col}: [{rule_id}] {message}\n    {excerpt}")
    for path in stale:
        print(
            f"{path}: [stale-waiver] no violations left; delete this entry from "
            f"{WAIVER_PATH.name} ({waivers[path].get('issue', 'no issue')})"
        )

    scanned = len(targets) or 1
    print(
        f"\nvoice-check: {scanned} file(s) scanned, {len(violations)} violation(s), "
        f"{waived_count} waived, {len(stale)} stale waiver(s)."
    )
    if violations or stale:
        print(
            "Hard rules only. For the full voice pass when the corpus is available:\n"
            "  python3 ~/Code/kk-voice/scripts/voicecheck.py <file>"
        )
        return 1
    print(
        "Clean. Full local voice pass (optional, needs ~/Code/kk-voice):\n"
        "  python3 ~/Code/kk-voice/scripts/voicecheck.py <file>"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
