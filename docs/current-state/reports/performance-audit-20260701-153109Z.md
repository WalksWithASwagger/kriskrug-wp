# Performance Audit Report

- Generated: `2026-07-01T15:32:12.982426+00:00`
- Base URL: `https://kriskrug.co`
- Route samples: `3` cold and `3` warm probes per route
- Asset pages: `https://kriskrug.co/, https://kriskrug.co/2026/06/30/zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey/`

## Matrix A - Route Baseline

| Route | HTTP | Redirects | Cold TTFB p50 | Cold total p50 | Warm TTFB p50 | Warm total p50 | Cache status | Final URL |
|---|---:|---:|---:|---:|---:|---:|---|---|
| / | 200 | 0 | 3.982 | 4.085 | 0.321 | 0.516 | x-jetpack-boost-cache=hit, x-gateway-cache-status=HIT | https://kriskrug.co/ |
| /about/ | 200 | 0 | 3.853 | 4.081 | 0.428 | 0.828 | x-jetpack-boost-cache=hit, x-gateway-cache-status=HIT | https://kriskrug.co/about/ |
| /blog/ | 200 | 0 | 0.784 | 1.084 | 0.423 | 0.730 | x-jetpack-boost-cache=miss, x-gateway-cache-status=HIT | https://kriskrug.co/blog/ |
| /projects/ | 200 | 1 | 0.926 | 1.215 | 0.704 | 0.893 | x-jetpack-boost-cache=hit, x-gateway-cache-status=HIT | https://kriskrug.co/recent-projects-include/ |
| /work/ | 200 | 1 | 4.181 | 4.363 | 0.660 | 0.949 | x-jetpack-boost-cache=hit, x-gateway-cache-status=HIT | https://kriskrug.co/recent-projects-include/ |

## Matrix B - Top Image Requests

| Page | Bytes | Status | Width/height | Loading | Fetch priority | Srcset | Source |
|---|---:|---:|---|---|---|---|---|
| https://kriskrug.co/ | 1795047 | 200 | no | lazy |  | no | https://bc-ai.ca/wp-content/uploads/2026/06/june-meetup-30-full-lineup-hero-1024x1024.png |
| https://kriskrug.co/2026/06/30/zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey/ | 621317 | 200 | yes |  |  | yes | https://s5102.pcdn.co/wp-content/uploads/2024/09/crowd-shot-vancovuer-ai.jpeg |
| https://kriskrug.co/ | 356274 | 200 | no |  | high | no | https://i0.wp.com/www.punkrockai.com/public/photos/michelle-diamond/195.webp?w=2200&ssl=1 |
| https://kriskrug.co/ | 263225 | 200 | no | lazy |  | no | https://www.futureproof.website/media/launch/futureproof-salmon-starfield-share-20260527.jpg |
| https://kriskrug.co/ | 227407 | 200 | no | lazy |  | no | https://i0.wp.com/bc-ai.ca/wp-content/uploads/2026/05/bcai-living-ecosystem.webp?w=1200&ssl=1 |
| https://kriskrug.co/ | 191933 | 200 | no | lazy |  | no | https://i0.wp.com/www.punkrockai.com/public/photos/michelle-diamond/195.webp?w=1200&ssl=1 |
| https://kriskrug.co/ | 63437 | 200 | yes |  | high | no | https://s5102.pcdn.co/wp-content/themes/kk-aurora/assets/img/kriskrug-wordmark.png |
| https://kriskrug.co/2026/06/30/zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey/ | 63437 | 200 | yes |  | high | no | https://s5102.pcdn.co/wp-content/themes/kk-aurora/assets/img/kriskrug-wordmark.png |

## Matrix C - Blocking Script Candidates

| Page | Count | Sources |
|---|---:|---|
| https://kriskrug.co/ | 3 | https://www.googletagmanager.com/gtag/js?id=G-X7JE8B32L7, https://s5102.pcdn.co/wp-content/boost-cache/static/04a53e0b4c.min.js, https://stats.wp.com/e-202627.js |
| https://kriskrug.co/2026/06/30/zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey/ | 3 | https://www.googletagmanager.com/gtag/js?id=G-X7JE8B32L7, https://s5102.pcdn.co/wp-content/boost-cache/static/4417b09126.min.js, https://stats.wp.com/e-202627.js |

## Matrix D - URL Hygiene

| Check | Result |
|---|---|
| Route redirect depth | All sampled routes are 0-1 redirect hop. |
| Homepage/post internal links missing trailing slash | None found in inspected pages. |

## Immediate Recommendations

- Use this report as the baseline for issue #125 before changing Jetpack Boost, theme scripts, or image payloads.
- Prioritize any image over 500 KB that lacks local ownership, explicit dimensions, or responsive metadata.
- Keep Track A image/content updates separate from Track B theme/script updates.
- Re-run this command after every optimization pass and compare the Matrix A route table plus Matrix B top images.
