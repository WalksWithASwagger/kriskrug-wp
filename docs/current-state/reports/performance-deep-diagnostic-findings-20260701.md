# Deep Performance Diagnostic Findings

- Generated: `2026-07-01T18:17:55.415025+00:00`
- Context: read-only follow-up after Aurora `1.3.25`, homepage image optimization, and Jetpack Boost Critical CSS partial generation.

## Canonical Warm Cache Probe

| Route | Samples | TTFB p50 | Total p50 | Redirects | Bytes | Last cache headers | Final URL |
|---|---:|---:|---:|---:|---:|---|---|
| `/` | 5 | 0.441 | 0.537 | 0 | 91246 | X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT | https://kriskrug.co/ |
| `/about/` | 5 | 0.430 | 0.529 | 0 | 99204 | X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT | https://kriskrug.co/about/ |
| `/blog/` | 5 | 0.419 | 0.614 | 0 | 132160 | X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT | https://kriskrug.co/blog/ |
| `/projects/` | 5 | 0.712 | 0.875 | 1 | 92419 | X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT | https://kriskrug.co/recent-projects-include/ |
| `/work/` | 5 | 0.783 | 0.868 | 1 | 92419 | X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT | https://kriskrug.co/recent-projects-include/ |

Cache status samples:
- `/`: `X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT` ; `X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT` ; `X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT` ; `X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT` ; `X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT`
- `/about/`: `X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT` ; `X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT` ; `X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT` ; `X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT` ; `X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT`
- `/blog/`: `X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT` ; `X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT` ; `X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT` ; `X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT` ; `X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT`
- `/projects/`: `X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT` ; `X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT` ; `X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT` ; `X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT` ; `X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT`
- `/work/`: `X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT` ; `X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT` ; `X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT` ; `X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT` ; `X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT`

## Jetpack Boost Critical CSS Failed Tag Archives

| URL | HTTP | Redirects | TTFB | Total | Bytes | Stylesheets | Cache headers | Canonical |
|---|---:|---:|---:|---:|---:|---:|---|---|
| https://kriskrug.co/tag/itunes/ | 200 | 0 | 0.850 | 0.942 | 57676 | 1 | X-Jetpack-Boost-Cache=miss, X-Gateway-Cache-Status=MISS |  |
| https://kriskrug.co/tag/hype-machine/ | 200 | 0 | 0.909 | 0.991 | 57748 | 1 | X-Jetpack-Boost-Cache=miss, X-Gateway-Cache-Status=MISS |  |
| https://kriskrug.co/tag/seeqpod/ | 200 | 0 | 0.997 | 1.098 | 57688 | 1 | X-Jetpack-Boost-Cache=miss, X-Gateway-Cache-Status=MISS |  |
| https://kriskrug.co/tag/8-tracks/ | 200 | 0 | 1.028 | 1.111 | 57700 | 1 | X-Jetpack-Boost-Cache=miss, X-Gateway-Cache-Status=MISS |  |
| https://kriskrug.co/tag/songza/ | 200 | 0 | 0.942 | 1.030 | 57676 | 1 | X-Jetpack-Boost-Cache=miss, X-Gateway-Cache-Status=MISS |  |
| https://kriskrug.co/tag/favtape/ | 200 | 0 | 1.004 | 1.110 | 57688 | 1 | X-Jetpack-Boost-Cache=miss, X-Gateway-Cache-Status=MISS |  |
| https://kriskrug.co/tag/musicovery/ | 200 | 0 | 0.899 | 0.983 | 57724 | 1 | X-Jetpack-Boost-Cache=miss, X-Gateway-Cache-Status=MISS |  |
| https://kriskrug.co/tag/danielle-sipple/ | 200 | 0 | 0.931 | 1.021 | 58159 | 1 | X-Jetpack-Boost-Cache=miss, X-Gateway-Cache-Status=MISS |  |
| https://kriskrug.co/tag/sxsw/ | 200 | 0 | 0.861 | 0.955 | 67815 | 1 | X-Jetpack-Boost-Cache=miss, X-Gateway-Cache-Status=MISS |  |
| https://kriskrug.co/tag/nyfw/ | 200 | 0 | 0.770 | 0.866 | 58027 | 1 | X-Jetpack-Boost-Cache=miss, X-Gateway-Cache-Status=MISS |  |

Stylesheet HEAD samples for failed tag archives:
- `https://kriskrug.co/tag/itunes/`
  - `200` `101467` bytes `https://s5102.pcdn.co/wp-content/boost-cache/static/f43a4040f3.min.css`
- `https://kriskrug.co/tag/hype-machine/`
  - `200` `101467` bytes `https://s5102.pcdn.co/wp-content/boost-cache/static/f43a4040f3.min.css`
- `https://kriskrug.co/tag/seeqpod/`
  - `200` `101467` bytes `https://s5102.pcdn.co/wp-content/boost-cache/static/f43a4040f3.min.css`
- `https://kriskrug.co/tag/8-tracks/`
  - `200` `101467` bytes `https://s5102.pcdn.co/wp-content/boost-cache/static/f43a4040f3.min.css`
- `https://kriskrug.co/tag/songza/`
  - `200` `101467` bytes `https://s5102.pcdn.co/wp-content/boost-cache/static/f43a4040f3.min.css`
- `https://kriskrug.co/tag/favtape/`
  - `200` `101467` bytes `https://s5102.pcdn.co/wp-content/boost-cache/static/f43a4040f3.min.css`
- `https://kriskrug.co/tag/musicovery/`
  - `200` `101467` bytes `https://s5102.pcdn.co/wp-content/boost-cache/static/f43a4040f3.min.css`
- `https://kriskrug.co/tag/danielle-sipple/`
  - `200` `101467` bytes `https://s5102.pcdn.co/wp-content/boost-cache/static/f43a4040f3.min.css`
- `https://kriskrug.co/tag/sxsw/`
  - `200` `101467` bytes `https://s5102.pcdn.co/wp-content/boost-cache/static/f43a4040f3.min.css`
- `https://kriskrug.co/tag/nyfw/`
  - `200` `101467` bytes `https://s5102.pcdn.co/wp-content/boost-cache/static/f43a4040f3.min.css`

## Interpretation

- Jetpack Boost advanced recommendations identify tag archive pages, not homepage/About/Work, as the Critical CSS failure set.
- The failed tag archives render external stylesheet links, so the Boost warning is probably archive-template CSS detection/generation rather than a missing stylesheet across the whole site.
- Warm canonical probes still show gateway cache hits, but Jetpack Boost page-cache headers vary by route and should not be treated as the primary cold-TTFB fix until the Boost warning is resolved or dismissed intentionally.
- The biggest cold-TTFB outliers remain homepage/About/Work, so the root cause is likely WordPress/render path or cache-bypass behavior rather than the previously fixed image payload.
