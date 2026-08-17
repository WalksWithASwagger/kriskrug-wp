# Third-party script diet — apply runbook (#706)

**Applied 2026-08-17T05:26Z.** Pixel: WPCode CPT `7917` (`META PIXEL`) set to draft + `wpcode_snippets` cache rebuilt. Gtag delay: Code Snippets **id 22** `KK Script Diet`, front-end, active. Canonical HTML after no-op title-saves (pages 3930 `/`, 1208 `/about/`, 1887 `/speaking/`, 12013 `/photography/`, 2418 `/contact/`, 2672 `/work/`): `fbevents` 0, `google_gtagjs-js` 0, `kk-gtag-delayed` 1. Snapshots in `~/kk-snapshots/` (mode 0600), not the repo. Rollback: reactivate WPCode 7917; POST `{"active":false}` to snippet 22. PSI mobile rerun still owed (≥30 min after purge).

KK ruling on #706 (2026-08-10): **drop the Facebook pixel entirely; delay gtag** to first interaction or 3 s idle.

Artifact: [`issue-706-script-diet-snippet.php`](issue-706-script-diet-snippet.php) — the gtag half. The pixel half is a source-level removal in **WPCode Lite**, not Code Snippets.

---

## Still live as of 2026-08-16

Logged-out `curl` of `https://kriskrug.co/` (HTTP 200) and `https://kriskrug.co/about/` (HTTP 200). Counts are whole-document (Jetpack Boost relocates the `<script>` tags into `<body>`).

| Marker | Home | About | Meaning |
|---|---|---|---|
| `fbevents` | 1 | 1 | Facebook pixel loader still present |
| `fbq(` | 2 | 2 | `init` + `PageView` still fire |
| `Meta Pixel` | 2 | 2 | Meta's start/end comment wrapper still in `<head>` |
| Pixel ID `1720755522050230` | present | present | Unchanged |
| `google_gtagjs` | 3 | 3 | Site Kit handle (`-js`, `-js-after`, sourceURL) still eager |
| `G-X7JE8B32L7` | 2 | 2 | Same GA4 property |
| `kk-gtag-delayed` | 0 | 0 | Prepared delay snippet is **not** live |
| `<meta name="generator" content="Site Kit by Google 1.185.0" />` | present | present | Same injector as 2026-08-15 |

Authenticated Code Snippets list (`GET /wp-json/code-snippets/v1/snippets`, Varlock-injected app password, HTTP 200): **21 snippets, none contain `fbq` / `fbevents` / `Meta Pixel` / `1720755522050230`.** There is no Code Snippets pixel ID. Do not invent one.

WPCode Lite (`insert-headers-and-footers/ihaf` **2.3.8**) is active. Its Header & Footer boxes and snippet bodies are **not** on REST (probed `wpcode/v1` and `wp/v2` types: no route). WPCode snippet ID is **unknown**. Do not invent one.

This lane did not edit live snippets, WPCode, cache, or GA4.

---

## KK one-sitting checklist

Do the pixel first. Snapshot before every write. Do not delete anything.

1. Copy the WPCode Header & Footer boxes (and any matching WPCode snippet) to `~/kk-snapshots/` before editing.
2. Snapshot Code Snippets via the REST command in step 0 (restore source for the gtag half).
3. In **WPCode** (not the Code Snippets plugin), find `1720755522050230` / `<!-- Meta Pixel Code -->`. If the box/snippet is pixel-only, deactivate or clear it. If mixed, delete only the Meta Pixel wrapper. If neither WPCode surface has it, **stop**.
4. Purge Pagely PressCACHE. Logged-out grep: `fbevents` / `fbq(` / `facebook.com/tr` expect 0 on `/` and `/about/`. Use `?cb=$RANDOM` if the canonical URL is still a HIT.
5. In the **Code Snippets** plugin, add `KK Script Diet` from [`issue-706-script-diet-snippet.php`](issue-706-script-diet-snippet.php), strip `<?php`, scope front-end, activate. Record the new ID here after install.
6. Purge PressCACHE again. Logged-out grep: `google_gtagjs-js` expect 0, `kk-gtag-delayed` expect 1. Then the browser/GA4 checks in step 3.
7. Rerun PSI mobile. **TBT / third-party / long tasks should move. LCP and CLS will not.** Do not credit this change if LCP/CLS shifts.

Rollback is a toggle on each surface, not a backup restore. Code Snippets safe mode undoes only the gtag delay; it does **not** put the pixel back.

---

## What injects each script today

Verified 2026-08-15 by reading the public homepage (`curl https://kriskrug.co/`, logged out) and grepping the repo. Both findings were re-confirmed against live HTML, not assumed from the PSI report.

### gtag → Site Kit by Google 1.185.0

- `<meta name="generator" content="Site Kit by Google 1.185.0" />` in `<head>`.
- `<!-- Google tag (gtag.js) snippet added by Site Kit -->` and `<!-- Google Analytics snippet added by Site Kit -->` immediately after the core block-supports style block.
- The tag itself: `<script id="google_gtagjs-js" src="https://www.googletagmanager.com/gtag/js?id=G-X7JE8B32L7" async>` followed by `<script id="google_gtagjs-js-after">`. The `-js` / `-js-after` id pair is WordPress printing an enqueued handle named `google_gtagjs` plus a `wp_add_inline_script(…, 'after')` payload. The payload contains `gtag("set", "developer_id.dZTNiMT", true)` — `dZTNiMT` is Site Kit's own developer ID, so this is Site Kit's tag, not a hand-pasted GA snippet.
- `google-site-kit/v1` is present in the public `https://kriskrug.co/wp-json/` namespace list.
- Not in the repo: no `gtag`/`googletagmanager` reference anywhere under `theme/`, `inc/`, `plugins/`, or `fixes/`.

**Consequence:** the injection point is a WordPress enqueue, so it can be intercepted in PHP without touching a single Site Kit setting. That is what the snippet does, and it is why rollback is one toggle.

### Facebook pixel → hand-installed markup in `wp_head`, not a plugin and not the theme

- `<!-- Meta Pixel Code -->` … `<!-- End Meta Pixel Code -->` — Meta's own canonical comment wrapper, i.e. someone pasted the block Meta hands you in Events Manager.
- Pixel ID `1720755522050230`. Base code is the standard `!function(f,b,e,v,n,t,s)` loader for `https://connect.facebook.net/en_US/fbevents.js`, then `fbq('init', '1720755522050230'); fbq('track', 'PageView');`.
- It prints inside `wp_head`, bracketed between Site Kit's AdSense platform meta and Site Kit's `google-site-verification` meta (Site Kit prints that one at `wp_head` priority 99), so the pixel's hook priority sits below 99.
- **Not the theme:** `grep -rn "fbq\|fbevents\|Meta Pixel" theme/ inc/ plugins/ fixes/` returns nothing.
- **Not a dedicated pixel plugin:** no pixel-related namespace in the public REST namespace list. What is there: `code-snippets/v1`, `google-site-kit/v1`, `jetpack/v4`, `jetpack-boost/v1`, `popup-maker/v2`, `redirection/v1`, `akismet/v1`, `zbscrm/v1`.
- Repo corroboration: `content/drafts/alt-text-backfill-2026-08-02/inventory.csv` already logged this pixel's `<noscript>` image site-wide with source `tracking-pixel-snippet`.

**Conclusion as of 2026-08-15:** hand-installed PHP/HTML on a `wp_head` hook, not the theme and not a dedicated pixel plugin.

**Closed 2026-08-16:** it is **not** a Code Snippets plugin snippet. The authenticated list (21 bodies) has no pixel. Do not look for a Code Snippets ID, and do not invent one.

**Remaining surface:** WPCode Lite 2.3.8 (`insert-headers-and-footers/ihaf`), whose bodies are not REST-enumerable. That is the wp-admin place to look (Header & Footer first, then WPCode's own snippet list). WPCode snippet ID is unknown; do not invent one. If both WPCode surfaces miss, stop and report — do not deactivate unrelated Code Snippets.

### One mechanism detail that matters for verification

Both scripts are injected into `<head>` but *render* near the end of `<body>`. Jetpack Boost's defer-JS pass relocates them. The head-side evidence of this is visible: the `<!-- Meta Pixel Code -->` wrapper in `<head>` is empty except for the `<noscript>` fallback, because the `<script>` inside it was moved out.

So: when you verify, grep the **whole document**, not the `<head>`. And note the snippet intervenes at enqueue time, before Boost ever sees the tag, so Boost's relocation is irrelevant to whether it works.

---

## Apply order

Do the pixel first. It is the bigger, more certain win and it is pure subtraction — if PSI moves as expected, that isolates the gtag change cleanly.

### 0. Snapshot before touching anything

```bash
# Rendered HTML, logged out — the before-picture for every grep below
curl -s https://kriskrug.co/ > /tmp/kk-706-home-before.html
grep -c "fbevents" /tmp/kk-706-home-before.html          # expect 1
grep -c "google_gtagjs-js" /tmp/kk-706-home-before.html  # expect 3 as of 2026-08-16 (tag + -after + sourceURL)
```

Also copy WPCode Header & Footer (and any matching WPCode snippet) to `~/kk-snapshots/` **before** step 1. That plugin has no REST dump; the Code Snippets JSON below does not restore the pixel.

```bash
# Full Code Snippets snapshot — gtag-half restore source only (pixel is not in this list).
# Write it OUTSIDE the repo: it is a code dump, do not commit it.
varlock run --inject vars -- sh -eu -c '
  umask 077
  snapshot_dir="${HOME}/kk-snapshots"
  snapshot_path="${snapshot_dir}/code-snippets-before-706-$(date -u +%Y%m%dT%H%M%SZ).json"
  tmp_path="${snapshot_path}.tmp"
  mkdir -p "$snapshot_dir"
  chmod 700 "$snapshot_dir"
  trap "rm -f -- \"${tmp_path}\"" EXIT HUP INT TERM
  curl --fail-with-body --silent --show-error \
    --user "${WP_USER:?}:${WP_APP_PASSWORD:?}" \
    https://kriskrug.co/wp-json/code-snippets/v1/snippets > "$tmp_path"
  jq -e "type == \"array\"" "$tmp_path" >/dev/null
  chmod 600 "$tmp_path"
  ln "$tmp_path" "$snapshot_path"
  rm "$tmp_path"
  trap - EXIT HUP INT TERM
  printf "Snapshot: %s\\n" "$snapshot_path"
'
```

The command fails on HTTP errors, accepts only a valid JSON array, and publishes
the final path only with a same-directory hard link that refuses to overwrite
an existing snapshot. The directory is
mode 0700 and the snapshot is mode 0600. A failed fetch or validation removes
the temporary file, so a truncated response cannot be mistaken for rollback
evidence.

PSI baseline already exists and is committed: `docs/current-state/reports/psi-mobile-2026-08-10.md`. Do not re-baseline — the whole point is comparing to it.

### 1. Locate the pixel in WPCode (wp-admin)

The Code Snippets plugin list was already read on 2026-08-16. Skip searching it for the pixel. Two different left-nav items exist; use the right one:

| Plugin | Left nav | Pixel? | Gtag delay? |
|---|---|---|---|
| **WPCode Lite** (Insert Headers and Footers) | **WPCode** | Yes — look here | No |
| **Code Snippets** (Shea Bunge) | **Snippets** | No — 21 bodies checked | Yes — install `KK Script Diet` here |

Exact clicks:

1. wp-admin → **WPCode → Header & Footer** (`admin.php?page=wpcode-headers-footers`). If that submenu is missing, try the legacy Insert Headers and Footers screen (`admin.php?page=ihaf`).
2. Search the Header (then Body, then Footer) box for `1720755522050230` or `<!-- Meta Pixel Code -->`.
3. If the boxes are empty of pixel markup: **WPCode → Code Snippets** (`admin.php?page=wpcode`) → search the same strings.
4. **Before editing, snapshot.** Copy the entire box or snippet body to `~/kk-snapshots/wpcode-pixel-before-706-$(date -u +%Y%m%dT%H%M%SZ).txt` (mode 0600). This is the restore source. WPCode has no REST dump.
5. Read the whole box/snippet. If it only prints the Meta Pixel block, deactivate the WPCode snippet (or clear that box). If it also carries unrelated head markup — a verification meta, a Pinterest tag, anything — delete only the `<!-- Meta Pixel Code -->` … `<!-- End Meta Pixel Code -->` wrapper and leave the rest. The Pinterest `p:domain_verify` meta and Site Kit's `google-site-verification` print as *separate* `wp_head` callbacks today; do not assume they share this box, and do not remove them "while you're there."

If neither WPCode surface matches, **stop and report**. Do not POST `active: false` at a Code Snippets ID. There isn't one.

### 2. Remove the pixel, then purge

In WPCode: **Save** the Header & Footer change, or toggle the matching WPCode snippet **inactive**. Do not delete the WPCode snippet until after a soak, and only if KK wants it gone permanently.

Then purge the WordPress page cache:

1. wp-admin → **Pagely® → PressCACHE™ → Purge page cache** (`admin.php?page=press_cache`).
2. That clears origin. The ARES gateway edge can still serve the canonical URL as a HIT; confirm with `?cb=$RANDOM`. Instant public purge is Pagely Atomic (`atomic.pagely.com`) if origin is clean and the edge is not.

**Verify:**

```bash
curl -s "https://kriskrug.co/?cb=$RANDOM" | grep -c "fbevents\|fbq(\|facebook.com/tr"   # expect 0
curl -s "https://kriskrug.co/about/?cb=$RANDOM" | grep -c "fbevents\|fbq("              # expect 0
```

Also grep a no-query canonical fetch after a few minutes. Confirm Code Snippets `active` flags still match the step-0 snapshot (a PHP fatal in *that* plugin can auto-disable unrelated snippets; WPCode edits should not, but check anyway).

### 3. Install the gtag delay

This half **is** the Code Snippets plugin (left nav **Snippets**). Sibling for reference: live `KK Asset Diet`, id 10, same front-end scope.

**wp-admin (preferred for a one-sitting apply):**

1. wp-admin → **Snippets → Add New** (`admin.php?page=add-snippet`).
2. Title: `KK Script Diet`.
3. Paste [`issue-706-script-diet-snippet.php`](issue-706-script-diet-snippet.php) **without** the opening `<?php` tag.
4. Location: **Only run on site front-end**. Priority default.
5. Save Changes and Activate. **Live id 22** (created 2026-08-17).

**REST alternative** (same plugin; still snapshot-first via step 0): create in wp-admin rather than guessing an ID. Do not POST against a placeholder `<ID>`.

It has passed `php -l` and `make validate` (phpcs, WordPress security ruleset) in the repo. The committed browser-semantics harness proves that nothing loads before interaction, an early `gtag()` call queues into `dataLayer` and survives, the tag is appended exactly once with `async`, interaction listeners are removed after boot, and the non-interaction path obeys the timing contract below.

**Timing contract:** interaction may boot gtag immediately. Without interaction,
gtag boots no earlier than 3 seconds after `load`: the loader waits three full
seconds, then requests the next idle opportunity. That idle request has a
one-second ceiling, so an active foreground page boots between roughly three
and four seconds after `load` (subject to normal browser timer throttling). A
browser without `requestIdleCallback` boots at the three-second timer.

Purge PressCACHE again (`admin.php?page=press_cache`), then verify with a cache-bust query.

**Verify:**

```bash
curl -s "https://kriskrug.co/?cb=$RANDOM" > /tmp/kk-706-home-after.html
grep -c "google_gtagjs-js" /tmp/kk-706-home-after.html   # expect 0
grep -c "kk-gtag-delayed"  /tmp/kk-706-home-after.html   # expect 1
grep -c "G-X7JE8B32L7"     /tmp/kk-706-home-after.html   # expect >=1, inside the delayed loader
```

If `google_gtagjs-js` is still present, the dequeue did not win the hook race. The snippet already registers its capture on both `wp_enqueue_scripts` (999) and `wp_print_scripts` (100); if both miss, Site Kit changed how it enqueues and the handle capture needs re-derivation. The snippet fails safe in that case — gtag simply loads as it does today, nothing breaks.

Then confirm analytics still fires, in a browser with devtools open:

1. Load `https://kriskrug.co/` logged out. Network tab filtered to `googletagmanager` — **nothing** during load.
2. Click anywhere. `gtag/js?id=G-X7JE8B32L7` requests, followed by a `/g/collect` beacon.
3. Reload, touch nothing. No request may fire in the first 3 s after `load`;
   the same requests then fire at the next idle opportunity, no more than one
   additional second later on an active foreground page.
4. Realtime in GA4 shows the session.

Step 4 is the one that actually proves the ruling was honoured — delayed, not dropped.

---

## Rollback

Each step is independently reversible. Nothing here needs a restore drill. The two halves live in **different plugins**.

| To undo | Do this | Effect |
|---|---|---|
| gtag delay | wp-admin → **Snippets** → toggle `KK Script Diet` inactive. REST: POST `{"active": false}` to `/wp-json/code-snippets/v1/snippets/22`. | Dequeue stops, Site Kit's own tag prints eagerly again. Site Kit settings were never touched. |
| Pixel removal | WPCode: re-activate the snippet, or paste the Header & Footer box back from `~/kk-snapshots/wpcode-pixel-before-706-*.txt`. | Pixel returns. There is no Code Snippets pixel id to POST. |
| gtag delay, instantly | Code Snippets safe mode: `https://kriskrug.co/wp-admin/admin.php?page=snippets&snippets-safe-mode=1` | Disables **all Code Snippets**, including unrelated live ones (`KK Schema`, `KK Asset Diet`, …). Confirm it works here before relying on it as the panic button. **Does not restore the pixel** (WPCode). |

Purge PressCACHE after any rollback (`admin.php?page=press_cache`), then re-run the verify greps inverted (cache-bust with `?cb=`).

Pixel ID `1720755522050230` is recorded here so a re-add never needs an Events Manager dig. It is public in the page source, not a secret.

---

## Expected measurement delta

Baseline: `docs/current-state/reports/psi-mobile-2026-08-10.md` (mobile, Lighthouse 13.4.1, emulated Moto G Power, slow 4G).

**Should move:**

| Metric | Before | Expected after | Why |
|---|---|---|---|
| Third-party transfer | 354 KiB | ~0 KiB during load | 176 KiB pixel deleted; 178 KiB gtag moved past the load window |
| Third-party main thread | 342 ms | ~0 ms during load | 186 ms pixel + 156 ms gtag |
| Long tasks from these origins | 4 (146, 115, 88, 67 ms) | 0 | All four belong to the pixel and gtag |
| Total Blocking Time | 160 ms | under 50 ms | Those four tasks were the TBT |
| Unused JavaScript | 131 KiB flagged | 131 KiB less | 58.2 pixel + 72.9 gtag |
| Legacy JS polyfills | 12.5 KiB | 0 | All of it was in `fbevents.js` |
| Efficient cache policy | fbevents 20-min TTL flagged | audit clears | Origin gone |
| Performance score | 43 | expect 50s | TBT improves; LCP and CLS do not, and they dominate this score |

**Should NOT move, and do not credit this change if they do:**

LCP 7.6 s and CLS 0.430. Both trace to the theme's reveal system and the Boost critical-CSS snapshot (#701), and the 944 KiB image-delivery backlog is its own lane. If LCP or CLS shifts in the rerun, that is same-day content drift or the still-owed Boost critical-CSS regeneration, not this diet.

**One honest caveat on the gtag half.** The bytes are not saved, they are moved. Whether PSI *shows* the gtag improvement depends on where Lighthouse's trace ends relative to the fire point. The snippet measures its three-second delay from the `load` event rather than from parse, and on this page load lands late, so gtag should fall outside the trace and the win should be visible. But if the rerun still attributes gtag cost, the fix is not broken — check the browser waterfall in the verify step above, which measures the thing that actually matters. If KK wants the metric to move unambiguously, the knob is the `3000` delay before `requestIdleCallback`; raising it or going interaction-only pushes the tag further out at the cost of losing bounced sessions from GA4.

**How to confirm:** rerun PSI mobile against `https://kriskrug.co/` (https://pagespeed.web.dev/analysis?url=https%3A%2F%2Fkriskrug.co%2F, Mobile tab), then write `docs/current-state/reports/psi-mobile-<YYYY-MM-DD>.md` in the same shape as the 2026-08-10 report and commit it. Close #706 against the third acceptance criterion: "Post-apply PSI shows TBT long tasks from these origins gone." LCP and CLS staying put is expected, not a failed apply.

Run it at least 30 minutes after the cache purge so PSI is not scoring a partially-warm edge.

---

## Not in scope

#709 (security headers, prep-only) touches the same Best Practices section of the same PSI report. It is a separate lane and stays separate.
