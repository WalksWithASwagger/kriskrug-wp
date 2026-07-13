# Issue #335: Lord of the Rings Drinking Game SEO Handoff

**Track:** A - Content + SEO
**Status:** repo-side human-review handoff; no live WordPress write
**Manifest:** `fixes/issue-335-lotr-drinking-game-seo-handoff-2026-07-13.json`

## Decision

The page already satisfies the search intent and its title, H1, URL, and body
all use the primary query naturally. A new article or body rewrite would add
risk without solving the visible problem. The smallest useful move is:

1. Keep the public post title and historical body unchanged.
2. Add a shorter search title and a standard meta description.
3. Replace two irrelevant automated collection-footer recommendations with a
   coherent link pair between two humorous 2004 archive posts.

This packet does not publish, deploy, update WordPress, purge cache, request
indexing, or change Search Console, GA4, DNS, schema, taxonomies, or theme code.

## Digest-Safe Evidence

The current Search Console window is 2026-07-04 through 2026-07-10. The prior
window is 2026-06-27 through 2026-07-03.

| Surface | Window | Impressions | Clicks | CTR | Average position |
| --- | --- | ---: | ---: | ---: | ---: |
| Target page | Current | 47 | 0 | 0% | 10.43 |
| Target page | Prior | 35 | 0 | 0% | 11.54 |
| Query `lord of the rings drinking game` | Current | 27 | 0 | 0% | 9.96 |
| Query `lord of the rings drinking game` | Prior | 12 | 0 | 0% | 12.67 |

The page and primary query are both moving toward page one while still earning
no clicks. This makes snippet clarity a stronger first move than more content.
Only aggregate Search Console values are retained here. No exports, OAuth
material, private analytics rows, or person-level data are included.

## Public Mapping

Read-only public HTML and WordPress REST checks on 2026-07-13 mapped the
opportunity to post 35:

- URL: https://kriskrug.co/2004/05/27/the-lord-of-the-rings-drinking-game/
- Slug: `the-lord-of-the-rings-drinking-game`
- Public modified value: `2026-06-14T22:30:33`
- Status: `publish`
- HTTP: `200`
- Canonical: self-referencing and correct
- H1 count: 1
- Robots: indexable, with `max-image-preview:large`

The current document title is 92 characters after Aurora appends the site
descriptor. The page has no standard meta description. Its Open Graph and
Twitter descriptions are 294 and 308 characters and begin with the article's
setup rather than the four game rules.

The public REST response exposes only the `footnotes` meta key. It does not
expose `jetpack_seo_html_title` or `advanced_seo_description`, so a future
publisher must not attempt a generic REST metadata write.

## Review-Ready Metadata

These are SEO fields only. Do not change the public post title, excerpt, body,
slug, status, date, or taxonomies as part of the metadata step.

| Field | Proposed value | Characters |
| --- | --- | ---: |
| `jetpack_seo_html_title` | The Lord of the Rings Drinking Game: 4 Original Rules | 53 |
| `advanced_seo_description` | Four original Lord of the Rings drinking game rules for Frodo, Sam, Legolas, and cliff falls, plus a trilogy marathon option. Play responsibly. | 143 |

The title preserves the exact primary query and adds a specific reason to
click. The description summarizes only material already present in the post
and adds a concise responsibility cue.

Aurora 1.3.38 must be live and verified as the standard-description owner
before this metadata is judged. If the two Jetpack fields remain absent from
REST, use the reviewed WordPress editor fields after a fresh readback. Do not
add a page-specific theme override or metadata snippet.

## Related-Link Review

The current collection-footer recommendation on both relevant posts points to
an unrelated 2023 AI companions article. The review-ready replacement pairs
the target with [McSweeney's Lists](https://kriskrug.co/2004/07/16/mcsweeneys-lists/),
post 58. That post is from the same 2004 archive, is explicitly a humor-list
entry, and includes an `Elvish or Yiddish` section.

Proposed footer destinations:

| Source | Modified guard | Current recommendation | Proposed recommendation |
| --- | --- | --- | --- |
| Post 58, `mcsweeneys-lists` | `2026-06-14T22:29:25` | AI companions article | The Lord of the Rings Drinking Game |
| Post 35, target page | `2026-06-14T22:30:33` | AI companions article | McSweeney's Lists |

These are destination and anchor decisions, not exact write payloads. Only
public `content.rendered` was inspected. A separately approved publisher must
snapshot authenticated `content.raw`, derive the exact footer-only patches,
and stop if either ID, slug, status, or modified guard changed.

One apparent candidate was rejected. Post 5236 contains the phrase `Lord of
the Rings trilogy`, but it discusses filmmaking technology. Linking that
phrase to a drinking game would misrepresent the destination.

## Separate Publisher Gate

Do not apply this handoff from the worker lane. In a future publisher session
with explicit approval for these exact WordPress edits:

1. Confirm Aurora 1.3.38 is live and emits one standard, Open Graph, and
   Twitter description on the target.
2. Fetch posts 35 and 58 by ID and confirm slug, `publish` status, and modified
   values. Stop if any guard changed.
3. Snapshot target metadata, both posts' authenticated `content.raw`, and
   their public HTML. Record checksums before writing.
4. Review the exact metadata and both related-footer destinations with the
   human.
5. Apply the target SEO fields through registered WordPress editor fields. Do
   not use REST while those fields are unregistered.
6. Derive each footer-only patch from the fresh raw snapshot. The only allowed
   top-level REST key for a content write is `content`.
7. Apply one write at a time and read it back before continuing. Do not send
   title, excerpt, slug, status, date, categories, tags, or meta.
8. Verify both pages remain `200`, self-canonical, indexable, and one-H1. Verify
   the target has one contextual inbound link from post 58 and each related
   footer points to the reviewed destination.
9. Retain the snapshots as rollback payloads. Restore only the changed fields
   if any public readback fails.

## Next Digest Verification

Wait at least 14 full days after the approved live change, then compare the
query and landing page together. Repeat at 28 days if volume remains low.

- Page baseline: 47 impressions, 0 clicks, 0% CTR, position 10.43
- Query baseline: 27 impressions, 0 clicks, 0% CTR, position 9.96
- Success signals: at least one page click, at least one query click, page
  position below 10, and query position below 9.5

Do not attribute movement to this handoff until the production changes are
approved, applied, publicly verified, and recrawled.
