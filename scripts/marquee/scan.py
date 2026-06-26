#!/usr/bin/env python3
"""SCAN — mine Kris's drafts for board-worthy lines and propose marquee candidates.

Reads content/drafts/*/post.md (YAML frontmatter + markdown body), extracts the
sharpest short lines, scores them for "board-ability," and writes the top proposals
into marquee.json -> candidates[] (and a richer proposals.json with provenance).

The REMIX/PICK step (human-in-the-loop via GitHub PR) refines a candidate into the
final board. This scanner is deliberately conservative: it surfaces real lines Kris
actually wrote, it does not invent copy.

Usage:  python3 scripts/marquee/scan.py [--limit N] [--write]
Without --write it prints the ranked proposals (dry run).
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

import yaml

from marquee_lib import DRAFTS_DIR, slugify, wrap_board, MAX_BOARD_CHARS

STRONG = re.compile(
    r"\b(is|are|isn't|aren't|won't|can't|don't|never|always|not|only|the|your|our|we|you)\b",
    re.I,
)
URL = re.compile(r"https?://|www\.|\]\(")
MD_NOISE = re.compile(r"[*_`#>\[\]]")
# Editorial scaffolding that lives in drafts but isn't an idea — never put it on the board.
STOPWORDS = re.compile(
    r"\b(outline|prompt|stub|hook|setup|angle|section|draft|tk|todo|caption|diagram|"
    r"image|images|alt|content|notes?|placeholder|wip|intro|conclusion|takeaway|cta|"
    r"the bc angle|in action|possible)\b",
    re.I,
)


def is_label(s: str) -> bool:
    """A header/label, not a claim: ends with a colon, or is all-caps scaffolding."""
    if s.endswith(":"):
        return True
    letters = [c for c in s if c.isalpha()]
    return bool(letters) and all(c.isupper() for c in letters)  # no lowercase => a LABEL


def parse_post(path: Path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    fm, body = {}, text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            try:
                fm = yaml.safe_load(text[3:end]) or {}
            except Exception:
                fm = {}
            body = text[end + 4:]
    return fm, body


def candidate_lines(body: str):
    """Yield (line, kind) for board-worthy raw lines: pull-quotes, bold leads, short declaratives."""
    for raw in body.splitlines():
        s = raw.strip()
        if not s or URL.search(s):
            continue
        kind = "line"
        m = re.fullmatch(r"[*_](.+?)[*_]", s)              # *pull quote* (highest value)
        if m:
            s, kind = m.group(1), "quote"
        else:
            m = re.match(r"\*\*(.+?)\*\*[:.]?\s*(.*)", s)  # **bold lead** + trailing sentence
            if m:
                # prefer the sentence AFTER the bold label if there is one, else the bold text
                s, kind = (m.group(2) or m.group(1)), "lead"
        s = MD_NOISE.sub("", s).strip(' "“”')
        s = re.split(r"(?<=[.!?])\s", s)[0].strip(" .")    # first sentence only
        if is_label(s) or STOPWORDS.search(s):
            continue                                       # drop headers + scaffolding
        words = s.split()
        has_lower = any(c.islower() for c in s)
        if 12 <= len(s) <= 60 and 3 <= len(words) <= 9 and has_lower and STRONG.search(s):
            yield s, kind


def score(line: str, kind: str, recency: float) -> float:
    sc = 0.0
    sc += {"lead": 3.0, "quote": 2.0, "line": 0.0}[kind]
    sc += 2.5 if len(line) <= MAX_BOARD_CHARS else 0.0      # fits the board outright
    sc += 1.5 if wrap_board(line) else -2.0                  # can it wrap cleanly?
    sc += min(len(STRONG.findall(line)), 3) * 0.4           # declarative punch
    sc -= 0.04 * len(line)                                   # prefer short
    sc += 2.0 * recency                                     # newer drafts weigh more
    return round(sc, 2)


def scan(limit: int):
    posts = sorted(DRAFTS_DIR.glob("*/post.md"))
    proposals = []
    for i, p in enumerate(posts):
        recency = i / max(len(posts) - 1, 1)               # 0..1, later folders newer (date-sorted names)
        fm, body = parse_post(p)
        title = (fm.get("title") or p.parent.name).strip()
        excerpt = (fm.get("excerpt") or "").strip()
        tags = [slugify(t) for t in (fm.get("tags") or [])][:5]
        seen = set()
        for line, kind in candidate_lines(body):
            key = line.lower()
            if key in seen:
                continue
            seen.add(key)
            rows = wrap_board(line)
            if not rows:
                continue
            proposals.append({
                "id": f"cand-{slugify(title)}-{slugify(line)[:24]}",
                "board": rows,
                "line": line,
                "kind": kind,
                "score": score(line, kind, recency),
                "dek": excerpt or f"Remixed from “{title}.”",
                "source": {"title": title, "slug": fm.get("slug") or p.parent.name},
                "tags": tags,
            })
    proposals.sort(key=lambda x: x["score"], reverse=True)
    # de-dupe near-identical boards, keep variety of sources
    out, used_src = [], {}
    for c in proposals:
        s = c["source"]["slug"]
        if used_src.get(s, 0) >= 2:
            continue
        used_src[s] = used_src.get(s, 0) + 1
        out.append(c)
        if len(out) >= limit:
            break
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=8)
    ap.add_argument("--write", action="store_true", help="write the scan to content/marquee/proposals.json")
    args = ap.parse_args()

    props = scan(args.limit)
    print(f"Scanned {len(list(DRAFTS_DIR.glob('*/post.md')))} drafts -> {len(props)} candidates\n")
    for c in props:
        print(f"  [{c['score']:>5}] {c['kind']:<5} {' / '.join(c['board'])}")
        print(f"          from: {c['source']['title']}")

    if args.write:
        # scan() proposes; a human curates which proposals become marquee.json candidates,
        # then promote.py picks the live board. We never auto-overwrite curated candidates.
        out = {"generated_from": "content/drafts", "count": len(props), "candidates": props}
        (DRAFTS_DIR.parent / "marquee" / "proposals.json").write_text(
            json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"\nWrote {len(props)} proposals -> content/marquee/proposals.json")
        print("Curate into marquee.json 'candidates', then: python3 promote.py --candidate <id>")


if __name__ == "__main__":
    main()
