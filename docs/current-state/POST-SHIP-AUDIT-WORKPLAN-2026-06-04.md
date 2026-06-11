# Post-Ship Audit + Workplan - 2026-06-04

**STATUS (2026-06-11):** Partially superseded. Steps referencing **#149** (Local WP QA), **#150** (article module tuning), and **#126** (Work OG) are **closed** with evidence. PRs #205, #210, and #212 are merged; open PRs are `0`; open issues are `63`, including the gated June 11 follow-ups #206-#208. GSAP/CDN production drift remains tracked by #189/#204, Rafiki/content queue closeout is tracked by #206-#208, and #62 is parked with the Luma spike result from #177/#212. Reconcile counts with `make status-readonly` before executing.

## Shipped Today

- PR #148 merged: `content: polish Work page proof metadata`.
- Issue #68 closed with live WordPress REST/public proof.
- PR #147 merged: `docs: record Aurora 1.3.10 deploy workplan`.
- Open PR queue is now `0`.
- `main` is current at `cadbc7e`.

## Audit Snapshot

Sources:

- `docs/current-state/reports/morning-truth-20260604-062927Z.md`
- `gh pr list --state open`
- `gh issue list --state open --limit 150`
- public fetches for Work metadata
- local-only draft queue audit

Current state:

- WordPress smoke: `6.9.4`, `0` failures, `0` warnings.
- WordPress draft counts from 2026-06-11 `make status-readonly`: `0` future posts, `74` draft posts, `5` draft pages.
- Local draft package audit: `51` local packages, `6` zero-word or missing-slug packages, `1` package with TODOs (`sovereign-ai-for-whom`).
- Issue queue from 2026-06-11 20:40 UTC live GitHub readback: `63` open issues, `29` priority-high, `6` Track B, `7` Aurora v2, `6` swarm-ready, `15` swarm-parked, `21` needs-human-review.
- Work page OG image is now nonblank in public HTML for `/recent-projects-include/` and `/work/`, but issue #126 still asks for social-share debugger validation.

## Ready For KK

- #95, media appearances draft: needs human editorial/backlink review before any publish path.
- #128, Jetpack contact forms: needs routing/notification decision and likely wp-admin confirmation.
- #75, publishing safety umbrella: keep open until the venv, draft queue, secret-scan, and sign-off rules are boring again.
- #126, Work page OG image: public HTML is fixed; either run a social-share debugger check or accept crawler-visible HTML as enough and close with evidence.

## Agent-Fixable

1. #149, restore Local WP QA path.
   - Rebuild/document `127.0.0.1:10003` and `kriskrug-local.local`.
   - Done when Track B browser QA can use real Local WP before static fixtures.

2. Draft audit tooling repair.
   - Recreate `scripts/notion-to-wp/.venv` and install `requirements.txt`.
   - Confirm `make draft-queue-audit FORMAT=json` works authenticated, not only `--local-only`.

3. #127, dedicated responsive QA.
   - Verify `/blog/`, latest post, and one media-heavy post at desktop/tablet/mobile widths.
   - Capture screenshots, focus checks, reduced-motion behavior, article map, and no horizontal overflow.

4. #125, Jetpack Boost/performance follow-up.
   - Confirm critical CSS freshness after the 1.3.10 deploy.
   - Decide whether the `KK Aurora: GSAP or ScrollTrigger not loaded` console warning is expected optional infrastructure or cleanup.

5. #150, tune real article modules.
   - Review real post bodies with Article Modules vocabulary.
   - Patch only spacing/contrast/rhythm problems exposed by actual WP output.

6. Track A draft queue packet.
   - Start with #95 or `the-75-percent-rule-ai-art-adjacent-work`.
   - Use authenticated slug/status checks, rollback notes, preview QA, and no publish without explicit approval.

## Stale Or Superseded Candidates

- #126: likely closable after social debugger validation.
- #13, #14, #15: Work/homepage now contain BC+AI, Indigenomics.ai, and The Upgrade AI proof, but the original standalone-section asks should get evidence comments before closure.
- #36: Work metadata is now handled; re-scope remaining meta-description work to pages still failing current public/source checks.
- Broad platform/marketing/archive issues (#49-#64): keep parked until each has an owner, source pack, and deploy path.

## Blocked / Watch

- Authenticated draft queue audit is blocked locally because `scripts/notion-to-wp/.venv/bin/python` is missing and system `python3` lacks `python-dotenv`.
- Local `aurora/v2` remains divergent and the locked agent worktree reports `theme/kk-aurora.zip` dirty in morning-truth; do not use it as source of truth without a separate Track B reconciliation pass.
- Morning-truth still reports homepage reveal safety net as `no` and GSAP/ScrollTrigger CDN as `yes`; keep this visible during Track B QA.

## Next Default Sequence

1. Restore local execution trust: venv + authenticated draft audit, then Local WP QA (#149).
2. Close or explicitly park #126 after social-share debugger validation.
3. Run the Aurora post-deploy QA packet: #127, #125, #150.
4. Move one Track A draft through review/prepublish gates, likely #95 or `the-75-percent-rule-ai-art-adjacent-work`.
5. Add evidence comments to stale proof-section issues (#13, #14, #15, #36) so future agents stop rediscovering already-live proof.

## Restart Commands

```bash
git fetch --prune
git status --short --branch
gh pr list --state open --limit 50
gh issue list --state open --limit 150
make morning-truth
python3 scripts/notion-to-wp/draft_queue_audit.py --local-only --format markdown
```

After venv repair:

```bash
scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/draft_queue_audit.py --format markdown
```
