# Issue Workdown Deploy Readback — 2026-06-18

## Scope

Deployment/readback closure lane for #9, #36, #43, and #45, plus image-audit narrowing evidence for #4/#40.

No plugin deploys, bulk media mutation, private inbox reads, or WordPress title writes were performed.

## Baseline

- `make status-readonly` passed before live writes.
- `make test` passed after local changes.
- `make docs-truth-check` passed before live deploy work.
- `make seo-audit` reported `Missing meta description: 0`.
- `make jetpack-feedback-audit FORMAT=json` ran PII-safe metadata-only checks:
  - Jetpack forms available.
  - Feedback inbox count: `547`.
  - Spam count: `104`.
  - `/contact/` page ID `2418` contains one Jetpack contact form.
  - No message bodies, names, emails, attachments, or CSV exports were requested.

## Live Writes

### Jetpack SEO setting

Updated only `advanced_seo_front_page_description` through `/wp-json/jetpack/v4/settings`.

- Before length: `246`
- After length: `153`
- After value: `Kris Krüg is an AI keynote speaker and creative technologist building community-first tools, talks, training, and media across BC+AI and Both Hands Full.`
- REST write status: `200`
- Readback: matched exact value.

Rollback: restore the previous `advanced_seo_front_page_description` value through the same Jetpack settings endpoint.

### Aurora theme

Uploaded through WordPress admin Appearance → Add Themes → Upload Theme, choosing only the bounded `Replace installed with uploaded` action.

- Final package: `/Users/kk/Desktop/kk-aurora-1.3.21.zip`
- SHA-256: `969f8d4ad366904d5619cf578b6a722054c5a749978954bac0cd140ce46a1bc3`
- `unzip -t`: no errors.
- WordPress confirmation: `Theme updated successfully.`
- PressCACHE admin purge: `Cache Purge: Success`.

Rollback: upload the prior `kk-aurora` package through the same theme replacement flow, then purge PressCACHE.

## Public Readback

Cache-busted readback with `Codex issue-workdown readback/1.0` user agent.

- `https://kriskrug.co/wp-content/themes/kk-aurora/style.css`: `Version: 1.3.21`.
- `/`: standard and Open Graph descriptions both match the new 153-character homepage description; Twitter Card is `summary_large_image`; `twitter:site` is `@feelmoreplants`; Twitter title/description now present.
- `/blog/`: standard, Open Graph, and Twitter descriptions all match the posts-page description; Twitter Card is `summary_large_image`; `twitter:site` is `@feelmoreplants`; `twitter:image:alt` length `66`.
- Latest post sample `sovereign-ai-for-whom`: standard/Open Graph/Twitter descriptions present; Twitter Card is `summary_large_image`; `twitter:site` is `@feelmoreplants`; Twitter title/description/image/alt present.
- `/blog/` exposes the visible `aurora-feed-links` section and 10 RSS discovery links.
- Category feeds returned `200` with RSS/XML content:
  - `/category/artificial-intelligence/feed/`
  - `/category/ai-tools/feed/`
  - `/category/speaking/feed/`
  - `/category/community/feed/`
- 404 search form readback:
  - HTTP status `404`.
  - `wp-block-search` present.
  - `Search kriskrug.co` visible label present.
  - `aria-label="Search kriskrug.co"` present.
  - `aria-label="Submit search"` present.

## Image Audit

Command:

```sh
make public-image-audit DEFAULT_URLS=1 CHECK_URLS=1 TIMEOUT=8 OUTPUT=docs/current-state/reports/public-image-audit-20260618-default.md
```

Result:

- Pages scanned: `8`.
- Images discovered: `89`.
- Missing `alt` attribute: `8`, all Facebook noscript tracking pixels.
- Empty non-decorative alt: `0`.
- Decorative empty alt: `8`.
- Filename-style alt: `0`.
- Images with `srcset`: `28`.
- Images with lazy loading: `64`.
- Broken checked image URLs: `1`, a legacy Flickr/Jetpack proxy on `/flickr-photographr-badge/` returning `429`.
- Oversized checked image URLs: `28`.

#4/#40 should remain open as a narrowed image-performance/follow-up lane unless the team decides the public-default sample is enough to split and close the broad original scope.
