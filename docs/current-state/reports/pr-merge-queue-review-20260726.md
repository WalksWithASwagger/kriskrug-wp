# PR merge-queue review — 2026-07-26

**Reviewer:** Cloud orchestrator (cannot approve/merge — GitHub App token blocked).  
**User ask:** review and merge PRs.  
**Blocker:** `gh pr review --approve` → *Resource not accessible by integration*. Secrets `GH_TOKEN` / `AGENT_MERGE_TOKEN` unset. Direct merge forbidden by branch protection (`REVIEW_REQUIRED`).

## Verdict summary

| Bucket | Count | Action |
|---|---:|---|
| **MERGE NOW (human)** | 1 | #506 unlocks agent merge path |
| **MERGE SAFE (CI green, no theme)** | ~33 | Squash after #506 + secrets, or merge manually |
| **HOLD** | 2 | #493 pixel gate; #505 theme + css-ratchet red |

All listed SAFE PRs were marked **ready for review** (undrafted) in this pass.

## 1) Merge first (human account)

| PR | Why |
|---|---|
| [#506](https://github.com/WalksWithASwagger/kriskrug-wp/pull/506) | Adds `agent-safe-merge` workflow + docs. Chicken/egg until your account merges it. Then set `AGENT_MERGE_TOKEN` (Actions) + `GH_TOKEN` (Cursor Cloud) and create label `agent-safe-merge`. |

## 2) Safe squash queue (recommended order)

### Futureproof Track A (same draft folder — order matters)
1. #501 speakers  
2. #503 assets  
3. #518 story  
4. #535 WP-draft verify package (no live create)

### Lane B drafts / pages
5. #504 About audit  
6. #507 Services  
7. #508 Speaking page  
8. #509–#513 home-section packages (#509 logos, #510 Join BC, #511 What People Say, #512 stages, #513 Creative Labs)

### Round 2 packets
9. #515 undesigned pages  
10. #516 a11y statement  
11. #517 SEO hubs  
12. #519 contact CTA  
13. #520 land acknowledgment  
14. #521 YCDD measure  
15. #522 stylesheet Path B brief  
16. #523 About/bio payload  
17. #524 alt-text inventory  

### Round 3 probes / checklists
18. #526 GSC sitemap  
19. #527 taxonomy sitemap plan  
20. #528 media appearances (already published — close #95 after)  
21. #529 fold #48→#288  
22. #530 publisher batch prep  
23. #531 post-Jetpack QA  
24. #532 Jetpack delete prep  
25. #533 WCAG smoke  
26. #534 perf/Boost plan  
27. #502 reclaim list (#369)

### Swarm closeouts
28. #514 round-1  
29. #525 round-2  
30. #536 round-3  

## 3) HOLD — do not merge yet

| PR | Reason |
|---|---|
| [#493](https://github.com/WalksWithASwagger/kriskrug-wp/pull/493) | Theme Aurora 1.5.0. Conflicts/css-ratchet cleared earlier; **pixel gate still owed** (`/opt/pw-browsers` missing in Cloud). |
| [#505](https://github.com/WalksWithASwagger/kriskrug-wp/pull/505) | Theme newsletter rewrite. **CI red** (`css-ratchet` + `summary`). Rebaseline or fix before merge. |

## 4) After merges (human)

- Close #48 using paste comment from #529; close or retarget #95 per #528  
- Comment Path B on #423 from #522  
- Attach WP creds → dry-run #535 path for Futureproof draft create  
- Pixel harness env → finish #493  

## Policy

Repo `allow_auto_merge=false` stays. Agent-safe-merge is opt-in and refuses `theme/`, `plugins/`, `inc/`.
