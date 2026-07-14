# Issue #342: Both Hands Full Canonical-Link Handoff

**Track:** A - Content + SEO
**Status:** repo-side human-review handoff; no live WordPress write
**Manifest:** `fixes/issue-342-both-hands-full-link-handoff-2026-07-13.json`

## Decision

Do not publish the draft in `WalksWithASwagger/bothhandsfull#103` as a new
KrisKrug.co post. The public article, title, and slug already exist at:

https://kriskrug.co/2026/01/24/both-hands-full/

Publishing another version would create duplicate content and compete with the
established URL. The existing article already contains the right contextual
anchor, but its destination is the old Notion keynote. The smallest useful
change is to preserve every word and replace only that href with the live
Both Hands Full canonical homepage.

This handoff does not update WordPress, publish content, deploy code, purge a
cache, request indexing, or change Search Console, analytics, DNS, metadata,
taxonomies, or theme code.

## Digest-Safe Evidence

The current 28-day Search Console window is 2026-06-13 through 2026-07-10:

| Surface | Impressions | Clicks | CTR | Average position |
| --- | ---: | ---: | ---: | ---: |
| Existing KrisKrug.co article | 56 | 3 | 5.36% | 8.27 |
| Both Hands Full property | 6 | 0 | 0.0% | 21.67 |
| Both Hands Full homepage | 4 | 0 | 0.0% | 16.5 |

The article is already earning search visibility. The target property is still
young enough that one relevant editorial path from the established article is
a sensible discovery and entity-association improvement. This is not a promise
that one link will improve rankings.

## Public Mapping

Read-only checks on 2026-07-13 locked the source to WordPress post 11171:

- Slug: `both-hands-full`
- Status: `publish`
- Public modified value: `2026-06-28T20:26:51`
- URL and canonical: `https://kriskrug.co/2026/01/24/both-hands-full/`
- HTTP: `200`
- H1 count: 1
- Robots: `max-image-preview:large`

The target `https://www.bothhandsfull.com` also returns `200`, emits the same
self-canonical URL, has one H1, and is indexable. Public REST
`content.rendered` currently has one old Notion anchor and zero editorial hrefs
to the target. The future publisher must repeat these guards against
authenticated `content.raw` before writing.

## Exact Href-Only Patch

Current public paragraph:

```html
<p>So I’m asking you to walk forward with <a href="https://kriskrug.notion.site/keynote-both-hands-full?source=copy_link">both hands full</a>.</p>
```

Review replacement:

```html
<p>So I’m asking you to walk forward with <a href="https://www.bothhandsfull.com">both hands full</a>.</p>
```

The sentence and anchor text stay unchanged. The replacement adds no `rel`
attribute and makes no metadata, title, excerpt, slug, status, date, taxonomy,
or unrelated body-copy change.

## Separate Publisher Gate

Do not apply this handoff from the worker lane. Add it to the human-gated July
publisher batch in #339 and apply it only after explicit approval of this exact
href replacement.

1. Fetch post 11171 by ID and confirm the slug, `publish` status, and modified
   value. Stop if any guard changed.
2. Fetch the raw body and public HTML. Confirm the exact current anchor occurs
   once and the canonical target href occurs zero times.
3. Snapshot `content.raw`, the public HTML, and their checksums before writing.
4. Replace the exact anchor once in the raw body. Send only the top-level
   `content` field. Do not send title, excerpt, slug, status, date, taxonomies,
   or meta.
5. Read back the authenticated raw body and anonymous public page. Confirm the
   old href is absent, the target href occurs once, and the article remains
   `200`, self-canonical, indexable, and one-H1.
6. Confirm the target still returns `200` with its matching self-canonical.
7. Retain the raw snapshot as the rollback payload. Restore only `content` if
   any guard or public readback fails.

The source is already indexed and the target homepage already has impressions,
so this publisher change does not need a separate indexing request.

## Measurement

Wait at least 14 full days after the approved live edit, then compare source
article and target-property visibility against the locked baseline. Repeat at
28 full days. Track impressions, clicks, CTR, and average position, but do not
attribute movement to this one link without broader supporting evidence.
