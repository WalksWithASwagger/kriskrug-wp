# The Marquee 🪧

A living hero element for kriskrug.co — a direct descendant of the **Kris Krug × Douglas Coupland
marquee boards** (shared copyright), where Doug supplied ideas and Kris remixed the topography onto
the board. Now the idea-feed is **Kris's own output**: the most interesting thing he's said this
week, remixed into lights.

Each board is, at once:

- a **graphic** (the animated marquee in the hero),
- a **micro blog post** (a sharp line + a paragraph of why it matters), and
- an **SEO surface** (its own indexed `/marquee/<slug>/` page with title, description, tags, OG image).

Over a year that's 50+ tiny, individually-rankable pages — a compounding "greatest hits of what Kris
was thinking." Very McLuhan: the *archive* becomes a medium of its own.

---

## The self-improving loop

```
  SCAN ─────────▶ REMIX ─────────▶ PICK ─────────▶ PROMOTE ─────────▶ ARCHIVE
  (your output)   (2–3 boards)     (you choose)    (takes hero)        (old → /marquee/)
```

1. **SCAN** — read what Kris is actually saying right now:
   - `content/drafts/*` field notes (~55 live)
   - published posts (WordPress MCP)
   - the Beehiiv dispatch (Beehiiv MCP)
   - optionally Slack / Notion / talks
   Extract candidate *lines* — the sharpest tension, claim, or turn of phrase. Short enough for a board.

2. **REMIX** — for the top theme, generate **2–3 board candidates** (`candidates[]` in `marquee.json`):
   phrase (1–3 short lines) + dek + source note + tags + draft SEO. Honors the Coupland move: take
   an idea, remix the *topography*, don't just quote it.

3. **PICK** — human-in-the-loop. Kris chooses one. (Pick-flow is the one open decision — see below.)

4. **PROMOTE** — chosen candidate becomes the `live` board (`meta.current`). Hero renders it.

5. **ARCHIVE** — the previous live board moves to `archive/` with full meta and gets a permanent,
   indexed `/marquee/<slug>/` page. Nothing is lost; the wall of past boards grows.

Cadence: **weekly, or whenever there's interesting shit to say.** Not a fixed cron unless wanted.

---

## Pick-flow — **GitHub draft PR** (chosen)

Every Monday (`.github/workflows/marquee-weekly.yml`) the loop scans drafts, rebuilds the
archive, and opens a **draft PR** listing the week's candidates. Kris picks one in the PR,
runs `promote.py`, and merges. Nothing goes live until promoted.

## Run it locally

```bash
cd scripts/marquee
python3 scan.py --limit 8 --write          # mine drafts → proposals.json (proposes, never overwrites)
python3 promote.py --list                  # see live board + curated candidates
python3 promote.py --candidate cand-mcluhan-tools-shape-us --week 2026-W28
python3 build.py                           # render /marquee/ archive (SEO pages + index wall)
```

The pipeline is **scan → curate → promote → build**: `scan.py` only *proposes*
(`proposals.json`); a human moves the good ones into `marquee.json` `candidates`;
`promote.py` applies the pick and archives the old board; `build.py` renders the wall.

## Files

| File | Role |
|---|---|
| `marquee.json` | Data model — `meta`, live + archived `boards[]`, curated `candidates[]`. Source of truth. |
| `proposals.json` | Raw output of the last scan (scores + provenance). Generated; curate from here. |
| `preview.html` | **Open in a browser.** v1 board, 4 skins live-switchable, 3 McLuhan candidates. |
| `dist/` | Built `/marquee/` archive — one SEO page per board + index wall. Generated. |
| `../../scripts/marquee/` | `scan.py` · `promote.py` · `build.py` · `render.py` · `marquee_lib.py` |
| `../../theme/kk-aurora/patterns/marquee-hero.php` | Drop-in WordPress hero pattern (self-contained, LED). |

## Skins
`led` (dot-matrix ticker · **default**) · `splitflap` (Solari departure board) ·
`letterpress` (Clash Display type-remix) · `teletype` (AI terminal). One board, four looks;
switch via `meta.default_skin` / a board's `skin`.

## Status — v1 prototype
- [x] Data model + McLuhan seed board ("The Model Is the Message")
- [x] Standalone visual preview with 4 skins + 3 candidates
- [x] WordPress drop-in pattern (LED)
- [x] Pick-flow chosen (**GitHub draft PR**) + weekly Action wired
- [x] SCAN step — reads `content/drafts/` → ranked proposals (proven on 55 real drafts)
- [x] `/marquee/` archive builder — SEO pages (OG, Twitter, JSON-LD) + index wall
- [x] Promote step — applies the pick, archives the previous board
- [ ] Extend SCAN to published posts + Beehiiv dispatch (MCP)
- [ ] `marquee` WP post type / route so `/marquee/` is served by WordPress (currently static `dist/`)
- [ ] Promote into the live home hero (swap the pattern into `front-page.html`)
