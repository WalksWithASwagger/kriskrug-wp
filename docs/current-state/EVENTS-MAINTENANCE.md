# Events maintenance: proposal and verification workflow

Owner: Kris Krüg. Implementation issue: [#1102](https://github.com/WalksWithASwagger/kriskrug-wp/issues/1102).

## Weekly sweep

**Kriskrug Events weekly proposals** is active in Codex on Mondays at 09:00 America/Vancouver. Kris owns it. Each completed sweep saves a private receipt in `.generated/current-state/events-maintenance/`. Step 7 defines when the run should also post a notice in its own chat.

The first run started on November 16 and ended at the account usage limit before it wrote a receipt. Check the latest dated receipt and the corresponding run history before treating a week as covered. Issue #1102 records the cadence decision.

## November 20 recovery sweep

A manual sweep checked the catalog against authenticated WordPress page 2250 and the logged-out Events page. All three showed 86 past rooms, 33 meetup editions, 41 frames and three upcoming cards. The private receipt `sweep-2026-11-20.md` in the directory above holds the exact proposed diff and coverage. It proposes adding the November 18 City Hall appearance and crediting the November 25 opening talk, *Original Intelligence*, on the existing meetup card. Review the proposal before applying it.

## November 11 manual sweep

The public-source sweep found no confirmed change to apply. The shared catalog
has 87 entries; the public page showed 84 past rooms, 33 meetup editions and
41 frames. November 23 AMPA and November 25 Vancouver AI remain upcoming;
November 5 Prompt Victoria is past. These are dated observations.

The [December 16 Vancouver AI listing](https://bc-ai.ca/events/2026-12-16-vancouver-ai-community-meetup)
confirms the event and venue but does not name Kris as host or speaker. The
public [Luma page](https://luma.com/dec-vanai) lists him as the host. Both
Google Calendar connectors were unavailable in the parallel audit, so the
result is limited to public sources. The November 11 sweep made no
private-message sweep, catalog edit or live write. See the
[follow-through receipt](reports/morning-followthrough-2026-11-11.md).

**December 16 ruling, 2026-11-12.** Kris ruled to add the meetup with the role
"Host & MC", the same wording as November 25. He gave no edition number, so
none is recorded. The display title "Vancouver AI Community Meetup: December
2026" comes from the public bc-ai.ca listing, and the catalog row merged in
[#1266](https://github.com/WalksWithASwagger/kriskrug-wp/pull/1266).

**December 16 is live, 2026-11-12.** With Kris's separate approval, page 2250
got one content-only write at 18:34 Vancouver. It added only the Upcoming card
and the hidden record row; counters stayed at 84 rooms, 33 editions and 41
frames. Normal and cache-busted public responses show the card with the Luma
link. Hashes, readbacks and the rollback steps are in the
[December 16 release receipt](reports/events-dec16-release-2026-11-12.md).

## Weekly sweep

1. Refresh current GitHub issue/PR state and the current-state front door. Read `scripts/events_page/events-catalog.yaml`, `meetup-editions.yaml` and `fragments/*.yaml` through `load_catalog()`. Preserve occupied checkouts and existing proposals.
2. Read live page **2250**, exact slug **events**, and the public `/events/` response. Credentials, if needed, flow through Varlock. Save any raw snapshots privately under `.generated/current-state/events-maintenance/`; public reports contain only redacted evidence.
3. Compare the next 90 days and the past 14 days with bounded read-only Calendar queries, public host/Luma pages, and relevant recent confirmation messages. Read exact candidate messages only where needed. Calendar presence or an invitation alone does not establish Kris's hosting/speaking role or authorize public inclusion. Private iMessage databases are not a source for this scheduled task; supplied confirmations can be evaluated in an active chat.
4. Check recently published kriskrug.co and BC + AI coverage for missing recap, gallery or recording links. Verify public canonical URLs, gallery anchors and credits. Use the [publisher checklist](../../scripts/notion-to-wp/README.md#event-coverage-publish-checklist); never infer rights from a thumbnail or overwrite registration URLs.
5. Compare live rollover and counters with the shared contract. #1100 already moves past events at the day-after-end cutoff, releases artwork and updates counters. Propose a fix only for observed drift, not a duplicate manual move.
6. Save an exact unified diff, source/date/role evidence, affected stable IDs, media/credit preservation notes, before/after counts, and any unresolved fields. Missing edition numbers, end times, roles or photos stay missing. Record coverage limits and unavailable sources explicitly.
7. Deduplicate against the last reviewed proposal. Notify Kris in the originating chat only for a new proposal, a live defect or an access decision. Do not create issue comments, message people, alter calendars, change the catalog or apply WordPress writes on a scheduled run.

Kris approves the concrete event/page proposal before application. Approval can cover a continuing, named release; do not ask again for steps already covered. For approved application, refresh the source, use a bounded patch that preserves unrelated live content and held entries, run the relevant tests/preview, snapshot, apply once, and verify authenticated plus public readbacks. Preserve rollback evidence and refuse to overwrite concurrent edits.

## Confirmation and post-event hooks

When a new confirmation arrives in an active authorized session, run steps 3–7 that day. When publishing event coverage, run the linked publisher checklist in the same approved pass. On the day after an event, verify the automatic transition and propose any newly available documentation links.

These hooks run during an authorized session. The installed weekly worker reads the sources listed above. Same-day confirmations and day-after checks depend on a session running at those times.

## Current baseline and applied first proposal

The September 29 first batch is already covered by merged #1108; #1099, #1100 and #1101 complete the data contract, live record/counters and documentation backfill. Do not repeat those fixes.

Kris approved the November 25 meetup and ALL IN entries, and both are now live. The [October 25 release receipt](reports/events-november-allin-release-2026-10-25.md) records 76 retained IDs, 72 past rooms, 33 meetup editions, 39 frames, four upcoming cards and 13 documentation links. The [original proposal patch](proposals/events-1102-november-meetup.patch) is already applied; do not apply it again. The October 25 record says the weekly heartbeat and private maintenance state recognized this release. TruNorth and other unconfirmed appearances remain excluded. Reconcile all baselines at each future run; these counts are dated evidence.
