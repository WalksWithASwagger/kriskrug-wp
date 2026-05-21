=== KK Sidebar Promos ===
Contributors: kriskrug
Tags: sidebar, widget, promo, automation
Requires at least: 6.2
Tested up to: 6.6
Requires PHP: 7.4
Stable tag: 0.1.2
License: GPLv2 or later

Auto-managed sidebar promo system. Featured promos auto-expire on their end date; evergreen "pillar" promos rotate to fill the remaining slots. The next Vancouver AI meetup syncs in from Luma automatically.

== Description ==

Solves the recurring problem of stale event promos lingering in the sidebar after the event is over.

* **Pillar promos** — evergreen things that always make sense to promote (memberships, courses, communities). Rotate weekly so the sidebar doesn't look static.
* **Featured promos** — time-bound things that require an end date. Auto-move to draft the day after they expire.
* **Luma sync** — point at your Luma calendar's iCal feed and the next upcoming event becomes a Featured promo automatically.

Render via the **KK Sidebar Promos** block, the **KK Sidebar Promos** widget, or `[kk_sidebar_promos limit="4"]`.

== Installation ==

1. Upload the `kk-sidebar-promos` folder to `/wp-content/plugins/`.
2. Activate the plugin (this seeds the four pillars and schedules the daily cron jobs).
3. Go to **Sidebar Promos → Settings** and paste your Luma iCal URL.
4. Drop the **KK Sidebar Promos** block into your sidebar template (or use the widget / shortcode).

== Development Checks ==

Run `php plugins/kk-sidebar-promos/tests/smoke.php` before packaging. It checks the no-promos empty state, attachment alt behavior, featured-promo expiry behavior, and Luma iCal parsing without a full WordPress install.

== Changelog ==

= 0.1.2 =
* Clamp shortcode, block, and widget promo limits to the supported 1-8 range.
* Refine card focus and hover states so keyboard focus is stable and visible while hover lift stays pointer-only.
* Expand smoke coverage for limit normalization, selection, and weekly pillar rotation.

= 0.1.1 =
* Preserve real attachment alt text in promo images; treat missing alt as decorative instead of repeating the visible promo title.
* Add local smoke coverage for rendering empty state, image alt behavior, featured-promo expiry behavior, and Luma iCal parsing.

= 0.1.0 =
* Initial release: CPT, auto-expiry, Luma iCal sync, block + widget + shortcode, four seeded pillars (Animation Accelerator, RAP Certification, BC + AI Membership, Vancouver AI Community).
