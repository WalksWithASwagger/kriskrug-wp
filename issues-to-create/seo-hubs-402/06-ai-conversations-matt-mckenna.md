# [CONTENT] Add Matt McKenna to the /ai-conversations/ hub

**Parent:** [#402](https://github.com/WalksWithASwagger/kriskrug-wp/issues/402)
**Child:** 6 of 9
**Suggested labels:** `content`, `seo`, `needs-human-review`, `priority:medium`
**Lane:** Track A
**Research:** `content/drafts/2026-08-02-seo-authority-hubs/hub-plan.md` term 5, `link-matrix.csv` data rows 15-17
**Blocked by:** child 1 (taxonomy; post 3330 is recategorized there). After 01, parallel-safe with 02, 04, 07.

---

## Context

`matt mckenna miami` is a person-entity query. The on-site answer is post **3183** (`/2023/09/22/coffee-community-and-sobriety-matt-mckennas-decade-at-dent/`): 18-block interview, DENT, sobriety, Imperial Moto Coffee in Miami in block 4.

Topic hub `/ai-conversations/` (page **12319**) does not link to it.

Post 3330 (`the-future-called-i-answered`) already links to 3183. Leave that link. Child 1 moves 3330 out of `web-early-blog` into `events-reports`; this child does not recategorize 3330 and does not add a second 3183 link there.

## Owns (write)

- Page **12319** interview-list card (row 15).
- Post **2833** inline name link (row 16).
- Post **2423** intro trailing sentence (row 17).

## Must not touch

- Post 3183 body (no spoke out in the matrix).
- Post 3330 (existing 3183 link; category is child 1).
- Other interview cards on 12319: this is an insert.
- Theme, schema, titles.

## Acceptance Criteria

- [ ] Page 12319 has an interview card titled `Matt McKenna's decade at DENT` linking 3183. Card blurb exactly: `Ten years of DENT, ten years sober, and a coffee shop in Miami.`
- [ ] Post 2833 links 3183 with exact anchor `Matt McKenna, who has been at every single one` as an **inline** link on the name in the DENT-community paragraph (row 16), not a bolted-on extra sentence if the name is already in that paragraph.
- [ ] Post 2423 links 3183 with exact anchor `I sat down with Matt McKenna a few years after this` (row 17).
- [ ] Post 3330 is not modified by this child.
- [ ] Content-only, snapshots, no em dashes, no duplicate footers.

## Tests/Evals

- `grep -n 'matt-mckennas-decade-at-dent'` on cache-busted `/ai-conversations/`.
- `grep -F` the two spoke anchors on 2833 and 2423.
- `git`/snapshot diff of 3330 is empty for this child's PR.
- Minimal-diff on 12319, 2833, 2423.

## Verification

```bash
curl -s -o /dev/null -w '%{http_code}\n' -L https://kriskrug.co/ai-conversations/
curl -s -o /dev/null -w '%{http_code}\n' -L https://kriskrug.co/2023/09/22/coffee-community-and-sobriety-matt-mckennas-decade-at-dent/

curl -sL "https://kriskrug.co/ai-conversations/?cb=$RANDOM" | grep -n 'matt-mckennas-decade-at-dent'
curl -sL "https://kriskrug.co/2023/08/19/dent-the-future-an-insiders-experiences-at-the-dent-conference/?cb=$RANDOM" | grep -F 'Matt McKenna, who has been at every single one'
```

## Agent Instructions

- Confirm page 12319 and post 3183 by ID/slug. Match existing interview-card markup on the hub.
- On 2833, prefer wrapping the existing name if it is already in the community paragraph. Only add words if the name is absent. The visible anchor text must match the matrix.
- Re-count intro blocks on 2423; insert by the intro paragraph, not a stale index.
- Skip a row if the exact href already exists (3330 is the known skip).
- Do not close #402.

### Data rows 15-17

| # | source_url | target_url | anchor_text | section_hint |
|---|---|---|---|---|
| 15 | `https://kriskrug.co/ai-conversations/` | `https://kriskrug.co/2023/09/22/coffee-community-and-sobriety-matt-mckennas-decade-at-dent/` | Matt McKenna's decade at DENT | Interview card list, new card |
| 16 | `https://kriskrug.co/2023/08/19/dent-the-future-an-insiders-experiences-at-the-dent-conference/` | `https://kriskrug.co/2023/09/22/coffee-community-and-sobriety-matt-mckennas-decade-at-dent/` | Matt McKenna, who has been at every single one | DENT community paragraph, inline on the name |
| 17 | `https://kriskrug.co/2019/03/30/dent-2019-photo-recap-gallery/` | `https://kriskrug.co/2023/09/22/coffee-community-and-sobriety-matt-mckennas-decade-at-dent/` | I sat down with Matt McKenna a few years after this | Intro paragraph, trailing sentence |

## Out of Scope

- Recategorizing 3330 (child 1).
- Adding a second 3183 link on 3330.
- Building a new conversations hub.
- Miami landing page or extra person-entity posts.
