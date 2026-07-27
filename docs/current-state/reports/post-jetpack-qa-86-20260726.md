# Post-Jetpack real-site QA — Issue #86

**Captured:** `2026-07-26T20:40Z`–`20:44Z` UTC  
**Mode:** public / read-only (no live writes, no wp-admin, no cache purge)  
**Base URL:** `https://kriskrug.co`  
**Live theme readback:** Aurora `1.4.8` (`/wp-content/themes/kk-aurora/style.css`)  
**WP generator:** `WordPress 7.0.2`  
**Branch:** `cursor/86-post-jetpack-qa-f196`

## Verdict

Core public smoke, Work redirects, GA4 + Google verification, and desktop Lighthouse are **PASS**. Accessibility is **mixed**: structure/keyboard/reduced-motion signals pass; WCAG contrast fails on homepage service kickers and Contact mailto. Mobile lab LCP remains the main performance gap (track under #125 / #127). Meta Pixel is present alongside GA4 — confirm intentional with KK.

## QA matrix

| # | Acceptance / check | Result | Evidence |
|---|---|---|---|
| 1 | Public smoke `/` `/about/` `/blog/` `/work/` `/contact/` | **PASS** | All `200`, 0 redirect hops |
| 2 | `/robots.txt` `/llms.txt` | **PASS** | Both `200` |
| 3 | `/sitemap.xml` → `/wp-sitemap.xml` | **PASS** | 1× `301` then `200` XML index |
| 4 | `/wp-sitemap.xml` | **PASS** | `200` |
| 5 | `/projects/` → `/work/` one hop | **PASS** | 1× `301` `Location: /work/` |
| 6 | `/recent-projects-include/` → `/work/` one hop | **PASS** | 1× `301` `Location: /work/` |
| 7 | GA4 `G-X7JE8B32L7` on sampled HTML | **PASS** | Present on `/` `/about/` `/blog/` `/work/` `/contact/` + `gtag/js?id=G-X7JE8B32L7` |
| 8 | Google site verification meta | **PASS** | `meta name="google-site-verification"` on all five routes |
| 9 | No Jetpack core / wp.com stats in public HTML | **PASS** | No `plugins/jetpack/`, `stats.wp.com`, or `pixel.wp.com` |
| 10 | Jetpack Boost still serving | **PASS** | `x-jetpack-boost-cache: hit` + bundled `boost-cache` CSS/JS on core routes |
| 11 | Desktop Lighthouse Home / About | **PASS** | Perf `97` / `98`; LCP ~1.2s; TBT `0`; CLS `0` |
| 12 | Mobile Lighthouse Home / About | **FAIL** | Perf `71` / `78`; LCP `3.7s` / `5.0s` (lab) |
| 13 | LCP / CLS / TBT / Speed Index recorded | **PASS** | See Lighthouse + TTFB tables below; INP **UNKNOWN** (not emitted in these lab runs) |
| 14 | Keyboard skip-link + focus ring | **PASS** | First Tab → `.skip-link` → `#aurora-main`; `outline: 2px solid` |
| 15 | `prefers-reduced-motion` CSS present | **PASS** | Theme `style.css` + Boost bundle; CDP emulate `reduce` matches |
| 16 | Contrast spot (pa11y WCAG2AA) | **FAIL** | Home: 3× `.aurora-kicker` `2.45:1`; Contact mailto `4.24:1` |
| 17 | Single `h1` / landmark basics | **PASS** | One `h1` + `main#aurora-main` on five routes |
| 18 | Console / page JS errors (CDP + LH) | **PASS** | `0` exceptions / LH console errors on sampled profiles |
| 19 | Meta / Facebook Pixel present | **UNKNOWN** (intent) | Pixel `1720755522050230` + `fbq` + noscript `facebook.com/tr` on all five — confirm wanted |

---

## 1. Public route smoke

| Route | Status | Redirect hops | Final URL | Cache (sample) |
|---|---:|---:|---|---|
| `/` | 200 | 0 | `https://kriskrug.co/` | Boost `hit` / Gateway `HIT` |
| `/about/` | 200 | 0 | `…/about/` | Boost `hit` / Gateway `HIT` |
| `/blog/` | 200 | 0 | `…/blog/` | Boost `hit` / Gateway `HIT` |
| `/work/` | 200 | 0 | `…/work/` | Boost `hit` / Gateway `HIT` |
| `/contact/` | 200 | 0 | `…/contact/` | Boost `hit` / Gateway `HIT` |
| `/robots.txt` | 200 | 0 | `…/robots.txt` | — |
| `/llms.txt` | 200 | 0 | `…/llms.txt` | — |
| `/sitemap.xml` | 200 | **1** | `…/wp-sitemap.xml` | `301` → core sitemap |
| `/wp-sitemap.xml` | 200 | 0 | `…/wp-sitemap.xml` | — |
| `/projects/` | 200 | **1** | `…/work/` | `301` → `/work/` |
| `/recent-projects-include/` | 200 | **1** | `…/work/` | `301` → `/work/` |

`robots.txt` advertises a single sitemap line: `Sitemap: https://kriskrug.co/sitemap.xml` (stale Jetpack news/image sitemap lines from the 2026-07-01 cleanup report are gone).

---

## 2. Tracking tags (HTML-visible)

Sampled routes: `/`, `/about/`, `/blog/`, `/work/`, `/contact/`.

| Marker | Result |
|---|---|
| GA4 `G-X7JE8B32L7` | **PASS** (all five) |
| `googletagmanager.com/gtag/js?id=G-X7JE8B32L7` | **PASS** |
| `google-site-verification` meta | **PASS** |
| Meta Pixel `fbq` / `connect.facebook.net` / `facebook.com/tr?id=1720755522050230` | **PRESENT** (all five) |
| Site Kit classnames in HTML | Not required for pass — GA4 ships without `google-site-kit` string in markup |
| `stats.wp.com` / Jetpack core plugin assets | **ABSENT** (**PASS**) |
| Third-party script hosts (external) | `www.googletagmanager.com`, Pagely CDN `s5102.pcdn.co` (+ FB pixel network) |

---

## 3. Performance

### 3a. TTFB baseline (`make performance-audit`, `SAMPLES=3`, `2026-07-26T20:40:18Z`)

| Route | Cold TTFB | Warm TTFB | Warm total | Bytes | Cache |
|---|---:|---:|---:|---:|---|
| `/` | 0.707s | 0.063s | 0.078s | 82 102 | Boost hit / Gateway HIT |
| `/about/` | 0.691s | 0.068s | 0.082s | 54 848 | Boost hit / Gateway HIT |
| `/blog/` | 0.251s | 0.065s | 0.093s | 124 326 | Boost hit / Gateway HIT |
| `/work/` | 0.212s | 0.066s | 0.079s | 56 904 | Boost hit / Gateway HIT |
| `/contact/` | 0.222s | 0.064s | 0.078s | 58 956 | Boost hit / Gateway HIT |

Cold TTFB remains well under the pre-Jetpack-off multi-second regime (historical cold p50 was ~3.7s). Warm path is sub-100 ms TTFB.

### 3b. Lighthouse (Chrome 148 + Lighthouse 12.8.2 via shared CDP port)

| URL | Profile | Perf | A11y | FCP | LCP | CLS | TBT | Speed Index | INP | Console errs |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `/` | desktop | **97** | 96 | 0.54s | **1.18s** | 0 | 0 ms | 0.72s | — | 0 |
| `/` | mobile | **71** | 96 | 1.00s | **3.71s** | **0.246** | 292 ms | 1.47s | — | 0 |
| `/about/` | desktop | **98** | 95 | 0.51s | **1.16s** | 0 | 0 ms | 0.60s | — | 0 |
| `/about/` | mobile | **78** | 95 | 1.88s | **5.03s** | 0 | 143 ms | 2.72s | — | 0 |

Notes:

- Desktop LCP is comfortably under 2.5 s.
- Mobile lab LCP is still the primary CWV risk (LCP element home: `h1#aurora-home-title`; about: proof-section body copy). Image weight audits still flag large responsive-image savings (~400–600 KiB).
- Home mobile CLS `0.246` exceeds the “good” 0.1 threshold in this lab run (layout-shift element list empty in LH details — treat as needs re-check on #125/#127).
- INP was not populated by these lab navigations → **UNKNOWN** for field INP; use CrUX / Search Console for production INP.
- Unthrottled CDP paint metrics (warm, no CPU/network throttle) were much faster (home LCP ~0.3 s) and are **not** a substitute for the Lighthouse mobile numbers above.

### 3c. CDP interaction smoke (supplement)

On `/`, `/about/`, `/blog/`, `/work/`, `/contact/` (desktop) plus home/about mobile viewports:

- Skip link focuses on first Tab with visible 2 px outline.
- `prefers-reduced-motion: reduce` emulation reports `matchMedia` true.
- Blog desktop recorded CLS `0.17` in the unthrottled CDP pass (supporting “watch CLS on listing surfaces”).
- Page JS exception count: **0** across these profiles.

---

## 4. Accessibility

### 4a. Structure (HTML)

| Route | `lang` | `h1` count | Skip link | `main` |
|---|---|---:|---|---:|
| `/` | `en-US` | 1 | `Skip to content` → `#aurora-main` | 1 |
| `/about/` | `en-US` | 1 | same | 1 |
| `/blog/` | `en-US` | 1 | same | 1 |
| `/work/` | `en-US` | 1 | same | 1 |
| `/contact/` | `en-US` | 1 | same | 1 |

Theme CSS (`style.css` v1.4.8): `:focus`, `:focus-visible`, `prefers-reduced-motion`, and `.skip-link` rules present. Live pages load CSS via Jetpack Boost combined bundle `c2441c2909.min.css`.

Only “missing alt” images found were the Meta Pixel `1×1` `facebook.com/tr` beacons (tracking pixel, not content imagery).

### 4b. pa11y WCAG2AA (`npx pa11y --standard WCAG2AA`)

| Route | Issues | Detail |
|---|---:|---|
| `/` | **3** | `.aurora-kicker` “I. / II. / III.” contrast **2.45:1** (need ≥4.5:1) under `#services` |
| `/about/` | 0 | clean |
| `/blog/` | 0 | clean |
| `/work/` | 0 | clean |
| `/contact/` | **1** | `a.kk-contact-email` mailto contrast **4.24:1** (need ≥4.5:1) |

Lighthouse accessibility scores (95–96) align: `color-contrast` audit score `0` on Home/About profiles.

---

## 5. Console / third-party regressions

- Lighthouse `errors-in-console`: **0** on all four Home/About profiles.
- CDP `Runtime.exceptionThrown` / `console.error`: **0** on seven sampled navigations.
- No Jetpack Stats beacon regression observed.
- Active third parties in public HTML: GA4 (gtag), Meta Pixel, Pagely/Boost static assets. No Clarity/Hotjar/GTM container id observed.

---

## KK follow-ups

1. **Mobile LCP / CLS (#125, #127)** — Keep #86’s performance acceptance open on mobile lab LCP (`~3.7s` home / `~5.0s` about) and home mobile CLS `0.246`. Desktop is already in good shape. Prioritize hero/masthead + image weight (`uses-responsive-images` savings).
2. **Contrast remediation (Track B)** — Fix homepage `.aurora-kicker` roman numerals (`2.45:1`) and Contact `.kk-contact-email` (`4.24:1`). Prior #293 is closed; these are **new/regressed** contrast offenders relative to the 2026-07-02 clean pa11y pass.
3. **Meta Pixel intent** — Confirm pixel `1720755522050230` should remain post-Jetpack. If unwanted, remove via snippet/plugin owner (not done in this read-only pass).
4. **Field INP / CrUX** — Lab INP unavailable here. KK: check Search Console / Site Kit CWV for real-user INP on Home + About.
5. **Manual visual pass (optional closeout)** — Keyboard path beyond first Tab, reduced-motion visual confirmation, and mobile viewport eyeballing still benefit from a human pass (#424 hover/focus QA overlaps).
6. **Do not close #86** until contrast fails are fixed and mobile LCP is either improved or explicitly accepted / moved to #125 with KK sign-off.

---

## Method / artifacts (agent-local, not committed)

- Public probe JSON: `/tmp/kk-86-qa/public-probe.json`, `redirects-theme.json`
- Performance audit: `/tmp/kk-86-qa/performance-audit.json` (`ROUTES='/,/about/,/blog/,/work/,/contact/' SAMPLES=3`)
- Lighthouse JSON: `/tmp/kk-86-qa/lighthouse/{home,about}-{desktop,mobile}.json`
- pa11y JSON: `/tmp/kk-86-qa/pa11y/{home,about,blog,work,contact}.json`
- CDP metrics: `/tmp/kk-86-qa/cdp-metrics.json`

**Out of scope this run:** wp-admin plugin inventory, Boost Critical CSS admin UI, cache purge, form submissions, authenticated Site Kit settings.
