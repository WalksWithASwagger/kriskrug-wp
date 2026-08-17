# Issue #480 — apply-ready CHECK (2026-08-17)

**Verdict:** **still apply-ready** as a prep pack. **Not apply-now.**
**DO NOT PATCH.** No live WordPress write. No REST POST/PATCH/DELETE.
**Captured:** 2026-08-17T06:30:07Z, logged out, cache-busted (`?cb=480applyready20260817`).
**Issue:** [#480](https://github.com/WalksWithASwagger/kriskrug-wp/issues/480). Gate 1 of [`WORK-PLAN-2026-08-17.md`](../WORK-PLAN-2026-08-17.md). Step 7 of [`AURORA-STYLESHEET-REBUILD-PLAN.md`](../AURORA-STYLESHEET-REBUILD-PLAN.md).
**Prior evidence:** [`issue-480-inline-css-retirement-2026-08-16.md`](issue-480-inline-css-retirement-2026-08-16.md) (PR #794, merged). That capture recorded live Aurora **1.6.5**. Public `style.css` today is **1.6.8**.
**Payloads:** [`content/source-packs/content-architecture-2026/issue-480-retire-inline-css/`](../../../content/source-packs/content-architecture-2026/issue-480-retire-inline-css/) — not rewritten this session.
**Lane:** Track A docs. This session did not snapshot, did not PATCH, and did not touch `theme/`, `plugins/`, or `inc/`.

---

## Headline

The six owned routes still serve the same page-content `<style>` inner-byte / `!important` / `::first-letter` table as 2026-08-16. REST id/slug pairs still match `page-map.json`. Cream-pack chrome is still **not** live. Track B still has no landing zone for `.kk-services-2026`, `.kkx-hero`, or the `.kk-contact` layout.

Applying any of the six payloads today would still un-design the page (contact / services / photography) or regress cream-button / card chrome and the about portrait hero (speaking / work / about). The pack stays apply-ready **after** those gates, not before.

---

## DO NOT PATCH

Do **not** PATCH `content` on pages 1208, 1887, 2672, 2666, 12013, or 2418 from this report.

Do **not** delete or edit the live anonymous `<style>` blocks.

Do **not** treat “still apply-ready” as permission to write. The next apply agent snapshots first, re-GETs `?slug=` immediately before each write, aborts unless exactly one page and the ID matches the table below, and only proceeds after the apply gates in the pack README.

Rollback, if a later session does write: restore the pre-edit snapshot via REST to the same slug-verified ID. Do not re-paste CSS from memory.

---

## Live theme readback

Public `https://kriskrug.co/wp-content/themes/kk-aurora/style.css?cb=480applyready20260817` on 2026-08-17T06:30:07Z:

| | 2026-08-16 report | 2026-08-17 this CHECK |
|---|---|---|
| `Version` | **1.6.5** | **1.6.8** |
| Bytes | 111,718 | 111,718 (same length, different bytes) |
| md5 | `af4097590b97f9dd703c3db97d670bf2` | `a02cf12be8ec9f9fe31bc59363fc3147` |
| Repo `theme/kk-aurora/style.css` | **1.6.6**, same length, **not** byte-identical | **1.6.8**, **byte-identical** to live |

Do not treat the repo Version as production proof. The public `style.css` readback is 1.6.8. After the 2026-08-17 Aurora deploy it happens to match repo `main`.

Public `revive-port.css`: 44,858 bytes, md5 `e10e375afbfed1302e248dcf847ba1c9`, byte-identical to repo `main`. The 2026-08-16 file was 31,561 bytes (`53ff15f7b9e3f219ebebf52186fdc97d`). The growth is the 1.6.8 homepage/Revive layer, not cream-pack and not the R7–R11 page namespaces.

Boost bundle on the homepage: `https://s5102.pcdn.co/wp-content/boost-cache/static/0f9e6b2840.min.css` (142,158 bytes). 2026-08-16 used `8d99a2084d.min.css` (131,031 bytes). Expected after the 1.6.8 homepage HTML write. Not a cream-pack deploy.

---

## Cream-pack chrome is still not live

Same distinctive-selector probes as 2026-08-16, all still **0** in live `style.css`, live `revive-port.css`, and Boost `0f9e6b2840.min.css`:

| Probe | Result |
|---|---|
| Homepage HTML contains `cream-pack` / `cream pack` | **false** |
| Homepage style `id=` list | Jetpack Boost + WP block / global-styles only. No Code Snippets style id. |
| `aurora-card[style*="--service-ribbon"]` | **0** in those three CSS surfaces |
| `aurora-button:not(.aurora-button-primary):not(.aurora-button-secondary)` | **0** in those three CSS surfaces |

`fixes/aurora-cream-pack-chrome.css` still exists in the repo only (3,431 bytes). Aurora 1.6.8 did not ship it.

Namespace hits in live theme CSS (public files, not repo-as-proof):

| Selector | `style.css` | `revive-port.css` |
|---|---:|---:|
| `kk-services-2026` | 0 | 0 |
| `kkx-hero` | 0 | 0 |
| `kk-r9-pack` | 0 | 0 |
| `aurora-about-page` | 0 | 0 |
| `kk-contact-2026` | 0 | 4 (palette remap only; no hero/grid/button layout) |
| `#aurora-about-title` | 1 (transparent background on `.aurora-hero-2026` copy, not light fill) | 0 |
| `aurora-hero-2026` | 3 | 6 |

Home hero 145% crop is still **right**-anchor (`.aurora-home-2026 .aurora-hero-media img`). About's 145% **left**-anchor still lives only in the page-content `<style>`.

---

## Per-route evidence (page-content `<style>` only)

Method: logged-out GET of each route (`?cb=480applyready20260817`), plus `GET /wp-json/wp/v2/pages?slug=…&_fields=id,slug,status,link,modified,title,content`. Byte counts are the CSS **inside** the page-content `<style>` (tags excluded), matching the 2026-08-02 / 2026-08-16 method. HTML and REST `content.rendered` agreed on every inner-byte / `!important` / `::first-letter` figure below.

Every route also renders the theme woven-marquee anonymous `<style>` (1,004 inner bytes, 0 `!important`, no `::first-letter`) starting `.aurora-woven-marquee { height: 6px; … }`. That block is header chrome, not post content. It is **not** in this pack and must not be PATCHed away.

| Route | HTTP | REST slug | ID | Style inner B | `!important` | `::first-letter` | Namespace | Live `modified` | vs 2026-08-16 |
|---|---|---|---:|---:|---:|---|---|---|---|
| `/about/` | 200 | `about` | 1208 | 3,490 | 25 | yes (1 rule) | `.aurora-about-page` | 2026-08-16T21:29:03 | CSS **same**; `modified` newer |
| `/speaking/` | 200 | `speaking` | 1887 | 959 | 14 | yes (1 rule) | `.kk-r9-pack` | 2026-08-16T21:29:32 | CSS **same**; `modified` newer |
| `/work/` | 200 | `work` | 2672 | 959 | 14 | yes (1 rule) | `.kk-r9-pack` | 2026-08-16T21:30:05 | CSS **same**; `modified` newer |
| `/services/` | **301** → `/generative-ai-services/` | `generative-ai-services` | 2666 | 4,418 | 13 | yes (1 rule) | `.kk-services-2026` | 2026-07-24T17:05:37 | CSS **same**; `modified` unchanged |
| `/photography/` | 200 | `photography` | 12013 | 5,024 | 12 | yes (1 rule) | `.kkx` | 2026-08-16T21:30:00 | CSS **same**; `modified` newer |
| `/contact/` | 200 | `contact` | 2418 | 5,422 | 17 | yes (2 rules) | `.kk-contact` / `.kk-contact-2026` | 2026-08-16T21:30:03 | CSS **same**; `modified` newer |
| **Six-route total** | | | | **20,272** | **95** | **7 rules** | | | **identical to 2026-08-16** |

`GET …/pages?slug=services` returned `[]`. Page 2666 owns `generative-ai-services` only. `/services/?cb=…` nofollow: HTTP **301**, `Location: /generative-ai-services/?cb=480applyready20260817`.

`::first-letter` `!important` share (still dead after #475 / PR #672): about 8, speaking 8, work 8, services 8, photography 8, contact 10 (two selectors). Remaining `!important` is still palette / button / card / hero-color fighting.

Five of six REST `modified` stamps moved ~30 minutes **after** the 2026-08-16T20:57Z–21:00Z capture (services did not). The page-content CSS table did not move with them. This CHECK treats that as a save/touch, not a CSS-pack invalidation. The next apply agent still re-GETs `?slug=` immediately before any write.

---

## REST ids / slugs vs `page-map.json`

| Route | Map ID | Live ID | Map slug | Live slug | Status | Markers in `content.rendered` |
|---|---:|---:|---|---|---|---|
| `/about/` | 1208 | 1208 | `about` | `about` | publish | all 6 present |
| `/speaking/` | 1887 | 1887 | `speaking` | `speaking` | publish | all 4 present |
| `/work/` | 2672 | 2672 | `work` | `work` | publish | all 4 present |
| `/services/` → `/generative-ai-services/` | 2666 | 2666 | `generative-ai-services` | `generative-ai-services` | publish | all 4 present |
| `/photography/` | 12013 | 12013 | `photography` | `photography` | publish | all 3 present |
| `/contact/` | 2418 | 2418 | `contact` | `contact` | publish | all 4 present |

Exactly one page per owned slug. No slug collision.

---

## Payload identity vs live `content.rendered`

Each pack file still has **zero** `<style>` and **zero** `::first-letter`. Compared to live REST after stripping the one anonymous page-content `<style>` and collapsing blank lines left by that strip:

| Payload | Squeezed body vs live | Notes |
|---|---|---|
| `about.html` | **identical** | |
| `speaking.html` | **identical** | |
| `work.html` | equivalent | three Jetpack image query strings are `&amp;` in the payload and `&#038;` in live REST. Same URL. |
| `services.html` | **identical** | |
| `photography.html` | one intentional glyph | live CTA still `Flickr ?`; payload still restores `Flickr →` (already documented in the pack README). |
| `contact.html` | **identical** | |

Do **not** apply `wp-payloads/{contact,services,speaking,work}.html` as the #480 write. Those are still a different visual system from live.

This session did not rewrite payloads. The `&#038;` encoding is REST rendering, not a reason to refresh `work.html`. The photography arrow remains the documented live-vs-payload glyph fix.

---

## What would regress if PATCHed today

Same gates as 2026-08-16. Aurora 1.6.8 did not land the missing tokens.

| Route | If PATCHed from this pack today | Why |
|---|---|---|
| `/about/` | Portrait hero regresses: page header returns, hero stays in the prose column, 145% **left**-anchor crop is lost (theme home crop is **right**-anchor only), `#aurora-about-title` loses light-on-photo fill, proof CTA loses plain `.aurora-button` cream ink. Dead first-letter (8 `!important`) is the only safe strip. | `.aurora-about-page` = 0 hits in live theme CSS. Cream-pack not live. |
| `/speaking/`, `/work/` | Plain `.aurora-button` reverts to pre-Revive dark treatment. `.aurora-card` / `.aurora-media-card` lose `border-radius: 2px` + `box-shadow: none`. Dead first-letter (8 `!important` each) is the only safe strip. | Cream-pack distinctive selectors still 0. `.kk-r9-pack` = 0 in live theme CSS. |
| `/services/` | Whole `.kk-services-2026` layout goes: ribbon grid, ribbon `::before`, proof cards, CTA. Page un-designs. | `kk-services-2026` = 0 in live theme CSS. Cream-pack does not cover it. |
| `/contact/` | Whole `.kk-contact` / `.kk-contact-2026` layout goes: hero grid, photo, cards, buttons. Page un-designs. | Live theme only remaps cream tokens on `.kk-contact-2026` (4 hits in `revive-port.css`). |
| `/photography/` | Whole `.kkx` cinematic hero + masonry + coda goes. Page un-designs. Applying would also restore `→` on the Flickr CTA (live still `?`). | `kkx-hero` = 0 in live theme CSS. |

---

## Apply order (unchanged; still not this session)

1. **Snapshot first**, slug-verified, per [INCIDENT-2026-05-15](../INCIDENT-2026-05-15-overwritten-post.md). This session did not snapshot.
2. **Cream-pack chrome first** if speaking / work / about are in the apply set. It is not live. File: `fixes/aurora-cream-pack-chrome.css`.
3. Apply `speaking.html` and `work.html` only after step 2 (or an equivalent theme token).
4. Apply `about.html` only after step 2 **and** a theme landing zone for `.aurora-about-page` hero layout + `#aurora-about-title` light-on-photo color.
5. **Do not apply** `contact.html`, `services.html`, or `photography.html` until Track B lands those namespaces. Cream-pack will not save them.
6. PATCH `content` only. No `title`. Re-GET `?slug=` immediately before each write; abort unless exactly one page and the ID matches the table above.
7. Purge Pagely + Boost. Logged-out grep: zero page-content `<style>` on the six routes.

**This CHECK stops before step 1.**

---

## Out of scope (do not bundle)

`/publications/` (1895), `/sponsor-deck/` (12625), and `/events/` (2250) still sit outside this issue's apply pack. This session did not re-measure them and did not add them to payloads.

---

## Writes from this session

None to WordPress. Repo-only: this receipt, plus a one-line pointer on the 2026-08-16 report. Live apply is still owed; cite `Refs #480`, not `Fixes`.
