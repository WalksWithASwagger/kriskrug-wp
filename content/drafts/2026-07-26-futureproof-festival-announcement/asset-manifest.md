# Asset Manifest — Futureproof Festival announcement (#497)

Wave 1 / FP-1. Design assets only. No post body, no WP API calls.

Staged under `images/` from public production URLs on [futureproof.website](https://www.futureproof.website/). Festival-repo local paths (`~/Code/futureproof-festival/public/...`) were not available in this cloud VM; public equivalents of those production files were used instead. Binaries copied as-is (no open/edit).

**Slug:** `2026-07-26-futureproof-festival-announcement`

## #644 update (2026-08-02) — Meetup #31 stage photo is now the preferred lead

The July 2026 Vancouver AI meetup gave us current, real-room proof: Kris on stage in front of the Futureproof art, mid-talk, in a packed room. That image is now the **preferred lead/hero candidate**, ahead of the July 26 poster. See [Preferred lead candidate](#preferred-lead-candidate-644) below for full sourcing. The six July 26 assets are preserved unchanged and re-roled as supporting visuals. Since the first #644 pass, the two Meetup #31 photos have also been staged as local WebP copies under `images/` (md5-identical to their R2 sources — see below), so they now sit at the same readiness as the July 26 poster set: local repo files for review, **not** WordPress media. Nothing in this file is an uploaded media id; every entry is still a public URL and/or a local file pending an actual media-library upload. Do not treat any `wp-image-TBD` class in `post.html` as resolved.

## Roles at a glance

| File | Role | Hero/featured? |
|---|---|---|
| **Meetup #31 stage photo** (`images/vanai-meetup31-stage-kris-futureproof-slide.webp`, staged local copy of the R2 source) | **lead / hero** | **Yes — preferred lead per #644, supersedes the poster below** |
| `images/futureproof-honest-conversation-poster.png` | official-graphic (was hero) | No longer preferred hero; strong backup / OG alternate |
| **Meetup #31 audience photo** (`images/vanai-meetup31-audience-wide-shot.webp`, staged local copy of the R2 source) | community-room supporting visual | No |
| `images/futureproof-wordmark-white-transparent.png` | wordmark | No |
| `images/manifesto-01-future-cultural-question.webp` | gallery-1 | No |
| `images/manifesto-06-who-shapes-us.webp` | gallery-2 | No |
| `images/manifesto-14-places-to-think.webp` | gallery-3 | No |
| `images/futureproof-salmon-starfield-share-20260527.jpg` | gallery-4 (launch key art / OG landscape alternate) | No — optional featured swap if portrait crop fights WP card |
| Historical conference photograph | supporting visual, **unresolved** | See flag below — no specific frame short-listed this pass |

## Public-asset HTTP verification (#644, re-checked 2026-08-02)

Every public URL in this manifest was re-fetched at review time with:
`curl -sIL --max-time 25 -o /dev/null -w "%{http_code} %{content_type}" "<url>"`

| Asset | URL | HTTP | Content-Type |
|---|---|---|---|
| Meetup #31 stage (lead) | `pub-163cd0d1569e46f48b869a9070f97d71.r2.dev/events/vancouver-ai-meetup-2026-07/large/b4717426bf89.webp` | 200 | image/webp |
| Meetup #31 audience | `pub-163cd0d1569e46f48b869a9070f97d71.r2.dev/events/vancouver-ai-meetup-2026-07/large/639c78efe5d2.webp` | 200 | image/webp |
| honest-conversation poster | `www.futureproof.website/graphics/honest-conversation/futureproof-honest-conversation-poster.png` | 200 | image/png |
| wordmark | `www.futureproof.website/brand/futureproof/futureproof-wordmark-white-transparent.png` | 200 | image/png |
| manifesto-01 | `www.futureproof.website/graphics/manifesto/manifesto-01-future-cultural-question.webp` | 200 | image/webp |
| manifesto-06 | `www.futureproof.website/graphics/manifesto/manifesto-06-who-shapes-us.webp` | 200 | image/webp |
| manifesto-14 | `www.futureproof.website/graphics/manifesto/manifesto-14-places-to-think.webp` | 200 | image/webp |
| salmon-starfield key art | `www.futureproof.website/media/launch/futureproof-salmon-starfield-share-20260527.jpg` | 200 | image/jpeg |

All eight returned HTTP 200. These are public-source availability checks only — nothing here is an uploaded WordPress media id, and a 200 on a public URL is not a rights clearance (see per-asset rights status below).

## Preferred lead candidate (#644)

### Meetup #31 stage photo — Kris presenting the Futureproof slide

- **Public derivative URL:** `https://pub-163cd0d1569e46f48b869a9070f97d71.r2.dev/events/vancouver-ai-meetup-2026-07/large/b4717426bf89.webp` — confirmed live, HTTP 200, `image/webp`, re-checked 2026-08-02 (see verification table above).
- **Staged local copy (in THIS repo):** `images/vanai-meetup31-stage-kris-futureproof-slide.webp` — 2400×1600 WebP, md5 `b7bbd2c264f77e179de5168b25ee16ab`, byte-identical to the R2 source (verified 2026-08-02). This is a local repo file for review only, **not** a WordPress media upload.
- **Upstream local derivative (not this repo):** `~/Code/bcai-website/.local-clone/photo-galleries/vancouver-ai-meetup-2026-07/derivatives/b4717426bf89-large.webp` (same 2400×1600 WebP, same md5; `derivatives/` is gitignored in that repo and regenerable from `manifest.json`). Checked `/Users/kk/Code/BC-AI-MAC/` per the #644 brief — that checkout does **not** carry this gallery, so bcai-website is the actual upstream, and the R2 URL remains the canonical public source.
- **Source-of-truth metadata** (`manifest.json` in the bcai-website photo-gallery pipeline, event slug `vancouver-ai-meetup-2026-07`, event title "Vancouver AI Meetup #31 — July 2026", event date 2026-07-29):
  - `"photographer": "Michael Caswell"` on this specific frame (sha `b4717426bf89...`). The gallery's two credited photographers for the whole event are Michael Caswell (211 frames) and Tristan Brand (168 frames), confirmed by re-reading `manifest.json` on 2026-08-02; this frame's per-photo credit is Caswell alone.
  - Source caption: *"Kris presents a Futureproof slide: 'Vancouver — WE NEED TO TALK ABOUT AI,' with salmon and city artwork."*
- **Owner/credit:** Photography **Michael Caswell**; editing **Kris Krüg** (per #644's issue text — not independently present in the pipeline's metadata, which tracks source photographer only, so the editing credit is carried forward from the issue as given).
- **Rights/approval status: unresolved hotlink.** This is BC + AI's own event photography, publicly hosted on BC + AI's R2 CDN for the `bc-ai.ca` event-page gallery. It is not yet uploaded to kriskrug.co's WordPress media library, and there is no written cross-site reuse release in this repo or the bcai-website repo — only the fact that BC + AI (Kris's own nonprofit) commissioned it and it is already public. Treat as **candidate, not upload-ready**, same as every other image in this manifest, until Kris signs off on reuse and it goes through an actual media upload.
- **Visual confirmation:** Viewed directly (2026-08-02) — matches the caption exactly. Kris on stage, mic in hand, BC+AI-branded jacket, in front of the full-bleed "VANCOUVER WE NEED TO TALK ABOUT AI" Futureproof artwork (salmon, ravens, aurora, city skyline).
- **Proposed article role:** lead/opening image, ahead of the July 26 poster. This is the "current, real room" proof the #645 editorial spine opens on.
- **Crop guidance:** Source is 2400×1600 (3:2 landscape). Full frame works for a WP `size-large` block. For a tighter card/OG crop, center on Kris and the "WE NEED TO TALK ABOUT AI" line; avoid cropping so tight that the salmon/raven artwork disappears, since that's the visual echo of the Futureproof key art used elsewhere in this manifest.
- **Alt text (draft, for `alt-text.md`):** "Kris Krüg speaks on stage at Vancouver AI Meetup #31, in front of a Futureproof slide reading 'Vancouver — we need to talk about AI,' with salmon and skyline artwork behind him. Photo: Michael Caswell."

## Supporting visuals curated for #644

### Community-room photo — audience facing the stage

- **Public derivative URL:** `https://pub-163cd0d1569e46f48b869a9070f97d71.r2.dev/events/vancouver-ai-meetup-2026-07/large/639c78efe5d2.webp` — confirmed live, HTTP 200, `image/webp`, re-checked 2026-08-02 (see verification table above).
- **Staged local copy (in THIS repo):** `images/vanai-meetup31-audience-wide-shot.webp` — 2400×1600 WebP, md5 `b4d162b8d689001d010033b4aae5e7bd`, byte-identical to the R2 source (verified 2026-08-02); a local repo file for review only, **not** a WordPress media upload.
- **Upstream local derivative (not this repo):** same pipeline, `~/Code/bcai-website/.local-clone/photo-galleries/vancouver-ai-meetup-2026-07/derivatives/639c78efe5d2-large.webp` (2400×1600 WebP, same md5).
- **Owner/credit:** Photography Michael Caswell, Vancouver AI Meetup #31, 2026-07-29.
- **Source caption:** *"A wide shot from the back of the room — silhouetted audience facing the lit stage and screen."*
- **Rights/approval status:** Unresolved hotlink, same status as the lead candidate above — public on BC + AI's R2 CDN, not yet a WP media upload, no independent cross-site release on file.
- **Proposed article role:** the "the room already exists" supporting shot — pairs with the lead to show both the speaker and the audience that's already showing up, ahead of any mention of the Space Centre or the festival stage.
- **Crop guidance:** Full frame reads well; it's a wide establishing shot, so don't crop into a tight square or it loses the "packed room" read.
- **Alt text (draft):** "A wide shot from the back of the room: a full, silhouetted audience faces the lit Futureproof stage and screen during Vancouver AI Meetup #31."

### Official festival graphic — carried forward from the July 26 set

The strongest already-vetted official campaign art remains `images/futureproof-honest-conversation-poster.png` (see full entry below, re-roled from hero to official-graphic support). It is hand-painted campaign art sourced directly from futureproof.website's own public asset paths, so rights/provenance are as clear as any asset in this package. No new official graphic was substituted in this pass — the July 26 selection holds up.

### Historical conference photograph — flagged, unresolved

#643's network-receipts ledger (`network-receipts.md`) identifies strong candidate pools for a historical Kris-as-photographer image: the [DENT 2014-2018 collection](https://www.flickr.com/photos/kk/collections/72157691620626391/) or the [Vancouver 2010 Olympics / True North Media House collection](https://www.flickr.com/photos/kk/collections/72157623159875205/). Provenance on *ownership* is about as clean as it gets — Kris is the photographer and copyright holder of his own Flickr uploads — but no single frame was short-listed in this curation pass; picking "the" representative image from either collection is an editorial/archive-review call better made by Kris directly (or in a follow-up pass with more time against a specific narrative beat in the finished #645 draft).

**Recommendation:** leave this slot open for #645. If the writer wants a historical beat, the safest path is a direct pull from Kris's own two named collections above rather than a single unreviewed frame picked here. If no time exists before review, the safer substitute is to skip the historical photo entirely — the lead, community-room, and official-graphic assets already carry the "this is real" argument without it.

## Assets (July 26 set, preserved unchanged)

### 1. Official graphic (was hero; see #644 update above for the new preferred lead)

- **File:** `images/futureproof-honest-conversation-poster.png`
- **Role:** `official-graphic` — strong backup/OG alternate; no longer the preferred lead as of #644 (see above)
- **Source URL:** `https://www.futureproof.website/graphics/honest-conversation/futureproof-honest-conversation-poster.png`
- **Festival-repo equivalent (for KK drop if re-export needed):** `public/graphics/honest-conversation/futureproof-honest-conversation-poster.png`
- **Format:** PNG 1200×1800 (portrait)
- **Alt:** Futureproof Festival poster: silhouetted figures walk toward a golden-lit portal between ornate arched windows marked with fish, trees, and eyes; teal and orange energy lines rise to a centered eye. White type reads "The most honest AI conversation happening anywhere this year." Teal line below: Vancouver · Oct 28-30, 2026 · Up to 600 people. BC+AI Ecosystem mark at lower left.

### 2. Wordmark

- **File:** `images/futureproof-wordmark-white-transparent.png`
- **Role:** `wordmark`
- **Source URL:** `https://www.futureproof.website/brand/futureproof/futureproof-wordmark-white-transparent.png`
- **Festival-repo equivalent:** `public/brand/futureproof/futureproof-wordmark-white-transparent.png`
- **Format:** PNG 2048×512 RGBA (white dotted letterforms on transparent; reads on kriskrug.co dark surfaces)
- **Alt:** FUTUREPROOF wordmark in white dotted grid letterforms on a transparent background.

### 3. Gallery-1

- **File:** `images/manifesto-01-future-cultural-question.webp`
- **Role:** `gallery-1`
- **Source URL:** `https://www.futureproof.website/graphics/manifesto/manifesto-01-future-cultural-question.webp`
- **Festival-repo equivalent:** `public/graphics/manifesto/manifesto-01-future-cultural-question.webp`
- **Format:** WebP 1200×1200
- **Alt:** Hand-painted Futureproof Festival poster reading "The Future Is a Cultural Question." over an aurora above a forested shoreline with salmon and painted eyes along the water.

### 4. Gallery-2

- **File:** `images/manifesto-06-who-shapes-us.webp`
- **Role:** `gallery-2`
- **Source URL:** `https://www.futureproof.website/graphics/manifesto/manifesto-06-who-shapes-us.webp`
- **Festival-repo equivalent:** `public/graphics/manifesto/manifesto-06-who-shapes-us.webp`
- **Format:** WebP 1200×1200
- **Alt:** Hand-painted Futureproof Festival poster reading "Who Gets to Shape What Shapes Us?" over rivers running through open hands.

### 5. Gallery-3

- **File:** `images/manifesto-14-places-to-think.webp`
- **Role:** `gallery-3`
- **Source URL:** `https://www.futureproof.website/graphics/manifesto/manifesto-14-places-to-think.webp`
- **Festival-repo equivalent:** `public/graphics/manifesto/manifesto-14-places-to-think.webp`
- **Format:** WebP 1200×1200
- **Alt:** Hand-painted Futureproof Festival poster reading "The Future Needs Places to Think." over a quiet tidepool reflecting stars.

### 6. Gallery-4 (launch key art / landscape alternate)

- **File:** `images/futureproof-salmon-starfield-share-20260527.jpg`
- **Role:** `gallery-4`
- **Source URL:** `https://www.futureproof.website/media/launch/futureproof-salmon-starfield-share-20260527.jpg`
- **Festival-repo equivalent:** `public/media/launch/futureproof-salmon-starfield-share-20260527.jpg`
- **Also live on kriskrug.co homepage** as Futureproof pillar art.
- **Format:** JPEG 1200×630 (OG / featured-landscape friendly)
- **Alt:** Futureproof Festival launch key art: a school of coral salmon marked with geometric and ink patterns swims toward a bright portal under green-yellow aurora and stars; black ravens carry glowing crystals; painted eyes float in dark water. Title type "FUTUREPROOF FESTIVAL," dates October 28-30, 2026, presented by BC+AI.

## KK NOTES (optional festival-repo drops)

Public site already supplied the honest-conversation poster, wordmark, and manifesto gallery set. No binaries are missing for acceptance.

If KK prefers named aurora / surrealist / dreamscape files from the festival repo exploration library instead of (or in addition to) the manifesto posters, drop them here and extend this manifest:

| Suggested local filename | Role | Preferred source (relative to festival repo `public/`) | Draft alt |
|---|---|---|---|
| `futureproof-aurora-poster.png` | gallery-alt-aurora | `graphics/` or `media/gallery/` aurora poster (exact basename TBD by KK) | Hand-painted Futureproof Festival aurora poster: curtains of northern light over a Pacific Northwest night landscape, festival title locked up in the safe type zone. |
| `futureproof-surrealist-poster.png` | gallery-alt-surrealist | `graphics/` or `media/gallery/` surrealist poster | Hand-painted Futureproof Festival surrealist poster: dream-logic figures and symbols arranged around the festival mark, no hype tagline readable in frame. |
| `futureproof-dreamscape-poster.png` | gallery-alt-dreamscape | `graphics/` or `media/gallery/` dreamscape poster | Hand-painted Futureproof Festival dreamscape poster: soft night sky and reflective water holding the festival title and date lockup. |

Do not write absolute `/Users/` paths into this package. Use `public/...` relative to the festival repo, or the public `https://www.futureproof.website/...` URLs above.

## Recommended visual sequence (#644)

**Desktop / linear read:**

1. Meetup #31 stage photo (lead) — Kris on stage, current room, opens the article.
2. Meetup #31 audience photo — the room from the crowd's side, right after the opening beats land.
3. `futureproof-honest-conversation-poster.png` — the official campaign art, where the piece turns from "here's proof" to "here's the festival."
4. Manifesto gallery-1 through gallery-3 (`manifesto-01`, `manifesto-06`, `manifesto-14`) — unchanged from the July 26 set, placed with the manifesto section of the copy.
5. `futureproof-salmon-starfield-share-20260527.jpg` — closing/share art, doubles as the OG image if the poster's portrait crop fights the WP card.

**Mobile:** same order; the two new meetup photos and the poster are all landscape-friendly at full width, so no separate mobile crop is required for those three. The manifesto set is already square (1200×1200) and unaffected.

Historical photograph: not included in either sequence pending the flag above.

## Acceptance checklist (#644)

- [x] Meetup stage image added as preferred lead candidate, Michael Caswell photography credit + Kris Krüg editing credit preserved
- [x] Public derivative confirmed live (HTTP 200) and source metadata cross-checked against the bcai-website pipeline's `manifest.json`
- [x] 3-5 supporting visuals curated: community-room photo (new), official festival graphic (carried forward), historical photo (flagged, deferred rather than force-picked)
- [x] Every candidate recorded with source URL, local source, owner/credit, rights status, proposed role, crop guidance, alt text
- [x] Two meetup photos now staged as local WebP copies under `images/` (md5-identical to the R2 source, verified 2026-08-02); still marked NOT WordPress media, and `wp-image-TBD` classes remain unresolved. All 8 public URLs curl-verified HTTP 200 on 2026-08-02 (see verification table)
- [x] No new campaign art generated; no source photographs edited or overwritten
- [x] Recommended desktop/mobile visual sequence produced

## Acceptance checklist (#497, original)

- [x] `images/` contains 4–6 files (6), each with a real alt string in this manifest
- [x] One file explicitly designated hero/featured (`futureproof-honest-conversation-poster.png`) — superseded by the #644 lead candidate above
- [x] Filenames web-safe; no absolute `/Users/` paths in tracked files
- [x] No binaries opened/edited; assets copied as-is from public URLs
- [x] Binaries obtained from public site (KK drop not required for the core set)
