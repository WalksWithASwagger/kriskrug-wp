# November meetup and ALL IN Events release: October 25, 2026

Kris explicitly approved publishing the prepared November 25 meetup and ALL IN entries. Page **2250**, exact slug **events**, was updated through Varlock at **2026-10-26 05:15:16 UTC** (October 25, 22:15 Pacific). The authenticated stored content matches the candidate exactly. Normal and cache-bypassed public responses both deliver the update; no manual cache purge was needed.

## Published entries

- **Vancouver AI Meetup: Where Humans Go, Where AI Goes**, November 25, 2026, Host & MC, linking to [the public Luma listing](https://luma.com/nov-vanai). The approved [catalog patch](../proposals/events-1102-november-meetup.patch) is now applied. The source still confirms the date, H.R. MacMillan Space Centre and Kris's role. No edition number, photograph or clock time was invented. The existing renderer supplies the date card and day-after rollover.
- **ALL IN Montreal**, September 15–18, Press, in the past record. Its title links to the final-day dispatch and four independent recap links retain the [final day](https://kriskrug.co/2026/09/18/all-in-montreal-final-day-a-heartbeat-under-my-boots/), [outbound trip](https://kriskrug.co/2026/09/15/headed-east-for-all-in-montreal/), [conference floor](https://kriskrug.co/2026/09/16/all-in-montreal-robot-mirror/) and [Uncle Evan/backpack](https://kriskrug.co/2026/09/17/all-in-montreal-day-two-uncle-evan-and-the-extremely-suspicious-backpack/) articles. All four return HTTP 200. The existing catalog text and primary recap are unchanged.

Only the new upcoming card, two record rows and two room-count values were inserted into fresh authenticated HTML. All **74 existing event IDs, 43 image elements, existing cards/rows, styles, scripts and surrounding shell** were preserved. Page title, slug, status, template and featured media are unchanged. TruNorth and other unconfirmed appearances remain excluded.

| At the release check | Before | After |
|---|---:|---:|
| Retained public IDs | 74 | 76 |
| Past rooms | 71 | 72 |
| Past meetup editions | 33 | 33 |
| Past frames | 39 | 39 |
| Upcoming cards | 3 | 4 |
| Documentation links | 9 | 13 |

## Verification

- Required startup doctor and Varlock-injected read-only status completed. WordPress 7.0.7; no public smoke failure or warning. The existing Aurora version-header difference remains documented; no theme deployment occurred.
- **110 focused tests and 170 subtests** passed across the catalog contract, fragment merge, renderer, past record and guarded deployer. No production code changed.
- Full `make verify`, documentation truth checks and `git diff --check` passed before the release-receipt commit.
- Dry-run deploy saved a private snapshot before the single content-only write. Fresh identity and source-hash checks refused concurrent edits.
- Authenticated readback equals the candidate. Public normal and fresh requests both returned 200 with 76 IDs, 43 images, four upcoming cards and 13 documentation links.
- Actual Chromium, private preview and normal live URL, at **1440, 768 and 390 pixels**: all cards fit, existing card images decode, registration/recap targets match, keyboard focus is visible, zero horizontal overflow and zero page errors. Screenshots were inspected.
- Controlled festival cutoff: three upcoming cards, 73 past rooms, 40 frames. One minute before November's day-after cutoff its card remains visible; one minute after it enters the past record, leaving zero upcoming cards, 76 rooms, 41 frames and 33 editions. Stats remain visible when the upcoming list is empty. These are browser-clock tests, not fabricated event activity.
- Luma's direct urllib fetch returned 403; its public web readback independently confirmed the exact listing. This was a source-access limitation, not a WordPress write failure.

## Maintenance and recovery

The weekly `kriskrug-events-weekly-proposals` heartbeat retains its Monday 09:00 schedule and propose-only scope. Its prompt and private state now recognize both entries as applied. It will not repeat the November approval request. #1102 remains open for the separately scoped event-driven intake; no instant inbox/calendar webhook is claimed. The six-hour first-real-KRÜG-signup monitor remains active and unchanged.

Private packet in the original checkout: `.generated/current-state/events-november-allin-2026-10-25/`. It contains raw before/applied snapshots, the exact diff, manifest, public source/page readbacks, screenshots, browser reports and the guarded adapter. No credentials are stored in the packet.

- Original raw SHA-256: `42ba3c5eae6feb68049c837a29bbb3ea13cf1a475c140c7a229d31880c3a49cf`.
- Candidate and stored raw SHA-256: `f904be2dbdea5b9ffddb72f9d19b54785cdf182cf4768ece5b127eae0270e2df`.
- Pre-write snapshot: `snapshots/page-2250-events-20261026T051514Z.json`.
- Rollback was previewed after the write without changing production. To restore, run the packet's `deploy.py --restore <snapshot> --execute --expect-current-sha256 <fresh-preview-hash>` through Varlock. A changed live hash stops the restore. Preserve the snapshot and packet.
