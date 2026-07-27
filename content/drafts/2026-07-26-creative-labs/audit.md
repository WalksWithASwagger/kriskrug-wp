# Audit: Creative Labs / Current work triptych (#412)

**Readback:** 2026-07-26 public homepage + repo `theme/kk-aurora/templates/front-page.html` on `main` (Aurora line post-1.4.8).
**Scope:** Homepage `#work` / `.aurora-work-band` only.
**No live writes.**

## Mapping

| KK language (issue #412 / pill bug) | Live / repo surface |
|---|---|
| Creative Labs section | `.aurora-work-band` labeled **Current work** |
| Pill / overlay breakage | `.aurora-work-card-body` absolutely positioned on image + `.aurora-work-card-media::after` gradient scrim |
| Ecosystem / Festival | Card kickers today are **Community** / **Festival** / **Tour** (services band has a separate Ecosystem card; out of scope) |

There is **no** string "Creative Labs" on the live homepage. The redesign includes naming the band so a stranger can say what it is.

## Live structure (verbatim shape)

- Kicker: `Current work`
- H2: `What Kris is building now.`
- Index link: `/work/`
- Three full-card links:
  1. `https://bc-ai.ca/`  -  Community / BC + AI
  2. `https://www.futureproof.website/`  -  Festival / Futureproof
  3. `/speaking/`  -  Tour / Keynotes 2026

## Failures against acceptance

### 1. Cryptic (fails 5-second test)

A stranger sees three tall images with faint numbered overlays and short jargon blurbs. "Current work" does not say **labs**, **what Kris builds in public**, or **where to go next**. Kickers (Community / Festival / Tour) are category tags, not plain descriptions of who KK is.

Jargon hotspots in live card copy:

- "Province-wide trust layer for responsible AI"
- "frontier tech, creative practice, and civic trust share one public room"
- "operating conditions for responsible AI"

### 2. Overlay / pill layout

In `revive-port.css`, card body text sits **on** the photo:

- `position: absolute; bottom/left/right` on `.aurora-work-card-body`
- Gradient scrim via `::after`
- Accent kicker forced with `!important`

That is the broken "pill section" feel: text fighting the crop, contrast tied to photo luck, hover scale making copy harder to read. Pill CSS root-cause may still land via the shared overlay bug; this redesign should **stop depending** on overlay copy either way.

### 3. Image crops and sources

| Card | Current asset | Native-ish size | Forced frame | Problem |
|---|---|---|---|---|
| BC + AI | `bc-ai.ca` … `bcai-living-ecosystem.webp` | ~899×600 landscape graphic | `aspect-ratio: 3/4` + `object-fit: cover` | Graphic, not people/place; center crop chops diagram edges |
| Futureproof | `futureproof.website` OG share JPG | 1200×630 | 3/4 cover | Marketing key art, not festival room; bad portrait crop |
| Keynotes | punkrockai Michelle Diamond webp | ~1200×800 landscape | 3/4 cover | Stage photo can lose head/hands depending on focal point; external host |

Acceptance requires Media Library + alt text + **no hotlinks**. Two of three cards are off-site; none are art-directed for 3:4.

### 4. Desktop stagger

At ≥900px, card 02 gets `margin-top: -2.5rem`. Looks intentional; also makes alignment feel "off" next to overlay text. Layout proposal drops or softens this unless KK wants the stagger with text-below-image.

## What still works (keep)

- Three-project spine is right: BC + AI, Futureproof, keynotes/speaking.
- Destination URLs are correct (external projects + `/speaking/`).
- Section sits in the right homepage slot (after contact sheet, before services).
- Full-card click target is fine if focus/hover rings stay intact (see interaction inventory).

## Collision notes

- **PR #505** edits newsletter on the same `front-page.html`. Do not ship a competing theme PR from this lane until that lands or this is rebased onto it with an isolated `#work` hunk.
- **#411** Join BC / Futureproof: different section; not present on Revive home. Copy should not reintroduce "rooms" language from that teardown.
- Shared pill/overlay bug: consume when fixed; do not add per-card `!important` patches here.

## 5-second test (current)

**Prompt:** What is this section?

**Likely answer today:** "Three projects with fancy photos." Missing: that these are Kris's public creative/civic labs, what each one does in one plain line, and that you can join or hire from here.

**Target answer after redesign:** "Creative Labs: the three things Kris builds in public. BC + AI community, Futureproof festival, and keynotes. Each card says what it is and where to go."
