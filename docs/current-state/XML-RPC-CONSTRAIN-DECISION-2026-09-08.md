# XML-RPC constrain decision packet — issue #1002

Status: **prep complete; live disable not authorized**. Captured 8 September 2026. No host, plugin, snippet, DNS, Pagely, or live WordPress setting was changed. This packet does not authorize a Code Snippets paste or a Pagely deny rule.

Related work, not reopened here:

- [#767](https://github.com/WalksWithASwagger/kriskrug-wp/issues/767) — username-enumeration apply is live (REST users, author probes, #331 v2 sitemap). Do not re-litigate those surfaces. HSTS remains on #709.
- [#709](https://github.com/WalksWithASwagger/kriskrug-wp/issues/709) — security-headers packet; rollout not authorized. Phase-1 apply procedure is [#1001](https://github.com/WalksWithASwagger/kriskrug-wp/issues/1001). XML-RPC is out of that header lane.

## Current reachability (status only)

Logged-out probes, 2026-09-08. GET and HEAD only. No request body. No method names sent. No response body retained.

| Probe | Command shape | Status | Reading |
|---|---|---:|---|
| GET `/xmlrpc.php` | `curl -sS -o /dev/null -w "%{http_code}\\n" https://kriskrug.co/xmlrpc.php` | `405` | Endpoint is present. WordPress answers "method not allowed" to GET. |
| HEAD `/xmlrpc.php` | same URL, HEAD | `405` | Same presence signal. |

Prior status-only GET, 2026-08-16 15:15 UTC ([#709 audit](reports/security-headers-audit-2026-08-15.md) §8.2): also `405`. No drift in the GET/HEAD signal.

`405` on GET/HEAD is **reachable**, not closed. Closed, for this packet, means the path is denied before WordPress XML-RPC handles it (`403`, `404`, or `410` on both GET and HEAD). A PHP filter that only flips `xmlrpc_enabled` does **not** change this GET/HEAD status.

Repeatable assert: `scripts/check_xmlrpc_reachability.sh`. Desired post-apply (host/WAF deny) is PASS. Current live state is FAIL / REACHABLE. That FAIL is expected until KK approves a host deny.

## Required-client inventory

Question: does anything we actually run need `xmlrpc.php`?

| Client | Last evidence | Needs public XML-RPC? |
|---|---|---|
| Jetpack core (`jetpack/jetpack`) | Authenticated plugin list 2026-08-03: **inactive**. Public `GET /wp-json/jetpack/v4/settings` on 2026-09-08: `404` `rest_no_route` (same as the 2026-08-03 SEO inventory). | **No.** Core is not a required client today. |
| Jetpack Boost | Active in the 2026-08-03 list. Homepage 2026-09-08 still sends `x-jetpack-boost-cache`. REST namespaces `jetpack-boost/v1` and `jetpack-boost-ds` appear in the public index. | **No** for normal Boost cache/CSS work. Boost talks REST and local files, not this endpoint. |
| Jetpack Protect | Active in the 2026-08-03 list. Public index still lists `jetpack-protect/v1`. | **Not proven.** Day-to-day scans use REST / WordPress.com APIs. A later reconnect *might* want a host allowlist rather than a public-open endpoint. |
| Jetpack CRM | Active in the 2026-08-03 list. Public `zbscrm/v1` is present and was already `401` unauthenticated in the #709 audit. | **No.** Local CRM / authenticated REST. |
| Repo / ops clients | [WP auth-client inventory](WP-AUTH-CLIENT-INVENTORY-2026-07-08.md) (#306): REST + application passwords. No XML-RPC caller. | **No.** |
| WordPress mobile app / remote posting | No current session or documented workflow uses it. | **No** unless KK later chooses that client. |
| Incoming pingbacks / trackbacks | No product requirement recorded. | **No.** |

`jetpack/v4` still appears in the public REST namespace index. That is not proof Jetpack core is active: the settings route that core actually registers remains `404`.

**Decision input:** Jetpack core is not required. Do not keep `xmlrpc.php` publicly reachable "for Jetpack" on today's inventory. If KK later reactivates Jetpack core, decide reconnect (host allowlist vs leave open) **before** applying a deny. Do not apply the fallback snippet in that case.

Cookie checks such as `is_user_logged_in()` do **not** preserve a Jetpack XML-RPC tunnel. Jetpack's site-to-WordPress.com calls are not a logged-in wp-admin cookie session. A snippet that "disables XML-RPC except when logged in" would still break a future Jetpack reconnect.

## Recommended control

**Preferred: Pagely / WAF deny of `/xmlrpc.php` (GET, HEAD, and POST) at the edge.** Same owner split as the [#709 packet](SECURITY-HEADERS-DECISION-2026-09-06.md) and the [#1001 phase-1 runbook](SECURITY-HEADERS-PHASE-1-APPLY-RUNBOOK.md): KK approves the exact change; a Pagely operator applies ARES/WAF and rollback; a repo agent records status-only GET/HEAD. [ACCESS_CHANNELS.md](ACCESS_CHANNELS.md) does not establish current host-panel access. This packet states the outcome, not invented Atomic syntax.

| Control | GET/HEAD after apply | Request reaches PHP? | Why / why not |
|---|---|---|---|
| **Pagely ARES / WAF path deny** | `403` / `404` / `410` — check script can PASS | No | Stops the request before WordPress boots. Only control that changes the public GET/HEAD signal. Matches how #709/#1001 prefer the host for headers. |
| Code Snippet (`xmlrpc_enabled` → false) | Still `405` — check script still FAIL | Yes | Functional disable for POST handlers, but the file still answers and PHP still bootstraps. Acceptable **fallback** only if the host cannot deny the path. Draft: `fixes/issue-1002-xmlrpc-constrain.php`. |
| "Disable XML-RPC" plugin | Typically still `405` | Yes | Same PHP-layer limit, plus another plugin to inventory. Do not add a plugin for this. |
| Theme `functions.php` | Typically still `405` | Yes | Couples a security toggle to Track B / Aurora releases. Do not. |

Do not silently switch from host deny to a snippet or plugin if Pagely cannot do it this week. KK chooses the fallback in writing.

Do not combine host deny and the snippet unless KK wants belt-and-suspenders after the host rule is proven. Host deny alone is enough.

## Rollback

Nothing is live. These are the undo paths for a **future** KK-approved apply.

| If the apply was… | Rollback | Then |
|---|---|---|
| Pagely / WAF deny | Pagely operator restores the prior ARES/WAF rule exactly (private pre-apply capture). Purge the gateway cache. | `scripts/check_xmlrpc_reachability.sh` should return FAIL / `405` again. If Jetpack core was reactivated and reconnect failed, removing the deny is the first undo. |
| Fallback snippet | Deactivate the Code Snippet. Do not delete until KK says so. | GET/HEAD stay `405` (they never changed). Confirm Boost still caches and wp-admin still loads. |

Snapshot before any apply: this packet plus a private copy of the host rule (or the inactive snippet body). Re-run the check script after apply and after rollback. Status codes only.

## Residual risk if left open

Leaving `/xmlrpc.php` reachable means the file remains a public WordPress front door. GET/HEAD `405` only proves presence. This packet did **not** test POST, did **not** list methods, and does **not** claim a specific vulnerability.

Known compounding context, already owned elsewhere:

- `wp-login.php` stays on the same host.
- HSTS is still absent (#709 / #1001). That header lane is separate and is not authorized here.
- Public username listing on REST / sitemap / `?author=` was applied under #767. Do not treat that apply as XML-RPC work.

Residual if KK leaves XML-RPC open: the unauthenticated POST surface stays available; method availability stays untested; future scanners will keep flagging reachability. That is a product decision, not an emergency close.

## Fallback snippet (prep only)

`fixes/issue-1002-xmlrpc-constrain.php` is a last-resort Code Snippet. Headers say **PREP ONLY / not deployed**. It flips `xmlrpc_enabled` to false because today's inventory does not require Jetpack core.

It is **not** the recommended control:

1. GET/HEAD stay `405`, so `scripts/check_xmlrpc_reachability.sh` still FAILs after a snippet-only apply.
2. Every hit still boots PHP.
3. If Jetpack core is later reactivated, this snippet must stay off.

## Check script

`scripts/check_xmlrpc_reachability.sh`

- GET and HEAD only. No POST. No request body. No method names.
- Prints PASS/FAIL and status codes. Does not print response bodies.
- Exit `0` only when both verbs are `403`, `404`, or `410`.
- Before a host deny, expect FAIL.

## Acceptance and handoff

- Reachability evidence (status only): above. Matches the 2026-08-16 GET `405`.
- Required-client inventory: Jetpack core not required; Boost/Protect/CRM do not justify a public-open endpoint on current evidence.
- Recommended control: Pagely / WAF deny. Snippet and plugin are worse. Theme hook is out.
- Rollback: above. Residual risk if left open: above.
- Cross-links: #767 (do not reopen), #709 / #1001 (do not roll headers out from this packet).
- Live apply remains a separate KK approval. Nothing in Code Snippets. Nothing in Pagely.

Prep acceptance is not apply authorization. Keep the live disable gated until KK picks host deny (preferred) or an explicit fallback.