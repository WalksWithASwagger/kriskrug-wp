# Issue #827 apply-ready readback (2026-08-17)

**Status:** PREPARED, NOT APPLIED. Content-only payloads for page 12013 and posts 1222 / 1056. No live WordPress write.
**Issue:** [#827](https://github.com/WalksWithASwagger/kriskrug-wp/issues/827) (child 2 of [#402](https://github.com/WalksWithASwagger/kriskrug-wp/issues/402)).
**Pack:** [`content/drafts/2026-08-02-seo-authority-hubs/fix-827/`](../../../content/drafts/2026-08-02-seo-authority-hubs/fix-827/)
**Blocker:** [#826](https://github.com/WalksWithASwagger/kriskrug-wp/issues/826) taxonomy repair is not live.

Do not close #827 or #402.

## Method

Logged-out HTTP + public REST, then authenticated GET `context=edit` for `content.raw` only. Fetch stamp `2026-08-17T06:29Z` (public) and `2026-08-17T06:35Z` (raw). No POST / PATCH / DELETE. No `.env*` reads. No PNG captures.

## Slug / ID pairs (public REST, then raw GET)

| ID | Kind | Slug | Link | `modified_gmt` | HTTP |
|---:|---|---|---|---|---:|
| 12013 | page | `photography` | https://kriskrug.co/photography/ | 2026-08-17T05:30:00 | 200 |
| 1222 | post | `to-all-you-wannabe-fashion-photographers` | https://kriskrug.co/2007/04/27/to-all-you-wannabe-fashion-photographers/ | 2026-07-11T19:48:05 | 200 |
| 1056 | post | `kk-on-modelmayhemcom` | https://kriskrug.co/2006/10/23/kk-on-modelmayhemcom/ | 2026-06-15T05:20:28 | 200 |

Also 200: https://kriskrug.co/category/photography-visual-storytelling/

Page 12013 `modified_gmt` matches the #706 PressCACHE no-op title-save recorded in the #480 reconfirm. Body and inline `<style>` are unchanged cream-pack. #480 has not been applied.

## Live link counts (body `content.rendered`, not chrome)

| ID | Internal `<a href>` | External `<a href>` | `kk-collection-footer` in raw | Planned anchors present |
|---:|---:|---:|---:|---|
| 12013 | **0** | 2 (both Flickr) | 0 | none of rows 11-12 |
| 1222 | 2 (footer pillar + sibling) | 8 | 2 string hits (comment + class) | row 13 absent |
| 1056 | 2 (footer pillar + sibling) | 1 (ModelMayhem) | 2 string hits | row 14 absent; no `/photography/` in body |

Post 1056 still does not link `/photography/`. Page 12013 still has zero internal links in the page body. Nav chrome on the public HTML does include `/photography/`; that is not page content.

## Block recount on 12013

Hub-plan "block 23" is stale. Today's rendered body has **22** block-level tags (`p`, `h2`, `figure`):

- 21 = `<h2>This is a fraction of it.</h2>`
- 22 = coda `<p>` ending `lives on Flickr.`

The helper inserts on that text, not on an index.

## Exact payload anchors

| Row | Source | Anchor | Target |
|---:|---|---|---|
| 11 | 12013 coda `<p>` | `the whole archive, twenty years of it` | `/category/photography-visual-storytelling/` |
| 12 | same `<p>`, new sentence | `the fashion and model years, 2006 to 2008` | post 1056 |
| 13 | 1222, before footer | `how I found those people in the first place` | post 1056 |
| 14 | 1056, after the peeps line | `where all of that ended up` | `/photography/` |

Flickr button text on 12013 is `See 144,000+ frames on Flickr ?`. Left alone. Inline `<style>` sha256 `23dc2ddaf20ffda0f94f619e9ade0068d3a9a0c5fdb38563538b6542a34c69b3`. No 1210 / checklist href.

## #826 still blocking live apply

Public REST 2026-08-17T06:32Z:

| ID | Slug | Live categories | Needed after #826 |
|---:|---|---|---|
| 3814 | `the-power-of-most-benevolent-outcomes-a-prayer-for-blessings-for-all-living-things` | `[1757]` | `[1678]` |
| 3330 | `the-future-called-i-answered` | `[1757]` | `[1676]` |
| 1067 | `hardcore-superstar-photoshoot` | `[1662]` | `[1756]` |
| 1063 | `made-in-vancouver-photoshoot` | `[1662]` | `[1756]` |
| 1147 | `fashion-photoshoot-for-discollection` | `[1665]` | `[1756]` |

`--apply` on the #827 helper aborts until those five swaps are live.

## #480 sequencing

Page 12013 is a shared write surface with #480. The current #480 `photography.html` is a full-page replace without rows 11-12. If it is applied after #827, it wipes these links. Sequence: #826, then #827, then re-cut #480 photography if the style-strip still needs to land.

## Not applied

This report is public readback plus a repo payload pack. Live HTML still has zero of the four anchors. KK approval is still required after #826.
