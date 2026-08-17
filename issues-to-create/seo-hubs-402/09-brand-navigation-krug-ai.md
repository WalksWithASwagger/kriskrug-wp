# [CONTENT] Add brand-navigation links for the krug ai query

**Parent:** [#402](https://github.com/WalksWithASwagger/kriskrug-wp/issues/402)
**Child:** 9 of 9
**Suggested labels:** `content`, `seo`, `needs-human-review`, `priority:medium`
**Lane:** Track A
**Research:** `content/drafts/2026-08-02-seo-authority-hubs/hub-plan.md` term 9, `link-matrix.csv` data rows 31-33
**Blocked by:** child 1 (taxonomy), child 4 (post 12030), and child 8 (post 11700)

---

## Context

`krug ai` is a brand navigational query. The homepage already answers it. Live `<title>` reads `Kris Krug | AI Keynote Speaker & Creative Technologist` (unaccented Krug). **No title change in this child.**

PR #670 thought the homepage title came from Jetpack `advanced_seo_title_formats.front_page`. That is stale. #756 and `docs/current-state/reports/title-format-source-diagnosis-20260815.md` showed the owner is `theme/kk-aurora/functions.php` (`document_title_parts` / `document_title_separator`). Jetpack SEO is deactivated (#661). Any title change is a **Track B** release, not this Track A child. Do not hunt page 3930 post-meta. Do not write Jetpack settings.

The useful move: who-and-what pages (`/speaking/`, `/about/`, `/glossary/`) one click from AI posts people actually land on.

Post **11879** (`ai-media-appearances-podcast-guesting`) already links `/about/`, `/speaking/`, `/publications/`, `/contact/`, and `/recent-projects-include/`. It is the model. Leave it.

This child is last because it shares post **12030** with child 4 and post **11700** with child 8. Full-body PATCHes on those posts cannot run in parallel.

## Owns (write)

- Post **12653** closing section → `/speaking/` (row 31).
- Post **12030** closing paragraph → `/about/` (row 32). Child 4 already added the drink-data sentence on an earlier paragraph. Do not retouch that sentence.
- Post **11700** early body, first term of art → `/glossary/` (row 33). Child 8 already added the MBO sentence in the **final** paragraph. Do not retouch that sentence.

## Must not touch

- Homepage / page 3930, `functions.php`, Jetpack, title formats, umlaut vs ASCII Krug.
- Post 11879.
- Rows 8 (12030 → 11936) and 4 (11700 → 3814).
- Theme, schema.

## Acceptance Criteria

- [ ] Children 4 and 8 have landed (or their 12030 / 11700 inserts are already live) before this child PATCHes those two posts.
- [ ] Post 12653 links `https://kriskrug.co/speaking/` with exact anchor `I give a talk about exactly this` (row 31), before the collection footer.
- [ ] Post 12030 links `https://kriskrug.co/about/` with exact anchor `why I keep saying this out loud` (row 32), in the closing paragraph, and still has child 4's drink-data anchor if that child has shipped.
- [ ] Post 11700 links `https://kriskrug.co/glossary/` with exact anchor `plain definitions for the words in here` (row 33), at the first term of art, and still has child 8's MBO anchor if that child has shipped.
- [ ] Post 11879 unchanged. Homepage `<title>` unchanged by this child.
- [ ] Content-only, snapshots, no em dashes, no duplicate footers.

## Tests/Evals

- `grep -F` the three exact anchors on cache-busted fetches.
- Regression: `grep -F 'what the water math looks like from street level'` still present on 12030 after this PATCH (if child 4 shipped).
- Regression: `grep -F 'the optimistic version of the same argument'` still present on 11700 after this PATCH (if child 8 shipped).
- `curl -sL https://kriskrug.co/ | grep -o '<title>[^<]*'` equals the pre-write snapshot (this child must not drift it).
- Minimal-diff on 12653, 12030, 11700 only.

## Verification

```bash
curl -s -o /dev/null -w '%{http_code}\n' -L https://kriskrug.co/speaking/
curl -s -o /dev/null -w '%{http_code}\n' -L https://kriskrug.co/about/
curl -s -o /dev/null -w '%{http_code}\n' -L https://kriskrug.co/glossary/

curl -sL "https://kriskrug.co/2026/07/31/ai-lands-inside-every-profession/?cb=$RANDOM" | grep -F 'I give a talk about exactly this'
curl -sL "https://kriskrug.co/2026/06/26/canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one/?cb=$RANDOM" | grep -F 'why I keep saying this out loud'
curl -sL "https://kriskrug.co/2026/05/04/punk-rock-ai/?cb=$RANDOM" | grep -F 'plain definitions for the words in here'

# Title owner is theme, not this child. Snapshot only.
curl -sL https://kriskrug.co/ | grep -o '<title>[^<]*'
```

## Agent Instructions

- Wait for child 4 on 12030 and child 8 on 11700. Re-snapshot those posts immediately before your PATCH so you merge onto current `content.raw`.
- Confirm 12653 slug `ai-lands-inside-every-profession`.
- On 11700, insert at the first term of art in the early body, not in the closing MBO paragraph.
- On 12030, insert in the closing paragraph, not in the compute-cost paragraph child 4 used.
- Leave 11879 as the model. Do not "complete" it.
- Do not edit `theme/kk-aurora/functions.php`. If a title bug is visible, file a note on #756 / parent #402 rather than expanding this child.
- Do not close #402.

### Data rows 31-33

| # | source_url | target_url | anchor_text | section_hint |
|---|---|---|---|---|
| 31 | `https://kriskrug.co/2026/07/31/ai-lands-inside-every-profession/` | `https://kriskrug.co/speaking/` | I give a talk about exactly this | Closing section, before the collection footer |
| 32 | `https://kriskrug.co/2026/06/26/canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one/` | `https://kriskrug.co/about/` | why I keep saying this out loud | Closing paragraph, before the collection footer |
| 33 | `https://kriskrug.co/2026/05/04/punk-rock-ai/` | `https://kriskrug.co/glossary/` | plain definitions for the words in here | Early body, first appearance of a term of art |

## Out of Scope

- Homepage title / umlaut / `document_title_parts` (Track B, #756).
- Jetpack `advanced_seo_title_formats` (plugin off; writes would no-op or 404).
- Page 3930 post-meta.
- Editing 11879.
- Schema Person markup (parent #402).
- `AGENTS.md` SEO guardrails (parent #402).
