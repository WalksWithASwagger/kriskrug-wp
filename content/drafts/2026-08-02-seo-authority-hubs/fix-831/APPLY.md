# #831 APPLY: Matt McKenna hub links

**Prepared, not applied. Do not PATCH until #826 is live and KK says go.**
Script is dry-run by default. `--apply` is the only write switch, and it refuses unless the five #826 category fixes are already live (3330 out of `web-early-blog` / 1757 into `events-reports` / 1676).

Parent: #402. This is child 6 of 9. Child 1 (#826) owns the 3330 recategorization. This pack does not recategorize 3330 and does not add a second 3183 link there.

Do not close #831 or #402 when this runbook merges.

## Live reconfirm (logged-out public REST + HTML GET, 2026-08-19T23:20Z)

No REST POST / PATCH / DELETE in this session. WP creds were unset, so there is no authenticated `context=edit` `content.raw`. Public REST confirmed slug/ID pairs. Snapshots in `before/` are public `content.rendered` plus a reconstructed 12319 raw from the 2026-07-01 architecture payload.

| ID | Kind | Slug | URL | HTTP | Internal body links | Notes |
|---|---|---|---|---:|---:|---|
| 12319 | page | `ai-conversations` | `/ai-conversations/` | 200 | **6** (none to 3183) | Three `aurora-media-card`s. Cache-busted HTML has **0** `matt-mckennas-decade-at-dent`. `modified_gmt` `2026-07-01T20:28:05`. |
| 2833 | post | `dent-the-future-an-insiders-experiences-at-the-dent-conference` | `/2023/08/19/dent-the-future-an-insiders-experiences-at-the-dent-conference/` | 200 | 3 (1 body + footer pair) | Community paragraph already has Instagram `Matt McKenna`. No 3183 href. One `kk-collection-footer`. |
| 2423 | post | `dent-2019-photo-recap-gallery` | `/2019/03/30/dent-2019-photo-recap-gallery/` | 200 | 2 (footer only) | Intro is block 1 of 25. Name also appears later in a figure caption. No 3183 href. One footer. |
| 3183 | post | `coffee-community-and-sobriety-matt-mckennas-decade-at-dent` | `/2023/09/22/coffee-community-and-sobriety-matt-mckennas-decade-at-dent/` | 200 | 2 (footer to hub) | **Do not touch.** No spoke out. Featured media 3232. |
| 3330 | post | `the-future-called-i-answered` | `/2023/09/29/the-future-called-i-answered/` | 200 | 6 including 3183 | **Do not touch.** Existing 3183 link stays. Categories already `[1676]`. |

Five target URLs were 200: `/ai-conversations/`, the 3183 interview, 2833, 2423, and 3330.

### #826 gate readback (public categories, not a write)

Public REST on 2026-08-19 already shows the five #826 category moves: 3814 in 1678, **3330 in 1676 and out of 1757**, 1067 / 1063 / 1147 in 1756. The `--apply` gate would pass on that evidence. This pack is still **not applied**. KK still has to approve the diff.

### Block recount (today's HTML, not the 2026-08-02 index)

Walking `p / h2 / h3 / ul / ol / figure / blockquote` in `content.rendered`:

- 12319 is a single HTML payload. The interview list is the "Listen and read" `aurora-proof-grid`. Insert the new card **before** the Conversations archive card, by text match on that archive href, not a card index.
- 2833 community paragraph sits under `Connections and Community: More Than a Conference`. The name is already there, Instagram-linked. Wrap and expand that existing name. Do not add a second sentence.
- 2423 intro is **block 1** (`Just back from Sante Fe... friends and collaborators.`). There is no stale "block 17". Insert the trailing sentence in that intro paragraph.

Featured media 3232 is a wide banner whose filename contains a non-ASCII multiply sign. The card uses ASCII `image-12.png` from the 3183 body instead, same Photon `resize=640,400` pattern as the other hub cards.

## Snapshot gaps

- **No `content.raw` from live REST.** Public `context=view` omits it. Authenticated `context=edit` was not available.
- Page **12319** `before/page-12319-content.raw.html` is reconstructed from `content/source-packs/content-architecture-2026/wp-payloads/topic-hubs/ai-conversations.html`. Public rendered matches that structure (WP only added `decoding="async"`, self-closing `img`, and `&#8217;`).
- Posts **2833** and **2423** `content.raw.html` files are public `content.rendered` stand-ins. Live `--apply` re-fetches `context=edit` and aborts if the find needle is missing (for example if raw uses `real_mckenna/` with a trailing slash).
- Posts **3183** and **3330** have identity-only snapshots. They are not in `items` and must stay an empty diff.

## Identity (slug check before any write)

Abort if any ID's live slug differs from `targets.json`. Never PATCH on ID alone.

| ID | Required slug |
|---:|---|
| 12319 | `ai-conversations` |
| 2833 | `dent-the-future-an-insiders-experiences-at-the-dent-conference` |
| 2423 | `dent-2019-photo-recap-gallery` |

## What the script writes

Content only. Titles, slugs, dates, status, featured media, tags, categories, and SEO meta stay untouched.

| ID | Find (exactly once) | Inserted copy |
|---|---|---|
| 12319 | archive-card `<article>` opening that links `/category/conversations-interviews/` | new `aurora-media-card` before it. Title `Matt McKenna's decade at DENT`. Blurb exactly `Ten years of DENT, ten years sober, and a coffee shop in Miami.` |
| 2833 | Instagram-linked `Matt McKenna` in the DENT community paragraph | same `<a>`, new href to 3183, visible text `Matt McKenna, who has been at every single one` |
| 2423 | `who have become friends and collaborators.` | trailing sentence in that same intro `<p>`. Exact anchor `I sat down with Matt McKenna a few years after this` |

Inserted copy is ASCII. No em dashes. No NCR needed in the new card or sentences.

Skip a row if that exact `href` + anchor already exists. 3330 is the known skip and is not in `items`.

## Must not

- Modify post 3183 body.
- Modify post 3330 (existing 3183 link; category is #826).
- Remove or rewrite the Shane Gibson, Sharad Khare, or Conversations archive cards on 12319.
- Duplicate `kk-collection-footer`.
- Bolt a second Matt McKenna sentence onto 2833 if the name is already in the community paragraph.
- Run bulk `inject_links.py`.

## Commands

```bash
python3 -m unittest scripts.tests.test_apply_issue_831_matt_mckenna

# Offline dry-run: rewrite the snapshotted before-files into after/. No network.
python3 scripts/apply_issue_831_matt_mckenna.py --from-files

# Live GET dry-run: authenticated context=edit + printed diffs. No snapshot, no POST.
make varlock-run CMD='python3 scripts/apply_issue_831_matt_mckenna.py'

# Apply only after #826 is live and KK approves that diff.
make varlock-run CMD='python3 scripts/apply_issue_831_matt_mckenna.py --apply'
```

`--item-id 12319` limits to one object. Re-run after a successful apply prints `[SKIP]`.

`--apply` GETs the five #826 posts and aborts unless 3814 is out of 1757 into 1678, 3330 is out of 1757 into 1676, and 1067 / 1063 / 1147 are out of their wrong buckets into 1756.

Snapshot dir (mode 0700, files 0600):
`backup/issue-831-matt-mckenna/rest-<page|post>-<id>-before-<stamp>.json`

## Rollback

```bash
make varlock-run CMD='python3 scripts/apply_issue_831_matt_mckenna.py --restore backup/issue-831-matt-mckenna/rest-page-12319-before-<stamp>.json'
make varlock-run CMD='python3 scripts/apply_issue_831_matt_mckenna.py --restore backup/issue-831-matt-mckenna/rest-page-12319-before-<stamp>.json --apply'
```

Restore is dry-run by default. It refuses snapshots outside the three write IDs or a slug mismatch. Rollback body is the snapshotted `content.raw`.

## After-apply logged-out gates

```bash
curl -s -o /dev/null -w '%{http_code}\n' -L https://kriskrug.co/ai-conversations/
curl -s -o /dev/null -w '%{http_code}\n' -L https://kriskrug.co/2023/09/22/coffee-community-and-sobriety-matt-mckennas-decade-at-dent/
curl -s -o /dev/null -w '%{http_code}\n' -L https://kriskrug.co/2023/08/19/dent-the-future-an-insiders-experiences-at-the-dent-conference/
curl -s -o /dev/null -w '%{http_code}\n' -L https://kriskrug.co/2019/03/30/dent-2019-photo-recap-gallery/

curl -sL "https://kriskrug.co/ai-conversations/?cb=$RANDOM" | grep -n 'matt-mckennas-decade-at-dent'
curl -sL "https://kriskrug.co/ai-conversations/?cb=$RANDOM" | grep -F "Matt McKenna's decade at DENT"
curl -sL "https://kriskrug.co/ai-conversations/?cb=$RANDOM" | grep -F 'Ten years of DENT, ten years sober, and a coffee shop in Miami.'
curl -sL "https://kriskrug.co/ai-conversations/?cb=$RANDOM" | grep -c 'shane-gibsons-ai-sales-dojo'
curl -sL "https://kriskrug.co/ai-conversations/?cb=$RANDOM" | grep -c 'human-biography-podcast-w-sharad-khare'

curl -sL "https://kriskrug.co/2023/08/19/dent-the-future-an-insiders-experiences-at-the-dent-conference/?cb=$RANDOM" \
  | grep -F 'Matt McKenna, who has been at every single one'
curl -sL "https://kriskrug.co/2019/03/30/dent-2019-photo-recap-gallery/?cb=$RANDOM" \
  | grep -F 'I sat down with Matt McKenna a few years after this'

# footer count must match the pre-write snapshot
curl -sL "https://kriskrug.co/2023/08/19/dent-the-future-an-insiders-experiences-at-the-dent-conference/?cb=$RANDOM" \
  | grep -c 'kk-collection-footer'
curl -sL "https://kriskrug.co/2019/03/30/dent-2019-photo-recap-gallery/?cb=$RANDOM" \
  | grep -c 'kk-collection-footer'
```

Expect: 12319 gains exactly one new interview card to 3183. Shane / Sharad / archive cards stay. 2833 and 2423 footer counts unchanged. 3330 and 3183 bodies unchanged.

## Out of payload

- Recategorizing 3330 (#826)
- A second 3183 link on 3330
- Post 3183 body edits
- Hub cards on 12013 / 12318 / 12316
- `inject_links.py`
