# Issue #480 — inline page-content CSS retirement (apply-ready prep)

**Captured:** 2026-08-16T20:57Z–21:00Z, logged out, cache-busted (`?cb=480readback`).
**Issue:** [#480](https://github.com/WalksWithASwagger/kriskrug-wp/issues/480). Step 7 of [`AURORA-STYLESHEET-REBUILD-PLAN.md`](../AURORA-STYLESHEET-REBUILD-PLAN.md).
**Lane:** Track A. **Zero live WordPress writes.** No REST POST/PATCH. No publisher scripts.
**Payloads:** [`content/source-packs/content-architecture-2026/issue-480-retire-inline-css/`](../../../content/source-packs/content-architecture-2026/issue-480-retire-inline-css/)
**This session did not take page snapshots.** Creds were unset. The next apply agent snapshots first.

PR #672 (Aurora 1.5.9) retired the theme drop cap. The six live `::first-letter { … !important }` rules are dead. This pack strips those blocks from apply-ready bodies and records what else would regress.

## Live theme readback

Public `https://kriskrug.co/wp-content/themes/kk-aurora/style.css` on 2026-08-16:

| | Value |
|---|---|
| `Version` | **1.6.5** |
| Bytes | 111,718 |
| md5 | `af4097590b97f9dd703c3db97d670bf2` |
| Repo `main` `theme/kk-aurora/style.css` | **1.6.6**, same byte length, **not** byte-identical |

Live `revive-port.css` is byte-identical to repo `main` (31,561 bytes, md5 `53ff15f7b9e3f219ebebf52186fdc97d`). Boost bundle on the homepage: `https://s5102.pcdn.co/wp-content/boost-cache/static/8d99a2084d.min.css` (131,031 bytes).

Do not treat the repo 1.6.6 line as production proof. The public `style.css` readback is 1.6.5.

## Per-route evidence (page-content `<style>` only)

Method: logged-out GET of each route, plus `GET /wp-json/wp/v2/pages?slug=…&_fields=id,slug,status,link,modified,content`. Byte counts are the CSS **inside** the page-content `<style>` (tags excluded), matching the 2026-08-02 inventory method. Each of the six pages has exactly one such block in `content.rendered`.

Every route also renders a **second** anonymous `<style>` in the document body (1,004 inner bytes, 0 `!important`, no `::first-letter`) that starts `.aurora-woven-marquee { height: 6px; … }`. That block is theme header chrome, not post content. It is **not** in this pack and must not be PATCHed away.

| Route | HTTP | REST slug | ID | Style inner B | `!important` | `::first-letter` | Namespace | Live `modified` |
|---|---|---|---:|---:|---:|---|---|---|
| `/about/` | 200 | `about` | 1208 | 3,490 | 25 | yes (1 rule) | `.aurora-about-page` | 2026-08-01T09:59:39 |
| `/speaking/` | 200 | `speaking` | 1887 | 959 | 14 | yes (1 rule) | `.kk-r9-pack` | 2026-07-24T17:22:56 |
| `/work/` | 200 | `work` | 2672 | 959 | 14 | yes (1 rule) | `.kk-r9-pack` | 2026-08-12T18:09:48 |
| `/services/` | **301** → `/generative-ai-services/` | `generative-ai-services` | 2666 | 4,418 | 13 | yes (1 rule) | `.kk-services-2026` | 2026-07-24T17:05:37 |
| `/photography/` | 200 | `photography` | 12013 | 5,024 | 12 | yes (1 rule) | `.kkx` | 2026-07-24T17:23:03 |
| `/contact/` | 200 | `contact` | 2418 | 5,422 | 17 | yes (2 rules) | `.kk-contact` / `.kk-contact-2026` | 2026-07-24T17:05:35 |
| **Six-route total** | | | | **20,272** | **95** | **7 rules** | | |

`GET …/pages?slug=services` returned `[]`. Page 2666 owns `generative-ai-services` only.

`::first-letter` `!important` share (dead after #475 / PR #672): about 8, speaking 8, work 8, services 8, photography 8, contact 10 (two selectors). Remaining `!important` is palette / button / card / hero-color fighting.

`/about/` is still 3,490 B, not the 959 B in the original issue table. That matches the 2026-08-02 comment on #480.

## Cream-pack chrome is not live

`fixes/aurora-cream-pack-chrome.css` is repo-only. It is **not** on the live front end as of this readback. Do not skip deploying it, and do not tell the next agent it is already shipped.

Evidence:

| Probe | Result |
|---|---|
| Homepage HTML contains `cream-pack` / `cream pack` | **false** |
| Homepage style `id=` list | Jetpack Boost + WP block / global-styles only. No Code Snippets style id. |
| `aurora-card[style*="--service-ribbon"]` in live `style.css` | **0** |
| same selector in live `revive-port.css` | **0** |
| same selector in Boost `8d99a2084d.min.css` | **0** |
| `aurora-button:not(.aurora-button-primary):not(.aurora-button-secondary)` in those three surfaces | **0** |

Cream-pack still matters for **speaking / work / about** (plain `.aurora-button` ink/paper + 2px card radius). It does **not** cover `.kk-contact-*`, `.kk-services-*`, or `.kkx-*`. Deploying it again after a later readback finds those selectors would be a duplicate; that is not the case today.

## What the payloads strip vs what still needs a theme token

Payloads are live `content.rendered` minus the page-content `<style>`. They contain **zero** `<style>` and **zero** `::first-letter` rules.

| Route | Stripped (do not put back) | Still needed as a theme token (apply would regress) |
|---|---|---|
| `/about/` | Dead first-letter (8 `!important`). Hero light-ink rules that already exist on `.aurora-hero-2026` for kicker / dek / secondary button in live `revive-port.css`. | Hide `.aurora-page-header`; full-bleed 100vw hero; 145% **left**-anchor crop (theme home crop is **right**-anchor only); about copy measure; about `h2` clamp; `#aurora-about-title` light fill (theme lists the id for transparent background only); plain `.aurora-button` on the proof CTA. |
| `/speaking/`, `/work/` | Dead first-letter (8 `!important` each). | Plain `.aurora-button` cream treatment; `.aurora-card` / `.aurora-media-card` `border-radius: 2px` + `box-shadow: none`. Cream-pack is the existing landing zone and is not live. |
| `/services/` | Dead first-letter (8). Palette locals (`--kk-ink` etc.) that already exist as `--revive-*` / `theme.json` paper/ink/signal. | The whole `.kk-services-2026` layout: ribbon grid, ribbon `::before`, proof cards, CTA button. **0** hits in live theme CSS. |
| `/contact/` | Dead first-letter (2 rules). Palette locals. | The whole `.kk-contact` / `.kk-contact-2026` layout: hero grid, photo, cards, buttons. Live theme only remaps cream tokens on `.kk-contact-2026` (4 hits in `revive-port.css`). |
| `/photography/` | Dead first-letter (8). Palette locals. | The whole `.kkx` cinematic hero + masonry + coda. **0** hits for `kkx-hero` in live theme CSS. |

Do not apply the aurora-primitive files already in `wp-payloads/{contact,services,speaking,work}.html` as the #480 write. Those are a different visual system from live (live contact/services still use the R7/R8 pack namespaces; live work was updated 2026-08-12 and is larger than the repo pack).

## Apply order

1. **Snapshot first**, slug-verified, per [INCIDENT-2026-05-15](../INCIDENT-2026-05-15-overwritten-post.md). This session did not snapshot.
2. **Cream-pack chrome first** if speaking / work / about are in the apply set. It is not live. File: `fixes/aurora-cream-pack-chrome.css`. Front-end CSS snippet, or fold into theme on Track B and drop the snippet.
3. Apply `speaking.html` and `work.html` only after step 2 (or an equivalent theme token).
4. Apply `about.html` only after step 2 **and** a theme landing zone for `.aurora-about-page` hero layout + `#aurora-about-title` light-on-photo color. Otherwise the portrait hero regresses.
5. **Do not apply** `contact.html`, `services.html`, or `photography.html` until Track B lands those namespaces. Cream-pack will not save them.
6. PATCH `content` only. No `title`. Re-GET `?slug=` immediately before each write; abort unless exactly one page and the ID matches the table above.
7. Purge Pagely + Boost. Logged-out grep: zero page-content `<style>` on the six routes.

**Rollback:** restore the pre-edit snapshot via REST to the same slug-verified ID. Do not re-paste CSS from memory.

## Out of scope (do not bundle)

The 2026-08-02 inventory found three more anonymous page-content blocks that #480 does not own: `/publications/` (1895, 15,386 B), `/sponsor-deck/` (12625, 7,752 B), `/events/` (2250, 2,182 B). Left alone.

## Writes from this session

None to WordPress. Repo-only: the six payloads, `page-map.json`, and the pack README. Live apply is still owed; cite `Refs #480`, not `Fixes`.
