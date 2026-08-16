# Third-party script diet — apply runbook (#706)

Prepared 2026-08-15. **Nothing here has been applied.** Both halves are live writes and stay KK-gated.

KK ruling on #706 (2026-08-10): **drop the Facebook pixel entirely; delay gtag** to first interaction or 3 s idle.

Artifact: [`issue-706-script-diet-snippet.php`](issue-706-script-diet-snippet.php) — the gtag half. The pixel half is a source-level deactivation, not code.

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

**Conclusion, stated at the confidence the evidence supports:** the pixel is hand-installed PHP/HTML on a `wp_head` hook, and the Code Snippets plugin is active and is the only surface on this site that does that. It is almost certainly a Code Snippet. This has **not** been confirmed by reading the snippet list, because that needs an authenticated REST call and credentials did not resolve in this worktree. Step 1 of the apply closes that gap in one call. Do not skip it.

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
grep -c "google_gtagjs-js" /tmp/kk-706-home-before.html  # expect 2 (tag + -after)
```

```bash
# Full Code Snippets snapshot — code bodies included, this is the restore source.
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

### 1. Locate the pixel, then read what else its snippet contains

From the snapshot JSON, find the snippet whose `code` contains `fbq` or `1720755522050230`. Record its `id`, `name`, `scope`, and `active`.

**Before deactivating, read the whole snippet body.** If it only prints the Meta Pixel block, deactivating it is the entire fix. If it also carries unrelated head markup — a verification meta, a Pinterest tag, anything — deactivating the snippet takes that down too. In that case edit the pixel block out and leave the rest, rather than flipping `active`.

The `<meta name="google-site-verification">` that renders directly after the pixel is *probably* Site Kit's (Site Kit prints it at `wp_head` 99), but confirm from the snippet body rather than trusting that.

If no snippet matches, stop and report. The pixel is then coming from a surface this prep did not identify, and the removal step needs re-derivation before anything is touched.

### 2. Deactivate the pixel

```bash
varlock run --inject vars -- sh -eu -c '
  curl --fail-with-body --silent --show-error -X POST \
    --user "${WP_USER:?}:${WP_APP_PASSWORD:?}" \
    -H "Content-Type: application/json" \
    --data "{\"active\": false}" \
    https://kriskrug.co/wp-json/code-snippets/v1/snippets/<ID>
'
```

Deactivate, do not delete. Per `wp-snippet-deploy`, REST DELETE is WAF-blocked anyway, and deactivation keeps the re-enable path to one call. Delete via wp-admin only after a soak, and only if KK wants it gone permanently.

Purge Pagely cache after the write (REST edits do not auto-purge).

**Verify:**

```bash
curl -s https://kriskrug.co/ | grep -c "fbevents\|fbq(\|facebook.com/tr"   # expect 0
curl -s https://kriskrug.co/about/ | grep -c "fbevents\|fbq("              # expect 0
```

Confirm no other snippet auto-deactivated (a PHP fatal makes Code Snippets disable things): re-fetch the snippet list and diff `active` flags against the snapshot.

### 3. Install the gtag delay

Paste `issue-706-script-diet-snippet.php` into Code Snippets as a new snippet, **stripping the leading `<?php`**. Name it `KK Script Diet`. Scope **front-end**. Sibling for reference: the existing `KK Asset Diet` snippet, same scope, same source-of-truth-in-repo convention.

It has passed `php -l` and `make validate` (phpcs, WordPress security ruleset) in the repo. The committed browser-semantics harness proves that nothing loads before interaction, an early `gtag()` call queues into `dataLayer` and survives, the tag is appended exactly once with `async`, interaction listeners are removed after boot, and the non-interaction path obeys the timing contract below.

**Timing contract:** interaction may boot gtag immediately. Without interaction,
gtag boots no earlier than 3 seconds after `load`: the loader waits three full
seconds, then requests the next idle opportunity. That idle request has a
one-second ceiling, so an active foreground page boots between roughly three
and four seconds after `load` (subject to normal browser timer throttling). A
browser without `requestIdleCallback` boots at the three-second timer.

Purge Pagely cache.

**Verify:**

```bash
curl -s https://kriskrug.co/ > /tmp/kk-706-home-after.html
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

Each step is independently reversible. Nothing here needs a restore drill.

| To undo | Do this | Effect |
|---|---|---|
| gtag delay | POST `{"active": false}` to the `KK Script Diet` snippet id | Dequeue stops, Site Kit's own tag prints eagerly again. Site Kit settings were never touched, so there is nothing to restore. |
| Pixel removal | POST `{"active": true}` to the pixel snippet id | Pixel returns. If step 1 required editing the body instead of toggling, restore the `code` field verbatim from the before-snapshot JSON. |
| Everything, instantly | Code Snippets safe mode | Disables all snippets at once. bc-ai.ca uses `…/wp-admin/admin.php?page=snippets&snippets-safe-mode=1`; confirm the same works here before relying on it as the panic button, since it is version-dependent. |

Purge Pagely cache after any rollback, then re-run the verify greps above inverted.

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

**How to confirm:** rerun PSI mobile against `https://kriskrug.co/` (https://pagespeed.web.dev/analysis?url=https%3A%2F%2Fkriskrug.co%2F, Mobile tab), then write `docs/current-state/reports/psi-mobile-<YYYY-MM-DD>.md` in the same shape as the 2026-08-10 report and commit it. Close #706 against the third acceptance criterion: "Post-apply PSI shows TBT long tasks from these origins gone."

Run it at least 30 minutes after the cache purge so PSI is not scoring a partially-warm edge.

---

## Not in scope

#709 (security headers, prep-only) touches the same Best Practices section of the same PSI report. It is a separate lane and stays separate.
