# VERIFY: Futureproof Festival announcement polish v2

**Package:** `content/drafts/2026-07-26-futureproof-festival-announcement/`
**Slug:** `futureproof-festival-announcement`
**Target:** existing WordPress post; guarded content sync was draft-only
**Refreshed:** 2026-08-12

## Result

The deeper article, revised visual sequence, video, source-page screenshots, and SEO fields are live on WordPress post `12732`. The guarded sync left the post as a private draft; a later WordPress action outside that script changed it to `publish`. Production was re-audited after that state change.

| Field | Current public readback |
|---|---|
| WordPress post ID | `12732` |
| Status | `publish` |
| Published | `true` |
| Slug | `futureproof-festival-announcement` |
| Authoring title (exact guarded write) | **Futureproof Festival of AI: A Bat Signal from Vancouver** |
| Rendered title treatment | H1 **Futureproof Festival of AI** plus front-end-rendered subtitle **A Bat Signal from Vancouver** |
| SEO title | **Futureproof Festival of AI in Vancouver \| Kris Krüg** |
| Featured media | `12739` |
| Canonical URL | `https://kriskrug.co/2026/08/11/futureproof-festival-announcement/` |
| Edit URL | `https://kriskrug.co/wp-admin/post.php?post=12732&action=edit` |

## Editorial and SEO checks

- Raw Markdown body token count: **1,964** (the verifier's deterministic package-size metric; live visible-text counts are lower because URLs and image markup are excluded by WordPress).
- Editorial destinations: **25 unique URLs**, all returned HTTP 200 on 2026-08-12.
- Internal KrisKrug.co links: **5**.
- Body media: **9 images** and **1 YouTube embed**.
- The full Vancouver AI Meetup #31 recording is embedded; the Futureproof segment is linked at **19:04**.
- Meta description: **146 characters**.
- `post.md` and `post.html` contain no em dashes, private filesystem paths, stale venue domain, disputed attendance totals, unresolved editorial markers, or the old TEDx location error. Canonical `post.html` intentionally retains local `images/...` plus `wp-image-TBD` tokens for the guarded publisher to rewrite; the production/readback body contains neither.
- `voicecheck.py --json` returned **0 findings** across `post.md` and `post.html`.
- Manual voice review passed; see `voice-audit-v2/`.

The article now distinguishes True North Media House from W2, identifies TEDxSummit as Doha, Qatar, and describes only program formats supported by the current festival pages.

## Visual sequence and rights

| Use | File | WordPress media ID | Source / approval |
|---|---|---:|---|
| Lead story photograph | `vanai-meetup31-stage-kris-futureproof-slide.webp` | 12725 | Michael Caswell; edited by Kris Krüg |
| Community proof | `vanai-meetup31-community-group-photo.webp` | 12733 | Michael Caswell |
| True North source receipt | `receipt-true-north-media-house.png` | 12734 | Editorial screenshot with source link |
| TEDx source receipt | `receipt-tedx-summit-kris-krug.png` | 12735 | Editorial screenshot with source link |
| DENT source receipt | `receipt-dent-kris-krug.png` | 12736 | Editorial screenshot with source link |
| Space Centre courtyard | `vanai-space-centre-courtyard-community.webp` | 12737 | Michelle Diamond; approved public promotional reuse |
| Space Centre at night | `space-centre-community-night.webp` | 12738 | Michelle Diamond; approved public promotional reuse |
| Honest-conversation poster | `futureproof-honest-conversation-poster.png` | 12727 | Futureproof brand-audit H02 approved |
| Featured and closing key art | `futureproof-salmon-starfield-share-20260711.jpg` | 12739 | Futureproof brand-audit L04 approved |

The previously selected May hero was rejected in the Futureproof brand audit and is no longer used. The three source screenshots render as standalone full-width figures rather than an unreadable three-column gallery. The old audience image carrying an expired promotion is no longer used.

## Guarded WordPress sync receipt

The sync command defaults to an authenticated dry run. `--apply` wrote only these fields:

```text
title
content
excerpt
featured_media
meta
```

Before any mutation it wrote a mode-600, gitignored REST snapshot:

`wp-snapshots/rest-post-12732-before-polish-v2-20260812T224659154754Z.json.tmp`

Readback hashes:

```text
before body: 97d0c9042b5763f0917330b78845798f79327107c08c4c97799809ec39d1a4f7
after body:  d8f8421b824754d64f021dde1da2c7ca9ddfa4a573695f937f90a6343f19cdf6
```

The guarded readback confirmed all payload fields exactly and preserved:

```text
status: draft
slug: futureproof-festival-announcement
categories: [1662]
tags: [1628, 1801, 542, 1719, 1800, 1495]
author: 1
date: 2026-08-11T12:00:00
date_gmt: 2026-08-11T20:00:00
```

The rendered WordPress body contains all nine media IDs, one iframe, responsive `srcset`/`sizes`, lazy loading, and lightbox triggers. It contains no local paths or placeholder media markers.

## State transition and public smoke checks

Immediately after the guarded sync, the exact readback remained `draft` and public exposure was closed:

```text
/?p=12732                                      -> 404
/futureproof-festival-announcement/            -> 404
/wp-json/wp/v2/posts/12732                      -> 401
public REST slug search                         -> []
```

The live state changed later. Public REST now reports `status=publish` and `featured_media=12739`. A final snapshot-first, content-only review fix replaced the poster alt and unsupported sponsor wording; exact readback preserved every protected field and advanced `modified_gmt` to `2026-08-12T23:22:22`. Current public checks:

```text
canonical dated URL                             -> 200
/futureproof-festival-announcement/             -> 301, then canonical 200
/wp-json/wp/v2/posts/12732                      -> 200, status=publish
public REST slug search                         -> one matching published post
```

The production page was checked at desktop and mobile widths:

- desktop viewport: **1440 × 1000**, no horizontal overflow;
- mobile viewport: **390 × 844**, no horizontal overflow;
- featured image responsive at both widths;
- all nine body images loaded at natural width;
- source screenshots are readable at full article width;
- YouTube iframe and all nine lightboxes are present;
- title, subtitle, excerpt, August 11 date, author, reading time, captions, and visual sequence render coherently;
- canonical URL, SEO title, 146-character meta description, approved Open Graph image, and `BlogPosting` structured data are present.
- poster alt now says **gathered in a circle**, and the sponsor CTA describes only the packages shown on the linked page.

## Test receipt

```text
verify_futureproof_polish_v2.py                 pass
external URL checks                             25/25 HTTP 200
voicecheck.py                                   0 findings
targeted sync/verifier tests                    13 passed
ruff                                            pass
py_compile                                      pass
make test publisher suite                       343 passed
make test SEO inventory suite                   12 passed
make test SEO backfill/link-safety suite         68 passed
plugin and theme smoke checks                   pass
```

Final content-only production fix receipt:

```text
snapshot: rest-post-12732-before-two-review-fixes-20260812T232221806662Z.json (local, mode 600)
before body: 68df6fb645b95e7d9414e27ebf9ac3d3bf61cfd2dd34fa9454f494a24f479d82
after body:  addd40d6c0a3df6655c56f2f6d8828809a5c02061d90fab6c42ada98b9ee5f96
payload: content only
protected fields changed: none
```

## Remaining follow-ups

1. Confirm Michael Caswell's cross-site reuse/credit line for the two Meetup photographs. The current captions credit him on-page.
2. Recheck or remove the August 15 ticket and call-for-talks deadline after it passes.
3. Keep the local mode-600 snapshot until the public page and repository closeout are accepted.

This is a WordPress publication path, not a Vercel deployment. No Vercel project update is required for this post.
