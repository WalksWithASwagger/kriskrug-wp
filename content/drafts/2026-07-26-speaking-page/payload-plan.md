# Payload plan - Speaking multimedia rebuild (#419)

**Mode:** DRAFT ONLY. Do not PATCH live WP from this package without KK approval + authenticated snapshot.  
**Target:** page ID `1887`, slug `speaking`, URL https://kriskrug.co/speaking/  
**Recommended copy + media:** Option A from `copy-options.md` + P0 pair from `multimedia-rebuild-plan.md`  
**Apply-ready body:** `payload-body.html`

## Goals (acceptance criteria)

1. Media inventory (videos + photos with sources) documented for KK curation.  
2. At 1440 and 390, a stage photo or video is visible without scrolling.  
3. At least 2 embedded or linked talk videos on the page.  
4. Booking CTA present above the fold and at page end.

## Content changes (Option A)

| Band | Change |
|---|---|
| Hero | New full-width library stage photo (`kk-laSalle-both-hands-full-25-scaled.jpg`, `loading="eager"`) + short support line + booking CTA |
| Watch | Two lazy YouTube iframes: `T5ANAthZewE` + `1OcC-0X6Nb8` |
| On stages | Three library stills (LaSalle mid, Michelle Diamond 184, Michelle Diamond 195) |
| Formats | Same four cards |
| Signature topics | Same four destinations; Both Hands Full / Punk Rock AI images moved to library-friendly assets where possible (LaSalle / CreativeMornings / Guy Kawasaki graphic / meetup still). Hotlinks removed. |
| End CTA | Unchanged pattern; second booking CTA |

Page-scoped CSS under `.kk-r9-pack` adds hero media aspect, embed 16:9 wrappers, and keeps R9 button/card resets.

## What stays intact

- Pack marker `<!-- content-architecture-2026:speaking -->`
- Wrapper classes compatible with live R9 pack (`kk-page kk-r9-pack`)
- Formats meanings and topic link targets
- `/contact/` as booking path (unless CTA issue overrides before apply)
- Title field (do not send `title` in REST update)

## Out of scope

- Homepage Speaking section (#414)
- Theme file edits / Track B
- Importing YouTube thumbnails into the media library
- Changing sitewide SEO plugins beyond page body
- Autoplay or background video

## Apply procedure (after KK approval)

1. Confirm secrets: `WP_USER` + `WP_APP_PASSWORD` present (length check only).  
2. Authenticated GET page `1887`; write `backup/<timestamp>-speaking-419/page-1887-before.json` + rendered HTML.  
3. Dry-run: print payload bytes; confirm ≥2 youtube embed URLs; confirm hero `<img>` present before Formats; confirm CTA count ≥2.  
4. KK signs media curation + copy option + screenshots plan.  
5. Body-only REST update (`content` raw = `payload-body.html`). Do not send `title`.  
6. Purge Pagely page cache for `/speaking/`.  
7. Logged-out verification (checklist below).  
8. If bad: restore snapshot `content.raw`.

## Verification checklist (issue acceptance + evals)

### Acceptance

- [ ] Media inventory reviewed (`multimedia-rebuild-plan.md`).  
- [ ] Screenshots at **1440** and **390**: stage photo (or video) visible without scrolling; hero CTA visible.  
- [ ] ≥2 talk videos embedded or clearly linked on the page.  
- [ ] Booking CTA above fold **and** at page end.

### Evals

- [ ] Video embeds lazy-load; no autoplay; Lighthouse LCP within 25% of previous page baseline (hero still should remain LCP).  
- [ ] All media and links 200 logged out; images from media library (`kriskrug.co/wp-content/uploads/…` via `i0.wp.com`) with alt text.  
- [ ] 5-second test: stranger says this person speaks on stages and can be booked.  
- [ ] `curl -sL https://kriskrug.co/speaking/ | grep -c 'youtube.com/embed'` → ≥2  
- [ ] `curl -sL https://kriskrug.co/speaking/ | grep -c 'Start a booking conversation'` → ≥2  
- [ ] Hotlink hosts `bothhandsfull.com/opengraph-image` and `punkrockai.com` image URLs absent from entry content after apply.

### Safety

- [ ] Pre-edit snapshot under `backup/`  
- [ ] Pagely purge after write  
- [ ] Logged-out smoke  
- [ ] Rollback path documented (restore before JSON)  
- [ ] No live write from this draft package without KK sign-off
