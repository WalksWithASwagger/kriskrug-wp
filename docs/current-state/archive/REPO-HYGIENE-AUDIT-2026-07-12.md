# Repo Hygiene Audit — Docs, Branches, Cruft & Bloat

**Audit date:** 2026-07-12
**Scope:** Read-only inventory of documentation, branches, and accumulated
cruft/bloat, plus a low-risk safe-cleanup pass. Heavy binaries are **documented
only** — no destructive action taken on them, per the `AGENTS.md` Hard Safety
Rules (rollback path + KK approval before destructive ops).

**What this pass actually changed** (safe cleanup):
- Deleted two unreferenced, stale root docs (recoverable via git history).
- Added scoped `.gitignore` rules so `docs/current-state/reports/` stops
  re-accumulating heavy capture artifacts.
- Added this report and indexed it in `docs/current-state/README.md`.

**Phase A follow-up (executed 2026-07-12, same branch):** pruned only the
capture artifacts that **no tracked file references** — verified by grepping
every basename/path across the full tracked corpus (not just markdown):
- 13 orphaned `docs/current-state/reports/` artifacts (~5.3M) — mostly
  `link-inject-rollback-*.json` operational dumps from 2026-06-15 plus a few
  predeploy `*.json/.html/.css` snapshots; nothing links to them.
- 16 orphaned `backup/<timestamp>/` page-snapshot dirs (~1.6M) — May-23 and
  late-June snapshots no doc or script cites.

All 104 referenced `reports/` artifacts and 27 referenced `backup/` dirs were
**kept** — the folders are tightly cross-linked (report `.md` files cite their
own sibling evidence), so removing them would leave dead links in the
historical docs. Those, plus `content/drafts/` images and the `.git` history
rewrite, remain deferred (see §4) for a future KK-approved, rollback-gated
task. Everything pruned is recoverable from git history until that rewrite.

Everything else below is a **recommendation** for a future KK-approved,
rollback-gated task — flagged, not executed.

---

## 1. Branches — clean, no action

Only two branches exist:

| Branch | Note |
|---|---|
| `origin/main` | canonical line |
| `claude/audit-docs-branches-cruft-or7ajn` | this audit's working branch |

A branch cleanup already ran on 2026-06-26
(`reports/branch-cleanup-20260626.md`). The historical `aurora/v2` /
`aurora/v3-reconcile` "evidence branches" referenced in older docs
(`README.md`, `TWO-TRACK-MODEL.md`) are **no longer on the remote**. Those doc
references are now stale but harmless historical context. **No branch action
required.**

## 2. Docs — mostly intentional, keep

`docs/` is 38M. The `docs/current-state/` folder holds **99 dated markdown
docs** plus `reports/`, `raw/`, and `archive/`. Per `AGENTS.md` and
`docs/current-state/README.md`, these dated docs are **intentional historical
reference**, indexed and cross-linked. They are **not cruft** — do not bulk
delete.

Minor doc-hygiene observations (no action this pass; note for maintainers):
- Several `README.md` / `TWO-TRACK-MODEL.md` references to `aurora/v2` and
  `aurora/v3-reconcile` branches and to local side-worktree paths
  (`/Users/kk/Code/...`) are stale — those branches/worktrees no longer exist
  in this clone. Left in place as historical context.
- The `docs/current-state/README.md` index is large but accurate; it remains
  the correct front door.

## 3. Cruft & bloat — disposition table

| Item | Size (tracked) | Disposition | Rationale |
|---|---|---|---|
| `DEPLOYMENT-READY-BATCH-1.md` (root) | 4K | **Deleted this pass** | Jan 3 2026 batch-deploy checklist for `fixes/` that were reconciled long ago (`FIXES-LIVE-RECONCILIATION-2026-05-20.md`). Unreferenced by any md/Makefile/script/workflow. |
| `PRODUCTION-IMPORT-GUIDE.md` (root) | 2K | **Deleted this pass** | Cloudways import + agent-swarm setup. `AGENTS.md` states the Cloudways path was "never used as planned" and the swarm is parked. Unreferenced. |
| `docs/current-state/reports/` non-md captures | 31M (80 PNGs, 5.4M JSON, HTML, CSV) | **gitignore future + flag existing for approval** | Folder's documented purpose is "timestamped `make morning-truth` outputs." PNG screenshots (23M under `screenshots/`), 0.5–2MB `link-inject-rollback-*.json`, and HTML page snapshots are one-off operational spillover. New `.gitignore` rules stop future growth; existing tracked copies await a KK-approved cleanup. |
| `backup/` page snapshots | 19M | **Document only — do NOT delete blindly** | Several snapshot dirs are still referenced as issue #76 rollback evidence in `docs/current-state/README.md` (`20260518-111546`, `-113350`, `-215912`, `-223014`, `-224340`). `.gitignore` already excludes the archive blobs (`*.gz/*.zip/*.sql`); only lightweight HTML/JSON snapshots are tracked. Prune only the snapshot dirs no doc references, under approval. |
| `content/drafts/` images | 238M | **Document only** | Largest working-tree item. Many images are for already-published posts (e.g. `sovereign-ai-for-whom` = WP draft `11905`; several 3–8MB PNGs). See §4. |
| `.git` history | 295M | **Document only** | Dominated by large PNGs committed over time. Shrinking needs a history rewrite — high-risk, gated. See §4. |

Working tree (excluding `.git`) is **332M**; `.git` adds **295M** ≈ **627M** total.

## 4. Deferred — needs KK approval + rollback path

These are the high-impact bloat reductions. Each is intentionally **not**
executed here.

### 4a. `docs/current-state/reports/` existing captures (31M)
- **Recommendation:** move screenshots/PNGs/HTML/JSON captures out of git
  (delete tracked copies; they are one-off evidence, reproducible from live
  or already summarized in the `.md` reports beside them). Keep the
  `morning-truth-*.md` and other markdown summaries.
- **Rollback:** all recoverable from git history until a history rewrite.
- Note: `.gitignore` added this pass prevents *future* accumulation only;
  it does not remove the ~31M already tracked.

### 4b. `content/drafts/` images (238M)
- **Recommendation:** for posts confirmed published to WP, the canonical copy
  lives in WP media — repo copies are redundant. Options: (a) delete images
  for verified-published drafts, keeping the markdown source; (b) adopt
  `git-lfs` for `content/drafts/**/images/*` going forward. `.gitignore`
  already excludes some working image dirs (e.g. `keep-the-machine-strange/img/`,
  `you-cant-drink-data/photos-raw/`) — extend that pattern deliberately.
- **Gate:** verify published status per draft before removing anything;
  content is high-value and hard to regenerate.

### 4c. `.git` history rewrite (295M)
- **Recommendation:** a `git filter-repo` pass to drop large binary blobs
  (drafts PNGs, reports screenshots) from history would reclaim the bulk of
  295M. This is the **only** way to shrink `.git`.
- **Gate:** follow the existing playbook
  (`CREDENTIAL-HISTORY-REWRITE-PREFLIGHT-2026-05-19.md` /
  `CREDENTIAL-HISTORY-REWRITE-EXECUTION-2026-05-19.md`). Requires force-push,
  coordination with anyone holding clones, and explicit KK approval. High
  blast radius — do as its own dedicated task.

## 5. Verification of this pass
- `git status` shows only: this report (new), `README.md` (index line),
  `.gitignore` (append), and the two root-doc deletions.
- `git check-ignore docs/current-state/reports/screenshots/x.png` → matches;
  `.../reports/morning-truth-x.md` → no match (markdown still tracked).
- `grep -rn "DEPLOYMENT-READY-BATCH-1\|PRODUCTION-IMPORT-GUIDE" .` → no hits
  after deletion (no dangling links).

---

**Bottom line:** branches are already clean; the dated docs are intentional and
stay; the genuinely reclaimable bloat is ~31M of `reports/` captures, ~238M of
`content/drafts/` images, and ~295M of `.git` history — all gated behind KK
approval. This pass removed only two dead root docs and stopped the `reports/`
folder from growing further.
