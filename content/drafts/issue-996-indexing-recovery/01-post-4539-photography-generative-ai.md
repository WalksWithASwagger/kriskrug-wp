# Rank 1 — post 4539 photography / generative AI

**URL:** https://kriskrug.co/2024/01/31/exploring-the-intersection-of-photography-and-generative-ai/
**Slug:** `exploring-the-intersection-of-photography-and-generative-ai`
**Status:** publish
**GSC:** named on 2026-09-06 as crawled-not-indexed. URL Inspection not available in the prep session.
**Action:** content improvement + internal-link repair + manual indexing recommendation
**Do not exclude.** Fresh public GET still shows 200, one self-canonical, no noindex.

## Identity guards (public REST 2026-09-08T05:54Z)

| Field | Value |
|---|---|
| id | 4539 |
| slug | `exploring-the-intersection-of-photography-and-generative-ai` |
| status | publish |
| link | `https://kriskrug.co/2024/01/31/exploring-the-intersection-of-photography-and-generative-ai/` |
| date | `2024-01-31T07:35:23` |
| modified | `2026-06-28T20:36:28` |
| modified_gmt | `2026-06-29T04:36:28` |
| featured_media | 4546 |
| categories | [1665] |
| public `content.rendered` sha256 | `61c47a5663714c78ece41476b542cf81dcc88849d63e9aff483080e62c5b0c46` |
| public `content.rendered` bytes | 12809 |

Abort on any ID/slug/status/modified mismatch. Re-GET `content.raw` before PATCH; do not treat the rendered hash as the abort condition.

## Live fields (public HTML authoritative)

| Field | Live 2026-09-08 | Proposal |
|---|---|---|
| HTTP | 200 | no change |
| canonical | self, one tag | no change |
| robots | `max-image-preview:large` | no change |
| `<title>` / `jetpack_seo_html_title` | `Photography Meets Generative AI: Frank Yu Residency` | **keep** |
| `advanced_seo_description` | present-tense February invite, 157 chars | **overwrite** (below) |
| H1 / post title | Exploring the Intersection of Photography and Generative AI | **keep** |
| inbound hrefs | 3820 and 3219 footers only | do not edit those two posts |
| Hartman inaugural-artist href | Notion `John-Hartman-Chasing-the-Muses…?pvs=4` | retarget to 4372 |
| Frank Yu href in the opener | LinkedIn only | add on-site 3082 in the new paragraph |

## A. Description overwrite

Allowlisted meta key only.

**Live:**
`Join the Future Proof Creatives AI Art Residency every Thursday in February with Frank Yu, exploring the shift from traditional photography to generative AI.`

**Proposed:**
`Frank Yu's February 2024 Future Proof Creatives residency on what happens when photography and generative AI share a table. A dated session record, still the photography-and-AI door on this site.`

Leave `jetpack_seo_html_title` alone.

## B. Content insert (answer-first)

Insert **before** the current first paragraph. Do not delete the February session facts.

**FIND** (exactly once):

```html
<p class="wp-block-paragraph">Dive into the <a href="https://kriskrug.notion.site/AI-Artist-in-Residence-Program-7b5ef79e367043ecb0e62af0dc2d7857">Future Proof Creatives AI Art Residency Program</a> every Thursday in February for a series of enlightening discussions with <a href="https://www.linkedin.com/in/frankyu/">Frank Yu</a>.
```

**REPLACE:**

```html
<p class="wp-block-paragraph">Photography does not stop being photography when a generative model enters the room. It becomes a fight about craft, authorship, and what you still choose to point a camera at. In February 2024, <a href="https://kriskrug.co/2023/09/06/exploring-the-world-of-ai-image-generation-with-artist-frank-yu/">Frank Yu</a> ran a free Future Proof Creatives residency on that intersection.</p>
<p class="wp-block-paragraph">Dive into the <a href="https://kriskrug.notion.site/AI-Artist-in-Residence-Program-7b5ef79e367043ecb0e62af0dc2d7857">Future Proof Creatives AI Art Residency Program</a> every Thursday in February for a series of enlightening discussions with <a href="https://www.linkedin.com/in/frankyu/">Frank Yu</a>.
```

## C. Hartman permalink retarget

Keeps the later Notion "Chasing the Muses" documentation link. Only the inaugural-artist href moves on-site.

**FIND** (exactly once):

```html
hosting <a href="https://kriskrug.notion.site/John-Hartman-Chasing-the-Muses-30924a146c4e4e0fae7267abc0f26ff1?pvs=4">Johnny Hartman (IHAVEROBOTS) as our inaugural artist</a>
```

**REPLACE:**

```html
hosting <a href="https://kriskrug.co/2023/12/28/building-ai-companions-w-john-anthony-hartman-of-ihaverobots/">Johnny Hartman (IHAVEROBOTS) as our inaugural artist</a>
```

## Inbound sources for this target

1. Post 3082 — wrap in `02-post-3082-frank-yu.md`
2. Post 4372 — wrap in `03-post-4372-hartman-companions.md`

Do not add a third wrap on 3820, 3219, or page 12316.

## Rollback

Restore snapshotted `content.raw` and the prior `advanced_seo_description`. Title, slug, and taxonomies were never in the write set.

## Manual indexing (after purge, KK only)

Submit this exact pretty permalink in URL Inspection if it is still crawled-not-indexed. That is a recommendation, not an agent action.
