# PageSpeed Insights — kriskrug.co mobile — 2026-08-10 08:52 PDT

Source: PSI report captured by KK (Lighthouse 13.4.1, emulated Moto G Power, slow 4G).
Live state at capture: Aurora 1.6.0 (deployed 2026-08-10 04:42 UTC), WP 7.0.3.

## Scores

| Category | Score |
|---|---|
| Performance (mobile) | **43** |
| Accessibility | 96 |
| Best Practices | 100 |
| SEO | 100 |
| Agentic Browsing | 2/3 (CLS check fails) |

## Metrics

| Metric | Value | Status |
|---|---|---|
| First Contentful Paint | 3.4 s | poor |
| Largest Contentful Paint | **7.6 s** | poor |
| Total Blocking Time | 160 ms | ok-ish |
| Cumulative Layout Shift | **0.43** | poor |
| Speed Index | 5.6 s | poor |

## The two dominant findings

1. **CLS 0.430 comes from ONE element**: `<main id="aurora-main" class="wp-block-group aurora-home-2026 aurora-home-revive aurora-keynote-first is…">` accounts for the full 0.430.
2. **LCP breakdown**: TTFB 30 ms, resource load delay 150 ms, resource load 40 ms, **element render delay 2,110 ms**. The LCP element is the krug-1.jpg hero portrait (`fetchpriority="high"`, loads fast) — its *paint* is being gated, not its download. Both findings point at the reveal system and/or the Boost deferred-CSS swap reflowing the page.

## Image delivery (est. 944 KiB savings)

| Image | Served | Displayed | Waste | Fix |
|---|---|---|---|---|
| futureproof-salmon-starfield JPG (hotlink to futureproof.website) | 321.9 KiB | — | 273.6 KiB | WebP/AVIF + rehost |
| theme asset vancouver-ai-meetup-30-kris-community.jpg | 226.2 KiB (1067px) | 276×184 | 218.0 KiB | responsive + WebP |
| theme asset kriskrug-wordmark.png | 62.0 KiB (468×229) | 90×44 | 61.3 KiB | resize + WebP |
| ~9 proof-grid content images via i0.wp.com | 720px variants | ~184–275px slots | ~390 KiB total | sizes/srcset audit |

## Third-party scripts

| Party | Transfer | Main thread | Unused |
|---|---|---|---|
| Facebook pixel (fbevents + config) | 176 KiB | 186 ms + long tasks 146/88 ms | 58.2 KiB |
| Google Tag Manager (gtag G-X7JE8B32L7) | 178 KiB | 156 ms + long tasks 115/67 ms | 72.9 KiB |

Cache TTL on fbevents: 20 minutes. Legacy JS (transpiled polyfills) 12.5 KiB in fbevents.

## Other findings

- **Non-composited animations: 56 elements** — theme transitions on `border-*-color`, `color`, `box-shadow` across buttons, footer tiles, article rows, nav links.
- **Forced reflow**: Boost bundle `7d33d1c7f5.min.js` 59 ms; gtag 34 ms.
- **Accessibility (96)**: one failing audit — insufficient contrast on unspecified element(s).
- **Best Practices trust suggestions (unscored)**: CSP effectiveness, strong HSTS, COOP, XFO/frame-ancestors, Trusted Types.
- **Discover real-user data**: No Data (site below CrUX threshold).

## Issues filed from this report

See the `psi-2026-08-10` label-search: `gh issue list --search "psi-2026-08-10"` — each issue quotes its slice of this report.
