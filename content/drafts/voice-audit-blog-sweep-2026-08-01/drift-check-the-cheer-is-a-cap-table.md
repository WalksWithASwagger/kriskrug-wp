# Drift check — post 12479 "Watch Who's Smiling" (the-cheer-is-a-cap-table)

**Verdict: live matches the audited draft. No drift.**

The live post (fetched 2026-08-01 via REST, `snapshots/2026-07-10-the-cheer-is-a-cap-table.txt`)
was compared word-for-word against the pre-publish draft that passed its voice
audit clean (`content/drafts/2026-07-07-the-cheer-is-a-cap-table/post.md`,
audit verdict "ships clean" in that folder's `voice-audit/00-summary.md`).

## Method

`drift_diff.py` (this folder): draft markdown stripped of frontmatter, image
lines, link syntax, and emphasis markers; live snapshot stripped of its
`Title:`/`Link:` header; both sides had typographic quotes straightened,
whitespace collapsed, and punctuation reattached after link boundaries (the
HTML stripper detaches it). Dashes were deliberately **not** normalized so any
em dash introduced after the audit would surface as drift. Word-level
`difflib.SequenceMatcher` over the full token streams.

## Result

- 1,506 content words on both sides; similarity ratio **1.0000**; zero
  non-equal hunks. Every word of the audited draft is live, unchanged.
- Em dashes: **0 in the draft, 0 in the live text** — no post-audit slop
  crept in. The live snapshot also came back **0 flags** in this sweep's
  mechanical pass (`slop-check-raw.json`), consistent with the original
  pre-publish audit.
- Title: draft "Watch Who's Smiling" vs live "Watch Who’s Smiling" — curly
  apostrophe only (WordPress texturize), formatting not content.

## Excluded from the comparison (formatting layer, by design)

- Images and the YouTube trailer embed (draft has markdown image lines and a
  bare URL; live renders figure/embed blocks — no text content to compare).
- Markdown vs rendered-HTML syntax, typographic quote conversion.
- Publish-date metadata: draft frontmatter says 2026-07-07, live published
  2026-07-10 (publish slipped three days; not a content change).

Nothing here needs a fix. This post can be treated as the sweep's clean
baseline: pre-publish audit + live readback agree.
