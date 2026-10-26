# Events catalog contract and reconciliation: October 25, 2026

Refs #1099, handing off to #1100 and #1101. This is an in-repository change with a read-only production comparison. No WordPress page save, media upload, event confirmation, or live deployment occurred.

## Reconciliation

Main was refreshed after #1149 merged. #1108 is confirmed merged as `6931d8ab4dcb34f579ee0d3893841c341ecad55b`; no competing Events PR was open. The shared source remains `scripts/events_page/events-catalog.yaml`, enriched by `meetup-editions.yaml` and `fragments/*.yaml`.

A fresh public `/events/` fetch was matched by `data-event-id` and `data-event-end`, not by copied counter text:

- All 74 live event identities exist in the merged catalog. None is duplicated within the complete record.
- All shared IDs have identical roll-off cutoff dates. No conflicting live/catalog date was found.
- The catalog has 75 publishable identities. Its sole extra is `2026-09-15-all-in-montreal`, the already-prepared, unpublished #402/PR #1141 record. This work does not approve or publish it.
- The catalog also retains the private proposed `trunorth-ai-leadership-summit-2026` row, for 76 total normalized records.
- Meetup #32 (`vancouver-ai-meetup-2026-08-26`), #33 (`vancouver-ai-meetup-2026-09-30`), Prompt Victoria (`2026-11-05-prompt-victoria`) and Capilano (`trecsa-world-tourism-day-2026`) from #1108 are present once and remain confirmed. #1018 is covered; no duplicate was added.
- Existing canonical recaps for AI Day, North House, Capilano and the prepared ALL IN record survive as both legacy `recap_url` and normalized `docs.recap`. Source/registration URLs remain unchanged.

The complete normalized before/after comparison finds no changed media object, source URL, title, date, end date, credit, or event ID. Only documentation lists are added and Meetup #27's status returns to the explicit catalog value `scaffold`: the old harvest default had silently promoted it to `confirmed`. Both statuses are historical public records, so output remains identical.

## Contract and validation

See the [pipeline input contract](../../../scripts/events_page/README.md#input-contract-for-1100). Missing/unknown status is unconfirmed. Harvest/fragment enrichment cannot promote a private authoritative row. Duplicate IDs/editions, invalid dates and unsafe documentation URLs stop generation. The renderer now uses the shared explicit status predicate; its layout, rollover and counters are otherwise untouched.

The existing production-mode local render is byte-for-byte unchanged: SHA-256 `8826b819a49b428b2c8703fd804f909902e917e79c85d7e9fba4f3c0b6f46b94`. It contains no local filesystem paths. The shell, all 41 art-bearing records, and source/credit data are preserved. No media sync was run.

Fourteen new focused contract tests cover all-status handling, base/harvest/fragment precedence, missing fields, duplicate IDs/editions, date validity, no invented time, legacy recap compatibility, independent documentation links, unsafe links and existing #1108 records. The 74 existing Events tests pass with the single expected contract update: new rows without status now remain unconfirmed. `make verify` passes all 1,133 Python tests, JavaScript validation, plugin/theme smoke tests, docs truth, PHP syntax and WordPress coding standards. The matching existing locked PHPCS runtime was added to PATH after the first run reported it missing; no dependencies or PHP sources changed. Ruff and `git diff --check` pass.

Private read-only evidence and the local review artifact are in `/Users/kk/Code/kriskrug-wp/.generated/current-state/events-catalog-1099-2026-10-25/`: `live.html`, `before.html`, `after.html`, `normalized-before.json`, and `reconciliation.json`.

## Owner choices retained

- October 27 at The Permanent: actual role and inclusion remain unconfirmed; omitted.
- IIA/KPMG October 5, TSC San Diego October 15, and TEDx West Van November 15: omitted until an explicit confirmation arrives.
- ALL IN's prepared record is not on the live page. Any future apply must preserve this distinction unless its publication is approved.

#1100 can now consume the tested contract for past-only record/counter semantics and independent recap/photos/video links. The day-after-end rollover and resume timer already shipped in #1134; do not redo them. #1101 can add verified documentation URLs and the publishing-checklist hook. Neither follow-up should infer missing roles, publish unconfirmed events, or treat catalog counts as live counts.
