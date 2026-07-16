# Issue #36 — public meta description re-probe

**Captured:** `2026-07-16T03:01:25Z`
**Mode:** public HTML only. No WP writes. No Search Console.
**Compared to:** `issue-36-public-render-diagnosis-20260617-211531Z.md`

## Headline finding

Across the probed marketing/core routes, the standard HTML meta tag `name="description"` is **absent**.
Social descriptions still emit via Jetpack-style `og:description` and usually `twitter:description`.
This is a **public-render regression vs the 2026-06-17 diagnosis**, which still saw a 246-character standard description on `/` and `/blog/`.

## Drift vs June diagnosis

| Signal | 2026-06-17 | 2026-07-16 (this probe) |
|---|---|---|
| `/` `name=description` | present, 246 chars | **missing** |
| `/blog/` `name=description` | present, 246 chars | **missing** |
| `/contact/` `name=description` | present, 152 chars | **missing** |
| `/` `og:description` | 246 chars | **294 chars** (still long) |
| `/blog/` `og:description` | 163 chars | **154 chars** (blog-specific) |
| `/` `og:title` | (also tracked under #346) | **still missing** |

## Table

| URL | Status | `description` | `og:description` | `twitter:description` | `og:title` |
|---|---:|---:|---:|---:|---|
| `/` | 200 | ∅ | 294 | 343 | ∅ |
| `/blog/` | 200 | ∅ | 154 | 154 | Writing — Kris Krug |
| `/blog/page/2/` | 200 | ∅ | 154 | 154 | Writing — Kris Krug |
| `/home/` | 200 | ∅ | ∅ | ∅ | Recent Posts & Updates: |
| `/services/` | 200 | ∅ | 300 | 367 | Generative AI Creative Services & Strategy |
| `/generative-ai-services/` | 200 | ∅ | 300 | 367 | Generative AI Creative Services & Strategy |
| `/contact/` | 200 | ∅ | 300 | 328 | Contact Kris Krüg |
| `/about/` | 200 | ∅ | 300 | 357 | About Kris Krüg |
| `/work/` | 200 | ∅ | 133 | 133 | Work |
| `/speaking/` | 200 | ∅ | 300 | 389 | AI Keynote Speaker Kris Krüg |
| `/publications/` | 200 | ∅ | 300 | 388 | Publications |

## Notable samples

- `/` og:description (294): Kris Krüg, Generative AI for Creative Professionals Generative engines now spill out adequate everything. What the world needs, and will pay for, is authored judgment, taste that can be explained, def…
- `/blog/` og:description (154): Read Kris Krüg's field notes on responsible AI, creative technology, community building, Indigenous tech, media, culture, practical workflows, and events.
- `/contact/` og:description (300): Contact Tell me what kind of room you are building. The fastest path is email. Send the shape of the thing: keynote, workshop, media appearance, strategy session, community partnership, or strange cre…
- `/about/` og:description (300): My name is Kris Krug – a boundary-pushing Creative Explorer, an intuitive Tech Whisperer, and a tenacious Culture Hacker.   In the fabric of the digital era, where technology often overshadows humanit…
- `/work/` og:description (133): Explore Kris Krüg's work across BC+AI, AI keynotes, community infrastructure, creative technology, training, and visual storytelling.

## Interpretation (narrows #36)

1. Do **not** reopen a broad REST “missing meta description” backfill — REST inventory was previously clean.
2. The live blocker is now **public render ownership**: standard `description` tag no longer appears on core routes.
3. Likely owners to check (human/admin): Jetpack SEO/social settings, theme/`document_title`/meta callbacks, Code Snippets, page cache after SEO plugin changes, Aurora 1.3.40 SEO modules once deployed.
4. Homepage still needs `og:title` (#346) and shorter social description.
5. `/blog/` and `/blog/page/2/` still lack self-canonicals (see SEO gap re-probe / #347) — separate from this meta-description gap.
6. Do **not** add a duplicate theme metadata emitter while Jetpack already emits OG/Twitter tags — diagnose the missing standard tag first.

## Agent-safe status

- Inventory only. No live writes.
- Re-run this probe after Aurora 1.3.40 deploy and any Jetpack/SEO setting change.

JSON twin: `issue-36-public-meta-reprobe-20260716.json`

