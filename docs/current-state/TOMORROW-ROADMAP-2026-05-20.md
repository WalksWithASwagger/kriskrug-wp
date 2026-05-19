# Tomorrow Roadmap - 2026-05-20

**Prepared after:** 2026-05-18 keynote authority polish and roadmap-decision capture
**Use for:** The next operating session. If the calendar has drifted, treat this as the next-session plan rather than a date-bound promise.
**Tracks:** Track A on `main`; Track B on `aurora/v2`.

## Where We Ended

The repo has one completed local commit ready to push before this roadmap commit:

- `63e49e4 content: polish keynote authority pages`

That commit includes:

- Second-pass polish for the live Speaking, Work, and About pages.
- Fresh page-level rollback snapshots under `backup/20260518-123159/page-snapshots/`.
- Verification record at `content/source-packs/keynotes-2026/verification/POLISH-VERIFICATION-2026-05-18.md`.
- Scrolled contact-sheet screenshots for the polished pages.
- Public video research, captions, thumbnails, and metadata under `content/source-packs/keynotes-2026/video-research/`.
- Authenticated WordPress draft candidates for future speaking/AI authority posts.

The current strategic decisions are recorded in `FULL-AUDIT-ROADMAP-2026-05-18.md`:

- Rewrite public git history to remove the revoked leaked password, but do it as a controlled standalone operation.
- Page-level snapshots are acceptable for small Track A content/snippet writes.
- Aurora should lead with community-room / event-energy media.
- Aurora's primary path should combine "Explore my work" and "Work with Kris."
- Brand direction is premium/editorial/human with weird AI details.
- Photography is a supporting credibility band in v1.
- Prep all three next posts, publish none until review.
- File clean Aurora epics, then comment/close old design issues gradually.
- Close PR `#74` after extracting useful design ideas.
- Park PR `#73` until Aurora/current-site priorities settle.

## Non-Negotiable Guardrails

1. Do not run a production connector write without a fresh dry-run and target slug/ID/status verification.
2. Do not use `--publish` for the next post batch.
3. Do not activate Aurora on production.
4. Do not mix Track A content/page work and Track B theme work in one commit.
5. Do not rewrite git history casually; use a final preflight summary immediately before force-push.

## Tomorrow's Recommended Order

### 1. Push and verify today's closeout

If not already done:

1. Push `main`.
2. Confirm `git rev-list --left-right --count main...origin/main` returns `0 0`.
3. Verify GitHub shows the keynote polish commit and this roadmap commit.
4. Comment on issue `#76` only if the polish pass needs a public issue breadcrumb beyond the already-closed deploy verification.

### 2. Run the credential-history rewrite preflight

Goal: make the force-push boring before doing it.

Preflight should list:

- The exact commit(s) containing the revoked credential.
- The exact replacement/redaction rule.
- The branches/tags that would be rewritten.
- The active local worktrees that need coordination.
- The recovery plan: backup ref, clone safety copy, and force-push-with-lease command.

Do not perform the force-push until the preflight is written down and the working tree is clean.

### 3. Start Aurora P0 on `aurora/v2`

Goal: get from "prototype with broken render" to "judgable design surface."

First worker scope:

- Branch/worktree: `aurora/v2` only.
- Fix desktop header/nav render.
- Re-run the six-page Local smoke from `AURORA-STAGING-REPORT-2026-05-18.md`.
- Capture desktop/mobile screenshots.
- Add a compact media inventory that prioritizes community-room/event-energy assets.

Do not:

- Merge Aurora into `main`.
- Activate Aurora on production.
- Rewrite content payloads from the theme branch.

### 4. Prep the three-post draft batch

Goal: create reviewable post packages, not live posts.

The `Speaking` payload update for podcast guesting, hosting, emcee, and moderation positioning has been deployed and verified. Use `content/source-packs/keynotes-2026/verification/SPEAKING-GUESTING-VERIFICATION-2026-05-18.md` as the evidence trail.

Post-prep order:

1. `Sovereign AI for Whom?`
2. RAP/certification follow-up
3. Comox Valley AI recap

Output for each:

- Clean excerpt/meta.
- Category recommendation.
- Internal-link recommendations.
- Image/featured-image decision.
- Fact-check or privacy checklist.
- Clear "ready for WP draft?" verdict.

No WordPress writes until all three have been reviewed.

### 5. File and clean up Aurora issues

Goal: make the backlog swarm-safe.

1. File clean Aurora epics from `issues-to-create/aurora-v2-redesign-epics.md`.
2. Comment on old design issues `#24-#35` with the new audit/epic pointer.
3. Remove stale `auto-implement` labels from old design issues until each issue has current acceptance criteria.
4. Close PR `#74` after extracting any useful preview ideas into the Aurora audit or issue comments.
5. Leave PR `#73` parked.

## Suggested Swarm

Run these in bounded lanes:

| Lane | Track | Write scope | Done when |
|---|---|---|---|
| Credential rewrite preflight | Git | Docs/commands only until final approval | Preflight names exact commits, rewrite plan, and recovery path |
| Aurora P0 | B | `aurora/v2`, `theme/kk-aurora/`, Aurora docs | Header/nav smoke passes and screenshots exist |
| Draft prep | A | `content/drafts/`, draft-prep docs | Three posts have review-ready packages; no WP writes |
| Issue hygiene | GitHub | Issues/labels/comments | New Aurora epics filed; stale design issues linked or cleaned |
| PR triage | GitHub | PR comments/state only | PR `#74` closed after extraction; PR `#73` explicitly parked |

## Human Checkpoints

Ask KK before:

- The actual git-history force-push.
- Any production WordPress write beyond page-level content/snippet changes.
- Publishing any of the three next posts.
- Choosing final Aurora hero media if the available community/event assets are weak.
- Closing old issues that may still carry useful business intent.
