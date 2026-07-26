# Perf Boost Stabilization (#125) — 2026-07-26

**Mode:** plan + public probes only (no wp-admin writes, no Boost regenerate, no PressCACHE purge, no theme edits)  
**Issue:** [#125](https://github.com/WalksWithASwagger/kriskrug-wp/issues/125) — Post-Jetpack performance stabilization + Boost Critical CSS cleanup  
**Branch:** `cursor/125-perf-boost-plan-f196`  
**Probe window:** ~2026-07-26T20:40Z  
**Base URL:** `https://kriskrug.co`

## Verdict

Post-Jetpack cold/warm TTFB gains are still holding on the five core routes. Jetpack core frontend remnants remain gone. Jetpack Boost is still active and shipping a single large concatenated CSS bundle (`c2441c2909.min.css`, **138 157 B**).

The actionable smell is **Critical CSS coverage drift**: `#jetpack-boost-critical-css` is present on `/` and `/blog/` only. About, Work, Contact, and sampled articles load the full Boost CSS without an inline critical sheet (and without the deferred `media=print`/`onload` pattern used on home/blog). Tag-archive Boost misses remain low-risk and should not be treated as homepage TTFB cause.

**Do not regenerate Critical CSS from this pass until KK opens Boost UI, confirms the warning surface, and only then regenerates if the UI is stable.**

## Live vs repo versions

| Surface | Version |
| --- | --- |
| Live public `kk-aurora/style.css` | **1.4.8** |
| Live Pagely CDN `s5102.pcdn.co/.../style.css` | **1.4.8** |
| Repo `theme/kk-aurora/style.css` | **1.4.8** |
| Public generator meta | WordPress **7.0.2** |

Theme line is in sync (no pending Aurora deploy lag on this readback).

## Acceptance checklist status (public-only)

| Criterion | Status | Note |
| --- | --- | --- |
| Fresh cold/warm probes for `/`, `/about/`, `/blog/`, `/work/`, `/contact/` | Done | 3 cold (cache-busted) + 3 warm each |
| Record TTFB, total time, cache headers, redirects, bytes | Done | Tables below |
| Check Jetpack Boost UI / Critical CSS warning | **Blocked** | Needs KK wp-admin; public evidence substitutes below |
| Do not trigger another Boost regeneration unless UI stable | Honored | No admin actions this pass |
| Tag-archive warning → document/dismiss as low-risk | Done | See Critical CSS / tags |
| Confirm Jetpack core inactive; Boost/Protect/Site Kit active | **Public proxy** | Core assets absent; Boost + Site Kit markers present; Protect REST namespace present. Plugin active list still needs KK admin glance |
| Close only after speed gain holds across repeated samples | **Not yet** | Gains hold in this sample; leave #125 open until KK UI check + optional regenerate + re-measure |

## Route probe (p50 of 3)

Cold = `?_cb=<epochms>` cache-bust. Warm = canonical URL.

| Route | HTTP | Redirects | Cold TTFB | Cold total | Cold bytes | Warm TTFB | Warm total | Warm bytes | Warm cache |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `/` | 200 | 0 | 0.833s | 0.847s | 82102 | 0.064s | 0.079s | 82102 | Boost `hit` / Gateway `HIT` |
| `/about/` | 200 | 0 | 0.709s | 0.723s | 54848 | 0.065s | 0.079s | 54848 | Boost `hit` / Gateway `HIT` |
| `/blog/` | 200 | 0 | 0.338s | 0.366s | 124398 | 0.051s | 0.090s | 124326 | Boost `miss` / Gateway `HIT` |
| `/work/` | 200 | 0 | 0.205s | 0.219s | 56904 | 0.064s | 0.082s | 56904 | Boost `hit` / Gateway `HIT` |
| `/contact/` | 200 | 0 | 0.186s | 0.200s | 58956 | 0.065s | 0.080s | 58956 | Boost `hit` / Gateway `HIT` |
| `/2026/07/18/i-am-nomad-ai-film/` | 200 | 0 | 0.225s | 0.252s | 107405 | 0.065s | 0.096s | 107405 | Boost `hit` / Gateway `HIT` |
| `/2026/07/10/the-cheer-is-a-cap-table/` | 200 | 0 | 0.643s | 0.673s | 100944 | 0.070s | 0.099s | 100944 | Boost `hit` / Gateway `HIT` |
| `/tag/sxsw/` | 200 | 0 | 0.327s | 0.340s | 64045 | 0.065s | 0.079s | 64045 | Boost `miss` / Gateway `HIT` |
| `/tag/itunes/` | 200 | 0 | 0.608s | 0.623s | 53808 | 0.065s | 0.079s | 53808 | Boost `miss` / Gateway `HIT` |

Cold probes were consistently Boost `miss` + Gateway `MISS` (expected under cache-bust). Warm gateway cache is healthy on core routes.

### vs 2026-07-01 / 2026-07-02 baselines

| Checkpoint | Home cold TTFB p50 | Home warm TTFB p50 |
| --- | ---: | ---: |
| Pre Jetpack-off (2026-07-01) | ~3.7s | ~0.5s |
| Post Jetpack-off | 0.635s | 0.363s |
| 2026-07-02 (Aurora 1.3.33) | 0.698s | 0.422s |
| **This probe (2026-07-26)** | **0.833s** | **0.064s** |

Interpretation: still far below the Jetpack-core penalty era. Warm is excellent. Cold home is a bit noisier than mid-July samples but remains sub-second and not a regression to the 3–4s class.

## Critical CSS / Boost smells (public HTML)

### Coverage matrix

| Surface | `#jetpack-boost-critical-css` | Crit bytes | Deferred full CSS (`media=print`→onload) | Boost static CSS hash | Boost static CSS bytes |
| --- | --- | ---: | --- | --- | ---: |
| `/` | Yes | 7474 | Yes | `c2441c2909` | 138157 |
| `/blog/` | Yes | 15332 | Yes | `c2441c2909` | 138157 |
| `/about/` | **No** | 0 | No | `c2441c2909` | 138157 |
| `/work/` | **No** | 0 | No | `c2441c2909` | 138157 |
| `/contact/` | **No** | 0 | No | `c2441c2909` | 138157 |
| Article (Nomad AI film) | **No** | 0 | No | `c2441c2909` | 138157 |
| Article (cheer / cap table) | **No** | 0 | No | `c2441c2909` | 138157 |
| `/tag/sxsw/`, `/tag/itunes/` | **No** | 0 | No | `c2441c2909` | 138157 |

### Smells

1. **Missing Critical CSS on high-value non-home templates** — About / Work / Contact / singles get only the full `c2441c2909.min.css` as a normal stylesheet. Home/blog still get inline critical + deferred full CSS. This is the primary Boost cleanup target for KK.
2. **Large concatenated CSS** — one sitewide Boost bundle at **~135 KiB** (compressed transfer still material on mobile LCP). Bundle includes current Aurora selectors (`aurora-home-2026`, `aurora-single-2026`, `aurora-writing-archive`, `aurora-hero-2026`, `skip-link`, `prefers-reduced-motion`) so it is not an obviously stale 1.3.x leftover, but it is heavy.
3. **Duplicate stylesheet link on `/` and `/blog/`** — same `c2441c2909` id/href appears twice (blocking + deferred). Expected Boost pattern when critical CSS is present; absent on pages without critical CSS.
4. **One render-blocking Boost JS** on home: `753a7e1c9e.min.js` (~21 KiB). Other routes use `1351e44c36.min.js` (~20 KiB). No `whenGsapReady` / old GSAP console-warn strings in these bundles (GSAP not present in sampled public HTML).
5. **Tag archives** — warm Boost `miss` + no critical CSS. Matches the historical “failed tag archives” Critical CSS set from 2026-07-01 deep diagnostic. Gateway still `HIT`. Treat as **low-risk / dismissible** unless Boost UI shows a blocking error on core pages.
6. **`/blog/` warm Boost `miss` with Gateway `HIT`** — odd but not a TTFB problem in this sample (warm TTFB 0.051s). Worth a KK glance in Boost Page Cache UI; do not clear caches solely for this header.

### Critical CSS content sanity (where present)

- Home critical includes `.aurora-home*`, `.aurora-hero*`, header/nav, `prefers-reduced-motion`.
- Blog critical includes `.aurora-writing-archive` / theme/archive selectors and `prefers-reduced-motion`.
- Historical article critical was previously very large (~60 KiB in June). Articles currently have **zero** critical CSS — regenerate should restore modest single-template critical sheets, not paste home CSS everywhere.

## Jetpack remnant sniff (public)

| Marker | `/` | `/about/` | `/blog/` | `/work/` | `/contact/` | Articles |
| --- | --- | --- | --- | --- | --- | --- |
| `pixel.wp.com` / `stats.wp.com` | Absent | Absent | Absent | Absent | Absent | Absent |
| Sharedaddy / likes | Absent | Absent | Absent | Absent | Absent | Absent |
| Jetpack form blocks | Absent | Absent | Absent | Absent | Absent | Absent |
| `/jetpack/` plugin CSS/JS paths | Absent | Absent | Absent | Absent | Absent | Absent |
| Boost (`boost-cache`, critical id, tokens) | Present | Present | Present | Present | Present | Present |
| Site Kit GA4 `G-X7JE8B32L7` | Present | Present | Present | Present | Present | Present |
| Contact mailto CTA | — | — | — | — | Present (`feelmoreplants@gmail.com`) | — |

`/wp-json/` still advertises `jetpack/v4`, `jetpack-boost/*`, `jetpack-protect/v1`, `my-jetpack/v1`, `google-site-kit/v1`. REST namespaces alone do **not** prove Jetpack core is active (Boost/Protect/My Jetpack packages register overlapping routes). Public HTML remains the better inactive-core signal until KK confirms plugins in wp-admin.

## Large CSS inventory (public)

| Asset | HTTP | Bytes |
| --- | ---: | ---: |
| Boost `.../c2441c2909.min.css` | 200 | **138157** |
| Theme `style.css` (direct) | 200 | 117636 |
| `assets/css/revive-port.css` | 200 | 28670 |
| `assets/css/typography-refined.css` | 200 | 16735 |
| `assets/css/bleeding-edge.css` | 200 | 12390 |
| `assets/css/animations.css` | 200 | 7540 |
| `assets/css/editor.css` | 200 | 5343 |

Logged-out pages do not link the split theme CSS files directly; Boost concatenation owns the delivered CSS. Theme `style.css` Version header is still the deploy/version readback source of truth.

Inline style totals (global styles + block supports + optional critical): home ~48 KiB across 17 `<style>` tags; articles ~56 KiB across 25 tags (mostly core block/library CSS, not Boost critical).

## KK actionable cleanup checklist

Do these in order. Stop if Boost UI is mid-generation or erroring.

### A. Admin read-only (5–10 min)

1. **Plugins:** Confirm `jetpack/jetpack` inactive; `jetpack-boost`, `jetpack-protect`, `google-site-kit` active. Do not reactivate Jetpack core.
2. **Jetpack Boost → Critical CSS:** Record whether the UI warns. If warning URLs are only `/tag/*` (or other low-traffic archives), **dismiss / accept as low-risk** — do not chase as homepage TTFB.
3. **Jetpack Boost → modules:** List enabled features. Candidates to leave on: Critical CSS, Page Cache (if stable). Candidates to consider turning **off** if unused/noisy: Image CDN / LCP image optimization leftovers that no longer apply post-Jetpack, deferred JS experiments that fight Pagely, any “concatenate JS” if it keeps a blocking `boost-cache` script on every page without measured win.
4. **Screenshot / note** generated-file count and last generation time before changing anything.

### B. Conditional Critical CSS regenerate (only if A is stable)

5. If UI is stable **and** failed items are understood (or limited to tags), regenerate Critical CSS once.
6. Expected public outcome after regenerate + cache settle:
   - `#jetpack-boost-critical-css` returns on `/about/`, `/work/`, `/contact/`, and at least one recent single.
   - Home/blog critical stay present and still include current Aurora selectors.
   - Boost static hash may change from `c2441c2909`; record the new hash.
7. **PressCACHE purge** after theme/Boost changes (Pagely). Do **not** rely on Boost clear-cache REST (historically `403 rest_forbidden`).
8. Do **not** stack multiple regenerations. One pass, then measure.

### C. Measurement commands (after B, or anytime for baseline)

From repo root (credential-free public probes):

```bash
# Core routes, markdown to stdout
make performance-audit ROUTES='/,/about/,/blog/,/work/,/contact/' SAMPLES=3

# Include longform single
LONGFORM_URL='https://kriskrug.co/2026/07/18/i-am-nomad-ai-film/' \
  make performance-audit ROUTES='/,/about/,/blog/,/work/,/contact/' SAMPLES=3

# Live theme version readback
curl -sS 'https://kriskrug.co/wp-content/themes/kk-aurora/style.css' | head -n 12

# Critical CSS presence (expect non-empty on about/work/contact/article after regenerate)
for u in / /about/ /blog/ /work/ /contact/ /2026/07/18/i-am-nomad-ai-film/; do
  echo -n "$u "
  curl -sS "https://kriskrug.co$u" \
    | python3 -c 'import sys,re; t=sys.stdin.read(); m=re.search(r"id=\"jetpack-boost-critical-css\"[^>]*>(.*?)</style>",t,re.S); print(len(m.group(1).encode()) if m else 0)'
done

# Boost CSS hash + size on home
curl -sS 'https://kriskrug.co/' | grep -oE 'boost-cache/static/[a-f0-9]+\.min\.css' | sort -u
curl -sS -o /dev/null -w '%{http_code} %{size_download}\n' \
  'https://s5102.pcdn.co/wp-content/boost-cache/static/c2441c2909.min.css'
```

Optional browser lab (KK laptop): Lighthouse mobile on `/` and one article; track LCP/TBT/CLS. Prior mobile LCP pain was image/font/network cost, not TTFB.

### D. Close criteria for #125

- [ ] KK recorded Boost Critical CSS UI state (warn vs clean; which URLs).
- [ ] Tag-only failures explicitly accepted as low-risk **or** cleared by regenerate.
- [ ] Critical CSS present again on About / Work / Contact / a sample single (public grep above).
- [ ] Repeated `make performance-audit` still shows sub-second cold TTFB on core routes (no return to ~3–4s).
- [ ] Jetpack core still inactive; no Sharedaddy / wp.com stats / Jetpack form markers on public HTML.

## Out of scope this pass

- wp-admin changes, Boost regenerate, PressCACHE purge
- Theme CSS/JS edits, GSAP CDN decisions, mobile LCP image work
- Deleting inactive `jetpack/jetpack` (still the rollback seat until KK closes the stability window)
- Contact form plugin replacement

## Artifact note

Raw probe JSON used for this report was generated in the agent workspace at `/tmp/perf125-20260726/probe-results.json` (not committed). Re-run the measurement block above to refresh numbers after any Boost/theme change.

## Disposition

Keep **#125 open**. Public evidence says the Jetpack-off win held and Boost is the remaining cleanup surface — specifically Critical CSS gaps on non-home templates plus a large sitewide Boost CSS bundle. Next human step is the KK Boost UI check in checklist A, then a single regenerate only if stable.
