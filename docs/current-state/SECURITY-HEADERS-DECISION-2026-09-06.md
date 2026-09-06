# Security headers decision packet — issue #709

Status: **prep complete; rollout not authorized**. Captured 6 September 2026. This packet updates the [August audit](reports/security-headers-audit-2026-08-15.md) with fresh GET evidence and supersedes its proposed policy. No host, plugin, snippet, DNS or live WordPress setting changed. The older audit's absolute statements about feasibility and origin behaviour are not deployment proof.

## Current evidence and limits

[Sanitized GET captures](reports/issue-709-headers-20260906.md) retain all redirect hops, HTTP status, content types and cache observations, with cookies, cache keys and request identifiers removed. Public Aurora stylesheet reads 1.6.11. `make doctor` and `make status-readonly` ran in the lane worktree; sandbox DNS and the absent lane venv degraded startup checks. Escalated public GETs and GitHub reads succeeded. No authenticated editor or host-control session was used.

| Surface | Observation |
|---|---|
| Homepage, contact, speaking, post 12744 | 200; no HSTS, CSP, XFO, nosniff, Referrer-Policy, Permissions-Policy or COOP |
| REST root | 200; `X-Content-Type-Options: nosniff` already present |
| Login, including admin redirect destination | 200; existing SAMEORIGIN, CSP frame-ancestors self and strict-origin-when-cross-origin |
| Deliberately nonexistent route | 404; no baseline security headers |
| Theme CSS | 200; no baseline security headers |
| HTTP apex / HTTPS www | 301 to HTTPS apex; no HSTS |

The field audit's blanket “zero headers” claim is false across the site, though the public HTML gap reproduces. These are observations through Pagely ARES. HIT, MISS, BYPASS and Boost headers describe intermediaries; even an uncached 404 is not direct origin access. No query parameter or MISS proves which layer adds/removes a header. Direct origin and CDN configuration remain unverified.

## Dependency inventory and exact proposal

Fresh HTML tag inspection of `/`, `/contact/` and `/speaking/` finds CDN-hosted Boost CSS/JS and Space Grotesk/DM Sans fonts at `s5102.pcdn.co`, inline scripts/styles, and two speaking iframes on `www.youtube-nocookie.com` (video IDs hYT-hsml_ds and -c7mgY2aSgM). Their allow attributes include encrypted-media, picture-in-picture and web-share, not camera/microphone/geolocation. `i0.wp.com` is an image dependency; Google Tag Manager is DNS-prefetched. Delayed analytics, dynamically requested resources and CSS URLs require runtime capture; outbound hyperlinks are not automatically CSP dependencies. The existing #706 analytics receipt supersedes the August Facebook inventory.

WordPress emits public oEmbed discovery links. Therefore external framing is a real compatibility candidate, even though actual consumers cannot be inferred from source. Keep the existing login framing policy; do not extend self-only framing to public pages until KK confirms WordPress oEmbed and partner/event-site requirements. Admin/editor dependencies, Site Kit authorization popups, media library/upload, previews, and current Jetpack functionality need an authenticated safe-environment rehearsal. None is claimed tested here.

Known host inventory: apex and `www.kriskrug.co` complete valid HTTPS requests; www redirects to apex. `s5102.pcdn.co` is a separate domain, outside apex HSTS scope. No authoritative DNS zone or complete subdomain inventory was available. **Do not include includeSubDomains or preload.** A DNS owner must inventory all present/future web subdomains and verify certificate renewal before any later proposal expands scope.

| Phase / header | Exact proposed value | Rationale, risk and gate |
|---|---|---|
| 1: X-Content-Type-Options | `nosniff` | Extends REST posture; validate CSS/JS/font/media MIME types first; wrong MIME may block loading. |
| 1: Referrer-Policy | `strict-origin-when-cross-origin` | Explicit consistent default; verify booking referrals and embeds do not require full cross-origin URLs. |
| 2: Strict-Transport-Security | `max-age=86400` | HTTPS pinning at apex and www separately; host must confirm TLS renewal and all serving paths. After seven clean days, separately approve `max-age=15768000`. |
| 3: Permissions-Policy candidate | `camera=(self), microphone=(self), geolocation=(self)` | Preserve first-party use; restrict third-party delegation only after the embedded-flow inventory. Do not restrict fullscreen/encrypted-media. Omit until rehearsal passes. |
| 3: CSP report-only | Full value below | Non-enforcing discovery; not strict XSS protection or permission to enforce. |
| Later: public frame protection | `Content-Security-Policy: frame-ancestors 'self'` | Only if consumer inventory permits; no new XFO needed. Preserve existing core login headers. External WordPress embeds could break. |
| Deferred: COOP | No header; evaluate `same-origin-allow-popups` in a separate rehearsal if a concrete isolation need emerges | Popup opener relationships and Site Kit authorization must work; do not set `same-origin` for a scanner score. |
| Deferred: Trusted Types | No `require-trusted-types-for` directive | Requires DOM-sink inventory and compatible policies across core/plugins; not proven impossible, but no safe implementation is established. |

Exact starter **report-only**, not enforcement-ready:

```text
Content-Security-Policy-Report-Only: default-src 'self'; script-src 'self' 'unsafe-inline' https://s5102.pcdn.co https://www.googletagmanager.com; style-src 'self' 'unsafe-inline' https://s5102.pcdn.co; img-src 'self' data: https:; font-src 'self' data: https://s5102.pcdn.co; connect-src 'self' https:; media-src 'self' blob: https:; frame-src 'self' https://www.youtube.com https://www.youtube-nocookie.com; object-src 'none'; base-uri 'self'; frame-ancestors 'self'
```

Broad HTTPS image/connect/media sources and unsafe-inline deliberately reduce initial noise; this policy cannot substantiate a strict anti-XSS claim. Missing dynamic dependencies should generate findings rather than be pre-emptively allowlisted. CSP frame-ancestors controls who embeds this site; frame-src controls videos embedded by this site.

## Delivery, monitoring and rollback

**Recommended owner:** KK approves the exact phase; Pagely support/account operator owns ARES configuration, cache invalidation and rollback; the assigned repo agent owns the before/after GET matrix and evidence. [Access channels](ACCESS_CHANNELS.md) does not establish current host-panel access. Do not send a support request implicitly. Ask Pagely to confirm whether edge rules cover cached HTML, origin errors, redirects and static resources and whether the separate CDN needs its own rule. Capture the actual old/new config before approval; this packet contains values, not invented Pagely control syntax.

Alternative: a dedicated WordPress plugin can supply PHP response headers but needs verified admin/login/REST hook coverage, activation/deactivation rollback and cache purge. Code Snippets has similar coverage limitations and a UI/config dependency. Neither covers server-generated errors or static/CDN responses reliably. Theme implementation unnecessarily couples this work to visual releases. Do not silently switch from the preferred host route if unavailable.

1. Obtain a safe staging environment or an approved local response-header override rehearsal. Save previous configuration privately. Verify baseline routes and existing core CSP; avoid duplicate/conflicting enforced policies.
2. Test phase 1 MIME/referrer behaviour, then apply only after separate KK approval. Repeat canonical GETs after host purge, both cold and warm. Check a 404 and a host-provided safe error fixture; never induce a production 500. Observe for 24 hours before the next phase.
3. Rehearse phase 2, approve and apply the one-day HSTS policy. Record daily TLS/redirect checks for seven days. Longer retention is a separate approval.
4. Rehearse the exact report-only CSP and Permissions-Policy candidate. For CSP use a bounded manual collection plan: agent saves browser console/securitypolicyviolation records privately for homepage, contact, speaking (play/fullscreen), representative post, search, 404, login, editor preview, media library and Site Kit popup. Record browser, route, directive, blocked origin and result; strip user IDs, query strings, credentials and report samples before committing aggregate evidence. Run Chromium and Firefox plus Safari where available, logged out and authenticated. This is controlled compatibility evidence, not population telemetry.
5. Review reports after the first pass and again after seven days of approved report-only operation with a repeat matrix; classify every first-party violation and required third-party origin. No collector is provisioned: no `report-to`/`report-uri` is claimed functional. If population coverage is requested, obtain separate approval for a collector with URL redaction, restricted access, 7-day retention and rate limits before adding an endpoint.
6. Enforcement requires zero unexplained required-flow violations, successful authenticated/media/embed tests, resolved framing consumers, and a separately reviewed narrower policy. Do not promote this permissive starter automatically. Lack of browser reports is not proof of safety.

Rollback owner is the same Pagely operator: restore the prior phase's exact rule, preserve pre-existing core headers, purge all affected caches, repeat the GET matrix and failed browser flow. Roll back nosniff for MIME failures, referrer policy for proven attribution breakage, Permissions-Policy for blocked intended APIs, and new CSP/frame rules for reporting overload or legitimate framing failures. Deferred COOP/Trusted Types have no deployed state to undo.

For HSTS serve `Strict-Transport-Security: max-age=0` over working HTTPS and purge; removing the header alone does not clear client state. Clients must reconnect successfully to receive the clearing value; cached HSTS **cannot be instantly undone for all clients**, and TLS must remain working through the prior retention window. [MDN HSTS reference](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Strict-Transport-Security). Report-only CSP monitors without enforcement; collection endpoints are additional configuration. [MDN report-only reference](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy-Report-Only).

## Acceptance and handoff

- Current header inventory: captured and committed with this packet, including redirect/error cases.
- Exact candidates, rationale, dependencies, rollout owners and rollback: above.
- CSP starts with a report-only proposal and concrete controlled collection plan; no deployment or browser compatibility pass claimed.
- Remaining execution gates: host capability/config readback, authoritative DNS inventory for any scope expansion, framing decision, safe authenticated browser tests, and KK approval of an exact rollout phase.
- #767 remains open and owns username exposure; its body was refreshed read-only. No username enumeration, REST restriction, generator suppression or credential testing is part of this lane. Missing headers do not prove compromise.

Prep acceptance is distinct from rollout verification. Keep #709 open until KK accepts the packet and decides whether a separately scoped rollout should follow.
