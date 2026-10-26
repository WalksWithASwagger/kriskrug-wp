# Events maintenance #1102: October 25, 2026

The weekly propose-only loop is active as Codex heartbeat `kriskrug-events-weekly-proposals`, **Kriskrug Events weekly proposals**, Monday 09:00 America/Vancouver. Creation returned ACTIVE and the app view readback succeeded. No matching Events automation existed; the separate SEO digest was inspected and retained. The worker keeps proposals local and stays quiet when nothing actionable changes. It cannot publish, send messages, change calendars or create public issue comments.

## First sweep

Fresh source is main after merged #1153 (`69d94d39`), with the #1101 live readback. The 74 production identities remain intact; the current record is 71 past rooms, 33 meetup editions and 39 frames. Three upcoming cards remain. #1108 already covered the original September audit batch. #1099–#1101 have merged and their scoped live changes are verified.

A bounded Calendar read and the [public Luma event](https://luma.com/nov-vanai) corroborate the November 25 Vancouver AI meetup at H.R. MacMillan Space Centre. The public page explicitly identifies Kris as host and MC. [The exact proposed catalog patch](../proposals/events-1102-november-meetup.patch) adds only `vancouver-ai-meetup-2026-11-25`, retaining source URL and explicit confirmation, with empty documentation/media slots. No edition number, artwork or recording is inferred. Existing identities are byte-preserved. The patch is **not applied** and no WordPress write was made for this proposal.

If approved and applied as a bounded update to the current live page, this adds one upcoming record (75 retained IDs; four upcoming cards) while keeping past counters at 71/33/39 on the audit date. Recompute at application time. Full catalog output also contains the held ALL IN entry and must not be sent to production as a replacement.

Coverage is deliberately limited: Calendar and public host/coverage sources were checked; no blanket inbox or iMessage audit was performed. Invitations and unrelated BC + AI activities are not treated as confirmed Kris appearances. The weekly sweep is now scheduled; same-day confirmation and day-after checks are documented active-session hooks, not installed webhooks. #1102 remains open for that event-driven integration rather than claiming it exists.

## Verification

The proposed record passes the shared normalization contract. Parsing the proposed YAML confirms exactly one new identity and no changes to existing rows. `git apply --check` validates the review patch without applying it. Docs truth, relative-link checks and `git diff --check` pass. The heartbeat was viewed after creation. No production code, workflow settings, subscriptions or other automation changed.
