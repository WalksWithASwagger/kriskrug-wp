# Events documentation links #1101: October 25, 2026

Prepared under KK's instruction to continue the kriskrug plan and ship what can be handled independently. The #1099 normalized documentation contract and #1100 renderer are already merged; page 2250 already exposes AI Day, Capilano and North House recaps. This pass adds the remaining verified meetup links and records the four-part ALL IN series in the catalog. Applied through Varlock at 2026-10-26 04:43 UTC (October 25 Pacific) after required CI passed. Authenticated raw readback exactly matches the candidate hash below; normal and cache-bypassed public pages both expose the six added links.

## Verified sources and bounded change

| Stable event ID | Documentation | Evidence |
|---|---|---|
| `vancouver-ai-meetup-2026-08-26` | [Recap](https://bc-ai.ca/news/vancouver-ai-meetup-32-data-for-good-taleeb-noormohamed-recap), [Photos](https://bc-ai.ca/events/vancouver-ai-meetup-2026-08#photos), [Video](https://www.youtube.com/watch?v=TrFhKXyJJ7M) | Published recap identifies the official full recording. The first-party gallery returns 200, has a `photos` anchor, 20 image elements and Michelle Diamond credit. YouTube oEmbed returns 200 with the matching Meetup #32 title. |
| `vancouver-ai-meetup-2026-09-30` | [Recap](https://bc-ai.ca/events/2026-09-30-vancouver-ai-meetup-33-september-30-at-the-space-centre), [Photos](https://bc-ai.ca/events/2026-09-30-vancouver-ai-meetup-33-september-30-at-the-space-centre#photos), [Video](https://www.youtube.com/watch?v=sK3kNVBrYjA) | Published event page contains the recap and official recording. Its gallery returns 200, has a `photos` anchor, 20 image elements and Michelle Diamond credit. YouTube oEmbed returns 200 with the matching Meetup #33 title. |
| `2026-09-15-all-in-montreal` | Published posts 12783, 12788, 12800 and 12829, September 15–18 | Exact WordPress post identities/status/canonical URLs verified. The September 18 primary `recap_url` is retained; three earlier articles append to normalized `docs.recap`. Catalog only: the previously held event is still absent from production. |

The current published #32 recap's recording takes precedence over the older example URL in the issue. Recording metadata and destination links were verified; playback was not evaluated. Two external full-gallery destinations returned 403 to the HTTP checker, so the verified first-party galleries are used. Existing promo art is not credited to Michelle; media objects, actual credits and registration/source URLs stay unchanged.

All 76 normalized identities are unchanged. Only documentation fields on the three named records differ. The live candidate changes only the two already-published meetup record rows: six added links, nine documentation links total. It preserves all 74 live IDs, all 43 image elements, counters, script, style and surrounding shell. ALL IN and TruNorth stay absent.

## Publication convention

The publisher README now requires stable-ID matching, verified canonical coverage URLs, independent recap/photos/video lists, preserved registration destinations and credits, a bounded page diff, approval covering the Events update, snapshot/hash guards, and authenticated plus public readback in the publishing receipt. The Events README links that procedure. No automatic publisher write or event-confirmation inference is introduced.

## Verification and release packet

The 96 focused Events tests, catalog render and docs truth/diff checks passed. The first full verification exposed an existing time-dependent #1090 privacy-fixture assertion; its separate test-only fix is PR #1152. After integrating merged PR #1152 (`530a1069`), `make verify` passes all 1,141 Python tests, JavaScript validation, plugin/theme smoke, docs truth, PHP syntax and coding standards.

The exact candidate passes Chromium at 1440px, 768px and 390px: nine documentation links, 71 visible past rooms, 33 meetup editions, 39 frames, three upcoming cards, zero horizontal overflow, visible keyboard focus and zero script errors. A controlled festival cutoff yields 72 rooms, 40 frames and two upcoming cards. Analytics are blocked in the verification browser. Dry-run deploy confirms page **2250**, slug **events**, status **publish**.

- Source raw SHA-256: `59a2ccab2b957cbe8320922e7f9bcbeb73d7b6613308bcc3d26bdbbaf4416716`.
- Candidate raw SHA-256: `42ba3c5eae6feb68049c837a29bbb3ea13cf1a475c140c7a229d31880c3a49cf`.
- Private packet: `/Users/kk/Code/kriskrug-wp/.generated/current-state/events-docs-1101-2026-10-25/`.

The packet holds source checks, fresh page snapshot, exact diff/manifest, bounded preparation and Varlock deploy adapters, responsive preview/screenshots and readback reports. The deploy adapter uses only a content payload and pins both hashes; it refuses concurrent changes. Rollback uses the pre-apply snapshot with the existing preview-first restore helper and expected-current hash. Do not replace the live page with a full catalog render while ALL IN is held.

The pre-apply rollback snapshot is `snapshots/page-2250-events-20261026T044341Z.json` (mode 0600). Actual public browser navigation at all three widths passes the same link, rollover, focus, overflow and console assertions; the mobile documentation row was visually inspected. `applied-readback.json`, `public-verification.json`, `events-live-browser-report.json` and screenshots record the result. A restore preview verified the original snapshot and current hash; no restore or cache purge was needed.
