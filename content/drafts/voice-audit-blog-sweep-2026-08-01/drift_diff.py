#!/usr/bin/env python3
"""Drift check: live post 12479 (the-cheer-is-a-cap-table) vs its audited draft.

Normalizes both sides to bare content words (markdown syntax off the draft,
Title:/Link: header off the live snapshot, typographic quotes straightened,
whitespace collapsed) and reports word-level differences with context.
Dashes are deliberately NOT normalized so a new em dash shows up as drift.

Read-only; prints to stdout.
"""

from __future__ import annotations

import difflib
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
DRAFT = Path(
    "/Users/kk/Code/kriskrug-wp/content/drafts/2026-07-07-the-cheer-is-a-cap-table/post.md"
)
LIVE = HERE / "snapshots" / "2026-07-10-the-cheer-is-a-cap-table.txt"

QUOTE_MAP = {
    "\u2018": "'",
    "\u2019": "'",
    "\u201c": '"',
    "\u201d": '"',
    "\u2026": "...",
    "\u00a0": " ",
}


def common_normalize(text: str) -> str:
    for src, dst in QUOTE_MAP.items():
        text = text.replace(src, dst)
    # the HTML stripper turns inline tags into spaces, which detaches
    # punctuation right after a link/emphasis close; reattach it
    text = re.sub(r"\s+([.,:;!?])", r"\1", text)
    return text


def draft_words(md: str) -> list[str]:
    # strip YAML frontmatter
    md = re.sub(r"\A---\n.*?\n---\n", "", md, flags=re.S)
    # drop image lines and bare-URL (embed) lines entirely
    lines = []
    for line in md.splitlines():
        s = line.strip()
        if re.fullmatch(r"!\[[^\]]*\]\([^)]*\)", s):
            continue
        if re.fullmatch(r"https?://\S+", s):
            continue
        lines.append(line)
    md = "\n".join(lines)
    md = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", md)  # inline images
    md = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", md)  # links -> text
    md = re.sub(r"^#{1,6}\s*", "", md, flags=re.M)  # heading markers
    md = re.sub(r"^\s*-\s+", "", md, flags=re.M)  # list bullets
    md = md.replace("**", "").replace("`", "")
    md = re.sub(r"(?<!\w)\*|\*(?!\w)", " ", md)  # emphasis asterisks
    return common_normalize(md).split()


def live_words(txt: str) -> list[str]:
    lines = txt.splitlines()
    body = [
        ln for ln in lines if not (ln.startswith("Title: ") or ln.startswith("Link: "))
    ]
    s = "\n".join(body)
    s = re.sub(r"^\s*-\s+", "", s, flags=re.M)  # stripped <li> bullets
    return common_normalize(s).split()


def main() -> None:
    draft_raw = DRAFT.read_text(encoding="utf-8")
    live_raw_full = LIVE.read_text(encoding="utf-8")
    m_draft = re.search(r"^title:\s*(.+)$", draft_raw, flags=re.M)
    m_live = re.search(r"^Title:\s*(.+)$", live_raw_full, flags=re.M)
    print(f"draft title: {m_draft.group(1).strip() if m_draft else '?'}")
    print(f"live  title: {m_live.group(1).strip() if m_live else '?'}")

    a = draft_words(draft_raw)
    b = live_words(live_raw_full)
    print(f"draft words: {len(a)}   live words: {len(b)}")

    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    ratio = sm.ratio()
    print(f"similarity ratio: {ratio:.4f}\n")

    n = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        n += 1
        ctx_a = " ".join(a[max(0, i1 - 10) : i1])
        ctx_b = " ".join(a[i2 : i2 + 10])
        print(f"--- hunk {n} [{tag}] draft[{i1}:{i2}] live[{j1}:{j2}]")
        print(f"  context before: ...{ctx_a}")
        print(f"  DRAFT: {' '.join(a[i1:i2]) or '(nothing)'}")
        print(f"  LIVE : {' '.join(b[j1:j2]) or '(nothing)'}")
        print(f"  context after : {ctx_b}...")
        print()
    if n == 0:
        print("NO CONTENT DIFFERENCES — live matches the audited draft word-for-word.")

    live_raw = LIVE.read_text(encoding="utf-8")
    print(f"em dashes in live text: {live_raw.count(chr(0x2014))}")
    print(
        f"em dashes in draft    : {DRAFT.read_text(encoding='utf-8').count(chr(0x2014))}"
    )


if __name__ == "__main__":
    main()
