# Jetpack Boost critical CSS — #731 status 2026-08-17

**Status:** still owed. App password cannot regenerate. Site is on **local/free** Critical CSS, not cloud. wp-admin session is required.
**Live theme:** Aurora **1.6.8** (public `style.css`). Issue text still says 1.6.5; regenerate against **1.6.8**.

## Why this session could not click Regenerate

| Probe | Result |
|---|---|
| `WP_AUTH_MODE=login` | RuntimeError: login did not produce an admin session (application password is not a wp-admin password) |
| `GET /wp-json/jetpack-boost-ds/critical-css-state` | **403** `rest_forbidden` |
| `GET .../critical-css-suggest-regenerate` | **403** |
| `POST .../critical-css-state/action/request-regenerate` | not attempted after GET 403 |
| `GET /wp-json/jetpack-boost/v1/cloud-css/request-generate` | **404** (no cloud-css routes; manual Boost) |
| `GET /wp-json/jetpack-boost/v1/list-source-providers` | **403** |
| `GET /wp-json/jetpack-boost/v1/connection` | 200, `connected: true` |
| One-shot mu-plugin `Modules_Setup::get_status()` | `critical_css: "1"`; **no `cloud_css`**. Cloud `regenerate_cloud_css()` skipped. Storage not cleared. Self-deleted. Report `wp-content/upgrade/kk-731-boost-regen.json` |

Do not POST `set-provider-css` with hand-written CSS. That is not a regen. Do not call `Regenerate::start()` on local mode from PHP: it would wipe `jb_store_css` and wait for the admin-page browser generator that we cannot run.

## Before-sample (canonical `/` and `/blog/`, 2026-08-17 05:47 UTC)

Private full dump: `~/kk-snapshots/boost-critical-home-before-731-20260817T054734Z.css` (mode 0600). `jb_store_css` edit snapshot: `~/kk-snapshots/jb_store_css-before-731-20260817T054800Z.json` (ids 12460 cornerstone, 12461 core_posts_page, both **modified 2026-07-01**).

| Signal | `/` | `/blog/` |
|---|---|---|
| `<style id="jetpack-boost-critical-css">` | present, 7474 bytes | present, 15332 bytes |
| `--aurora-black:#030405` | **1** | **1** |
| `--aurora-ink:#f7f7f2` | **1** | **1** |
| `--revive-surface` | 0 | — |
| `aurora-creative-labs` / `aurora-logo-soup` | **0** (1.6.8 bands not in snapshot) | n/a |
| Boost CSS bundle hash | `0f9e6b2840` | — |

The 1.6.8 homepage HTML is live; the inlined critical snapshot is still the pre-cream / pre-labs first paint. After the full sheet loads, cream `!important` wins. That is the #731 FOUC, not a theme-file miss.

## What KK does in wp-admin

1. Jetpack → Boost (`admin.php?page=jetpack-boost`).
2. Optimize Critical CSS Loading → **Regenerate**. Stay on the page. Prior hangs are documented in `PERFORMANCE-RECOVERY-2026-07-01.md`.
3. If it hangs, leave #731 open and paste the UI state.

After success, a public grep should show `--aurora-black:#030405` **0** on `/` and `/blog/`, and homepage critical CSS should mention the 1.6.8 bands or at least drop the dark tokens. Record the new inline length + a short before/after excerpt in this reports folder. Homepage CLS spot-check vs `psi-mobile-2026-08-10.md` (CLS 0.43). Keep the #701 geometry guard.

## Out of scope here

PSI mobile API returned **429** without a key (`quota_limit_value: 0`). #706 browser Network checks are in `issue-706-script-diet-apply-20260817.md`.
