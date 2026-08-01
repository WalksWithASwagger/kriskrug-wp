# Testimonials Showpiece v2 — Swarm Issue Board

**Status:** Filed + ready to kick Wave 1 later (no implementation started)  
**Epic:** [#593](https://github.com/WalksWithASwagger/kriskrug-wp/issues/593)  
**Plan:** Testimonials showpiece v2 (Cursor plan)  
**Live target:** https://kriskrug.co/testimonials/ (WP page **2409**)  
**Kickoff doc:** [`content/drafts/2026-08-01-testimonials-overhaul/START-HERE.md`](../content/drafts/2026-08-01-testimonials-overhaul/START-HERE.md)  
**Out of scope forever:** homepage #415, Jetpack CPT, Review schema, headshots, auto-sync

## Later kickoff (copy-paste)

```bash
git fetch origin main
# Four parallel agents from origin/main — see START-HERE.md
# Open: #594 #595 #596 #597
curl -s https://kriskrug.co/wp-content/themes/kk-aurora/style.css | grep -i '^Version:'
```

## Wave diagram

```
Wave 1 (parallel, zero file overlap):
  TSTM-1 inventory ──┐
  TSTM-2 linkedin  ──┼──► Wave 2: TSTM-5 curate+consent
  TSTM-4 copy      ──┘              │
  TSTM-3 theme CSS (Track B, parallel; class contract fixed in EPIC)
                                    ▼
Wave 3:              TSTM-6 payload HTML  +  TSTM-7 consent outreach
                                    ▼
Wave 4 (human gates): TSTM-8 theme pixel deploy  →  TSTM-9 content body deploy
```

## Exclusive file ownership (no overlap)

| Issue | Owns (write) | Must not touch |
|-------|--------------|----------------|
| TSTM-1 #594 | `content/drafts/2026-08-01-testimonials-overhaul/quote-inventory.md` | curated-set, consent-log, payload, theme |
| TSTM-2 #595 | `…/linkedin-gaps.md` | inventory rows (read-only), payload |
| TSTM-3 #596 | `theme/kk-aurora/style.css` (`.aurora-tstm-*` block + Version bump only) | any Track A content/payload |
| TSTM-4 #597 | `…/copy-v2.md` | quote picks, payload HTML |
| TSTM-5 #598 | `…/curated-set-v2.md`, `…/consent-log.md` | theme, payload HTML, linkedin-gaps writes |
| TSTM-6 #599 | `content/source-packs/…/testimonials.html`, `page-map.json` markers | theme CSS, consent outreach |
| TSTM-7 #600 | `…/consent-outreach.md`, packet `README.md` | payload, theme, live WP |
| TSTM-8 #601 | live theme SFTP + pixel artifacts | page 2409 body |
| TSTM-9 #602 | live page 2409 body via content_architecture_deploy | theme files |

## Fixed class contract (shared read-only between TSTM-3 and TSTM-6)

Do not invent alternate names. Payload uses **dual class** (`aurora-tstm-*` + existing fallbacks).

- `.aurora-tstm` — page root wrapper
- `.aurora-tstm-hero` — hero block
- `.aurora-tstm-stats` / `.aurora-tstm-stat` — stat chips
- `.aurora-tstm-press` — institutional / press band
- `.aurora-tstm-featured` — oversized featured quotes
- `.aurora-tstm-section` — era/section header + intro
- `.aurora-tstm-wall` — CSS-columns quote wall
- `.aurora-tstm-card` — card (also keep `.aurora-quote-card`)
- `.aurora-tstm-cite` — name + optional LinkedIn
- `.aurora-tstm-chip` — context chip (meetup #, RAP, etc.)
- `.aurora-tstm-cta` — bottom CTA

## Version bump rule

Live readback (2026-08-01 afternoon): Aurora **1.5.3**. Repo `main` theme header may still read **1.5.0** — always re-curl live before bumping. Issue **#478** claims **1.6.0** for dead-CSS consolidation. TSTM-3 must bump to the **next unused patch after live** (likely **1.5.4**) — never steal `#478`'s 1.6.0 label.

## Hard blocks (every content/deploy issue)

Never publish: William Jordan, Stephanie McKay, unresolved/tilde names, Butterfield **conference/camera** mis-attribution. Butterfield **2006 photography LinkedIn rec only** is allowed in Archive.

## Locked page sections (order)

1. Hero + stat chips  
2. Press band (Power 50, Portfolio.YVR, CreativeMornings, BC Studies)  
3. Featured (3 oversized)  
4. The Rooms (meetup T1)  
5. Programs (RAP consented)  
6. Talks and teaching  
7. Coaching and training  
8. Community threads (T2 logged)  
9. Film Club / satellites  
10. Archive (photography/connector)  
11. CTA

## Pre-existing on main (v1 — keep)

| Path | Notes |
|------|--------|
| `content/drafts/2026-08-01-testimonials-overhaul/{README,copy,curated-set,linkedin-gaps,quote-inventory}.md` | v1 packet; Wave 1 expands / adds v2 files |
| `content/source-packs/…/wp-payloads/testimonials.html` | live-enriched body; TSTM-6 rebuilds |
| `backup/20260801-testimonials*` | rollback for v1 deploys |

## Filed issue numbers

| Key | Issue | Wave | Ready now? |
|-----|-------|------|------------|
| EPIC | [#593](https://github.com/WalksWithASwagger/kriskrug-wp/issues/593) | — | board |
| TSTM-1 | [#594](https://github.com/WalksWithASwagger/kriskrug-wp/issues/594) | 1 | yes `swarm-ready` |
| TSTM-2 | [#595](https://github.com/WalksWithASwagger/kriskrug-wp/issues/595) | 1 | yes `swarm-ready` |
| TSTM-3 | [#596](https://github.com/WalksWithASwagger/kriskrug-wp/issues/596) | 1 | yes `swarm-ready` (KK review before merge) |
| TSTM-4 | [#597](https://github.com/WalksWithASwagger/kriskrug-wp/issues/597) | 1 | yes `swarm-ready` |
| TSTM-5 | [#598](https://github.com/WalksWithASwagger/kriskrug-wp/issues/598) | 2 | after #594+#595 |
| TSTM-6 | [#599](https://github.com/WalksWithASwagger/kriskrug-wp/issues/599) | 3 | after #597+#598 |
| TSTM-7 | [#600](https://github.com/WalksWithASwagger/kriskrug-wp/issues/600) | 3 | after #598 |
| TSTM-8 | [#601](https://github.com/WalksWithASwagger/kriskrug-wp/issues/601) | 4 | `blocked` until KK |
| TSTM-9 | [#602](https://github.com/WalksWithASwagger/kriskrug-wp/issues/602) | 4 | `blocked` until KK |
