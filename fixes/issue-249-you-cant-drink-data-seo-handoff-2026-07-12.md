# Issue #249: You Can't Drink Data SEO Handoff

**Track:** A - Content + SEO
**Status:** repo-side human-review handoff; no live WordPress write
**Manifest:** `fixes/issue-249-you-cant-drink-data-seo-handoff-2026-07-12.json`

## Decision

Use the single backlink reserved by issue #249 on the About page. The current
About introduction already joins technology, activism, AI, and human capacity,
and it has a canonical repo payload with a stable content marker. The homepage
has a legacy internal slug and less direct surrounding copy.

Neither surface currently contains the preferred phrase or target URL. This
handoff therefore proposes one sentence for human review instead of pretending
there is existing copy that can simply be wrapped in a link.

This PR does not publish, deploy, update WordPress, change Search Console, GA4,
DNS, analytics, schema, theme code, snippets, or secrets. It does not claim a
ranking improvement. The issue stays open until a separate publisher session
is approved, snapshotted, applied, publicly verified, and remeasured.

## Issue Baseline

Issue #249 records a 28-day baseline for 2026-06-12 through 2026-07-09:

| Surface | Impressions | Clicks | CTR | Average position |
|---|---:|---:|---:|---:|
| Landing page | 294 | 6 | 2.04% | 7.96 |
| Normalized `you cant drink data` variants | Present | 0 | Not provided | 8.4-8.7 |

These are issue-level aggregates only. No private Search Console export,
account identifier, or person-level analytics data is included.

## Target Mapping

Read-only public REST and HTML checks on 2026-07-12 mapped the target to:

- Post ID: `11936`
- Slug: `you-cant-drink-data`
- URL: `https://kriskrug.co/2026/05/23/you-cant-drink-data/`
- Status: `publish`
- Public modified value: `2026-06-28T18:40:25`
- Canonical: self-referencing target URL
- Public HTTP status: `200`

Any future publisher must stop if ID, slug, status, or modified value differs.

## Source Mapping

The selected source is the About page:

- Page ID: `1208`
- Slug: `about`
- URL: `https://kriskrug.co/about/`
- Status: `publish`
- Public modified value: `2026-07-01T11:33:51`
- Canonical: `https://kriskrug.co/about/`
- Content marker: `content-architecture-2026:about`
- Repo payload: `content/source-packs/content-architecture-2026/wp-payloads/about.html`
- Repo payload SHA-256: `1b3957ab6cbe9bb9b2401dc4fe9bd5006726de1ec70d1d86ac7711a0ccd8fb26`

The current About body contains zero instances of the preferred anchor and
zero links to the target. Its opening paragraph appears exactly once in the
tracked payload.

The homepage was also checked. It is page `3930`, with internal slug
`empowering-events-organizations-for-the-ai-age`, public URL `/`, published
status, and modified value `2026-06-29T16:49:49`. It also contains zero target
links, but the About introduction is the more coherent and better-guarded fit.

## Sentence-Level Proposal

Current paragraph:

```html
<p>I have spent two decades documenting technology, art, activism, conferences, communities, and the back rooms where culture actually changes. These days, most of that work points at one question: how do we use AI to increase human capacity instead of flattening human judgment?</p>
```

Review-ready replacement:

```html
<p>I have spent two decades documenting technology, art, activism, conferences, communities, and the back rooms where culture actually changes. These days, most of that work points at one question: how do we use AI to increase human capacity instead of flattening human judgment? That question includes the physical costs of AI infrastructure, which I confronted on the streets of Vancouver and wrote about in <a href="https://kriskrug.co/2026/05/23/you-cant-drink-data/">you can't drink data</a>.</p>
```

The only copy change is the final sentence. It adds the preferred anchor once,
opens in the same tab like other internal links, and makes no new ranking or
outcome claim.

## Separate Publisher Gate

Do not apply this proposal from this PR. In a future session with explicit
approval for the one live body edit:

1. Fetch page `1208` with edit context and only `id`, `slug`, `status`,
   `modified`, and `content`. Confirm the exact identity and modified guard
   above. Stop if any value differs.
2. Confirm `content.raw` contains the current paragraph exactly once and the
   target URL zero times. Stop for review if either count differs.
3. Create `backup/<UTC>-issue-249-ycdd-about-backlink/` containing the full
   edit-context response, public About HTML, and SHA-256 checksums before any
   write.
4. Build the after-body from the freshly fetched `content.raw`. Replace only
   the one paragraph shown above and review that exact body diff.
5. Send only the top-level REST key `content` to page `1208`. Do not send title,
   slug, status, dates, author, excerpt, media, comments, format, meta,
   template, parent, or menu order.
6. Read back authenticated raw content and public HTML. Confirm one visible
   anchor, one target href, unchanged source identity and non-content fields,
   source and target HTTP `200`, and both self-referencing canonicals.
7. Retain the before snapshot as the rollback body. Before rollback, require
   the current modified value to match the recorded post-write value; stop if
   someone has edited the page since the backlink write. Restore only
   `content`, then repeat the readback checks.

## Next Digest Verification

Measure only in the first SEO Growth Digest with at least seven full days after
the approved edit and public readback. Preserve a 28-day comparison window and
record the live-edit timestamp.

For both the landing page and normalized `you cant drink data` query variants,
record impressions, clicks, CTR, and average position. Compare the page with
`294 / 6 / 2.04% / 7.96` and the query cluster with `0` clicks and position
`8.4-8.7`.

A positive directional signal requires at least one query-cluster click and an
average position below `8.4`. If the seven-day gate is not met or impressions
are zero, record the result as not yet measurable. Do not claim causation from
this handoff or PR.

The PR must use `Refs #249`, not `Closes #249`. The remaining publisher gate is
human approval, snapshot, body-only application, public readback, and the next
eligible digest.
