# Issue #480 — apply-ready reconfirm (2026-08-17)

**Captured:** 2026-08-17T06:30Z, logged out, cache-busted public GET + public REST. **GET only.**
**Issue:** [#480](https://github.com/WalksWithASwagger/kriskrug-wp/issues/480). Still open. **Not applied. Not closed.**
**Prior evidence:** [`issue-480-inline-css-retirement-2026-08-16.md`](issue-480-inline-css-retirement-2026-08-16.md) (live theme then **1.6.5**). Payloads from PR #794 remain on `main`.
**Lane:** Track A reconfirm. **Zero live WordPress writes.** No REST POST/PATCH/DELETE. No SFTP. No Code Snippets. No theme edits.
**Payloads:** [`content/source-packs/content-architecture-2026/issue-480-retire-inline-css/`](../../../content/source-packs/content-architecture-2026/issue-480-retire-inline-css/) — **not recut**.

This pass exists because the 2026-08-16 pack was cut against Aurora 1.6.5. Live is now **1.6.8**. The question is whether the six bodies, the cream-pack gate, and the apply order still hold.

## Live theme readback (do not use the repo Version as proof)

Public `https://kriskrug.co/wp-content/themes/kk-aurora/style.css` on 2026-08-17:

| | 2026-08-16 report | This readback |
|---|---|---|
| `Version` | **1.6.5** | **1.6.8** |
| Bytes | 111,718 | 111,718 |
| md5 | `af4097590b97f9dd703c3db97d670bf2` | `a02cf12be8ec9f9fe31bc59363fc3147` |
| Repo `theme/kk-aurora/style.css` | 1.6.6, same length, not byte-identical to live | **1.6.8**, **byte-identical** to this live file (`a02cf12be8ec…`) |

Live `revive-port.css`: 44,858 bytes, md5 `e10e375afbfed1302e248dcf847ba1c9`, byte-identical to repo `main`. That is a real grow from the 2026-08-16 live file (31,561 / `53ff15f7…`) — homepage 1.6.8 work, not cream-pack.

Boost bundle on `/`: `https://s5102.pcdn.co/wp-content/boost-cache/static/0f9e6b2840.min.css` (142,158 bytes). The 2026-08-16 bundle was `8d99a2084d.min.css` (131,031). Hash moved with the 1.6.8 homepage HTML write; that is not a Boost critical-CSS regen (#731 still owed).

`?slug=services` is still `[]`. `/services/` still **301** → `/generative-ai-services/`. Page 2666 owns `generative-ai-services` only.

## Cream-pack chrome is still not live

`fixes/aurora-cream-pack-chrome.css` is still repo-only. **Do not tell the next agent it is deployed.**

#845 / #690 landed the editor swatch alias `Cream Elevated (same as Panel)` in `theme.json` (hex unchanged). That is **not** the cream-pack chrome file. An alias in the palette picker does not paint plain `.aurora-button` or 2px riso cards.

| Probe | Result |
|---|---|
| Homepage HTML contains `cream-pack` / `cream pack` | **false** |
| Homepage `style id=` list | Jetpack Boost + WP block / global-styles only. No Code Snippets style id. |
| `aurora-card[style*="--service-ribbon"]` in live `style.css` | **0** |
| same selector in live `revive-port.css` | **0** |
| same selector in Boost `0f9e6b2840.min.css` | **0** |
| `aurora-button:not(.aurora-button-primary):not(.aurora-button-secondary)` in those three surfaces | **0** |
| Live `revive-port.css` `kk-services-2026` / `kkx-hero` / `aurora-about-title` | **0 / 0 / 0** |
| Live `revive-port.css` `kk-contact-2026` | **4** (palette remap only; same as 2026-08-16) |

`--service-ribbon` still exists on homepage `.aurora-service-card` in `revive-port.css`. That is not the cream-pack `aurora-card[style*="--service-ribbon"]` rule.

## Per-route evidence (page-content `<style>` only)

Same method as 2026-08-16: logged-out GET plus `GET /wp-json/wp/v2/pages?slug=…&_fields=id,slug,status,link,modified,content`. Inner bytes are CSS inside the page-content `<style>` (tags excluded). Each of the six pages still has exactly one such block in `content.rendered`.

Every route still also renders the theme-header anonymous `<style>` that starts `.aurora-woven-marquee { height: 6px; … }` (1,004 inner bytes, 0 `!important`, no `::first-letter`). **Not in this pack. Do not PATCH it away.**

| Route | HTTP | REST slug | ID | Style inner B | `!important` | `::first-letter` | Namespace | Live `modified` | vs pack |
|---|---|---|---:|---:|---:|---|---|---|---|
| `/about/` | 200 | `about` | 1208 | 3,490 | 25 | yes (1) | `.aurora-about-page` | 2026-08-16T21:29:03 | drifted |
| `/speaking/` | 200 | `speaking` | 1887 | 959 | 14 | yes (1) | `.kk-r9-pack` | 2026-08-16T21:29:32 | drifted |
| `/work/` | 200 | `work` | 2672 | 959 | 14 | yes (1) | `.kk-r9-pack` | 2026-08-16T21:30:05 | drifted |
| `/services/` | **301** → `/generative-ai-services/` | `generative-ai-services` | 2666 | 4,418 | 13 | yes (1) | `.kk-services-2026` | 2026-07-24T17:05:37 | **same** |
| `/photography/` | 200 | `photography` | 12013 | 5,024 | 12 | yes (1) | `.kkx` | 2026-08-16T21:30:00 | drifted |
| `/contact/` | 200 | `contact` | 2418 | 5,422 | 17 | yes (2) | `.kk-contact` / `.kk-contact-2026` | 2026-08-16T21:30:03 | drifted |
| **Six-route total** | | | | **20,272** | **95** | **7 rules** | | | |

Style inner bytes, `!important` counts, `::first-letter` counts, and namespaces are **unchanged** from the 2026-08-16 table. All six still have inline page-content CSS. **Still has `<style>`: yes / yes / yes / yes / yes / yes.**

`modified` drifted on five IDs. That matches the #706 PressCACHE no-op title-saves (`1208`, `1887`, `12013`, `2418`, `2672`; plus `3930` which is not in this pack). Titles and slugs were unchanged. Page 2666 was not in that list and its `modified` is still the pack timestamp.

## Payload recut verdict: do not recut

All six payloads still contain **zero** `<style>` and **zero** `::first-letter` rules.

| Payload | Normalized match to live minus `<style>` | Recut? |
|---|---|---|
| `about.html` | yes | no |
| `speaking.html` | yes | no |
| `work.html` | no — sole diff is Jetpack `&amp;` vs live `&#038;` on one image query string | no |
| `services.html` | yes | no |
| `photography.html` | no — known Flickr CTA `→` restore vs live `?` (same as 2026-08-16) | no |
| `contact.html` | yes | no |

Live HTML did not meaningfully diverge. `modified` drift is a timestamp, not a body rewrite. Do not invent a new design. Do not recut.

Do **not** apply the aurora-primitive files under `wp-payloads/{contact,services,speaking,work}.html` as a substitute. Those are still a different visual system from live.

## Apply order (gates unchanged)

**Nothing in this pack is apply-now.** Cream-pack is still not on the front end. Track B still has not landed `.kk-contact-*` / `.kk-services-2026` / `.kkx-*` layout.

1. **Snapshot first**, slug-verified, per [INCIDENT-2026-05-15](../INCIDENT-2026-05-15-overwritten-post.md). This session did not snapshot.
2. **Cream-pack chrome first** if speaking / work / about are in the apply set. File: `fixes/aurora-cream-pack-chrome.css`. Still not live. Front-end CSS snippet, or fold into theme on Track B and drop the snippet.
3. Apply `speaking.html` and `work.html` only after step 2 (or an equivalent theme token for plain `.aurora-button` + 2px card radius / no shadow).
4. Apply `about.html` only after step 2 **and** a theme landing zone for `.aurora-about-page` hero layout + `#aurora-about-title` light-on-photo color. Otherwise the portrait hero regresses.
5. **Do not apply** `contact.html`, `services.html`, or `photography.html` until Track B lands those namespaces. Cream-pack will not save them.
6. PATCH `content` only. No `title`. Re-GET `?slug=` immediately before each write; abort unless exactly one page and the ID matches the table above. Expect the five drifted `modified` values; do not treat timestamp drift alone as a recut trigger.
7. Purge Pagely + Boost. Logged-out grep: zero page-content `<style>` on the six routes.

**Rollback:** restore the pre-edit snapshot via REST to the same slug-verified ID. Do not re-paste CSS from memory.

| Payload | Apply now? | Why |
|---|---|---|
| `speaking.html`, `work.html` | **Blocked** — after cream-pack | Inner markup is already aurora primitives. Cream-pack still not live. |
| `about.html` | **Blocked** — after cream-pack **and** about-hero tokens | Theme 1.6.8 still does not hide `.aurora-page-header`, full-bleed the about hero, or paint `#aurora-about-title` light. |
| `contact.html`, `services.html`, `photography.html` | **Blocked** until Track B lands the live namespaces | `kk-contact-*`, `kk-services-*`, and `kkx-*` still have no layout CSS in the theme. |

## Collision with #827 (page 12013)

[#827](https://github.com/WalksWithASwagger/kriskrug-wp/issues/827) owns the photography-hub write surface: page **12013** block 23 (archive link + fashion-years link to post 1056). This reconfirm: live `/photography/` still has **zero** `https://kriskrug.co/…` hrefs. The #827 anchors (`the whole archive, twenty years of it`, `the fashion and model years, 2006 to 2008`) are **not** on live and are **not** in `photography.html`.

If #827 lands first, applying this pack's `photography.html` would wipe those two links unless the payload is recut from the post-#827 body. **Sequence: do not apply `photography.html` until Track B lands `.kkx` anyway; if #827 writes 12013 before that, recut `photography.html` from the new live HTML (strip `<style>` only; keep the new links). Do not fold #827 anchors into this pack in the #480 lane.**

#827 itself says leave the inline `<style>` on 12013 unchanged. The two issues can coexist only if the later writer starts from the then-current body.

## Out of scope (unchanged)

`/publications/` (1895), `/sponsor-deck/` (12625), `/events/` (2250) still carry anonymous page-content `<style>` blocks. #480 does not own them.

## Writes from this session

None to WordPress. Repo-only: this report. Live apply is still owed; cite `Refs #480`, not `Fixes`. **Not applied.**
