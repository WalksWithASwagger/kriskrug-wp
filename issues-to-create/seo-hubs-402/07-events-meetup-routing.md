# [CONTENT] Route Vancouver AI meetup recaps to /events/

**Parent:** [#402](https://github.com/WalksWithASwagger/kriskrug-wp/issues/402)
**Child:** 7 of 9
**Suggested labels:** `content`, `seo`, `needs-human-review`, `priority:medium`
**Lane:** Track A
**Research:** `content/drafts/2026-08-02-seo-authority-hubs/hub-plan.md` term 6, `link-matrix.csv` data rows 18-25
**Blocked by:** child 1 (taxonomy). After 01, parallel-safe with 02, 04, 05, 06, 08.

---

## Context

This is the healthiest #402 cluster with one clean gap. Nine Vancouver AI meetup recap posts exist. Six checked in PR #670 already link to `/vancouver-ai/` (page 12315). **None** linked to `/events/` (page **2250**), which is the page that carries the live registration card.

Someone searching `vancouver ai community meetup` wants the next one. Recaps currently send them to a topic hub instead of the calendar.

PR #670 saw the live card as: "Wed, Sept 30, Space Centre, Vancouver AI Community Meetup, Register on Luma." Re-read `/events/` on apply day. If that card has moved or expired, keep the `/events/` href (the page stays the current calendar) and do not hard-code a stale date in the new sentences. The matrix anchors already avoid dates ("the next one", "the current calendar").

**Do not write page 2250.** #635 is the only issue allowed to mutate the events catalog, event media, or page 2250. This child only points **at** `/events/`.

Post **4348** (2023 directory, 60 external links, no date-proofing) matters most: put the live calendar link high in the intro, ahead of the 2023-era external list.

## Owns (write)

- Posts **4495, 9197, 8418, 6815, 6251, 5768, 4348**: one `/events/` link each (rows 18-24).
- Page **12315** (`/vancouver-ai/`): add `the calendar` as a **second** link on the Events and recaps card, block 11, beside the existing "Browse AI events" → `/ai-events/` link. Do not replace that archive link (row 25).

## Must not touch

- Page **2250** body, Luma embed, registration card, event media (#635).
- Existing `/vancouver-ai/` links on the recap posts: keep them. This child adds `/events/`, it does not swap destinations.
- Theme, schema, titles.

## Acceptance Criteria

- [ ] Each of the seven recap posts contains a link to `https://kriskrug.co/events/` with the exact matrix anchor for that row, placed before the collection footer (4348: intro, not footer).
- [ ] Page 12315 Events and recaps card links `/events/` with exact anchor `the calendar` **and** still links `/ai-events/` (or the existing "Browse AI events" href). Two links, not a replacement.
- [ ] Page 2250 `content.raw` is bit-identical to the pre-session snapshot.
- [ ] No recap title or date in the new sentences that can rot (no "Sept 30" in inserted copy).
- [ ] Content-only, snapshots, no em dashes, no duplicate footers.

## Tests/Evals

- For each of the seven recap permalinks: `grep -c '/events/'` increases by 1 versus snapshot (4348 may already mention events in external lists; assert the **new** exact anchor is present).
- `grep -F 'the calendar'` on cache-busted `/vancouver-ai/` and confirm href `/events/`.
- `diff` of page 2250 snapshot vs post-session fetch is empty.
- Minimal-diff on the eight owned bodies.

## Verification

```bash
curl -s -o /dev/null -w '%{http_code}\n' -L https://kriskrug.co/events/
curl -s -o /dev/null -w '%{http_code}\n' -L https://kriskrug.co/vancouver-ai/

# Re-read the live card (do not copy dates into new copy)
curl -sL "https://kriskrug.co/events/?cb=$RANDOM" | grep -i -n 'luma\|register\|meetup' | head

curl -sL "https://kriskrug.co/2023/12/27/2024-vancouver-ai-community-meetups/?cb=$RANDOM" | grep -F 'the live calendar, which is the version that stays current'
curl -sL "https://kriskrug.co/vancouver-ai/?cb=$RANDOM" | grep -F 'the calendar'
```

## Agent Instructions

- Snapshot page 2250 first so you can prove you did not write it.
- Re-fetch each recap by ID. Confirm slugs in the table. Insert before `kk-collection-footer` except 4348 (intro).
- On 12315, add the calendar link next to the existing events-archive link in the Events and recaps card. If that card has been redesigned, find the "Browse AI events" href by text, not by block 11 alone.
- Skip a row if that exact `/events/` href + anchor already exists.
- Do not close #402.

### Data rows 18-25

| # | source_url | target_url | anchor_text | section_hint |
|---|---|---|---|---|
| 18 | `https://kriskrug.co/2024/01/28/inside-the-innaugural-vancouver-ai-community-meetup/` | `https://kriskrug.co/events/` | we still do this every month, and the next one is on the calendar | Final paragraph, before the collection footer |
| 19 | `https://kriskrug.co/2025/05/11/vancouver-ai-meetup-16-where-tech-creativity-and-community-collide/` | `https://kriskrug.co/events/` | the next one | Final paragraph, before the collection footer |
| 20 | `https://kriskrug.co/2025/03/02/vancouver-ai-the-community-building-bcs-ai-future-february-meetup-recap/` | `https://kriskrug.co/events/` | come to the next one | Final paragraph, before the collection footer |
| 21 | `https://kriskrug.co/2024/09/01/august-vancouver-ai-community-meetup-recap-hackers-hustlers-heretics/` | `https://kriskrug.co/events/` | the current calendar | Final paragraph, before the collection footer |
| 22 | `https://kriskrug.co/2024/07/08/creativity-in-the-age-of-ai-vancouver-ai-community-meetup-june-2024-highlights/` | `https://kriskrug.co/events/` | where the next one lands | Final paragraph, before the collection footer |
| 23 | `https://kriskrug.co/2024/06/02/june-vancouver-ai-community-meetup-recap-a-confluence-of-minds-and-machines/` | `https://kriskrug.co/events/` | still monthly, still free, still worth the trip | Final paragraph, before the collection footer |
| 24 | `https://kriskrug.co/2023/12/27/2024-vancouver-ai-community-meetups/` | `https://kriskrug.co/events/` | the live calendar, which is the version that stays current | Intro section, high in the post, ahead of the 2023-era external link list |
| 25 | `https://kriskrug.co/vancouver-ai/` | `https://kriskrug.co/events/` | the calendar | Events and recaps card, block 11, added beside the existing Browse AI events link |

## Out of Scope

- Editing `/events/` / page 2250 / Luma / event heroes (#635).
- Replacing `/vancouver-ai/` links with `/events/`.
- Recategorizing meetup posts.
- Schema Event markup (parent #402 schema lane).
