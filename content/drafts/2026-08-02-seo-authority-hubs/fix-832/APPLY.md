# #832 APPLY: route Vancouver AI meetup recaps to /events/

**Prepared, not applied. Do not PATCH until #826 is live and KK says go.**
Script is dry-run by default. `--apply` is the only write switch, and it refuses unless the five #826 category fixes are already live.

Parent: #402. This is child 7 of 9. It **adds** `/events/` links. It does not swap existing `/vancouver-ai/` destinations.

Do not close #832 or #402 when this runbook merges.

**Do not write page 2250.** #635 owns `/events/`. The apply script hard-refuses ID 2250 on `--item-id`, `--restore`, `targets.items`, and any POST URL that contains `/pages/2250`.

## Live reconfirm (logged-out public REST GET, 2026-08-19T23:22:56Z)

No REST POST / PATCH / DELETE in this session. WP_USER / WP_APP_PASSWORD were unset, so there is no authenticated `context=edit` `content.raw` for the seven recaps or page 2250. Public REST confirmed slug/ID pairs and `content.rendered`. Page 12315 `modified_gmt` still matches the 2026-07-01 backup, so that backup's `content.raw` is the before-file for 12315.

| ID | Kind | Slug | URL | HTTP | `kriskrug.co/events/` | `/vancouver-ai/` | Notes |
|---|---|---|---|---:|---|---|---|
| 4495 | post | `inside-the-innaugural-vancouver-ai-community-meetup` | `/2024/01/28/inside-the-innaugural-vancouver-ai-community-meetup/` | 200 | **no** | yes (3) | Baked footer present. |
| 9197 | post | `vancouver-ai-meetup-16-where-tech-creativity-and-community-collide` | `/2025/05/11/vancouver-ai-meetup-16-where-tech-creativity-and-community-collide/` | 200 | **no** | yes (1) | Baked footer present. |
| 8418 | post | `vancouver-ai-the-community-building-bcs-ai-future-february-meetup-recap` | `/2025/03/02/vancouver-ai-the-community-building-bcs-ai-future-february-meetup-recap/` | 200 | **no** | yes (1) | Baked footer present. Authenticated raw block terminus reconfirmed 2026-08-28. |
| 6815 | post | `august-vancouver-ai-community-meetup-recap-hackers-hustlers-heretics` | `/2024/09/01/august-vancouver-ai-community-meetup-recap-hackers-hustlers-heretics` | 200 | **no** | yes (1) | No `kk-collection-footer`. Ends on the Related hub line. One AWS `/events/` URL is unrelated. |
| 6251 | post | `creativity-in-the-age-of-ai-vancouver-ai-community-meetup-june-2024-highlights` | `/2024/07/08/creativity-in-the-age-of-ai-vancouver-ai-community-meetup-june-2024-highlights/` | 200 | **no** | yes (1) | `meetup.com/vancouver-ai-meetup/events/` is not the hub. Footer present. |
| 5768 | post | `june-vancouver-ai-community-meetup-recap-a-confluence-of-minds-and-machines` | `/2024/06/02/june-vancouver-ai-community-meetup-recap-a-confluence-of-minds-and-machines/` | 200 | **no** | yes (1) | No footer. Has `/ai-events/` plus a Northeastern `/events/` URL. |
| 4348 | post | `2024-vancouver-ai-community-meetups` | `/2023/12/27/2024-vancouver-ai-community-meetups/` | 200 | **no** | **no** (only `lu.ma/vancouver-ai`) | 2023 directory. Footer names AI Ethics. Insert in the intro, ahead of the dated list. |
| 12315 | page | `vancouver-ai` | `/vancouver-ai/` | 200 | **no** | n/a | Events and recaps card still has only "Browse AI events" -> `/ai-events/`. |
| 2250 | page | `events` | `/events/` | 200 | fixture only | n/a | **Must not write.** Public rendered SHA-256 `4353740134b28aa577de881cd41aaf071e8304444540687cb3562206145beb43`. |

`/events/`, `/vancouver-ai/`, `/ai-events/`, and the seven recap permalinks were HTTP 200.

The live `/events/` card still talks about Luma and registration. Do not copy any date from that card into the new sentences. Matrix anchors already avoid dates.

## Snapshot gaps

- No committed `context=edit` `content.raw` fixture for posts 4495, 9197, 8418, 6815, 6251, 5768, 4348. Their `before/*-content.raw.html` files are public `content.rendered` stand-ins so `--from-files` can run offline. Post 8418's authenticated raw terminus was reconfirmed on 2026-08-28 at the unchanged `modified_gmt` and is pinned in `targets.json` with raw SHA-256 `ebf28d1f...bf3a4a15`; the rendered stand-in remains an explicit alternate for offline characterization. Recut any other `find` if a future authenticated dry run misses.
- Page 2250 has public rendered only. That is enough to prove this pack never mutates it. There is no 2250 `content.raw` in the pack.
- Page 12315 raw is the 2026-07-01 backup. Live `modified_gmt` is still `2026-07-01T20:27:36`, and the Browse AI events button text is unchanged.

## Identity (slug check before any write)

Abort if any ID's live slug differs from `targets.json`. Never PATCH on ID alone.

| ID | Required slug |
|---:|---|
| 4495 | `inside-the-innaugural-vancouver-ai-community-meetup` |
| 9197 | `vancouver-ai-meetup-16-where-tech-creativity-and-community-collide` |
| 8418 | `vancouver-ai-the-community-building-bcs-ai-future-february-meetup-recap` |
| 6815 | `august-vancouver-ai-community-meetup-recap-hackers-hustlers-heretics` |
| 6251 | `creativity-in-the-age-of-ai-vancouver-ai-community-meetup-june-2024-highlights` |
| 5768 | `june-vancouver-ai-community-meetup-recap-a-confluence-of-minds-and-machines` |
| 4348 | `2024-vancouver-ai-community-meetups` |
| 12315 | `vancouver-ai` |

Page 2250 slug `events` is recorded only as the must-not-write fixture.

## What the script writes

Content only. Titles, slugs, dates, status, featured media, tags, categories, and SEO meta stay untouched.

| ID | Find (exactly once) | Inserted copy |
|---|---|---|
| 4495 | toast line ending `community!</p>` | trailing sentence, exact anchor `we still do this every month, and the next one is on the calendar` (row 18) |
| 9197 | `converge to shape our collective future.</p>` | trailing sentence, exact anchor `the next one` (row 19) |
| 8418 | raw empty paragraph block immediately before the baked footer; rendered stand-in retained as an explicit offline alternate | new paragraph, exact anchor `come to the next one` (row 20) |
| 6815 | Related hub sentence (keeps the `/vancouver-ai/` link) | trailing sentence, exact anchor `the current calendar` (row 21) |
| 6251 | Host sign-off line | new paragraph before the footer, exact anchor `where the next one lands` (row 22) |
| 5768 | `continue to explore, create, and inspire together.</p>` | trailing sentence, exact anchor `still monthly, still free, still worth the trip` (row 23) |
| 4348 | italic intro goal paragraph | new intro paragraph ahead of the 2023-era list, exact anchor `the live calendar, which is the version that stays current` (row 24) |
| 12315 | `Browse AI events` button on the Events and recaps card | second link, exact anchor `the calendar` (row 25). `/ai-events/` stays. |

Inserted copy is ASCII. No em dashes. No dates. Existing `/vancouver-ai/` hrefs stay.

Skip a row if that exact `href` + anchor already exists.

## Must not

- PATCH, POST, or restore page 2250, its Luma embed, registration card, or event media (#635).
- Replace `/vancouver-ai/` links with `/events/`.
- Recategorize meetup posts (4348's AI Ethics footer is out of payload).
- Hard-code a meetup date in the new sentences.
- Duplicate `kk-collection-footer`.
- Run bulk `inject_links.py`.

## Commands

```bash
python3 -m unittest scripts.tests.test_apply_issue_832_events_routing

# Offline dry-run: rewrite the snapshotted before-files into after/. No network.
python3 scripts/apply_issue_832_events_routing.py --from-files

# Live GET dry-run: authenticated context=edit + printed diffs. No snapshot, no POST.
make varlock-run CMD='python3 scripts/apply_issue_832_events_routing.py'

# Apply only after #826 is live and KK approves that diff.
make varlock-run CMD='python3 scripts/apply_issue_832_events_routing.py --apply'
```

`--item-id 4495` limits to one object. `--item-id 2250` aborts. Re-run after a successful apply prints `[SKIP]`.

`--apply` GETs the five #826 posts and aborts unless 3814 is out of 1757 into 1678, 3330 is out of 1757 into 1676, and 1067 / 1063 / 1147 are out of their wrong buckets into 1756.

Snapshot dir (mode 0700, files 0600):
`backup/issue-832-events-routing/rest-<page|post>-<id>-before-<stamp>.json`

## Rollback

```bash
make varlock-run CMD='python3 scripts/apply_issue_832_events_routing.py --restore backup/issue-832-events-routing/rest-post-4495-before-<stamp>.json'
make varlock-run CMD='python3 scripts/apply_issue_832_events_routing.py --restore backup/issue-832-events-routing/rest-post-4495-before-<stamp>.json --apply'
```

Restore is dry-run by default. It refuses snapshots outside the eight owned IDs, a slug mismatch, or page 2250.

## After-apply logged-out gates

```bash
curl -s -o /dev/null -w '%{http_code}\n' -L https://kriskrug.co/events/
curl -s -o /dev/null -w '%{http_code}\n' -L https://kriskrug.co/vancouver-ai/

# Re-read the live card (do not copy dates into new copy)
curl -sL "https://kriskrug.co/events/?cb=$RANDOM" | grep -i -n 'luma\|register\|meetup' | head

curl -sL "https://kriskrug.co/2024/01/28/inside-the-innaugural-vancouver-ai-community-meetup/?cb=$RANDOM" \
  | grep -F 'we still do this every month, and the next one is on the calendar'
curl -sL "https://kriskrug.co/2025/05/11/vancouver-ai-meetup-16-where-tech-creativity-and-community-collide/?cb=$RANDOM" \
  | grep -F 'the next one'
curl -sL "https://kriskrug.co/2025/03/02/vancouver-ai-the-community-building-bcs-ai-future-february-meetup-recap/?cb=$RANDOM" \
  | grep -F 'come to the next one'
curl -sL "https://kriskrug.co/2024/09/01/august-vancouver-ai-community-meetup-recap-hackers-hustlers-heretics/?cb=$RANDOM" \
  | grep -F 'the current calendar'
curl -sL "https://kriskrug.co/2024/07/08/creativity-in-the-age-of-ai-vancouver-ai-community-meetup-june-2024-highlights/?cb=$RANDOM" \
  | grep -F 'where the next one lands'
curl -sL "https://kriskrug.co/2024/06/02/june-vancouver-ai-community-meetup-recap-a-confluence-of-minds-and-machines/?cb=$RANDOM" \
  | grep -F 'still monthly, still free, still worth the trip'
curl -sL "https://kriskrug.co/2023/12/27/2024-vancouver-ai-community-meetups/?cb=$RANDOM" \
  | grep -F 'the live calendar, which is the version that stays current'
curl -sL "https://kriskrug.co/vancouver-ai/?cb=$RANDOM" | grep -F 'the calendar'
curl -sL "https://kriskrug.co/vancouver-ai/?cb=$RANDOM" | grep -F 'Browse AI events'

# Page 2250 must match the pre-session public rendered snapshot
curl -s "https://kriskrug.co/wp-json/wp/v2/pages/2250?_fields=id,slug,modified_gmt,content" \
  | python3 -c "import hashlib,json,sys; d=json.load(sys.stdin); print(d['id'], d['slug']); print(hashlib.sha256(d['content']['rendered'].encode()).hexdigest())"
```

Expect: each of the seven recaps gains exactly one new `https://kriskrug.co/events/` anchor. 12315 keeps `/ai-events/` and adds `the calendar`. Existing `/vancouver-ai/` hrefs stay. Page 2250 rendered SHA-256 stays `4353740134b28aa577de881cd41aaf071e8304444540687cb3562206145beb43` unless #635 has written it for its own reasons. Footer counts on 4495 / 9197 / 8418 / 6251 / 4348 stay the same.

## Out of payload

- Page 2250 / Luma / event heroes (#635)
- Taxonomy repair (#826)
- Replacing `/vancouver-ai/` with `/events/`
- Recategorizing 4348
- Schema Event markup (parent #402 schema lane)
- `inject_links.py`
