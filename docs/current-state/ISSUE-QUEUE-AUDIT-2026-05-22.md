# Issue Queue Audit - 2026-05-22

**Purpose:** route the 63 open GitHub issues into actionable lanes after the backup-gate retirement, StoryHive draft reset, and WordPress 7 readiness work.
**Track:** queue control for Track A on `main`; Track B/Aurora stays separate.
**Snapshot:** 2026-05-22 18:00 PDT.

## Queue Truth

- Open PRs: `0`.
- Open issues: `63`.
- Open issues with historical `auto-implement`: `47`.
- Open `track-b` + `aurora-v2`: `13`.
- Open `needs-human-review`: `3`.
- Open `swarm-ready`: `13`.
- Open `swarm-parked`: `11`.
- Open `priority:high`: `28`.
- `auto-implement` is historical only. It no longer starts the parked Agent PR Generator.
- Do not close issues from title memory. Close only after target checks and a short evidence comment.

## Close Or Re-Scope First

These are the queue-fog reducers. They should be checked before starting new feature work.

| Issue | Current read | Next action |
|---|---|---|
| `#3` Projects page 404 | The public story now centers Work, not a standalone Projects page. | Verify `/projects/`, `/work/`, nav, and redirects. Close as superseded by Work only if evidence is attached. |
| `#12` Homepage polymath hero | Homepage positioning work likely shipped after January issue creation. | Verify live homepage copy, H1 behavior, role proof, CTAs, mobile, and close or re-scope to H1/alt polish. |
| `#16` About polymath journey | About role-section work shipped through May content passes. | Verify live About page against acceptance criteria, then close or re-scope residual polish. |
| `#17` Work/Projects architecture | Overlaps heavily with `#68`. | Keep one canonical Work issue. Prefer `#68` for the current Work page target and close/re-scope `#17`. |
| `#68` Work page from recent projects | Still useful, but acceptance should include current `/work/` URL/canonical/OG reality. | Re-scope as Work metadata/content polish if the page already exists. |

## Track A Polish And Site Quality

These are current-site improvements. They can move after target checks, rollback notes, and deploy paths are clear.

- `#4` image alt text: keep as the broad image accessibility lane; first concrete slice is homepage/About/Work visible images.
- `#5` color contrast: needs current-theme contrast audit before changes.
- `#7` services pricing: content/product decision first; do not invent pricing.
- `#8`, `#9`, `#10`: small accessibility/UX quick wins only after confirming the current rendered targets.
- `#11`: membership matrix may be stale; verify whether this belongs on kriskrug.co or another property.
- `#13`, `#14`, `#15`, `#18`: authority/community sections; treat as source-pack/content passes, not theme work.
- `#19`, `#20`, `#21`, `#22`: community proof, voice, photography credential, and land acknowledgement. These should become one editorial polish packet unless a target page needs its own issue.
- `#23`: category reorganization remains `needs-human-review`; no bulk taxonomy writes without approval.
- `#36`, `#43`: Jetpack/SEO/social metadata work; verify current rendered metadata before changing.
- `#38`, `#40`, `#41`, `#42`, `#45`: internal links, image performance, plugin bloat, lazy loading, RSS. Run as audit-first lanes.
- `#46`, `#47`, `#48`: accessibility audit, keyboard navigation, and accessibility statement. Statement/page work can move through draft review; broad audit needs a separate evidence packet.

## Draft Publishing Queue

This lane exists so WordPress drafts stop pretending to be a schedule.

- `#75` remains the publishing-trust gate. Credential rotation and Feature/category guarding are partly done; keep it open for secret-scan evidence, queue reconciliation, and publish sign-off rules.
- `#95` is stale in title/body because the strict backup gate is retired and private draft `11879` exists. Re-scope it to review, image decision, preview QA, rollback/delete note, and no publish/backlinks without KK approval.
- `#44` glossary page exists as a draft lane; run it through the same draft quality gate as posts.

Current draft audit command:

```bash
make draft-queue-audit
LOCAL_ONLY=1 make draft-queue-audit
```

Current draft shape:

- WordPress has `42` draft posts, `5` draft pages, and no scheduled queue.
- StoryHive drafts `11876`, `11877`, and `11878` are reviewable, not schedule-ready.
- Keynote/media drafts `11879`-`11885` are thin and need expansion/media/block-native rebuild before scheduling.
- Older admin drafts are rescue candidates, not release calendar items.

## WordPress 7 Readiness

No GitHub issue currently tracks this lane. If tracker visibility is needed, create one issue from [WP-7-UPGRADE-2026-05-22.md](WP-7-UPGRADE-2026-05-22.md) instead of burying it in Track A polish.

Current stance:

- Production is still WordPress `6.9.4`.
- WordPress 7.0 is public, but production upgrade should wait for Pagely staging/support guidance or a clear expedited path.
- Use `make wp7-smoke EXPECT_VERSION=6.9.4` and `make wp7-admin-readiness` before any staging request or production window.
- Keep production AI provider connectors empty until KK approves provider, cost, privacy, and retention rules.

## Track B / Aurora

These stay out of `main` and belong on `aurora/v2`.

- Legacy design issues: `#24`, `#25`, `#26`, `#27`, `#28`, `#29`, `#30`, `#31`, `#32`, `#33`, `#34`, `#35`.
- Final QA gate: `#86`.

Current stance:

- `#86` remains open intentionally.
- Local QA evidence exists, but real staging with production-like media is still required before closing.
- Do not use Track A polish as a back door into Aurora activation.

## Parked Strategy And Product Epics

These are broad strategy/product lanes. Do not start them as quick implementation work.

- Marketing strategy: `#49`, `#50`, `#51`, `#52`, `#53`, `#54`, `#55`, `#56`, `#57`, `#58`.
- Archive and knowledge-base strategy: `#59`, `#60`, `#61`.
- Platform/portal concepts: `#62`, `#63`, `#64`.

Recommended handling:

- Add evidence comments when current site/source packs already cover part of the scope.
- Re-scope broad issues into smaller source-pack or deploy-packet slices only when there is a concrete target.
- Keep parked labels on dependency-heavy items until there is a clear owner, source pack, and deploy path.

## Recommended Next Issue Actions

1. Comment and re-scope `#95` because the issue text is now stale.
2. Verify and close/re-scope `#3`, `#12`, and `#16` with live evidence.
3. Consolidate `#17` and `#68` around the current Work page URL/canonical/OG fix.
4. Run one StoryHive proof post through review, preview QA, and schedule decision before adding more drafts.
5. Batch `#8`, `#9`, `#10`, `#36`, `#43`, and `#48` only after target checks identify exact current-theme surfaces.
