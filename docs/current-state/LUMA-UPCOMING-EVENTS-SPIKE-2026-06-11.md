# Luma Upcoming Events MVP Spike

Date: 2026-06-11
Issue: #177
Related: #62, #196
Scope: documentation-only feasibility spike. No event MVP implementation, deploy, GitHub write, or production change.

## Question

Can the existing `plugins/kk-sidebar-promos` Luma iCal sync support a one-feed upcoming-events MVP before building the broader #62 multi-calendar portal?

## Short Answer

Yes, but as reuse-with-extension, not as a zero-code reuse.

The plugin already has the useful foundation for a one-feed MVP: one configurable Luma iCal URL, WordPress HTTP fetch, a lightweight iCal parser, daily WP-Cron, manual sync from admin, a private promo CPT, and local smoke coverage. That is enough to avoid starting from scratch.

The current sync deliberately imports only the next upcoming event and turns it into one Featured sidebar promo. It does not persist a list of upcoming events, expose event-specific fields beyond summary/date/link, or render an event-list page/block. A real "upcoming events" MVP should extend the existing parser/sync path into a small one-feed event list, rather than treating the sidebar promo renderer as the product surface.

## What Exists

- `includes/luma-sync.php` fetches the configured iCal URL, parses VEVENT records, picks the earliest event whose `start_ts` is in the future, and upserts one published Featured promo keyed by `source=luma` and `source_id=<uid>`.
- `kk_sp_parse_ical()` can parse multiple VEVENT records from one feed, but the sync only uses the single next event.
- The parsed event shape is currently `uid`, `start_ts`, `summary`, `summary_short`, and `url`.
- `includes/cron.php` schedules daily `kk_sp_luma_sync` and daily Featured promo expiry.
- `includes/render.php` provides the existing block/widget/shortcode surface for sidebar promos. It is optimized for one Featured card plus rotating Pillars, not an event list.
- `DEPLOYMENT.md` documents manual admin upload, Luma iCal configuration, manual sync, daily cron, rollback, and pre-deploy smoke checks.
- `.github/workflows/test-pr.yml` runs the plugin smoke test when `plugins/kk-sidebar-promos/` changes.

## MVP Feasibility

Feasible MVP:

- One configured Luma iCal feed only.
- Upcoming events only.
- Render a simple page/block/shortcode listing the next N events from that feed.
- Each item can safely start with title/summary, start date/time, and event URL.
- No RSVP integration beyond linking to Luma.
- No multi-calendar merge, search, filters, subscribe output, or cross-project taxonomy.

Recommended implementation path for a follow-up issue:

1. Extract a small reusable function from the existing Luma path that returns normalized upcoming events from one iCal body/feed.
2. Add fixture-based tests for multiple VEVENTs, timezone dates, all-day dates, missing UID fallback, escaped text, old events being excluded, and ordering by start time.
3. Add either a shortcode/block for `[kk_upcoming_events]` or a narrow dynamic block that renders the next N normalized events.
4. Decide whether the MVP reads the feed live with transient caching or stores normalized events in a separate CPT/meta shape. Do not overload `kk_promo` unless the product stays "one featured promo."
5. Gate any production usage behind #196 if the work depends on deploying `kk-sidebar-promos`.

## Risks And Limits

- Product scope risk: #62 asks for a unified multi-source calendar with filters, subscriptions, and RSVP integration. The one-feed MVP should be positioned as a validation step, not a partial delivery of #62.
- Data model risk: `kk_promo` stores promo metadata, not event metadata. It stores the event date as a Featured promo end date and has no first-class start/end/location/status fields.
- Parser drift risk: Luma iCal output may change. Current parser covers a useful subset but does not currently persist description, location, organizer, status, recurrence, or event end time.
- Ordering risk: the promo renderer chooses the newest non-expired Featured promo by post date, not by event start time. That is fine for sidebar promos and wrong for an event list.
- Cron risk: WP-Cron depends on site traffic and plugin activation. A page/block MVP should have a visible stale/fallback state if the feed fetch fails.
- Deployment risk: the plugin is built and tested but still parked for production; #196 owns the deploy/park/archive decision.

## Follow-Up Issues

- Keep #62 parked as the broad unified calendar portal until the one-feed MVP proves useful.
- Resolve #196 before any production plugin deploy or production dependency on `kk-sidebar-promos`.
- New implementation issue: "Add one-feed Luma upcoming-events renderer" with scope limited to one feed, upcoming events only, no RSVP integration, no multi-calendar filtering.
- New test issue if split out: "Expand Luma iCal fixtures for upcoming-events MVP" covering multi-event parsing, timezone/all-day handling, ordering, stale feed behavior, and field escaping.
- New product decision issue if needed: "Choose upcoming-events surface" to decide between a page shortcode, dynamic block, or Aurora template placement.

## Verification Performed

- Read issue #177, #62, and #196 from GitHub without writes.
- Inspected `plugins/kk-sidebar-promos/includes/luma-sync.php`, `render.php`, `cron.php`, `settings.php`, `cpt.php`, `DEPLOYMENT.md`, `readme.txt`, and `tests/smoke.php`.
- Confirmed the existing local smoke test includes Luma iCal parser coverage and that CI runs it for sidebar promo plugin changes.

## Decision

Reuse the existing Luma sync foundation for a one-feed MVP, but implement the MVP in a separate follow-up code issue. Do not deploy the plugin or broaden #177 into event-product implementation.
