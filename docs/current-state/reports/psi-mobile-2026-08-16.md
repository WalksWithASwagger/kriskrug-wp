# PageSpeed Insights — kriskrug.co mobile — 2026-08-16 11:59 PDT

Source: [PSI report `qx4j9jir1j`](https://pagespeed.web.dev/analysis/https-kriskrug-co/qx4j9jir1j?form_factor=mobile) (Lighthouse 13.4.1, emulated Moto G Power, slow 4G, HeadlessChromium 150). Captured in-session after #706 origin apply + Aurora **1.6.8**.
Live state at capture: Aurora 1.6.8, WP 7.0.4, WPCode 7917 drafted, Code Snippets id 22 active.

Baseline: [`psi-mobile-2026-08-10.md`](psi-mobile-2026-08-10.md) (Aurora 1.6.0, pixel + blocking gtag still on).

## Scores

| Category | 2026-08-10 | 2026-08-16 | Delta |
|---|---:|---:|---|
| Performance (mobile) | **43** | **84** | +41 |
| Accessibility | 96 | 100 | +4 |
| Best Practices | 100 | 100 | — |
| SEO | 100 | 100 | — |
| Agentic Browsing | 2/3 (CLS fail) | **3/3** | pass |

## Metrics

| Metric | 2026-08-10 | 2026-08-16 | #706 expected |
|---|---|---|---|
| First Contentful Paint | 3.4 s | 2.1 s | not claimed |
| Largest Contentful Paint | **7.6 s** | **3.9 s** | should not move; **did** (1.6.8 homepage + other same-day work, not the diet) |
| Total Blocking Time | 160 ms | **10 ms** | should move; **did** |
| Cumulative Layout Shift | **0.43** | **0** (gauge) | should not move; **did** |
| Speed Index | 5.6 s | 4.4 s | not claimed |

Do not credit LCP or CLS to #706. The 1.6.8 front-page HTML write and cream theme landed the same evening. Layout-shift culprits (passed-audits drawer) still names `krug-1.jpg` (0.376) plus `#aurora-main`.

## #706 script diet vs this report

| Signal | 2026-08-10 | 2026-08-16 | Verdict |
|---|---|---|---|
| Facebook pixel (`fbevents`, id `1720755522050230`) | 176 KiB + 186 ms + two long tasks | **absent** | pass |
| gtag `G-X7JE8B32L7` in the PSI trace | 178 KiB + 156 ms + two long tasks | **still present**: unused-JS 176.9 KiB transfer / 72.4 KiB unused; 1 long task on `/gtag/js` | expected caveat (delay is from `load`, not parse) |
| Third-party long tasks from these origins | 4 | 1 (gtag only) | pixel half closed; gtag half is Network-pass, PSI-partial |
| Efficient cache policy on fbevents | flagged (20 min TTL) | gone | pass |

Logged-out browser Network (same evening, `issue-706-script-diet-apply-20260817.md`): 0 gtag requests for 2.5 s with no input; gtag on click; idle fire ~2.9 s after Playwright `load`. PSI still sees gtag because its trace outlasts that delay.

## LCP breakdown (not #706)

| Subpart | 2026-08-10 | 2026-08-16 |
|---|---:|---:|
| Time to first byte | 30 ms | 20 ms |
| Resource load delay | 150 ms | 80 ms |
| Resource load duration | 40 ms | 30 ms |
| Element render delay | **2,110 ms** | **270 ms** |

## Image delivery (est. 200 KiB; was 944 KiB)

Theme assets are now WebP (`futureproof-salmon-starfield-600.webp`, `vancouver-ai-meetup-30-kris-community-600.webp`, `kriskrug-wordmark-*.webp`). Remaining waste is mostly i0.wp.com content JPEGs plus one pcdn WebP compression note (33.5 KiB).

## Other findings

- **Non-composited animations: 10 elements** (was 56).
- **Forced reflow**: Boost bundle `1c4366cdd3.min.js` **103 ms** (was `7d33d1c7f5.min.js` 59 ms). Still #731 / Boost, not the diet.
- **Best Practices trust suggestions (unscored)**: CSP, HSTS, COOP, XFO/frame-ancestors, Trusted Types — unchanged, owned by #709.
- **Discover real-user data**: No Data.
- Filmstrip still shows blank frames then a dark first paint of the cream homepage. That is the stale Boost critical-CSS snapshot (`--aurora-black:#030405`), owned by **#731**.

## Do not close from this file alone

- **#706** pixel half is done. Gtag half is done on origin HTML + Network. PSI still attributes gtag unused-JS / one long task. Close only if KK accepts the documented delay caveat.
- **#731** is not done. Critical CSS rows are still 2026-07-01; wp-admin Regenerates is still required.
