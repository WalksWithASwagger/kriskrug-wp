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

from marquee_lib import load, DIST_DIR, ROOT
from render import (BOARD_RULES, TOKENS_DIST, TOKENS_WP, board_section,
                    inline_js, theme_js)
from og import og_available, render_og

SITE = "https://kriskrug.co"
BASE = "/marquee"

# Theme targets — build.py compiles the live board into deployable theme assets so the home
# hero renders FROM marquee.json (closes the promote → hero loop).
THEME = ROOT / "theme" / "kk-aurora"
PARTIAL = THEME / "parts" / "marquee-current.html"
THEME_JS = THEME / "assets" / "js" / "marquee.js"

PAGE_CSS = """
*{box-sizing:border-box}
html,body{margin:0;background:var(--kkm-deep);color:var(--kkm-text);
  font-family:"Clash Display",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  background:radial-gradient(1200px 600px at 50% -10%,rgba(241,91,67,.06),transparent 60%),var(--kkm-deep)}
.wrap{max-width:1000px;margin:0 auto;padding:28px 18px 72px}
a{color:var(--kkm-cyan);text-decoration:none}
.top{display:flex;justify-content:space-between;align-items:center;font-family:"JetBrains Mono",monospace;
  font-size:12px;color:var(--kkm-text-muted);text-transform:uppercase;letter-spacing:.16em;margin-bottom:8px}
.dek{font-size:clamp(16px,2.2vw,20px);line-height:1.55;color:var(--kkm-text);max-width:64ch;margin:26px auto 0}
.dek b{color:#fff}
.src{font-family:"JetBrains Mono",monospace;font-size:12px;color:var(--kkm-text-muted);margin-top:18px;line-height:1.7;
  border-left:2px solid var(--kkm-line);padding-left:14px;max-width:64ch}
.src .k{color:var(--kkm-cyan)}
.tags{display:flex;flex-wrap:wrap;gap:6px;margin-top:14px}
.tag{font-family:"JetBrains Mono",monospace;font-size:10px;color:var(--kkm-text-muted);border:1px solid var(--kkm-line);
  border-radius:999px;padding:3px 9px}
.nav{display:flex;justify-content:space-between;margin-top:40px;font-family:"JetBrains Mono",monospace;font-size:12px}
h1.idx{font-size:clamp(26px,5vw,46px);margin:6px 0 4px;letter-spacing:-.02em}
.lede{color:var(--kkm-text-muted);max-width:60ch;margin:0 0 28px;line-height:1.6}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px}
.card{background:var(--kkm-surface);border:1px solid var(--kkm-line);border-radius:14px;padding:18px;display:block;transition:.15s}
.card:hover{border-color:var(--kkm-signal)}
.card .ph{font-family:"JetBrains Mono",monospace;font-weight:700;color:var(--kkm-signal);font-size:15px;line-height:1.3}
.card .wk{font-family:"JetBrains Mono",monospace;font-size:10px;color:var(--kkm-text-muted);margin-top:10px;
  text-transform:uppercase;letter-spacing:.1em}
.live{color:var(--kkm-wildcard)}
"""


def page_head(title, desc, url, og_title, og_image=None, og_alt=None):
    e = html.escape
    img = ""
    if og_image:
        a = e(og_alt or og_title)
        u = e(og_image)
        # Mirror the theme's OG/Twitter image convention (1200x630, @feelmoreplants, secure_url).
        img = (
            f'<meta property="og:image" content="{u}">'
            f'<meta property="og:image:secure_url" content="{u}">'
            f'<meta property="og:image:width" content="1200">'
            f'<meta property="og:image:height" content="630">'
            f'<meta property="og:image:alt" content="{a}">'
            f'<meta name="twitter:site" content="@feelmoreplants">'
            f'<meta name="twitter:image" content="{u}">'
            f'<meta name="twitter:image:alt" content="{a}">'
        )
    return f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{e(url)}">
<meta property="og:type" content="article"><meta property="og:title" content="{e(og_title)}">
<meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{e(url)}">
<meta name="twitter:card" content="summary_large_image">{img}
<style>{TOKENS_DIST}{PAGE_CSS}{BOARD_RULES}</style></head><body><div class="wrap">"""


def board_page(b, prev_b, next_b):
    e = html.escape
    seo = b.get("seo", {})
    slug = seo.get("slug") or b["id"]
    url = f"{SITE}{BASE}/{slug}/"
    title = seo.get("title") or " ".join(b["board"])
    desc = seo.get("description") or b.get("dek", "")
    src = b.get("source", {})
    src_line = " · ".join(x for x in [src.get("title"), src.get("author")] if x)
    og_image = f"{url}og.png"
    og_alt = f'Marquee board: {" ".join(b["board"])}'
    # Article schema aligned to the site's Person entity (fixes/schema-snippets-deployed.php).
    jsonld = {
        "@context": "https://schema.org", "@type": "Article",
        "headline": title, "description": desc, "abstract": b.get("dek", ""), "url": url,
        "datePublished": b.get("date"),
        "author": {"@id": f"{SITE}/#person"}, "publisher": {"@id": f"{SITE}/#person"},
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "image": {"@type": "ImageObject", "url": og_image, "width": 1200, "height": 630, "caption": og_alt},
        "keywords": ", ".join(b.get("tags", [])),
        "articleSection": "Marquee",
        "isBasedOn": src.get("author") or src.get("title"),
    }
    out = page_head(title, desc, url, title, og_image=og_image, og_alt=og_alt)
    out += f'<div class="top"><span>marquee · {e(b.get("week",""))}</span><a href="{BASE}/">← all boards</a></div>\n'
    out += board_section(b["board"], b.get("kicker", "marquee"), b.get("skin", "led")) + "\n"
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
    out += f"<script>{inline_js()}</script></div></body></html>"
    return slug, out


def index_page(boards):
    e = html.escape
    url = f"{SITE}{BASE}/"
    live = next((b for b in boards if b.get("status") == "live"), boards[0] if boards else None)
    og = f'{url}{(live.get("seo", {}).get("slug") or live["id"])}/og.png' if live else None
    out = page_head("The Marquee — archive of remixed boards | Kris Krüg",
                    "A growing wall of marquee boards: the sharpest line from what Kris Krüg is making and saying, remixed into lights. One graphic, one micro-post, one indexed page at a time.",
                    url, "The Marquee — Kris Krüg", og_image=og, og_alt="The Marquee — Kris Krüg")
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


def live_board(data):
    for b in data.get("boards", []):
        if b.get("status") == "live":
            return b
    return data.get("boards", [None])[0]


def write_theme_partial(data):
    """Compile the live board into a deployable theme partial + the deferred animation asset.

    parts/marquee-current.html holds the pre-rendered board (token colors via theme presets,
    no script). assets/js/marquee.js is the single-source flip animation, enqueued deferred.
    This is what closes the promote → home-hero loop.
    """
    b = live_board(data)
    if not b:
        return
    section = board_section(b["board"], b.get("kicker", "marquee"), b.get("skin", "led"))
    partial = (
        "<!-- GENERATED by scripts/marquee/build.py from content/marquee/marquee.json -->\n"
        "<!-- Live marquee board. Regenerated by promote.py → build.py; do not edit by hand. -->\n"
        f"<style>{TOKENS_WP}{BOARD_RULES}</style>\n"
        f"{section}\n"
    )
    PARTIAL.parent.mkdir(parents=True, exist_ok=True)
    PARTIAL.write_text(partial, encoding="utf-8")
    THEME_JS.parent.mkdir(parents=True, exist_ok=True)
    THEME_JS.write_text(theme_js(), encoding="utf-8")
    print(f"  theme  → parts/marquee-current.html  ({' / '.join(b['board'])})")
    print(f"  theme  → assets/js/marquee.js")


def slug_of(b):
    return b.get("seo", {}).get("slug") or b["id"]


def sitemap_xml(boards):
    """A urlset for the /marquee/ index + each board page, with the board's og image."""
    NS = ('xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
          'xmlns:image="http://www.sitemaps.org/schemas/sitemap-image/1.1"')
    rows = [f'  <url><loc>{SITE}{BASE}/</loc></url>']
    for b in boards:
        slug = slug_of(b)
        loc = f"{SITE}{BASE}/{slug}/"
        lastmod = f"<lastmod>{b['date']}</lastmod>" if b.get("date") else ""
        rows.append(
            f'  <url><loc>{loc}</loc>{lastmod}'
            f'<image:image><image:loc>{loc}og.png</image:loc></image:image></url>'
        )
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<urlset {NS}>\n' + "\n".join(rows) + "\n</urlset>\n")


def main():
    data = load()
    boards = data.get("boards", [])
    write_theme_partial(data)
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    # Prune-and-overwrite (NOT rmtree): removes only dirs for boards that no longer exist, so
    # committed og.png files survive scan-only CI rebuilds (which can't re-render them).
    valid = {slug_of(b) for b in boards}
    for child in DIST_DIR.iterdir():
        if child.is_dir() and child.name not in valid:
            shutil.rmtree(child)

    og_on = og_available()
    if not og_on:
        print("  og     → skipped (no browser; existing og.png preserved)")
    for i, b in enumerate(boards):
        prev_b = slug_of(boards[i - 1]) if i > 0 else None
        next_b = slug_of(boards[i + 1]) if i < len(boards) - 1 else None
        slug, page = board_page(b, prev_b, next_b)
        d = DIST_DIR / slug
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(page, encoding="utf-8")
        if og_on:
            ok = render_og(b, d)
            print(f"  board → {BASE}/{slug}/  (og.png {'✓' if ok else '—'})")
        else:
            print(f"  board → {BASE}/{slug}/")

    (DIST_DIR / "index.html").write_text(index_page(boards), encoding="utf-8")
    (DIST_DIR / "marquee-sitemap.xml").write_text(sitemap_xml(boards), encoding="utf-8")
    print(f"  index → {BASE}/  ({len(boards)} board{'s' if len(boards)!=1 else ''})")
    print(f"  sitemap → {BASE}/marquee-sitemap.xml")
    print(f"\nBuilt archive into {DIST_DIR.relative_to(DIST_DIR.parents[2])}")


if __name__ == "__main__":
    main()
