# Performance Audit Report

- Generated: `2026-07-01T18:15:36.148355+00:00`
- Base URL: `https://kriskrug.co`
- Route samples: `3` cold and `3` warm probes per route
- Asset pages: https://kriskrug.co/, https://kriskrug.co/2026/06/30/zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey/

## Matrix A - Route Baseline

| Route | HTTP | Redirects | Cold TTFB p50 | Cold total p50 | Warm TTFB p50 | Warm total p50 | Bytes | Cache status | Final URL |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| `/` | 200 | 0 | 4.047 | 4.138 | 0.429 | 0.519 | 91246 | X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT | https://kriskrug.co/ |
| `/about/` | 200 | 0 | 3.994 | 4.098 | 0.417 | 0.531 | 99204 | X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT | https://kriskrug.co/about/ |
| `/blog/` | 200 | 0 | 1.024 | 1.200 | 0.427 | 0.650 | 132160 | X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT | https://kriskrug.co/blog/ |
| `/projects/` | 200 | 1 | 1.480 | 1.593 | 0.706 | 0.853 | 92419 | X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT | https://kriskrug.co/recent-projects-include/ |
| `/work/` | 200 | 1 | 4.904 | 4.993 | 0.881 | 0.980 | 92419 | X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT | https://kriskrug.co/recent-projects-include/ |

## Matrix B - Top Image Requests

| Page | Bytes | HTTP | Width/height | Loading | Fetch priority | Srcset | Source |
|---|---:|---:|---|---|---|---|---|
| https://kriskrug.co/2026/06/30/zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey/ | 621317 | 200 | yes |  |  | yes | https://s5102.pcdn.co/wp-content/uploads/2024/09/crowd-shot-vancovuer-ai.jpeg |
| https://kriskrug.co/ | 356274 | 200 | yes |  | high | no | https://i0.wp.com/www.punkrockai.com/public/photos/michelle-diamond/195.webp?w=2200&ssl=1 |
| https://kriskrug.co/ | 263225 | 200 | yes | lazy |  | no | https://www.futureproof.website/media/launch/futureproof-salmon-starfield-share-20260527.jpg |
| https://kriskrug.co/ | 256972 | 200 | yes | lazy |  | yes | https://i0.wp.com/bc-ai.ca/wp-content/uploads/2026/06/june-meetup-30-full-lineup-hero-1024x1024.png?w=720&ssl=1 |
| https://kriskrug.co/ | 227407 | 200 | yes | lazy |  | yes | https://i0.wp.com/bc-ai.ca/wp-content/uploads/2026/05/bcai-living-ecosystem.webp?w=1200&ssl=1 |
| https://kriskrug.co/ | 191933 | 200 | yes | lazy |  | no | https://i0.wp.com/www.punkrockai.com/public/photos/michelle-diamond/195.webp?w=1200&ssl=1 |
| https://kriskrug.co/ | 63437 | 200 | yes |  | high | no | https://s5102.pcdn.co/wp-content/themes/kk-aurora/assets/img/kriskrug-wordmark.png |
| https://kriskrug.co/2026/06/30/zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey/ | 63437 | 200 | yes |  | high | no | https://s5102.pcdn.co/wp-content/themes/kk-aurora/assets/img/kriskrug-wordmark.png |
| https://kriskrug.co/ | 50622 | 200 | yes | lazy |  | no | https://www.bothhandsfull.com/opengraph-image?46af5f0ff830fe03 |
| https://kriskrug.co/ | 44 | 200 | yes | eager | high | no | https://www.facebook.com/tr?id=1720755522050230&ev=PageView&noscript=1 |
| https://kriskrug.co/2026/06/30/zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey/ | 44 | 200 | yes |  |  | no | https://www.facebook.com/tr?id=1720755522050230&ev=PageView&noscript=1 |

## Matrix C - Blocking Script Candidates

| Page | Count | Sources |
|---|---:|---|
| https://kriskrug.co/ | 0 |  |
| https://kriskrug.co/2026/06/30/zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey/ | 0 |  |

## Matrix D - URL Hygiene

| Check | Result |
|---|---|
| Route redirect depth | All sampled routes are 0-1 redirect hop. |
| Homepage/post internal links missing trailing slash | None found in inspected pages. |

## HTML / Theme Checks

- `style_version`: `1.3.25`
- `resized_vancouver_png_present`: `True`
- `direct_heavy_vancouver_src_absent`: `True`
- `hero_dimensions_present`: `True`
- `vancouver_dimensions_present`: `True`
- `critical_css_mentions`: `6`

## Immediate Diagnostic Notes

- Use cold TTFB and cache headers to separate origin/render cost from warm-cache behavior.
- Treat `X-Jetpack-Boost-Cache=miss` on warm canonical probes as a cache-behavior finding to explain before deeper script changes.
- Chrome DevTools/Lighthouse metrics are not included unless a DevTools MCP or local Lighthouse runner is available.
