# #827 APPLY: wire internal links on /photography/

**Prepared, not applied. Do not PATCH until KK says go.**
Script is dry-run by default. `--apply` is the only write switch.

Parent: #402. This is child 2 of 9. **Live apply waits for KK and should follow #826 apply.** Child 1 is prepared on `main` and is not live: public REST on 2026-08-17T06:32Z still has 1067/1063 in `[1662]` and 1147 in `[1665]`. Do not recategorize those posts here. 1056 and 1222 are already in `photography-visual-storytelling` (`[1756]`); this child still must not PATCH them until KK approves, after #826.

## Live reconfirm (logged-out, 2026-08-17T06:32Z)

Public GET only. No REST POST/PATCH/DELETE. `inject_links.py` was not run.

| URL | HTTP | Identity |
|---|---|---|
| `https://kriskrug.co/photography/` | 200 | page 12013, slug `photography`, `modified_gmt` 2026-08-17T05:30:00 |
| `https://kriskrug.co/category/photography-visual-storytelling/` | 200 | term archive |
| `https://kriskrug.co/2006/10/23/kk-on-modelmayhemcom/` | 200 | post 1056, slug `kk-on-modelmayhemcom`, cats `[1756]` |
| `https://kriskrug.co/2007/04/27/to-all-you-wannabe-fashion-photographers/` | 200 | post 1222, slug `to-all-you-wannabe-fashion-photographers`, cats `[1756]` |

Page 12013 `content.rendered` still has **zero** internal `href`s. The two body links are both `https://www.flickr.com/photos/kk/` (intro + coda button). Exact anchors for rows 11-14 are absent. `checklist-of-model-photographer-negotiation-items` is absent. Inline `<style>` is present (5039 chars, sha256 `23dc2ddaf20ffda0f94f619e9ade0068d3a9a0c5fdb38563538b6542a34c69b3` of the rendered `<style>` block). Do not touch it.

Post 1056 body still does not contain `/photography/` or `kriskrug.co/photography`. It still has one `kk-collection-footer`. The peeps line is `I&#8217;ve met a couple cool peeps already.`

Post 1222 body still does not contain the row 13 anchor. Footer count is 1. No link to post 1210.

Block recount on today's 12013 rendered HTML (walk `p`/`h2`/`h3`/`ul`/`ol`/`figure`/`blockquote`): **22** blocks. `This is a fraction of it` is the coda `h2` (block 21). The closing paragraph is block **22**, not stale index 23. Insert by that text match.

## Identity (slug check before any write)

Abort if any ID's live slug differs from `targets.json`. Page 12013 uses `/wp/v2/pages/12013`. Posts 1222 and 1056 use `/wp/v2/posts/<id>`. Never PATCH on ID alone.

## What the script writes

Content-only. No `categories`. No titles, slugs, dates, status, featured media, tags, or SEO meta.

| ID | Rows | REST body |
|---|---|---|
| 12013 | 11, 12 | Insert two sentences at the end of the coda `<p>` after `This is a fraction of it`. Archive link, then fashion-years link to 1056. Flickr button stays. `<style>` must be byte-identical. |
| 1222 | 13 | One paragraph before the existing `kk-collection-footer`. Footer count stays 1. |
| 1056 | 14 | One sentence after the peeps line, still inside that paragraph. Footer count stays 1. |

Skip a row if that exact `href` + anchor already exists. Do not add data rows 34-37. Do not link post 1210.

Inserted copy (also in the snippet files):

- 12013: ` The on-site version is <a href="https://kriskrug.co/category/photography-visual-storytelling/">the whole archive, twenty years of it</a>. Start with <a href="https://kriskrug.co/2006/10/23/kk-on-modelmayhemcom/">the fashion and model years, 2006 to 2008</a>.`
- 1222: `<p>The year before this rant I posted <a href="https://kriskrug.co/2006/10/23/kk-on-modelmayhemcom/">how I found those people in the first place</a>.</p>`
- 1056: ` Here is <a href="https://kriskrug.co/photography/">where all of that ended up</a>.`

## Commands

```bash
python3 -m unittest scripts.tests.test_apply_issue_827_photography_hub

# Dry run: authenticated GET + printed plan. No snapshot, no POST.
make varlock-run CMD='python3 scripts/apply_issue_827_photography_hub.py'

# Apply only after KK approves that diff, and after #826 is live.
make varlock-run CMD='python3 scripts/apply_issue_827_photography_hub.py --apply'
```

`--id 12013` limits to one target. Re-run after a successful apply prints `[SKIP]`.

Snapshot dir (mode 0700, files 0600):
`backup/issue-827-photography-hub/rest-{pages|posts}-<id>-before-<stamp>.json`

## Rollback

```bash
make varlock-run CMD='python3 scripts/apply_issue_827_photography_hub.py --restore backup/issue-827-photography-hub/rest-pages-12013-before-<stamp>.json'
make varlock-run CMD='python3 scripts/apply_issue_827_photography_hub.py --restore backup/issue-827-photography-hub/rest-pages-12013-before-<stamp>.json --apply'
```

Restore is dry-run by default. It refuses snapshots outside the three IDs or a slug mismatch. Restore writes `content` only.

## After-apply logged-out gates

```bash
curl -s -o /dev/null -w '%{http_code}\n' -L https://kriskrug.co/photography/
curl -s -o /dev/null -w '%{http_code}\n' -L https://kriskrug.co/category/photography-visual-storytelling/
curl -s -o /dev/null -w '%{http_code}\n' -L https://kriskrug.co/2006/10/23/kk-on-modelmayhemcom/

curl -sL "https://kriskrug.co/photography/?cb=$RANDOM" | grep -F 'the whole archive, twenty years of it'
curl -sL "https://kriskrug.co/photography/?cb=$RANDOM" | grep -F 'the fashion and model years, 2006 to 2008'
curl -sL "https://kriskrug.co/photography/?cb=$RANDOM" | grep -c 'checklist-of-model-photographer-negotiation-items'
# last command must print 0 until child 3

curl -sL "https://kriskrug.co/2007/04/27/to-all-you-wannabe-fashion-photographers/?cb=$RANDOM" \
  | grep -F 'how I found those people in the first place'
curl -sL "https://kriskrug.co/2006/10/23/kk-on-modelmayhemcom/?cb=$RANDOM" \
  | grep -F 'where all of that ended up'
```

Expect: 12013 body gains exactly two internal links (archive + 1056), Flickr remains, no 1210. 1222 and 1056 `kk-collection-footer` counts unchanged from the pre-write snapshot.

## Out of payload

- Post 1210 ModelMayhem 404 rewrite and data rows 34-37 (#828)
- Recategorizing 1067 / 1063 / 1147 (#826)
- Hub cards on 12318 / 12316 / 12319
- Regenerating `/photography/` or stripping its inline CSS
- Closing #402
