# #318 authenticated publish-status proof — 2026-08-28

**Issue:** #318 (`[OPS] Remove 13 tracked images from three draft packages after publish-status proof`)  
**Result:** no deletion candidates. All three matching WordPress posts are drafts, so all 13 tracked images stay.  
**Live changes:** none. The verification used authenticated `GET` requests only.

## Method

The repository WordPress client queried both `posts` and `pages` for each exact
package slug with `status=any`, `context=edit`, and a restricted field list. The
check recorded only object identity, status, modified time, featured-media ID,
body media IDs, and upload basenames. It did not print post bodies or credentials.

Every referenced attachment ID was then read in edit context to verify its
current source basename. Public route/search evidence was not used as a
substitute for the authenticated all-status result.

## WordPress classification

| Package slug | WP object | Status | Modified | Media references | Classification |
|---|---:|---|---|---|---|
| `how-we-did-it-behind-the-scenes-of-the-sfu-siat-microcredential-project` | post 12038 | `draft` | 2026-06-11T11:14:58 | featured 0; body IDs none | unpublished / in-flight |
| `human-element-shane-loki-talk` | post 12048 | `draft` | 2026-05-24T14:42:00 | featured 12041; body 12043–12047; attachment 12042 exists but is not referenced in the captured body | unpublished / in-flight |
| `cotton-underwear-paradox` | post 12081 | `draft` | 2026-05-26T16:25:38 | featured 12098; body 12098–12101 | unpublished / in-flight |

No matching page exists for any slug. None of the three packages is ambiguous:
each exact slug maps to one post, and every matching post is a draft.

## Verified attachment map

| Package | Media IDs | Verified source basenames |
|---|---|---|
| Human Element | 12041–12047 | `01-human-element-shane-loki-talk.png` through `07-human-element-shane-loki-talk.png` |
| Cotton Underwear | 12098–12101 | `01-vancouver-ai-data-centre-protest-editorial.jpg` through `04-public-benefit-not-private-extraction-editorial.jpg` |
| SFU SIAT | none referenced | the two local Rafiki variants are not represented in the captured WordPress draft |

All eleven queried attachments exist with status `inherit`. This proves that
some local files have WordPress counterparts; it does not make the source
packages safe to prune while their posts remain unpublished.

## Exact tracked inventory

| Bytes | Path |
|---:|---|
| 1,467,985 | `content/drafts/2026-05-24-how-we-did-it-behind-the-scenes-of-the-sfu-siat-microcredential-project/images/rafiki-v1.png` |
| 1,410,389 | `content/drafts/2026-05-24-how-we-did-it-behind-the-scenes-of-the-sfu-siat-microcredential-project/images/rafiki-v2.png` |
| 2,320,108 | `content/drafts/2026-05-24-human-element-shane-loki-talk/images/01-human-element-shane-loki-talk.png` |
| 3,613,000 | `content/drafts/2026-05-24-human-element-shane-loki-talk/images/02-human-element-shane-loki-talk.png` |
| 2,434,250 | `content/drafts/2026-05-24-human-element-shane-loki-talk/images/03-human-element-shane-loki-talk.png` |
| 2,407,770 | `content/drafts/2026-05-24-human-element-shane-loki-talk/images/04-human-element-shane-loki-talk.png` |
| 3,543,409 | `content/drafts/2026-05-24-human-element-shane-loki-talk/images/05-human-element-shane-loki-talk.png` |
| 2,452,690 | `content/drafts/2026-05-24-human-element-shane-loki-talk/images/06-human-element-shane-loki-talk.png` |
| 2,442,310 | `content/drafts/2026-05-24-human-element-shane-loki-talk/images/07-human-element-shane-loki-talk.png` |
| 556,107 | `content/drafts/2026-05-25-cotton-underwear-paradox/images/01-vancouver-ai-data-centre-protest-editorial.jpg` |
| 628,753 | `content/drafts/2026-05-25-cotton-underwear-paradox/images/02-clean-water-city-protest-editorial.jpg` |
| 582,141 | `content/drafts/2026-05-25-cotton-underwear-paradox/images/03-engineers-against-data-centres-editorial.jpg` |
| 559,189 | `content/drafts/2026-05-25-cotton-underwear-paradox/images/04-public-benefit-not-private-extraction-editorial.jpg` |
| **24,418,101** | **Total: 13 files** |

Package totals are 2,878,374 bytes (SFU SIAT), 19,213,537 bytes (Human
Element), and 2,326,190 bytes (Cotton Underwear).

## Disposition

The issue contract says unpublished, in-flight, and ambiguous packages must be
left untouched. All three packages are unpublished/in-flight, so:

- deletion allow-list: **empty**;
- archive/rollback move: **not applicable**;
- ignore-rule change: **not justified**;
- tracked image deletion: **none**;
- Markdown or package changes: **none**.

This resolves #318 as a documented no-op. If one of these posts is published in
the future, open a new narrowly scoped cleanup issue with a fresh authenticated
status/media readback and an exact KK-approved path list. Do not carry forward
this dated proof as future deletion authorization.
