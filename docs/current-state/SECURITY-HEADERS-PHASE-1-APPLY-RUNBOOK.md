# Security headers phase 1 apply runbook — nosniff + Referrer-Policy

**Issue:** [#1001](https://github.com/WalksWithASwagger/kriskrug-wp/issues/1001) (this runbook). Parent: [#709](https://github.com/WalksWithASwagger/kriskrug-wp/issues/709).
**Status:** Documentation only. This file is the apply procedure for phase 1. It does **not** authorize a live change.
**Source of truth:** [`SECURITY-HEADERS-DECISION-2026-09-06.md`](SECURITY-HEADERS-DECISION-2026-09-06.md). That packet supersedes the [August 2026 audit](reports/security-headers-audit-2026-08-15.md) on phase order and values.
**Captured for this doc:** 8 September 2026. No host, plugin, snippet, DNS, or live WordPress setting was changed while writing it.

Do not close #709 from this runbook or from a PR that only lands this file. Close #1001 when the runbook is merged. Keep #709 open until KK accepts a separately scoped live rollout.

## What phase 1 is

Two response headers, exact values, preferred owner **Pagely ARES**:

| Header | Exact value | Why this phase |
|---|---|---|
| `X-Content-Type-Options` | `nosniff` | Extends the existing WordPress REST posture to public HTML, redirects, errors, and static responses that ARES can reach. Wrong `Content-Type` on CSS/JS/font/media may then block loading — check MIME first. |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Makes the site-wide default explicit. Login already sends this value from WordPress core. Confirm booking referrals and embeds do not require a full cross-origin URL in `Referer`. |

Owner split from the decision packet:

| Role | Owns |
|---|---|
| KK | Approves this exact phase. Does not send a Pagely ticket implicitly. Answers the open questions below before anyone applies. |
| Pagely support / account operator | ARES configuration, cache invalidation, rollback. Captures the actual old/new config before apply. |
| Assigned repo agent | Before/after GET matrix and sanitized evidence. No live header mutation. |

[`ACCESS_CHANNELS.md`](ACCESS_CHANNELS.md) does not establish current host-panel access. This runbook therefore states values, coverage questions, and verification — not invented Atomic / ARES control syntax.

## Non-goals (explicit)

This phase does **not** include:

- **HSTS.** `Strict-Transport-Security` is phase 2 in the decision packet (`max-age=86400` first; later `max-age=15768000` is a separate approval). Do not add `includeSubDomains` or `preload`.
- **CSP** of any kind, including report-only. That is phase 3.
- **COOP**, Trusted Types, Permissions-Policy, public `X-Frame-Options`, or public `frame-ancestors`.
- **XML-RPC** changes.
- **A live apply from the agent.** No Pagely ticket from the agent. No Code Snippet enable. No plugin/theme header patch as a silent fallback.
- **Re-opening or re-litigating #767.** Security Desk live reconfirm 2026-09-07 (cache-busted): REST users `401`, users sitemap absent, `/?author=1` → `404`. Those surfaces are live PASS. HSTS remains absent and stays on #709 phase 2.

Do not silently switch from ARES to a WordPress plugin, Code Snippet, or theme `functions.php` if the host route is unavailable. Those alternatives exist in the decision packet and have worse coverage (they miss static/CDN and many server-generated errors). KK must choose a different surface in writing.

## Remaining questions for KK (do not invent Pagely UI)

The runbook stops here until these are answered. Inventing dashboard clicks would be false precision.

1. **How does Pagely accept two ARES response-header rules on this account?** Panel field, support request wording, or another operator-owned control — Pagely must name the mechanism. This repo has no verified panel session.
2. **What response classes does one edge rule cover?** Confirm cached HTML, origin errors, redirects (HTTP→HTTPS and www→apex), and static resources. A cache `MISS` or query parameter is not direct origin proof.
3. **Does `s5102.pcdn.co` need its own rule?** It is a separate CDN host, outside apex HSTS scope, and already serves Boost CSS/JS and fonts. Phase 1 still needs a yes/no on whether nosniff/Referrer-Policy must be set there too.
4. **Staging or approved local override first?** The decision packet requires a safe staging environment or an approved local response-header rehearsal, plus a private save of the previous config, before production apply.
5. **Host-provided safe error fixture?** Check a 404 and a host-provided safe error page. Never induce a production 500.
6. **Booking / embed Referer need?** Confirm no paid or partner flow requires the full cross-origin URL in `Referer`.
7. **Where is the private old/new ARES config stored?** Capture it before approval. Do not commit host-private syntax, cookies, cache keys, or request identifiers to this repo.

## Preconditions (before any human apply)

1. KK answers the questions above and **separately approves this exact phase**.
2. Pagely operator saves the current ARES header configuration privately.
3. Baseline GET matrix is on disk: [sanitized 2026-09-06 capture](reports/issue-709-headers-20260906.md). Re-run the same routes immediately before apply if that capture is stale; sanitize with the redaction rules below.
4. Existing WordPress core headers stay in place:
   - `/wp-json/` already sends `X-Content-Type-Options: nosniff`.
   - `/wp-login.php` (and the admin-redirect destination) already send `X-Frame-Options: SAMEORIGIN`, `Content-Security-Policy: frame-ancestors 'self'`, and `Referrer-Policy: strict-origin-when-cross-origin`.
5. Do not add a second enforced CSP or a conflicting Referrer-Policy on login.
6. MIME spot-check on a representative CSS, JS, font, and media URL (`Content-Type` matches the body) before flipping nosniff site-wide.
7. Local browser rehearsal on 2026-09-06 already overrode these two values (plus later-phase headers) in a private Chromium session only. That is compatibility evidence, not apply authorization. See [sanitized rehearsal](reports/issue-709-browser-rehearsal-20260906.json).

## Apply sequence (Pagely operator, after KK approval)

No Atomic click path is recorded here. The operator uses Pagely's actual control for this account.

1. Confirm the saved previous configuration is retrievable.
2. Add **only** these two headers at ARES, with the exact values in the table above.
3. Do not add HSTS, CSP, COOP, Permissions-Policy, or public framing headers in the same change.
4. Purge every cache the operator confirms is in path (ARES gateway and Jetpack Boost at minimum). REST and HTML can otherwise keep serving the pre-header object; #767's deploy receipt already showed stale ARES `HIT` after an origin change.
5. Tell the repo agent the change is live and which response classes the rule is claimed to cover.
6. Agent fills the after-matrix (next section), cold and warm, after the purge.
7. Observe 24 hours before any later phase. Phase 2 HSTS is a different approval.

## Before / after GET matrix

### Command

Logged out. Follow redirects so hops are visible. Discard the body.

```bash
curl -sS -L -D - -o /dev/null --max-redirs 5 'https://kriskrug.co/'
```

For the two redirect entries, also capture the **first hop** without `-L` so the 301 itself is recorded, then the followed chain with `-L`.

Do not send cookies. Do not use an authenticated WordPress session. A cache-busting query is allowed as a second observation; it is not origin proof. Record both canonical and cache-busted URLs when used.

### Redaction before anything is committed

Retain: every redirect hop, HTTP status, `content-type`, security headers present or absent, and cache *status* words already used in the 2026-09-06 evidence (`HIT`, `MISS`, `BYPASS`, `EXPIRED`, Boost `hit`/`miss`, `x-gateway-skip-cache`).

Remove before commit (never paste into the repo):

- `Set-Cookie` / `Cookie`
- `x-gateway-cache-key` and any other cache key
- `x-gateway-request-id` and any other request identifier
- `Authorization`, nonces, app-password material
- Authenticated HTML, editor URLs with `reauth` session proof, or user IDs in query strings

Match the sanitization already used in [`reports/issue-709-headers-20260906.md`](reports/issue-709-headers-20260906.md).

### Routes (from #709 / 2026-09-06 packet)

Fill After only after an approved apply. Before values below are the 2026-09-06 sanitized capture. Re-run Before immediately pre-apply if KK wants a same-day baseline.

| # | Request | Before (2026-09-06) | After (status / nosniff / Referrer-Policy / HSTS / notes) |
|---:|---|---|---|
| 1 | `http://kriskrug.co/` | 301 → HTTPS apex; no phase-1 headers; no HSTS | |
| 2 | `https://www.kriskrug.co/` | 301 → HTTPS apex; no phase-1 headers; no HSTS | |
| 3 | `https://kriskrug.co/` | 200 HTML; no nosniff; no Referrer-Policy; no HSTS | |
| 4 | `https://kriskrug.co/contact/` | 200 HTML; none of the three | |
| 5 | `https://kriskrug.co/speaking/` | 200 HTML; none of the three | |
| 6 | `https://kriskrug.co/2026/09/03/what-i-showed-founders-about-ai-workflows/` (post 12744) | 200 HTML; none of the three | |
| 7 | `https://kriskrug.co/wp-json/` | 200 JSON; **nosniff already present**; no Referrer-Policy; no HSTS | |
| 8 | Deliberately nonexistent path (use a fresh dated slug; do not reuse a now-cached 404) | 404 HTML; none of the three | |
| 9 | `https://kriskrug.co/wp-admin/` | 302 → login; login 200 keeps core XFO + `frame-ancestors 'self'` + Referrer-Policy | |
| 10 | `https://kriskrug.co/wp-login.php` | 200; core XFO + `frame-ancestors 'self'` + Referrer-Policy; no nosniff recorded | |
| 11 | `https://kriskrug.co/wp-content/themes/kk-aurora/style.css` | 200 `text/css`; no phase-1 headers | |

Optional extras (August audit, not required to close #1001): `/about/`, `/feed/`, one category archive, one `s5102.pcdn.co` CSS or font URL — only if question 3 says the CDN is in scope.

Record each row twice after apply: once after purge (expect `MISS` or `BYPASS` where that is normal) and once warm. A warm `HIT` that still lacks the new headers is a failed apply, not a pass.

### After-state pass / fail

Pass only if every class Pagely claimed to cover shows:

- `X-Content-Type-Options: nosniff`
- `Referrer-Policy: strict-origin-when-cross-origin`
- **No** new `Strict-Transport-Security`
- **No** new CSP, CSP-Report-Only, COOP, Permissions-Policy, or public `X-Frame-Options` / public `frame-ancestors`

And:

- REST still has nosniff (do not drop the core header).
- Login still has `X-Frame-Options: SAMEORIGIN` and `Content-Security-Policy: frame-ancestors 'self'` plus the same Referrer-Policy. Adding nosniff on login is expected if ARES covers that route; changing or duplicating an *enforced* CSP is a fail.
- Representative CSS/JS/font/media still load (nosniff MIME check).
- Speaking youtube-nocookie facades still create their iframes (decision-packet rehearsal already did this locally; repeat on live only after apply).

Fail and roll back if CSS/JS/fonts/media stop loading, or if a required booking/embed flow loses attribution and KK judges the Referrer-Policy at fault.

## Rollback (phase 1 only)

Owner: the same Pagely operator.

From the decision packet, narrowed to this phase:

1. Restore the **prior** ARES rule exactly (the private pre-apply capture). That means remove the two phase-1 headers from surfaces that did not have them.
2. Preserve pre-existing core headers on login and REST. Do not strip login XFO / `frame-ancestors` / Referrer-Policy or REST nosniff.
3. Purge all affected caches (ARES and Boost at minimum).
4. Repeat this GET matrix, cold and warm.
5. Repeat the failed browser flow (MIME load failure and/or proven referral breakage).

Trigger:

- Roll back **nosniff** for MIME failures (browser blocked CSS/JS/font/media).
- Roll back **Referrer-Policy** for proven attribution breakage.

Do not apply HSTS-clearing `max-age=0` here. HSTS is not installed in phase 1; that rollback belongs to phase 2.

Code Snippets and theme files are not the rollback path for an ARES apply. If KK later chose a different surface in writing, that surface's own disable/purge path would apply — and that choice is out of scope for this issue.

## After 24 clean hours

Stop. File or resume phase 2 (HSTS) only with a new KK approval. Phase 3 CSP remains a later packet. This runbook is complete when:

- the procedure above is on `main`, and
- #1001 can close.

#709 stays open until KK authorizes a live phase and the after-matrix is filled from that apply.
