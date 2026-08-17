# [CONTENT] Wire Most Benevolent Outcomes inbound and outbound links

**Parent:** [#402](https://github.com/WalksWithASwagger/kriskrug-wp/issues/402)
**Child:** 8 of 9
**Suggested labels:** `content`, `seo`, `needs-human-review`, `priority:medium`
**Lane:** Track A
**Research:** `content/drafts/2026-08-02-seo-authority-hubs/hub-plan.md` terms 1 and 2, `link-matrix.csv` data rows 1-6
**Blocked by:** child 1 (taxonomy; 3814 must leave `web-early-blog` first). After 01, parallel-safe with 02, 04, 06, 07. **Not** parallel with 09 on post 11700.

---

## Context

Terms `most benevolent outcome` and `most benevolent outcome prayer` share one hub: post **3814**. The ranking asset **is** the hub. PR #670 explicitly declined to build a spiritual landing page. 3814 is 33 blocks, includes the full prayer, and is the deepest on-domain treatment. It had no inbound links from anything published after 2023.

As of the 2026-08-02 research (and still true in the 2026-08-15 #339 live readback), 3814 had exactly two internal links, both auto-footer, one pointing at `/category/web-early-blog/`. Child 1 fixes the category/footer. This child adds four spokes in and two spokes out.

#328 (closed) and #339 (open) also talk about two copy-preserving inserts on 3814. Those live applies never happened. This child's six matrix rows are the apply-ready set. Re-read 3814 before writing. If a later #339 apply has already added worldview or `/ai-ethics/` sentences, skip the duplicate row rather than stacking.

Do not add a spiritual hub page.

## Owns (write)

- Page **3948** (`/the-kk-worldview/`) new paragraph after the "On Truth and Understanding" list (row 1).
- Post **11936** block 4 trailing sentence (row 2). Child 4 does not edit 11936.
- Post **11358** block 6 trailing sentence (row 3).
- Post **11700** final paragraph before footer (row 4). Only that MBO sentence. Child 9 later adds a `/glossary/` link earlier in 11700. Do not edit the early-body term-of-art paragraph here.
- Post **3814** trailing sentence in block 5 (row 5) and end of "Embracing the Digital Future" (row 6).

## Must not touch

- Category of 3814 (child 1). If 3814 still footers into `web-early-blog`, abort and send it back to child 1.
- Building `/most-benevolent-outcomes/` or any new page.
- Row 33 (11700 → `/glossary/`, child 9).
- `/about/` drink-data sentence (#249 / #339).
- Theme, schema, titles.

## Acceptance Criteria

- [ ] Child 1 has recategorized 3814. Rendered footer is the ethics collection, not `/category/web-early-blog/`.
- [ ] Page 3948 links 3814 with exact anchor `there is a prayer I actually say about this` (row 1).
- [ ] Post 11936 links 3814 with exact anchor `I say a prayer about this most mornings, which is either funny or the whole point` (row 2).
- [ ] Post 11358 links 3814 with exact anchor `I have my own version of the seance` (row 3).
- [ ] Post 11700 links 3814 with exact anchor `the optimistic version of the same argument` (row 4), in the final paragraph, not the glossary slot.
- [ ] Post 3814 links `/the-kk-worldview/` with exact anchor `the rest of my lens, written out plainly` (row 5).
- [ ] Post 3814 links `/ai-ethics/` with exact anchor `the less mystical version of this, which is how I actually practice it` (row 6), before the "How To Practice MBOs" heading.
- [ ] No new spiritual hub. Title of 3814 unchanged. No em dashes. Content-only snapshots.

## Tests/Evals

- `grep -F` all six exact anchors on cache-busted fetches.
- Internal link count on 3814: snapshot plus 2 (the two spokes out). Footer links may also have changed because of child 1; compare against a post-child-1 snapshot, not the 2026-08-02 count.
- 11700: MBO anchor present; do not require a `/glossary/` href from this child.
- Minimal-diff on 3948, 11936, 11358, 11700, 3814.

## Verification

```bash
curl -s "https://kriskrug.co/wp-json/wp/v2/posts/3814?_fields=id,slug,categories,link"
# categories must include 1678 (ai-ethics-philosophy), not rely on 1757 as primary

curl -sL "https://kriskrug.co/the-kk-worldview/?cb=$RANDOM" | grep -F 'there is a prayer I actually say about this'
curl -sL "https://kriskrug.co/2023/11/04/the-power-of-most-benevolent-outcomes-a-prayer-for-blessings-for-all-living-things/?cb=$RANDOM" | grep -F 'the rest of my lens, written out plainly'
curl -sL "https://kriskrug.co/2023/11/04/the-power-of-most-benevolent-outcomes-a-prayer-for-blessings-for-all-living-things/?cb=$RANDOM" | grep -F 'the less mystical version of this, which is how I actually practice it'
```

## Agent Instructions

- Re-count blocks on 3814, 11936, 11358. Insert by the quoted phrases in `hub-plan.md`, not by stale indexes alone.
- On 3948, add a new paragraph after the "On Truth and Understanding" `<ul>`, not inside the list.
- On 11700, row 4 goes in the **final** paragraph before the collection footer. Leave the early-body glossary slot for child 9.
- If #339 has already applied different 3814 inserts, keep those and only add missing matrix anchors. Do not revert #339 copy.
- Do not close #402. Do not close #339 from this work.

### Data rows 1-6

| # | source_url | target_url | anchor_text | section_hint |
|---|---|---|---|---|
| 1 | `https://kriskrug.co/the-kk-worldview/` | `https://kriskrug.co/2023/11/04/the-power-of-most-benevolent-outcomes-a-prayer-for-blessings-for-all-living-things/` | there is a prayer I actually say about this | On Truth and Understanding section, block 10, new paragraph after the list |
| 2 | `https://kriskrug.co/2026/05/23/you-cant-drink-data/` | `https://kriskrug.co/2023/11/04/the-power-of-most-benevolent-outcomes-a-prayer-for-blessings-for-all-living-things/` | I say a prayer about this most mornings, which is either funny or the whole point | Block 4, they-are-right-about-a-lot-of-it paragraph, trailing sentence |
| 3 | `https://kriskrug.co/2026/02/20/spa-at-the-end-of-time/` | `https://kriskrug.co/2023/11/04/the-power-of-most-benevolent-outcomes-a-prayer-for-blessings-for-all-living-things/` | I have my own version of the seance | Block 6, the astral-plane audio paragraph, trailing sentence |
| 4 | `https://kriskrug.co/2026/05/04/punk-rock-ai/` | `https://kriskrug.co/2023/11/04/the-power-of-most-benevolent-outcomes-a-prayer-for-blessings-for-all-living-things/` | the optimistic version of the same argument | Final paragraph, before the collection footer |
| 5 | `https://kriskrug.co/2023/11/04/the-power-of-most-benevolent-outcomes-a-prayer-for-blessings-for-all-living-things/` | `https://kriskrug.co/the-kk-worldview/` | the rest of my lens, written out plainly | Block 5, after the shared-with-me-by-a-friend line, trailing sentence |
| 6 | `https://kriskrug.co/2023/11/04/the-power-of-most-benevolent-outcomes-a-prayer-for-blessings-for-all-living-things/` | `https://kriskrug.co/ai-ethics/` | the less mystical version of this, which is how I actually practice it | Block 21, end of Embracing the Digital Future, before the How To Practice heading |

## Out of Scope

- New spiritual / optimism landing page.
- Recategorizing 3814 (child 1).
- Glossary link on 11700 (child 9).
- #328 / #339 publisher residue except skip-if-already-present.
- Encoding MBO tone into `AGENTS.md` (parent #402).
