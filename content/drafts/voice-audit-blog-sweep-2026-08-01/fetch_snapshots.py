#!/usr/bin/env python3
"""Read-only snapshot fetch for the 2026-08-01 blog voice sweep.

Fetches rendered content for the 15 in-scope posts from the public WP REST
API and writes, per post, into snapshots/ beside this script:

  <date>-<slug>.html  raw content.rendered exactly as fetched
  <date>-<slug>.txt   stripped plain text (Title:/Link: header, paragraph
                      breaks preserved as blank lines)

Also writes manifest.json (id, slug, date, link, title, body word count).
Never writes anywhere else; never authenticates; safe to re-run.
"""

from __future__ import annotations

import html
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

# (id, expected date, expected slug) — from the sweep plan
POSTS = [
    (12653, "2026-07-31", "ai-lands-inside-every-profession"),
    (12638, "2026-07-28", "no-one-knows-what-to-call-us-yet"),
    (12612, "2026-07-18", "i-am-nomad-ai-film"),
    (12479, "2026-07-10", "the-cheer-is-a-cap-table"),
    (12473, "2026-07-06", "artists-learn-machines-extract"),
    (11879, "2026-07-02", "ai-media-appearances-podcast-guesting"),
    (
        12034,
        "2026-06-30",
        "zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey",
    ),
    (12032, "2026-06-28", "what-would-chat-do-and-why-thats-the-wrong-question"),
    (
        12030,
        "2026-06-26",
        "canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one",
    ),
    (12035, "2026-06-24", "ai-wont-fix-your-broken-permit-process"),
    (12363, "2026-06-23", "vancouver-made-world-cup"),
    (12357, "2026-06-23", "ethos-lab-block-party"),
    (12190, "2026-06-22", "the-great-canadian-proximity-game"),
    (12263, "2026-06-20", "god-skills-agentic-loop-workflows"),
    (12257, "2026-06-18", "why-we-built-the-responsible-ai-professional-certification"),
]

API = "https://kriskrug.co/wp-json/wp/v2/posts/{pid}?_fields=id,slug,date,link,title,content"
HERE = Path(__file__).resolve().parent
SNAP = HERE / "snapshots"

SCRIPT_STYLE_RE = re.compile(r"<(script|style)\b.*?</\1\s*>", re.I | re.S)
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
BLOCK_CLOSE_RE = re.compile(
    r"</(p|h[1-6]|ul|ol|blockquote|figure|figcaption|pre|div|section|article|table|tr)\s*>",
    re.I,
)
LEFTOVER_ENTITY_RE = re.compile(r"&(#\d+|#x[0-9a-fA-F]+|[a-zA-Z]{2,10});")


def fetch_json(pid: int) -> dict:
    req = urllib.request.Request(
        API.format(pid=pid),
        headers={
            "User-Agent": "kk-voice-audit/1.0 (read-only snapshot; kriskrug.co ops)"
        },
    )
    last_err = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as err:  # noqa: BLE001 — report and retry, then give up
            last_err = err
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"post {pid}: fetch failed after 3 attempts: {last_err}")


def strip_html(raw: str) -> str:
    s = SCRIPT_STYLE_RE.sub(" ", raw)
    s = HTML_COMMENT_RE.sub(" ", s)
    s = re.sub(r"<br\s*/?\s*>", "\n", s, flags=re.I)
    s = re.sub(r"<li[^>]*>", "\n- ", s, flags=re.I)  # keep list items visible
    s = re.sub(r"</li\s*>", "\n", s, flags=re.I)
    s = BLOCK_CLOSE_RE.sub("\n\n", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = s.replace("\u00a0", " ").replace("\u200b", "")
    s = re.sub(r"[ \t]+", " ", s)
    s = "\n".join(line.strip() for line in s.splitlines())
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def main() -> int:
    SNAP.mkdir(exist_ok=True)
    manifest = []
    problems = []

    for pid, exp_date, exp_slug in POSTS:
        data = fetch_json(pid)
        slug = data.get("slug", "")
        date = (data.get("date") or "")[:10]
        link = data.get("link", "")
        title = (
            strip_html(data.get("title", {}).get("rendered", ""))
            .replace("\n", " ")
            .strip()
        )
        raw = data.get("content", {}).get("rendered", "")

        if slug != exp_slug:
            problems.append(
                f"post {pid}: slug mismatch — expected {exp_slug!r}, REST says {slug!r}"
            )
        if date != exp_date:
            problems.append(
                f"post {pid}: date mismatch — expected {exp_date}, REST says {date}"
            )

        stem = f"{date}-{slug}"  # REST values are ground truth
        (SNAP / f"{stem}.html").write_text(raw, encoding="utf-8")

        body = strip_html(raw)
        txt = f"Title: {title}\nLink: {link}\n\n{body}\n"
        (SNAP / f"{stem}.txt").write_text(txt, encoding="utf-8")

        leftovers = sorted(set(LEFTOVER_ENTITY_RE.findall(body)))
        if leftovers:
            problems.append(
                f"post {pid}: possible leftover entities in txt: {leftovers}"
            )

        words = len(body.split())
        manifest.append(
            {
                "id": pid,
                "slug": slug,
                "date": data.get("date"),
                "link": link,
                "title": title,
                "body_words": words,
                "html_file": f"snapshots/{stem}.html",
                "txt_file": f"snapshots/{stem}.txt",
            }
        )
        print(f"ok  {pid}  {stem}  ({words} words)")

    (HERE / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    if problems:
        print("\nPROBLEMS:")
        for p in problems:
            print(f"  - {p}")
        return 1
    print(f"\nall {len(POSTS)} posts fetched clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
