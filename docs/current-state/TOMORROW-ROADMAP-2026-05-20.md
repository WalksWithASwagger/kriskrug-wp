# Tomorrow Roadmap - 2026-05-20

**Prepared after:** 2026-05-19 Speaking/Work/About authority-page continuation, Horizons proof, and Track A issue-swarm docs integration
**Use for:** The next operating session. If the calendar has drifted, treat this as the next-session plan rather than a date-bound promise.
**Tracks:** Track A on `main`; Track B on `aurora/v2`.

Current pointer: [`NEXT-ROUND-WORK-2026-05-19.md`](NEXT-ROUND-WORK-2026-05-19.md) is the fresher command sheet after the queue sweep, Track A prep, and keynote closeout.

## Where We Ended

Local `main` was fetched and rebased onto `origin/main` before this closeout. The three newer remote docs/preview commits are integrated:

- `9fbbc76 preview: add redesign direction pages`
- `b292fd9 docs: record queue sweep and revert static previews`
- `8285831 docs: prepare Track A issue swarm`

The live Speaking, Work, and About authority pages have now had three connected Track A passes:

- `63e49e4 content: polish keynote authority pages` - second-pass overhaul of the live Speaking, Work, and About pages.
- `ca332f7 content: add horizons speaking proof` - source-backed Horizons by Compass Datacenters proof point and video card on Speaking.
- `793f364 content: polish authority page IA` - tighter Work hierarchy, About interlinking/proof-list structure, and Speaking booking-lane cards.

The source pack now includes:

- Fresh page-level rollback snapshots under `backup/20260518-123159/`, `backup/20260518-215912/`, `backup/20260518-223014/`, and `backup/20260518-224340/`.
- Verification records at `content/source-packs/keynotes-2026/verification/DEPLOY-VERIFICATION-2026-05-18.md`, `POLISH-VERIFICATION-2026-05-18.md`, `SPEAKING-GUESTING-VERIFICATION-2026-05-18.md`, `SPEAKING-HORIZONS-VERIFICATION-2026-05-18.md`, and `IA-POLISH-CONTINUATION-VERIFICATION-2026-05-18.md`.
- Public video research, captions, thumbnails, and metadata under `content/source-packs/keynotes-2026/video-research/`.
- Authenticated WordPress draft candidates for future speaking/AI authority posts.
- A deployed Podcast EPK refresh at `/podcast-guesting-page-epk/`, with rollback snapshots under `backup/20260519-105949/` and verification in `content/source-packs/keynotes-2026/verification/PODCAST-EPK-DEPLOY-VERIFICATION-2026-05-19.md`.

Live public checks after the latest pass confirmed:

- `/speaking/`, `/recent-projects-include/`, `/work/`, and `/about/` return `200`.
- `/work/` still redirects to `/recent-projects-include/`.
- The authority-page markers are present, images lazy-load cleanly in Playwright, and no target page shows `Leave a Reply`.

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

### 1. Verify this closeout

If not already done:

1. Fetch/prune origin.
2. Confirm `git rev-list --left-right --count main...origin/main` returns `0 0`.
3. Verify GitHub shows the Horizons proof commit, the IA polish commit, and the documentation closeout commit.
4. Use [`NEXT-ROUND-WORK-2026-05-19.md`](NEXT-ROUND-WORK-2026-05-19.md) as the current work order.

### 2. Choose the next Track A authority round

Goal: turn the new authority pages into a stronger supporting network, not just prettier pages.

Recommended order:

1. **Speaking proof posts and clips** - turn the public video intake into source-backed post packages for Bass Coast, Whistler Institute, ChannelNext, Vancouver AI March 2026, and Horizons. Start with review-ready drafts; do not publish without KK review.
2. **Podcast / appearance support post** - the EPK page is now the home for guest appearances, hosting, emcee work, CBC, and produced interviews. Next step is deciding whether to publish the supporting appearances roundup after KK review.
3. **Photo and asset source pack** - inventory better LaSalle, CreativeMornings, Vancouver AI meetup, and Whistler photos; use WP-hosted or owned stable assets only.
4. **About proof-source cleanup** - keep the publication/client lists, but progressively source, group, and link the most impressive proof instead of expanding an unsourced wall of names.
5. **Current-theme technical quick wins** - title separator snippet, Twitter-to-X replacement, and broken-link scan.

### 3. Run the credential-history rewrite preflight

Goal: make the force-push boring before doing it.

Preflight should list:

- The exact commit(s) containing the revoked credential.
- The exact replacement/redaction rule.
- The branches/tags that would be rewritten.
- The active local worktrees that need coordination.
- The recovery plan: backup ref, clone safety copy, and force-push-with-lease command.

Do not perform the force-push until the preflight is written down and the working tree is clean.

### 4. Start Aurora P0 on `aurora/v2`

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

### 5. Prep the three-post draft batch

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

### 6. File and clean up Aurora issues

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
| Speaking proof network | A | `content/source-packs/keynotes-2026/`, `content/drafts/` | Video/appearance post packages are review-ready; no publish without approval |
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
