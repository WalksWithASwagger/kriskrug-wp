# Jetpack delete prep checklist — #276

**Captured:** `2026-07-26` (public probe only; America/Vancouver day)  
**Issue:** [WalksWithASwagger/kriskrug-wp#276](https://github.com/WalksWithASwagger/kriskrug-wp/issues/276)  
**Lane:** Track A / platform ops (docs only — **no live WP admin actions**)  
**Mode:** PREP CHECKLIST ONLY — do **not** deactivate or delete plugins in this pass  
**Related:** [#125](https://github.com/WalksWithASwagger/kriskrug-wp/issues/125) (post-Jetpack perf + Boost), [#222](https://github.com/WalksWithASwagger/kriskrug-wp/issues/222) (platform trust epic), [#277](https://github.com/WalksWithASwagger/kriskrug-wp/issues/277) (contact CTA decision), PR [#273](https://github.com/WalksWithASwagger/kriskrug-wp/pull/273) (content-architecture / post-Jetpack evidence closeout; issue bodies that say “Related: #273” mean this PR)

## Verdict

Public HTML shows **no Jetpack core frontend remnants** (no stats pixel, no Jetpack Forms, no `/wp-content/plugins/jetpack/` asset paths). **Jetpack Boost** remains clearly live (boost-cache CSS/JS + `x-jetpack-boost-cache` headers + Image CDN via `i0.wp.com`). **Site Kit** owns Analytics (`G-X7JE8B32L7`) and emits `generator: Site Kit by Google 1.183.0`. WordPress **core sitemap** is healthy (`/sitemap.xml` → `/wp-sitemap.xml`).

**Do not delete yet from this agent session.** Deletion still needs: authenticated confirm that `jetpack/jetpack` is inactive, KK approval, a fresh plugin/page snapshot, and Pagely-aware delete steps below. This document is the prep packet for that human-gated pass.

---

## Rollback window assumptions

| Assumption | Value / basis | Status for #276 |
|---|---|---|
| Jetpack core deactivated | ~`2026-07-01` (isolation + jetpack-off + post-cleanup reports same day) | Anchor date |
| “Installed inactive” purpose | Rollback insurance only (reactivate if a missing feature is required) | Per `post-jetpack-cleanup-20260701T194455Z.md` |
| Elapsed stability (to probe day) | **~25 days** (`2026-07-01` → `2026-07-26`) | Window likely satisfied for a 14–30 day ops norm |
| Explicit window length in #276 | Not stated in issue body | **KK must stamp** preferred window (recommend: ≥14 days already met; optional hold to 30 days = ~2026-07-31) |
| Local rollback artifacts | Laptop/gitignored dirs from PR #273 notes: `backup/20260701T192429Z-jetpack-off/`, `backup/20260701T194455Z-post-jetpack-cleanup/` | Confirm still reachable before delete |
| Pagely backup insurance | Atomic daily S3 backups historically ~14-day retention (see `WP-7-UPGRADE-2026-05-22.md`) | Record a **fresh** Atomic backup timestamp before delete; do not rely on July 1 local folders alone |
| Contact / forms decision | #277 still open; public mailto CTA stable | Prefer #277 decision stamp (or explicit “delete Jetpack anyway”) before permanent delete |
| Speed audit gate | #125 still open for Boost Critical CSS / repeated samples | Core delete is **orthogonal** to Boost; do not block solely on #125 if cold TTFB gain already held since 2026-07-01 |

**Assumption stamp for KK:** treat the rollback window as **closed for core reactivation insurance** once (a) ≥14 days inactive without public breakage, (b) contact CTA acceptable, (c) Site Kit + core sitemap healthy, (d) KK approves permanent deletion. Items (a)–(c) look green from public evidence; (d) is human-only.

---

## Public remnant probe (2026-07-26)

**Base:** `https://kriskrug.co`  
**Live Aurora `style.css` Version:** `1.4.8`  
**Method:** unauthenticated HTTP GET only (no wp-admin, no plugin mutate)

### Remnant matrix

| Signal | Expect if Jetpack core gone from frontend | Observed |
|---|---|---|
| Stats pixel (`pixel.wp.com` / `stats.wp.com` / `b.gif`) | Absent | **Absent** on `/`, `/about/`, `/blog/`, `/work/`, `/contact/` |
| Jetpack Forms (`jetpack-contact-form`, `grunion`, `wp-block-jetpack-contact-form`) | Absent | **Absent**; `/contact/` has **0** `<form>` tags |
| Jetpack core plugin assets (`/wp-content/plugins/jetpack/…`) | Absent in HTML | **Absent** (no `jp_paths` in HTML) |
| Jetpack Boost CSS/JS (`boost-cache/static/*.css|js`, critical-css markers) | Present (keep Boost) | **Present** on sampled HTML routes |
| `x-jetpack-boost-cache` response header | Present on HTML | **hit** on `/`, `/about/`, `/blog/`, `/work/`, `/contact/` |
| Image CDN `i0.wp.com` | May remain via **Boost** Image CDN | **Present** (dns-prefetch + `<img>`/`og:image`) — treat as Boost, **not** core remnant |
| Site Kit / GA4 | Present | **Present** (`G-X7JE8B32L7`, gtag, `google-site-verification`, Site Kit generator) |
| Core sitemap | Healthy | `/sitemap.xml` → `200` `/wp-sitemap.xml` (posts/pages/tax/users index) |
| `robots.txt` Jetpack sitemap clutter | Clean | Single `Sitemap: https://kriskrug.co/sitemap.xml` (news/image Jetpack-era lines from July 1 cleanup remain gone) |

### Route smoke (public)

| Route | HTTP | Notes |
|---|---|---|
| `/` | 200 | Boost HIT; gateway HIT; Site Kit + GA4; no stats/forms |
| `/about/` | 200 | same pattern |
| `/blog/` | 200 | same pattern; heavier Photon img count via Boost CDN |
| `/work/` | 200 | same pattern |
| `/contact/` | 200 | mailto CTA present (`feelmoreplants@gmail.com`); no form markup |
| `/robots.txt` | 200 | gateway BYPASS; curated robots; one sitemap line |
| `/llms.txt` | 200 | present |
| `/sitemap.xml` | 200 | redirects to `/wp-sitemap.xml` |
| `/wp-sitemap.xml` | 200 | WP core sitemap index |

Warm TTFB on this probe was sub-100ms gateway HIT (not a cold audit). Historical cold win after Jetpack-off: homepage cold p50 ~3.7s → ~0.6s (`jetpack-off-performance-20260701T192807Z.md`).

### On-disk / REST signals (not a substitute for Plugins screen)

| Check | Result | Interpretation |
|---|---|---|
| `GET /wp-content/plugins/jetpack/jetpack.php` | HTTP **200**, **0-byte** body | Plugin tree almost certainly **still installed** on disk (Pagely often empties PHP responses) |
| `GET …/jetpack/readme.txt` | HTTP **403** | Path exists; listing/plaintext blocked |
| `GET …/jetpack-boost/jetpack-boost.php` | HTTP 200, 0-byte | Boost installed (expected — **keep**) |
| `GET …/jetpack-protect/jetpack-protect.php` | HTTP 200, 0-byte | Protect installed (expected — **keep**) |
| `wp-json` namespaces | `jetpack/v4`, `my-jetpack/v1`, `jetpack-boost/*`, `jetpack-protect/v1`, `zbscrm/v1`, `google-site-kit/v1` | Family packages / siblings may register routes even when core is inactive; **does not prove core is active**. Confirm inactive in wp-admin before delete. |

### `/contact/` detail

- Mailto CTAs present (primary subject `Inquiry from kriskrug.co`).
- No Jetpack / CF7 / WPForms / Gravity markers in public HTML (aligned with #277 decision memo probe same day).
- Cache: Pagely gateway + Jetpack Boost both participating on HTML.

---

## Pre-delete verification matrix (KK / authenticated pass)

Complete **before** clicking Delete. Snapshot-first; dry-run mental model; one plugin only.

| # | Check | How | Pass criteria | Owner |
|---|---|---|---|---|
| 1 | Snapshot active plugins | wp-admin → Plugins, or authenticated REST; save list + timestamp | Written snapshot exists | KK / ops |
| 2 | Snapshot inactive plugins | Same | `jetpack/jetpack` listed inactive | KK / ops |
| 3 | Confirm target slug | Plugins screen row for **Jetpack** (not Boost / Protect / CRM) | Exact target `jetpack/jetpack` | KK |
| 4 | Confirm siblings stay | Boost, Protect, CRM (Zero BS), Site Kit, Akismet, Redirection, Code Snippets, WPCode/IHAF | All remain installed; active set unchanged except Jetpack row gone after delete | KK |
| 5 | Contact page body snapshot | Copy `/contact/` content or REST `pages?slug=contact` | Snapshot stored; mailto CTA intact | KK / ops |
| 6 | Site Kit status | Site Kit settings: Analytics + Search Console connected | GA4 + GSC still connected | KK |
| 7 | `robots.txt` | Public GET | Still one core sitemap line; no Jetpack sitemap spam | Ops |
| 8 | Sitemap | `/sitemap.xml` + `/wp-sitemap.xml` | 200 XML index | Ops |
| 9 | Public remnant re-probe | Same matrix as above after delete | Still no stats/forms; Boost headers still present | Ops |
| 10 | Image CDN spot-check | Homepage + blog hero/images still load via `i0.wp.com` **or** origin if CDN toggled | No mass broken images | Ops |
| 11 | OG/social spot-check | View-source `/`, one post | `og:description` / `twitter:description` still present (Aurora/Site Kit path — not Jetpack) | Ops |
| 12 | #277 / contact friction | KK checklist on #277 | Explicit OK to proceed without form plugin | KK |
| 13 | Pagely backup | Atomic backup list | Fresh backup timestamp recorded; restore path known | KK |
| 14 | KK approval | Comment on #276 | Written “delete Jetpack core now” | KK |

**Delete scope (from #276):** delete **only** Jetpack core (`jetpack/jetpack`).  
**Do not delete:** Jetpack Boost, Jetpack Protect, Jetpack CRM / Zero BS CRM, Site Kit, Akismet, Redirection, Code Snippets, WPCode / Insert Headers and Footers, or any other active plugin.

---

## Pagely steps for KK (human-gated delete)

Pagely host notes from prior ops: SFTP/SSH often blocked; prefer **wp-admin Plugins UI** for plugin delete; use Atomic for backup/restore; purge PressCACHE after material changes. Staging self-serve may be unavailable on this plan (`WP-7-UPGRADE-2026-05-22.md`).

### Before

1. Sign in to **Pagely Atomic** for `kriskrug.co`.
2. Confirm a **recent successful backup** (record UTC timestamp). If the newest backup is stale relative to today’s content edits, wait for the next daily backup or request one per Pagely’s backup UX — do not delete without a restore path.
3. Optional but recommended: export / screenshot **Plugins → Installed** (Active + Inactive).
4. Optional: copy `/contact/` HTML or REST JSON into the same day’s backup notes folder (local/gitignored), not necessarily into git.
5. Comment on #276 with: backup timestamp, inactive confirmation for `jetpack/jetpack`, and explicit approval.

### Delete (wp-admin)

1. **Plugins → Installed Plugins**.
2. Find **Jetpack** (core). Confirm status **Inactive**.
3. Confirm you are **not** on Jetpack Boost / Protect / CRM.
4. Use **Delete** on Jetpack core only. Confirm the prompt.
5. Do **not** bulk-select other Jetpack-branded plugins.

### After

1. **Pagely / PressCACHE:** purge page cache (and wait 2–5 minutes if Boost still serves a stale HTML shell — known caveat from `HANDOFF-2026-06-17.md`).
2. Smoke: `/`, `/about/`, `/blog/`, `/work/`, `/contact/`, `/robots.txt`, `/llms.txt`, `/sitemap.xml`.
3. Re-check remnant matrix (stats pixel, forms, Boost still alive, images OK).
4. Record outcome on #276 (PASS/FAIL + any surprise).
5. Close #276 only when acceptance criteria in the issue are met.

### If something breaks

1. **Do not** reinstall random Jetpack modules “to see.”
2. Reinstall **Jetpack core** from wordpress.org / Plugins → Add New (same major family as before if possible), leave **inactive** unless a specific feature is required, then activate only that need.
3. If `/contact/` regresses, restore the contact page snapshot from the jetpack-off backup era and purge caches.
4. If images break, check **Jetpack Boost → Image CDN** first (not core); Photon `i0.wp.com` is Boost-owned in the current public HTML.
5. Pagely Atomic restore only if delete cascades beyond the plugin directory (unexpected) — treat as last resort; record restore intent first.

---

## What breaks if deleted too early

| Risk | Why it matters | Early-delete failure mode | Mitigation if already deleted |
|---|---|---|---|
| Need Jetpack Forms again | #277 not decided; mailto friction unknown | No one-click “reactivate forms + prior submissions UI”; historical form inbox debt returns only after reinstall + rebuild | Reinstall Jetpack; rebuild form deliberately; prefer new form issue over nostalgia |
| Need Jetpack Stats / WP.com traffic | Site Kit replaces analytics — but WP.com-only reports / old dashboards disappear with core | Cannot open legacy Jetpack Stats without reinstall + reconnect | Use Site Kit / GA4; reinstall only if a WP.com metric is mandatory |
| Need Jetpack Social / Publicize / Related Posts / Likes / Subscriptions | Intentionally not replaced in July cleanup | Feature gap only if product later wants them | Reinstall + enable specific modules, or implement lighter Aurora/static equivalents |
| Need Jetpack SEO title meta as live owner | Aurora now owns titles/descriptions on live `1.4.8`; stored `jetpack_seo_*` meta may still exist in DB | Unlikely public break if Aurora/Site Kit path healthy; early delete mainly removes easy Jetpack SEO admin UI | Aurora/Site Kit already public path; reinstall only for admin convenience |
| Image CDN confusion | `i0.wp.com` looks “Jetpack-y” but is served with Boost active | Operator deletes Boost by mistake while “removing Jetpack” | Delete **core only**; verify Boost still active after |
| Connection / My Jetpack leftovers | Sibling plugins share Jetpack Connection packages; `jetpack/v4` may remain in `wp-json` | Panic that “Jetpack is still there” → over-deletion of Boost/Protect | Expect some namespaces to remain; judge by Plugins screen + public HTML |
| Lost rollback insurance inside stability window | Reactivating inactive core is faster than reinstall + reconnect | If a latent dependency appears on day 3–10, recovery is slower | Keep inactive through KK’s stamped window; use Pagely backup |
| Cache inconsistency after delete | PressCACHE success ≠ Boost HTML/CSS immediately fresh | Stale pages look “broken” briefly | Purge PressCACHE; wait; avoid Critical CSS regen unless #125 requires it |
| CRM / Protect / Akismet collateral | Mis-click on Jetpack-branded rows | Security/spam/CRM outage unrelated to core TTFB win | Stick to single-plugin delete checklist |

**Bottom line:** deleting too early does **not** automatically undo the TTFB win (that win came from deactivation). The real early-delete costs are **slower rollback**, **form/social feature reinstall work**, and **operator error against Boost/Protect**. Public evidence today does not show a core frontend dependency.

---

## Rollback note (for post-delete #276 acceptance)

> Reinstall and/or reactivate **Jetpack core** (`jetpack/jetpack`) **only** if a specific missing feature is required (forms, WP.com stats, Social/Publicize, etc.). Do **not** reactivate “for speed.” Keep Jetpack Boost, Protect, Site Kit, Akismet, Redirection, and Code Snippets as the performance/security/analytics baseline. After any reinstall, purge PressCACHE and re-smoke the public remnant matrix.

---

## Explicitly not done in this pass

- No plugin deactivate/delete.
- No PressCACHE purge.
- No wp-admin or authenticated REST plugin inventory (secrets not assumed).
- No #276 close; no live comments required for prep commit.
- No changes to Boost Critical CSS (#125) or contact CTA decision (#277).

---

## Sources

- Issue #276 body (goal, preconditions, tasks, acceptance).
- `docs/current-state/reports/cold-ttfb-isolation-20260701T190629Z.md`
- `docs/current-state/reports/jetpack-off-performance-20260701T192807Z.md`
- `docs/current-state/reports/post-jetpack-cleanup-20260701T194455Z.md`
- `docs/current-state/HANDOFF-2026-06-17.md` (Boost/PressCACHE caveats)
- `docs/current-state/WP-7-UPGRADE-2026-05-22.md` (Pagely Atomic / backup norms)
- Sibling probe: `contact-cta-decision-277-20260726.md` on branch `cursor/277-contact-cta-decision-f196` (mailto / no-form confirmation)
- Public GET probes `2026-07-26` against `https://kriskrug.co` as tabulated above
