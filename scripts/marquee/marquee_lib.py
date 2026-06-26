"""Shared helpers for the Marquee loop: data IO, slugs, board text wrapping."""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MARQUEE_JSON = ROOT / "content" / "marquee" / "marquee.json"
DRAFTS_DIR = ROOT / "content" / "drafts"
DIST_DIR = ROOT / "content" / "marquee" / "dist"

# Board geometry: the LED board reads best at ~16 chars/line, up to 3 lines.
MAX_LINE_CHARS = 16
MAX_LINES = 3
MAX_BOARD_CHARS = MAX_LINE_CHARS * MAX_LINES


def load() -> dict:
    return json.loads(MARQUEE_JSON.read_text(encoding="utf-8"))


def save(data: dict) -> None:
    MARQUEE_JSON.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[\s_]+", "-", text).strip("-")[:60]


def wrap_board(line: str):
    """Greedy-wrap a phrase into <=MAX_LINES uppercase rows of <=MAX_LINE_CHARS.

    Returns a list of rows, or None if it can't fit cleanly (too long for the board).
    """
    words = line.upper().split()
    rows, cur = [], ""
    for w in words:
        if len(w) > MAX_LINE_CHARS:
            return None  # single word won't fit a row
        if cur and len(cur) + 1 + len(w) > MAX_LINE_CHARS:
            rows.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        rows.append(cur)
    if not rows or len(rows) > MAX_LINES:
        return None
    return rows
