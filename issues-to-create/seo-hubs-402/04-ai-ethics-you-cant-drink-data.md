# [CONTENT] Add You Can't Drink Data to the /ai-ethics/ hub

**Parent:** [#402](https://github.com/WalksWithASwagger/kriskrug-wp/issues/402)
**Child:** 4 of 9
**Suggested labels:** `content`, `seo`, `needs-human-review`, `priority:medium`
**Lane:** Track A
**Research:** `content/drafts/2026-08-02-seo-authority-hubs/hub-plan.md` term 3, `link-matrix.csv` data rows 7-10
**Blocked by:** child 1 (taxonomy). After 01, parallel-safe with 02, 06, 07, 08. **Not** parallel with 09 on post 12030.

---

## Context

Post **11936** (`/2026/05/23/you-cant-drink-data/`) is the on-site owner of `you cant drink data`: 60+ blocks, first-person, already linking out to BC AI, Punk Rock AI, Both Hands Full, and Your Taste Is Your Moat. The gap is inbound.

`/ai-ethics/` (page **12318**) is the topic hub. Its "Source trail" section links Punk Rock AI and the RAP certification, not the post that owns the term.

Companion post 11929 (`both-hands-full-at-the-data-center`) already links to 11936. Leave it.

Do **not** add the About-page "you can't drink data" sentence. That residue lives on #249 / #339, not in this matrix.

Do **not** add the MBO trailing sentence on 11936. That is child 8, data row 2.

## Owns (write)

- Page **12318** Source trail: new first card (row 7).
- Post **12030** trailing sentence on the first compute/infrastructure-cost paragraph (row 8). Only that sentence. Child 9 later adds an `/about/` sentence in the closing paragraph of the **same** post. Do not edit the closing paragraph here.
- Post **6144** final paragraph before footer (row 9).
- Post **11882** creative-labour paragraph trailing sentence (row 10).

## Must not touch

- Post 11936 body (no spoke out; already linked).
- Post 11929.
- `/about/` (#249 / #339).
- Rows 1-6 (MBO), row 32 (12030 → `/about/`, child 9).
- Schema, titles, theme.

## Acceptance Criteria

- [ ] Page 12318 Source trail has a first-position card titled `You Can't Drink Data` linking `https://kriskrug.co/2026/05/23/you-cant-drink-data/`, ahead of Punk Rock AI. Card blurb exactly: `A thousand people on Granville Street, and the AI guy standing in the middle of them.`
- [ ] Post 12030 links 11936 with exact anchor `what the water math looks like from street level` (row 8).
- [ ] Post 6144 links 11936 with exact anchor `two years later I went to the protest and wrote down what the signs said` (row 9).
- [ ] Post 11882 links 11936 with exact anchor `the march where the illustrators showed up as a guild` (row 10).
- [ ] Existing Source trail cards on 12318 remain. This is an insert, not a rebuild.
- [ ] 12030 closing paragraph has no new `/about/` link from this child.
- [ ] Content-only, slug/ID snapshots, no em dashes, no duplicate footers.

## Tests/Evals

- `grep -F 'You Can't Drink Data'` (or the HTML-escaped equivalent) on cache-busted `/ai-ethics/` and confirm the card href is 11936, and that it appears **before** the Punk Rock AI card.
- `grep -F` the three spoke anchors on 12030, 6144, 11882.
- `grep -c` of 11936 permalinks on 12318 increases by 1.
- Minimal-diff on all four bodies: only the new card/sentences.

## Verification

```bash
curl -s -o /dev/null -w '%{http_code}\n' -L https://kriskrug.co/ai-ethics/
curl -s -o /dev/null -w '%{http_code}\n' -L https://kriskrug.co/2026/05/23/you-cant-drink-data/

curl -sL "https://kriskrug.co/ai-ethics/?cb=$RANDOM" | grep -n 'you-cant-drink-data'
curl -sL "https://kriskrug.co/2026/06/26/canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one/?cb=$RANDOM" | grep -F 'what the water math looks like from street level'
```

## Agent Instructions

- `GET` page 12318 and posts 12030, 6144, 11882, 11936 (11936 read-only). Confirm slugs.
- Re-find the Source trail by the existing Punk Rock AI card, not by a stale block index.
- Match the existing card HTML pattern on 12318. Do not invent a new card component.
- On 12030, insert row 8 on the first paragraph that raises compute or infrastructure cost. Leave the closing paragraph for child 9.
- Skip any row whose exact href already exists.
- Do not close #402.

### Data rows 7-10

| # | source_url | target_url | anchor_text | section_hint |
|---|---|---|---|---|
| 7 | `https://kriskrug.co/ai-ethics/` | `https://kriskrug.co/2026/05/23/you-cant-drink-data/` | You Can't Drink Data | Source trail section, new first card ahead of Punk Rock AI |
| 8 | `https://kriskrug.co/2026/06/26/canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one/` | `https://kriskrug.co/2026/05/23/you-cant-drink-data/` | what the water math looks like from street level | First paragraph that raises compute or infrastructure cost, trailing sentence |
| 9 | `https://kriskrug.co/2024/06/29/ai-is-not-your-friend-why-we-need-to-rethink-our-relationship-with-artificial-intelligence/` | `https://kriskrug.co/2026/05/23/you-cant-drink-data/` | two years later I went to the protest and wrote down what the signs said | Final paragraph, before the collection footer |
| 10 | `https://kriskrug.co/2026/05/19/we-trained-ai-on-stolen-work/` | `https://kriskrug.co/2026/05/23/you-cant-drink-data/` | the march where the illustrators showed up as a guild | Creative labour paragraph, trailing sentence |

## Out of Scope

- Spoke out from 11936 (already done).
- About-page backlink (#249 / #339).
- MBO sentence on 11936 (child 8).
- `/about/` link on 12030 (child 9).
- Building a new ethics hub page. Wire the one that shipped.
