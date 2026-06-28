# Asset Diet — reduce unused CSS/JS (2026-06-28)

**Trigger:** Google Search Console / PageSpeed flagged "Reduce unused CSS" and "Reduce unused JavaScript," pointing at WordPress plugins loading assets on pages that don't use them.

**Outcome:** One reversible Code Snippet (`KK Asset Diet`, id 10, front-end) now strips the unused plugin payloads site-wide. Homepage went from **2 CSS + 12 JS** requests to **1 CSS + 4 JS**. Live-verified, tests green, key pages cache-purged.

---

## What was actually true (vs the stale audit)

`docs/current-state/SEO_AUDIT.md` (2026-05-14) blamed "Catch Responsive theme ~50K inline CSS." **That theme is gone** — the site runs the `kk-aurora` block theme, whose CSS/JS Jetpack Boost already concatenates + minifies into `boost-cache/static/*` bundles. The theme is not the problem.

Live HTML inspection (homepage, /about/, a post, /contact/) showed the reducible weight was entirely **plugin JavaScript loading on every page**:

| Asset | Loaded on | Action taken |
|---|---|---|
| Jetpack Instant Search (`jp-search.js`, served unminified) + `hooks`/`i18n`/`i18n-loader` deps | every page | disabled `search` module → core WP search |
| Jetpack Carousel + Swiper | gallery pages | disabled `carousel` module |
| Jetpack Sharing (`sharedaddy/sharing.min.js`) | posts | disabled `sharedaddy` module |
| Popup Maker (`popup-maker-site` JS + CSS, auto-popup #3884) | every page | `pum_popup_is_loadable` → false + dequeue |
| jQuery Migrate | every page | deregistered on front end |

CSS was already healthy (Boost defers non-critical CSS); the fat was in JS.

## Implementation

`fixes/asset-diet-snippet.php` is the source of truth, mirrored into Code Snippets entry **id 10** (front-end scope) on production. Deployed over the `code-snippets/v1` REST API using the WP Application Password — kriskrug.co accepts app-password auth on that namespace (no nonce needed, unlike bc-ai.ca). The snippet:

1. `add_filter('jetpack_active_modules', …)` — removes `search`, `carousel`, `sharedaddy`.
2. `wp_default_scripts` — drops `jquery-migrate` from jQuery's deps on the front end.
3. `pum_popup_is_loadable => __return_false` + `wp_dequeue_*('popup-maker-site')` — retires the site-wide auto-popup #3884 and its assets.

Reversible: deactivate/delete snippet 10 to restore everything.

## Before → after (per page, verified cache-bypassed)

| Page | Before | After |
|---|---|---|
| Homepage / About | 2 CSS, 12 JS | **1 CSS, 4 JS** |
| Blog post | 2 CSS, ~13 JS | **1 CSS, 5 JS** |
| Contact | form assets | form assets preserved |

## Verification

- **Core search works:** `/?s=vancouver` → 200 with 19 results; public smoke `/?s=ai` → PASS. Replacing Instant Search did not break search.
- **No fatals live:** `scripts/wp7-public-smoke.py` PASS on `/`, `/blog/`, `/speaking/`, `/work/`, `/contact/`, `/wp-json/`, `/sitemap.xml`, `/?s=ai`.
- **Snippet health:** id 10 active, `code_error: null`; the other 8 snippets untouched.
- **Repo tests:** `make test` green (31 + 57 unit tests, plugin smoke); `phpcs` clean on the new file.
- **Contact form** (Jetpack/grunion) assets still load on /contact/ only.

## Cache purge

Pagely-ARES edge has no REST purge route and Jetpack Boost's cache routes are nonce-gated (403 with the app password). Purged the key surface via the repo's established no-op-save method (a title re-save fires `save_post` → per-URL ARES purge + Boost CSS regen): **homepage + 7 nav pages + 8 most-recent posts (16/16), all now serve fresh with zero stale-asset markers.** The long-tail archive refreshes on Pagely's TTL, or via a Pagely Atomic "Purge All" for instant total.

## Follow-ups (optional)

- **jQuery itself** still loads. With Popup Maker, search, carousel, and sharing gone it may now have no consumer — worth a browser-console check, then a possible dequeue for a further win.
- **Stale dead CSS rules** (`.pum-overlay`, `jp-carousel`, `swiper`) linger in Boost's inlined bundle until it regenerates; they match nothing in the DOM and add no request.
- **Services page** isn't at slug `services`; it wasn't in the purge set (TTL will refresh it).
