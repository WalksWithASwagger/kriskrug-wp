# Perf probe (#125) 2026-08-02

**Issue:** [#125](https://github.com/WalksWithASwagger/kriskrug-wp/issues/125) post-Jetpack performance stabilization + Boost Critical CSS cleanup
**Mode:** public read-only. No wp-admin session, no writes, no cache purge, no Boost regeneration, no theme deploy.
**Branch:** `docs/125-perf-probes`
**Probe window:** 2026-08-02 20:19 to 20:26 PDT (2026-08-03 03:19 to 03:26 UTC)
**Vantage:** KK laptop, Vancouver. Pagely ARES edge answered from `35.168.216.102` (AWS us-east-1). Absolute TTFB here carries roughly 190 ms of cross-continent DNS + TCP + TLS that a us-east-1 probe host would not pay. Server wait time is broken out separately below so the numbers can be compared across vantage points.
**Live versions at probe time:** Aurora `1.5.7` (public `style.css` readback), WordPress `7.0.2`, edge `Pagely-ARES/1.22.28`. Repo `main` is `1.5.8`, matching the known undeployed `aurora-tstm` gap.

## Verdict

The post-Jetpack speed gain holds. Every one of the five core routes returns `200` with zero redirects, warm server wait between 92 and 151 ms, cold server wait between 231 and 373 ms. Nothing is anywhere near the 3 to 4 second Jetpack-core era.

Two things changed since the 2026-07-26 probe, one good and one that needs KK.

Good: `/blog/` warm now reports `x-jetpack-boost-cache: hit`. On 2026-07-26 it was a persistent warm `miss`. That smell is gone without anyone touching it.

Needs KK: **the Boost Critical CSS is stale relative to the live theme.** Aurora went 1.4.8 to 1.5.7 on 2026-08-01 (full-bleed portrait hero, PR #618). The concatenated Boost bundle picked up the new CSS, but the inline critical sheet on `/` did not. Proof is in the crop values: the home critical CSS still carries `object-position: 62% 30%`, a value that commit `b87be22` deleted when it shipped 1.5.7. The live bundle carries the replacement values `68% 26%` and `88% 20%`. So above-the-fold first paint on the homepage is being styled by a pre-hero-rework stylesheet until the deferred bundle lands.

Critical CSS coverage itself is unchanged from 2026-07-26: present on `/` and `/blog/`, absent on `/about/`, `/work/`, `/contact/`. Byte counts are byte-for-byte identical to the 2026-07-26 report (7474 on home, 15332 on blog), which is independent confirmation that no regeneration has run in that window.

Two findings outside the strict probe scope are recorded below because they are the biggest remaining weight and no earlier #125 report named them: the desktop LCP hero resolves to a 1.17 MB JPEG at `fetchpriority="high"`, and a Meta Pixel is loading on all five routes.

## What I could not check, and why

Three acceptance criteria on #125 need a wp-admin session. This lane is public read-only and has none, so they stay open. I am not going to infer them.

| Criterion | Why it is blocked |
| --- | --- |
| "Check Jetpack Boost UI once and record whether Critical CSS still warns" | Needs wp-admin. There is no public surface that reports Boost's generated-file count, its failed-item list, or its warning state. `/wp-json/jetpack-boost/v1/status` returns `404` unauthenticated. |
| "Do not trigger another Boost regeneration unless the UI is stable" | Honored by default. No admin action was taken this pass. |
| "Confirm Jetpack core remains inactive and Boost/Protect/Site Kit remain active" | Partially answerable from public evidence (see below), but the plugin activation list itself is admin-only. The site's MCP adapter returns `{"abilities":[]}`, so there is no read-only tool path to plugin state either. |

## Method

Two independent rounds, five samples per route per pass, roughly four minutes apart. Cold means a `?_cb=<epoch_ms>` cache-bust plus `Cache-Control: no-cache`, which forces the ARES edge to `MISS` and go to origin. Warm means the canonical URL with no query string, edge cache eligible.

All probes used `--compressed`, so `size_download` is gzip wire bytes, not decoded HTML bytes. Both are reported. The 2026-07-26 report recorded decoded bytes, so compare against the uncompressed column, not the wire column.

```bash
BASE="https://kriskrug.co"
ROUTES=(/ /about/ /blog/ /work/ /contact/)
FMT='%{http_code}\t%{num_redirects}\t%{time_namelookup}\t%{time_connect}\t%{time_appconnect}\t%{time_starttransfer}\t%{time_total}\t%{size_download}\t%{url_effective}\n'

for r in "${ROUTES[@]}"; do
  # cold: cache-busted, forces origin
  for i in $(seq 1 5); do
    cb=$(python3 -c 'import time;print(int(time.time()*1000))')
    curl -sS -L -o /dev/null --compressed \
      -H 'Cache-Control: no-cache' -H 'Pragma: no-cache' \
      -w "$FMT" "${BASE}${r}?_cb=${cb}"
  done
  # warm: canonical, edge cache eligible
  for i in $(seq 1 5); do
    curl -sS -L -o /dev/null --compressed -w "$FMT" "${BASE}${r}"
  done
done
```

Header capture, one cold and one warm per route:

```bash
for r in / /about/ /blog/ /work/ /contact/; do
  cb=$(python3 -c 'import time;print(int(time.time()*1000))')
  echo "===== COLD ${r} ====="; curl -sS -D - -o /dev/null --compressed "https://kriskrug.co${r}?_cb=${cb}"
  echo "===== WARM ${r} ====="; curl -sS -D - -o /dev/null --compressed "https://kriskrug.co${r}"
done
```

Byte comparison, wire versus decoded:

```bash
for r in / /about/ /blog/ /work/ /contact/; do
  raw=$(curl -sS -o /dev/null -w '%{size_download}' "https://kriskrug.co$r")
  wire=$(curl -sS -o /dev/null --compressed -w '%{size_download}' "https://kriskrug.co$r")
  printf '%-12s uncompressed=%-8s wire=%-8s\n' "$r" "$raw" "$wire"
done
```

Critical CSS presence and staleness:

```bash
# critical CSS byte count per route
for u in / /about/ /blog/ /work/ /contact/; do
  echo -n "$u "
  curl -sS --compressed "https://kriskrug.co$u" \
    | python3 -c 'import sys,re; t=sys.stdin.read(); m=re.search(r"id=\"jetpack-boost-critical-css\"[^>]*>(.*?)</style>",t,re.S); print(len(m.group(1).encode()) if m else 0)'
done

# staleness proof: crop values in critical CSS vs the deployed bundle
curl -sS --compressed https://kriskrug.co/ \
  | python3 -c 'import sys,re; t=sys.stdin.read(); c=re.search(r"id=\"jetpack-boost-critical-css\"[^>]*>(.*?)</style>",t,re.S).group(1); print(sorted(set(re.findall(r"object-position:[^;}]*",c))))'
curl -sSL --compressed https://s5102.pcdn.co/wp-content/boost-cache/static/ec2a031717.min.css \
  | grep -oE 'object-position:[^;}]*' | sort -u
```

## Results, round 1 (03:19 to 03:20 UTC)

`ttfb` is `time_starttransfer` and includes DNS, TCP, and TLS. `wait` is `time_starttransfer` minus `time_appconnect`, which is the server-side portion only. All values are p50 of 5 samples, seconds.

| Route | Pass | HTTP | Redirects | TTFB p50 | TTFB min | TTFB max | Wait p50 | Total p50 | Wire bytes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `/` | cold | 200 | 0 | 0.531 | 0.512 | 0.630 | 0.366 | 0.532 | 18606 |
| `/` | warm | 200 | 0 | 0.369 | 0.281 | 0.500 | 0.097 | 0.379 | 18606 |
| `/about/` | cold | 200 | 0 | 0.437 | 0.406 | 0.853 | 0.245 | 0.523 | 13056 |
| `/about/` | warm | 200 | 0 | 0.289 | 0.275 | 0.357 | 0.104 | 0.378 | 13056 |
| `/blog/` | cold | 200 | 0 | 0.560 | 0.544 | 0.669 | 0.373 | 0.560 | 20985 |
| `/blog/` | warm | 200 | 0 | 0.362 | 0.270 | 0.391 | 0.099 | 0.381 | 20967 |
| `/work/` | cold | 200 | 0 | 0.421 | 0.399 | 0.429 | 0.231 | 0.421 | 12382 |
| `/work/` | warm | 200 | 0 | 0.365 | 0.285 | 0.799 | 0.151 | 0.377 | 12382 |
| `/contact/` | cold | 200 | 0 | 0.424 | 0.406 | 0.612 | 0.239 | 0.508 | 12944 |
| `/contact/` | warm | 200 | 0 | 0.295 | 0.267 | 0.376 | 0.092 | 0.374 | 12944 |

## Results, round 2 (03:23 to 03:24 UTC)

| Route | Pass | HTTP | Redirects | TTFB p50 | TTFB min | TTFB max | Total p50 | Wire bytes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `/` | cold | 200 | 0 | 0.656 | 0.535 | 0.803 | 0.657 | 18606 |
| `/` | warm | 200 | 0 | 0.274 | 0.271 | 0.379 | 0.362 | 18606 |
| `/about/` | cold | 200 | 0 | 0.416 | 0.402 | 0.601 | 0.504 | 13056 |
| `/about/` | warm | 200 | 0 | 0.300 | 0.287 | 0.391 | 0.383 | 13056 |
| `/blog/` | cold | 200 | 0 | 0.563 | 0.534 | 0.591 | 0.563 | 20986 |
| `/blog/` | warm | 200 | 0 | 0.282 | 0.277 | 0.366 | 0.370 | 20967 |
| `/work/` | cold | 200 | 0 | 0.425 | 0.407 | 0.455 | 0.426 | 12382 |
| `/work/` | warm | 200 | 0 | 0.364 | 0.282 | 0.387 | 0.384 | 12382 |
| `/contact/` | cold | 200 | 0 | 0.450 | 0.400 | 0.742 | 0.538 | 12944 |
| `/contact/` | warm | 200 | 0 | 0.292 | 0.278 | 0.353 | 0.371 | 12944 |

Round 2 matches round 1 inside normal jitter. The only route that moved more than 100 ms at p50 was cold `/` (0.531 to 0.656), and its round 2 min was 0.535, so that is sampling noise on the origin, not a step change.

## Combined, 10 samples per route and pass

| Route | Pass | TTFB p50 | TTFB min | TTFB max | Total p50 | Server wait p50 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `/` | cold | 0.550 | 0.512 | 0.803 | 0.551 | 0.366 |
| `/` | warm | 0.284 | 0.271 | 0.500 | 0.368 | 0.097 |
| `/about/` | cold | 0.428 | 0.402 | 0.853 | 0.516 | 0.245 |
| `/about/` | warm | 0.295 | 0.275 | 0.391 | 0.379 | 0.104 |
| `/blog/` | cold | 0.561 | 0.534 | 0.669 | 0.562 | 0.373 |
| `/blog/` | warm | 0.291 | 0.270 | 0.391 | 0.376 | 0.099 |
| `/work/` | cold | 0.422 | 0.399 | 0.455 | 0.422 | 0.231 |
| `/work/` | warm | 0.365 | 0.282 | 0.799 | 0.380 | 0.151 |
| `/contact/` | cold | 0.437 | 0.400 | 0.742 | 0.524 | 0.239 |
| `/contact/` | warm | 0.293 | 0.267 | 0.376 | 0.374 | 0.092 |

Connection overhead was flat across every sample: DNS 3 to 6 ms, TCP 84 to 90 ms, TLS 93 to 102 ms. That is roughly 190 ms of fixed transport cost from this vantage on every single request, warm or cold.

### Cross-check against the repo's own target

The repo already ships a probe. Running it from the same host at 03:29 UTC agrees with the hand-rolled curl numbers, which is the point of running both.

```bash
make performance-audit ROUTES='/,/about/,/blog/,/work/,/contact/' SAMPLES=3
```

| Route | HTTP | Redirects | Cold TTFB p50 | Cold total p50 | Warm TTFB p50 | Warm total p50 | Bytes | Cache |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `/` | 200 | 0 | 0.548 | 0.648 | 0.357 | 0.516 | 89311 | Boost hit, Gateway HIT |
| `/about/` | 200 | 0 | 0.492 | 0.583 | 0.356 | 0.457 | 58576 | Boost hit, Gateway HIT |
| `/blog/` | 200 | 0 | 0.556 | 0.722 | 0.354 | 0.535 | 124791 | Boost hit, Gateway HIT |
| `/work/` | 200 | 0 | 0.533 | 0.629 | 0.379 | 0.464 | 56904 | Boost hit, Gateway HIT |
| `/contact/` | 200 | 0 | 0.538 | 0.627 | 0.371 | 0.459 | 58956 | Boost hit, Gateway HIT |

Its byte column matches the uncompressed column above exactly, because that target probes without `--compressed`. Its cold TTFB falls inside the observed range of my two rounds on four of five routes. The exception is `/work/`, where it read `0.533` against my range of `0.399` to `0.455`, which puts the whole set of cold p50s inside a 130 ms band regardless of which probe you trust. Its `critical_css_mentions` counter reported `6` and its theme readback reported `1.5.7`, both consistent with the findings below.

## Transferred bytes

| Route | Uncompressed | Gzip wire | Ratio |
| --- | ---: | ---: | ---: |
| `/` | 89311 | 18606 | 4.8x |
| `/about/` | 58576 | 13056 | 4.5x |
| `/blog/` | 124791 | 20967 | 6.0x |
| `/work/` | 56904 | 12382 | 4.6x |
| `/contact/` | 58956 | 12944 | 4.6x |

`content-encoding: gzip` on all five. Brotli is not offered: an explicit `Accept-Encoding: br, gzip` request still comes back `content-encoding: gzip`. Moving the edge to brotli would cut roughly another 15 to 20 percent off HTML transfer, but that is a Pagely configuration question, not something this repo controls.

Against 2026-07-26 decoded bytes: `/` grew 82102 to 89311 (+8.8%, consistent with the 1.5.7 hero markup), `/blog/` 124398 to 124791 (flat), `/work/` 56904 to 56904 (identical), `/contact/` 58956 to 58956 (identical), `/about/` 54848 to 58576 (+6.8%, the About hero payload from PR #618).

## Cache and edge headers

Header set is identical in shape on all five routes. Example, warm `/`:

```
HTTP/2 200
date: Mon, 03 Aug 2026 03:21:05 GMT
content-type: text/html; charset=UTF-8
content-length: 18606
vary: Accept-Encoding
server: Pagely-ARES/1.22.28
x-gateway-request-id: a2882c5c4cde290153b26698d324072a
x-jetpack-boost-cache: hit
vary: Accept-Encoding
content-encoding: gzip
x-gateway-cache-key: 1785657460.595|standard|https|kriskrug.co|||/
x-gateway-cache-status: HIT
x-gateway-skip-cache: 0
```

| Route | Cold `x-gateway-cache-status` | Cold `x-jetpack-boost-cache` | Warm `x-gateway-cache-status` | Warm `x-jetpack-boost-cache` |
| --- | --- | --- | --- | --- |
| `/` | MISS | miss | HIT | hit |
| `/about/` | MISS | miss | HIT | hit |
| `/blog/` | MISS | miss | HIT | hit |
| `/work/` | MISS | miss | HIT | hit |
| `/contact/` | MISS | miss | HIT | hit |

Three notes on the header surface.

1. There is no `cache-control`, no `age`, and no `expires` on the HTML responses. Cache state is only observable through `x-gateway-cache-status` and `x-jetpack-boost-cache`. Anyone writing a future probe should not grep for `cache-control` and conclude the cache is off.
2. `vary: Accept-Encoding` is emitted twice on every response. Harmless duplication, but worth knowing before someone chases it as a bug.
3. `x-gateway-rate-limit-delayed` appeared on two cold requests (`0.245` on `/`, `0.117` on `/blog/`). That is the edge deliberately slowing a burst of cache-busted requests from one client. It is an artifact of probing, not a user-facing latency source, and it inflates cold p50 slightly. Cold numbers here should be read as an upper bound.

## Redirects

Zero redirects on all five canonical routes. Supplementary checks:

| Request | Hops | Final | Status |
| --- | ---: | --- | ---: |
| `http://kriskrug.co/` | 1 | `https://kriskrug.co/` | 200 |
| `https://www.kriskrug.co/` | 1 | `https://kriskrug.co/` | 200 |
| `https://kriskrug.co/about` | 0 | `https://kriskrug.co/about` | 200 |
| `https://kriskrug.co/contact` | 0 | `https://kriskrug.co/contact` | 200 |
| `https://kriskrug.co/sitemap.xml` | 1 | `https://kriskrug.co/wp-sitemap.xml` | 200 |

The slashless variants serve `200` rather than redirecting to the trailing-slash canonical. The `<link rel="canonical">` on both `/about` and `/about/` points at `/about/`, so search engines get the right signal, but two URLs serve the same body. That is a URL hygiene item, not a perf item, and it belongs to the SEO lane (#274), not here. Flagging only, not touching.

## Assets loaded on the public page

Every one of the five routes declares the same small set of subresources in markup: one stylesheet, one Boost JS bundle, one GA4 tag, and one inline Meta Pixel bootstrap that injects a fourth request at runtime.

**Stylesheets, one, shared by all five routes:**

| Asset | HTTP | Uncompressed | Gzip wire |
| --- | ---: | ---: | ---: |
| `s5102.pcdn.co/wp-content/boost-cache/static/ec2a031717.min.css` | 200 | 142406 | 25075 |

**Scripts, two distinct bundles plus GA4:**

| Asset | Used on | HTTP | Uncompressed | Gzip wire |
| --- | --- | ---: | ---: | ---: |
| `boost-cache/static/5ada0d03dd.min.js` | `/` | 200 | 21150 | 5708 |
| `boost-cache/static/4882321c23.min.js` | `/about/`, `/blog/`, `/work/`, `/contact/` | 200 | 20365 | 5420 |
| `googletagmanager.com/gtag/js?id=G-X7JE8B32L7` | all five | 200 | n/a | n/a |

**Inline `<style>` totals** (WP global styles, block supports, plus critical CSS where present): `/` 50797 B, `/blog/` 55311 B, `/contact/` 38588 B, `/about/` 36656 B, `/work/` 34125 B.

Absent from all five rendered pages, and from both Boost JS bundles: GSAP, ScrollTrigger, Popup Maker frontend code, jQuery, any `googlesitekit` frontend bundle. GA4 is delivered as a direct `gtag` tag. The Google site verification meta is present (`nT4GJiTjalxw1bqaK2VtOksFqHi6V_M28eA4q0l0FPo`). A WP core `speculationrules` prefetch block is present on all five routes.

### One third-party tag the earlier reports did not name

All five routes carry an inline **Meta Pixel** bootstrap, `fbq('init', '1720755522050230')` followed by `fbq('track', 'PageView')`, plus a `<noscript>` tracking image at `facebook.com/tr?id=1720755522050230`. The bootstrap injects `connect.facebook.net/en_US/fbevents.js` as an async script at runtime, so it does not show up in a scan of `<script src=...>` in the served HTML. That is why the 2026-07-26 asset inventory missed it, and it is worth naming here because #125 explicitly says "avoid reintroducing frontend/script bloat."

It is async, so it does not block render, and it is not a TTFB factor. Whether it should still be there is KK's call, not this lane's. Flagging only.

## Image weight, the largest remaining lever

TTFB and HTML bytes are in good shape. Images are not. The cross-check run of `make performance-audit` surfaced two heavy assets tied to the 1.5.7 hero work, both verified independently.

| Asset | Where | Role | Bytes |
| --- | --- | --- | ---: |
| `krug-1.jpg?w=2000` | `/` and `/about/` hero | LCP candidate, `fetchpriority="high"` | 1167330 |
| `krug-1.jpg?w=1280` | same, srcset candidate | | 269907 |
| `krug-1.jpg?w=640` | same, srcset candidate | | 65506 |
| `hero.png` (full size) | `/` newsletter card, `src` fallback | featured image | 2222547 |
| `hero.png?w=1024` | same, largest srcset candidate | | 465140 |

Two specifics worth recording.

1. The hero portrait is served with `sizes="100vw"` and `fetchpriority="high"`. On a wide desktop viewport that resolves to the 2000w candidate at **1.17 MB**, fetched at high priority, as the LCP element. On a phone it resolves to 640w at 64 KB, which is fine. So this is a desktop-wide problem specifically, and `sizes="100vw"` is the reason: the image is a full-bleed background, so `100vw` is technically honest, but it means every wide viewport pays 1.17 MB for a photo that sits behind a scrim.
2. The newsletter card thumbnail points its `src` at the unresized 2.17 MB `hero.png`. Its srcset tops out at a 454 KB PNG at 1024w. Any browser using srcset avoids the 2.17 MB file, so this is a fallback-path and PNG-format issue rather than a guaranteed 2.17 MB download, but a 454 KB PNG for a card thumbnail is still the wrong format.

Neither is in scope for this probe lane to fix. Both belong to a theme or media lane. They are recorded here because they are now the biggest measurable weight on the homepage, and because the prior #125 notes flagged "mobile LCP is image/font/network cost, not TTFB" without naming the files.

## Critical CSS state

| Route | `#jetpack-boost-critical-css` | Critical bytes | Deferred full CSS pattern | Boost bundle hash |
| --- | --- | ---: | --- | --- |
| `/` | Yes | 7474 | Yes | `ec2a031717` |
| `/blog/` | Yes | 15332 | Yes | `ec2a031717` |
| `/about/` | No | 0 | No | `ec2a031717` |
| `/work/` | No | 0 | No | `ec2a031717` |
| `/contact/` | No | 0 | No | `ec2a031717` |

The deferral pattern on `/` and `/blog/` is Boost's `media="not all"` plus an `onload` that restores `data-media="all"`, emitted as a second `<link>` with the same id and href. Routes without critical CSS get the bundle once, as a plain blocking `media='all'` stylesheet.

### The staleness finding, with proof

The Boost bundle is fresh. It contains the 1.5.7 hero rules:

```
.aurora-home-2026 .aurora-hero-media img{bottom:0;left:0;max-width:none;right:auto;top:0;width:145%}
.aurora-home-2026 .aurora-hero-copy{margin:0 auto 0 max(0px, calc((100% - var(--aurora-max)) / 2));max-width:min(34rem, 100%)}
```

The home critical CSS is not. Neither of those rules appears in it at all, and it still carries `object-position: 62% 30%`, which is one of the two values commit `b87be22` removed when it shipped the 1.5.7 hero on 2026-08-01. Distinct `object-position` values:

- home critical CSS: `54% 38%`, `62% 30%`
- deployed Boost bundle: `68% 26%`, `88% 20%`, `center top`

Token counts across the three surfaces:

| Token | Live `style.css` (1.5.7) | Boost bundle `ec2a031717` | Home critical CSS |
| --- | ---: | ---: | ---: |
| `aurora-home-title` | 4 | 7 | 0 |
| `aurora-about-title` | 1 | 1 | 0 |
| `aurora-hero-copy` | 17 | 22 | 4 |
| `aurora-hero-media` | 9 | 9 | 7 |

Practical effect: on a first, uncached homepage view, the hero paints with pre-1.5.7 geometry until the deferred bundle applies. That is a visible shift on the exact element PR #618 was built to fix. It does not show up in TTFB, which is why the timing tables above look clean.

Corroborating detail worth recording: the bundle contains zero occurrences of `aurora-tstm`, while repo `main` `style.css` has 40. That independently confirms the AGENTS.md truth that 1.5.8 is built but not deployed.

## Jetpack remnant sniff

| Marker | `/` | `/about/` | `/blog/` | `/work/` | `/contact/` |
| --- | --- | --- | --- | --- | --- |
| `pixel.wp.com` | Absent | Absent | Absent | Absent | Absent |
| `stats.wp.com` | Absent | Absent | Absent | Absent | Absent |
| Sharedaddy / likes | Absent | Absent | Absent | Absent | Absent |
| Jetpack form block | Absent | Absent | Absent | Absent | Absent |
| `/plugins/jetpack/` asset path | Absent | Absent | Absent | Absent | Absent |
| Boost `boost-cache/static/` | Present | Present | Present | Present | Present |
| GA4 `G-X7JE8B32L7` | Present | Present | Present | Present | Present |

Jetpack core frontend is still gone from every sampled route.

### Public evidence on plugin activation, and its limits

REST namespace listing at `/wp-json/` returns 20 namespaces: `akismet/v1`, `code-snippets/v1`, `google-site-kit/v1`, `jetpack-boost-ds`, `jetpack-boost/v1`, `jetpack-protect/v1`, `jetpack/v4`, `jetpack/v4/explat`, `mcp`, `my-jetpack/v1`, `oembed/1.0`, `popup-maker/v1`, `popup-maker/v2`, `pum/v1`, `redirection/v1`, `wp-abilities/v1`, `wp-block-editor/v1`, `wp-site-health/v1`, `wp/v2`, `zbscrm/v1`.

The presence of `jetpack/v4` is not evidence that Jetpack core is active. Boost and Protect bundle the shared `jetpack-connection` package, which registers that namespace on its own. The stronger signal is which routes are inside it. Enumerating `/wp-json/jetpack/v4` returns only connection, sync, licensing, identity-crisis, JITM, and WAF routes. The Jetpack core module controllers are not registered:

```
/wp-json/jetpack/v4/module/all  -> 404 rest_no_route
/wp-json/jetpack/v4/site        -> 404 rest_no_route
```

That is consistent with Jetpack core being inactive, which matches the 2026-07-01 deactivation record. Second corroborating signal: `/sitemap.xml` redirects to `/wp-sitemap.xml`, WordPress core's sitemap, not Jetpack's. Jetpack's sitemaps module would own that URL if core were active.

Protect is live: `/wp-json/jetpack-protect/v1/status` returns `401` (auth required) rather than `404` (route absent). Boost is live by its rendered output. Site Kit registers `google-site-kit/v1`, and GA4 fires on all five routes.

None of this proves the plugin list. It proves the frontend and REST surface behave the way an inactive-core, active-Boost, active-Protect, active-Site-Kit install behaves. The list itself still needs one wp-admin glance.

## What changed since 2026-07-26

| Thing | 2026-07-26 | 2026-08-02 | Read |
| --- | --- | --- | --- |
| Live Aurora | 1.4.8 | 1.5.7 | Hero rework shipped |
| Boost CSS hash | `c2441c2909` | `ec2a031717` | Bundle regenerated, picked up 1.5.7 |
| Boost CSS size | 138157 B | 142406 B | +4249 B, the new hero rules |
| Home JS bundle | `753a7e1c9e` (~21 KiB) | `5ada0d03dd` (21150 B) | Rehashed, same size class |
| Other-route JS | `1351e44c36` (~20 KiB) | `4882321c23` (20365 B) | Rehashed, same size class |
| `/blog/` warm Boost cache | `miss` | `hit` | Resolved, no intervention |
| Critical CSS on `/` | 7474 B | 7474 B | Byte-identical, not regenerated |
| Critical CSS on `/blog/` | 15332 B | 15332 B | Byte-identical, not regenerated |
| Critical CSS on about/work/contact | Absent | Absent | Unchanged gap |
| Critical CSS vs live theme | In sync with 1.4.8 | **Stale vs 1.5.7** | New finding |
| Jetpack core frontend | Absent | Absent | Holding |

The headline delta: the CSS bundle regenerated when 1.5.7 deployed, but the critical CSS did not. That is the concrete, dated evidence the issue was asking for, and it turns "regenerate Critical CSS at some point" into "regenerate Critical CSS because the homepage hero specifically needs it."

TTFB comparison against 2026-07-26 is not apples to apples. That report measured warm TTFB around 0.064s, this one measures 0.284s on home. The difference is transport, not the server: strip the ~190 ms of DNS/TCP/TLS this Vancouver vantage pays plus its round-trip, and server wait lands at 0.092 to 0.151 s warm. Future probes should record the `time_starttransfer` minus `time_appconnect` figure so this stops being ambiguous.

## Acceptance criteria status on #125

| Criterion | Status | Evidence |
| --- | --- | --- |
| Fresh cold/warm probes for the five core routes | Met | Two rounds, 5 samples each, tables above |
| Record TTFB, total time, cache headers, redirects, bytes | Met | Tables above, plus server wait split and gzip wire vs decoded bytes |
| Check Jetpack Boost UI once, record whether Critical CSS still warns | **Blocked, needs admin** | No public surface exposes it. `/wp-json/jetpack-boost/v1/status` is `404` unauthenticated, MCP adapter has zero abilities |
| Do not trigger another Boost regeneration unless UI stable | Honored | No admin actions taken |
| Tag-archive-only warnings documented as low-risk | Carried forward from 2026-07-26 | Not re-probed this pass, tag archives were out of the five-route scope. The prior finding stands: tag archives miss Boost cache and critical CSS, gateway still HITs, low risk |
| Confirm Jetpack core inactive, Boost/Protect/Site Kit active | **Public proxy only** | Core module REST routes absent, core frontend markers absent, core sitemap replaced by WP core sitemap. Protect returns 401 not 404. Boost renders. Site Kit namespace present, GA4 fires. Plugin list itself needs admin |
| Close only after the speed gain holds across repeated samples | Met for this window | Two rounds four minutes apart agree inside jitter, all routes sub-second cold, server wait under 400 ms cold and under 160 ms warm |

Net: five of seven met or honored from the public side. The two that remain are both admin-gated, and one of them is now more urgent than it was, because of the stale critical CSS.

## Recommended next step for KK

One wp-admin session, in this order.

1. Plugins screen. Confirm `jetpack/jetpack` inactive, `jetpack-boost` / `jetpack-protect` / `google-site-kit` active. Do not reactivate core.
2. Jetpack Boost, Critical CSS panel. Record the generated-file count, the last generation timestamp, and the exact failed-item list before touching anything. If the failures are only `/tag/*`, accept as low-risk per the existing #125 language.
3. Only if that panel is stable and the failures are understood: regenerate Critical CSS once. The trigger is documented above, the sheet predates the 1.5.7 hero.
4. Purge PressCACHE afterward. Do not use the Boost clear-cache REST route, it has returned `403 rest_forbidden` historically.
5. Re-run the critical CSS staleness check from the Method section. Expect `object-position` on the home critical sheet to move from `62% 30%` to the `68% 26%` / `88% 20%` pair, and ideally expect a non-zero critical sheet to appear on `/about/`, `/work/`, and `/contact/`. Record the new bundle hash if it changes from `ec2a031717`.
6. Do not stack a second regeneration. One pass, then measure.

## Out of scope this pass

wp-admin changes of any kind. Boost regeneration. PressCACHE purge. Theme edits or the 1.5.8 deploy, which stays gated on #601. Deleting the inactive `jetpack/jetpack` install, which is still the rollback seat. Mobile Lighthouse lab numbers, which need a browser this lane does not drive.

Three items were found and deliberately not acted on, each because it belongs to a different lane:

- The `sizes="100vw"` hero and the oversized newsletter PNG are theme and media work.
- The Meta Pixel is KK's tracking decision, not a perf gate.
- The trailing-slash duplicate URL behaviour is SEO lane (#274).

Each is written up above with the numbers needed to open a scoped issue if KK wants one.

## Artifacts

Raw sample TSVs, header dumps, and downloaded HTML lived in the agent scratchpad and are not committed. Every number above is reproducible from the commands in the Method section. Only this `.md` is tracked, per the `reports/` gitignore policy on PNG, HTML, and CSV captures.
