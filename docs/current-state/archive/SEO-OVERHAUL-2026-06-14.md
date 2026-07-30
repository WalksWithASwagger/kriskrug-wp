# SEO overhaul — 2026-06-14

A one-day, end-to-end SEO overhaul of kriskrug.co (Pagely WordPress, all writes via REST). Every write was guarded, readback-verified, and rollback-recorded. Branch: `codex/parallel-lanes-20260614`.

## What changed

| Lever | Result | Issue |
|---|---|---|
| **Metadata backfill** (additive) | post metadata coverage **~3% → ~97%**: missing meta-description 961→24, missing social 819→1, missing SEO title 961→364 (the 364 are intentional long-title skips where WP keeps the full title) | #36 |
| **Crafted flagship metadata** | **107 posts** got hand-crafted SEO titles (≤60ch, keyword-front-loaded) + descriptions (140–160ch, SERP-safe) in KK voice — the entire AI-era body of work (late-2023→2026) | #36 |
| **Key-page descriptions** | 8 flagship pages (home/about/speaking/work/services/podcast/blog/contact) → crafted 150–158ch descriptions | #36 |
| **Alt text** | 4 fixes applied incl. the About page's empty OG-card image | #176 |
| **Category taxonomy** | 5 new categories created; **461 high-confidence posts** reassigned out of "Misc" (839→378); spread across the new ~14-category taxonomy | #223 |
| **Root files** | llms.txt + robots.txt AI-crawler policy verified live (served dynamically by WP) | #221 |

## Tooling built

- `scripts/seo-backfill/` — additive backfill (`backfill_meta.py`, default dry-run) + `--from-file` **overwrite mode** for KK-approved crafted values (slug-guarded, records prior values), pure `backfill_lib.py`, 24 unit tests. `make seo-backfill` / `make seo-audit`.
- `scripts/seo-backfill/reassign_categories.py` — read-modify-write category reassignment (drops Misc, preserves other categories, records old).

**Safety property:** every metadata write is `{"meta": {<=3 allowlisted keys>}}` — it cannot touch title/slug/content, so the 2026-05-15 overwrite incident class is structurally unreachable. Post-write verification is entity-normalization tolerant.

## Artifacts & rollback records

- Crafted review docs + approved JSONs: `content/drafts/SEO-CRAFTED-2026-06-14*.md` + `seo-crafted-approved-2026-06-14*.json` (4 batches).
- Backfill + overwrite reports (with prior values): `docs/current-state/reports/seo-backfill-*.md`, `seo-overwrite-*.md`.
- Category reassignment rollback: `docs/current-state/reports/category-reassign-*.md`.
- Page-description rollback: `docs/current-state/reports/seo-page-desc-rollback-2026-06-14.json`.
- Alt-text rollback: `docs/current-state/reports/alt-text-rollback-2026-06-14.json`.
- Misc→category first-pass mapping: `docs/current-state/CATEGORY-MAPPING-MISC-2026-06-14.md`.

## Open items (see plan / issues)

- **Categories #223**: 378 low-confidence Misc posts remain (mostly pre-2023 legacy blog) → era-bucket into Web & Early Blog / Photography, then retire empty Misc + Oil Spill.
- **Public-render verification**: confirm crafted metadata renders logged-out (Pagely cache may need a purge — see [[pagely-page-cache-purge]]).
- **Internal linking #38**, **featured images for 6 posts**, **favicon #161** (needs a square brand asset) — each its own pass, gated on KK assets/approvals.
