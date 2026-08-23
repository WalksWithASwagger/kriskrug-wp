# #830 APPLY: Cyber Love Garden hub links

**Prepared, not applied. Do not PATCH until KK says go.**
Script is dry-run by default. `--apply` is the only write switch, and it refuses unless #826's post 2819 contact-href repair is already live (no `kriskrug.com/contact`).

Parent: #402. This is child 5 of 9. Child 1 (#826) still owns the 2819 contact-href repair (row 30). This pack does not recategorize anything and does not retouch that href except to abort if the repair is missing.

Do not close #830 or #402 when this runbook merges.

## Live reconfirm (logged-out public REST, 2026-08-19T23:21:16Z)

No REST POST / PATCH / DELETE in this session. WP creds were unset, so there is no authenticated `context=edit` `content.raw`. Public REST confirmed slug/ID pairs and snapshotted `content.rendered` into `before/`. Page 12316 `content.raw.html` is the 2026-07-01 topic-hub source pack, which still matches live rendered except WordPress adding `decoding="async"` on `<img>`.

| ID | Kind | Slug | URL | HTTP | Internal body links | Notes |
|---|---|---|---|---:|---:|---|
| 12316 | page | `ai-for-creatives` | `/ai-for-creatives/` | 200 | 5 (Both Hands Full, Taste Is Your Moat, archive, services, speaking) | No Cyber Love Garden card. `modified_gmt` `2026-07-01T20:27:40`. |
| 2819 | post | `exquisite-corpse-collaborative-ai-art-experiment-on-discord-w-midjourney-zoom-out` | `/2023/08/16/exquisite-corpse-collaborative-ai-art-experiment-on-discord-w-midjourney-zoom-out/` | 200 | 3 (contact + footer) | No link to 2650. `https://kriskrug.co/contact/` is live. `kriskrug.com/contact` is absent. `modified_gmt` `2026-08-18T02:16:05`. |
| 2661 | post | `headed-to-burning-man-shambhala-or-coachella-ignite-your-festival-persona` | `/2023/07/06/headed-to-burning-man-shambhala-or-coachella-ignite-your-festival-persona/` | 200 | 2 (footer only) | No link to 2650. One baked `kk-collection-footer`. |
| 3567 | post | `community-art-project-development-process-guide` | `/2023/10/15/community-art-project-development-process-guide/` | 200 | 2 (footer only) | No link to 2650. Intro is still the italic technology-brings-people-together paragraph. |
| 2650 | post | `the-cyber-love-garden-a-crossroads-of-art-and-ai-at-otherworld` | `/2023/05/30/the-cyber-love-garden-a-crossroads-of-art-and-ai-at-otherworld/` | 200 | footer into `/ai-for-creatives/` | Destination only. Do not PATCH this body. Featured media 2654. |

Five target URLs were 200: `/ai-for-creatives/`, the three spoke posts, and post 2650. `/contact/` was also 200.

### #826 row 30 on 2819 (today)

Public rendered has `href="https://kriskrug.co/contact/"` and zero `kriskrug.com/contact`. That is the #826 repair this child must not redo and must not regress. `--apply` still GETs 2819 and aborts if the dead href is back or the repaired href is missing.

### Block recount (today's HTML, not the 2026-08-02 index)

Insertion is by **text match**, not a stale block index.

- 12316: insert a Read next card after Taste Is Your Moat and before the AI creatives archive card. Both Hands Full and Taste cards stay byte-identical.
- 2819: Discord-experiment paragraph that ends `glimpse into our journey.` Do not touch the contact paragraph.
- 2661: closing body line `See you on the dance floor!` before the baked footer.
- 3567: intro paragraph that ends `the communal experience can be the message.`

## Identity (slug check before any write)

Abort if any ID's live slug differs from `targets.json`. Never PATCH on ID alone.

| ID | Required slug |
|---:|---|
| 12316 | `ai-for-creatives` |
| 2819 | `exquisite-corpse-collaborative-ai-art-experiment-on-discord-w-midjourney-zoom-out` |
| 2661 | `headed-to-burning-man-shambhala-or-coachella-ignite-your-festival-persona` |
| 3567 | `community-art-project-development-process-guide` |
| 2650 | `the-cyber-love-garden-a-crossroads-of-art-and-ai-at-otherworld` (read-only destination) |

## What the script writes

Content only. Titles, slugs, dates, status, featured media, tags, categories, and SEO meta stay untouched.

| ID | Find (exactly once) | Inserted copy |
|---|---|---|
| 12316 | Taste card close, then the archive card open | new Read next card titled `The Cyber Love Garden` linking 2650. Blurb exactly: `Art, AI, and XR in a burn camp built for it.` (row 26) |
| 2819 | Discord experiment paragraph ending `glimpse into our journey.` | trailing sentence: exact anchor `the garden where we ran this in person` (row 27) |
| 2661 | `See you on the dance floor!</p>` | trailing sentence: exact anchor `what we built at Otherworld` (row 28) |
| 3567 | intro ending `the communal experience can be the message.` | trailing sentence: exact anchor `a worked example of all of this` (row 29) |

Inserted copy is ASCII. No em dashes. No NCR needed in the new sentences. Existing NCRs and unicode in 2819 / 2661 / 3567 stay as they are.

Skip a row if that exact `href` + anchor already exists.

## Snapshot gaps

- No authenticated `content.raw` for 2819, 2661, or 3567. `before/post-*-content.raw.html` is the public `content.rendered` stand-in so `--from-files` can run offline. Live `--apply` must GET `context=edit` and will abort if the find needle is missing in raw.
- Page 12316 raw is reconstructed from `content/source-packs/content-architecture-2026/wp-payloads/topic-hubs/ai-for-creatives.html`, not from `context=edit`.
- Post 2650 body is not snapshotted as a write target.

## Must not

- Repair or rewrite the 2819 contact href (row 30 / #826). Abort if that repair is not live.
- Touch post 2650 body.
- Recategorize 1147 or any other post.
- Remove or rewrite the Both Hands Full or Taste Is Your Moat cards on 12316.
- Duplicate `kk-collection-footer`.
- Run bulk `inject_links.py`.

## Source-pack write-surface warning

Page 12316 is also the topic-hub payload at `content/source-packs/content-architecture-2026/wp-payloads/topic-hubs/ai-for-creatives.html`. That file does **not** include this garden card. If that payload is applied after these links land, it will wipe the card unless it is re-cut.

## Commands

```bash
python3 -m unittest scripts.tests.test_apply_issue_830_cyber_love_garden

# Offline dry-run: rewrite the snapshotted before-files into after/. No network.
python3 scripts/apply_issue_830_cyber_love_garden.py --from-files

# Live GET dry-run: authenticated context=edit + printed diffs. No snapshot, no POST.
make varlock-run CMD='python3 scripts/apply_issue_830_cyber_love_garden.py'

# Apply only after #826 2819 contact repair is live and KK approves that diff.
make varlock-run CMD='python3 scripts/apply_issue_830_cyber_love_garden.py --apply'
```

`--item-id 12316` limits to one object. Re-run after a successful apply prints `[SKIP]`.

`--apply` GETs post 2819 and aborts unless `kriskrug.com/contact` is absent and `https://kriskrug.co/contact/` is present.

Snapshot dir (mode 0700, files 0600):
`backup/issue-830-cyber-love-garden/rest-<page|post>-<id>-before-<stamp>.json`

## Rollback

```bash
make varlock-run CMD='python3 scripts/apply_issue_830_cyber_love_garden.py --restore backup/issue-830-cyber-love-garden/rest-page-12316-before-<stamp>.json'
make varlock-run CMD='python3 scripts/apply_issue_830_cyber_love_garden.py --restore backup/issue-830-cyber-love-garden/rest-page-12316-before-<stamp>.json --apply'
```

Restore is dry-run by default. It refuses snapshots outside the four write IDs or a slug mismatch. Rollback body is the snapshotted `content.raw`.

## After-apply logged-out gates

```bash
curl -s -o /dev/null -w '%{http_code}\n' -L https://kriskrug.co/ai-for-creatives/
curl -s -o /dev/null -w '%{http_code}\n' -L https://kriskrug.co/2023/05/30/the-cyber-love-garden-a-crossroads-of-art-and-ai-at-otherworld/
curl -s -o /dev/null -w '%{http_code}\n' -L https://kriskrug.co/2023/08/16/exquisite-corpse-collaborative-ai-art-experiment-on-discord-w-midjourney-zoom-out/
curl -s -o /dev/null -w '%{http_code}\n' -L https://kriskrug.co/2023/07/06/headed-to-burning-man-shambhala-or-coachella-ignite-your-festival-persona/
curl -s -o /dev/null -w '%{http_code}\n' -L https://kriskrug.co/2023/10/15/community-art-project-development-process-guide/

curl -sL "https://kriskrug.co/ai-for-creatives/?cb=$RANDOM" | grep -F 'The Cyber Love Garden'
curl -sL "https://kriskrug.co/ai-for-creatives/?cb=$RANDOM" | grep -F 'Art, AI, and XR in a burn camp built for it.'
curl -sL "https://kriskrug.co/ai-for-creatives/?cb=$RANDOM" | grep -c 'both-hands-full'
curl -sL "https://kriskrug.co/ai-for-creatives/?cb=$RANDOM" | grep -c 'your-taste-is-your-moat'

curl -sL "https://kriskrug.co/2023/08/16/exquisite-corpse-collaborative-ai-art-experiment-on-discord-w-midjourney-zoom-out/?cb=$RANDOM" \
  | grep -F 'the garden where we ran this in person'
curl -sL "https://kriskrug.co/2023/08/16/exquisite-corpse-collaborative-ai-art-experiment-on-discord-w-midjourney-zoom-out/?cb=$RANDOM" \
  | grep -c 'kriskrug.com/contact'
# last command must print 0

curl -sL "https://kriskrug.co/2023/07/06/headed-to-burning-man-shambhala-or-coachella-ignite-your-festival-persona/?cb=$RANDOM" \
  | grep -F 'what we built at Otherworld'
curl -sL "https://kriskrug.co/2023/10/15/community-art-project-development-process-guide/?cb=$RANDOM" \
  | grep -F 'a worked example of all of this'
```

Expect: 12316 gains one new Read next card (2650) and still has Both Hands Full and Taste Is Your Moat. 2819 garden anchor present and `kriskrug.com/contact` absent. 2661 and 3567 footer counts unchanged.

## Out of payload

- Contact-link repair on 2819 (#826 row 30)
- Taxonomy repair on 1067 / 1063 / 1147 / 3814 / 3330 (#826)
- Post 2650 body
- Hub cards on 12013 / 12318 / 12319
- `inject_links.py`
