# Master Plan: Truth, Reclaim, Then Lanes — 2026-07-30

**Status:** active plan of record for ops hygiene + sequenced product lanes.
**Lane:** Docs / ops first; then Track A or Track B — never interleaved in one commit.
**Does not authorize** live WordPress writes, theme deploys, or history rewrite.

Day runbook: [`WORK-PLAN-2026-08-23.md`](WORK-PLAN-2026-08-23.md). Declared snapshot: [`CURRENT-STATE-2026-07-30.md`](CURRENT-STATE-2026-07-30.md).

## Goal

Make this repo trustworthy again so agents and humans stop navigating by stale work plans.

## Success criteria

- One declared snapshot + one active work plan; older plans bannered historical or archived
- `AGENTS.md` + [`README.md`](README.md) point at that pair
- #549 archive pass moved May–June plan crust out of the front door
- #369 first wave (buckets **A+D only**, ~212 MB) deleted in a dedicated reclaim PR
- Issue labels match reality (#475 unblocked; #476+ correctly blocked; #423 no longer a fake DECISION)
- Product work continues on two clear lanes without waiting on `.git` history rewrite

**Reclaim first wave locked:** A+D only (published draft `images/` + report screenshots). Buckets B/C/E and Phase C `filter-repo` stay deferred.

## Phases

### Phase 0 — Truth reset

- Write this file + CURRENT-STATE + WORK-PLAN 2026-07-30
- Retarget AGENTS.md, README, Makefile `WORK_PLAN_DEFAULT`, docs/INDEX
- Banner-demote WORK-PLAN 07-16 / 07-19 / 07-26 (and peers)
- Create, review, and commit a `make morning-truth-checkpoint` report for this durable truth reset
- Fix obvious post-merge lies in active docs (e.g. CHANGELOG 1.5.0 “still unmerged”)

### Phase 1 — Docs archive (#549)

- `git mv` superseded May–June `docs/current-state/*.md` into `archive/`
- Keep durable process docs at top level (TWO-TRACK-MODEL, incident, Varlock, SEO runbooks, visual baseline, stylesheet rebuild, reclaim runbooks, newest front door)
- Refresh README index

### Phase 2 — Binary reclaim (#369 A+D)

Follow [`reports/repo-bloat-318-next-steps-20260726.md`](reports/repo-bloat-318-next-steps-20260726.md):

- Bucket D: report screenshots under `docs/current-state/reports/screenshots/` + listed root PNGs
- Bucket A: published-post `content/drafts/**/images/` from the §1.1 table; keep `.md`; add ASSETS stub
- No B/C/E; no `filter-repo`; no force-push; do not touch untracked in-flight drafts

### Phase 3 — Issue / branch hygiene

- Strip stale `blocked` from closed #474; keep #476–#481 blocked until prior step lands
- Retitle #423 from DECISION shell to Path A epic (decision already recorded)
- Label #369 (`tech-debt`, ops-relevant labels available)
- Dependabot #556 on its own merit
- Delete stale remotes: `codex/415-homepage-trust-identity`, `codex/approved-community-photo-20260720`, `codex/publications-editorial-archive`, `cursor/494-pixel-gate` (unless KK flags one to keep)

**2026-07-30 execution:** stale remotes deleted (including `cursor/494-pixel-gate-f196`). Issue edit/label API blocked for Cloud App token — paste-ready commands in [`reports/phase-3-hygiene-20260730.md`](reports/phase-3-hygiene-20260730.md).

### Phase 4 — Product lanes

Do **not** interleave theme visual deltas with content publishes.

**Track A:** Prefer `scripts/notion-to-wp/create_local_wp_draft.py` over new `publish_*.py` one-offs. Dry-run → slug-match → publish. Futureproof #496–#500 draft-only. Stop treating `FIX_QUEUE.md` as the day backlog.

**Track B:** After content batch quiet — #475 (1.5.1) → #476 (1.5.2) → #477/#479/#478/#480/#481, one PR each, pixel-gated. Plan of record: [`AURORA-STYLESHEET-REBUILD-PLAN.md`](AURORA-STYLESHEET-REBUILD-PLAN.md).

## Explicitly deferred

- `.git` history rewrite / Phase C (#318)
- Full `fixes/` live reconciliation rewrite
- Page redesign cluster #416–#420 as product decisions
- Local disk cleanup of gitignored `photos-raw/`

## Approval gates

| Gate | Owner |
|---|---|
| Phase 0–1 docs PRs | Agent draft; KK merge (or agent-safe-merge if labeled) |
| #369 A+D deletes | Locked by this plan; execute in dedicated reclaim PR |
| Live theme uploads / pixel gate | KK for each #475+ deploy |
| Content publish / schedule | KK per post |
