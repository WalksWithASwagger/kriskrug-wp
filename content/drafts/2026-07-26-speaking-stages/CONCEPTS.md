# Concepts: three art directions for `#stages`

Each concept is buildable inside Aurora (`front-page.html` + `revive-port.css`) without touching the newsletter band. Markup stubs live in `markup/`.

Shared requirements (all concepts):

- Image-led, not text-on-white
- Every engagement is a real link (200 logged out)
- Hover **and** `:focus-visible` states
- Stage photography as backbone; venue/event logos optional secondary
- Mobile: stacks cleanly at 375; no orphan logos
- No em dashes in copy

---

## Concept A - Photo marquee (recommended default)

**One-liner:** Horizontal (desktop) / stacked (mobile) strip of stage stills. Each tile is the engagement. Hover lifts the photo and reveals talk title + destination type.

**Composition**

- Kicker + short H2 above a full-bleed-feeling rail (edge-to-edge within `--revive-max` or slightly past it)
- 5 to 7 tiles; each tile = photo + event name + talk title + chevron
- Optional mono event mark in a corner (only when a cleared SVG/PNG exists in media library)

**Interaction**

- Hover/focus: scale 1.02, warm underline on title, soft vignette lifts so text stays AA
- Keyboard: each tile is one `<a>`; focus ring uses existing Aurora focus token
- Optional: slow CSS scroll on `prefers-reduced-motion: no` for overflow; never autoplay video here

**Why it wins**

- Direct answer to "image-led"
- Hides nothing: talk titles are visible on hover/focus and partially at rest on desktop
- Plays to KK's stage photo archive

**Risks**

- Needs 5+ cleared stage action photos (portraits alone fail the brief; see `VISUALS.md`)
- Crop discipline at 375 / 768 / 1440

**Markup:** `markup/concept-a-photo-marquee.html`

---

## Concept B - Receipt cards (linked dossier)

**One-liner:** Dense but calm grid of engagement cards. Photo crop left or top; event, year, talk title, and one-line outcome. Looks like a booking dossier, not a logo wall.

**Composition**

- Section head: kicker "Stages with receipts" + H2 + link to `/speaking/`
- 2x3 or 3x2 card grid
- Card anatomy: image (3:2), event label, talk title (linked), meta line ("Keynote · 2026 · Watch" / "Writeup")

**Interaction**

- Whole card is one link (avoid nested interactive elements)
- Hover: border + image brightness; focus-visible outline on card
- Optional secondary chip for destination type (Video / Portal / Writeup) as non-interactive text

**Why it wins**

- Strongest for "every stage links somewhere real"
- Easy to QA (link checklist maps 1:1 to cards)
- Scales when more talks get published writeups

**Risks**

- Can feel card-heavy if over-styled; keep flat: no drop shadows, no pill clusters
- Needs disciplined copy length so cards align

**Markup:** `markup/concept-b-receipt-cards.html`

---

## Concept C - Featured reel + supporting stages

**One-liner:** One large featured stage (photo + watch CTA) with a compact linked list of supporting rooms beside/below. Closest to `speaking-proof-grid` energy, tuned for homepage height budget.

**Composition**

- Left/top: hero still from LaSalle or CreativeMornings with overlaid title block (scrim for AA)
- Right/bottom: 4 to 6 text+thumb rows (ChannelNext, Vancouver AI, Web Summit, Bass Coast, Whistler, Futureproof)
- Closing line: "Book a room" -> `/contact/` or `/speaking/`

**Interaction**

- Featured: primary button "Watch the talk" + secondary "Speaking page"
- List rows: hover slides a thin accent bar; focus-visible on each row link
- No autoplay; YouTube only on click-through

**Why it wins**

- Sells the keynote hardest (good bridge to #419)
- Uses one hero photo well when the full stage archive is not yet curated

**Risks**

- Can steal thunder from the masthead stage photo if too tall; keep section max ~80vh on desktop
- Overlay text needs careful contrast testing

**Markup:** `markup/concept-c-featured-reel.html`

---

## Hybrid note

If KK likes A visuals + B rigor: ship Concept A tiles, but keep the Concept B destination table as the source of truth for URLs and labels.

## Out of concept scope

- Client logo soup (#413)
- Newsletter thumbs (#416 / PR #505)
- Full Speaking page multimedia rebuild (#419)
- Testimonial / network diagram (#415)
