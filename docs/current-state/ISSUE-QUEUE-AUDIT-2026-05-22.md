# Issue Queue Audit - 2026-05-22

**Purpose:** route the current GitHub issue backlog into actionable lanes after the backup-gate retirement, StoryHive draft reset, WordPress 7 readiness work, and the first queue-hygiene pass.
**Track:** queue control for Track A on `main`; Track B/Aurora stays separate.
**Snapshot:** 2026-05-22 18:55 PDT.

## Queue Truth

- Open PRs: `0`.
- Open issues: `61`.
- Open issues with historical `auto-implement`: `45`.
- Open `track-b` + `aurora-v2`: `13`.
- Open `needs-human-review`: `3`.
- Open `swarm-ready`: `13`.
- Open `swarm-parked`: `11`.
- Open `priority:high`: `26`.
- `auto-implement` is historical only. It no longer starts the parked Agent PR Generator.
- Do not close issues from title memory. Close only after target checks and a short evidence comment.
- First hygiene pass closed `#16` and `#17`; re-scoped `#3`, `#12`, `#68`, and `#95` with evidence comments.

## Close Or Re-Scope First

These are the queue-fog reducers. They should be checked before starting new feature work.

| Issue | Current read | Next action |
|---|---|---|
| `#3` Projects page 404 | Public `/projects/` still returns `404`; `/work/` exists. | Re-scoped to redirect `/projects/` to the canonical Work page. Keep open. |
| `#12` Homepage polymath hero | Homepage has an empty H1 plus `Kris Krüg, Generative AI for Creative Professionals`; BC+AI was not visible in fetched homepage text. | Re-scoped to homepage H1 and role-proof hero polish. Keep open. |
| `#16` About polymath journey | Live About page now has the current role spine: BC+AI, Indigenomics, The Upgrade AI, Work/Projects, and Kris Krug. | Closed as completed on 2026-05-22. |
| `#17` Work/Projects architecture | Work page exists and carries project proof content; remaining gap belongs to `#68`. | Closed as superseded by `#68` on 2026-05-22. |
| `#68` Work page from recent projects | `/work/` returns `200` but resolves/canonicalizes/OGs to `/recent-projects-include/`. | Re-scoped to Work page canonical, OG, and proof metadata. Keep open. |

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
- `#95` is re-scoped because the strict backup gate is retired and private draft `11879` exists. It now tracks review, image decision, preview QA, rollback/delete note, and no publish/backlinks without KK approval.
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

1. Implement `#3` and `#68` together as a small Work routing/metadata polish packet: `/projects/` redirect, `/work/` canonical decision, OG URL, and rollback note.
2. Implement `#12` as homepage H1 plus role-proof hero polish.
3. Run one StoryHive proof post through review, preview QA, and schedule decision before adding more drafts.
4. Batch `#8`, `#9`, `#10`, `#36`, `#43`, and `#48` only after target checks identify exact current-theme surfaces.
5. Keep broad strategy issues parked until there is a concrete source pack, owner, and deploy path.
