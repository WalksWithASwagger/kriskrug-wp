=== KK Marquee Board ===
Contributors: kriskrug
Tags: cpt, marquee, archive, seo
Requires at least: 6.2
Tested up to: 6.6
Requires PHP: 7.4
Stable tag: 0.1.0
License: GPLv2 or later

Serves The Marquee at /marquee/ — a custom post type for the self-improving marquee boards that lead the homepage. Public, REST-enabled (synced from the repo by scripts/marquee/sync.py), and auto-included in the Jetpack sitemap.

== Description ==

The Marquee is the LED "now showing" board in the homepage hero. Each week the sharpest line from Kris's writing is remixed onto a board; past boards are archived. This plugin makes that archive a real, served, indexed part of kriskrug.co.

* **Custom post type `marquee_board`** — public, with a `/marquee/` archive and `/marquee/<slug>/` single pages.
* **Board fidelity in meta** — board lines, week, skin, attribution, source, and tags are stored as REST meta; the rendered LED board is the post content; the dek is the excerpt; the OG share card is the featured image.
* **Article schema** — each board emits Article JSON-LD linked to the site Person entity, plus a breadcrumb.
* **Sync, not authoring** — the source of truth is `content/marquee/marquee.json`; `scripts/marquee/sync.py` pushes boards over REST (create-by-default, slug-idempotent, dry-run first).

== Installation ==

1. Upload the `kk-marquee-board` folder to `/wp-content/plugins/`.
2. Activate the plugin (the activation hook flushes rewrite rules so `/marquee/` resolves).
3. Deploy the theme templates `archive-marquee_board.html` + `single-marquee_board.html` on the next theme cutover.
4. Run `scripts/marquee/sync.py` (dry-run, then `--execute` with approval) to publish boards.

See DEPLOYMENT.md for the full runbook and rollback.

== Changelog ==

= 0.1.0 =
* Initial release: marquee_board CPT, meta, Article schema, board asset enqueue.
