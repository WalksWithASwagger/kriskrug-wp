# issues-to-create/

**STATUS: Historical payloads — do not mass-file without reconciliation.**

See [`docs/current-state/archive/ISSUES-TO-CREATE-RECONCILIATION-2026-06-09.md`](../docs/current-state/archive/ISSUES-TO-CREATE-RECONCILIATION-2026-06-09.md) for the June 2026 per-payload disposition (filed / shipped / valid / obsolete). The 2026-08-15 conservative archive (14 files whose every mapped issue is closed) lives in [`archive/`](archive/) and is recorded in [`docs/current-state/reports/BACKLOG-GROOMING-DOSSIER-2026-08-15.md`](../docs/current-state/reports/BACKLOG-GROOMING-DOSSIER-2026-08-15.md) section 5.

Use `make issues FILE=...` only after KK approves the "still valid" list.

## Keep (still open children, or never filed)

- [`aurora-launch-audit-2026-05-23.json`](aurora-launch-audit-2026-05-23.json) → filed as #116–#127; #122 and #127 still open
- [`batch-1-critical-bugs.json`](batch-1-critical-bugs.json) → filed as #1–#11; #4 still open
- [`batch-site-redesign-2026-07-17.json`](batch-site-redesign-2026-07-17.json) → filed as #403–#424; 11 still open
- [`contact-form-implementation-stub-from-277.md`](contact-form-implementation-stub-from-277.md) → contingent stub; file only if KK picks Option B on #277
- [`testimonials-showpiece-v2-swarm-2026-08-01.md`](testimonials-showpiece-v2-swarm-2026-08-01.md) → #593–#602; #593 and #602 still open
- [`voice-audit-blog-sweep-swarm-2026-08-01.json`](voice-audit-blog-sweep-swarm-2026-08-01.json) / [`voice-audit-blog-sweep-swarm-2026-08-01.md`](voice-audit-blog-sweep-swarm-2026-08-01.md) → #603–#616; #603 and #612 still open
- [`world-cup-fashion-cake-agent-tasks.md`](world-cup-fashion-cake-agent-tasks.md) → never filed; needs KK before filing
- [`seo-hubs-402/`](seo-hubs-402/) → 9 unfiled children of #402 (taxonomy first). Do not `gh issue create` until KK approves. Do not close #402.

## Archive (every mapped issue closed)

Moved, not deleted. Rule: archive only when every mapped issue is closed. See [`archive/README.md`](archive/README.md).

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

January batches (`batch-*.json`) were mostly superseded by the Aurora cutover; open residue from those batches is on the keep list above (#4 and the #403–#424 set).
