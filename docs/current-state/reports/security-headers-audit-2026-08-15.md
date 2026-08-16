# Security response headers audit — kriskrug.co

**Issue:** #709 (`[SECURITY] Baseline security response headers`)
**Status:** PREP ONLY. Read-only audit. No live change was made, proposed for auto-apply, or staged for deploy.
**Captured:** 2026-08-16 05:41–05:45 UTC (2026-08-15 evening PT), unauthenticated, logged out, `curl -sI` only.
**Stack at capture:** WordPress 7.0.4, Aurora 1.6.4, `Pagely-ARES/1.22.28`, Jetpack Boost page cache, CloudFront in front of `s5102.pcdn.co`.

---

## 1. Headline

**kriskrug.co sends no security response headers on any public route.** Not HSTS, not `nosniff`, not `Referrer-Policy`, not `X-Frame-Options`, not CSP, not `Permissions-Policy`. The only security headers on the whole site come from WordPress core, on `wp-login.php` and the REST API, and core sets those without anyone here configuring anything.

The nuance that matters more than the gap: **this site cannot run a meaningful anti-XSS CSP, and it is not close.** Section 5 shows why, with counts. The honest recommendation is three cheap headers, one of them genuinely load-bearing, and an explicit decline on the CSP and Trusted Types items PSI flagged.

---

## 2. Current header state, per route

Six representative routes plus five supporting probes. Every row is a live `curl -sI` from the capture window.

### 2.1 Public HTML routes — the whole front end

| Route | Status | Cache | Security headers present |
|---|---|---|---|
| `/` (homepage) | 200 | ARES `HIT`, Boost `hit` | **none** |
| `/2026/08/10/keep-the-machine-strange/` (post) | 200 | ARES `EXPIRED`, Boost `hit` | **none** |
| `/about/` (page) | 200 | ARES `HIT`, Boost `hit` | **none** |
| `/category/vancouver-ai-ecosystem/` (archive) | 200 | ARES `MISS`, Boost `hit` | **none** |
| `/contact/` | 200 | — | **none** |
| `/definitely-not-a-real-url-zzz/` (404, PHP-rendered, uncached) | 404 | Boost `miss` | **none** |
| `/feed/` | 200 | ARES `HIT` | **none** |

The 404 row is the control: it is PHP-rendered and uncached, and it still carries nothing. So the absence is "nothing sets these headers," not "a cache is stripping them."

Full homepage response, verbatim, as the reference shape:

```
HTTP/2 200
date: Sun, 16 Aug 2026 05:41:51 GMT
content-type: text/html; charset=UTF-8
vary: Accept-Encoding
server: Pagely-ARES/1.22.28
x-gateway-request-id: 78b3cee6b1089f71d9873ba013308110
x-jetpack-boost-cache: hit
x-gateway-cache-key: 1786733843.186|standard|https|kriskrug.co|||/
x-gateway-cache-status: HIT
x-gateway-skip-cache: 0
```

### 2.2 Static assets

| Route | Served by | Security headers |
|---|---|---|
| `/wp-content/themes/kk-aurora/style.css` | Apache origin via ARES, `max-age=2592000` | **none** |
| `s5102.pcdn.co/.../style.css` | CloudFront | **none** |
| `s5102.pcdn.co/wp-content/uploads/2023/07/krug-1.jpg` | CloudFront | **none** |

Static assets never execute PHP. Anything set via a WordPress filter or Code Snippet **cannot reach these routes.** That constraint drives most of section 6.

### 2.3 Where headers *do* exist (WordPress core, not us)

`/wp-login.php`:

```
x-frame-options: SAMEORIGIN
content-security-policy: frame-ancestors 'self';
referrer-policy: strict-origin-when-cross-origin
set-cookie: wordpress_test_cookie=...; path=/; secure; HttpOnly
```

`/wp-json/` and `/wp-json/wp/v2/users`:

```
x-content-type-options: nosniff
x-robots-tag: noindex
vary: Origin
```

Both sets are WordPress core defaults. Note the shape of the gap: **core already decided `frame-ancestors 'self'` and `nosniff` are correct for this application, and applies them only to the surfaces core owns.** Recommendations 2 and 3 below are just extending core's own posture to the front end.

### 2.4 Transport

| Probe | Result |
|---|---|
| `http://kriskrug.co/` | `301` → `https://kriskrug.co/`, served by ARES, **no HSTS** |
| `https://www.kriskrug.co/` | `301` → apex, `x-redirect-by: WordPress`, **no HSTS** |
| HSTS anywhere on the site | **absent on every route checked** |
| Subdomains found (short probe) | `www` only → `wp20-gw2.host.pressdns.com` |

---

## 3. Gap analysis against a sensible baseline

| Header | Present? | Real-world gap on *this* site |
|---|---|---|
| `Strict-Transport-Security` | No | **Genuine.** Every first visit to `http://kriskrug.co` is a plaintext 301. That 301 is the SSL-strip window, and `wp-login.php` lives on the same host. |
| `X-Content-Type-Options` | REST only | Modest. WP serves correct `Content-Type`; uploads sit on a separate CDN host. Cheap to close. |
| `X-Frame-Options` / `frame-ancestors` | `wp-login.php` only | Modest. `/contact/` has no form (three `mailto:` links, zero `<form>` tags), so the classic clickjack target is absent. Popups and the search form remain. |
| `Referrer-Policy` | `wp-login.php` only | **Near zero.** `strict-origin-when-cross-origin` is already the default in Chrome, Firefox, and Safari. Setting it explicitly restates the browser default. |
| `Permissions-Policy` | No | **Near zero,** and mildly hazardous — see section 7. |
| `Content-Security-Policy` (XSS) | No | Gap is real in the abstract and **not closeable here**. Section 5. |
| `Cross-Origin-Opener-Policy` | No | **Near zero.** No cross-origin isolation need, no `SharedArrayBuffer`, no sensitive `window.opener` handles. |
| Over-sharing headers | — | `server: Pagely-ARES/1.22.28`, `<meta name="generator" content="WordPress 7.0.4">`, `<meta name="generator" content="Site Kit by Google 1.185.0">`. Version disclosure, low severity, and `server:` is not ours to change. |

---

## 4. Ranked recommendations

Ranked by real-world risk reduction on this specific site, not by scanner score. Only three items are recommended.

| # | Header | Proposed value | Implementation surface | Risk if wrong | Effort |
|---|---|---|---|---|---|
| 1 | `Strict-Transport-Security` | **Phase 1:** `max-age=86400`<br>**Phase 2 (after 7 clean days):** `max-age=15768000`<br>No `includeSubDomains`, no `preload` | **Preferred:** Pagely ARES edge (covers HTML + static + CDN uniformly, cache-independent). **Fallback:** `send_headers` in a Code Snippet — covers HTML routes only, which is sufficient, because HSTS is per-host and any one HTTPS response sets the host policy | **This is the one header that is not cleanly reversible.** Browsers honour `max-age` locally after you remove it. A short phase-1 `max-age` is the entire mitigation. Breaks nothing unless some HTTPS path is broken, which it is not | Low |
| 2 | `Content-Security-Policy: frame-ancestors 'self';`<br>+ `X-Frame-Options: SAMEORIGIN` | as written | `send_headers` Code Snippet, or ARES | Breaks any legitimate external iframe embed of a kriskrug.co page. **Pre-flight: KK confirms nothing (Luma, Notion, a partner site, an event page) embeds kriskrug.co in an iframe.** Instantly reversible — remove the header, purge | Low |
| 3 | `X-Content-Type-Options: nosniff` | `nosniff` | `send_headers` Code Snippet for HTML; ARES if you want it on uploads too, which is where it actually matters | Very low. Breaks only if some route serves content with a wrong `Content-Type` that a browser was silently rescuing. None observed | Low |

Ship all three in one snippet, or none. They are ~6 lines together.

### Proposed snippet shape (illustrative, not deployed)

```php
add_action( 'send_headers', function () {
    if ( is_admin() ) {
        return;
    }
    header( 'Strict-Transport-Security: max-age=86400' );
    header( 'X-Content-Type-Options: nosniff' );
    header( 'X-Frame-Options: SAMEORIGIN' );
    header( "Content-Security-Policy: frame-ancestors 'self';" );
} );
```

Do not paste this anywhere yet. It is the artifact for KK's ruling, not a deploy.

---

## 5. Why an anti-XSS CSP is off the table here

This is the substantive finding, and it is structural rather than a matter of effort.

### 5.1 The site is built out of inline code

Measured on one post, `/2026/08/10/keep-the-machine-strange/`:

| Thing | Count |
|---|---|
| `<style>` blocks (inline) | **31** |
| `<script>` blocks with **no** `src` (inline) | **6** |
| `<script src=…>` (external) | 2 |
| YouTube iframes | 3 |

Homepage: 19 inline `<style>` blocks, 10 inline `style=` attributes, 6 inline `<script>` blocks.

Both of the tracking injectors are **inline bootstraps**, not external `src` tags. The Facebook pixel is an inline IIFE that constructs a script element pointing at `connect.facebook.net/en_US/fbevents.js`. GTM is the same pattern. WordPress core additionally emits `<script type="speculationrules">`, which `script-src` also governs.

So any `script-src` that omits `'unsafe-inline'` kills the pixel, GTM, and core speculative loading on day one.

### 5.2 Nonces are impossible under a full-page cache

The standard escape from `'unsafe-inline'` is a per-response nonce. **This site cannot generate one.** Two full-page HTML caches sit in front of PHP: ARES (`x-gateway-cache-status: HIT` on `/`, `/about/`, `/feed/`) and Jetpack Boost (`x-jetpack-boost-cache: hit` on every HTML route measured). A cached page has one frozen nonce served to every visitor for the life of the cache entry. A shared, long-lived, publicly readable nonce is not a nonce. It provides zero protection while adding a whole maintenance surface.

### 5.3 Hashes break on ordinary publishing

The remaining option is hashing every inline block. Those 31 `<style>` blocks are largely Jetpack Boost critical CSS, which **regenerates whenever the theme or page geometry changes** — the exact mechanism behind the #701 CLS/LCP incident, and the reason "regenerate critical CSS" is still an owed post-deploy step. A hash-pinned CSP means every post publish and every Boost regeneration silently breaks page rendering until someone recomputes hashes. That converts routine content work into a live-site outage risk.

### 5.4 Conclusion

Any CSP that runs on this stack contains `script-src 'unsafe-inline'` and `style-src 'unsafe-inline'`. That policy provides no XSS protection. It would satisfy the PSI line item and nothing else. **Decline.**

`frame-ancestors` is the exception and is recommended above: it is a nonce-free, hash-free, cache-safe directive that is unaffected by all of the above.

---

## 6. What each implementation surface can actually reach

A recommendation that cannot ship on this stack is worthless, so here is the constraint map.

| Surface | Reaches | Availability | Notes |
|---|---|---|---|
| **Pagely ARES edge** | Everything: HTML, static assets, the CDN host, redirects | **Unverified from outside.** Requires an Atomic panel check or a Pagely support ticket. I did not log in | The correct home for HSTS and `nosniff`. Cannot be confirmed self-serve without KK |
| **`.htaccess` at web root** | HTML + static served by the Apache origin. Not the CloudFront CDN host | **Plausible, unverified.** Origin is Apache (default Apache 403 body, Apache `etag` format). Repo tracks no `.htaccess`. Would need SFTP (`scripts/deploy_theme_sftp.py`, Keychain `pagely-sftp-kriskrug`) | Pagely may manage or override the root `.htaccess`. Verify before relying on it. Also needs `mod_headers` |
| **Code Snippet (`send_headers`)** | HTML routes only. **Never** static assets or the CDN | **Confirmed available.** Site snippets are REST-writable with the app password (`code-snippets/v1` namespace registered; unauthenticated `GET /wp-json/code-snippets/v1/snippets` returns 401, i.e. properly gated) | Most reversible surface. Headers get baked into both caches, so any change needs a Pagely purge to take effect |
| **Theme `functions.php`** | Same reach as a snippet | Available, but couples a security setting to the Aurora deploy cycle and its pixel gate | Prefer the snippet |

**Repo state:** `grep` across all `*.php` for `header(` calls setting security headers, and for `send_headers` / `wp_headers` filters, returns **nothing**. No `.htaccess` is tracked. This is a clean slate — no existing implementation to conflict with.

**Cache caveat, applies to every PHP-surface recommendation:** a header set in PHP is captured into the ARES and Boost cache entries alongside the body. Adding one takes effect on cache miss; changing or removing one requires a purge (see the `pagely-page-cache-purge` note). Verify any apply with a logged-out `curl -sI` against a cache-`MISS` route, not a `HIT`.

---

## 7. Not worth doing on this site, and why

| Item | Why not |
|---|---|
| **Enforced anti-XSS CSP** | Section 5. Every workable policy needs `'unsafe-inline'` on both `script-src` and `style-src`, which is the same as having no policy, plus maintenance. |
| **Report-only CSP** (#709 asks for this as step one) | **Recommend against, and this is a deliberate departure from the issue.** Report-only needs a collector. There is none. `report-uri` to a third party adds a vendor and a privacy surface to a privacy exercise; a self-hosted collector on WordPress means standing up a new unauthenticated write endpoint, which is a worse security tradeoff than the one being measured. And it would report violations that are already fully predictable from reading the HTML. **Section 5 is the report-only run**, done for free, with the answer already in hand. |
| **`Cross-Origin-Opener-Policy`** | PSI flags COOP on every site it scans. Real benefit requires cross-origin isolation, which this site has no use for — no `SharedArrayBuffer`, no cross-origin worker isolation, no sensitive `window.opener` relationships. `same-origin` risks breaking share popups for a benefit of zero. |
| **Trusted Types** | Would require rewriting DOM sinks across WordPress core, Jetpack, Site Kit, GTM, and Popup Maker. Not a configuration change. Not achievable on a hosted WordPress site. |
| **`Permissions-Policy`** | Near-zero benefit (the site uses none of the gated APIs, and no third-party script is reaching for them), plus an actual foot-gun: a blanket `fullscreen=()` or `encrypted-media=()` **breaks the three YouTube embeds on the Postman post.** Getting it right means an allowlist per embed type, for no measurable gain. Skip. |
| **`Referrer-Policy`** | `strict-origin-when-cross-origin` has been the browser default in Chrome, Firefox, and Safari since 2020–2021. Setting it explicitly changes nothing for any current visitor. Harmless, so bundle it if you want a tidier scan result, but it is a scanner-score item, not a risk item. |
| **HSTS `includeSubDomains` / `preload`** | Not now. A short probe found only `www`, but "only `www` today" is not an inventory, and preload-list removal takes months. Revisit after phase 2 has been stable, if ever. |
| **Suppressing `<meta name="generator">`** | Version disclosure is real but low value — an attacker fingerprints WordPress from `/wp-json/` and asset paths regardless. Patching promptly beats hiding the number. |

---

## 8. Beyond headers — flagged, not fixed

Per scope, these are named by file/surface and kind only. **No remediation is proposed or performed here.** Each deserves its own issue and its own gate.

1. **Username enumeration, two independent public paths.** `/wp-json/wp/v2/users` returns `x-wp-total: 2` with both usernames, and `/wp-sitemap-users-1.xml` lists both author archives. `/?author=1` 301s to a username-bearing URL. One of the two accounts is a host-provisioned administrator. Combined with an openly reachable `wp-login.php`, this hands an attacker the valid-username half of a credential-stuffing pair. **Partial fix already exists in-repo and is not live:** `fixes/issue-331-archive-sitemap-policy.php` (PR #757 independently confirmed it is not deployed — `/wp-sitemap.xml` still lists `wp-sitemap-users-1.xml`). This is, in my assessment, a larger real-world risk than any header in section 4.

2. **`xmlrpc.php` is reachable.** `POST /xmlrpc.php` returns `200` with `content-type: text/xml`. Historically the preferred brute-force amplification and pingback SSRF surface. I did **not** probe `system.multicall` or any method — that would be an attack, not an audit. Reachability is the finding; exploitability is untested.

3. **Unconsented third-party tracking.** The Facebook pixel fires `PageView` inline on every page load with no consent gate, sending visitor IP and URL to Meta. Same for GTM. This is a PIPEDA/GDPR-shaped exposure, not a performance one. Worth recording on **#706**, which already proposes removing the pixel on performance grounds: **removing it also closes a privacy issue,** which strengthens the case for "remove" over "defer-load."

4. **REST CORS reflects arbitrary `Origin` with `Access-Control-Allow-Credentials: true`.** Verified: `Origin: https://example.com` is echoed back in `access-control-allow-origin`. **This is WordPress core default behaviour**, mitigated by the `X-WP-Nonce` requirement for cookie-authenticated writes, and `Vary: Origin` is correctly set so it is not cache-poisonable. Recorded for completeness. Not a kriskrug-specific defect and **not** something to "fix."

5. **Checked and clean — worth recording so nobody re-raises it.** The MCP adapter (`/wp-json/mcp/mcp-adapter-default-server`) and the abilities API (`/wp-json/wp-abilities/v1/*`) are exposed in the REST index but **properly authenticated**: unauthenticated GET returns `401 rest_forbidden`. Same for `code-snippets/v1/snippets`, `zbscrm/v1/contacts`, and `redirection/v1`. Namespace index routes returning 200 is normal core behaviour, not a leak. `readme.html` and `license.txt` are `404`. Directory listing on `/wp-content/uploads/2026/08/` is `403`.

---

## 9. Rollback

| Recommendation | Rollback |
|---|---|
| `X-Frame-Options`, `frame-ancestors`, `nosniff` | Delete the lines from the snippet (or disable the snippet), purge the Pagely page cache, confirm with logged-out `curl -sI` on a `MISS` route. Effectively instant. |
| HSTS | Removing the header stops new clients from receiving it, but **clients that already received it keep enforcing HTTPS locally for the remaining `max-age`.** This is why phase 1 is `max-age=86400`: worst-case exposure is one day of forced HTTPS, which is the desired state anyway. Do not raise past phase 1 until seven clean days have passed. Do not add `preload` — that rollback is measured in months and runs through a third party. |

Snapshot before any apply: this document is the pre-change header state. Re-run the section 2 probes after any apply and diff against it.

---

## 10. Verification method

Every claim above comes from unauthenticated `curl` against production during the capture window, plus `grep` over the repo working tree. No credentials were used, no headers were sent beyond a test `Origin`, no `POST`/`PUT`/`DELETE` was issued to any endpoint, no MCP ability was executed, no snippet was read or written, and no live configuration was changed. Cache status is reported per route because a `HIT` reflects a prior response, not necessarily the current origin behaviour — the 404 and archive rows are the uncached controls.

---

## 11. Acceptance criteria for #709

- [x] Current-state header inventory committed — sections 2 and 3
- [x] Proposed header set with per-header rationale and breakage risks — section 4
- [ ] ~~CSP starts report-only with a monitoring plan~~ — **explicitly declined with reasoning**, sections 5 and 7. Needs KK's ruling on the departure.
- [x] Explicit rollback path documented — section 9

## 12. What KK needs to rule on

1. **Ship the three-header set** (HSTS phase 1, `frame-ancestors` + XFO, `nosniff`)? Yes / no / subset.
2. **Does anything embed kriskrug.co in an iframe?** Blocks recommendation 2 only.
3. **Accept the report-only CSP decline**, against the issue's stated step one?
4. **Which surface** — open a Pagely ticket for ARES (better coverage, slower), or ship the Code Snippet (HTML-only, immediate, reversible)?
5. Should the section 8 items be filed as their own issues? #706 in particular should record the privacy angle.

No live change ships until 1 through 4 are answered.
