# Live Site Inventory — kriskrug.co

> **STATUS: Historical.** Frozen May 14 baseline fingerprint. For live WP / theme versions use [`CURRENT-STATE-2026-07-16.md`](CURRENT-STATE-2026-07-16.md) + public `style.css` readback.

**Captured:** 2026-05-14 from public endpoints (no admin access used).
**Method:** WP REST API, homepage HTML, response headers. See `raw/` for source dumps.

## Identity

| Field | Value |
|---|---|
| URL | https://kriskrug.co |
| Name | Kris Krüg \| Generative AI Tools & Techniques |
| Tagline | Empowering Events & Organizations for the AI Age |
| Timezone | UTC-8 (no DST string set — worth fixing) |
| Site icon / logo | **Not set** (`site_icon: 0`, `site_logo: 0`) |
| WordPress.com blog ID | 159424804 |
| Jetpack-connected | Yes, **Free plan** (confirmed via `isFreePlan: true` in instant-search config) |

## Hosting & infrastructure

| Field | Value |
|---|---|
| Host | **Pagely** (enterprise managed WP) |
| Web server | `Pagely-ARES/1.22.2` |
| Edge cache | Pagely PressCache (`x-gateway-cache-status: HIT` on homepage) |
| CDN origin for assets | `s5102.pcdn.co` (Pagely CDN) |
| WordPress version | **6.9.4** |
| Shortlink namespace | `wp.me/PaMVFO-*` |
| Server IP | unknown (fronted by Pagely gateway) |

> ⚠️ The repo's `docs/cloudways-setup.md` describes a *different* server — a Cloudways dev/staging instance at `24.144.80.107`. That is **not** production. Production lives on Pagely.

## Theme

| Field | Value |
|---|---|
| Active theme | **catch-responsive** (Catch Responsive, classic theme) |
| Theme version | 2.8.7 (per `blocks.css?ver=2.8.7`). The `?ver=20231219-181413` on the main stylesheet is a cache-bust timestamp from the vendor's release; whether the local copy has been modified isn't knowable without SSH-level inspection. |
| Theme type | **Classic** (not Full Site Editing) — sidebar layout, `nav-primary` + `catchresponsive-nav-menu`, `#main` + `.sidebar-primary` structure |
| Custom background | `https://s5102.pcdn.co/wp-content/themes/catch-responsive/images/body-bg.jpg` |
| Custom theme edits | Unknown — needs SSH to diff against upstream Catch Responsive |

The REST API exposes `wp_template`, `wp_template_part`, `wp_global_styles`, and `wp_font_family` post types, but those are WP core endpoints that exist on every modern install; the active *theme* doesn't use them. Don't be misled by the namespace list — this is a classic theme.

## Plugins (fingerprinted from public assets)

| Plugin | Version | Notes |
|---|---|---|
| **Jetpack** | 15.8 | Many modules active: Stats, Instant Search, Carousel, Likes, Boost, Forms, Testimonials, Protect, Blaze, Import |
| **Popup Maker** | 1.22.0 | `pum-*` markup on homepage; popup theme ID 3875 is the default |
| **Zero BS CRM** (Jetpack CRM) | unknown | REST namespace `zbscrm/v1` |
| **Site Kit by Google** | 1.178.0 | GA4 ID `G-X7JE8B32L7`; namespace `google-site-kit/v1` |
| **Akismet** | unknown | namespace `akismet/v1` |

**Inferred from REST namespaces but not confirmed loaded on homepage:** `jp_pay` (Jetpack Payments, exposes `jp_pay_order` / `jp_pay_product` post types).

Other plugins may exist that don't surface front-end assets — list will only be complete once we have wp-admin or SSH access.

## Content shape

### Post types (custom + core)

| Type | REST base | Source |
|---|---|---|
| post, page, attachment | core | WP |
| `jetpack-testimonial` | `jetpack-testimonial` | Jetpack Testimonials module |
| `feedback` | `feedback` | Jetpack Forms responses |
| `jetpack_form` | `jetpack-forms` | Jetpack Forms |
| `popup`, `popup_theme`, `pum_cta` | `popups`, `popup-themes`, `ctas` | Popup Maker |
| `jp_pay_order`, `jp_pay_product` | same | Jetpack Payments |
| `jb_store_css` | same | Jetpack Boost (critical CSS storage) |

### Volume

| Metric | Value |
|---|---|
| Published pages | **34** (all top-level — no parent/child hierarchy) |
| Published posts (estimate) | **~868** (the `Misc` category alone has 867 entries; second category has 1) |
| Categories | 2 active — `Misc` (867 posts, slug `uncategorized`) and `Oil Spill` (1 post) |
| Tags | Many (see `raw/tags.json`) |

The category situation is striking: 99%+ of posts are uncategorized. That's a content-organization problem worth flagging but not urgent.

### Public users (REST `/users` endpoint)

| ID | Slug | Display name |
|---|---|---|
| 1 | `kk` | Kris Krüg |
| 18 | `wpadmin5102` | Krüg |

> The `wpadmin5102` account looks like a Pagely-generated admin user. Worth confirming it's yours and not a stale shared credential.

### Notable pages

The top 34 pages include:
- **Marketing offers:** `ai-upgrade-for-modern-media-leaders`, `ai-upgrade-for-creative-professionals`, `ai-upgrade-community-coaching-w-kris-krug-peter-bittner`
- **Multilingual intros:** Urdu, Russian, Swahili, Japanese, Hindi, Chinese, Farsi (seven language variants of a welcome page)
- **Standard site pages:** `home`, `about`, `contact`, `blog`, `news`, `events`, `speaking`, `publications`, `testimonials`, `privacy-policy`
- **Services:** `generative-ai-services`, `generative-ai-workshop-for-artists-creatives`, `motleykrug-podcast`, `podcast-guesting-page-epk`
- **Reconciliation:** `reconciliation-indigenous-land-acknowledgement`

Two pages have empty rendered titles (IDs 3930 and 2808 — `empowering-events-organizations-for-the-ai-age` and `subscribe`); worth inspecting.

## Integrations & external services

| Service | How it's wired | Identifier |
|---|---|---|
| Google Analytics 4 | Site Kit | `G-X7JE8B32L7` |
| Google Search verification | meta tag | `b8AYlJgL8znsPoqYbg7SkgQIGXjWVZds_UJHZN_yiAs` |
| Pinterest verification | meta tag (two — duplicate?) | `c09752015a5f4947aa6075b567b0dab3`, `f8bbe5b7c69e3578569bd54295826f17` |
| WordPress.com stats | Jetpack | site ID 159424804 |
| Akismet | API key configured server-side (not visible) | — |

## API namespaces (full list)

From `raw/wp-json-root.json`: `oembed/1.0`, `akismet/v1`, `jetpack/v4`, `jetpack-boost-ds`, `jetpack-boost/v1`, `my-jetpack/v1`, `jetpack/v4/explat`, `wpcom/v2`, `jetpack/v4/stats-app`, `jetpack/v4/import`, `popup-maker/v2`, `popup-maker/v1`, `pum/v1`, `wpcom/v3`, `jetpack/v4/blaze-app`, `jetpack/v4/blaze`, `google-site-kit/v1`, `zbscrm/v1`, `jetpack-protect/v1`, `wp-abilities/v1`, `mcp`, `wp/v2`, `wp-site-health/v1`, `wp-block-editor/v1`.

The `mcp` namespace is the Jetpack-served MCP endpoint — currently locked behind plan.

## Known gaps in this inventory

These cannot be filled in without admin or SSH access:
- Plugin list (only front-end-visible plugins are fingerprinted above)
- Mu-plugins / drop-ins
- `wp-config.php` constants
- Active theme child-theme status and any custom modifications
- Custom user accounts beyond IDs 1 and 18 (REST only exposes authors of public content)
- Cron schedule
- Database size, table prefix, charset
- File modification dates / hand-edited core files
- Media library size (uploads/)
