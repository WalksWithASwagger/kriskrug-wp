# Preview QA — scheduled queue (#207)

**Date:** 2026-06-14 · **By:** authenticated wp-admin preview (desktop 1323px + mobile 414px) + programmatic REST content scan
**Scope:** the 9 `future` posts scheduled 2026-06-16 → 07-02
**Result:** ✅ **PASS — all 9 clean on desktop and mobile. No blockers.**

## Method
- Programmatic scan of each rendered post (REST) for: missing featured image, images without alt text, internal/external link counts, and danger strings (localhost / local file paths / Notion URLs / `preview=true` leakage / raw markdown / expiring S3 links).
- Authenticated wp-admin preview render of every post on desktop; mobile (414px) spot-check across the three layout variants (illustrated hero, text-only, real photo).

## Per-post

| Date | Post | WP ID | Category | Featured img | Alt gaps | Render (desktop/mobile) |
|---|---|---|---|---|---|---|
| 06-16 | Sovereign AI for Whom? | 11905 | AI Ethics & Philosophy | ✅ 11899 | 0 | ✅ / ✅ |
| 06-18 | Why We Built the Responsible AI Professional Certification | 12257 | AI Ethics & Philosophy | ✅ 12244 | 0 | ✅ |
| 06-20 | A Practical Guide to Agentic Workflows | 12263 | AI for Creatives | ✅ 12258 | 0 | ✅ (see note) |
| 06-22 | The Great Canadian Proximity Game | 12190 | AI Ethics & Philosophy | ✅ 12311 | 0 | ✅ |
| 06-24 | AI Won't Fix Your Broken Permit Process | 12035 | AI Ethics & Philosophy | ✅ 12312 | 0 | ✅ |
| 06-26 | Canada Doesn't Need a Bigger AI Machine | 12030 | AI Ethics & Philosophy | ✅ 12313 | 0 | ✅ / ✅ |
| 06-28 | What Would Chat Do? | 12032 | AI Ethics & Philosophy | ✅ 12314 | 0 | ✅ |
| 06-30 | Zero to One: From Meetup to Movement | 12034 | Vancouver AI Ecosystem | ✅ 6835 (real photo) | 0 | ✅ / ✅ |
| 07-02 | AI Media Appearances, Podcast Guesting, and Broadcast Commentary | 11879 | Conversations & Interviews | ✅ 11205 (real photo) | 0 | ✅ |

## Checks confirmed
- **Categories** are correctly assigned (no "Misc"/Uncategorized) — the #75 Feature→Misc risk did not occur.
- **Featured images** present and rendering on all 9; the two real-photo posts (12034, 11879) use library photos, not generated art.
- **Alt text**: zero images missing alt across all 9.
- **No private/local URLs**: no localhost, local file paths, Notion links, S3 expiring URLs, or `preview=true` leakage in any rendered body.
- **No raw markdown** in rendered output.
- **Titles, deks, author, read-time** all render correctly; Aurora theme layout intact desktop + mobile.

## Notes (non-blocking)
- **12263** featured image (12258) has baked-in "GOD SKILLS" text — renders legibly, but this is the item KK previously flagged for naming / generated-image-text sign-off. Worth a final glance before 06-20.
- **12030** has 0 internal links (5 external). Optional: add an internal link for SEO/site cohesion; not a blocker.
- **12035** featured image carries baked text "CIVIC PERMIT PROCESS AUDIT…" — legible, no misspelling, acceptable.

No post was scheduled, published, or edited during this QA pass (preview-only).
