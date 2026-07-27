# Speaking page audit - #419

**Status:** draft only. Public HTML readback. No live WP write.  
**Fetched:** 2026-07-26 (public `GET https://kriskrug.co/speaking/`)  
**WP page ID:** 1887  
**Evidence:** `evidence/public-entry-content-2026-07-26.html`, `evidence/snapshot-meta.json`

## Issue claim (KK teardown 2026-07-17)

> My speaking section is not selling any keynotes. It's way below the fold before you get to any actual photos of me on stages. There's no videos. I've got great talks online, great photos online. This should be a multimedia extravaganza that makes people want to hire me.

## Live structure (2026-07-26)

Page body is a single `<!-- wp:html -->` pack (`content-architecture-2026:speaking`), matching `content/source-packs/content-architecture-2026/wp-payloads/speaking.html` plus R9 button/card CSS:

1. Lead - kicker `Speaking`, display H2, lead paragraph (text only)
2. Formats - 4× `.aurora-card` (Keynotes / Workshops / Executive briefings / Hosting)
3. Signature topics - 4× `.aurora-media-card` (Both Hands Full, Punk Rock AI, Developing an AI mindset, Responsible AI)
4. CTA - single `.aurora-card` (`Book Kris for a keynote` → `/contact/`)

Title/meta (public):

| Field | Value |
|---|---|
| `<title>` | AI Keynote Speaker Kris Krüg | Humanizing AI, Creativity & Community |
| Meta description | Book Kris Krüg for AI keynotes, workshops, podcast guesting, moderation, hosting, and emcee work on creativity, community, and responsible technology. |
| Canonical | `https://kriskrug.co/speaking/` |
| OG image | library photo `5156893053_e4e246abb4_k.jpg` (not a stage shot) |

## Finding 1 - No talk videos on the page (confirmed)

| Probe | Result |
|---|---|
| `<iframe>` in full HTML | **0** |
| `youtube` / `youtu.be` / `vimeo` in `<main>` | **0** |
| WP embed / video blocks | none |

Fails acceptance: "At least 2 embedded or linked talk videos on the page."

Repo already has a curated public video research index at `content/source-packs/keynotes-2026/video-research/README.md` (LaSalle, Bass Coast, ChannelNext, Whistler, Vancouver AI March 2026, STORYHIVE). None of those URLs appear on the live Speaking page.

## Finding 2 - Stage photography is below the fold (confirmed)

Order of visuals in entry content:

| # | Image | What it is | Stage photo? |
|---|---|---|---|
| 1 | `bothhandsfull.com/opengraph-image…` | portal graphic (hotlinked) | no |
| 2 | `punkrockai.com/.../195.webp` | portal / event photo (hotlinked) | weak / not owned stage hero |
| 3 | `AI-Immortality-w-Guy-Kawasaki.png` | keynote graphic | no |
| 4 | `kk-laSalle-both-hands-full-10-scaled.jpg` | Kris on stage at LaSalle | **yes** (only one) |

Text before the first `<img>` in `<main>` is the whole lead + Formats block. At 1440 and 390 that means: H1 chrome, Speaking kicker, H2, lead, Formats grid, then media cards. A stranger does not see Kris on a stage without scrolling.

Fails acceptance: "At 1440 and 390, a stage photo or video is visible without scrolling."

## Finding 3 - Booking CTA only at page end (confirmed)

`Start a booking conversation` → `/contact/` appears **once**, in the final section.

Fails acceptance: "Booking CTA present above the fold and at page end."

Coordinates with the separate CTA decision issue; this package drafts dual CTAs (hero + end) pointing at `/contact/` so the page can ship once KK confirms the booking path.

## Finding 4 - Media quality / ownership issues in the topics grid

- Two of four topic images are **third-party hotlinks** (`bothhandsfull.com`, `punkrockai.com`), not media-library assets.
- Issue evals require: images from media library with alt text; all media/links 200 logged out.
- Only one owned stage photo is used, and it is tied to the Responsible AI card rather than the hero.

Sponsor-deck drafts already point at stronger owned stage assets (verified 200 on 2026-07-26):

- `…/2026/05/kk-laSalle-both-hands-full-25-scaled.jpg`
- `…/2026/05/kk-laSalle-both-hands-full-10-scaled.jpg`
- `…/2024/09/AI_Meetup_August2024_MichelleDiamond-184-scaled.jpg`
- `…/2024/09/AI_Meetup_August2024_MichelleDiamond-195-scaled.jpg`

## Finding 5 - 5-second test currently fails

Live first viewport sells: title + abstract claim + four text format cards. It does **not** sell: "this person speaks on stages and I can book them."

## Root cause summary

| Problem | Root cause | Fix lane |
|---|---|---|
| No videos | Content-architecture pack never embedded talks | Track A page content |
| Stage media below fold | Lead + Formats first; topics third | Track A page content (reorder) |
| CTA only at end | Single terminal card | Track A page content (+ CTA issue) |
| Weak / hotlinked media | Topic cards use portal OG images | Track A: library stage photos + embeds |

## Recommended direction

See `multimedia-rebuild-plan.md` (media inventory + layout), `copy-options.md` (recommend **Option A**), and `payload-plan.md` / `payload-body.html` for the apply-ready body.
