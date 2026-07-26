# Asset Manifest — Futureproof Festival announcement (#497)

Wave 1 / FP-1. Design assets only. No post body, no WP API calls.

Staged under `images/` from public production URLs on [futureproof.website](https://www.futureproof.website/). Festival-repo local paths (`~/Code/futureproof-festival/public/...`) were not available in this cloud VM; public equivalents of those production files were used instead. Binaries copied as-is (no open/edit).

**Slug:** `2026-07-26-futureproof-festival-announcement`

## Roles at a glance

| File | Role | Hero/featured? |
|---|---|---|
| `images/futureproof-honest-conversation-poster.png` | **hero** | **Yes — designated featured** |
| `images/futureproof-wordmark-white-transparent.png` | wordmark | No |
| `images/manifesto-01-future-cultural-question.webp` | gallery-1 | No |
| `images/manifesto-06-who-shapes-us.webp` | gallery-2 | No |
| `images/manifesto-14-places-to-think.webp` | gallery-3 | No |
| `images/futureproof-salmon-starfield-share-20260527.jpg` | gallery-4 (launch key art / OG landscape alternate) | No — optional featured swap if portrait crop fights WP card |

## Assets

### 1. Hero / featured

- **File:** `images/futureproof-honest-conversation-poster.png`
- **Role:** `hero` (designated featured / `featured_media_id` candidate)
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

## Acceptance checklist (#497)

- [x] `images/` contains 4–6 files (6), each with a real alt string in this manifest
- [x] One file explicitly designated hero/featured (`futureproof-honest-conversation-poster.png`)
- [x] Filenames web-safe; no absolute `/Users/` paths in tracked files
- [x] No binaries opened/edited; assets copied as-is from public URLs
- [x] Binaries obtained from public site (KK drop not required for the core set)
