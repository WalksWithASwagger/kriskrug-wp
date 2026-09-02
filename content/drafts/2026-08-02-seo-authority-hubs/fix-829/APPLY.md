# #829 APPLY: You Can't Drink Data on the /ai-ethics/ hub

**Applied and verified 2026-08-29.** The aggregate authenticated re-run is
idempotent: all four targets return `[SKIP]` and `[OK] nothing pending.` Script
remains dry-run by default. Do not reapply or extend this pack to #830-#834.

Parent: #402. This is child 4 of 9. Child 1 (#826) still owns the taxonomy pass. This pack does not recategorize or retitle anything.

Close #829 with the verified receipt. Keep parent #402 open.

## Applied receipt

KK approved the exact #829 live apply after the four-object authenticated dry
run. Page 12318 and posts 12030, 6144, and 11882 were applied one at a time.
Each write passed the #826 category gate, exact ID/slug check, mode-0600
pre-write snapshot, authenticated idempotency readback, public REST check,
cache-bypassed rendered check, ordinary cached-page check, and dry-run restore
preview. No rollback was applied.

Durable evidence:
[`docs/current-state/reports/issue-829-applied-20260829.md`](../../../../docs/current-state/reports/issue-829-applied-20260829.md).

## Pre-apply live reconfirm (logged-out public GET, 2026-08-19T23:23Z)

No REST POST / PATCH / DELETE in this session. `WP_USER` and `WP_APP_PASSWORD` were unset, so there is no fresh `context=edit` `content.raw` from this run. Public REST confirmed slug/ID pairs and snapshotted `content.rendered` into `before/`.

`content.raw` is present only where a historical authenticated snapshot still matches live `modified_gmt`:

| ID | Raw source | Matches live modified_gmt? |
|---|---|---|
| 12318 | `backup/20260701T202734Z-content-architecture/page-snapshots/page-12318-ai-ethics-after.json` | yes (`2026-07-01T20:27:51`) |
| 12030 | `backup/20260801-voice-sweep/canada-12030/after.json` | yes (`2026-08-01T19:57:26`) |
| 6144 | none | no raw fetched |
| 11882 | none. A 2026-06-23 draft snapshot exists with slug `both-hands-full-vancouver-ai-march-2026` and older `modified_gmt`. Not used. | no raw fetched |
| 11936 | read-only identity only. Body not snapshotted and not in the write set. | n/a |

| ID | Kind | Slug | URL | HTTP | Notes |
|---|---|---|---|---:|---|
| 12318 | page | `ai-ethics` | `/ai-ethics/` | 200 | Source trail = Punk Rock AI + RAP + archive. **No** You Can't Drink Data card. `you-cant-drink-data` href count = 0. |
| 12030 | post | `canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one` | `/2026/06/26/canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one/` | 200 | First compute paragraph ends `We lack consent architecture.` Body has **0** `/about/` hrefs (row 32 / #834 stays off this pack). No 11936 link. |
| 6144 | post | `ai-is-not-your-friend-why-we-need-to-rethink-our-relationship-with-artificial-intelligence` | `/2024/06/29/ai-is-not-your-friend-why-we-need-to-rethink-our-relationship-with-artificial-intelligence/` | 200 | Final paragraph ends `Peace out! ???`. One baked `kk-collection-footer`. No 11936 link. |
| 11882 | post | `we-trained-ai-on-stolen-work` | `/2026/05/19/we-trained-ai-on-stolen-work/` | 200 | Already has two 11936 hrefs under other anchors (`environmental cost` and the Related list). Exact row-10 guild anchor is **absent**. Skip rule is href+anchor, so this row still inserts. |
| 11936 | post | `you-cant-drink-data` | `/2026/05/23/you-cant-drink-data/` | 200 | Read-only. Already links BC AI, Punk Rock AI, Both Hands Full, Your Taste Is Your Moat. Do not edit. |

Four target URLs plus the hub post were 200. Public HTML greps matched the REST table: no new card, no three new anchors.

### Block recount (today's HTML, not the 2026-08-02 index)

Walking `p / h2 / h3 / ul / ol / figure / blockquote` is not how this pack inserts. Insertion is by **text match**:

- 12318: the existing Punk Rock AI Source trail card, not a stale card index.
- 12030: `We lack consent architecture.</p>` (first compute / infrastructure-cost paragraph). The closing `just a faster leak` paragraph is left for #834.
- 6144: `Peace out! ???</p>` immediately before `kk-collection-footer`.
- 11882: `training material without consent.</p>` (creative-labour paragraph).

Existing Punk Rock AI, RAP, and AI ethics archive cards stay. This is an insert, not a rebuild.

## Identity (slug check before any write)

Abort if any ID's live slug differs from `targets.json`. Never PATCH on ID alone.

| ID | Required slug |
|---:|---|
| 12318 | `ai-ethics` |
| 12030 | `canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one` |
| 6144 | `ai-is-not-your-friend-why-we-need-to-rethink-our-relationship-with-artificial-intelligence` |
| 11882 | `we-trained-ai-on-stolen-work` |

## What the script writes

Content only. Titles, slugs, dates, status, featured media, tags, categories, and SEO meta stay untouched.

| ID | Find (exactly once) | Inserted copy |
|---|---|---|
| 12318 | Punk Rock AI `<article class="aurora-media-card">` opener | new first card titled `You Can't Drink Data` (row 7), blurb exactly `A thousand people on Granville Street, and the AI guy standing in the middle of them.` |
| 12030 | `We lack consent architecture.</p>` | trailing sentence: exact anchor `what the water math looks like from street level` (row 8) |
| 6144 | `Peace out! ???</p>` | trailing sentence before the footer: exact anchor `two years later I went to the protest and wrote down what the signs said` (row 9) |
| 11882 | `training material without consent.</p>` | trailing sentence: exact anchor `the march where the illustrators showed up as a guild` (row 10) |

Inserted copy is ASCII. No em dashes. No NCR needed in the new sentences. Existing encoded apostrophes in 12030 / 6144 / 11882 stay as they are.

Skip a row if that exact `href` + anchor already exists.

## Must not

- Touch post 11936 body (no spoke out; already linked).
- Touch post 11929.
- Touch `/about/` (#249 / #339).
- Edit the 12030 closing paragraph (row 32 / #834).
- Add rows 1-6 (MBO) or the MBO sentence on 11936 (child 8 / #833).
- Duplicate `kk-collection-footer`.
- Rebuild the 12318 Source trail or drop the Punk Rock AI / RAP / archive cards.
- Run bulk `inject_links.py`.
- Mix theme, schema, or title edits.

## Shared-surface warnings

Page 12318 is also the topic-hub payload `content/source-packs/content-architecture-2026/wp-payloads/topic-hubs/ai-ethics.html`. That file is a full-page replacement **without** this card. If it is applied after these links land, it will wipe the card unless it is re-cut.

Post 12030 is also an #834 write surface (row 32, `/about/` in the closing
paragraph). Its #829 dependency is live, but #834 remains blocked on #833's
shared post-11700 write. Recut #834 after #833 is verified. Do not apply the
#834 `/about/` sentence in this pack.

## Commands

```bash
python3 -m unittest scripts.tests.test_apply_issue_829_ai_ethics_hub

# Offline dry-run: rewrite the snapshotted before-files into after/. No network.
python3 scripts/apply_issue_829_ai_ethics_hub.py --from-files

# Live GET dry-run: authenticated context=edit + printed diffs. No snapshot, no POST.
make varlock-run CMD='python3 scripts/apply_issue_829_ai_ethics_hub.py'

# Historical apply command. Do not rerun after the verified 2026-08-29 apply.
make varlock-run CMD='python3 scripts/apply_issue_829_ai_ethics_hub.py --apply'
```

`--item-id 12318` limits to one object. Re-run after a successful apply prints `[SKIP]`.

`--from-files` uses `before/*-content.raw.html` when present, else the public `before/*-content.rendered.html`. Live `--apply` always GETs `context=edit` `content.raw` and still requires the slug check.

`--apply` GETs the five #826 posts and aborts unless 3814 is out of 1757 into 1678, 3330 is out of 1757 into 1676, and 1067 / 1063 / 1147 are out of their wrong buckets into 1756.

Snapshot dir (mode 0700, files 0600):
`backup/issue-829-ai-ethics-hub/rest-<page|post>-<id>-before-<stamp>.json`

## Rollback

```bash
make varlock-run CMD='python3 scripts/apply_issue_829_ai_ethics_hub.py --restore backup/issue-829-ai-ethics-hub/rest-page-12318-before-<stamp>.json'
make varlock-run CMD='python3 scripts/apply_issue_829_ai_ethics_hub.py --restore backup/issue-829-ai-ethics-hub/rest-page-12318-before-<stamp>.json --apply'
```

Restore is dry-run by default. It refuses snapshots outside the four IDs or a slug mismatch. Rollback body is the snapshotted `content.raw`.

## After-apply logged-out gates

```bash
curl -s -o /dev/null -w '%{http_code}\n' -L https://kriskrug.co/ai-ethics/
curl -s -o /dev/null -w '%{http_code}\n' -L https://kriskrug.co/2026/05/23/you-cant-drink-data/
curl -s -o /dev/null -w '%{http_code}\n' -L https://kriskrug.co/2026/06/26/canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one/
curl -s -o /dev/null -w '%{http_code}\n' -L https://kriskrug.co/2024/06/29/ai-is-not-your-friend-why-we-need-to-rethink-our-relationship-with-artificial-intelligence/
curl -s -o /dev/null -w '%{http_code}\n' -L https://kriskrug.co/2026/05/19/we-trained-ai-on-stolen-work/

curl -sL "https://kriskrug.co/ai-ethics/?cb=$RANDOM" | grep -n 'you-cant-drink-data'
curl -sL "https://kriskrug.co/ai-ethics/?cb=$RANDOM" | grep -F "You Can't Drink Data"
curl -sL "https://kriskrug.co/ai-ethics/?cb=$RANDOM" | grep -F 'A thousand people on Granville Street, and the AI guy standing in the middle of them.'
# You Can't Drink Data card must appear before the Punk Rock AI card

curl -sL "https://kriskrug.co/2026/06/26/canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one/?cb=$RANDOM" \
  | grep -F 'what the water math looks like from street level'
# 12030 closing paragraph must still have no /about/ from this child
curl -sL "https://kriskrug.co/2026/06/26/canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one/?cb=$RANDOM" \
  | grep -F 'just a faster leak'

curl -sL "https://kriskrug.co/2024/06/29/ai-is-not-your-friend-why-we-need-to-rethink-our-relationship-with-artificial-intelligence/?cb=$RANDOM" \
  | grep -F 'two years later I went to the protest and wrote down what the signs said'
curl -sL "https://kriskrug.co/2026/05/19/we-trained-ai-on-stolen-work/?cb=$RANDOM" \
  | grep -F 'the march where the illustrators showed up as a guild'

# footer count on 6144 must match the pre-write snapshot (1 rendered hit)
curl -sL "https://kriskrug.co/2024/06/29/ai-is-not-your-friend-why-we-need-to-rethink-our-relationship-with-artificial-intelligence/?cb=$RANDOM" \
  | grep -c 'kk-collection-footer'
```

Expect: 12318 Source trail gains exactly one new 11936 card, still ahead of Punk Rock AI. 12030 / 6144 / 11882 each gain the named anchor once. 12030 closing paragraph unchanged. 6144 footer count unchanged. 11882 keeps its two older 11936 hrefs.

## Out of payload

- Taxonomy repair on 3814 / 3330 / 1067 / 1063 / 1147 / 2819 (#826)
- Photography hub wiring (#827)
- Post 1210 checklist rewrite (#828)
- Cyber Love Garden / Matt McKenna / meetup / MBO / brand-nav children (#830-#834)
- `/about/` sentence on 12030 (#834)
- Spoke out from 11936
- `inject_links.py`
