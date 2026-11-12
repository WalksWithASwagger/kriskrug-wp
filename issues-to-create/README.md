# issues-to-create/

**STATUS: Historical payloads plus a few contingent stubs. New issues are written directly on GitHub, not here.**

See [`docs/current-state/archive/ISSUES-TO-CREATE-RECONCILIATION-2026-06-09.md`](../docs/current-state/archive/ISSUES-TO-CREATE-RECONCILIATION-2026-06-09.md) for the June 2026 per-payload disposition (filed / shipped / valid / obsolete). The 2026-08-15 conservative archive (14 files whose every mapped issue is closed) lives in [`archive/`](archive/) and is recorded in [`docs/current-state/reports/BACKLOG-GROOMING-DOSSIER-2026-08-15.md`](../docs/current-state/reports/BACKLOG-GROOMING-DOSSIER-2026-08-15.md) section 5.

`make issues FILE=...` previews and stops. It only creates issues when `CONFIRM=1` is set, and it skips any title that already exists on GitHub. Use it only after KK approves the "still valid" list.

Status below was re-verified with `gh issue view <n> --json state` on 2026-11-12.

## Keep (still open children, or never filed)

- [`batch-site-redesign-2026-07-17.json`](batch-site-redesign-2026-07-17.json) → filed as #403–#424; **#403 and #424 still open** (every other child in #403–#424 is closed)
- [`contact-form-implementation-stub-from-277.md`](contact-form-implementation-stub-from-277.md) → contingent stub; file only if KK picks Option B on #277
- [`world-cup-fashion-cake-agent-tasks.md`](world-cup-fashion-cake-agent-tasks.md) → never filed; needs KK before filing
- [`seo-hubs-402/`](seo-hubs-402/) → filed 2026-08-16 as #826-#834 (children of #402). #402 and every child except #828 are closed as applied; **#828** (negotiation checklist rewrite) is still open. Do not re-file or re-apply the closed children. Receipt: [`docs/current-state/reports/seo-hub-split-402-20260816.md`](../docs/current-state/reports/seo-hub-split-402-20260816.md)

## Archive (every mapped issue closed)

Moved, not deleted. Rule: archive only when every mapped issue is closed. See [`archive/README.md`](archive/README.md).

- [`archive/batch-1-critical-bugs.json`](archive/batch-1-critical-bugs.json) → #1–#11 (moved 2026-11-12 after #4 closed)
- [`archive/testimonials-showpiece-v2-swarm-2026-08-01.md`](archive/testimonials-showpiece-v2-swarm-2026-08-01.md) → #593–#602 (moved 2026-11-12 after #593 and #602 closed)
- [`archive/aurora-v2-redesign-epics.md`](archive/aurora-v2-redesign-epics.md) → filed as #80–#86
- [`archive/batch-2-content-positioning.json`](archive/batch-2-content-positioning.json) → #12–#23 (including #22, closed 2026-08-16)
- [`archive/batch-3-4-all-remaining.json`](archive/batch-3-4-all-remaining.json) → #24–#48
- [`archive/batch-eng-hardening-2026-06-24.json`](archive/batch-eng-hardening-2026-06-24.json) → #251–#256
- [`archive/batch-marketing-archives-portal.json`](archive/batch-marketing-archives-portal.json) → #49–#64
- [`archive/batch-session-followups-2026-06-24.json`](archive/batch-session-followups-2026-06-24.json) → #247–#250
- [`archive/content-extraction-updates.json`](archive/content-extraction-updates.json) → #65–#68
- [`archive/events-archive-backfill-swarm-2026-08-01.json`](archive/events-archive-backfill-swarm-2026-08-01.json) → #586–#592
- [`archive/futureproof-announcement-post-2026-07-26.md`](archive/futureproof-announcement-post-2026-07-26.md) → #496–#500
- [`archive/jetpack-seo-audit-all-posts.md`](archive/jetpack-seo-audit-all-posts.md) → obsolete (#194 filed it; #661 proved Jetpack SEO writes no-op)
- [`archive/long-run-workday-2026-07-16.md`](archive/long-run-workday-2026-07-16.md) → #368, #369
- [`archive/monday-agent-queue-2026-07-16.md`](archive/monday-agent-queue-2026-07-16.md) → #360–#366
- [`archive/style-css-dangling-form-selectors.md`](archive/style-css-dangling-form-selectors.md) → #698
- [`archive/visual-baseline-capture-mode-mismatch.md`](archive/visual-baseline-capture-mode-mismatch.md) → #697
- [`archive/aurora-launch-audit-2026-05-23.json`](archive/aurora-launch-audit-2026-05-23.json) → #116–#127 (moved 2026-08-19 after #122 and #127 closed)
- [`archive/voice-audit-blog-sweep-swarm-2026-08-01.json`](archive/voice-audit-blog-sweep-swarm-2026-08-01.json) / [`archive/voice-audit-blog-sweep-swarm-2026-08-01.md`](archive/voice-audit-blog-sweep-swarm-2026-08-01.md) → #603–#616 (moved 2026-08-19 after #603 and #612 closed)

January batches (`batch-*.json`) were mostly superseded by the Aurora cutover; open residue from those batches is on the keep list above (#403 and #424).
