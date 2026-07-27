# Alt-text inventory — Issue #4 (2026-07-26)

**Mode:** agent-safe inventory + remediation plan only.  
**Writes:** none (no live WP media PATCH; `WP_USER` unset in this session).  
**Branch:** `cursor/4-alt-text-inventory-f196`  
**Tooling:** `python3 scripts/public_image_audit.py` (`make public-image-audit`), public REST media readbacks, theme source scan.

## Verdict

High-visibility Aurora surfaces (`/`, `/about/`, `/speaking/`, `/generative-ai-services/`) are in good shape for **content** `<img>` alt. The clear live content gap on the requested page set is **media `6835`** (`crowd-shot-vancovuer-ai.jpeg`) rendering with **empty alt on `/home/`**. June Priority-A gaps (`3960`, `7892`, `7819`, `11976`) are **already fixed** on media. Archive-wide empty-alt debt remains large (~47% empty in a 500-image public media sample) and needs a creds+KK gated PATCH batch — not this pass.

## Method

| Probe | Scope |
|---|---|
| Public HTML crawl | `/`, `/home/`, `/about/`, `/speaking/`, `/blog/`, `/generative-ai-services/` (+ `/services/` → same URL) |
| Blog samples | `/2026/07/18/i-am-nomad-ai-film/`, `/2026/07/10/the-cheer-is-a-cap-table/`, `/2026/06/24/ai-wont-fix-your-broken-permit-process/` |
| Legacy spot | `/flickr-photographr-badge/` (prior #4 evidence) |
| Theme | `theme/kk-aurora/` templates, parts, patterns — hardcoded `<img>` |
| Scripts | `scripts/public_image_audit.py` + `make public-image-audit`; execute path requires `--execute --media-alt-file` + WP creds |
| Prior art | `docs/current-state/reports/issue-4-public-image-alt-20260716.md`, `docs/current-state/ALT-TEXT-AUDIT-PACKET-2026-06-14.md` |

Classifier states from the audit script: `missing-attr`, `empty`, `decorative-empty`, `filename-style`, `ok`. Weak/title-as-alt reviewed manually on top of that.

## Aggregate (requested + samples)

### Core pages (`/`, `/home/`, `/about/`, `/speaking/`, `/blog/`, `/generative-ai-services/`)

| Metric | Count |
|---:|---:|
| Pages scanned | 6 |
| Images found | 64 |
| Missing alt attribute | 6 (all Facebook noscript `facebook.com/tr` pixels) |
| Empty non-decorative alt | 1 (`6835` crowd-shot on `/home/`) |
| Filename-style alt | 0 |
| Content images OK | 57 |

### Blog samples + flickr badge

| Metric | Count |
|---:|---:|
| Pages scanned | 4 |
| Images found | 24 |
| Missing alt attribute | 4 (FB pixels) |
| Empty non-decorative alt | 1 (`12604` on flickr badge page) |
| Recent post content/featured alts | descriptive / OK |

## Severity ranking

### S0 — Fix first (high-visibility empty content alt)

| # | Media ID | Where | Current | Proposed alt (draft) | Conf |
|---|---:|---|---|---|---|
| 1 | **6835** | `/home/` recent-post card for *Zero to One…* (same file also used as that post’s featured image; archive card falls back to **post title** as alt) | `""` | `Crowded Vancouver AI community meetup under blue and magenta lights — attendees watch a speaker in an industrial studio space.` | High (image viewed) |

**Why S0:** empty alt on a public listing surface; same attachment already leaks weak title-as-alt elsewhere when WP falls back.

### S1 — Real empty content alt, lower traffic

| # | Media ID | Where | Current | Proposed alt | Conf |
|---|---:|---|---|---|---|
| 2 | **12604** | `/flickr-photographr-badge/` | `""` | `Early Flickr Photographer badge graphic for Kris Krug (kk+) with contact lines, portrait, barcode, and handwritten KK+ signature.` | High (image viewed) |

Note: another image on that page already has good alt (`Vintage Flickr badge image…`); this empty one is a second badge asset. Related 2026-07-11 Flickr re-uploads (`12589`–`12608` sample) also show empty `alt_text` in public REST — treat as a **batch** after KK, not one-offs without review.

### S2 — Weak / thin / title-as-alt (not empty, improve when touching media)

| # | Media / surface | Current alt | Issue | Proposed polish |
|---|---|---|---|---|
| 3 | About inline `…/2023/07/krug-1.jpg` | `Portrait of Kris Krug` | Thin; little context | `Close portrait of Kris Krug looking toward camera.` (or keep if KK prefers minimal) |
| 4 | Media **11205** `/home/` + blog | `AI for Creative Professionals Kris Krug` | Keyword-y, low visual detail | Describe the photo (stage/portrait context) after visual confirm |
| 5 | `/blog/` featured cards | Often **post title** as alt | Useful for SEO fallback when media alt empty; weak for screen readers who need *what the image shows* | Prefer media-library descriptive alt; titles belong in link text / headings |
| 6 | Social meta on `/about/`, `/`, `/speaking/`, `/generative-ai-services/` | `og:image` present; **`og:image:alt` / `twitter:image:alt` absent** in HTML | SEO/social a11y gap (not `<img alt>`) | Theme/SEO lane: emit image alts from featured media `alt_text` (Aurora already sets some homepage OG alts in `functions.php` for specific routes) |

### S3 — Noise / out of media-PATCH scope

| Item | Notes |
|---|---|
| Facebook noscript tracking pixel (`missing-attr` on every page) | Not a content photo. Prefer `alt=""` + decorative markers, or stop emitting `<img>` for the pixel. Theme/snippet/plugin change — **not** a media-library PATCH. |
| Aurora hardcoded templates | All reviewed hardcoded `<img>` already have descriptive `alt` (front-page hero/grid, header wordmark, speaking-proof-grid, photo-gallery pattern placeholders). **No theme edit required for #4 content gaps.** |
| Oversized images flagged by audit | Perf debt, not alt. Separate from this issue. |

### Closed / already remediated (do not re-PATCH)

| Media ID | June packet status | 2026-07-26 readback |
|---:|---|---|
| 3960 (About featured) | was empty | Descriptive banner alt present |
| 7892, 7819 | were empty | Descriptive alts present |
| 11976 | filename-style | Descriptive protest-sign alt present |

## Theme hardcoded `<img>` scan

| File | Result |
|---|---|
| `templates/front-page.html` | 12 imgs, all descriptive alts |
| `parts/header.html` | Wordmark `alt="Kris Krug home"` |
| `parts/speaking-proof-grid.html` | Stage photo has descriptive alt |
| `patterns/photo-gallery.php` | Placeholder alts explicitly call for replacement + descriptive text |
| Other templates (`page.html`, `single.html`, …) | No hardcoded content `<img>` |

Repo/live Aurora Version readback this pass: **1.4.8**.

## Scripts already in repo

| Path | Role |
|---|---|
| `scripts/public_image_audit.py` | Read-only public HTML image audit; optional `--execute --media-alt-file` for **exact** media_id→alt writes (never auto-applies crawl findings) |
| `make public-image-audit` | Makefile wrapper (`DEFAULT_URLS=1`, `URLS=…`, `CHECK_URLS=1`, `OUTPUT=…`) |
| `scripts/tests/test_public_image_audit.py` | Classifier/unit coverage |
| `scripts/wp_post_ia_rollout.py` | Featured-image / IA dry-run (includes `missing_featured_alt`) |
| Draft `alt-text.md` packets under `content/drafts/*/` | Per-post publisher practice for **new** assets |

## Archive debt (authenticated inventory later)

Public REST sample (first 5 media pages × 100 images): **235 / 500 (47%)** with empty `alt_text`. Many are historical Flickr/archive re-uploads (2026-07-11 batch) and older Midjourney/export assets. **Do not bulk-PATCH** without:

1. Visibility ranking (linked from public pages / featured / last-N posts first)
2. KK-approved alt copy (or explicit decorative `alt=""` policy — note: current `--execute` path **rejects** empty alt strings)
3. Creds + rollback note (snapshot old alts JSON before write)
4. Dry-run `make public-image-audit` on touched URLs after apply

## Remediation plan (gated)

### Phase A — agent-safe (this deliverable)

1. Inventory report (this file).
2. Draft proposed alts for worst offenders: `content/drafts/2026-07-26-alt-text/`.
3. No live writes.

### Phase B — KK + creds (follow-up session)

1. Confirm/edit proposed alts in the draft packet.
2. Snapshot current alts for target IDs.
3. Apply with:
   ```bash
   python3 scripts/public_image_audit.py --execute --media-alt-file content/drafts/2026-07-26-alt-text/media-alt-patch.json
   ```
   (requires `WP_USER` + `WP_APP_PASSWORD`)
4. Re-run:
   ```bash
   make public-image-audit URLS="/home/,/flickr-photographr-badge/" CHECK_URLS=1 OUTPUT=docs/current-state/reports/alt-text-verify-YYYYMMDD.md
   ```
5. Optional Track B follow-up (separate commit): FB pixel decorative alt / `og:image:alt` emission — **do not mix** with media PATCH commit.

### Phase C — archive program

1. Crawl public URLs beyond the default set; join to media IDs.
2. Rank empty-alt media by inbound public use.
3. Batch 10–20 KK-approved alts per session; never “all images” in one mutate.

## Proposed PATCH payload (not applied)

See `content/drafts/2026-07-26-alt-text/media-alt-patch.json` — currently **two** S0/S1 items only.

## Drift vs 2026-07-16 public report

| Finding (2026-07-16) | 2026-07-26 |
|---|---|
| Empty crowd-shot on `/home/` | **Still open** (`6835`) |
| Empty on flickr badge page | **Still open** (`12604`); sibling badge already fixed |
| FB pixel `missing-attr` | Unchanged (noise) |
| About featured empty (June packet) | **Fixed** (`3960`) |

---

**Captured:** 2026-07-26 · public read-only · Issue #4  
**Next human gate:** approve S0/S1 alts → authorize media PATCH with creds.
