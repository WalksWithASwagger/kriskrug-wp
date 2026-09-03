# Issue #480 — apply-ready inline-CSS retirement pack

**Lane:** Track A. **No live WordPress writes in this pack.** Bodies only.
**Issue:** [#480](https://github.com/WalksWithASwagger/kriskrug-wp/issues/480) (step 7 of the Aurora stylesheet rebuild).
**Built:** 2026-08-16, from logged-out public HTML + public REST `content.rendered`.
**Reconfirm:** 2026-08-17 against live Aurora **1.6.8** — [`issue-480-apply-ready-20260817.md`](../../../../docs/current-state/reports/issue-480-apply-ready-20260817.md). Cream-pack still not live. **Not applied.**
**Photography recut:** 2026-08-18 after live #827. `photography.html` coda now keeps rows 11–14 (`the whole archive, twenty years of it` + `the fashion and model years, 2006 to 2008`). Other five payloads unchanged. Still do not PATCH.
**This session did not snapshot and did not PATCH.** The next apply agent must snapshot first.

This directory is a sibling of `wp-payloads/` on purpose. `scripts/tests/test_content_architecture_payloads.py` forbids `kk-*` / `kkx-*` class prefixes on every `*.html` under `wp-payloads/`. Live `/contact/`, `/services/`, `/photography/`, `/speaking/`, and `/work/` still use those namespaces. These payloads keep the live markup and only remove the anonymous `<style>` block (including every dead `::first-letter` suppression). Putting them under `wp-payloads/` would fail the payload guard.

Do not apply the already-rewritten aurora-primitive files in `wp-payloads/{contact,services,speaking,work}.html` as a substitute for this pack. Those are a different visual system from what is live today. This pack does not invent a new design.

## Public REST slug / ID pairs (GET only, 2026-08-16)

Confirmed with `GET https://kriskrug.co/wp-json/wp/v2/pages?slug=…&_fields=id,slug,status,link,modified,title`. `?slug=services` returns `[]`. The nav route `/services/` 301s to `/generative-ai-services/`.

| Route | REST slug | Page ID | Status | `modified` (REST) | Payload |
|---|---|---:|---|---|---|
| `/about/` | `about` | 1208 | publish | 2026-08-01T09:59:39 | `about.html` |
| `/speaking/` | `speaking` | 1887 | publish | 2026-07-24T17:22:56 | `speaking.html` |
| `/work/` | `work` | 2672 | publish | 2026-08-12T18:09:48 | `work.html` |
| `/services/` → `/generative-ai-services/` | `generative-ai-services` | 2666 | publish | 2026-07-24T17:05:37 | `services.html` |
| `/photography/` | `photography` | 12013 | publish | 2026-07-24T17:23:03 | `photography.html` |
| `/contact/` | `contact` | 2418 | publish | 2026-07-24T17:05:35 | `contact.html` |

Before any PATCH: re-GET the slug, confirm exactly one page, confirm `id` matches this table, then snapshot that ID. Never PATCH on an unverified slug match ([incident 2026-05-15](../../../../docs/current-state/INCIDENT-2026-05-15-overwritten-post.md)).

## What was stripped

Each payload is live `content.rendered` with:

- the one anonymous page-content `<style>…</style>` removed
- every `::first-letter` / `p::first-letter` suppression deleted with that block (dead after Aurora 1.5.9 / PR #672)
- Jetpack `data-recalc-dims` attributes dropped
- `<!-- wp:html -->` wrapper added so the body is apply-ready

No new classes, no new copy, no new visual design. Photography's Flickr CTA arrow (`→`) is restored from the keynotes source pack; live rendered HTML had mangled it to `?`.

## Apply gates (do not skip)

Cream-pack chrome is **not live**. Logged-out readback 2026-08-16:

- Distinctive selector `aurora-card[style*="--service-ribbon"]` is absent from live `style.css`, live `revive-port.css`, and the Boost bundle `8d99a2084d.min.css`.
- Distinctive selector `aurora-button:not(.aurora-button-primary):not(.aurora-button-secondary)` is absent from the same three surfaces.
- No `cream-pack` string and no Code Snippets style id on the homepage HTML.

Do **not** tell a later agent that cream-pack is already deployed. `fixes/aurora-cream-pack-chrome.css` still exists in the repo only.

| Payload | Apply now? | Why |
|---|---|---|
| `speaking.html`, `work.html` | After cream-pack (or an equivalent theme token for plain `.aurora-button` + 2px card radius / no shadow) | Inner markup is already aurora primitives. The stripped block was first-letter (dead) + those two chrome rules. |
| `about.html` | After cream-pack **and** a theme landing zone for `.aurora-about-page` hero layout + `#aurora-about-title` light-on-photo color | Theme 1.6.5 already styles `.aurora-hero-2026` kicker / dek / secondary button. It does **not** hide `.aurora-page-header`, full-bleed the about hero, or paint `#aurora-about-title` light. Applying now regresses the portrait hero. |
| `contact.html`, `services.html`, `photography.html` | **Blocked** until Track B lands the live namespaces | `kk-contact-*`, `kk-services-*`, and `kkx-*` have no layout CSS in the theme (revive-port only remaps cream tokens on `.kk-contact-2026` / `.kk-page`). Cream-pack does not cover these classes. Applying these three un-designs the pages. |

## Leftover declarations (theme token vs regress)

Dead, do not migrate: every `::first-letter` / `initial-letter` `!important` rule on all six routes.

| Route | Still needed after strip | Already in live theme 1.6.5? | Cream-pack covers? |
|---|---|---|---|
| `/about/` | Hide `.aurora-page-header`; `overflow-x: clip`; full-bleed hero (`100vw` breakout); 145% left-anchor crop; about copy measure; about `h2` clamp | Partial: generic `.aurora-hero-2026` + home-only 145% **right**-anchor. `#aurora-about-title` is only listed for transparent background, not light fill. | Plain `.aurora-button` in the proof CTA only |
| `/speaking/`, `/work/` | Plain `.aurora-button` ink/paper + hover; `.aurora-card` / `.aurora-media-card` `border-radius: 2px` and `box-shadow: none` | No for the plain button. Cards have other theme rules. | Yes |
| `/services/` | Entire `.kk-services-2026` system (palette locals, ribbon grid, proof cards, CTA button) | No (`kk-services-2026` = 0 hits in live theme CSS) | No |
| `/contact/` | Entire `.kk-contact` / `.kk-contact-2026` layout (hero grid, cards, buttons, photo) | Palette remap only (4 hits in `revive-port.css`). No hero/grid/button rules. | No |
| `/photography/` | Entire `.kkx` system (hero, masonry, shot hover, coda button) | No (`kkx-hero` = 0 hits) | No |

Palette locals (`--kk-ink`, `--paper`, `--accent`, …) map to existing Revive / `theme.json` tokens (`--revive-ink`, `--revive-surface`, `--revive-accent`, `--wp--preset--color--paper`). Do not re-declare them in page content.

## Apply order for the next agent

1. Snapshot each of the six IDs (slug-verified). This session did not have `WP_USER` / `WP_APP_PASSWORD` and did not snapshot.
2. Deploy `fixes/aurora-cream-pack-chrome.css` as a front-end CSS snippet **if** speaking / work / about are in the apply set. It is not live today. Do not deploy it a second time if a later readback finds the distinctive selectors above.
3. Do **not** apply contact / services / photography until Track B has a landing zone for those namespaces (or KK accepts the visual loss).
4. PATCH body only. No `title` field. Slug-verify immediately before each write.
5. Purge Pagely + Boost. Logged-out readback: zero page-content `<style>` on the six routes; visual check the hero / ribbons / masonry.
6. Rollback = restore the pre-edit snapshot via REST to the same slug-verified ID.

## Out of scope

- `/publications/` (1895), `/sponsor-deck/` (12625), `/events/` (2250) also carry anonymous page-content `<style>` blocks. They are not in #480. Do not bundle them here.
- Theme / plugins / `inc/` / cream-pack file edits.
- The existing `wp-payloads/{about,contact,services,speaking,work}.html` files (about still has a repo-side `<style>` that is **not** byte-identical to live).
