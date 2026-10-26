# Events maintenance: proposal and verification workflow

Owner: Kris Krüg. Implementation issue: [#1102](https://github.com/WalksWithASwagger/kriskrug-wp/issues/1102). The weekly Codex heartbeat **Kriskrug Events weekly proposals** runs Monday at 09:00 America/Vancouver in the originating chat. It prepares local review material; it does not publish or change the source catalog.

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

These are operating hooks, not installed webhooks. The scheduled worker is weekly; it does not promise instant inbox/iMessage monitoring or guaranteed day-after execution. #1102 remains open for a separately scoped event-driven intake integration if that stronger cadence is required. Do not expand the weekly heartbeat's access or create watchers silently.

## Current baseline and first proposal

The September 29 first batch is already covered by merged #1108; #1099, #1100 and #1101 complete the data contract, live record/counters and documentation backfill. Do not repeat those fixes. The live page retains 74 IDs, with 71 past rooms, 33 meetup editions and 39 frames at the October 25 check.

The [October 25 sweep receipt](reports/events-maintenance-1102-2026-10-25.md) records a new November 25 meetup proposal. The [exact patch](proposals/events-1102-november-meetup.patch) is review material only. Prepared ALL IN and unconfirmed appearances remain absent from production. Reconcile all baselines at each future run; these counts are dated evidence.
