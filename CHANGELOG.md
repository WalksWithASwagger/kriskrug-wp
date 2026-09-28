# Changelog

Notable changes to this operations hub. Aurora version history and deploy
markers stay in [`theme/kk-aurora/CHANGELOG.md`](theme/kk-aurora/CHANGELOG.md).
This file is the repo-wide log.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Newest window first. Sections below are grouped by work theme because this
repo ships content, theme, docs, and CI in the same tree.

This cut lists **merged pull requests only**. Built 2026-09-28 from:

```
gh pr list --repo WalksWithASwagger/kriskrug-wp --state merged --limit 200 --search "merged:>=2026-08-29"
```

`gh` returned **85** merged PRs (earliest `2026-08-29T17:15:43Z`, latest
`2026-09-28T05:34:55Z`). A Sep 27 audit counted 111 using a window that
started 2026-08-28. Repeating that older start date on 2026-09-28 returns
112, because #1085 and #1086 landed after the audit. This file uses the
last-30-days window from today.

Direct pushes to `main` are not listed. If a fact is not on the PR title
or a receipt I could read, it is marked **TODO for KK**.

## [Unreleased]

## [2026-08-29 to 2026-09-28]

### Content

- Landed the ALL IN Montréal post 2 package (already live as post 12788) (#1078)
- Synced speaking meetup poster alt from the homepage (#1045)
- ALL IN FAQ magnets for #1028 (paste-ready, not live) (#1044)
- Paste-ready ALL IN cross-link matrix (#1031, #1030)
- theBreaker 460 outreach and social packet (#1021)
- Connected the North House example to a workflow enquiry (#979)
- theBreaker 460 recap (published) plus a Publications clipping (#998)
- Prepared the Open Studio context-brief teaching packet (#991)
- Published the North House recap as post 12744 (#972)
- Applied KK's publish rulings to the North House recap (#971)
- North House recap draft, event photo, and events entry refresh (#957)
- Executed the #745 draft-queue triage (#956)
- Recorded the #735 brand canon ruling (#949)
- Built Press Kit v2 payload, rights clearance, and contract tests (#946)
- Generated event artboards and editorial marks (#943)
- Added the North House cohort appearance (#940)
- Recorded issue #829 live closeout (#937)

### Events

- Rebuilt `/events/` as a full-bleed contact sheet (#1022)
- Added the TRECSA World Tourism Day panel, Sep 25 (#1014, #1013)

### SEO

- Consolidated the Kris Krüg Person entity in the schema snippet (#1082)
- #274 sitemap follow-through receipt (GSC last-read still blocked) (#1050)
- Added the #1025 crawl-waste robots and noindex policy (#1047)
- Track A crawl hygiene for #1025 (soft draft) (#1029)
- #331: closed the pre-deploy evidence gate and dropped dead code from the v2 snippet (#941)
- Prepared a narrow user sitemap guard (#932)

### Theme

- Added The Sky Smoked Back to the Creative AI network (#1043). Public
  `style.css` readback on 2026-09-28 still reports Aurora `1.6.12` in
  parity with `main`.
- Canonical Kris Krüg spelling: theme source mirror plus live sweep evidence (#999)
- Aurora 1.6.11: dropped the redundant event CSS and shipped `/events/` (#970)
- Aurora 1.6.10: event artboards and editorial marks CSS (#958)
- Added the browser-only context brief proof (#993)

### Documentation

- Pointed the README Events link at the live BC + AI Luma calendar (#1086)
- Added the 2026-09-21 current-state snapshot and retired the stale July pointer (#1076)
- Split agent runtime guidance (#1075)
- Inventoried legacy WordPress writers as rollback-only (#1074, #1068)
- Inventoried unreferenced legacy helpers and the superseded mobile QA plan (#1073)
- Wave 6b p2: D28 hub-plan banner plus D29 INDEX labels (#1071, #1070)
- Wave 5 stale docs/code scout, find-only (#1064)
- Wave 4b p2: bannered closed-hub drafts and the audits pointer (#1062, #1061)
- Wave 4 p1: #331 apply honesty plus apply-pack test drift (#1060, #1059)
- Wave 3 stale docs/code scout, find-only (#1058)
- Wave 2c p2: historical banners and safe script deletes (#1056)
- Bannered closed SEO apply packets so agents do not re-apply (#1054, #1053)
- Wave 1 stale docs/code scout, find-only (#1052)
- Closed the AI Second Brain search-decline packet (#1049, #994)
- Closed the Events search click-through packet (#1048, #995)
- Added the per-article owned-distribution and backlink checklist (#1046)
- Refreshed active truth and hardened #830 drift checks (#1012)
- Preserved the approved Open Studio plan and gates (#990)
- Triaged GSC 404 and canonical errors (#1011, #997)
- Diagnosed Events search click-through (#1010, #995)
- Verified Google sitemap readback after #331 (#1009, #274)
- Triaged unindexed primary articles and prepared a five-URL recovery batch (#1008, #996)
- Inventoried public `backup/` / `raw/` captures for scrub (#1007, #1003)
- XML-RPC constrain decision packet (prep only) (#1006)
- Phase-1 nosniff + Referrer-Policy apply runbook (#1005, #1001)
- Diagnosed AI Second Brain search decline (#1000, #994)
- Verified the favicon gap and prepared a native release packet (#987)
- Verified the INP audit claim with measured interaction evidence (#992)
- Refreshed the security header decision packet (#989, #709)
- Prepared the branded booking handoff (#988, #984)
- Draft-queue triage sheet and 2026-09-03 decision sheet (#947)
- Repaired repository-wide relative links (#945)
- Refreshed authority hub pack status (#939)
- Corrected authority hub run order (#938)
- Corrected repository identity and access truth (#935)
- Closed out issue 4 media gate (#934)
- Corrected testimonials issue status (#933)

### CI and dependencies

- Granted `security-events` and stopped the SARIF upload from blocking `main` (#1085)
- Ran the full gate on direct pushes to `main` (#1083)
- Made the Ruff gate assertion version-agnostic (#1019)
- Added the changed-file Ruff ratchet (#936)
- Deleted the uncalled reusable-wordpress-validation workflow (#944)
- Retired the inert swarm merge helper (#1072)
- Retired the repo-local workflow skill (#975)
- Ruff requirement bumps: `>=0.15.16` to `>=0.16.5` (#973), then `>=0.16.6` (#1017), `>=0.16.7` (#1032), `>=0.16.8` (#1080)
- `github/codeql-action/upload-sarif` bumps: 4.37.8 to 4.37.9 (#974), 4.38.0 (#1033), 4.38.1 (#1081)

### Ops and safety

- Archived the `/events/` page 2250 deploy rollback snapshot (#1084)
- Closed the 2026-09-20 P1 deploy-safety findings (#1079, #1034, #1035, #1036, #1037)
- Archived the Publications theBreaker deploy rollback evidence (#1020)
- Deploy receipts for the six approved live lanes (#948)

### Known gaps (TODO for KK)

- Direct-to-`main` commits in this window have no merged PR and are omitted on purpose. **TODO for KK:** say whether those should be backfilled by commit SHA.
- Authenticated draft-queue counts were unavailable in the 2026-09-28 `make status-readonly` session (no WordPress credentials). Last dated authenticated read on file is still 2026-08-29. **TODO for KK:** refresh those numbers before treating them as current.
- Public smoke on 2026-09-28 observed WordPress `7.0.6`. That is not a merged PR. **TODO for KK:** confirm whether the declared snapshot should move off `7.0.5` / `7.0.4`.
- No GitHub Releases exist for this window. This changelog is not a release.
