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

## Pick-flow (the one open decision)

How the 2–3 options reach Kris each round. Candidates, pick whichever feels right — all are buildable:

| Option | How it feels | Cost |
|---|---|---|
| **GitHub draft PR** | Loop opens a PR with rendered candidates + source notes; approve & merge. Fits this repo. | low |
| **WordPress drafts** | Candidates land as draft `marquee` posts; pick/publish from WP admin. No git in the weekly loop. | med |
| **Email / Beehiiv digest** | A short digest of the options hits the inbox; reply/click to choose. Lowest friction. | med |

Default until told otherwise: **GitHub draft PR** (matches how everything else here ships).

---

## Files

| File | Role |
|---|---|
| `marquee.json` | Data model — `meta`, live `boards[]`, pending `candidates[]`. Single source of truth. |
| `preview.html` | **Open in a browser.** v1 board, 4 skins live-switchable, 3 McLuhan candidates. |
| `archive/` | Past boards (one record each) → become `/marquee/<slug>/` pages. |
| `../../theme/kk-aurora/patterns/marquee-hero.php` | Drop-in WordPress block pattern (self-contained). |

## Skins
`splitflap` (Solari departure board · default) · `led` (dot-matrix ticker) ·
`letterpress` (Clash Display type-remix) · `teletype` (AI terminal). One board, four looks; switch in `marquee.json`.

## Status — v1 prototype
- [x] Data model + McLuhan seed board ("The Model Is the Message")
- [x] Standalone visual preview with 4 skins + 3 candidates
- [x] WordPress drop-in pattern (split-flap)
- [ ] Pick-flow chosen + wired
- [ ] SCAN step (reads drafts/posts/Beehiiv → candidates)
- [ ] `marquee` post type + `/marquee/` archive route + SEO/OG
- [ ] Promote into the live hero on the home page
