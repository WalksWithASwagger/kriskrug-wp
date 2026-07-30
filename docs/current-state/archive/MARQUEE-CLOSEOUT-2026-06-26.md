# Marquee Closeout — 2026-06-26

## Summary

**The Marquee** is a self-improving hero element for kriskrug.co — a descendant of the
Krug × Coupland marquee boards, except the idea-feed is Kris's own output. It scans his
writing, remixes the sharpest line onto an LED "marquee board," lets him pick from a weekly
batch, and archives every past board as an indexed micro-page. Each board is at once a
**graphic**, a **micro-post**, and an **SEO surface**.

Tiers 1 and 2 are **merged to `main`**. The marquee works end-to-end in the repo and is
on-brand, perf-safe, and share-ready. It is **not yet served on the live domain** — that is
Tier 3 (a WordPress post type). The home hero already leads with the live board via a
generated theme partial, so it ships with the next theme cutover.

- Repo line: `main`
- Shipped PRs: **#257** (v1 prototype), **#259** (Tier 1), **#260** (Tier 2)
- Live board: **"The Model Is the Message"** (after Marshall McLuhan), `2026-W26`
- Default skin: `led`, in Aurora's Signal red (`#F15B43`)
- Production status: not yet serving `/marquee/`; home-hero partial ships with the theme

## What shipped

- **v1 — #257.** Data model (`content/marquee/marquee.json`), scan→curate→promote→build loop,
  4 skins, GitHub draft-PR pick-flow, weekly scan Action, static `/marquee/` archive builder.
- **Tier 1 — #259.** Made it real: the hero now renders **from** `marquee.json` via a generated
  theme partial (`theme/kk-aurora/parts/marquee-current.html`), so `promote` actually changes the
  hero. Re-skinned to Aurora tokens (no invented hex). Perf-safe: pre-rendered cells (works with
  JS off, no CLS) + deferred, front-page-only animation (`assets/js/marquee.js`).
- **Tier 2 — #260.** SEO completeness: a branded **1200×630 OG share card** per board
  (`dist/<slug>/og.png`), full `og:image`/`twitter:image` meta (`@feelmoreplants`), **Article**
  JSON-LD linked to the site Person `@id` (`https://kriskrug.co/#person`), and
  `dist/marquee-sitemap.xml`. Build hardened (prune-and-overwrite) so committed OG PNGs survive
  scan-only CI rebuilds.

## How to operate it

```bash
cd scripts/marquee
python3 scan.py --limit 8 --write          # mine drafts → content/marquee/proposals.json
python3 promote.py --list                  # show live board + curated candidates
python3 promote.py --candidate <id> --week 2026-W28
python3 build.py                           # regenerate hero partial + /marquee/ archive + OG + sitemap
```

The pipeline is **scan → curate → promote → build**. `scan.py` only proposes; a human moves the
good lines into `marquee.json` `candidates`; `promote.py` applies the pick and archives the old
board; `build.py` compiles everything. OG images render locally (needs node + Chromium); in
scan-only CI there is no browser, so the build preserves the committed `og.png`.

## Not live yet / Tier 3 and beyond

- **Serve `/marquee/` from WordPress.** Register a `marquee_board` post type so the archive (and
  `/marquee-sitemap.xml`) is served and editable in wp-admin, with native 301s. Precedent:
  `inc/digital-composting.php`. `promote.py` would create/update WP posts via REST (precedent:
  `scripts/seo-backfill/backfill_lib.py`).
- **Robots line is staged, not active.** `fixes/robots-txt-ai-policy.php` already lists
  `/marquee-sitemap.xml`, commented to deploy **with** Tier 3 serving (it is deployed via Code
  Snippets, so editing the repo file does not change production).
- **Extend SCAN** to published posts + the Beehiiv dispatch (MCP); add a REMIX step that rewrites
  raw extracted fragments into sharper aphorisms.
- **Hero decision.** The marquee currently **leads above** the photo hero (`front-page.html`),
  built so a one-line switch can promote it to full hero takeover once it's proven.

## Notes

- **Lanes.** The marquee is cross-cutting: data/scripts are Track A, the generated theme
  partial + JS are Track B. Tier 1 touched both (one PR, documented); Tier 2 was clean Track A.
- **Recommendation at closeout:** let it ride for a few weekly cycles before Tier 3 — Tiers 1–2
  made it genuinely good, and Tier 3 is the step that puts it on the live domain.

## File map

| Path | Role |
|---|---|
| `content/marquee/marquee.json` | Data model — live + archived boards, curated candidates (source of truth) |
| `content/marquee/README.md` | Full feature docs + status checklist |
| `content/marquee/dist/` | Built `/marquee/` archive — SEO pages, OG PNGs, `marquee-sitemap.xml` |
| `scripts/marquee/` | `scan.py` · `promote.py` · `build.py` · `render.py` · `og.py` · `render_og.cjs` · `marquee_lib.py` |
| `scripts/tests/test_marquee_render.py` · `test_marquee_seo.py` | Tier 1 + Tier 2 guarantees |
| `theme/kk-aurora/parts/marquee-current.html` | Generated live board (deployed with theme) |
| `theme/kk-aurora/assets/js/marquee.js` | Generated deferred flip animation |
| `theme/kk-aurora/patterns/marquee-hero.php` | Thin hero wrapper that includes the partial |
| `.github/workflows/marquee-weekly.yml` | Monday scan → draft PR of candidates |
| `fixes/robots-txt-ai-policy.php` | Staged `/marquee-sitemap.xml` line (activates with Tier 3) |
