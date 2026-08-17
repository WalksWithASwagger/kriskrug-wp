# [CONTENT] Add Cyber Love Garden to the /ai-for-creatives/ hub

**Parent:** [#402](https://github.com/WalksWithASwagger/kriskrug-wp/issues/402)
**Child:** 5 of 9
**Suggested labels:** `content`, `seo`, `needs-human-review`, `priority:medium`
**Lane:** Track A
**Research:** `content/drafts/2026-08-02-seo-authority-hubs/hub-plan.md` term 8, `link-matrix.csv` data rows 26-29
**Blocked by:** child 1 (taxonomy, and the 2819 href repair). After 01, do not PATCH 2819 until row 30 is live.

---

## Context

`cyber love garden` is a distinctive term with no meaningful competition. Post **2650** (`/2023/05/30/the-cyber-love-garden-a-crossroads-of-art-and-ai-at-otherworld/`) is the owner: Otherworld burn, XR garden, Midjourney 5.1 prompts in captions. It is already in `ai-creatives` and already footers into `/ai-for-creatives/`.

The hub does not return the favour. Page **12316** (`/ai-for-creatives/`) links Both Hands Full and Your Taste Is Your Moat and nothing else in that "Read next" slot.

This child adds the hub card plus three inbound spokes. The dead `kriskrug.com/contact` href on post 2819 is **not** this child's job (child 1, row 30). This child only adds the garden sentence on 2819 (row 27). If child 1 has not repaired the href yet, wait; do not combine the repair into this PATCH.

## Owns (write)

- Page **12316** Read next card (row 26).
- Post **2819** trailing sentence to 2650 (row 27) only.
- Post **2661** trailing sentence (row 28).
- Post **3567** intro trailing sentence (row 29).

## Must not touch

- Row 30 (contact href on 2819).
- Post 2650 body (no spoke out required).
- Both Hands Full / Taste Is Your Moat cards on 12316: keep them.
- Theme, schema, titles.

## Acceptance Criteria

- [ ] Child 1's 2819 href repair is live before this child PATCHes 2819.
- [ ] Page 12316 has a Read next card titled `The Cyber Love Garden` linking 2650. Card blurb exactly: `Art, AI, and XR in a burn camp built for it.`
- [ ] Post 2819 links 2650 with exact anchor `the garden where we ran this in person` (row 27).
- [ ] Post 2661 links 2650 with exact anchor `what we built at Otherworld` (row 28).
- [ ] Post 3567 links 2650 with exact anchor `a worked example of all of this` (row 29).
- [ ] 2819 still has no `kriskrug.com/contact` href after this PATCH (do not regress child 1).
- [ ] Content-only, snapshots, no em dashes, no duplicate footers.

## Tests/Evals

- `grep -F 'The Cyber Love Garden'` on cache-busted `/ai-for-creatives/` and confirm href is 2650.
- `grep -F` the three spoke anchors.
- On 2819 after apply: garden anchor present AND `kriskrug.com/contact` absent.
- Minimal-diff: four inserts only.

## Verification

```bash
curl -s -o /dev/null -w '%{http_code}\n' -L https://kriskrug.co/ai-for-creatives/
curl -s -o /dev/null -w '%{http_code}\n' -L https://kriskrug.co/2023/05/30/the-cyber-love-garden-a-crossroads-of-art-and-ai-at-otherworld/

curl -sL "https://kriskrug.co/ai-for-creatives/?cb=$RANDOM" | grep -n 'cyber-love-garden'
curl -sL "https://kriskrug.co/2023/08/16/exquisite-corpse-collaborative-ai-art-experiment-on-discord-w-midjourney-zoom-out/?cb=$RANDOM" | grep -F 'the garden where we ran this in person'
curl -sL "https://kriskrug.co/2023/08/16/exquisite-corpse-collaborative-ai-art-experiment-on-discord-w-midjourney-zoom-out/?cb=$RANDOM" | grep -c 'kriskrug.com/contact'   # 0
```

## Agent Instructions

- Confirm page 12316 slug `ai-for-creatives` and post 2650 slug. Match existing Read next card markup.
- On 2819, insert row 27 on the Discord-experiment paragraph. Do not retouch the contact href except to abort if child 1's repair is missing.
- Skip a row if the exact href already exists.
- Do not close #402.

### Data rows 26-29

| # | source_url | target_url | anchor_text | section_hint |
|---|---|---|---|---|
| 26 | `https://kriskrug.co/ai-for-creatives/` | `https://kriskrug.co/2023/05/30/the-cyber-love-garden-a-crossroads-of-art-and-ai-at-otherworld/` | The Cyber Love Garden | Read next section, new card |
| 27 | `https://kriskrug.co/2023/08/16/exquisite-corpse-collaborative-ai-art-experiment-on-discord-w-midjourney-zoom-out/` | `https://kriskrug.co/2023/05/30/the-cyber-love-garden-a-crossroads-of-art-and-ai-at-otherworld/` | the garden where we ran this in person | Discord experiment paragraph, trailing sentence |
| 28 | `https://kriskrug.co/2023/07/06/headed-to-burning-man-shambhala-or-coachella-ignite-your-festival-persona/` | `https://kriskrug.co/2023/05/30/the-cyber-love-garden-a-crossroads-of-art-and-ai-at-otherworld/` | what we built at Otherworld | Body, trailing sentence |
| 29 | `https://kriskrug.co/2023/10/15/community-art-project-development-process-guide/` | `https://kriskrug.co/2023/05/30/the-cyber-love-garden-a-crossroads-of-art-and-ai-at-otherworld/` | a worked example of all of this | Intro paragraph, trailing sentence |

## Out of Scope

- Contact-link repair (child 1).
- New hub page. Wire 12316.
- Recategorizing 1147 (child 1).
