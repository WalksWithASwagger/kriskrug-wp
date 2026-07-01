# Performance Audit Report

- Generated: `2026-07-01T18:56:46.255633+00:00`
- Base URL: `https://kriskrug.co`
- Route samples: `3` cold and `3` warm probes per route
- Asset pages: https://kriskrug.co/, https://kriskrug.co/2026/06/30/zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey/

## Matrix A - Route Baseline

| Route | HTTP | Redirects | Cold TTFB p50 | Cold total p50 | Warm TTFB p50 | Warm total p50 | Bytes | Cache status | Final URL |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| `/` | 200 | 0 | 3.654 | 3.764 | 0.521 | 0.620 | 90809 | X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT | https://kriskrug.co/ |
| `/about/` | 200 | 0 | 3.807 | 3.952 | 0.527 | 0.868 | 88426 | X-Jetpack-Boost-Cache=miss, X-Gateway-Cache-Status=HIT | https://kriskrug.co/about/ |
| `/blog/` | 200 | 0 | 0.839 | 1.080 | 0.522 | 0.937 | 133036 | X-Jetpack-Boost-Cache=miss, X-Gateway-Cache-Status=HIT | https://kriskrug.co/blog/ |
| `/projects/` | 200 | 1 | 1.039 | 1.249 | 0.808 | 1.038 | 92551 | X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT | https://kriskrug.co/work/ |
| `/work/` | 200 | 0 | 4.183 | 4.275 | 0.518 | 0.615 | 92551 | X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT | https://kriskrug.co/work/ |

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

- `style_version`: `1.3.27`
- `resized_vancouver_png_present`: `True`
- `direct_heavy_vancouver_src_absent`: `True`
- `hero_dimensions_present`: `True`
- `vancouver_dimensions_present`: `True`
- `critical_css_mentions`: `6`

## Immediate Diagnostic Notes

- Use cold TTFB and cache headers to separate origin/render cost from warm-cache behavior.
- Treat `X-Jetpack-Boost-Cache=miss` on warm canonical probes as a cache-behavior finding to explain before deeper script changes.
- Chrome DevTools/Lighthouse metrics are not included unless a DevTools MCP or local Lighthouse runner is available.
