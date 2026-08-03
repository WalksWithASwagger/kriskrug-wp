# KK Marquee Board

> **STATUS: BUILT, NOT DEPLOYED. PARKED.**
> This plugin is **not installed and not active on kriskrug.co.** Verified 2026-08-02 by public
> readback: `/marquee/` returns **404**, `/wp-json/wp/v2/types` does not list `marquee_board`, the
> REST route index has no `marquee_board` collection, and the live sitemap index
> (`wp-sitemap-*.xml`) contains zero marquee entries.
> **Do not deploy this without KK approval.** `make marquee-package` builds an upload zip and the
> smoke tests pass, which makes this directory look ready to push. It is not. See
> [`../../docs/current-state/DECISION-PARKED-PLUGINS-2026-08-02.md`](../../docs/current-state/DECISION-PARKED-PLUGINS-2026-08-02.md)
> and issue [#571](https://github.com/WalksWithASwagger/kriskrug-wp/issues/571).

## The live marquee does not come from here

The LED board on the homepage **is** live, and it is served entirely by the theme:
`theme/kk-aurora/parts/marquee-current.html` plus `theme/kk-aurora/assets/js/marquee.js`. This
plugin adds only the `/marquee/` archive and the per-board `/marquee/<slug>/` pages. Leaving it
parked breaks nothing on the homepage.

## Why it is parked

The product question is still open. Research spike
[#406](https://github.com/WalksWithASwagger/kriskrug-wp/issues/406) recommended in writing, item 3:
do not activate the gated Tier 3 WordPress plugin or the `/marquee/` archive, on the grounds that
the compounding-SEO-archive ambition was never switched on and adds maintenance drag for a payoff
the site does not need. KK's teardown note on
[#405](https://github.com/WalksWithASwagger/kriskrug-wp/issues/405) was "It looks broken and
static. I don't know why it's there."

Go-live is also not a one-step deploy. The plugin alone yields an empty archive; boards only appear
after `scripts/marquee/sync.py --execute` writes real indexable URLs over REST. That is a live-write
sequence under the post-2026-05-15 rules, and rolling it back after crawl means cleaning up 404s.

## Unpark or archive trigger

If KK accepts #406 Option B (keep the visual, kill the automation) or Option A (kill it entirely),
this plugin should be **archived with a tombstone** in that same pass, together with
`.github/workflows/marquee-weekly.yml`, which is still on a Monday cron. If the marquee instead gets
a product owner and a reason to have a public archive, open a fresh deploy issue with the rollback
path spelled out.

## What it does

Registers the public, REST-enabled `marquee_board` custom post type so `/marquee/` becomes a real
WordPress archive with `/marquee/<slug>/` singles. Board fidelity (lines, week, skin, attribution,
source, tags) is stored as REST meta, the rendered LED board is the post content, the dek is the
excerpt, the OG share card is the featured image. Each board emits Article JSON-LD plus a
breadcrumb. Boards are pushed from the repo by `scripts/marquee/sync.py` (create-by-default,
slug-idempotent, dry-run by default). Source of truth stays `content/marquee/marquee.json`.

Theme templates `archive-marquee_board.html` and `single-marquee_board.html` already exist under
`theme/kk-aurora/templates/` and would ship on a normal theme cutover.

Version 0.1.0. Built 2026-06-28.

## Local checks (safe, no live writes)

```bash
make plugin-smoke                            # both parked plugins
php plugins/kk-marquee-board/tests/smoke.php # this one only
find plugins/kk-marquee-board -name '*.php' -print0 | xargs -0 -n1 php -l
```

Passing smoke tests are **not** deploy authorization. They only mean the PHP is internally
consistent.

## Other docs in this directory

- [`DEPLOYMENT.md`](DEPLOYMENT.md): the runbook that applies **only if** KK approves a deploy.
- [`readme.txt`](readme.txt): WordPress-style plugin readme and changelog.

Known stale reference in both of those files: they describe boards being indexed via the Jetpack
sitemap. Live serves core WordPress sitemaps at `wp-sitemap-*.xml`. Public CPTs are auto-included
either way, so nothing is broken, but the wording should be corrected next time those files are
touched.
