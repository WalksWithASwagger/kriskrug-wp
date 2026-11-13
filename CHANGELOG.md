# Changelog

Notable changes to this operations hub. Aurora version history and deploy
markers stay in [`theme/kk-aurora/CHANGELOG.md`](theme/kk-aurora/CHANGELOG.md).
This file is the repo-wide log.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Newest window first. Sections below are grouped by area because this repo
ships content, theme, tooling, CI, and docs in the same tree.

This log lists **merged pull requests only**, one line per PR, using the PR
title. Direct pushes to `main` are not listed.

## How this file is kept

Each weekly roadmap reset runs `make changelog SINCE=YYYY-MM-DD` (the day after
the end date of the newest section below; check for PRs merged late on that day) and the output becomes a new dated section. The script
is `scripts/changelog_from_prs.py`. It groups by title prefix, then by changed
paths, and does not add descriptions beyond the PR title.

## [Unreleased]

Nothing yet. Merges after the newest dated section below land here until the
next weekly refresh.

## [2026-09-29 to 2026-11-12]

Generated 2026-11-12 with `make changelog SINCE=2026-09-29`: **122** merged PRs
(earliest `2026-09-29T15:35:38Z`). Anything merged after that run is picked up
by the next weekly refresh.

### Content

- Add combined Gorgeous Ghost draft package (#771, #1016) (#1270)
- Owned-distribution record for the Canada Now article (#1176) (#1271)
- Add TIDEPOOL.ING and Little Supercluster to the Work index (#1281)
- Commit the public Downtown Eastside package files (#1276)
- Add the Dec 16 Vancouver AI meetup to the events catalog (#1266)
- Mark the superseded #480 payload pack do-not-apply (#1252)
- Mark Prompt Victoria past in the Events catalog (#1262)
- Publish the approved Futureproof reciprocal link (#1210)
- Reconcile the approved Publications redesign (#1207)
- Reconcile live About, Photography, and MØTLEYKRÜG (#1205)
- Preserve Speaking and Services icons in WordPress (#1204)
- Connect Services offers to Contact prompts (#1203)
- Lead Work with three sourced case studies (#1202)
- Bring stage proof and booking to Speaking (#1201)
- Add the 2021 Galiano summer program to Events (#1193)
- Sync the live Testimonials redesign (#1192)
- Add the first 2023 and 2022 Events archive entries (#1190)
- Keep the live Events redesign in the catalog renderer (#1189)
- Record Canada Now episode source (#1184)
- Link Futureproof: Year One to the proceedings (#1186)
- Add Futureproof recap and gallery links (#1185)
- Add IIA debate to the events archive (#1183)
- Sync published Futureproof feature and release receipt (#1170)
- Revise Futureproof recap as Year One (#1169)
- Prepare Futureproof 2026 personal essay (#1167)
- Connect Events records to recaps, photos and video (#1153)
- Keep Events confirmation explicit during catalog enrichment (#1150)
- Ship three brand-navigation links from AI articles (#1149)
- Repair Work card readability and route Subscribe to KRÜG (#1144)
- Land ALL IN review package and readiness closeout (#1141)
- Date-based Next up roll-off and Futureproof tickets link (#1134)
- Point llms.txt meetup link at /events/ (#1133)
- Mark the September 30 meetup as past to restore the catalog gate (#1122)
- Meetup #32, #33 label, Prompt Victoria, Capilano recap (#1099) (#1108)

### Theme

- Aurora 1.7.2 release candidate (archive social meta, conditional marquee.js, changelog markers) (#1261)
- Preserve approved blog layout above inline WordPress defaults (#1173)
- Redesign Writing for scannable posts and quieter reading (#1172)
- Pair responsive header grid areas and restore mobile tap targets (#1171)
- Fix social attribution and personal newsletter destinations (#1142)
- Point sitewide chrome and the page sitemap at final URLs (#1132)
- Restore the broken BC+AI card and Work social image (#1118)
- Refresh approved festival copy and footer YouTube link (#1109)

### Publisher and tooling

- Clear whole-tree Ruff findings and exclude scripts/archive from the changed-file gate (#1280)
- Add read-only page payload parity check (#1267)
- Run the Notion connector's guards before any upload and fail on readback mismatch (#1259)
- Compare Luma events against real Unix time in sidebar-promos sync (#1251)
- Add JSON_HEX_TAG and JSON_HEX_AMP to the JSON-LD emitters (#1256)
- Route the audit credential readers through common.load_env (#1264)
- Archive two spent publishers and fail Context Creators on a failed check (#1263)
- Route every publisher slug lookup through one fail-closed helper (#1257)
- Declare env vars the scripts read in .env.schema (#1255)
- Make the docs gate require the current roadmap (#1249)
- Stop WPClient.get_all at the last page instead of one past it (#1260)
- Report transport failures in the public smoke check (#1188)
- Refresh WordPress startup baseline to 7.0.8 (#1166)
- Report squash-merged branches with exact PR/SHA evidence (#1113)
- Retain startup smoke failures and align snapshot defaults (#1092)
- Load notion-to-wp through Varlock (#1091)

### CI and tests

- Harden the workflow and add large-file and PHP compatibility gates (#1272)
- Retire the swarm-era agent definitions, state records and disabled workflows (#1265)
- Make every existing test run in CI (#1258)
- Patch Playground isomorphic-git development dependency (#1206)
- Update qs security override to 6.16.1 (#1187)
- Bump @wp-playground/cli from 3.1.61 to 3.1.62 in the npm-minor-patch group (#1180)
- Update pytest requirement from >=9.1.1 to >=9.2.0 (#1179)
- Bump github/codeql-action/upload-sarif from 4.39.1 to 4.39.2 in the actions-minor-patch group (#1178)
- Bump the actions-minor-patch group with 2 updates (#1164)
- Bump @wp-playground/cli from 3.1.60 to 3.1.61 in the npm-minor-patch group (#1163)
- Update ruff requirement from >=0.17.1 to >=0.17.3 (#1162)
- Make KRÜG signup privacy fixture deterministic (#1152)
- Synchronize Events record, counters and documentation links (#1151)
- Bump the npm-minor-patch group with 2 updates (#1138)
- Bump github/codeql-action/upload-sarif from 4.38.3 to 4.39.0 in the actions-minor-patch group (#1139)
- Update ruff requirement from >=0.17.0 to >=0.17.1 (#1137)
- Bump the actions-minor-patch group with 4 updates (#1128)
- Bump the npm-minor-patch group with 2 updates (#1127)
- Update ruff requirement from >=0.16.10 to >=0.17.0 (#1126)
- Bump proxy-addr from 2.0.7 to 2.0.8 (#1124)
- Update python-dotenv requirement from >=1.2.3 to >=1.2.4 in /scripts/notion-to-wp (#1119)
- Bump @wp-playground/cli from 3.1.56 to 3.1.57 in the npm-minor-patch group (#1123)
- Update ruff requirement from >=0.16.9 to >=0.16.10 (#1120)
- Update python-dotenv requirement from >=1.2.3 to >=1.2.4 (#1121)
- Bump @wp-playground/cli from 3.1.55 to 3.1.56 in the npm-minor-patch group (#1116)
- Bump @wp-playground/cli from 3.1.52 to 3.1.55 in the npm-minor-patch group (#1095)
- Bump github/codeql-action/upload-sarif from 4.38.1 to 4.38.2 in the actions-minor-patch group (#1097)
- Update ruff requirement from >=0.16.8 to >=0.16.9 (#1096)
- Add weekly npm browser-toolchain updates (#1093)

### Docs and ops

- Cut the November 12 roadmap and repoint the front doors (#1284)
- Define merge lanes for scripts, tests, Makefile, CI and dependency PRs (#1269)
- Drop the local design-proofs path from the Writing review (#1282)
- Record the Events cadence decision and the Dec 16 ruling (#1268)
- Redact legacy Cloudways host details (#1247)
- Guard make issues against unconfirmed and duplicate creation (#1250)
- Reconcile make seo-audit guidance and Makefile help text (#1248)
- Replace the swarm-era PR template with the repo's real gates (#1254)
- Repoint front doors away from archived and retired guidance (#1253)
- Record remaining maintenance decisions and cleanup (#1209)
- Reconcile November roadmap and repository state (#1208)
- Record the Aurora rollback archive location (#1177)
- Record November work plan and September audit closeout (#1175)
- Record the completed Aurora 1.7.1 Writing release (#1174)
- Prepare host hardening and revoked-history review (#1168)
- Close Article 3 correction release (#1161)
- Record Article 3 source audio audit (#1160)
- Reconcile Article 3 review with the current publication (#1159)
- Publish the approved November meetup and ALL IN Events entries (#1158)
- Record the pre-Futureproof shipping and remaining decisions (#1157)
- Patch the practice test server body-parser dependency (#1156)
- Prepare the first-practice release and five-person study packet (#1155)
- Establish the propose-only Events maintenance loop (#1154)
- Record live KRÜG completed-signup measurement (#1148)
- Prepare completed KRÜG signup measurement and record GA4 setup (#1147)
- Fix Publications overflow and close site-readiness checks (#1146)
- Record live Person and Speaking schema release (#1145)
- Reconcile page imagery and editorial readiness before Futureproof (#1143)
- Align startup checks with current main and record site readiness (#1140)
- Close out Brands for Better photo update (#1136)
- Reconcile Snippet 5 preflight with KK's Sep 28 approval (#1135)
- Conversion-path inventory and success-only event packet (#1110)
- Reconcile workflow, backup and practice-test guidance (#1112)
- Snippet 5 save preflight for Person + Speaking videos (#1111)
- Add the September 28 weekly workplan and maintenance receipt (#1094)

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
- Closed out the issue 4 media-gate docs (#934). Issue #4 was open when this window was cut and is closed now.
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
- Landed the 2026-09-20 P1 deploy-safety fixes named in #1034-#1037 (#1079). Those four issues were open when this window was cut and are closed now.
- Archived the Publications theBreaker deploy rollback evidence (#1020)
- Deploy receipts for the six approved live lanes (#948)

### Known gaps

- Direct-to-`main` commits have no merged PR and are omitted on purpose.
- No GitHub Releases exist. This changelog is not a release.
