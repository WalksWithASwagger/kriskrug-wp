# WordPress host and credential-history review, 2026-11-01

**State: waiting for owner review. Preparation only.** Parent:
[kk-kb #4819](https://github.com/WalksWithASwagger/kk-kb/issues/4819).
No support request was sent, host setting changed, credential tested, history
rewritten, or production code deployed. KK owns the next decision; next check
2026-11-02. Provider replies and staging verification remain outstanding.

## Evidence and recommendation

Source tested: `72a05acbb0b50ca312342fb4ff891504e9708107` in an isolated
`kriskrug-wp` worktree. The primary checkout and its unpublished drafts were
preserved. Existing PR #1166 owns the WordPress startup baseline update; this
package does not edit those shared files.

Recommend confirming Pagely's security patch coverage first, then rehearsing
PHP 8.5 on staging if the account supports it. Keep the existing two-header
phase separate from PHP and XML-RPC changes so rollback has one clear cause.
Do not authorize a blanket XML-RPC deny using September's plugin inventory.

Public requests on November 1 retained only status, selected headers and
public version strings. [Machine-readable evidence](reports/host-security-public-20261101.json)
contains no cookies, cache keys, request identifiers or HTML bodies.

| Surface | Observed result |
| --- | --- |
| Home, Contact, Speaking | 200; no `nosniff`, Referrer-Policy or HSTS |
| REST index | 200; existing `X-Content-Type-Options: nosniff` |
| Login | 200; existing `SAMEORIGIN`, CSP `frame-ancestors 'self'`, and `strict-origin-when-cross-origin` |
| Deliberately nonexistent page | 404; none of the three baseline headers above |
| Aurora stylesheet | 200, `text/css`, public version `1.6.12` |
| XML-RPC GET and HEAD | 405; endpoint presence only, not proof of POST behavior |
| Public WordPress generator | `7.0.8`; not authenticated installation inventory |
| PHP version | Not exposed by sampled responses; host runtime and backports unknown |

These responses passed through Pagely ARES. They do not establish direct-origin
behavior, all CDN rules, active plugins or required XML-RPC clients. No XML-RPC
POST, user-enumeration probe, login attempt or authenticated content read ran.

The WordPress connector returned an expired-session error. The standard
`make doctor` / `make status-readonly` wrappers were not run: source inspection
showed direct process-credential inspection and an authenticated draft-queue
path through `load_env`. This task forbids value-file and process-environment
reads. Public checks, GitHub metadata and credential-free PHP tests replace
those startup observations; private queue and host state remain unknown.

## PHP options, local compatibility and rollback

Pagely documents per-application PHP selection in Atomic, with account-specific
availability and a possible support enablement requirement. Its extension
matrix, updated August 25, lists through PHP 8.3, while its general FAQ says
newer versions are available. These pages do **not** verify this account's
8.4/8.5 options. Ask the host for the actual selectable versions and extension
sets before choosing a target. Sources: [version selection](https://support.pagely.com/hc/en-us/articles/115000013092-Changing-PHP-Versions),
[current FAQ](https://support.pagely.com/hc/en-us/articles/26009642535195-Does-Pagely-Support-the-Latest-Versions-of-PHP),
[extension matrix](https://support.pagely.com/hc/en-us/articles/360057574951-PHP-Versions-and-Supported-Extensions-Reference).

Upstream PHP security support ends on December 31 of 2026 for 8.2, 2027 for
8.3, 2028 for 8.4 and 2029 for 8.5. WordPress 7.0 core lists compatibility
with all four; that does not certify the site's plugins or custom snippets.
Sources: [PHP support schedule](https://www.php.net/supported-versions.php),
[WordPress compatibility table](https://make.wordpress.org/core/handbook/references/php-compatibility-and-wordpress-versions/).

PHP's October 21 advisory names fixes in 8.2.35, 8.3.36, 8.4.27 and 8.5.12
for CVE-2026-109618 and CVE-2026-109619. Vendors can backport these fixes;
an older version string alone cannot establish exposure. Request package and
backport attestation rather than probing production. Also ask whether the
October 23 session-handler advisory applies to this account's configuration.
No PHP setting is proposed as a substitute for verified patches.
Source: [PHP's dated advisories](https://www.php.net/archive/2026.php).

**Local result:** `make php-syntax plugin-smoke theme-smoke` passed using
Homebrew PHP CLI **8.5.12**: all **54 tracked PHP files** parsed; Sidebar
Promos, Marquee Board, Practice, Aurora SEO title and final-URL smoke suites
passed. These suites use synthetic WordPress stubs. They do not boot WordPress,
third-party plugins, Pagely PHP-FPM, the database, cron or a browser. PHP
8.2/8.3/8.4 were not installed or tested. No global runtime changed.

After a separately approved staging session, the operator must:

1. Record current PHP package/SAPI, enabled extensions, relevant ini settings,
   active theme/plugins/snippets, and the previous Atomic choice privately.
   Confirm current and rollback runtimes both carry required security fixes.
2. Rehearse the proposed target on an owner-approved staging copy with outbound
   mail, webhooks and indexing disabled. Do not create a production-data copy
   merely because this document exists; its data/access plan needs approval.
3. Verify home/Contact/Speaking, wp-admin/editor, media upload, theme titles,
   REST authentication, scheduled tasks and each required Jetpack connection.
   Record sanitized errors and compare against baseline. Local CLI checks are
   supporting evidence, not the staging acceptance result.
4. Before production approval, identify the host operator, maintenance window,
   retrieval-tested configuration snapshot and exact rollback version. Change
   PHP alone. No simultaneous plugin/core/theme/database upgrade.
5. On a new fatal error, failed required flow, broken extension or material
   latency regression, restore the previous **patched** runtime and settings,
   restart workers/purge caches through the operator's supported procedure,
   and repeat the failed flow. Never silently fall back to an unpatched runtime.

## Headers and XML-RPC

Reuse the [existing phase-1 apply and rollback runbook](SECURITY-HEADERS-PHASE-1-APPLY-RUNBOOK.md):
`X-Content-Type-Options: nosniff` and
`Referrer-Policy: strict-origin-when-cross-origin` at ARES. Preserve the
existing REST/login headers. Check CSS/JS/font/media MIME types and booking/
embed flows in staging, confirm CDN/redirect/error coverage, privately save
the old rules, then compare cold and warm responses after an approved apply.
Restore only the changed rules and purge affected caches on a proven failure.
HSTS, CSP, public framing restrictions and later phases remain separate.
Pagely documents [response-header rules in Atomic](https://support.pagely.com/hc/en-us/articles/360056097471-Setting-Response-Headers-in-Atomic);
actual account access and coverage have not been verified.

The [September XML-RPC packet](XML-RPC-CONSTRAIN-DECISION-2026-09-08.md)
records Jetpack core as inactive **then**. That inventory is not current proof.
Ask the operator to confirm Jetpack core/Protect connections, mobile posting,
remote publishing and incoming pingback requirements before choosing a rule.
Where a required Jetpack connection uses XML-RPC, request a host-maintained
restriction that preserves that verified service and test connect/reconnect
on staging. Do not invent IP ranges, use a logged-in-cookie exception, or turn
on the old blanket-disable snippet. If no required client remains, prepare an
edge path deny with a saved-rule rollback. Either live choice needs KK approval.
Sources: [Pagely XML-RPC guidance](https://support.pagely.com/hc/en-us/articles/360024843412-Disabling-XML-RPC),
[Jetpack connection requirements](https://jetpack.com/support/getting-started-with-jetpack/troubleshoot-jetpack-connection-error-messages/).

GitHub readback found #709, #1001 and #1002 closed. Their documents are reusable
preparation, not evidence that the corresponding host changes were applied.

## Revocation and residual history

The [May 19 execution record](archive/CREDENTIAL-HISTORY-REWRITE-EXECUTION-2026-05-19.md)
reports a revoked WordPress application password and a completed rewrite of
three then-existing branches. Its companion preflight names a rotation-record
commit. Those are historical claims; this session has no issuer-side revocation
receipt. Do not recover, print, copy or test the old credential to obtain one.

Current GitHub repository metadata reports **public, main, zero visible forks**.
That count cannot prove the absence of deleted/private copies or cached views.
A type-only local Git lookup confirms the previously documented old commit
object still exists. Its body was not opened; local presence does not prove
remote reachability. No old SHA URL, raw snapshot, clone or fork was fetched.

GitHub says rotation can be sufficient and support removal is conditional on
risk that rotation cannot mitigate. Support can address eligible cached/PR
references; a local rewrite alone does not erase other clones or forks. This
package therefore requests eligibility and residual-risk clarification, not
an assertion that removal is required or available. Source:
[GitHub sensitive-data guidance](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository).

The [two unsent support drafts](HOST-SECURITY-SUPPORT-DRAFTS-2026-11-01.md)
request host patch/client metadata, issuer-side revocation evidence and GitHub
history-review eligibility. Known historical identifiers remain in the existing
incident record; no secret or old credential-bearing artifact should
be attached. Provider replies, live application and removal are not completed.
