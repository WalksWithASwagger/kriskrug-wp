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

## Booking claim-to-source matrix (#904)

The Profound export identifies the planner question only. It is not a factual source. KK's 2026-08-27 ruling is authoritative for the location update: Vancouver only. Prior residence labels are retired.

| Claim family | Visible claim | Current first-party source |
|---|---|---|
| Identity and location | Kris is an AI keynote speaker based in Vancouver, British Columbia, Canada. | KK ruling for #904, 2026-08-27; `fixes/schema-snippets-deployed.php` (`person_job`, `person_descr`) |
| Formats | Keynotes, workshops, executive briefings, and hosting and moderation. | Existing Formats cards in `payload-body.html`; public page 1887 readback, 2026-08-27 |
| Audiences and topics | Leaders, creators, creative teams, executives, schools, nonprofits, companies, public-interest technology audiences, public sector groups, and cultural organizations; creative agency, human judgment, leadership, trust, consent, power, and organizational memory. | `content/source-packs/keynotes-2026/talk-topic-bank.md`; existing Formats cards in `payload-body.html` |
| Booking inputs | Audience, date, location, format, and the room's question. | Existing end-booking CTA in `payload-body.html`; public page 1887 readback, 2026-08-27 |
| Next step | Contact Kris through `/contact/`. | Existing hero and end-booking links in `payload-body.html`; public page 1887 readback, 2026-08-27 |

---

## Content changes (six-talk architecture)

| Band | Change |
|---|---|
| Hero | Cleared Meetup 30 theme still (`loading="eager"`) + short support line + booking CTA |
| Planner facts | Answer-first Vancouver, British Columbia, Canada identification + five source-backed booking facts from the matrix above |
| Signature keynotes | Six cards from `talk-topic-bank.md`, in bank order. Status tags: delivered / available in development / program option |
| Watch | Two accessible click-to-load facades with inert `youtube-nocookie.com` iframes: `hYT-hsml_ds` (CreativeMornings / Punk Rock AI) and `-c7mgY2aSgM` (LaSalle / Both Hands Full). CreativeMornings credit line included. |
| Workshop add-ons | The seven topic-bank add-ons. Labeled as add-ons, not keynotes. |
| Formats | Same four cards |
| End CTA | Second booking CTA plus specific proof links to `/events/` and `/testimonials/`. Name spelled Kris Krüg. |

Removed from the prior draft: Responsible AI as a signature card; LaSalle stills; Michelle Diamond 184 / 195; Vancouver AI March 2026 and ChannelNext as the lead videos; any seventh taxonomy.

Page-scoped CSS under `.kk-r9-pack` keeps the cream rail, hero media, and 16:9 embeds.

## Schema and proof-triangle preparation (#641)

- `fixes/schema-snippets-deployed.php` prepares exactly two `VideoObject` records for page `1887`, one for each embedded recording.
- Both records reuse the canonical Person only through `about: {"@id":"https://kriskrug.co/#person"}`. No Event, Service, creator, publisher, or inline Person node is added.
- The final booking card links to `/events/` and `/testimonials/`. Both targets already link back to `/speaking/`, so their page bodies are unchanged in this lane.
- The schema change is repo-prepared only. Production snippet ID `5` still requires a fresh authenticated snapshot, exact-diff approval, bounded save, cache-busted readback, and rollback proof after the body deployment.

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
- Live Code Snippets or schema deployment
- Autoplay or background video

## Apply procedure (after KK approval)

1. Confirm secrets: `WP_USER` + `WP_APP_PASSWORD` present (length check only).
2. Authenticated GET page `1887`; write `backup/<timestamp>-speaking-419/page-1887-before.json` + rendered HTML.
3. Dry-run: print payload bytes; confirm `booking-facts` appears before `signature-keynotes`; confirm five planning cards; confirm six `<h3>` talk titles; confirm `Responsible AI` absent from the keynote grid; confirm two `youtube-nocookie.com` embed URLs; confirm hero `<img>` is the Meetup 30 theme asset; confirm CTA count ≥2; confirm the `/events/` and `/testimonials/` proof links.
4. KK signs media constraint + copy + screenshots plan.
5. Body-only REST update (`content` raw = `payload-body.html`). Do not send `title`.
6. Purge Pagely page cache for `/speaking/`.
7. Logged-out verification (checklist below).
8. If bad: restore snapshot `content.raw`.

## Verification checklist (issue acceptance + evals)

### Acceptance

- [ ] Six talks match the topic bank. No seventh keynote card. Responsible AI is not in the grid.
- [ ] The answer-first block appears before the keynote grid and identifies Kris as an AI keynote speaker based in Vancouver, British Columbia, Canada.
- [ ] Five planning cards cover location, formats, audiences and topics, booking inputs, and the `/contact/` next step.
- [ ] Screenshots at **1440** and **390**: Meetup 30 still visible without scrolling; hero CTA visible.
- [ ] ≥2 talk videos embedded (CreativeMornings + LaSalle).
- [ ] Booking CTA above fold **and** at page end.
- [ ] The final booking card links to `/events/` and `/testimonials/` with specific anchor text.

### Evals

- [ ] Video facades keep both iframes inert until activation; no autoplay.
- [ ] No uncleared stage photos: no `kk-laSalle-both-hands-full-*`, no `AI_Meetup_August2024_MichelleDiamond-184`, no `MichelleDiamond-195`, no `punkrockai.com/public/photos`.
- [ ] Hero image is the Meetup 30 theme asset with Michelle Diamond credit in the caption, not the alt.
- [ ] 5-second test: stranger says this person speaks on stages and can be booked.
- [ ] `grep -c 'youtube-nocookie.com/embed'` on the payload → 2
- [ ] `grep -c 'Start a booking conversation'` on the payload → 2
- [ ] Zero em dashes. Brand: Kris Krüg, BC + AI where named.

### Safety

- [ ] Pre-edit snapshot under `backup/`
- [ ] Pagely purge after write
- [ ] Logged-out smoke
- [ ] Rollback path documented (restore before JSON)
- [ ] No live write from this draft package without KK sign-off
