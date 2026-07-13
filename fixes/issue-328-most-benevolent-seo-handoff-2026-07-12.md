# Issue #328: Most Benevolent SEO Handoff

**Track:** A - Content + SEO
**Status:** repo-side human-review handoff; no live WordPress write
**Manifest:** fixes/issue-328-most-benevolent-seo-handoff-2026-07-12.json

## Decision

The ranking page and the best contextual source paragraphs live in WordPress,
not in a canonical repo payload. This PR therefore stops at a precise handoff.
It does not publish, deploy, update WordPress, or change Search Console, GA4,
DNS, analytics, schema, or theme code.

A post-specific theme override or another metadata snippet would create a
second owner and a much wider blast radius than issue #328 warrants. The
smallest safe move is to prepare two copy-preserving contextual links for a
separately approved publisher session.

## Digest-Safe Evidence

The same-date digest file named by the issue was not present in the local
notion-local or kk-kb mirrors. This handoff uses only the aggregate values
copied into the live issue:

| Query | Impressions | Average position | CTR |
|---|---:|---:|---:|
| most benevolent | 20 | 8.4 | 0.0% |

No Search Console export, OAuth material, private analytics rows, or
person-level data is included.

## Public Mapping

Read-only public HTML and WordPress REST checks on 2026-07-12 mapped the query
to post 3814:

- URL: https://kriskrug.co/2023/11/04/the-power-of-most-benevolent-outcomes-a-prayer-for-blessings-for-all-living-things/
- Slug: the-power-of-most-benevolent-outcomes-a-prayer-for-blessings-for-all-living-things
- Public modified value: 2026-06-28T20:37:13
- HTTP: 200
- Canonical: self-referencing and correct
- Exact phrase: present in the visible title, headings, and body

The current document title is 115 characters after Aurora appends the site
descriptor. The page does not currently render a standard meta description;
it does render Open Graph and Twitter descriptions from the excerpt. The
earlier repo backfill skipped a custom SEO title for post 3814 because the
generated title was too long.

Those metadata observations are recorded for a future owner-confirmation pass,
but this handoff does not recommend a target-specific theme or snippet change.

## Review-Ready Link Patches

Both public source bodies contain the listed needle exactly once and currently
contain zero links to the target URL. Apply only after a fresh readback confirms
the same ID, slug, published status, and modified value.

### Priority 1: Community Weaving

- Source post: 2950
- URL: https://kriskrug.co/2023/09/01/community-weaving-how-digital-interactions-shape-our-physical-world/
- Public modified value: 2026-06-28T20:38:58
- Existing phrase:

    Most Benevolent Outcomes

- Review replacement:

    <a href="https://kriskrug.co/2023/11/04/the-power-of-most-benevolent-outcomes-a-prayer-for-blessings-for-all-living-things/">Most Benevolent Outcomes</a>

### Priority 2: Embracing the Future

- Source post: 2665
- URL: https://kriskrug.co/2023/07/09/embracing-the-future-my-journey-with-generative-ai-and-building-a-learning-community-on-discord/
- Public modified value: 2026-06-28T20:39:43
- Existing phrase:

    cultivating the most benevolent outcomes

- Review replacement:

    <a href="https://kriskrug.co/2023/11/04/the-power-of-most-benevolent-outcomes-a-prayer-for-blessings-for-all-living-things/">cultivating the most benevolent outcomes</a>

These replacements wrap existing words only. They add no sentence, claim, or
keyword repetition, and they make no title, taxonomy, metadata, status, slug,
or date change.

## Separate Publisher Gate

Do not apply these patches from this PR. In a future session with explicit
approval for live WordPress edits:

1. Fetch each source by ID and confirm slug, published status, and modified
   value. Stop for human review if any guard has changed.
2. Snapshot content.raw and rendered HTML for each source before editing.
3. Confirm the needle still occurs exactly once and the target href occurs
   zero times.
4. Review the exact body-only diff. The only allowed top-level REST key is
   content.
5. Apply one source at a time. Do not send title, slug, status, date,
   categories, tags, or meta.
6. Read back the source, verify the visible link and target 200 response, then
   retain the before snapshot as the rollback payload.

## Next Digest Verification

The next SEO Growth Digest should keep the query and landing page paired:

- Query: most benevolent
- Landing page: post 3814 URL above
- Baseline: 20 impressions, 0 clicks, 0.0% CTR, average position 8.4
- Compare: impressions, clicks, CTR, and average position
- Success signal: average position below 7 and at least one click

Record whether and when the two link patches were applied. Do not attribute
movement to this PR before the live links are approved, applied, publicly
verified, and recrawled.
