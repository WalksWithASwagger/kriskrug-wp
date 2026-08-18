# #827 applied, 2026-08-18

**Issue:** [#827](https://github.com/WalksWithASwagger/kriskrug-wp/issues/827) (child 2 of [#402](https://github.com/WalksWithASwagger/kriskrug-wp/issues/402)).
**Lane:** Track A. Ran after live #826 category proof. KK go: "proceed".
**Script:** `make varlock-run CMD='python3 scripts/apply_issue_827_photography_hub.py --apply'`
**Stamp:** `20260818T021841Z`

`--apply` confirmed #826 categories, then wrote page 12013 and posts 1222 / 1056. Re-run: all three `[SKIP]`. Flickr exit, `?` on the Flickr button, and the page-content `<style>` were not rewritten. No post 1210 / checklist rows 34–37.

## Live readback (logged-out cache-bust, 2026-08-18T02:19Z)

| ID | Anchor | Present |
|---|---|---|
| 12013 | `the whole archive, twenty years of it` → `/category/photography-visual-storytelling/` | 1 |
| 12013 | `the fashion and model years, 2006 to 2008` → post 1056 | 1 |
| 1222 | `how I found those people in the first place` → post 1056 | 1 |
| 1056 | `where all of that ended up` → `/photography/` | 1 href (phrase also appears in chrome) |

`checklist-of-model-photographer-negotiation-items` count is **0**. Flickr `kkx-btn` still present. 1222 and 1056 still have exactly one `kk-collection-footer`.

## #480 collision

`content/source-packs/content-architecture-2026/issue-480-retire-inline-css/photography.html` is a full-page replacement **without** these two links. Recut it before any #480 photography PATCH.

## Snapshots / rollback

`backup/issue-827-photography-hub/rest-page-12013-before-20260818T021841Z.json`
`backup/issue-827-photography-hub/rest-post-{1222,1056}-before-20260818T021841Z.json`
