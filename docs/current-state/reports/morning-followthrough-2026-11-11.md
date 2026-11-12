# Morning follow-through — 2026-11-11

This supplements the [maintenance receipt](repo-maintenance-2026-11-11.md)
after Kris supplied Claude's parallel read-only findings. Observations are
November 11 in America/Vancouver; the independent transport and WordPress
readbacks below ran at approximately 05:30 UTC on November 12. The earlier
source reconciliation and roadmap shipped in PRs #1207 and #1208.

Subsequent release: Kris approved the BC + AI target and exact link. The
[publication receipt](../../../content/drafts/futureproof-2026-editorial/README.md)
records successful authenticated/public verification at 05:58 UTC on November
12. The pending-link discussion below is the earlier review checkpoint.

## Remaining branch cleanup

There were zero open PRs before this follow-through. The primary checkout was
clean apart from the four preserved untracked groups, with no extra worktree.
The following tips were verified, archived and removed:

| Branch | Removed from | Preserved tip | Evidence on main |
|---|---|---|---|
| `codex/publications-1191` | Local | `936f29c51ddfb2082cbc41f153399eb0881bdeee` | Zero commits outside main; the approved Publications body is now reconciled by #1207. |
| `codex/qs-security-patch` | Local | `354aa99831c691ee74939a69efe8e75e74b066c3` | Its four-line patch pins `qs` 6.16.1; main already has the same override and lock entry through #1187, plus newer Playground fixes. |
| `codex/showpiece-review` | Local and origin | `f2cec03f2485d47806cfb245abbc4f9e670ca87f` | About, Photography and MØTLEYKRÜG bodies equal main (#1205); main's Contact has newer inquiry anchors/behavior (#1203). Main's generalized page-scope test contains the showpiece checks. |

Recovery refs use the existing prefixes:

```text
refs/archive/cleanup-20261111/local/<former-branch-name>
refs/archive/cleanup-20261111/remote/<former-branch-name>
```

All four new refs were read back against the exact tips. The `qs` checkpoint
commit is not an ancestor of main, so its local branch required explicit
deletion after verifying the patch and archiving the commit. The remote
showpiece deletion used a lease on its inspected tip. No default branch or
worktree was removed. The retained `codex/local-checkpoint-2026-10-02` points to
`eb385d3f7d8d6b28d152309261fa9ade0df7233c`; its unique note identifies
`.generated/` as owned state. That branch and the existing local files remain.

Together with the first pass, cleanup removed 15 pre-existing local branches
and nine remote branches, with six additional stale tracking refs pruned and
30 verified recovery refs. These counts exclude this session's temporary PR
branches. No disk-space recovery is claimed.

## HSTS decision packet: issue #767

Fresh logged-out GETs found no `Strict-Transport-Security` header on the apex
homepage, the www homepage redirect, either hostname's login response, or the
apex Aurora stylesheet. Both hosts passed certificate verification and served
the same Let's Encrypt certificate, covering apex and www, expiring December
26, 2026 at 08:15:26 UTC. Sampled HTTP requests to `/` and `/wp-login.php` on
both hosts redirected to HTTPS. This is sampled route evidence, not a proof
that every route or port supports HTTPS. Automatic renewal was not verified.

Public homepage responses still lacked `nosniff` and a referrer policy; login
retained its existing referrer policy. The stalled first-phase header rollout
therefore remains unproven. Enumeration protection and the prior keep-admin
decision are already complete.

**Recommendation for Kris's review:** separate HSTS from that first-phase
header rollout. Propose this exact header on HTTPS responses for `kriskrug.co`
and `www.kriskrug.co` at Pagely's gateway:

```http
Strict-Transport-Security: max-age=86400
```

Do not add `includeSubDomains` or `preload`. This recommendation does not
authorize a host change. It leaves MIME, framing and script policies unchanged.
HSTS changes future connection handling; a certificate failure can prevent
access, so working HTTPS and renewal coverage still matter.
[MDN's HSTS reference](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Strict-Transport-Security)
explains the browser policy and certificate consequences.

**Unsent Pagely request for approval:**

> Please prepare a standalone HSTS change for kriskrug.co and www.kriskrug.co:
> `Strict-Transport-Security: max-age=86400`, without includeSubDomains or
> preload, on HTTPS responses. Confirm automatic certificate renewal, the
> exact ARES rule, and coverage of cached HTML, www redirects, login, static
> assets and errors. Preserve existing headers and HTTP-to-HTTPS redirects.
> Supply the saved-rule recovery steps and cache behavior. Return the proposal
> for owner review before changing production. No other host setting or paid
> service is requested.

Pagely documents [response headers at the ARES gateway](https://support.pagely.com/hc/en-us/articles/360056097471-Setting-Response-Headers-in-Atomic)
and [HSTS support requests](https://support.pagely.com/hc/en-us/articles/360000864312-Setting-Up-HSTS-HTTP-Strict-Transport-Security).
An authenticated account review must still establish this application's
actual rule controls and coverage. A WordPress-only snippet would not establish
coverage for the host redirect or cached/static responses.

After a separately approved apply, verify apex, www redirect, login and the
stylesheet over HTTPS, including confirmed cold/warm cache responses where
available; retain the HTTP redirects. Record observed coverage and check
TLS/redirect/header health over the next seven days before proposing a longer
duration. No monitor or schedule was installed in this pass.

Recovery requires serving `max-age=0` over working HTTPS on both hosts and
refreshing the affected cache. A browser must receive that response to clear
its policy early; otherwise the previous policy persists until expiry. Merely
removing the header does not immediately undo it. See the
[HSTS expiration rules](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Strict-Transport-Security#expiration).

## Futureproof reciprocal link: issue #1165

The verified candidate is [Futureproof Festival of AI 2026: What We Built Together](https://bc-ai.ca/news/the-robots-in-the-lobby),
published November 4 and updated November 6, by Kris. It is a photo/community
recap with a 2027 outlook and already links to
[Futureproof: Year One](https://kriskrug.co/2026/11/01/futureproof-2026-year-one/).
Kris still decides whether it satisfies the original community-synthesis
dependency; the distinct institutional implications contract should not be
silently rewritten.

The slug lookup uniquely resolved to published post **12934**. Its fresh raw
body equals the tracked `content/drafts/futureproof-2026-editorial/post.html`,
with SHA-256 `a972362c4c0a22e74edf70dfe73cefb1e60f72da800f9de37701652c42ac9fc3`.
It does not yet contain the target URL. The prepared change adds this clause
between the proceedings link and “or revisit” in its closing Explore sentence:

> read [BC + AI's recap of what we built together](https://bc-ai.ca/news/the-robots-in-the-lobby),

The rest of that paragraph, including photo/presentation credits, is preserved.
The proposed body hash is
`f93a859e4ce457e99d1699db7c99b05c34cb2500eacd684c49d87a34d615cf59`.
The before snapshot and exact unified diff are private review artifacts, not
an applied release. Approval was requested in the active chat. Before any
approved write, recheck slug/ID and the before hash, snapshot current state,
apply once, and verify authenticated/public readback plus source reconciliation.

## Events cadence and public-source sweep: issue #1102

Claude's November 11 read-only inventory found no Events heartbeat among Codex
automations, Claude scheduled tasks or launchd, and no evidence of the expected
November 2/9 runs. Treat the historical Monday 09:00 America/Vancouver cadence
as not running. Decide whether to reinstate the existing propose-only contract
or retain manual sweeps before installing anything.

The bounded public-source sweep found no confirmed edit: catalog 87 entries;
public counters 84 past rooms, 33 meetup editions and 41 frames. November 23
AMPA and November 25 Vancouver AI remain upcoming; Prompt Victoria is past.
Both Google Calendar connectors were unavailable in that audit. This is a
public-source no-change result, not complete calendar coverage.

The [December 16 Vancouver AI page](https://bc-ai.ca/events/2026-12-16-vancouver-ai-community-meetup)
confirms the date and H.R. MacMillan Space Centre but does not name Kris as host
or speaker. Independent public readback confirmed that gap. Hold the candidate
until his role is confirmed. No catalog, calendar or WordPress mutation was
made; no private-message monitoring or automation was created. The
[maintenance contract](../EVENTS-MAINTENANCE.md) now records these limits.

## Evidence and verification

Private readbacks, the branch receipt and the one-paragraph proposal are under
`.generated/current-state/repo-maintenance-2026-11-11/followthrough/`.
The supplied Claude packet remains in its original scratchpad; it was not
deleted or copied into the public repository. Local docs-truth, PHP syntax
(56 files) and WordPress coding standards passed. All 96 checked relative
Markdown links resolve; all 107 original untracked files retain their hashes.
Independent documentation review approved the change after making recurring
schedule verification conditional on choosing that cadence. Required CI is
recorded on the follow-through PR.
