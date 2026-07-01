# Performance Audit Report

- Generated: `2026-07-01T16:00:04.270908+00:00`
- Base URL: `https://kriskrug.co`
- Route samples: `3` cold and `3` warm probes per route
- Asset pages: `https://kriskrug.co/, https://kriskrug.co/2026/06/30/zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey/`

## Matrix A - Route Baseline

| Route | HTTP | Redirects | Cold TTFB p50 | Cold total p50 | Warm TTFB p50 | Warm total p50 | Cache status | Final URL |
|---|---:|---:|---:|---:|---:|---:|---|---|
| / | 200 | 0 | 3.949 | 4.101 | 0.282 | 0.515 | x-jetpack-boost-cache=hit, x-gateway-cache-status=HIT | https://kriskrug.co/ |
| /about/ | 200 | 0 | 3.666 | 3.893 | 0.342 | 0.655 | x-jetpack-boost-cache=hit, x-gateway-cache-status=HIT | https://kriskrug.co/about/ |
| /blog/ | 200 | 0 | 0.681 | 0.880 | 0.411 | 0.742 | x-jetpack-boost-cache=miss, x-gateway-cache-status=HIT | https://kriskrug.co/blog/ |
| /projects/ | 200 | 1 | 0.691 | 0.928 | 0.635 | 0.842 | x-jetpack-boost-cache=miss, x-gateway-cache-status=HIT | https://kriskrug.co/recent-projects-include/ |
| /work/ | 200 | 1 | 4.044 | 4.266 | 0.572 | 0.774 | x-jetpack-boost-cache=miss, x-gateway-cache-status=HIT | https://kriskrug.co/recent-projects-include/ |

## Matrix B - Top Image Requests

| Page | Bytes | Status | Width/height | Loading | Fetch priority | Srcset | Source |
|---|---:|---:|---|---|---|---|---|
| https://kriskrug.co/2026/06/30/zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey/ | 621317 | 200 | yes |  |  | yes | https://s5102.pcdn.co/wp-content/uploads/2024/09/crowd-shot-vancovuer-ai.jpeg |
| https://kriskrug.co/ | 356274 | 200 | yes |  | high | no | https://i0.wp.com/www.punkrockai.com/public/photos/michelle-diamond/195.webp?w=2200&ssl=1 |
| https://kriskrug.co/ | 263225 | 200 | yes | lazy |  | no | https://www.futureproof.website/media/launch/futureproof-salmon-starfield-share-20260527.jpg |
| https://kriskrug.co/ | 256972 | 200 | yes | lazy |  | yes | https://i0.wp.com/bc-ai.ca/wp-content/uploads/2026/06/june-meetup-30-full-lineup-hero-1024x1024.png?w=720&ssl=1 |
| https://kriskrug.co/ | 227407 | 200 | yes | lazy |  | yes | https://i0.wp.com/bc-ai.ca/wp-content/uploads/2026/05/bcai-living-ecosystem.webp?w=1200&ssl=1 |
| https://kriskrug.co/ | 191933 | 200 | yes | lazy |  | no | https://i0.wp.com/www.punkrockai.com/public/photos/michelle-diamond/195.webp?w=1200&ssl=1 |
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
