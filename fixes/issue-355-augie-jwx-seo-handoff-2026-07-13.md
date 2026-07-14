# Issue #355: Augie Studio JWX SEO Handoff

**Track:** A - Content + SEO
**Status:** repo-side human-review handoff; no live WordPress write
**Manifest:** `fixes/issue-355-augie-jwx-seo-handoff-2026-07-13.json`

## Decision

Preserve the original 2024 hands-on review and add one dated correction before
it. Augie Studio still has search demand, but its product context changed after
JWX acquired Aug X Labs in January 2026. The direct-to-consumer product is being
retired and the technology now serves publishers inside JWX Studio.

The useful change is therefore not a fresh product endorsement or a rewrite of
Kris's historical experience. It is one transparent status note plus metadata
that distinguishes the original review from the current enterprise product.

This handoff does not publish, deploy, update WordPress, purge cache, request
indexing, or change Search Console, GA4, DNS, schema, taxonomies, or theme code.

## Digest-Safe Evidence

The 28-day Search Console evidence covers 2026-06-12 through 2026-07-09:

| Surface | Impressions | Clicks | CTR | Average position |
| --- | ---: | ---: | ---: | ---: |
| Landing page | 186 | 0 | 0.00% | 11.62 |
| Query `augie ai` | 45 | 0 | 0.00% | 12.73 |
| Query `augie studio` | 32 | 0 | 0.00% | 17.19 |

Only aggregate values are retained. No Search Console export, OAuth material,
private query row, or person-level analytics data is included.

## Public Mapping

Read-only public REST and HTML checks on 2026-07-13 mapped the opportunity to
post 6019:

- URL: https://kriskrug.co/2024/06/18/augie-studio-review-ai-driven-video-production-analysis/
- Slug: `augie-studio-review-ai-driven-video-production-analysis`
- Status: `publish`
- Public modified value: `2026-06-14T20:11:57`
- HTTP: `200`
- Canonical: self-referencing and correct
- H1 count: 1
- Robots: indexable, with `max-image-preview:large`
- Standard meta description count: 0

The current Open Graph description still calls Augie a cutting-edge platform
revolutionizing consumer video production. Public REST exposes only the
`footnotes` meta key, not the two Jetpack SEO fields. A publisher must not use
a generic REST metadata write while those fields remain unregistered.

## First-Party Product Truth

The update is limited to facts confirmed by current first-party sources:

1. JWX announced the acquisition of Aug X Labs on January 15, 2026:
   https://jwx.com/news/jwx-augie-acquisition
2. JWX says Augie Studio is being incorporated into JWX Studio and the
   direct-to-consumer product will be sunset.
3. JWX Studio currently describes itself as an AI-assisted video production
   and repurposing product for publishers and media enterprises:
   https://jwx.com/jwx-studio
4. The current Augie sign-in surface says the consumer product is no longer
   offered while enterprise users transition: https://my.augie.studio/

All three URLs returned HTTP `200` during the read-only check. The packet does
not include acquisition terms, financial claims, or unannounced roadmap claims.

## Review-Ready Metadata

These are SEO fields only. Do not change the visible post title, excerpt, slug,
status, date, media, taxonomies, embeds, or original review body.

| Field | Proposed value | Characters |
| --- | --- | ---: |
| `jetpack_seo_html_title` | Augie Studio Review: AI Video Tool After JWX Acquisition | 56 |
| `advanced_seo_description` | A hands-on Augie Studio review, updated after JWX acquired Aug X Labs and sunset the consumer product. See what changed and who JWX Studio now serves. | 150 |

Issue #351's Aurora standard-description release, or its verified successor,
must own the standard description before these fields are judged in production.
If the Jetpack fields remain absent from REST, use only their reviewed editor
surfaces. Do not add a one-post theme override or metadata snippet.

## Review-Ready Status Note

Insert exactly this paragraph before the current opening paragraph:

```html
<p><strong>Update, July 2026:</strong> <a href="https://jwx.com/news/jwx-augie-acquisition">JWX acquired Aug X Labs</a>, the company behind Augie Studio, in January 2026. JWX is sunsetting Augie&#8217;s direct-to-consumer product and integrating its technology into <a href="https://jwx.com/jwx-studio">JWX Studio</a> for publishers and media enterprises. The hands-on review below is preserved as a snapshot of the 2024 product.</p>
```

The insertion point is the one current opening paragraph beginning `Hey tech
rebels and digital visionaries`. A future publisher must find that exact HTML
once and must find zero existing copies of the update note. The after-body is
the new paragraph, four newline characters, and the untouched original body.

No sentence, heading, embed, media reference, footer, team name, or historical
claim after the insertion may change in this batch.

## Separate Publisher Gate

Do not apply this handoff from the worker lane. In a future publisher session
with explicit approval for these exact changes:

1. Confirm the standard-description owner is live and emits one standard, Open
   Graph, and Twitter description on the target.
2. Fetch post 6019 with edit context. Confirm ID, slug, published status,
   modified value, canonical, visible title, and one-H1 state. Stop on drift.
3. Confirm `content.raw` contains the exact opening paragraph once and the
   update note zero times. Stop and regenerate the packet if either count
   differs.
4. Snapshot the edit-context response, raw body, public HTML, rollback body,
   and SHA-256 checksums before any write.
5. Review the full before/after body diff and the two metadata values with Kris.
6. Send only the top-level `content` key for the body insertion. Do not send
   `meta`, title, slug, status, dates, taxonomies, excerpt, author, media,
   comments, template, format, sticky, or password fields.
7. Apply the two SEO fields only through a registered endpoint or their exact
   WordPress editor controls. Do not guess a REST payload.
8. Read back authenticated raw content and cache-busted public HTML. Confirm
   the note and both official links appear once, the target remains `200`,
   self-canonical, indexable, and one-H1, and the original review is otherwise
   byte-preserved.
9. Retain the before snapshot as rollback input. Stop before rollback if a later
   edit changed the post. Restore only content and the two reviewed SEO fields,
   then repeat public and authenticated readback.

## Next Digest Verification

Wait at least 14 full days after a verified live change, then compare the page
and both queries against the locked 28-day baseline. Repeat at 28 full days.

Directional success requires at least one combined query click, `augie ai`
below average position 10, `augie studio` below 15, and landing-page CTR above
1.0%. Record impressions, clicks, CTR, and average position even when the
signals are mixed.

Do not attribute movement to this handoff until the changes are approved,
applied, publicly verified, and recrawled.
