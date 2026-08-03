# KK Sidebar Promos

> **STATUS: BUILT, NOT DEPLOYED. PARKED.**
> This plugin is **not installed and not active on kriskrug.co.** Verified 2026-08-02 by public
> readback: `/wp-json/wp/v2/types` does not list `kk_promo`, the REST route index has no promo
> collection route, and no `kk-sp__` markup or plugin asset path appears on `/`, `/about/`,
> `/blog/`, `/glossary/`, or the newest post.
> **Do not deploy this without KK approval.** `make sidebar-promos-package` builds an upload zip
> and the smoke tests pass, which makes this directory look ready to push. It is not. See
> [`../../docs/current-state/DECISION-PARKED-PLUGINS-2026-08-02.md`](../../docs/current-state/DECISION-PARKED-PLUGINS-2026-08-02.md)
> and issue [#571](https://github.com/WalksWithASwagger/kriskrug-wp/issues/571).

## Why it is parked

There is nowhere to render it. The Aurora theme has no sidebar and no widget area:
`theme/kk-aurora/parts/` contains only `footer.html`, `header.html`, `marquee-current.html`, and
`speaking-proof-grid.html`. No `sidebar.html`, no `dynamic_sidebar` call, no widget-area template.
Issue [#196](https://github.com/WalksWithASwagger/kriskrug-wp/issues/196) closed as no-go on
2026-06-17 for this exact reason, and the finding was re-verified against the repo and the live
render on 2026-08-02.

Activating it anyway would seed four promo posts and schedule two daily cron jobs in production
feeding a block nobody has placed.

## Unpark trigger

If Aurora gains a sidebar, a promo rail, or any equivalent widget surface, open a fresh deploy
issue that names the exact target template part, plus the rollback path. Not before.

## What it does

A `kk_promo` custom post type with two flavours:

- **Pillar** promos are evergreen (memberships, courses, communities) and rotate weekly so the slot
  does not look frozen.
- **Featured** promos carry an "active until" date and auto-move to draft the day after it passes.

A daily WP-Cron job runs the expiry; a second one reads a Luma iCal feed and files the next
upcoming event as a Featured promo. Renders via the `kk/sidebar-promos` block, a classic widget, or
`[kk_sidebar_promos limit="4"]`.

Version 0.1.2. First built 2026-05-15.

## Local checks (safe, no live writes)

```bash
make plugin-smoke                              # both parked plugins
php plugins/kk-sidebar-promos/tests/smoke.php  # this one only
find plugins/kk-sidebar-promos -name '*.php' -print0 | xargs -0 -n1 php -l
```

Passing smoke tests are **not** deploy authorization. They only mean the PHP is internally
consistent.

## Other docs in this directory

- [`DEPLOYMENT.md`](DEPLOYMENT.md): the runbook that applies **only if** KK approves a deploy.
- [`readme.txt`](readme.txt): WordPress-style plugin readme and changelog.
