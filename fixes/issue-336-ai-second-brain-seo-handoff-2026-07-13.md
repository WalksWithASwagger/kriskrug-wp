# Issue #336: AI Second Brain SEO Handoff

**Track:** A - Content + SEO
**Status:** repo-side human-review handoff; no live WordPress write
**Manifest:** `fixes/issue-336-ai-second-brain-seo-handoff-2026-07-13.json`

## Decision

This is the strongest current on-page opportunity on KrisKrug.co. The article
already matches the search intent and has an established URL, so the smallest
useful move is a tighter search title, a concise description, and two links
from existing relevant copy. No new article or speculative content is needed.

This handoff does not publish, deploy, update WordPress, purge cache, or change
Search Console, GA4, DNS, schema, taxonomies, or theme code.

## Digest-Safe Evidence

The 28-day Search Console review covers 2026-06-12 through 2026-07-09:

| Surface | Impressions | Clicks | CTR | Average position |
| --- | ---: | ---: | ---: | ---: |
| Target page | 1,053 | 10 | 0.95% | 11.27 |
| Query `ai second brain` | 46 | 2 | n/a | 17.52 |

Only aggregate values copied into GitHub issue #279 are retained. No Search
Console export, OAuth material, private analytics row, or person-level data is
included.

## Public Mapping

Read-only public HTML and authenticated WordPress REST checks on 2026-07-13
mapped the opportunity to post 8802:

- URL: https://kriskrug.co/2025/04/01/how-to-build-an-ai-second-brain-that-actually-works-for-you/
- Slug: `how-to-build-an-ai-second-brain-that-actually-works-for-you`
- Public modified value: `2026-06-28T20:27:34`
- Status: `publish`
- HTTP: `200`
- Canonical: self-referencing and correct
- H1 count: 1
- Robots: indexable, with `max-image-preview:large`

The current document title is 116 characters after Aurora appends the site
descriptor. The page has no standard meta description and uses the 262-character
excerpt for Open Graph and Twitter descriptions.

The authenticated REST response currently exposes only the `footnotes` meta
key. It does not expose `jetpack_seo_html_title` or
`advanced_seo_description`. A publisher must not attempt a generic REST meta
write while those fields are unregistered.

## Review-Ready Metadata

These are SEO fields only. Do not change the public post title, excerpt, body,
slug, status, date, or taxonomies.

| Field | Proposed value | Characters |
| --- | --- | ---: |
| `jetpack_seo_html_title` | Build an AI Second Brain That Actually Works for You | 52 |
| `advanced_seo_description` | Build an AI second brain that works with your thought patterns, captures creative chaos, and turns scattered notes and voice memos into finished work. | 150 |

The title keeps the exact topic and the article's real promise. The description
is grounded in the article's existing material about thought patterns, creative
chaos, scattered notes, voice memos, and finished work.

Aurora 1.3.38 should be live and verified as the standard-description owner
before this metadata change is judged. If the Jetpack fields remain absent from
REST, use the reviewed WordPress editor fields after a fresh readback. Do not
add another theme override or metadata snippet for one post.

## Review-Ready Link Patches

Both public source bodies contain the listed needle exactly once and currently
contain zero links to the target. Each patch wraps existing words only.

### Priority 1: AI for Journalists

- Source post: 9774
- URL: https://kriskrug.co/2025/06/24/what-journalists-need-to-know-about-ai-right-now/
- Public modified value: `2026-06-14T20:05:53`
- Existing phrase: `AI as a second brain`
- Review replacement:

  ```html
  <a href="https://kriskrug.co/2025/04/01/how-to-build-an-ai-second-brain-that-actually-works-for-you/">AI as a second brain</a>
  ```

### Priority 2: STORYHIVE Interview

- Source post: 12327
- URL: https://kriskrug.co/2026/06/17/storyhive-haus-of-owl-jordan-dack/
- Public modified value: `2026-06-17T19:47:06`
- Existing phrase: `knowledge bases and named assistants`
- Review replacement:

  ```html
  <a href="https://kriskrug.co/2025/04/01/how-to-build-an-ai-second-brain-that-actually-works-for-you/">knowledge bases and named assistants</a>
  ```

## Separate Publisher Gate

Do not apply this handoff from the worker lane. In a future publisher session
with explicit approval for these exact WordPress edits:

1. Confirm Aurora 1.3.38 is live and emits one standard, Open Graph, and Twitter
   description on the target.
2. Fetch the target and both sources by ID. Confirm slug, published status, and
   modified values. Stop if any guard changed.
3. Snapshot target metadata plus public HTML and each source's `content.raw`
   plus public HTML. Record checksums before writing.
4. Review the exact metadata values and link wrappers with the human.
5. Apply the two target SEO fields through a registered endpoint or the
   WordPress editor. Do not use REST while those fields are unregistered.
6. Apply one source link at a time. The only allowed top-level source REST key
   is `content`; do not send title, excerpt, slug, status, date, categories,
   tags, or meta.
7. Read back each write before continuing. Verify the target remains `200`,
   self-canonical, indexable, and one-H1, and verify each source has one visible
   contextual link.
8. Retain the snapshots as rollback payloads. Restore only the changed fields
   if any public readback fails.

## Next Digest Verification

Wait at least 14 full days after the approved live change, then compare the
query and landing page together:

- Page baseline: 1,053 impressions, 10 clicks, 0.95% CTR, position 11.27
- Query baseline: 46 impressions, 2 clicks, position 17.52
- Success signals: page position below 10, page CTR above 1.2%, and query
  position below 15

Do not attribute movement to this handoff until the production changes are
approved, applied, publicly verified, and recrawled.
