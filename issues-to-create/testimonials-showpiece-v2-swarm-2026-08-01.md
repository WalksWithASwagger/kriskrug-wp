# Testimonials Showpiece v2 — Swarm Issue Board

**Status:** Filed on WalksWithASwagger/kriskrug-wp  
**Plan:** Testimonials showpiece v2 (Cursor plan)  
**Live target:** https://kriskrug.co/testimonials/ (WP page **2409**)  
**Out of scope forever for this swarm:** homepage #415, Jetpack CPT, Review schema, headshots, auto-sync

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
| TSTM-1 | `content/drafts/2026-08-01-testimonials-overhaul/quote-inventory.md` | curated-set, consent-log, payload, theme |
| TSTM-2 | `…/linkedin-gaps.md` | inventory rows (read-only), payload |
| TSTM-3 | `theme/kk-aurora/style.css` (`.aurora-tstm-*` block + Version bump only) | any Track A content/payload |
| TSTM-4 | `…/copy-v2.md` | quote picks, payload HTML |
| TSTM-5 | `…/curated-set-v2.md`, `…/consent-log.md` | theme, payload HTML, linkedin-gaps writes |
| TSTM-6 | `content/source-packs/…/testimonials.html`, `page-map.json` markers | theme CSS, consent outreach |
| TSTM-7 | `…/consent-outreach.md`, packet `README.md` | payload, theme, live WP |
| TSTM-8 | live theme SFTP + pixel artifacts under agreed backup path | page 2409 body |
| TSTM-9 | live page 2409 body via content_architecture_deploy | theme files |

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

Live readback (2026-08-01): Aurora **1.5.2**. Issue **#478** already claims **1.6.0** for dead-CSS consolidation. TSTM-3 must bump to the **next unused patch after live** (likely **1.5.3**) unless KK redirects — never steal `#478`'s 1.6.0 label.

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

## Issue titles to file

1. `[EPIC] Testimonials showpiece v2 — /testimonials/ (WP 2409)`
2. `[CONTENT] TSTM-1: Consolidate quote inventory v2`
3. `[CONTENT] TSTM-2: Resolve LinkedIn URLs for showpiece cites`
4. `[THEME] TSTM-3: Add aurora-tstm showpiece CSS (+ version bump)`
5. `[CONTENT] TSTM-4: Write testimonials showpiece copy v2`
6. `[CONTENT] TSTM-5: Curate set + consent log`
7. `[CONTENT] TSTM-6: Rebuild testimonials.html payload (no live deploy)`
8. `[CONTENT] TSTM-7: Consent outreach shortlist + packet README`
9. `[DEPLOY] TSTM-8: Pixel-gate theme deploy for aurora-tstm`
10. `[DEPLOY] TSTM-9: Snapshot-gate deploy testimonials page body`


## Filed issue numbers

| Key | Issue |
|-----|-------|
| EPIC | #593 |
| TSTM-1 | #594 |
| TSTM-2 | #595 |
| TSTM-3 | #596 |
| TSTM-4 | #597 |
| TSTM-5 | #598 |
| TSTM-6 | #599 |
| TSTM-7 | #600 |
| TSTM-8 | #601 |
| TSTM-9 | #602 |
