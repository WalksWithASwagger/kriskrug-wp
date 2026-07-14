# Issue #353: Legacy Body H1 Migration Packet

**Track:** A - Content + SEO
**Status:** repo-only migration packet; no live WordPress write
**Manifest:** `fixes/issue-353-body-h1-migration-2026-07-13.json`
**Tool:** `scripts/body_h1_migration.py`

## Decision

Fourteen published routes render the template title plus at least one body H1.
This packet prepares exact source-digest-gated changes from body H1 to H2. It
does not change titles, copy, slugs, dates, links, media, taxonomy, metadata,
publication status, Search Console, or the intentional homepage hero H1.

This packet does not claim a ranking lift. The repair gives each affected route
one clear document-level H1 and removes an avoidable heading-structure defect.

## Evidence Boundary

An authenticated, read-only WordPress `context=edit` inventory ran on July 13,
2026 in America/Vancouver:

- 967 published posts and 45 published pages were scanned.
- 15 source objects contained body H1 elements.
- Homepage page ID `3930` is the intentional exception and remains unchanged.
- The other 14 sources contain 44 body H1 elements.
- Twelve targets use Gutenberg `core/heading` level-1 blocks.
- Two targets contain one source-digest-locked classic H1 element each.
- No credential, application password, raw body, or private snapshot is stored
  in this packet.

## Locked Scope

| ID | Type | Body H1s | Format | Source SHA-256 prefix | URL |
|---:|---|---:|---|---|---|
| 11358 | Post | 9 | Gutenberg | `9b10466fd29f` | `https://kriskrug.co/2026/02/20/spa-at-the-end-of-time/` |
| 7927 | Post | 5 | Gutenberg | `979c550f2d4c` | `https://kriskrug.co/2024/12/31/ais-next-chapter-notes-from-bcs-ai-ecosystem/` |
| 6453 | Post | 1 | Gutenberg | `305ffb31101b` | `https://kriskrug.co/2024/07/28/small-file-rebellion-hacking-the-digital-carbon-footprint-at-our-networks-2024/` |
| 6435 | Post | 1 | Gutenberg | `a8c8a906c137` | `https://kriskrug.co/2024/07/27/digital-rebellion-w-lori-emersons-at-our-networks-2024/` |
| 6344 | Post | 9 | Gutenberg | `ca5290eacbab` | `https://kriskrug.co/2024/07/19/fuck-the-status-quo-ais-messy-love-child-with-creativity/` |
| 4826 | Post | 1 | Gutenberg | `59306ae2ade2` | `https://kriskrug.co/2024/03/05/join-the-future-proof-creatives-community/` |
| 4174 | Post | 1 | Gutenberg | `b968d719dcb3` | `https://kriskrug.co/2024/01/19/2024-the-year-of-ai-revolution-a-rebels-guide-to-predicting-the-future/` |
| 4372 | Post | 1 | Gutenberg | `1b2368b8bab5` | `https://kriskrug.co/2023/12/28/building-ai-companions-w-john-anthony-hartman-of-ihaverobots/` |
| 3908 | Post | 1 | Gutenberg | `ea43cecce977` | `https://kriskrug.co/2023/11/01/web3-will-fail-if-it-doesnt-put-people-before-profits-and-technology/` |
| 3567 | Post | 1 | Gutenberg | `0cf92d30ac25` | `https://kriskrug.co/2023/10/15/community-art-project-development-process-guide/` |
| 3151 | Post | 6 | Gutenberg | `189796c84ae7` | `https://kriskrug.co/2023/09/18/newsletter-002-rebirth-and-revolution/` |
| 2857 | Post | 6 | Gutenberg | `c6b1ce00c4cf` | `https://kriskrug.co/2023/08/22/through-my-lens-new-projects-and-updates-from-kris-krug/` |
| 1547 | Post | 1 | Classic | `1264538397e9` | `https://kriskrug.co/2009/12/14/photo-essay-inside-the-negotiations-cop15/` |
| 12013 | Page | 1 | Classic | `bf8dabd8d52e` | `https://kriskrug.co/photography/` |

The manifest records each exact ID, endpoint, type, slug, status, modified GMT
timestamp, URL, raw length, before digest, expected-after digest, body H1 count,
format, and heading text.

## Homepage Exclusion

Page ID `3930`, `https://kriskrug.co/`, contains the intentional homepage hero
H1. Its ID, slug, URL, modified timestamp, length, digest, format, and heading
text are locked separately in the manifest. The migration target list cannot
contain ID `3930`, and the inventory audit fails if its source or H1 count
changes unexpectedly.

## Transformation Contract

For Gutenberg targets, the tool parses each complete `wp:heading` comment and
its JSON attributes. It changes only reviewed blocks whose parsed `level` is
`1`: the level value becomes `2`, and that block's opening and closing H1 tags
become H2. It rejects loose H1 markup, malformed blocks, unexpected counts, or
an after digest that differs from the manifest.

For the two classic targets, the tool changes only the opening and closing tag
names of the single complete H1 element. The full authenticated source digest,
length, identity, modified timestamp, and count must all match first.

The exact patch keeps heading text, order, classes, anchors, and every
non-heading byte unchanged.

## Read-Only Audit And Plan

The default command performs a full authenticated inventory. It accepts the 14
reviewed sources in either their exact pending or exact migrated state, preserves
the homepage exception, accepts new H2/H3-only content, and rejects any new
non-homepage body H1 source.

```bash
python3 scripts/body_h1_migration.py audit \
  --env-path "$HOME/Code/kriskrug-wp/scripts/notion-to-wp/.env"
```

Plan one target without writing or printing its body:

```bash
python3 scripts/body_h1_migration.py plan \
  --target-id 11358 \
  --env-path "$HOME/Code/kriskrug-wp/scripts/notion-to-wp/.env"
```

## Separately Approved Production Run

No live action is authorized by this packet. A future publisher session needs
Kris's exact action-time approval, then must process one target at a time:

1. Run the full audit and stop on any drift.
2. Run `plan` for one approved target and review both digests and H1 counts.
3. Use the exact per-target confirmation string printed below.
4. Let the tool write a complete private raw-body snapshot before its only POST.
5. Let the tool read the same target back and verify identity, expected digest,
   expected length, and zero body H1s.
6. Complete public normal, cache-busted, and Googlebot readback before the next
   target.

The guarded command shape is:

```bash
python3 scripts/body_h1_migration.py apply \
  --target-id 11358 \
  --confirm APPLY-ISSUE-353-TARGET-11358 \
  --env-path "$HOME/Code/kriskrug-wp/scripts/notion-to-wp/.env"
```

The confirmation string is a technical interlock, not permission. The tool
refuses a batch apply and cannot accept more than one target ID.

## Snapshot And Rollback

Before the POST, the tool creates
`/private/tmp/kriskrug-issue-353-<id>-<UTC timestamp>.json` with mode `0600`.
It contains the complete authenticated raw body, identity fields, modified GMT
timestamp, rollback digest, and expected-after digest. The snapshot is local and
must not be committed.

If write or readback verification fails, stop the batch. In a separately
approved rollback session, verify the same ID, type, slug, status, and URL, then
restore only `content` from that target's snapshot and verify the snapshot
digest. Do not automate a blind rollback over intervening edits.

## Per-Target Completion Gate

Each approved route must pass all of these before the next target:

- WordPress readback matches the expected-after source digest and contains zero
  body H1 elements.
- Normal, cache-busted, and Googlebot HTTP requests return `200`.
- Rendered HTML contains exactly one H1, supplied by the template title.
- The canonical is self-referential and unique.
- The route remains indexable and present in the correct post/page sitemap.
- Title, slug, status, dates, copy, links, media, taxonomy, and metadata remain
  unchanged.

Do not request Search Console indexing for this migration. Ordinary crawling is
sufficient after the content repair.
