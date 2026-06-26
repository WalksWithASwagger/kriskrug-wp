#!/usr/bin/env python3
"""PROMOTE — apply Kris's pick: a candidate becomes the live board.

The previously-live board is flipped to `archived` (it stays in boards[] forever, so
the archive only grows). The chosen candidate is removed from candidates[] and promoted
to a full board record with week/date and SEO scaffold.

Usage:
  python3 scripts/marquee/promote.py --candidate <candidate-id> --week 2026-W28
  python3 scripts/marquee/promote.py --list        # show current live + candidates
"""
from __future__ import annotations
import argparse
import datetime as dt

from marquee_lib import load, save, slugify


def find_live(data):
    for b in data["boards"]:
        if b.get("status") == "live":
            return b
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidate")
    ap.add_argument("--week")
    ap.add_argument("--date")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    data = load()

    if args.list or not args.candidate:
        live = find_live(data)
        print("LIVE:", " / ".join(live["board"]) if live else "(none)")
        print("\nCANDIDATES:")
        for c in data.get("candidates", []):
            print(f"  {c['id']}\n     {' / '.join(c['board'])}")
        if not args.candidate:
            return

    cand = next((c for c in data.get("candidates", []) if c["id"] == args.candidate), None)
    if not cand:
        raise SystemExit(f"No candidate '{args.candidate}'. Run --list to see options.")

    date = args.date or dt.date.today().isoformat()
    iso = dt.date.fromisoformat(date).isocalendar()
    week = args.week or f"{iso[0]}-W{iso[1]:02d}"

    # demote current live
    live = find_live(data)
    if live:
        live["status"] = "archived"

    phrase = " ".join(cand["board"])
    slug = slugify(phrase)
    board = {
        "id": f"{week.lower()}-{slug}",
        "status": "live",
        "week": week,
        "date": date,
        "after": cand.get("after"),
        "skin": data["meta"].get("default_skin", "led"),
        "board": cand["board"],
        "kicker": f"now showing · {week.lower()}",
        "dek": cand.get("dek", ""),
        "source": cand.get("source", {}),
        "tags": cand.get("tags", []),
        "seo": {
            "title": f"{phrase.title()} — a Kris Krüg marquee board",
            "description": (cand.get("dek", "")[:155]).strip(),
            "slug": slug,
            "og_image": "auto",
        },
    }
    data["boards"].insert(0, board)
    data["meta"]["current"] = board["id"]
    data["candidates"] = [c for c in data["candidates"] if c["id"] != args.candidate]
    save(data)
    print(f"\nPromoted → {phrase}\n  live id: {board['id']}\n  previous live archived.")
    print("Next: python3 scripts/marquee/build.py")


if __name__ == "__main__":
    main()
