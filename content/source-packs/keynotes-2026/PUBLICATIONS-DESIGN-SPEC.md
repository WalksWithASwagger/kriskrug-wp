# Publications design spec

Status: **Phase 1 foundation** (2026-08-01). Machine-checked via
`assets/press-media-manifest.json` and `scripts/tests/test_publications_editorial_payload.py`.

This spec codifies the Publications tear-sheet image and layout system so the page
cannot drift back to full-page screenshot crops, mismatched ratios, or the superseded
dark-neon ghost skin.

## Image tiers

| Tier | Name | Use | Required when |
|------|------|-----|---------------|
| **1** | Designed / owned art | YouTube/Vimeo thumbnails, podcast cover art, KK-owned photographs, magazine cover scans | Any slot under 300px wide, or when source publishes designed artwork |
| **2** | Standardized article clip | Masthead + headline region only, captured at exact output size | Feature cards, wall tiles, feed thumbs for article pages |
| **3** | Text-only | No image | No Tier 1 or Tier 2 art exists; never use a bad crop as filler |

**Rule:** CSS must never invent a crop. Files are produced at the slot ratio at capture time.

## Slot taxonomy

| Slot | Ratio | Output (px) | Min tier | Payload context |
|------|-------|-------------|----------|-----------------|
| `feature-lead` | 16:10 | 1200 × 750 | 2 | Right now — lead card |
| `feature` | 16:10 | 1200 × 750 | 2 | Right now — secondary cards |
| `wall` | 16:10 | 1200 × 750 | 1 or 2 | The wall — curated visual grid |
| `feed-thumb-clip` | 16:10 | 1200 × 750 | 2 | Recent run — article clip thumb (≥ 200px rendered) |
| `feed-thumb-video` | 16:9 | 1280 × 720 | 1 | Recent run — broadcast / YouTube thumb |
| `podcast` | 1:1 | 600 × 600 | 1 | Heard on — podcast cover shelf |
| `in-print` | varies | per entry | 1 | In print — KK-owned photo or cover scan |

Slots under 300px rendered width **must** use Tier 1 art. Tier 2 clips are forbidden in
stamp-sized slots (legacy 4-up board, ~88px feed thumbs).

## Capture methods

| Method | Tier | Output | Tooling |
|--------|------|--------|---------|
| `article_clip` | 2 | 1200 × 750 JPEG | Playwright, 1440 viewport, h1-anchored masthead+headline clip; hide sticky/ad/consent |
| `youtube_thumbnail` | 1 | 1280 × 720 JPEG | YouTube `maxresdefault` → `hqdefault` fallback |
| `vimeo_thumbnail` | 1 | per oEmbed | Vimeo oEmbed `thumbnail_url` |
| `itunes_artwork` | 1 | 600 × 600 JPEG | iTunes Lookup API from Apple Podcasts show ID |
| `owned_photo` | 1 | per manifest | KK-owned file from kk-kb media-credits (Phase 2+) |

### Article clip rules (`article_clip`)

1. Viewport: **1440 × 900** (minimum height for scroll room).
2. Before capture, inject CSS to hide: cookie/consent banners, fixed/sticky headers and
   footers, ad iframes and `[class*="ad"]` containers, chat widgets.
3. Scroll the primary article `h1` into the upper third of the viewport.
4. Clip region: **1440 × 900** (16:10 at viewport width), top-aligned after scroll settle.
5. Resize to **1200 × 750** JPEG, quality 88.
6. Never capture below the fold as a substitute for a headline clip.

## Naming convention

```
press-YYYY-MM-DD-<slug>[-context|-thumb|-cover].jpg
```

- Date matches the publication / air / list date on the tear sheet.
- Slug: lowercase, hyphenated outlet or topic fragment.
- Recaptured assets append **`-v2`** before `.jpg` to dodge CDN cache on deploy.
- Manifest `key` is always the **target** filename (including `-v2` when recapture is pending).

Examples:

- `press-2026-07-31-biv-ecosystem-context-v2.jpg` (Tier 2 clip)
- `press-2026-05-20-storyhive-v2.jpg` (Tier 1 YouTube thumb)
- `press-2025-01-31-rachel-thexton-cover-v2.jpg` (Tier 1 podcast)

## Credit fields (manifest + payload)

Every manifest entry includes:

| Field | Required | Notes |
|-------|----------|-------|
| `outlet` | yes | Display name |
| `credit` | yes | Attribution line for payload `.kk-press-credit` or figcaption |
| `source_url` | yes | Canonical public URL |
| `published_date` | yes | ISO `YYYY-MM-DD` |

Article clips: credit must name the outlet and any visible third-party photographer
(e.g. `Coverage screenshot: BIV. Article photo: Rob Kruyt / BIV.`).

## Payload `<img>` contract

Every press image in `wp-payloads/publications.html`:

```html
<img
  src="../assets/press-YYYY-MM-DD-slug-v2.jpg"
  data-media-key="press-YYYY-MM-DD-slug-v2.jpg"
  alt="…"
  width="1200"
  height="750"
  loading="lazy"
/>
```

- `width` / `height` must match manifest `width` / `height` exactly (layout reservation).
- `data-media-key` must equal the manifest `key` and basename of `src`.
- Ratio implied by width:height must match the entry's `slot` ratio.

## Forbidden markers (regression guard)

The superseded July 2026 dark-neon draft skin must never return:

- class `kk-publications`
- colors `#00e5ff`, `#ff6a6a`
- token `--press-night`

## Contact-sheet review gate

Before any media upload or live PATCH:

1. Run `python3 scripts/capture_press_media.py` (or `--only <key>` for partial runs).
2. Open `content/source-packs/keynotes-2026/assets/contact-sheet.html` locally.
3. KK approves every crop, thumb, and credit line on the sheet.
4. Only then: dry-run → apply via `scripts/deploy_publications_tearsheet.py`.

The contact sheet lists: thumbnail, target key, tier, slot, outlet, credit, source link,
capture method, and file status (`pending_recapture` | `captured` | `approved`).

## Manifest location

`content/source-packs/keynotes-2026/assets/press-media-manifest.json`

Extended tests in `scripts/tests/test_publications_editorial_payload.py` fail CI when:

- a payload `<img>` lacks a manifest entry
- `width` / `height` attrs disagree with manifest slot dimensions
- naming breaks `press-YYYY-MM-DD-*`
- forbidden neon ghost markers reappear

## Related docs

- `assets/publications-press-media.md` — human checklist (superseded for ratios by this spec)
- `verification/PUBLICATIONS-KB-GAP-REPORT-2026-08-01.md` — coverage research
- `scripts/capture_press_media.py` — manifest-driven capture tool
- `scripts/deploy_publications_tearsheet.py` — gated deploy helper
