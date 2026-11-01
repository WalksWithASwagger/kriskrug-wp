# Unsent host and repository support requests

Prepared for [kk-kb #4819](https://github.com/WalksWithASwagger/kk-kb/issues/4819).
**Drafts only. KK has not authorized sending either request.** Review with the
[evidence and rollback package](HOST-SECURITY-REVIEW-2026-11-01.md). Account
identifiers and any existing private ticket reference must be supplied through
the authenticated support portal, not added to Git. No secret attachment is
needed. Owner: KK; next review November 2, 2026.

## Pagely: patch attestation and staging change proposal

**Subject:** kriskrug.co: confirm PHP patch coverage and prepare staged host hardening

Please provide a read-only assessment for our kriskrug.co application. This is
an information and planning request, not permission to alter production or
purchase an add-on.

Please confirm:

1. The running PHP version, package build, SAPI and vendor support coverage,
   including fixes/backports for CVE-2026-109618 and CVE-2026-109619. Does the
   October 23 PHP session-handler advisory apply to this site's configuration?
2. Which stable PHP versions this account can select now, with the extension
   differences and any account restrictions. We have local syntax and stub-test
   coverage on PHP 8.5.12, but have not certified the live plugin set. Please
   propose an 8.5 staging rehearsal if supported, or name the supported target
   and explain the constraint. Do not change versions yet.
3. The account's staging mechanism, a patched rollback runtime, how the prior
   configuration is retained/restored, and which caches/workers need refresh.
4. How to apply only `X-Content-Type-Options: nosniff` and
   `Referrer-Policy: strict-origin-when-cross-origin` through ARES after later
   approval. Please identify coverage for cached HTML, redirects, errors,
   static files and the separate CDN, preserving WordPress's current REST and
   login headers. No HSTS, CSP or framing-policy change is requested here.
5. Whether current Jetpack connections, mobile apps or publishing clients need
   XML-RPC. Please propose a restriction that preserves verified required
   clients, including reconnect behavior, with an exact saved-rule rollback.
   We have not sent XML-RPC POSTs or enumerated methods. A September inventory
   showed Jetpack core inactive, but it is too old to justify a blanket deny.

For the historical WordPress application-password incident recorded in May,
please advise who can provide issuer-side revocation evidence. We need only
the credential record's non-secret identifier, revocation timestamp, issuer/
operator confirmation and the incident/ticket reference. If no such record is
retained, please state that limitation; do not send a password or ask us to
replay the old one. We are not requesting rotation of current credentials.

Our November 1 public checks found WordPress's generator at 7.0.8, Aurora CSS
at 1.6.12, and XML-RPC GET/HEAD at 405. Public HTML lacks the two proposed
headers; REST already has nosniff and login retains its core framing/referrer
headers. These are edge observations, not proof of the origin's PHP version.
Please reply with the assessment and proposed staging/rollback procedure for
owner review. Production work requires a separate approval.

## GitHub: residual-history review eligibility

**Subject:** WalksWithASwagger/kriskrug-wp: eligibility review after historical credential rewrite

We maintain WalksWithASwagger/kriskrug-wp. Our May 19, 2026 operations record
states that a WordPress application password had been revoked and that the
affected history was rewritten. We are collecting issuer-side revocation
evidence separately and do not yet have a fresh attestation to attach.

Please advise whether this case qualifies for further sensitive-data removal
review under your current policy, and what metadata you need to assess cached
views, pull-request references or residual fork-network objects. We understand
that successful credential revocation may be sufficient and that support does
not guarantee removal where rotation mitigates the risk.

The current repository API reports zero visible forks. We do not interpret
that as proof that no historical or private copy exists. A local old commit
object remains, but we have not retrieved its content or probed old remote
SHA/raw URLs. Please distinguish any GitHub-hosted residual reference you can
verify from local copies outside your control.

We can provide the existing incident record and known affected identifiers
through this authenticated ticket without credential values or raw snapshots.
Our historical notes mention two PRs closed during the rewrite; that is not a
verified count of all affected PR references. The original tool output's
First Changed Commit list and any LFS-orphan report have not been recovered.
Please specify the minimum metadata required if those records are unavailable.

Please do not delete or dereference PRs, alter repositories/forks or run removal
until the owner reviews the exact proposed scope and consequences. No new
history rewrite or third-party contact is authorized by this request. Do not
return old credential strings in your reply.
