# Issue #340: Legacy BC + AI Link Handoff

**Track:** A - Content + SEO
**Status:** repo-side human-review handoff; no live WordPress write
**Manifest:** `fixes/issue-340-legacy-bcai-links-handoff-2026-07-13.json`

## Decision

A public read-only audit found 41 `bc-ai.net` links across 13 published
KrisKrug.co posts. Thirty links have exact successors on the indexed
`bc-ai.ca` site. The other 11 point to historical Hackathon or Squamish
surfaces without a truthful one-to-one successor.

This handoff prepares only the 30 exact href replacements. It leaves all
visible copy unchanged and records the 11 ambiguous links without modifying
them. Do not apply these patches from this PR.

## Why This Matters

The legacy organization root currently returns a temporary `302` to
`https://vancouver.bc-ai.net/ecosystem`. The destination renders the generic
title `Notion`, declares `noindex`, and has no canonical. Other audited legacy
subdomains have the same generic metadata and no canonical, with inconsistent
`noindex` posture.

The current BC + AI organization and community routes all return `200`, are
self-canonical or canonical-equivalent, are indexable, and each appears once
in the live sitemap.

The measured query-page pair also supports the repair. For the 28-day window
from 2026-06-13 through 2026-07-10, the query `bc ai` produced 49 impressions,
0 clicks, 0% CTR, and average position 8.73 for:

`https://kriskrug.co/2025/02/16/bcs-ai-ecosystem-a-mycelial-network-of-creation/`

The prior 28-day window produced 50 impressions, 0 clicks, and average
position 9.2. The page's only BC AI link currently points to the legacy
noindex surface.

## Approved Mappings

| Legacy destination | Indexed canonical destination |
|---|---|
| `https://bc-ai.net/` and `https://www.bc-ai.net/` | `https://bc-ai.ca/` |
| `https://vancouver.bc-ai.net/` | `https://bc-ai.ca/communities/vancouver-ai` |
| `https://vancouver.bc-ai.net/ai-ethical-futures-lab` | `https://bc-ai.ca/communities/futures-lab` |
| `https://surrey.bc-ai.net/` | `https://bc-ai.ca/communities/surrey` |
| `https://mac.bc-ai.net/`, `http://mac.bc-ai.net/`, and `https://mind.bc-ai.net/` | `https://bc-ai.ca/communities/mac` |

The manifest records each post ID, slug, public modified timestamp, exact old
href, exact replacement href, expected counts, and existing anchor text.

## Intentionally Unresolved

- Nine historical Data Storytelling Hackathon links remain unchanged. The
  current Build Night page is related but is not a truthful replacement for
  the historical registration and event references.
- Two Squamish AI links remain unchanged because `bc-ai.ca` does not currently
  expose a dedicated Squamish community page.

Do not send either group to a generic events or communities index merely to
eliminate a legacy hostname.

## Separate Publisher Gate

Any future live session requires exact action-time approval. Then:

1. Fetch all 13 posts by ID and confirm slug, published status, and modified
   timestamp. Stop if any guard changed.
2. Snapshot each `content.raw` body with a SHA-256 checksum.
3. Confirm every expected legacy href count and every expected new href count.
4. Generate and review an href-only diff. Visible anchor text and all other
   body markup must remain byte-for-byte unchanged.
5. Send only the `content` top-level REST key, one post at a time. Do not send
   title, slug, status, date, taxonomies, metadata, or featured media.
6. Read back each changed post, verify its source page and destination return
   `200`, and retain the before snapshot as the rollback payload.
7. Stop and roll back the individual post if any link count, canonical, or
   public-render invariant fails.

## Measurement

Start the clock only after a separately approved publisher session and clean
public readback. Compare the `bc ai` query and Mycelial Network landing page
after 14 full days and again after 28 full days using impressions, clicks,
CTR, and average position. Do not attribute movement to this repo-only PR.

## Out Of Scope

- No WordPress write, deployment, cache purge, Search Console request, GA4
  change, DNS change, Notion change, or analytics change.
- No visible article copy, title, description, schema, taxonomy, media, or
  publication-date edit.
- No guessed replacement for the Hackathon or Squamish links.
