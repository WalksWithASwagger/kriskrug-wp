# Decision packet: parked plugins (`kk-sidebar-promos`, `kk-marquee-board`)

**Date:** 2026-08-02
**Issue:** [#571](https://github.com/WalksWithASwagger/kriskrug-wp/issues/571)
**Mode:** repo-only. No live writes, no deploy, no zip built.
**Gate run:** `make plugin-smoke` exit 0 (both plugins pass) on PHP 8.5.9.

This packet answers three things per plugin: is it live, what would deploying cost, and what
should happen to it. The KK decision line at the bottom is the only thing still open.

---

## 1. Live truth first

Neither plugin is running on kriskrug.co. Confidence: **high**, because the evidence is
positive-signal rather than one page that happened to look empty.

Both plugins register a custom post type on `init`, unconditionally, the moment they activate.
That makes the public REST surface a reliable detector: it does not depend on the theme, on
which page you load, or on whether an asset-dequeue snippet stripped the CSS.

| Probe | Expected if live | Observed 2026-08-02 |
|---|---|---|
| `GET /wp-json/wp/v2/types` | contains `kk_promo` and `marquee_board` | 200, 16 types, neither present |
| `GET /wp-json/` route index | `/wp/v2/marquee_board` collection route | 445 routes, 20 namespaces, no marquee or promo route |
| `GET /marquee/` (CPT archive, `has_archive => true`) | 200 archive | **404** |
| `GET /wp-content/plugins/kk-sidebar-promos/assets/css/sidebar-promos.css` | 200 | **404** |
| `GET /wp-content/plugins/kk-marquee-board/assets/marquee.css` | 200 | **404** |
| Sitemap index `/sitemap.xml` | a `marquee_board` sub-sitemap | 301 to core `wp-sitemap-*.xml`, post/page/category/tag/user only, zero marquee entries |
| HTML of `/`, `/about/`, `/blog/`, `/glossary/`, newest post | `kk-sp__` card markup or plugin asset paths | zero hits on all five |

Two caveats stated honestly:

- The bare-404 asset probes are the **weakest** evidence here. Pagely returns 403 on
  `plugins/jetpack/readme.txt`, so this host does apply path rules, and the live site also runs
  the "KK Asset Diet" snippet that dequeues plugin CSS/JS. A missing stylesheet alone would not
  prove much. The REST type list, the REST route index, and the core sitemap all would still
  show a registered CPT regardless of any of that, and all three come back clean.
- The live plugin roster visible from REST namespaces is Akismet, Code Snippets, Redirection,
  Jetpack (plus Boost, Protect, My Jetpack), Popup Maker, Google Site Kit, Jetpack CRM, and the
  WP Abilities/MCP adapter. Neither KK plugin is in it.

Separate but relevant: the homepage LED marquee that **is** live is served by the theme
(`theme/kk-aurora/parts/marquee-current.html` plus `assets/js/marquee.js`), not by the plugin.
The plugin only adds the `/marquee/` archive and the per-board single pages. Nothing on the
homepage breaks by leaving the plugin off.

---

## 2. `kk-sidebar-promos` v0.1.2

**What it does.** A `kk_promo` custom post type with two flavours. Pillar promos are evergreen
(membership, courses, community) and rotate weekly. Featured promos carry an "active until" date
and auto-move to draft the day after it passes. A daily WP-Cron job runs the expiry, a second one
pulls the next upcoming event from a Luma iCal feed and files it as a Featured promo. Rendering is
available three ways: the `kk/sidebar-promos` block, a classic widget, or `[kk_sidebar_promos]`.
Activation seeds four pillars and schedules both cron jobs.

**Files:** 8 PHP files plus one stylesheet, roughly 1,100 lines. Smoke coverage in
`plugins/kk-sidebar-promos/tests/smoke.php` (242 lines) hits limit clamping, selection and weekly
rotation, the empty state, attachment alt handling, expiry, and the iCal parser.

**What deploying would take.** `make sidebar-promos-package COPY_PATH=1 OPEN_ADMIN=1`, upload
under Plugins then Add New then Upload Plugin, activate, paste the Luma iCal URL in settings, run
one manual sync, then place the block. Call it 30 to 45 minutes with KK at the keyboard, per
`plugins/kk-sidebar-promos/DEPLOYMENT.md`.

**Rollback.** Deactivate. That unschedules both cron jobs and flushes rewrite rules. The `kk_promo`
posts stay in the database, so reactivating restores state without data loss. Low blast radius,
with one real caveat: activation writes four seeded posts and two cron entries into production, so
"rollback" leaves residue that has to be cleaned by hand if the answer is a permanent no.

**The blocker, and it has not moved.** There is no sidebar to put this in. `theme/kk-aurora/parts/`
contains exactly four parts: `footer.html`, `header.html`, `marquee-current.html`,
`speaking-proof-grid.html`. No `sidebar.html`, no `dynamic_sidebar` call, no widget area anywhere
in the tracked theme. The word "sidebar" appears in exactly one tracked theme file, and it is
`IMPLEMENTATION-PLAN.md`. The live post I checked renders no element with a sidebar class at all.
This is the same finding that closed [#196](https://github.com/WalksWithASwagger/kriskrug-wp/issues/196)
as no-go on 2026-06-17, re-verified today against both the repo and the live render.

**Recommendation: keep parked.**

Not archive. The code is clean, it passes its own tests, and the underlying problem it solves
(stale event promos rotting in a promo slot after the event is over) is a real recurring problem
that will come back the moment Aurora grows any promo surface. Archiving it would mean rewriting
it later. Not deploy either, because deploying a renderer with nowhere to render is how you end up
with four orphan seeded posts and two cron jobs firing daily against a block nobody placed.

Park it, banner it, and revisit if and only if Aurora gains a sidebar or promo rail. That trigger
is worth naming out loud: **if a `parts/sidebar.html` or equivalent promo rail lands in the theme,
reopen this as a deploy issue with the exact target surface named.**

---

## 3. `kk-marquee-board` v0.1.0

**What it does.** Registers the public `marquee_board` CPT so `/marquee/` becomes a real WordPress
archive and each board gets its own `/marquee/<slug>/` page. Board fidelity (lines, week, skin,
attribution, source, tags) lives in REST meta, the rendered LED board is the post content, the dek
is the excerpt, the OG card is the featured image. Each board emits Article JSON-LD plus a
breadcrumb. Boards are pushed from the repo by `scripts/marquee/sync.py`, which is create-by-default,
slug-idempotent, and dry-run by default. Source of truth stays `content/marquee/marquee.json`.

**Files:** 3 PHP files plus CSS and JS, roughly 200 lines of PHP. Smoke in
`plugins/kk-marquee-board/tests/smoke.php`. Theme templates `archive-marquee_board.html` and
`single-marquee_board.html` already exist in `theme/kk-aurora/templates/`, so they would ship on
the next theme cutover.

**What deploying would take.** More than the sidebar plugin, because the plugin alone gets you an
empty archive. Full go-live is: package and upload and activate, flush permalinks, verify
`/marquee/` returns 200, add REST credentials, dry-run `scripts/marquee/sync.py`, then run it with
`--execute` to create boards and upload OG images, then confirm the boards land in the sitemap.
That is a multi-step live-write sequence, and steps 4 through 6 are exactly the REST-write shape
that the 2026-05-15 incident rules govern.

**Rollback.** Deactivate, which flushes rewrite rules and stops `/marquee/` resolving. Boards
remain in the database and can be trashed from wp-admin. Recoverable, but the sync step publishes
real indexable URLs, so a rollback after Google has crawled them means 404s or redirects to clean
up. Bigger blast radius than the sidebar plugin.

**Two facts that argue against deploying.** First, [#406](https://github.com/WalksWithASwagger/kriskrug-wp/issues/406)
already researched this and recommended, in writing, item 3: do not activate the gated Tier 3
WordPress plugin or the `/marquee/` archive, because "the compounding-SEO-archive ambition was
never turned on and adds maintenance drag for a payoff the site does not need." Second, KK's own
teardown quote on [#405](https://github.com/WalksWithASwagger/kriskrug-wp/issues/405) is "It looks
broken and static. I don't know why it's there." The product question about what the marquee is
for is still open. Building it a public SEO archive before answering that is backwards.

**Recommendation: keep parked, and it is the closer of the two to archive.**

The difference from the sidebar plugin is that the sidebar plugin is blocked on a missing surface,
which could appear. This one is blocked on an unanswered product question, and the last written
answer to that question was "keep the visual, kill the automation." Under that recommendation the
plugin never ships. I am still saying park rather than archive today for one reason: the marquee
direction was never formally decided, `#406` closed as a research spike rather than a ruling, and
archiving code on the strength of a recommendation nobody accepted is the kind of cleanup that has
to be undone.

Named trigger: **if KK accepts #406 Option B or Option A, this plugin should be archived with a
tombstone in the same pass, along with `.github/workflows/marquee-weekly.yml`, which is still on a
Monday cron.**

One doc drift found while reading, not fixed here because it is outside this lane's file
ownership: `plugins/kk-marquee-board/readme.txt` and `DEPLOYMENT.md` both say boards get indexed
via the Jetpack sitemap. Live is serving core WordPress sitemaps at `wp-sitemap-*.xml`, not
Jetpack's. The auto-include behaviour for public CPTs holds either way, so nothing is broken, but
the reference is stale and should be corrected whenever those files are next touched.

---

## 4. What this PR actually changes

The safe half of option 2 from the issue, applied to both plugins regardless of the final ruling:

- `plugins/kk-sidebar-promos/README.md` (new): STATUS banner, built-not-deployed, verified
  2026-08-02, deploy requires KK approval.
- `plugins/kk-marquee-board/README.md` (new): same.
- This packet.

That is the accident-prevention half. `make sidebar-promos-package` and `make marquee-package` both
still exist and still work, and a session skimming a clean, smoke-passing plugin directory could
reasonably read it as ready to push. The banner is what stops that. It costs nothing and it does
not pre-empt the decision.

Left deliberately untouched: `readme.txt`, `DEPLOYMENT.md`, the plugin code, `AGENTS.md`, and the
Makefile targets. If the ruling is archive, removing the targets and the AGENTS.md mention belongs
in that follow-up, not here.

---

## 5. KK decision line

| Plugin | Recommendation | Alternative if you disagree |
|---|---|---|
| `kk-sidebar-promos` | **Keep parked.** Revisit when Aurora has a sidebar or promo rail. | Archive with tombstone if you are confident Aurora will never carry a promo rail. Do not deploy: there is no render target. |
| `kk-marquee-board` | **Keep parked.** Blocked on the open marquee product question. | Archive with tombstone, together with `marquee-weekly.yml`, if you are ready to accept #406 Option A or B. Do not deploy: #406 explicitly recommends against activating it. |

Neither recommendation is deploy. If either answer comes back "archive," the follow-up issue needs
to cover: move to an archive path, tombstone note, drop the `make` package target, and strip the
`AGENTS.md` orientation mention.

---

**Verification trail for this packet:** `make plugin-smoke` exit 0. Live probes were read-only
`curl` GETs against public endpoints on 2026-08-02. No authentication was used, no WordPress write
of any kind was made, no zip was built.
