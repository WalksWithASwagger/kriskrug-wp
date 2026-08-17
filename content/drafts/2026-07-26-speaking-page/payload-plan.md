# Payload plan - Speaking multimedia rebuild (#419)

**Mode:** DRAFT ONLY. Do not PATCH live WP from this package without KK approval + authenticated snapshot.
**Target:** page ID `1887`, slug `speaking`, URL https://kriskrug.co/speaking/
**Taxonomy:** KK #638 ruling 2026-08-17. Six-talk topic bank. Workshops are add-ons. No seventh keynote card. Responsible AI is not a signature talk.
**Apply-ready body:** `payload-body.html`

---

## Asset constraint (say this plainly)

#419's binding criterion is a stage photo or video visible without scrolling at 1440 and 390.

Cleared stills are not enough for a photo strip. The #637 inventory found one photographer-cleared stage-action frame with written site-use approval:

1. `theme/kk-aurora/assets/img/vancouver-ai-meetup-30-kris-community.jpg` (and the 600 / 1200 webp derivatives). Vancouver AI Meetup 30, H.R. MacMillan Space Centre, June 2026. Photo: Michelle Diamond, Diamond's Edge Photography. KK committed it as the canonical approved event photo (`6b0ae1d`).

The second local stage still, `content/source-packs/keynotes-2026/assets/punk-rock-ai-creative-mornings.jpg`, is **not cleared**. LaSalle library frames 11830 to 11834 have no photographer on file. Meetup stills 6854 and 6847 are not photographs of Kris Krüg. Punkrockai.com hotlinks are out.

So the payload is designed around **that one cleared stage-action frame** as the above-the-fold still, plus **two recorded talk embeds** (CreativeMornings / Punk Rock AI, LaSalle / Both Hands Full). No uncleared stage photos. No invented seventh talk.

The Meetup 30 frame reads as community-host energy, not keynote-buyer energy. The six-talk bank and the two recordings carry the keynote claim.

---

## Goals (acceptance criteria)

1. Media inventory (videos + photos with sources) documented for KK curation. See `photography-inventory.md`, `video-set.md`, and the constraint above.
2. At 1440 and 390, a stage photo or video is visible without scrolling. Hero still is the first content block after the heading.
3. At least 2 embedded or linked talk videos on the page.
4. Booking CTA present above the fold and at page end.

---

## Content changes (six-talk architecture)

| Band | Change |
|---|---|
| Hero | Cleared Meetup 30 theme still (`loading="eager"`) + short support line + booking CTA |
| Signature keynotes | Six cards from `talk-topic-bank.md`, in bank order. Status tags: delivered / available in development / program option |
| Watch | Two lazy YouTube iframes: `hYT-hsml_ds` (CreativeMornings / Punk Rock AI) and `-c7mgY2aSgM` (LaSalle / Both Hands Full). CreativeMornings credit line included. |
| Workshop add-ons | The seven topic-bank add-ons. Labeled as add-ons, not keynotes. |
| Formats | Same four cards |
| End CTA | Second booking CTA. Name spelled Kris Krüg. |

Removed from the prior draft: Responsible AI as a signature card; LaSalle stills; Michelle Diamond 184 / 195; Vancouver AI March 2026 and ChannelNext as the lead videos; any seventh taxonomy.

Page-scoped CSS under `.kk-r9-pack` keeps the cream rail, hero media, and 16:9 embeds.

---

## What stays intact

- Pack marker `<!-- content-architecture-2026:speaking -->`
- Wrapper classes compatible with live R9 pack (`kk-page kk-r9-pack`)
- `/contact/` as booking path
- Title field (do not send `title` in REST update)

## Out of scope

- Homepage Speaking section (#414)
- Theme file edits / Track B / Aurora bump
- Importing YouTube thumbnails into the media library
- Ingesting Meetup 30 into the media library (apply lane, not this one)
- Live PATCH of page 1887
- Autoplay or background video

## Apply procedure (after KK approval)

1. Confirm secrets: `WP_USER` + `WP_APP_PASSWORD` present (length check only).
2. Authenticated GET page `1887`; write `backup/<timestamp>-speaking-419/page-1887-before.json` + rendered HTML.
3. Dry-run: print payload bytes; confirm six `<h3>` talk titles; confirm `Responsible AI` absent from the keynote grid; confirm ≥2 youtube embed URLs; confirm hero `<img>` is the Meetup 30 theme asset; confirm CTA count ≥2.
4. KK signs media constraint + copy + screenshots plan.
5. Body-only REST update (`content` raw = `payload-body.html`). Do not send `title`.
6. Purge Pagely page cache for `/speaking/`.
7. Logged-out verification (checklist below).
8. If bad: restore snapshot `content.raw`.

## Verification checklist (issue acceptance + evals)

### Acceptance

- [ ] Six talks match the topic bank. No seventh keynote card. Responsible AI is not in the grid.
- [ ] Screenshots at **1440** and **390**: Meetup 30 still visible without scrolling; hero CTA visible.
- [ ] ≥2 talk videos embedded (CreativeMornings + LaSalle).
- [ ] Booking CTA above fold **and** at page end.

### Evals

- [ ] Video embeds lazy-load; no autoplay.
- [ ] No uncleared stage photos: no `kk-laSalle-both-hands-full-*`, no `AI_Meetup_August2024_MichelleDiamond-184`, no `MichelleDiamond-195`, no `punkrockai.com/public/photos`.
- [ ] Hero image is the Meetup 30 theme asset with Michelle Diamond credit in the caption, not the alt.
- [ ] 5-second test: stranger says this person speaks on stages and can be booked.
- [ ] `grep -c 'youtube.com/embed'` on the payload → 2
- [ ] `grep -c 'Start a booking conversation'` on the payload → 2
- [ ] Zero em dashes. Brand: Kris Krüg, BC + AI where named.

### Safety

- [ ] Pre-edit snapshot under `backup/`
- [ ] Pagely purge after write
- [ ] Logged-out smoke
- [ ] Rollback path documented (restore before JSON)
- [ ] No live write from this draft package without KK sign-off
