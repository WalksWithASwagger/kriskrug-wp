# #827 APPLY: photography hub internal links

**Prepared, not applied. Do not PATCH until #826 is live and KK says go.**
Script is dry-run by default. `--apply` is the only write switch, and it refuses unless the five #826 category fixes are already live.

Parent: #402. This is child 2 of 9. Child 1 (#826) still owns 1067 / 1063 / 1147. This pack does not recategorize or retitle them.

Do not close #827 or #402 when this runbook merges.

## Live reconfirm (logged-out + authenticated GET, 2026-08-17T06:35Z)

No REST POST / PATCH / DELETE in this session. Public REST confirmed slug/ID pairs. Authenticated `context=edit` snapshotted `content.raw` into `before/` (repo pack, not `backup/` secrets).

| ID | Kind | Slug | URL | HTTP | Internal body links | Notes |
|---|---|---|---|---:|---:|---|
| 12013 | page | `photography` | `/photography/` | 200 | **0** | Two Flickr exits only. Inline `<style>` still present. |
| 1222 | post | `to-all-you-wannabe-fashion-photographers` | `/2007/04/27/to-all-you-wannabe-fashion-photographers/` | 200 | 2 (footer only) | No link to 1056. One baked `kk-collection-footer`. |
| 1056 | post | `kk-on-modelmayhemcom` | `/2006/10/23/kk-on-modelmayhemcom/` | 200 | 2 (footer only) | Does not link `/photography/`. One baked footer. |

Four target URLs were 200: `/photography/`, `/category/photography-visual-storytelling/`, `/2006/10/23/kk-on-modelmayhemcom/`, `/2007/04/27/to-all-you-wannabe-fashion-photographers/`.

Page 12013 `modified_gmt` is `2026-08-17T05:30:00` (PressCACHE no-op title-save from #706). The coda text and the inline `<style>` are still the cream-pack body. #480 has not been applied.

### Block recount (today's HTML, not the 2026-08-02 index)

Walking `p / h2 / h3 / ul / ol / figure / blockquote` in `content.rendered`:

- Block 21 is the `<h2>This is a fraction of it.</h2>`
- Block 22 is the coda `<p>` that ends `lives on Flickr.`
- There is no block 23. Insertion is by **text match** on `lives on Flickr.</p>`, not a stale index.

Flickr stays. The archive link is a second link in that same closing paragraph. The Flickr control remains the existing `kkx-btn` (`See 144,000+ frames on Flickr ?`). Do not "fix" the `?`.

## Identity (slug check before any write)

Abort if any ID's live slug differs from `targets.json`. Never PATCH on ID alone.

| ID | Required slug |
|---:|---|
| 12013 | `photography` |
| 1222 | `to-all-you-wannabe-fashion-photographers` |
| 1056 | `kk-on-modelmayhemcom` |

## What the script writes

Content only. Titles, slugs, dates, status, featured media, tags, categories, and SEO meta stay untouched.

| ID | Find (exactly once) | Inserted copy |
|---|---|---|
| 12013 | `lives on Flickr.</p>` | two sentences in the same `<p>`: exact anchors `the whole archive, twenty years of it` (row 11) and `the fashion and model years, 2006 to 2008` (row 12) |
| 1222 | Megan Cole line, then the baked footer comment | trailing sentence before the footer: exact anchor `how I found those people in the first place` (row 13) |
| 1056 | `I've met a couple cool peeps already.</p>` | new sentence after that line: exact anchor `where all of that ended up` (row 14) |

Inserted copy is ASCII. No em dashes. No NCR needed in the new sentences. Existing latin1-unsafe characters in 12013 (em dashes, `ü`) and 1222 (`Â£`) stay as they are.

Skip a row if that exact `href` + anchor already exists.

## Must not

- Link post 1210 or add checklist copy (rows 34-37 / #828).
- Touch the inline `<style>` on 12013.
- Remove or rewrite the Flickr exit.
- Duplicate `kk-collection-footer`.
- Recategorize 1067 / 1063 / 1147.
- Run bulk `inject_links.py`.
- Mix the #480 style-strip into this write.

## #480 write-surface warning

Page 12013 is also an #480 write surface. `content/source-packs/content-architecture-2026/issue-480-retire-inline-css/photography.html` is a full-page replacement **without** these two links. If that payload is applied after these links land, it will wipe them unless it is re-cut.

Sequencing: **#826 live first, then #827, then re-cut the #480 photography payload if needed.** Do not apply #480 photography.html as it stands after this pack.

## Commands

```bash
python3 -m unittest scripts.tests.test_apply_issue_827_photography_hub

# Offline dry-run: rewrite the snapshotted before-files into after/. No network.
python3 scripts/apply_issue_827_photography_hub.py --from-files

# Live GET dry-run: authenticated context=edit + printed diffs. No snapshot, no POST.
make varlock-run CMD='python3 scripts/apply_issue_827_photography_hub.py'

# Apply only after #826 is live and KK approves that diff.
make varlock-run CMD='python3 scripts/apply_issue_827_photography_hub.py --apply'
```

`--item-id 12013` limits to one object. Re-run after a successful apply prints `[SKIP]`.

`--apply` GETs the five #826 posts and aborts unless 3814 is out of 1757 into 1678, 3330 is out of 1757 into 1676, and 1067 / 1063 / 1147 are out of their wrong buckets into 1756.

Snapshot dir (mode 0700, files 0600):
`backup/issue-827-photography-hub/rest-<page|post>-<id>-before-<stamp>.json`

## Rollback

```bash
make varlock-run CMD='python3 scripts/apply_issue_827_photography_hub.py --restore backup/issue-827-photography-hub/rest-page-12013-before-<stamp>.json'
make varlock-run CMD='python3 scripts/apply_issue_827_photography_hub.py --restore backup/issue-827-photography-hub/rest-page-12013-before-<stamp>.json --apply'
```

Restore is dry-run by default. It refuses snapshots outside the three IDs or a slug mismatch. Rollback body is the snapshotted `content.raw`.

## After-apply logged-out gates

```bash
curl -s -o /dev/null -w '%{http_code}\n' -L https://kriskrug.co/photography/
curl -s -o /dev/null -w '%{http_code}\n' -L https://kriskrug.co/category/photography-visual-storytelling/
curl -s -o /dev/null -w '%{http_code}\n' -L https://kriskrug.co/2006/10/23/kk-on-modelmayhemcom/
curl -s -o /dev/null -w '%{http_code}\n' -L https://kriskrug.co/2007/04/27/to-all-you-wannabe-fashion-photographers/

curl -sL "https://kriskrug.co/photography/?cb=$RANDOM" | grep -F 'the whole archive, twenty years of it'
curl -sL "https://kriskrug.co/photography/?cb=$RANDOM" | grep -F 'the fashion and model years, 2006 to 2008'
curl -sL "https://kriskrug.co/photography/?cb=$RANDOM" | grep -c 'checklist-of-model-photographer-negotiation-items'
# last command must print 0 until child 3 / #828

curl -sL "https://kriskrug.co/2007/04/27/to-all-you-wannabe-fashion-photographers/?cb=$RANDOM" \
  | grep -F 'how I found those people in the first place'
curl -sL "https://kriskrug.co/2006/10/23/kk-on-modelmayhemcom/?cb=$RANDOM" \
  | grep -F 'where all of that ended up'

# footer count must match the pre-write snapshot (2 raw hits = comment + class)
curl -sL "https://kriskrug.co/2007/04/27/to-all-you-wannabe-fashion-photographers/?cb=$RANDOM" \
  | grep -c 'kk-collection-footer'
curl -sL "https://kriskrug.co/2006/10/23/kk-on-modelmayhemcom/?cb=$RANDOM" \
  | grep -c 'kk-collection-footer'
```

Expect: 12013 body gains exactly two new internal `<a href>` (archive + 1056), not three. Flickr button still present. 1222 and 1056 footer counts unchanged. No 1210 href on 12013.

## Out of payload

- Post 1210 rewrite and checklist inbounds (#828)
- Taxonomy repair on 1067 / 1063 / 1147 / 3814 / 3330 (#826)
- Inline CSS retirement on 12013 (#480)
- Hub cards on 12318 / 12316 / 12319
- `inject_links.py`
