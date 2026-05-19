# Next Round Work - 2026-05-19

Use this as the next-session command sheet after the GitHub queue sweep, Track A prep swarm, and keynote authority-page polish.

## Current Snapshot

- Track A branch: `main`.
- Track B branch: `aurora/v2`.
- Aurora redesign PR: `#77`, draft, base `aurora/v2`, clean but not production-ready.
- Sidebar promos PR: `#73`, base `main`, parked because it is production-adjacent plugin work and mergeability currently reports `DIRTY`.
- Queue sweep correction PR `#78` merged to `main` as `b292fd9`.
- Track A prep PR `#79` merged to `main` as `8285831`.
- Keynote authority-page commits were rebased on top of current `origin/main` before this closeout:
  - `ca332f7 content: add horizons speaking proof`
  - `793f364 content: polish authority page IA`
- Speaking authority post packages landed in `6dd220e content: add speaking post packages`.

## What Just Landed

### GitHub Queue And Issue Prep

- `docs/current-state/GITHUB-QUEUE-SWEEP-2026-05-18.md` records the branch and PR decisions.
- `docs/current-state/INTERNAL-LINKING-STRATEGY-2026-05-18.md` prepares issue `#38`.
- `docs/current-state/TRACK-A-SEO-SOCIAL-PREP-2026-05-18.md` prepares issues `#36` and `#43`.
- `content/drafts/accessibility-statement-2026-05/README.md` prepares issue `#48`.
- `content/drafts/ai-glossary-2026-05/README.md` prepares issue `#44`.

These are prep artifacts only. They do not close the issues because no live WordPress pages or settings were changed.

### Keynote Authority Pages

- `content/source-packs/keynotes-2026/wp-payloads/about.html`
- `content/source-packs/keynotes-2026/wp-payloads/speaking.html`
- `content/source-packs/keynotes-2026/wp-payloads/work.html`
- `content/source-packs/keynotes-2026/post-packages/README.md`
- `content/source-packs/keynotes-2026/verification/SPEAKING-HORIZONS-VERIFICATION-2026-05-18.md`
- `content/source-packs/keynotes-2026/verification/IA-POLISH-CONTINUATION-VERIFICATION-2026-05-18.md`

These record the latest Speaking, Work, and About payload, verification evidence, and the next companion-post queue after the Horizons proof and IA-polish passes.

## Next Work, In Order

### 1. Verify `main` After Push

Before starting another lane:

```bash
git fetch --prune origin
git status --short --branch
git rev-list --left-right --count main...origin/main
gh pr list --state open --limit 20
```

Expected after this closeout is pushed: `main` and `origin/main` are even, with only PR `#77` and PR `#73` open unless new work has arrived.

### 2. Get More Eyes On Aurora

Goal: turn PR `#77` from a prototype into a judged design surface.

Use these review anchors:

- Local preview: `http://kriskrug-local.local`
- Branch: `codex/aurora-redesign-2026-05-18`
- Smoke report on PR #77 branch: `docs/current-state/AURORA-REDESIGN-SMOKE-2026-05-18.md`
- Review packet on PR #77 branch: `docs/current-state/AURORA-REVIEW-PACKET-2026-05-19.md`
- Desktop screenshot on PR #77 branch: `docs/current-state/aurora-smoke-2026-05-18/aurora-home-desktop.png`
- Mobile screenshot on PR #77 branch: `docs/current-state/aurora-smoke-2026-05-18/aurora-home-mobile.png`
- Fresh desktop/mobile screenshots on PR #77 branch: `docs/current-state/aurora-review-2026-05-19/`
- Current issue routing: `docs/current-state/AURORA-ISSUE-SWARM-2026-05-19.md`

Decision needed after review: continue implementation, file/update GitHub issues, or collect feedback first.

### 3. Run One Track A Publisher Session

Only after a fresh backup or page-level snapshot:

1. Apply the title separator Code Snippet from `TRACK-A-QUICK-FIX-PACK-2026-05-18.md`.
2. Dry-run then apply the `feelmoreplants` to `x.com/kriskrug` replacement if counts are sane.
3. Disable or retune the Beehiiv popup on mobile/tablet.
4. Run Broken Link Checker as a one-shot scan, export the CSV, then disable the plugin.

Stop rule: no connector publish and no bulk post updates in this lane.

### 4. Prep The Three-Post Draft Batch

Output should be review-ready packages, not live posts:

1. `Sovereign AI for Whom?`
2. RAP/certification follow-up
3. Comox Valley AI recap

For each: clean excerpt/meta, category recommendation, internal links, image decision, fact-check/privacy checklist, and a clear "ready for WP draft?" verdict.

Parallel authority-post lane now exists in `content/source-packs/keynotes-2026/post-packages/`. Use that pack when preparing companion posts for LaSalle College, Whistler Institute, Vancouver AI March 2026, Horizons, ChannelNext, Bass Coast, or CBC/appearance proof.

Speaking companion drafts were prepared locally on 2026-05-19:

- `content/drafts/2026-05-19-both-hands-full-ai-creatives-lasalle-college/`
- `content/drafts/2026-05-19-inside-vancouvers-ai-boom-whistler-institute/`
- `content/drafts/2026-05-19-both-hands-full-vancouver-ai-march-2026/`
- `content/drafts/2026-05-19-horizons-ai-models-future-machine-learning/`
- `content/drafts/2026-05-19-ai-keynote-chaos-creativity-channelnext/`
- `content/drafts/2026-05-19-dear-ai-bass-coast-brain-stage/`
- `content/drafts/2026-05-19-ai-media-appearances-podcast-guesting/`

CBC/media appearance sources were collected in `content/source-packs/keynotes-2026/media-appearances/`. The `/podcast-guesting-page-epk/` refresh was deployed and verified on 2026-05-19 after a fresh page snapshot. Next in that lane: publish the standalone appearances roundup only after KK review, then tighten internal links from `/speaking/` and `/about/` if needed.

### 5. Clean GitHub Backlog Safely

- Keep PR `#73` parked until mergeability is clarified, capability hardening, staging activation, backup/deploy approval, and checks are handled.
- Keep PR `#77` draft until Aurora has review sign-off and smoke evidence.
- Treat `claude/setup-wordpress-rebuild-KVLxh` as an archival deletion candidate, not a merge candidate.
- Filed Aurora epics `#80`-`#86`.
- Routed stale design issues `#24`-`#35` toward the active Aurora lane and removed their stale `auto-implement` labels.

### 6. Credential-History Cleanup Preflight

The leaked application password was revoked, but git history still contains it. Do not rewrite history inside a mixed work session.

Next safe step is a preflight doc only:

- exact commits containing the secret,
- replacement/redaction method,
- branches/tags impacted,
- active worktrees to coordinate,
- backup refs and recovery commands,
- force-push-with-lease command to run only after explicit approval.

Preflight now exists at `docs/current-state/CREDENTIAL-HISTORY-REWRITE-PREFLIGHT-2026-05-19.md`; the rewrite itself has not been run.

## Recommended Swarm Lanes

| Lane | Track | Scope | Done when |
|---|---|---|---|
| Aurora review | B | PR `#77`, Local preview, screenshots, issue comments | KK and reviewers give continue/pivot/feedback-first signal |
| Track A publisher | A | Quick-fix pack only | Backup proof, applied fixes, curl verification, rollback notes |
| Draft prep | A | `content/drafts/` and draft-prep docs | Three post packages are review-ready; no live writes |
| Issue hygiene | GitHub | Comments/labels/issues | Old design issues point to current Aurora lane; parked items stay parked |
| Credential preflight | Git | Docs only | Rewrite plan is explicit enough to approve or reject |

## Human Checkpoints

Ask KK before:

- activating Aurora on production,
- publishing any draft post,
- running the actual credential-history rewrite,
- merging PR `#73`,
- deleting old remote branches that may still contain unique design material.
