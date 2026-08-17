# Jetpack inactive diagnosis — #276

**Captured:** 2026-08-16 19:35–19:37 America/Vancouver (`2026-08-17T02:35Z`–`02:37Z`)
**Issue:** [WalksWithASwagger/kriskrug-wp#276](https://github.com/WalksWithASwagger/kriskrug-wp/issues/276)
**Mode:** READ-ONLY public HTML / headers / REST. No plugin deactivate, no delete, no PressCACHE purge, no authenticated writes.
**Live stack at capture:** WordPress 7.0.4, Aurora `style.css` Version **1.6.5**, `Pagely-ARES/1.22.28`.
**Predecessor:** [`jetpack-delete-prep-276-20260726.md`](jetpack-delete-prep-276-20260726.md) (prep packet; this report is a live re-probe, not a replacement of the Pagely delete steps).

Related, not absorbed: [#706](https://github.com/WalksWithASwagger/kriskrug-wp/issues/706) (delay Site Kit gtag / drop Facebook pixel), [#731](https://github.com/WalksWithASwagger/kriskrug-wp/issues/731) (Boost critical CSS regen), [#277](https://github.com/WalksWithASwagger/kriskrug-wp/issues/277) (contact CTA).

---

## 1. Verdict

**Jetpack core is still inactive on the public site. The #276 premise remains true. Do not close the issue as obsolete.**

What the 2026-08-15 audit marked PRESENT (`jb_store_css`, `jp_act_log_event`, Boost cache headers, Photon `i0.wp.com` URLs) is **Jetpack Boost + Jetpack Protect**, not a core reactivation. Those signals are expected while Boost/Protect stay installed, and they are **out of #276 delete scope**.

**Recommended action:** **keep #276 open and wait for KK.** The rollback window since the 2026-07-01 deactivation is elapsed (~46 days). Deletion is still a human-gated wp-admin action: authenticated Plugins-screen confirm that `jetpack/jetpack` is inactive, Pagely backup timestamp, and written KK approval. Do not split Boost vs Jetpack into a new issue; Boost already has #731, Protect stays, Site Kit/gtag/FB pixel stay on #706.

---

## 2. What must be true (falsifiable claims)

| Claim | Source | Result 2026-08-16 |
|---|---|---|
| Jetpack **core** does not fire on public HTML (no stats pixel, no sharing, no forms, no `/plugins/jetpack/` assets, no `generator: Jetpack`) | #276 precondition | **PASS** on 7 routes |
| Jetpack core plugin tree may still sit on disk as rollback insurance | July 1 cleanup + July 26 prep | **PASS** (installed; see disk probe) |
| Jetpack **Boost** remains live (keep) | #276 "delete only core" | **PASS** (headers + HTML + CPT) |
| Jetpack **Protect** remains live (keep) | #276 sibling exclusion | **PASS** (REST namespace + activity-log CPT) |
| Site Kit owns Analytics (`G-X7JE8B32L7`) | #276 precondition; **not #706** | **PASS** (generator `Site Kit by Google 1.185.0`) |
| Core sitemap healthy | #276 precondition | **PASS** (`/sitemap.xml` → `/wp-sitemap.xml`) |
| Contact page has no Jetpack form markup | #276 smoke + #277 | **PASS** (mailto CTA, 0 `<form>` tags) |
| `jb_store_css` / `jp_act_log_event` PRESENT in REST types | 2026-08-15 audit | **PASS as Boost/Protect types**, not core |

---

## 3. Three products, not one "Jetpack"

| Product | Plugin slug | Public evidence 2026-08-16 | #276 action |
|---|---|---|---|
| **Jetpack core** | `jetpack/jetpack` | No frontend remnants. `GET /wp-json/jetpack/v4/settings` → **404 `rest_no_route`**. Core CPTs `jetpack-testimonial` / `feedback` → **404**. Disk tree still present (`jetpack.php` 200/0-byte; `modules/sharedaddy/sharing.js` and `_inc/build/admin.js` publicly fetchable). | **Delete only this**, after KK gate |
| **Jetpack Boost** | `jetpack-boost/jetpack-boost` | `x-jetpack-boost-cache` on HTML; `boost-cache/static/*.min.css\|js`; `<style id="jetpack-boost-critical-css">` on `/` and `/blog/`; `data-jetpack-boost`; Image CDN `i0.wp.com` + `preconnect`; REST type `jb_store_css` described as "Cache entries for the Jetpack Boost plugin." | **Keep** |
| **Jetpack Protect** | `jetpack-protect/jetpack-protect` | Namespace `jetpack-protect/v1`; REST type `jp_act_log_event` ("Activity Log Events"); `jetpack/v4/activity-log` + `jetpack/v4/waf` routes. Listing events is **401**. | **Keep** |
| **Site Kit** | `google-site-kit/google-site-kit` | `<meta name="generator" content="Site Kit by Google 1.185.0">`; `gtag/js?id=G-X7JE8B32L7`. | **Keep.** Delay/diet is **#706**, not this ticket |
| **Facebook pixel** | not Jetpack | `connect.facebook.net/en_US/fbevents.js`, `fbq('init', '1720755522050230')` on every sampled HTML route | **#706.** Do not treat as Jetpack |

`jetpack/v4` and `my-jetpack/v1` remaining in `/wp-json/` do **not** prove core is active. The live route set is Connection / Sync / licensing / JITM / WAF / activity-log (shared packages used by Boost and Protect). Namespaces that **were** present in the May inventory and are **gone now**: `wpcom/v2`, `wpcom/v3`, `jetpack/v4/blaze`, `jetpack/v4/blaze-app`, `jetpack/v4/stats-app`, `jetpack/v4/import`.

---

## 4. Checks selected and results

Unauthenticated `curl` GET only, `User-Agent: Mozilla/5.0 (compatible; kriskrug-wp-verify/276)`. HTML routes also probed with `?cb=<unix>` (cache-bust) and a second warm pass without `cb`.

### 4.1 Public HTML remnant matrix

Seven routes: `/`, `/about/`, `/blog/`, `/work/`, `/contact/`, `/speaking/`, `/2026/07/18/i-am-nomad-ai-film/`. All HTTP **200**.

| Signal | Owner | Observed |
|---|---|---|
| `generator: Jetpack` | core | **ABSENT** (generators are `WordPress 7.0.4` + `Site Kit by Google 1.185.0` only) |
| `/wp-content/plugins/jetpack/` in HTML | core | **ABSENT** (0 asset URLs on all 7 routes) |
| `pixel.wp.com` / `stats.wp.com` / `jp-tracks` | core Stats | **ABSENT** |
| Sharing (`sharedaddy`, `sd-sharing`, `jetpack-sharing`) | core | **ABSENT** |
| Forms (`jetpack-contact-form`, `grunion`, `<form>`) | core | **ABSENT**; `/contact/` has **0** `<form>` tags |
| Instant Search / carousel / related posts / likes / VideoPress | core | **ABSENT** |
| `x-jetpack-boost-cache` | Boost | **Present.** Warm (no `cb`): `/` `hit`, `/about/` `miss`, `/blog/` `miss`, `/work/` `hit`, `/contact/` `hit`. Cache-busted GETs were `miss` as expected |
| `boost-cache/static/*.min.css\|js` | Boost | **Present** (e.g. `/` → `8d99a2084d.min.css`, `a83fd32200.min.js` on `s5102.pcdn.co`) |
| `#jetpack-boost-critical-css` | Boost | **Present** on `/` and `/blog/` only (same pattern as the 1.6.5 stylesheet brief) |
| `data-jetpack-boost` | Boost | **Present** on all 7 routes |
| `i0.wp.com` image URLs | Boost Image CDN (Photon-compatible) | **Present** (home 34, blog 89, post 45). Treat as Boost, not core |
| `gtag` / `G-X7JE8B32L7` / `googletagmanager.com` | Site Kit | **Present** on all 7. **#706**, not #276 |
| `fbevents` / `connect.facebook.net` | Facebook pixel | **Present** on all 7. **#706**, not #276 |

`/contact/` mailto CTA still live: `mailto:feelmoreplants@gmail.com?subject=Inquiry%20from%20kriskrug.co`.

### 4.2 REST types (the 2026-08-15 "PRESENT" pair)

`GET https://kriskrug.co/wp-json/wp/v2/types` → HTTP 200. Keys include `jb_store_css` and `jp_act_log_event`.

| Type | REST | Description / listing | Attribution |
|---|---|---|---|
| `jb_store_css` | `wp/v2/jb_store_css` | "Cache entries for the Jetpack Boost plugin." Public list returns **2** published rows, both dated **2026-07-01** (`core_posts_page` id 12461, `cornerstone_d41d8cd9` id 12460). Stale vs live Aurora 1.6.5; that debt is **#731**, not #276 | **Boost** |
| `jp_act_log_event` | `wp/v2/activity-log-events` | Name "Activity Log Events". Collection **401** `invalid_user_permission_activity_log_event` | **Protect** |
| `jetpack-testimonial` | — | **404** `rest_type_invalid` | Core module **not registered** |
| `feedback` | — | **404** `rest_type_invalid` | Core Forms **not registered** |

### 4.3 REST namespaces vs May inventory

Live `/wp-json/` namespaces at capture: `oembed/1.0`, `akismet/v1`, `code-snippets/v1`, `jetpack/v4`, `jetpack-boost-ds`, `redirection/v1`, `jetpack-boost/v1`, `my-jetpack/v1`, `jetpack/v4/explat`, `wp/v2`, `popup-maker/v2`, `pum/v1`, `google-site-kit/v1`, `zbscrm/v1`, `jetpack-protect/v1`, `wp-abilities/v1`, `mcp`, `wp-site-health/v1`, `wp-block-editor/v1`.

`GET /wp-json/jetpack/v4/settings` → **404** (this was the #233/#249 SEO-title write path; gone while core is inactive). Matches [`SEO-STRIKING-DISTANCE-2026-08-02.md`](../SEO-STRIKING-DISTANCE-2026-08-02.md) (re-verified there 2026-08-03).

### 4.4 On-disk plugin tree (not a substitute for Plugins screen)

| Path | HTTP | Body | Interpretation |
|---|---|---|---|
| `/wp-content/plugins/jetpack/jetpack.php` | 200 | 0 bytes | Pagely empties PHP; **tree still installed** |
| `/wp-content/plugins/jetpack/readme.txt` | 403 | 146 B | Path exists; plaintext blocked |
| `/wp-content/plugins/jetpack/modules/sharedaddy/sharing.js` | 200 | 18,206 B JS | Static asset reachable; **not referenced** in public HTML |
| `/wp-content/plugins/jetpack/_inc/build/admin.js` | 200 | 1,508,397 B JS | Same: on disk, not enqueued publicly |
| `/wp-content/plugins/jetpack-boost/jetpack-boost.php` | 200 | 0 bytes | Boost installed (keep) |
| `/wp-content/plugins/jetpack-protect/jetpack-protect.php` | 200 | 0 bytes | Protect installed (keep) |
| `/wp-content/plugins/google-site-kit/google-site-kit.php` | 200 | 0 bytes | Site Kit installed (keep) |

### 4.5 Sitemap / robots

- `/robots.txt` 200: single `Sitemap: https://kriskrug.co/sitemap.xml`. No Jetpack news/image/video sitemap lines.
- `/sitemap.xml` 200 → `/wp-sitemap.xml` (core index: posts, pages, category, post_tag, users).
- `/llms.txt` 200.

### 4.6 Authenticated plugin list

**BLOCKED.** Process `WP_USER` / `WP_APP_PASSWORD` unset. `varlock run --inject vars` did not resolve those names in this session. `GET /wp-json/wp/v2/plugins` unauthenticated → 401 `rest_cannot_view_plugins`. Last committed authenticated snapshot: 2026-08-03 in `SEO-STRIKING-DISTANCE-2026-08-02.md` (`inactive | Jetpack | jetpack/jetpack`). Public evidence is consistent with that snapshot; KK should still confirm on the Plugins screen before delete.

---

## 5. Commands run (exact)

```
curl -fsS "https://kriskrug.co/wp-content/themes/kk-aurora/style.css"
curl -sS -D - "https://kriskrug.co{/,/about/,/blog/,/work/,/contact/,/speaking/,/2026/07/18/i-am-nomad-ai-film/}"
curl -sS "https://kriskrug.co/wp-json/"
curl -sS "https://kriskrug.co/wp-json/wp/v2/types"
curl -sS "https://kriskrug.co/wp-json/wp/v2/types/{jb_store_css,jp_act_log_event,jetpack-testimonial,feedback}"
curl -sS "https://kriskrug.co/wp-json/wp/v2/jb_store_css?per_page=100"
curl -sS "https://kriskrug.co/wp-json/wp/v2/activity-log-events"
curl -sS "https://kriskrug.co/wp-json/jetpack/v4/settings"
curl -sS -w '%{http_code} %{size_download}' \
  "https://kriskrug.co/wp-content/plugins/jetpack/{jetpack.php,readme.txt,modules/sharedaddy/sharing.js,_inc/build/admin.js}"
curl -sS -L "https://kriskrug.co/sitemap.xml"
curl -sS "https://kriskrug.co/robots.txt"
```

HTML was grepped for the remnant needles in section 4.1. No wp-admin. No plugin mutate.

---

## 6. Why not close, split, or delete from this session

| Option | Decision | Why |
|---|---|---|
| Close #276 as obsolete | **No** | Core is still installed on disk. Acceptance criteria ("Jetpack core is deleted") are unmet. Premise "inactive" is still accurate, not disproven. |
| Keep and wait | **Yes** | Window elapsed; remaining gates are KK (Plugins confirm + backup + approval). #277 still open as a soft forms-decision gate. |
| Split Boost vs Jetpack | **No new issue** | The 08-15 PRESENT types are already owned: Boost → #731 (critical CSS dated 2026-07-01, live theme is 1.6.5), Protect stays, core delete stays #276. Splitting would duplicate #731. |
| Absorb #706 | **No** | gtag + Facebook pixel are Site Kit / marketing tags. They fire on every sampled page and are independent of whether `jetpack/jetpack` exists. |
| Delete now from this agent | **No** | Explicitly out of scope. No live writes. |

Rollback-window stamp: deactivated ~2026-07-01 (`post-jetpack-cleanup-20260701T194455Z.md`); this probe is **2026-08-16** (~46 days). #276 never named a day count; 14- and 30-day ops norms are both exceeded.

---

## 7. Remaining risks

- Authenticated Plugins-screen confirm is still required. Public REST cannot list `status=inactive`.
- Operator error: deleting Boost or Protect because REST still says "jetpack". The delete target remains **`jetpack/jetpack` only**.
- Image CDN: `i0.wp.com` will keep working only while Boost Image CDN stays on. That is not a reason to keep core.
- #277 still open: if KK later wants Jetpack Forms, reinstall is the rollback path (already written in the July 26 prep packet). Mailto CTA is stable today.
- Boost critical CSS rows are frozen at 2026-07-01. Regenerating them is **#731**, after the 1.6.6 deploy window, not part of core delete.

---

## 8. Next verification step (human, not this PR)

1. wp-admin → Plugins: confirm row **Jetpack** is **Inactive**, slug `jetpack/jetpack`.
2. Record a fresh Pagely Atomic backup timestamp.
3. Comment on #276 with that confirm + "delete Jetpack core now".
4. Follow [`jetpack-delete-prep-276-20260726.md`](jetpack-delete-prep-276-20260726.md) Pagely steps. Re-smoke the remnant matrix after delete.
5. Leave Boost, Protect, Site Kit, Akismet, Redirection, Code Snippets, WPCode/IHAF, CRM untouched.

---

## Sources

- Issue #276 body (goal, preconditions, "delete only Jetpack core").
- Public GET probes 2026-08-16 against `https://kriskrug.co` as tabulated above.
- [`jetpack-delete-prep-276-20260726.md`](jetpack-delete-prep-276-20260726.md)
- [`post-jetpack-cleanup-20260701T194455Z.md`](post-jetpack-cleanup-20260701T194455Z.md)
- [`SEO-STRIKING-DISTANCE-2026-08-02.md`](../SEO-STRIKING-DISTANCE-2026-08-02.md) (2026-08-03 authenticated inactive row)
- [`morning-truth-20260816-050712Z.md`](morning-truth-20260816-050712Z.md) (namespaces + `x-jetpack-boost-cache`)
