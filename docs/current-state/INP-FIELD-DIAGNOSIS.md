# INP field diagnosis — 2026-09-06

Issue: #986. Read-only diagnosis of the September 4 audit. **The claimed field INP failure cannot be confirmed from current public data, and no >200 ms interaction was reproduced.** This is not a field pass. No site code, analytics settings, imagery or interactions were changed.

## Field evidence and availability

Public PageSpeed UI checked September 6, 2026, 10:46–10:49 PDT for `https://kriskrug.co/` in both device modes. [Retained PSI report](https://pagespeed.web.dev/analysis/https-kriskrug-co/o2x0defz3d?form_factor=desktop). Text captures: [mobile](reports/inp-2026-09-06/psi-mobile.txt), [desktop](reports/inp-2026-09-06/psi-desktop.txt).

| Segment | URL p75 INP | Origin p75 INP | Collection dates | Availability |
|---|---|---|---|---|
| Mobile | unavailable | unavailable | not exposed | PSI field panel: “No Data” |
| Desktop | unavailable | unavailable | not exposed | PSI field panel: “No Data” |

Neither a URL-level field result nor an origin fallback result was exposed. Do not fabricate a collection window or infer a pass/fail. The unauthenticated PSI v5 API request also returned HTTP 429 (`RESOURCE_EXHAUSTED`, daily quota limit zero); the browser UI was the successful alternative. No paid API or new credentials were provisioned.

Lighthouse is separate evidence: mobile TBT 40 ms, desktop TBT 0 ms. Mobile lab CLS 0.121 and desktop 0.495 deserve separate investigation in the existing #731/#701 context; they do not establish an INP problem. Lab scores are diagnostic, not a substitute for field INP.

## Current analytics and deployment comparison

The [#706 deployment record](reports/issue-706-script-diet-apply-20260817.md) records delayed analytics and removed Facebook pixel on August 17; #706 is closed, while #731 remains open. Current public HTML still contains `kk-gtag-delayed`: first `pointerdown`, `keydown`, `touchstart` or `wheel` boots gtag, or a timer three seconds after load schedules it through `requestIdleCallback` (one-second timeout). Thus the audit's proposed deferral already exists in substantial form. No further deferral is justified by these measurements.

In the four first-pass interaction runs, the resource records show gtag starting after the first keyboard interaction; no Facebook resource was observed. The samples occur about 20 days after #706, so even an available 28-day collection ending today could overlap pre-change traffic. The actual PSI reporting window is unavailable and cannot be compared precisely.

`make doctor` ran: GitHub authenticated, live style reachable, isolated branch clean, but this worktree has no Python venv or injected WP credentials. `make status-readonly` was attempted in the sandbox and repeated with network access; authenticated draft counters remain unavailable. This public diagnosis needs neither credentials nor a publisher environment. Public stylesheet readback and coordinator status identify Aurora 1.6.11; repo version alone is not production proof.

## Repeated interaction measurements

Host: macOS arm64, headless Chrome for Testing 151.0.7922.34 via Playwright. Fresh context each run, network unthrottled. Desktop 1440×1000, DPR 1, CPU 1×; mobile emulation 390×844, DPR 3, touch enabled, CPU 4×. These are simulated devices, not a representative field population.

Run each sequence twice per device: load homepage; focus first primary-nav link and press ArrowRight; scroll to first logo and click/tap American Express; focus CIBC and press Enter; scroll to 700 px, focus Speaking in the header and press ArrowRight. A second pair of runs per device repeats the sequence and then actually clicks/taps Speaking to navigate. Focus/scroll themselves are setup, not INP interactions. Hover entries with interactionId zero are excluded.

Event Timing observer uses the minimum 16 ms reporting threshold. Durations are rounded by Chrome; absent entries do not prove zero latency. The unload-safe second pass forwards events to the Node collector. Navigation changes the performance time origin, so its recorded end timestamp is from the destination document; do not subtract it from the source start timestamp.

| First pass action | Desktop repeat 1 / 2 (ms) | Mobile repeat 1 / 2 (ms) |
|---|---:|---:|
| Nav ArrowRight | 40 / 24 | 32 / 24 |
| Logo click/tap | 32 / 40 | 40 / 32 |
| Logo Enter | 16 / 16 | no entry / no entry |
| Header ArrowRight after scroll | no entry / no entry | 16 / no entry |

Second-pass maximum eligible event durations: desktop 40/40 ms; mobile 40/32 ms. Actual Speaking taps produced 24/24 ms entries on mobile. Desktop navigation produced no eligible entry; retained CDP traces confirm the action sequence but do not supply an Event Timing latency for it.

| Representative second-pass event | Input delay | Processing | Presentation estimate | Total |
|---|---:|---:|---:|---:|
| Desktop 1 logo pointerdown | 0.8 | 0.2 | 39.0 | 40 |
| Desktop 2 nav keydown | 0.2 | 0.4 | 39.4 | 40 |
| Mobile 1 logo pointerdown | 16.4 | 1.9 | 21.7 | 40 |
| Mobile 2 nav keydown | 4.2 | 2.5 | 25.3 | 32 |
| Mobile Speaking tap, repeat 1 | 13.3 | 5.6 | 5.1 | 24 |
| Mobile Speaking tap, repeat 2 | 12.4 | 3.9 | 7.7 | 24 |

All values are milliseconds. Presentation is `startTime + duration - processingEnd`, clamped to zero; it inherits rounded duration uncertainty. These event maxima are lab observations, not a calculated field p75 or full-session INP.

Evidence: [first pass](reports/inp-2026-09-06/interactions.json), [navigation pass](reports/inp-2026-09-06/navigation.json). Adjacent gzip Chrome trace files retain EventDispatch, FunctionCall, layout, paint and task timings, stripping all args, URLs, request headers, cookies and DOM content. Decompress to inspect in DevTools. They establish timing but intentionally cannot attribute functions to scripts. The adjacent `.cjs` scripts reproduce collection with Playwright on NODE_PATH and output into `/tmp`; the retained JSON points to the committed sanitized traces.

## Ranked next actions and bounded fix criteria

1. **No INP code fix is supported yet.** Keep the logo behavior, header and photography intact. There is no proven affected source or expected improvement to specify. Supply the auditor's original device/scope/window/INP values if available; compare with this dated evidence.
2. **If real users still report delay, repeat the exact troublesome interaction on their device class**, at least twice, with full local DevTools attribution. Review any trace for sensitive content before sharing. Only then open a bounded fix against the implicated handler/style/script; require the same interaction to fall below 200 ms with reduced implicated input, processing or presentation time and unchanged visual/keyboard behavior. Do not duplicate #706 deferral or #731 critical CSS work on speculation.
3. **If public field samples stay unavailable, request approval for minimal temporary RUM attribution.** Use a reviewed web-vitals attribution collector, recording INP, its three timing components, coarse device class, route category and a small allowlisted component name. Never collect typed content, form values, arbitrary selectors/text, full query strings, user IDs or persistent cross-session identifiers. Define consent, endpoint ownership, access and short retention before deployment; avoid storing IPs and set a sunset date. No tracking was installed here.

For any future verified fix, rerun the identical desktop/mobile click, tap and keyboard sequences twice with the same throttling and retained traces immediately. Then check available URL and origin mobile/desktop CrUX segments over a subsequent complete rolling 28-day window; target p75 INP ≤200 ms. Record exact dates and sample availability. Missing samples remain a limitation, not a green result.
