# Repo bloat #318 — next steps (2026-07-26)

**Status:** ops runbook only. **No deletes in this commit.**  
**Branch:** `cursor/318-reclaim-next-steps-f196`  
**Parent:** [#318](https://github.com/WalksWithASwagger/kriskrug-wp/issues/318) · sibling [#369](https://github.com/WalksWithASwagger/kriskrug-wp/issues/369)  
**Ranked path source:** [PR #502](https://github.com/WalksWithASwagger/kriskrug-wp/pull/502) / `origin/cursor/369-reclaim-list-f196` → `docs/current-state/reports/repo-reclaim-list-20260726.md` (~**266 MB** working-tree candidates)

This note turns the #369 reclaim list into an executable gate sequence for #318 Phase B (working-tree reclaim). Phase C (`.git` / `filter-repo`) stays out of scope until A/B land and KK coordinates a mirror backup.

---

## 0. Preconditions (already true)

| Item | State |
|---|---|
| Phase A orphan prune | Done (PR #317) |
| Ranked reclaim list (#369) | Open as PR #502 — list only, no deletes |
| Hard safety rules | Rollback path + KK approval before destructive ops (`AGENTS.md`) |
| History rewrite | **Forbidden** in any delete PR from this lane |

---

## 1. KK approval gate — exact paths

**Do not open a delete PR until KK replies with an explicit allow-list** (issue comment on #369 or #318 is enough). Soft “looks good” without paths is not approval.

### Preferred first approval shape (recommended)

**Approve Tier A + D only** (~**212 MB**). Leave B / C / E for a second KK pass.

Reply template KK can paste:

```text
#369 / #318 approve shape: A+D only
Allow-list = every path under §1.1 and §1.2 in
docs/current-state/reports/repo-bloat-318-next-steps-20260726.md
(and the matching rows in repo-reclaim-list-20260726.md).
Do NOT delete B/C/E or any §3 exclusion.
No filter-repo / force-push.
```

Alternate shapes (from #369 list): **A+B+D** (~233 MB) or **A–E** (~266 MB). Prefer A+D first.

### 1.1 Bucket A — published draft `images/` only (~188.6 MB)

Keep all `content/drafts/**/*.md`. Delete **image binaries under `images/` only** after a final WP media spot-check (public status already `publish`; Cloud secrets preferred for authenticated confirm).

| Path | ~Size | Live post ID | Slug |
|---|---:|---:|---|
| `content/drafts/2026-05-23-data-center-protest-signs/images/` | 40.2 MB | 11929 | `data-center-protest-signs` |
| `content/drafts/2026-05-16-why-we-built-the-responsible-ai-professional-certification/images/` | 33.3 MB | 12257 | `why-we-built-the-responsible-ai-professional-certification` |
| `content/drafts/2026-05-07-web-summit-vancouver-2026/images/` | 28.1 MB | 11826 | `web-summit-vancouver-2026` |
| `content/drafts/2026-05-13-sovereign-ai-for-whom/images/` | 22.8 MB | 11905 | `sovereign-ai-for-whom` |
| `content/drafts/2026-06-07-god-skills-agentic-loop-workflows/images/` | 21.6 MB | 12263 | `god-skills-agentic-loop-workflows` |
| `content/drafts/2026-06-04-ai-keynote-slides-visual-workflow/images/` | 7.8 MB | 12183 | `ai-keynote-slides-visual-workflow` |
| `content/drafts/2026-06-23-vancouver-made-world-cup/images/` | 7.2 MB | 12363 | `vancouver-made-world-cup` |
| `content/drafts/2026-06-04-the-great-canadian-proximity-game/images/` | 3.9 MB | 12190 | `the-great-canadian-proximity-game` |
| `content/drafts/2026-06-16-storyhive-haus-of-owl-jordan-dack/images/` | 3.8 MB | 12327 | `storyhive-haus-of-owl-jordan-dack` |
| `content/drafts/2026-05-24-what-would-chat-do-and-why-thats-the-wrong-question/images/` | 3.8 MB | 12032 | `what-would-chat-do-and-why-thats-the-wrong-question` |
| `content/drafts/2026-06-23-ethos-lab-block-party/images/` | 3.2 MB | 12357 | `ethos-lab-block-party` |
| `content/drafts/2026-05-24-canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one/images/` | 3.1 MB | 12030 | `canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one` |
| `content/drafts/2026-05-24-ai-wont-fix-your-broken-permit-process/images/` | 3.0 MB | 12035 | `ai-wont-fix-your-broken-permit-process` |
| `content/drafts/2026-07-07-the-cheer-is-a-cap-table/images/` | 2.9 MB | 12479 | `the-cheer-is-a-cap-table` |
| `content/drafts/2026-05-14-calling-us-all-in/images/` | 2.4 MB | 11765 | `calling-us-all-in` |
| `content/drafts/2026-07-05-artists-learn-machines-extract/images/` | 1.3 MB | 12473 | `artists-learn-machines-extract` |

Per-draft stub (add beside markdown when removing `images/`):

```markdown
<!-- assets: live in WP media (post-id NNNNN); repo originals recoverable from git history -->
```

### 1.2 Bucket D — report screenshots / capture spill (~24.1 MB)

Keep all `docs/current-state/reports/*.md` (especially `morning-truth-*.md`). Delete tracked screenshot binaries only. `.gitignore` already blocks new `reports/screenshots/` growth.

| Path | ~Size |
|---|---:|
| `docs/current-state/reports/screenshots/aurora-opal-20260701/` | 6.0 MB |
| `docs/current-state/reports/screenshots/aurora-opal-live-20260701/` | 6.0 MB |
| `docs/current-state/reports/screenshots/aurora-readability-*-20260701.png` (4 root files under `screenshots/`) | 5.3 MB |
| `docs/current-state/reports/screenshots/aurora-opal-1329-live-20260701/` | 1.9 MB |
| `docs/current-state/reports/screenshots/topic-hubs-20260701/` | 1.8 MB |
| `docs/current-state/reports/screenshots/content-architecture-20260701/` | 1.6 MB |
| `docs/current-state/reports/front-page-feature-pillars-final-polish-desktop-20260703-165421Z.png` | 1.1 MB |
| `docs/current-state/reports/front-page-feature-pillars-final-polish-mobile-20260703-165421Z.png` | 0.3 MB |
| Remaining tracked files under `docs/current-state/reports/screenshots/` | residual → delete whole tracked screenshots tree |

Small root JSON/HTML/CSV captures under `reports/` (~0.7 MB) are **not** in wave-1 unless KK adds them by path.

### 1.3 Hold for later (not wave-1)

| Bucket | ~Size | Why hold |
|---|---:|---|
| **B** `content/drafts/2026-05-23-you-cant-drink-data/photos/` | 20.7 MB | Source-like photo archive; KK call on outtakes vs WP media / LFS / gitignore |
| **C** unpublished / not-found draft `images/` (3 dirs) | 23.3 MB | Public miss ≠ safe; needs auth confirm of private/draft fate |
| **E** obsolete `backup/` QA dirs | 9.5 MB | May-25 QA docs may cite; separate review |

---

## 2. Staged delete PR recipe (safe A/D first)

One concern per PR. Prefer **two PRs** even inside A+D so rollback blast radius stays small.

### Wave 1a — Bucket D only (~24 MB) — docs/ops lane

1. Branch from `main`: `cursor/318-reclaim-delete-D-<short>`.
2. Confirm KK allow-list includes every path about to be removed.
3. Dry inventory (no delete yet):

```bash
git ls-files 'docs/current-state/reports/screenshots/**' \
  'docs/current-state/reports/front-page-feature-pillars-final-polish-*-20260703-165421Z.png'
du -sh docs/current-state/reports/screenshots \
  docs/current-state/reports/front-page-feature-pillars-final-polish-*-20260703-165421Z.png
```

4. Delete with `git rm -r` / `git rm` **only** approved paths.
5. Commit: `docs(#318): remove approved report screenshot captures`.
6. PR title: `docs(#318): reclaim report screenshots (bucket D)`.
7. PR body must paste the exact path list + link this next-steps doc + PR #502 list.
8. Merge only after KK approval (Cloud agents cannot approve).

### Wave 1b — Bucket A only (~189 MB) — content lane

1. Fresh branch from updated `main`: `cursor/318-reclaim-delete-A-<short>`.
2. For each slug in §1.1, re-verify publish + media still on WP (slug/ID match — `AGENTS.md` idempotency rule). Prefer authenticated REST when `WP_USER` / `WP_APP_PASSWORD` are present; public probe is a floor, not a ceiling.
3. Per approved dir:

```bash
# example — repeat only for KK-approved paths
git rm -r -- content/drafts/<draft-dir>/images
# add/adjust stub note in the draft markdown or a sibling ASSETS.md
```

4. Optionally extend `.gitignore` with `content/drafts/**/images/` (or per-draft rules mirroring `you-cant-drink-data/photos-raw/`) so images do not re-enter — call that out in the PR for KK.
5. Commit: `content(#318): remove published draft images (bucket A)`.
6. PR must include: allow-list paths, WP ID/slug proof table, stub note pattern, **no** B/C paths.
7. Do **not** mix theme / schema / redirect edits into this PR.

### Wave 2+ (after separate KK OK)

- **B:** decide delete vs Git LFS vs gitignore for `you-cant-drink-data/photos/`.
- **C:** auth-confirm unpublished drafts, then keep / LFS / delete.
- **E:** obsolete `backup/` dirs only after confirming May-25 QA docs may go history-only.
- **Phase C:** `git filter-repo` playbook (`CREDENTIAL-HISTORY-REWRITE-PREFLIGHT-2026-05-19.md`) — dedicated KK thread, mirror clone + dated tag first. Not this lane.

### Rollback for any wave

Until Phase C, every binary is recoverable via `git checkout <pre-delete-sha> -- <path>`. Record the pre-merge SHA in the PR description.

---

## 3. What NOT to delete (deploy handoffs + protected paths)

Copied from #369 § Exclusions preserved — **hard deny** even if someone asks for “full reclaim.”

### Deploy handoffs (active / indexed)

| Path | Why keep |
|---|---|
| `backup/aurora-deploy-20260724/` | Active Revive/Aurora **1.4.1** handoff + e2e/R9 evidence |
| `backup/aurora-deploy-20260716/` | CURRENT-STATE / WORK-PLAN **1.3.40** package + checksums |
| `backup/aurora-deploy-20260713/` | Auditable “do not upload 1.3.39” marker |
| `backup/aurora-deploy-20260614/` | Historical deploy handoff still indexed |

### Issue #76 / content rollback snapshots

| Path | Why keep |
|---|---|
| `backup/20260518-111546/` | #76 rollback — README |
| `backup/20260518-113350/` | #76 rollback — README |
| `backup/20260518-215912/` | #76 / Speaking rollback |
| `backup/20260518-223014/` | IA-polish rollback |
| `backup/20260518-224340/` | About rollback |

### Content-architecture / GSC / recovery evidence

| Path | Why keep |
|---|---|
| `backup/20260701T193335Z-content-architecture/` | Deploy snapshots |
| `backup/20260701T202734Z-content-architecture/` | Deploy snapshots |
| `backup/20260706T190831Z-content-architecture/` | Work visual-card snapshots |
| `backup/20260706T191550Z-content-architecture/` | Work visual-card final deploy |
| `backup/20260618-050328Z/` | GSC-404 before |
| `backup/20260618-050833Z/` | GSC-404 after |
| `backup/20260618-051950Z/` | a11y CTA hotfix |
| `backup/20260604-work-page-68/` | Work page metadata proof |
| `backup/20260525-201025Z/` | May-25 content recovery |
| `backup/20260525-220404Z/` | Events page after |
| `backup/2026-05-16/` | Manifest / checksums for `backup-check` |
| `backup/page-snapshots/` | Indexed page snapshot crumbs |

### Always keep (any wave)

- All `docs/current-state/reports/*.md` (esp. `morning-truth-*.md`)
- All `content/drafts/**/*.md` (and non-`images/` source text)
- Theme / plugins / scripts / schema / redirects (wrong lane)
- Any `backup/*/DEPLOY-HANDOFF.md` tree not on an explicit E allow-list
- Phase C history rewrite tooling as “cleanup” inside an A/D PR

---

## 4. Post-delete morning-truth checks

Run after each wave merges (or on the delete PR branch before merge). Prefer writing a report when allowed; otherwise stdout-only.

```bash
# Preferred when the session may write docs:
make morning-truth

# If the task forbids new report files:
make status-readonly
```

### Must-pass checklist

| Check | How | Pass criteria |
|---|---|---|
| Startup truth runs | `make morning-truth` or `make status-readonly` | Exit 0; WP smoke failures = `0` (warnings OK) |
| Markdown reports intact | `ls docs/current-state/reports/morning-truth-*.md \| tail` | Newest reports still present; no accidental `*.md` deletes |
| Deploy handoffs intact | `test -f backup/aurora-deploy-20260724/DEPLOY-HANDOFF.md` (and 0716/0713/0614) | Files exist; README links still resolve |
| #76 rollback dirs intact | `ls -d backup/20260518-{111546,113350,215912,223014,224340}` | All five dirs present |
| Bucket A markdown kept | `find content/drafts -name '*.md' \| wc -l` before/after | Count unchanged (or stubs added only) |
| Only allow-listed binaries gone | `git diff --name-status origin/main...HEAD` | Every deleted path ⊆ KK allow-list; zero §3 hits |
| Working-tree size moved | `du -sh content/drafts docs/current-state/reports backup` | Rough drop ≈ approved reclaim (A≈189M, D≈24M) |
| Validate still green | `make validate` | PHP/theme smoke still pass (unchanged by binary deletes) |
| Draft queue tooling | `LOCAL_ONLY=1 make draft-queue-audit` | Still runs; published drafts remain listed |

### Capture in the delete PR / closeout note

Paste into the PR (or a short `reports/repo-bloat-318-wave*-verify-YYYYMMDD.md`):

1. Pre-merge SHA + allow-list shape (`A+D` / etc.).
2. `du -sh` before/after for `content/drafts`, `reports`, `backup`.
3. Morning-truth (or status-readonly) summary lines: WP version, smoke failures, open PR/issue counts.
4. Explicit statement: “No deploy handoff or #76 rollback path touched.”
5. Reminder: `.git` size will **not** shrink until Phase C.

---

## 5. Sequencing summary

```text
PR #502 list (#369)  →  KK path allow-list (prefer A+D)
        →  Wave 1a delete D (docs)
        →  morning-truth checks
        →  Wave 1b delete A (content) + stubs + optional gitignore
        →  morning-truth checks
        →  separate KK thread for B/C/E
        →  only then Phase C filter-repo (mirror + force-push coordination)
```

### Acceptance for this next-steps doc

- [x] Points at #369 / PR #502 ranked list
- [x] Exact A+D path allow-lists for KK paste-approval
- [x] Staged delete PR recipe (D then A); no deletes executed here
- [x] Hard exclusions for deploy handoffs / rollbacks / markdown
- [x] Post-delete morning-truth / status-readonly verification recipe
- [ ] KK approval on #369/#318 (human)
- [ ] Wave delete PRs (future session)

---

**Sources:** `repo-reclaim-list-20260726.md` (PR #502), `REPO-HYGIENE-AUDIT-2026-07-12.md`, `reports/issue-318-phase-b-reclaim-inventory-20260716.md`, `AGENTS.md` hard safety rules, `CURRENT-STATE-2026-07-16.md` + README deploy/rollback citations.
