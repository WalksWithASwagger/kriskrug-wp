#!/usr/bin/env python3
"""BUILD — render the /marquee/ archive: one SEO page per board + an index wall.

Each board becomes a graphic + micro-post + indexed page (title, meta description,
canonical, OpenGraph, Twitter card, JSON-LD CreativeWork). Output is static HTML in
content/marquee/dist/, ready to ship to WordPress or serve directly.

Usage:  python3 scripts/marquee/build.py
"""
from __future__ import annotations
import html
import shutil

from marquee_lib import load, DIST_DIR
from render import BOARD_CSS, BOARD_JS, board_html

SITE = "https://kriskrug.co"
BASE = "/marquee"

PAGE_CSS = """
*{box-sizing:border-box}
html,body{margin:0;background:#0a0a0f;color:#f6f5f2;
  font-family:"Clash Display",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  background:radial-gradient(1200px 600px at 50% -10%,rgba(255,59,59,.06),transparent 60%),#0a0a0f}
.wrap{max-width:1000px;margin:0 auto;padding:28px 18px 72px}
a{color:#00e0c6;text-decoration:none}
.top{display:flex;justify-content:space-between;align-items:center;font-family:"JetBrains Mono",monospace;
  font-size:12px;color:#8a8aa0;text-transform:uppercase;letter-spacing:.16em;margin-bottom:8px}
.dek{font-size:clamp(16px,2.2vw,20px);line-height:1.55;color:#d9d9e3;max-width:64ch;margin:26px auto 0}
.dek b{color:#fff}
.src{font-family:"JetBrains Mono",monospace;font-size:12px;color:#8a8aa0;margin-top:18px;line-height:1.7;
  border-left:2px solid #1d1d2b;padding-left:14px;max-width:64ch}
.src .k{color:#00e0c6}
.tags{display:flex;flex-wrap:wrap;gap:6px;margin-top:14px}
.tag{font-family:"JetBrains Mono",monospace;font-size:10px;color:#8a8aa0;border:1px solid #1d1d2b;
  border-radius:999px;padding:3px 9px}
.nav{display:flex;justify-content:space-between;margin-top:40px;font-family:"JetBrains Mono",monospace;font-size:12px}
h1.idx{font-size:clamp(26px,5vw,46px);margin:6px 0 4px;letter-spacing:-.02em}
.lede{color:#8a8aa0;max-width:60ch;margin:0 0 28px;line-height:1.6}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px}
.card{background:#101019;border:1px solid #1d1d2b;border-radius:14px;padding:18px;display:block;transition:.15s}
.card:hover{border-color:#ff3b3b}
.card .ph{font-family:"JetBrains Mono",monospace;font-weight:700;color:#ff5a5a;font-size:15px;line-height:1.3}
.card .wk{font-family:"JetBrains Mono",monospace;font-size:10px;color:#8a8aa0;margin-top:10px;
  text-transform:uppercase;letter-spacing:.1em}
.live{color:#ffb000}
"""


def page_head(title, desc, url, og_title):
    e = html.escape
    return f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{e(url)}">
<meta property="og:type" content="article"><meta property="og:title" content="{e(og_title)}">
<meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{e(url)}">
<meta name="twitter:card" content="summary_large_image">
<style>{PAGE_CSS}{BOARD_CSS}</style></head><body><div class="wrap">"""


def board_page(b, prev_b, next_b):
    e = html.escape
    seo = b.get("seo", {})
    slug = seo.get("slug") or b["id"]
    url = f"{SITE}{BASE}/{slug}/"
    title = seo.get("title") or " ".join(b["board"])
    desc = seo.get("description") or b.get("dek", "")
    src = b.get("source", {})
    src_line = " · ".join(x for x in [src.get("title"), src.get("author")] if x)
    jsonld = {
        "@context": "https://schema.org", "@type": "CreativeWork",
        "headline": " ".join(b["board"]), "abstract": desc, "url": url,
        "datePublished": b.get("date"), "creator": {"@type": "Person", "name": "Kris Krüg"},
        "keywords": ", ".join(b.get("tags", [])),
        "isBasedOn": src.get("author") or src.get("title"),
    }
    out = page_head(title, desc, url, title)
    out += f'<div class="top"><span>marquee · {e(b.get("week",""))}</span><a href="{BASE}/">← all boards</a></div>\n'
    out += board_html(b["board"], b.get("kicker", "marquee"), b.get("skin", "led")) + "\n"
    out += f'<p class="dek">{b.get("dek","")}</p>\n'
    if src_line or src.get("remixed_from"):
        out += '<p class="src">'
        if b.get("after"):
            out += f'<span class="k">after</span> {e(b["after"])}<br>'
        if src_line:
            out += f'<span class="k">source</span> {e(src_line)}<br>'
        if src.get("remixed_from"):
            out += f'<span class="k">remix</span> {e(src["remixed_from"])}'
        out += "</p>\n"
    if b.get("tags"):
        out += '<div class="tags">' + "".join(f'<span class="tag">#{e(t)}</span>' for t in b["tags"]) + "</div>\n"
    out += '<div class="nav">'
    out += (f'<a href="{BASE}/{prev_b}/">← previous board</a>' if prev_b else "<span></span>")
    out += (f'<a href="{BASE}/{next_b}/">next board →</a>' if next_b else "<span></span>")
    out += "</div>\n"
    out += f'<script type="application/ld+json">{html.escape(__import__("json").dumps(jsonld))}</script>'
    out += f"<script>{BOARD_JS}</script></div></body></html>"
    return slug, out


def index_page(boards):
    e = html.escape
    url = f"{SITE}{BASE}/"
    out = page_head("The Marquee — archive of remixed boards | Kris Krüg",
                    "A growing wall of marquee boards: the sharpest line from what Kris Krüg is making and saying, remixed into lights. One graphic, one micro-post, one indexed page at a time.",
                    url, "The Marquee — Kris Krüg")
    out += '<div class="top"><span>kriskrug.co</span><a href="/">← home</a></div>\n'
    out += '<h1 class="idx">The Marquee</h1>\n'
    out += '<p class="lede">A descendant of the Krug × Coupland marquee boards. Each week the sharpest line from what I\'m making gets remixed into lights — then archived here as its own little indexed page.</p>\n'
    out += '<div class="grid">'
    for b in boards:
        slug = b.get("seo", {}).get("slug") or b["id"]
        live = b.get("status") == "live"
        out += (f'<a class="card" href="{BASE}/{slug}/"><div class="ph">{e(" ".join(b["board"]))}</div>'
                f'<div class="wk {"live" if live else ""}">{e(b.get("week",""))} · {"● live" if live else "archived"}</div></a>')
    out += "</div></div></body></html>"
    return out


def main():
    data = load()
    boards = data.get("boards", [])
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True)
    order = boards  # live first as authored
    for i, b in enumerate(order):
        prev_b = (order[i - 1].get("seo", {}).get("slug") or order[i - 1]["id"]) if i > 0 else None
        next_b = (order[i + 1].get("seo", {}).get("slug") or order[i + 1]["id"]) if i < len(order) - 1 else None
        slug, page = board_page(b, prev_b, next_b)
        d = DIST_DIR / slug
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(page, encoding="utf-8")
        print(f"  board → {BASE}/{slug}/")
    (DIST_DIR / "index.html").write_text(index_page(order), encoding="utf-8")
    print(f"  index → {BASE}/  ({len(order)} board{'s' if len(order)!=1 else ''})")
    print(f"\nBuilt archive into {DIST_DIR.relative_to(DIST_DIR.parents[2])}")


if __name__ == "__main__":
    main()
