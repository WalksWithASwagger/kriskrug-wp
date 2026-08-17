# [CONTENT] Wire internal links on /photography/ (page 12013)

**Parent:** [#402](https://github.com/WalksWithASwagger/kriskrug-wp/issues/402)
**Child:** 2 of 9
**Suggested labels:** `content`, `seo`, `needs-human-review`, `priority:high`
**Lane:** Track A
**Research:** `content/drafts/2026-08-02-seo-authority-hubs/hub-plan.md` terms 4, 7, 10 (structural hub only), `link-matrix.csv` data rows 11-14
**Blocked by:** child 1 (taxonomy repair)

---

## Context

`/photography/` (page **12013**) is a curated gallery with **zero** internal links. It exits to Flickr and never routes into the 158-post `photography-visual-storytelling` archive. PR #670 called this the single biggest structural gap behind three of #402's ten terms (`modelmayhem.com`, `hardcore photoshoot`, `negotiation equipment for photographers`).

This child wires the hub and the 2006 ModelMayhem ranking asset (post 1056). It does **not** add the negotiation-checklist sentence on page 12013. That is data row 34, owned by child 3, after post 1210 is rewritten.

`modelmayhem.com` is a navigational query for someone else's site. Do not optimize a title for it. The value is crawl path into the 2006-2008 fashion cluster.

Page 12013 carries a large inline `<style>` block, same pattern as `/about/`. Edit the existing content. Do not regenerate the page.

## Owns (write)

- Page **12013** block 23: archive link (row 11) and fashion-years link to post 1056 (row 12) only.
- Post **1222** trailing sentence to post 1056 (row 13).
- Post **1056** new sentence to `/photography/` (row 14).

## Must not touch

- Data rows 34-37 (checklist inbounds and 1210 outbound). Leave a clean block 23 so child 3 can add a third sentence later.
- Posts 1067, 1063, 1147 (child 1 owns categories; this child does not recategorize or retitle them).
- Flickr exit on 12013: keep it. The archive link is a **second** link in the same closing paragraph.
- Theme CSS, schema, titles.

## Acceptance Criteria

- [ ] Child 1 has landed (or this agent re-verifies the five category fixes are already live) before PATCHing 1056/1222 footers.
- [ ] Page 12013 block 23 links `https://kriskrug.co/category/photography-visual-storytelling/` with exact anchor `the whole archive, twenty years of it` (row 11).
- [ ] Same block 23 links post 1056 with exact anchor `the fashion and model years, 2006 to 2008` (row 12).
- [ ] Page 12013 still has **no** link to post 1210. Child 3 adds that.
- [ ] Post 1222 links 1056 with exact anchor `how I found those people in the first place` (row 13), before the collection footer.
- [ ] Post 1056 links `/photography/` with exact anchor `where all of that ended up` (row 14), after the "I've met a couple cool peeps already" line.
- [ ] Inline `<style>` on 12013 is unchanged. Flickr link remains. No duplicate `kk-collection-footer`.
- [ ] All four target URLs still 200. Slug/ID snapshots taken. Content-only payloads.

## Tests/Evals

- Count new internal `<a href>` on 12013: plus two (archive + 1056), not three.
- `grep -F` each exact anchor on a cache-busted fetch of the three URLs.
- `grep -c 'kk-collection-footer'` on 1222 and 1056 is unchanged from the pre-write snapshot.
- Diff of 12013 `content.raw` does not touch the `<style>` block.

## Verification

```bash
curl -s -o /dev/null -w '%{http_code}\n' -L https://kriskrug.co/photography/
curl -s -o /dev/null -w '%{http_code}\n' -L https://kriskrug.co/category/photography-visual-storytelling/
curl -s -o /dev/null -w '%{http_code}\n' -L https://kriskrug.co/2006/10/23/kk-on-modelmayhemcom/

# After apply
curl -sL "https://kriskrug.co/photography/?cb=$RANDOM" | grep -F 'the whole archive, twenty years of it'
curl -sL "https://kriskrug.co/photography/?cb=$RANDOM" | grep -F 'the fashion and model years, 2006 to 2008'
curl -sL "https://kriskrug.co/photography/?cb=$RANDOM" | grep -c 'checklist-of-model-photographer-negotiation-items'
# last command must print 0 until child 3
```

## Agent Instructions

- `GET /wp-json/wp/v2/pages/12013?context=edit`. Confirm slug `photography`. Snapshot before edit.
- Insertion points are block indexes from the 2026-08-02 rendered body. Re-count blocks on today's HTML before inserting. If block 23 is no longer the "This is a fraction of it" paragraph, insert there by text match, not by stale index.
- Skip a row if that exact `href` + anchor already exists.
- Content-only PATCH. Dry-run. KK approval before live.
- Do not run bulk `inject_links.py`.
- Do not close #402.

### Data rows 11-14

| # | source_url | target_url | anchor_text | section_hint |
|---|---|---|---|---|
| 11 | `https://kriskrug.co/photography/` | `https://kriskrug.co/category/photography-visual-storytelling/` | the whole archive, twenty years of it | Block 23, closing section, second link beside the existing Flickr exit |
| 12 | `https://kriskrug.co/photography/` | `https://kriskrug.co/2006/10/23/kk-on-modelmayhemcom/` | the fashion and model years, 2006 to 2008 | Block 23, closing section, new sentence |
| 13 | `https://kriskrug.co/2007/04/27/to-all-you-wannabe-fashion-photographers/` | `https://kriskrug.co/2006/10/23/kk-on-modelmayhemcom/` | how I found those people in the first place | Body, trailing sentence, before the collection footer |
| 14 | `https://kriskrug.co/2006/10/23/kk-on-modelmayhemcom/` | `https://kriskrug.co/photography/` | where all of that ended up | Block 2, after the met-a-couple-cool-peeps line, new sentence |

## Out of Scope

- Rewriting post 1210 or linking to it (child 3).
- Recategorizing 1067 / 1063 / 1147 (child 1).
- Building content for the `modelmayhem.com` query.
- Regenerating `/photography/` or stripping its inline CSS.
