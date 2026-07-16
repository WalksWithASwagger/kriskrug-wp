# #363 Publisher batch orchestration prep

**Captured:** `2026-07-16T00:43:21Z`  
**Primary:** #339  
**Depends on:** #362 green on live Aurora **1.3.40**

## Stop conditions (all currently true)

1. Live Aurora is still **1.3.37** (public `style.css`) — Phase 1 not done.
2. Cloud secrets `WP_USER` / `WP_APP_PASSWORD` are **absent**.
3. #339 checklist boxes are **unchecked** in the issue body.
4. #339 deploy checkbox still names the obsolete **1.3.39** zip + hashes from 2026-07-13.

## Critical: refresh #339 before any live write

Do **not** treat a tick of the current first checkbox as approval to upload 1.3.39.

Required KK update to #339 (human edit of the issue):

- Replace deploy artifact with `kk-aurora-seo-search-titles-1.3.40-1.3.40-20260716.zip`
- SHA-256 `8e1c1321f94b1caf5d899697f5ddef6256d1274c74a67cd64d84645b1c24fad5`
- Rollback `kk-aurora-live-1.3.37-1.3.37-20260716.zip` / `cfa1307e68db77c9bd8b9423fbd35be984a1d98b6d4f6829b3a540b701a1d1b4`
- Keep all content SEO checkboxes; only the theme zip line changes

Until that edit + ticks exist, agents stop.

## Execution order (when unlocked)

1. Confirm live `style.css` Version `1.3.40`.
2. Quote #339 checklist as approved (exact wording) in the session log.
3. Refresh target IDs/slugs/`modified`; stop on stale guards.
4. Snapshot under `backup/<timestamp>-july-publisher/`.
5. Apply SEO fields for posts **35** and **8802**, then body-only patches in order: #249 → #328 → #335 → #336 → #342.
6. Authenticated + anonymous readback; schedule measurement windows.
7. Update source issues; do **not** burn GSC indexing quota in-session.

## Repo readiness (already green)

| Packet | Files | Unit tests |
|---|---|---|
| #249 | `fixes/issue-249-*` | `test_issue_249_seo_handoff` |
| #328 | `fixes/issue-328-*` | `test_issue_328_seo_handoff` |
| #335 | `fixes/issue-335-*` | `test_issue_335_lotr_seo_handoff` |
| #336 | `fixes/issue-336-*` | `test_issue_336_ai_second_brain_seo_handoff` |
| #342 | `fixes/issue-342-*` | `test_issue_342_both_hands_full_link_handoff` |
| #351 lineage | handoff + package | `test_issue_351_aurora_release` |

`make verify` passed in the orchestra session (2026-07-16).

## Out of scope

#331 archive indexability, remaining #353 body-H1 routes, #316 schema, #345 blogname.
