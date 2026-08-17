# Alt-text inventory — issue #4 (2026-08-16)

**Mode:** read-only live sample + prior-art reconciliation. No media PATCH, no `post_content` write, no snippet edit.
**Captured:** 2026-08-16 evening PT, logged-out `curl` / `scripts/public_image_audit.py` GET only.
**Branch:** `docs/4-alt-text-inventory-20260816`
**Does not replace:** `content/drafts/alt-text-backfill-2026-08-02/inventory.md` (216-route crawl, still the apply-ready plan). This file answers whether that plan is still true on the live site two weeks later.

---

## Verdict

**#4 is still a real gap, but not on the front door.** Homepage, `/about/`, `/work/`, `/speaking/`, `/photography/`, and the two most recent posts are clean for content `<img>` alt. The remaining debt is inner marketing pages, two 2026 post heroes that still ship `alt=""`, one unlinked `/home/` leftover, and archive meetup galleries.

Do not close #4. Do not start a new sitewide alt-writing pass. Apply the 2026-08-02 batch plan (still unapplied) after KK approval.

Acceptance criteria on #4 remain **0 of 7 met**. Every criterion is about live images. Zero live writes have shipped since the August inventory.

---

## What prior passes already covered (do not redo)

| When | Artifact | What it proved | Live writes? |
|---|---|---|---|
| 2026-06-17 | #4 comment + `wp_post_ia_rollout.py --since 2025-01-01` | Recent published posts: `missing_featured_alt=0`. One filename-style content alt on post 577 fixed. | One content-only replace on `/flickr-photographr-badge/` |
| 2026-06-18 | `make public-image-audit`, `docs/current-state/reports/public-image-audit-20260618-default.md` | 8 default routes, 89 images: missing-attr = FB pixels, empty non-decorative = 0 on that default set except `/home/` later | None |
| 2026-07-02 | Child **#287 CLOSED** | 76 images / 8 pages. Tracking pixel + decorative wordmark. One `/home/` crowd-shot candidate. | None |
| 2026-07-16 | `docs/current-state/reports/issue-4-public-image-alt-20260716.md` | Same pixel/wordmark pattern | None |
| 2026-07-26 | PR **#524 MERGED**, `docs/current-state/reports/alt-text-inventory-20260726.md` | High-vis Aurora surfaces clean; `/home/` media 6835 empty | None |
| 2026-08-02 | PR **#658 MERGED**, `content/drafts/alt-text-backfill-2026-08-02/` | 216 routes, 1,185 content images with no usable alt. Top 10 routes clean. 35 apply-ready strings for 36 attachments. Two-surface finding: library writes miss in-content blocks. | **None. Plan only.** |
| 2026-08-10 | `docs/current-state/reports/featured-image-audit-2026-08-10.md` | Featured **crops**, not alt. 2026 post heroes swapped; alt on those new files was already written (Futureproof 12739, Keep the Machine Strange 12720 confirmed this pass). | Featured swaps, not an alt backfill |

Closed children of #4: **#287** (inventory), **#176** (top-20 audit packet). Neither applied live alt. Featured-image coverage for posts since 2025-01-01 was already called clean in June; this pass confirms recent 2026 posts still have descriptive featured alt **except** two heroes that share empty library `alt_text` with `/home/` (media 12646 and 6835).

---

## Sample this pass

Two concentric samples. Cache-busted public HTML. Classifier: `scripts/public_image_audit.py` (`missing-attr` / `empty` / `decorative-empty` / `filename-style` / `ok`).

### A. Requested high-visibility set (the original ask)

| Route | Images | Content OK | Empty content | Missing attr | Filename-style |
|---|---:|---:|---:|---:|---:|
| `/` | 17 | 16 | **0** | 1 (FB pixel) | 0 |
| `/about/` | 7 | 6 | **0** | 1 | 0 |
| `/work/` | 14 | 13 | **0** | 1 | 0 |
| `/speaking/` | 6 | 5 | **0** | 1 | 0 |
| `/photography/` | 19 | 18 | **0** | 1 | 0 |
| `/2026/08/11/futureproof-festival-announcement/` | 12 | 11 | **0** | 1 | 0 |
| **Subtotal A** | **75** | **69** | **0** | **6** | **0** |

Also checked (not in the original six, same conclusion): `/blog/` 21/20/0, `/contact/` 3/2/0, `/2026/08/10/keep-the-machine-strange/` 5/4/0.

Matches the 2026-08-02 "top routes are clean" claim. Still true.

### B. Known-dirty confirmation set (to avoid a false "done")

| Route | Images | Content OK | Empty content | Missing attr |
|---|---:|---:|---:|---:|
| `/home/` (unlinked legacy) | 14 | 11 | **2** | 1 |
| `/2026/07/31/ai-lands-inside-every-profession/` | 12 | 10 | **1** (hero 12646) | 1 |
| `/2026/06/30/zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey/` | 3 | 1 | **1** (hero 6835) | 1 |
| `/cinematic-podcasts-hollywood-grade-storytelling-meets-generative-ai/` | 4 | 1 | **2** | 1 |
| `/ai-upgrade-for-creative-professionals/` | 14 | 2 | **11** | 1 |
| `/motleykrug-podcast/` | 12 | 5 | **6** | 1 |
| `/art-island-perspectives-from-a-creative-community/` | 9 | 4 | **4** | 1 |
| `/reconciliation-indigenous-land-acknowledgement/` | 5 | 3 | **1** | 1 |
| `/flickr-photographr-badge/` | 4 | 2 | **1** | 1 |
| `/2024/09/01/august-vancouver-ai-community-meetup-recap-hackers-hustlers-heretics/` | 42 | 2 | **39** | 1 |
| **Subtotal B** | **119** | **41** | **68** | **10** |

### Combined

| | Count |
|---|---:|
| Pages sampled | 19 |
| `<img>` occurrences | 223 |
| Descriptive alt (`ok`) | 136 |
| Empty content alt (`alt=""`) | **68** |
| Missing `alt` attribute | **19**, all Meta noscript `facebook.com/tr?id=1720755522050230` |
| Filename-style alt | 0 in this sample |
| Decorative-empty (classifier) | 0 |

Ranked by empty content alts: August 2024 meetup recap (39) >> AI Upgrade course page (11) >> Motleykrug (6) >> Art Island (4) >> cinematic-podcasts (2) = `/home/` (2) >> four single-hero pages (1 each). The six requested front-door routes sit at 0.

---

## Empty alt vs missing alt vs decorative

**Empty `alt=""` on content images is a violation here, not a decorative pattern.** None of the 68 empties matched decorative markers (`aurora-brand-logo`, `custom-logo`, `site-logo`, `pixel`, `tracking`, `spacer`). They are photos, course cards, podcast covers, and gallery frames that a screen reader currently skips.

**Missing `alt` (no attribute) is the Meta Pixel noscript 1x1, one per route.** `scripts/public_image_audit.py` classifies these as `missing-attr` because `facebook.com/tr` does not contain the substring `pixel`. They are tracking beacons, not content. Correct treatment is `alt=""` (or stop emitting `<img>`). They are **not** in the 68. Pixel is injected by a WP snippet/plugin, not Aurora: `theme/kk-aurora/` has no `facebook.com/tr` match. Related: #706 script-diet wanted the pixel gone; if it stays, the a11y fix is one snippet edit.

**Wordmark is no longer empty.** Header `img.aurora-brand-logo` renders `alt="Kris Krug home"` inside `<a class="aurora-brand" aria-label="Kris Krug home">` (`theme/kk-aurora/parts/header.html`). That is why `decorative-empty` is 0. Child #294 already closed the brand-name question. Redundant name (alt + aria-label) is a Track B polish, not a #4 gap. Leave it.

**Library alt does not always win.** Media 2596 still has REST `alt_text="On location in the studio of Gordon Payne on Hornby Island"` and still renders `alt=""` on `/art-island-perspectives-from-a-creative-community/`. Same two-surface bug as 2026-08-02: in-content image blocks bake empty alt into `post_content`. A media-library-only batch would no-op on that page.

---

## Highest-impact missing alts (looked at the file)

Only strings for images opened at ~800px this pass. Meetup-gallery frames I did not open are listed as a batch, not invented.

Encoding: write `ü` as `&#252;` on apply (latin1 / NCR rule from the August inventory). ASCII below except that NCR.

| # | Impact | Media | Where it renders | Surface | Proposed alt |
|---:|---|---:|---|---|---|
| 1 | Above-fold post hero | 12646 | `/2026/07/31/ai-lands-inside-every-profession/` hero; `/home/` card. Library `alt_text=""`. Same file also appears in-body on that post **with** a good alt (`Crowded Vancouver AI Meetup gathering in the H.R. MacMillan Space Centre planetarium…`), so the hero is the bug. | media-library `alt_text` | `Vancouver AI Meetup 30 spillover in the Space Centre courtyard, name-tagged crowd talking in clusters, shot from the balcony` |
| 2 | Above-fold post hero | 6835 | `/2026/06/30/zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey/` hero; `/home/` card; in-body on the Aug 2024 recap. Library title is the useless `Evoto`. | library + one `post_content` block | `Vancouver AI meetup crowd packed into an industrial studio under blue and magenta light, watching a speaker off camera` |
| 3 | Course page, near-fold | 7523 | `/ai-upgrade-for-creative-professionals/` | `post_content` | `Instructor card: Peter Bittner, Founder and CEO of The Upgrade, multimedia journalist and UC Berkeley lecturer, beside Kris Kr&#252;g, Founder and CEO of Future Proof Creatives, artist, educator and consultant` |
| 4 | Course page headshots | 7530 | same | `post_content` | `Portrait of Kris Kr&#252;g in a black beanie against teal and orange light, labelled Founder and CEO, Future Proof Creatives, artist, educator, consultant` |
| 5 | Course page headshots | 7529 | same | `post_content` | `Black and white portrait of Peter Bittner labelled Founder and CEO, The Upgrade, new media journalist and lecturer at UC Berkeley Graduate School of Journalism` |
| 6 | Course social proof | 7524 | same | `post_content` | `Logo wall headed Our students and clients have come from, showing UCLA, Apple, IBM, Berkeley, Adobe, NASA, Amazon, Columbia Business School, National Geographic, Accenture, UC Davis, Emily Carr, United Nations, RBC, Vancouver Film School, BCIT, Salesforce, Fleishman Hillard, Saatchi and Saatchi and News Product Alliance` |
| 7 | Podcast page hero | 2872 | `/motleykrug-podcast/` | `post_content` | `M&#216;TLEYKR&#220;G podcast cover: an AI portrait of Kris Kr&#252;g with a braided mohawk and long beard standing in neon rain, the word KR&#220;G in green glitch type` |
| 8 | Service page | 7765 | `/cinematic-podcasts-hollywood-grade-storytelling-meets-generative-ai/` | `post_content` | `A speaker in a blazer, jeans and sneakers presenting under magenta LED tubes in a warehouse gallery hung with collage paintings, a Prompt Pix sign on the floor` |
| 9 | Service page | 7766 | same | `post_content` | `Two YouTube cards side by side: Carrie Cassel on transforming education for the age of AI, and Rajith on mastering Kubernetes at AWS Community Day` |
| 10 | Art Island cover | 2592 | `/art-island-perspectives-from-a-creative-community/` | `post_content` | `Art Island episode 4 cover, Sea Changes: painter Michelle Nyberg in black-framed glasses beside one of her floral abstracts on an easel, Hornby Arts logo below` |
| 11 | Art Island BTS (library already has alt) | 2596 | same, renders empty anyway | `post_content` (do **not** only PATCH media) | `Painter Gordon Payne at his easel in his Hornby Island studio while a camera operator frames the shot on a gimbal and a boom mic hangs overhead` |
| 12 | Art Island BTS | 2597 | same | `post_content` | `A photographer crouched on a wide empty tidal flat with a Canon 5D Mark III and a tripod, mountains and low cloud on the horizon` |
| 13 | Art Island BTS | 2595 | same | `post_content` | `Behind the scenes on Art Island: an interview in a woodstove cabin under a round LED softbox, boom mic overhead, camera on a tripod` |
| 14 | Land acknowledgement | 3901 | `/reconciliation-indigenous-land-acknowledgement/` | `post_content` | `Round white vinyl sticker with a hand-drawn LAND BACK logo, two arrows circling the words` |
| 15 | Legacy badge | 12604 | `/flickr-photographr-badge/` | `post_content` or media | `Early Flickr Photographer badge for kk+: Flickr beta logo, contact lines, a portrait of Kris shooting through a camera, barcode, and a handwritten KK+ signature` |

Course-page testimonial cards (7535, 7536, 7539, 7540, 7541, 7542) are empty images of text. I did not re-open them this pass. Apply-ready quote-in-alt strings already live in `content/drafts/alt-text-backfill-2026-08-02/inventory.md` batch 1. Same for remaining Motleykrug episode covers 2873, 2874, 2877, 3003, 3010 (3003 failed to download this pass; do not invent).

**Not authored:** the other 38 empty frames on the August 2024 meetup recap. Filenames name people (`brittney-smaila`, `ed-kennedy`, `anita-enya`, Michelle Diamond contact sheets). That is a visual gallery pass, not a filename-to-alt script.

---

## Recommended split

| Lane | What | Why | First move |
|---|---|---|---|
| **Theme / snippet (Track B or Code Snippets)** | Meta Pixel noscript `<img>` missing `alt` | One edit clears every route. Not a media record. Pixel is not in Aurora source. | If #706 keeps the pixel: add `alt=""`. If #706 kills the pixel: this finding dies with it. Do not PATCH 2,000 attachments for it. |
| **Media-library REST** | Featured heroes 12646 and 6835 | Featured images read `alt_text` at render. Two PATCHes fix two post heroes plus the `/home/` cards. Confirm with public readback on those two posts. | Cheapest high-traffic win. KK approval + latin1-safe strings. |
| **Per-post / per-page REST `post_content`** | Course pages, Motleykrug, Art Island, land-back, cinematic-podcasts, flickr badge, meetup galleries | Core image blocks bake `alt=""` into HTML. Library writes no-op (proof: 2596). | Apply August batch 1 (35 strings, 7 pages) first. Then gallery posts one at a time. |
| **Do not media-batch the archive** | ~1,000 remaining in-content empties from the August crawl | A library script will report success and change almost nothing. | Keep #4 open as the parent; spawn apply issues per batch, not another inventory. |

`/home/` still returns 200 and is not linked from `/`. KK still owes the 2026-08-02 question: redirect/unpublish vs fix. If it redirects, skip its two cards and only fix 12646/6835 as post heroes.

---

## Out of scope

- **Meta Pixel / tracking beacons** as content alt. Decorative `alt=""` or removal, not a description.
- **SVG icons** in theme chrome (none sampled as content `<img>` gaps).
- **OG / Twitter image alt** (`og:image:alt`). Different surface; noted in the July 26 inventory, belongs with SEO/theme, not this `<img alt>` issue.
- **Wordmark `alt="Kris Krug home"`** redundancy with the link `aria-label`. Already named; #294 closed.
- **Featured-image crops / aspect** (`featured-image-audit-2026-08-10.md`). Different ticket.
- **Keep the Machine Strange `DRYRUN/` placeholder srcs.** Those images already have alt. Broken-src is not #4.
- **WCAG images-of-text** on course testimonial PNGs. Issue **#46**, not a reason to skip alt.
- **Inventing alt for the 38 unseen meetup-gallery frames**, photoblog Flickr-ID alts, or the 1,070 archive rows from August that this pass did not re-fetch.
- **Live writes of any kind.** This report does not apply.

---

## How to re-run

```bash
python3 scripts/public_image_audit.py \
  --urls "/, /about/, /work/, /speaking/, /photography/, /2026/08/11/futureproof-festival-announcement/" \
  --timeout 20 --format markdown
```

Known-dirty confirmation:

```bash
python3 scripts/public_image_audit.py \
  --urls "/home/, /ai-upgrade-for-creative-professionals/, /motleykrug-podcast/, /art-island-perspectives-from-a-creative-community/, /2024/09/01/august-vancouver-ai-community-meetup-recap-hackers-hustlers-heretics/" \
  --timeout 25 --format markdown
```

Public REST check (no auth): `GET /wp-json/wp/v2/media/<id>?_fields=id,alt_text,source_url,title`.

Full 216-route recount remains `python3 content/drafts/alt-text-backfill-2026-08-02/recount_live.py` (read-only, long).

---

## Recommended next step

KK approves **two library PATCHes** (12646, 6835) plus **August batch 1 `post_content` applies** (7 pages, strings already written). Relabel #4 from "write alt for all images" to "apply remaining batches; front door is done." Do not spawn another inventory agent.
