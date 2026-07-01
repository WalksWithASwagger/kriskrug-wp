# Post-theme Live Performance Audit

- Generated: `2026-07-01T16:34:09.828407+00:00`
- Base URL: `https://kriskrug.co`
- Samples: `3` cold cache-busted and `3` warm canonical probes per route
- Context: Aurora `1.3.25` uploaded, PressCACHE purged, Jetpack Boost critical CSS regeneration started but still reported in progress during this audit.

## Route Matrix

| Route | HTTP | Redirects | Cold TTFB p50 | Cold total p50 | Warm TTFB p50 | Warm total p50 | Bytes | Cache status | Final URL |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| `/` | 200 | 0 | 3.675 | 3.762 | 0.425 | 0.528 | 91246 | X-Jetpack-Boost-Cache=hit, X-Gateway-Cache-Status=HIT | https://kriskrug.co/ |
| `/about/` | 200 | 0 | 4.355 | 4.450 | 0.427 | 0.515 | 88950 | X-Jetpack-Boost-Cache=miss, X-Gateway-Cache-Status=HIT | https://kriskrug.co/about/ |
| `/blog/` | 200 | 0 | 0.863 | 1.047 | 0.432 | 0.606 | 132160 | X-Jetpack-Boost-Cache=miss, X-Gateway-Cache-Status=HIT | https://kriskrug.co/blog/ |
| `/projects/` | 200 | 1 | 1.165 | 1.301 | 0.717 | 0.868 | 82165 | X-Jetpack-Boost-Cache=miss, X-Gateway-Cache-Status=HIT | https://kriskrug.co/recent-projects-include/ |
| `/work/` | 200 | 1 | 4.966 | 5.135 | 0.777 | 0.868 | 82165 | X-Jetpack-Boost-Cache=miss, X-Gateway-Cache-Status=HIT | https://kriskrug.co/recent-projects-include/ |

## Homepage Image Requests

| Bytes | HTTP | Dimensions | Loading | Fetch priority | Srcset | Source |
|---:|---:|---|---|---|---|---|
| 356274 | 200 | yes |  | high | no | https://i0.wp.com/www.punkrockai.com/public/photos/michelle-diamond/195.webp?w=2200&ssl=1 |
| 263225 | 200 | yes | lazy |  | no | https://www.futureproof.website/media/launch/futureproof-salmon-starfield-share-20260527.jpg |
| 256972 | 200 | yes | lazy |  | yes | https://i0.wp.com/bc-ai.ca/wp-content/uploads/2026/06/june-meetup-30-full-lineup-hero-1024x1024.png?w=720&ssl=1 |
| 227407 | 200 | yes | lazy |  | yes | https://i0.wp.com/bc-ai.ca/wp-content/uploads/2026/05/bcai-living-ecosystem.webp?w=1200&ssl=1 |
| 191933 | 200 | yes | lazy |  | no | https://i0.wp.com/www.punkrockai.com/public/photos/michelle-diamond/195.webp?w=1200&ssl=1 |
| 63437 | 200 | yes |  | high | no | https://s5102.pcdn.co/wp-content/themes/kk-aurora/assets/img/kriskrug-wordmark.png |
| 44 | 200 | yes | eager | high | no | https://www.facebook.com/tr?id=1720755522050230&ev=PageView&noscript=1 |
| 0 | 200 | yes | lazy |  | no | https://www.bothhandsfull.com/opengraph-image?46af5f0ff830fe03 |

## HTML Checks

- `style_version`: `1.3.25`
- `resized_vancouver_png_present`: `True`
- `direct_heavy_vancouver_src_absent`: `True`
- `hero_dimensions_present`: `True`
- `vancouver_dimensions_present`: `True`
