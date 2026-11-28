# Track A Clanker & Canonical Cleanup Packet (2026-11-28)

**Status:** PREP ONLY. Repo payload updates and reviewed SEO metadata packet. No live WordPress writes have been run. Applying live requires separate explicit approval from Kris Krüg plus pre-write page snapshots.

## Scope

### 1. Tracked page body fixes (ready for guarded REST deploy)

| Page | ID | Slug | Change |
|---|---:|---|---|
| Work | `2672` | `work` | Fix `Ethos Lab Block Party` to canonical `Ethọ́s Lab Block Party` in `content/source-packs/content-architecture-2026/wp-payloads/work.html`. |
| About | `1208` | `about` | Add a space before `<br />` in `I make things. <br />I bring people together.` in `content/source-packs/content-architecture-2026/wp-payloads/about.html` so screen readers and crawlers do not mash the sentences together. |
| Photography | `12013` | `photography` | Add a space before `<br />` in `In the room. <br />Behind the lens.` in `content/source-packs/content-architecture-2026/wp-payloads/photography.html`. |
| Data Centres Reading Guide | `13069` | `data-centres-public-compute-and-the-public-interest` | Remove the duplicate `<h1>` in `content/drafts/2026-11-24-data-centres-guide-redesign/build.py`, `guide.css`, and `content.new.html` by matching the repo's visually hidden `.aurora-page-header` `<h1>` + `<h2 class="dc-hero__title">` pattern. |

### 2. Live SEO title & meta description cleanup (`seo-meta-updates.json`)

Live public HTML readback on 2026-11-28 found stale Jetpack SEO metadata stored in `wp_postmeta` / `wp_options`:

- `/subscribe/` (page `2808`): live `<meta name="description">` still reads *"Subscribe to my newsletter, and let's explore this thrilling landscape together. Learn, grow, and be inspired as we navigate the ever-evolving..."* and `<title>` reads *"Stay Connected With Kris Krüg Email Newsletter"*.
- `/work/` (page `2672`): live meta uses `Ethos Lab` and `BC+AI`.
- `/generative-ai-services/` (page `2666`) and `/` (homepage): live meta uses `BC+AI` instead of `BC + AI`.

**Dependency note:** `theme/kk-aurora/inc/seo-meta-rest.php` previously registered `jetpack_seo_html_title` and `advanced_seo_description` for `post` only, not `page`. Once Aurora `1.7.5` deploys (registering both keys for `page`), the page meta rows in `seo-meta-updates.json` can be applied cleanly through the REST API with readback. The homepage option `advanced_seo_front_page_description` updates in wp-admin (or WP-CLI).

## Verification & Rollback Plan (for future live apply)

1. Capture live `context=edit` snapshots for pages `2672`, `1208`, `12013`, `13069`, `2808`, `2666` into `backup/YYYYMMDD-HHMMSS/`.
2. Dry-run each payload diff against live `content.raw` with slug/ID/status checks before any write.
3. Apply only after explicit KK live-write approval, then verify both authenticated `context=edit` readback and logged-out public HTML.
4. Rollback: restore the saved `content.raw` / `meta` JSON from the pre-write snapshot directory.
