# #318 repo bloat — current remaining-bloat remeasure (2026-08-16)

**Status:** measurement + recommendation only. **No deletes, no `git rm --cached`, no history rewrite.**
**Issue:** [#318](https://github.com/WalksWithASwagger/kriskrug-wp/issues/318), related [#737](https://github.com/WalksWithASwagger/kriskrug-wp/issues/737), [#749](https://github.com/WalksWithASwagger/kriskrug-wp/issues/749)
**Measured against:** `origin/main` `59505f1` (2026-08-16), local checkout at `/Users/kk/Code/kriskrug-wp`
**Does not duplicate:** [#800](https://github.com/WalksWithASwagger/kriskrug-wp/pull/800) (merged — `backup/` JSON-keep decision + archive proposal) or [#795](https://github.com/WalksWithASwagger/kriskrug-wp/pull/795) (closed as CONFLICTING/out-of-scope, not merged — see §4)

---

## 1. Headline numbers

| Metric | Current | Prior baseline | Source |
|---|---:|---:|---|
| Working tree (all files, `du -sh .`) | 2.9 GiB | ~1.8 GiB pre-reclaim → ~1.5 GiB (2026-08-05) | #318 comment, 2026-08-05 |
| `.git` | 426 MiB | ~295 MiB (2026-07-12 audit) / ~352 MiB (2026-08-03) | #317 audit, PR #558 |
| **Tracked content** (`git ls-files`, sum of on-disk bytes) | **104.2 MiB / 2,249 files** | ~129.5 MiB pre-wave-2 → ~85.5 MiB post-#679 | PR #679 |
| `backup/` tracked | 15.60 MiB / 403 files | 14.72 MiB / 403 files (2026-08-16, same-day proposal) | #737 proposal doc |
| `content/drafts/` tracked | 62.32 MiB / 770 files | — | this measurement |
| `content/drafts/` tracked **images** | 55.20 MiB / 71 files | Bucket B+C = 44.0 MiB per #679 (numbers drift as drafts are added/removed) | PR #679 |
| `content/drafts/` on-disk (tracked + ignored) | 706 MiB | 683 MiB (2026-08-05) | #318 comment |
| `docs/` tracked | 10.81 MiB / 436 files | — | this measurement |
| `docs/` on-disk (tracked + ignored) | 370 MiB | ~2.3 GiB claimed in #749 (2026-08-15) | #749 |

Working tree and `.git` both grew since the last dated snapshot (2.9 GiB / 426 MiB vs 1.5 GiB / 352 MiB) — expected, since normal work (theme/content commits, new draft folders, new backup snapshots) continues between audits. The **tracked** total (104.2 MiB) is what actually matters for clone/checkout cost, and it has been shrinking steadily: ~129.5 MiB → 85.5 MiB (#679) → 104.2 MiB now (new tracked content added since, e.g. `fv-ai-launch` images, new `backup/` manifests — see §3.2).

Method note: summed `git ls-files -z | xargs -0 du -k` across **all** batches with `awk`, not `du -c | tail -1` (the latter only reports the last xargs batch's subtotal on a file list this size and silently under/over-counts — verified by cross-checking both methods before trusting either number in this report).

---

## 2. Per-target findings

### 2.1 `backup/` (#737)

- **403 tracked files, 15.60 MiB.** Matches the #737/[#800](https://github.com/WalksWithASwagger/kriskrug-wp/pull/800) proposal count exactly (403 files); bytes are ~0.9 MiB higher than the 2026-08-16 proposal snapshot because one more `manifest-*.json` (`manifest-20260816T151617Z.json`) landed same-day.
- **Ignore gap is closed.** `backup/**/*.html` and `backup/**/*.png`/`*.jpg`/`*.jpeg` are in `.gitignore` (commit `f684f17`, confirmed live via `git check-ignore -v backup/test.html`). No new spill.
- **Execution not done.** The KK-approval packet (`docs/current-state/reports/issue-737-backup-tree-archive-proposal-20260816.md`, landed in #800) has an exact allow-list — `git rm --cached` 129 HTML + 2 leftover PNG (~7.89 MiB), archive-copy first to `/Users/kk/Code/_archive/kriskrug-wp/backup-tracked-tree-2026-08-16/` — but **#737 has zero comments** and no KK reply. Nothing has been cached-rm'd; `git ls-files backup/ | wc -l` is still 403, exactly as the proposal predicted it would remain until that reply lands.
- **Remaining work:** small (~7.9 MiB), fully speced, blocked only on a one-line KK approval + a mechanical follow-up PR. Low risk, low effort.

### 2.2 `content/drafts/` images (#318 Phase B)

- **706 MiB on disk**, but only **62.32 MiB / 770 files tracked**. The blanket `content/drafts/**/images/` ignore rule (line 102) already stops *new* spill — confirmed no drafts added since have leaked images into the index.
- Untracked bulk is dominated by `2026-05-23-you-cant-drink-data/photos-raw/` (560 MiB, correctly ignored per the per-draft rule at line 60) — this is local-only working material, not repo bloat.
- **71 tracked legacy images, 55.20 MiB**, remain across 6 draft folders:

| Draft | Tracked images | Notes |
|---|---:|---|
| `2026-05-23-you-cant-drink-data` | 53 | PR #679 "Bucket B" — needs KK call (outtakes vs WP media vs LFS) |
| `2026-05-24-human-element-shane-loki-talk` | 7 | PR #679 "Bucket C" — needs publish-status confirm |
| `2026-05-25-cotton-underwear-paradox` | 4 | same |
| `2026-09-09-fv-ai-launch` | 4 | future-dated event (Sep 2026) — almost certainly still in-flight, should stay untouched |
| `2026-05-24-how-we-did-it-behind-the-scenes-of-the-sfu-siat-microcredential-project` | 2 | PR #679 "Bucket C" |
| `2026-07-31-both-hands-on-the-power-cord` | 1 | recently added |

- This is **exactly** the work #679 explicitly deferred ("Bucket B... needs KK call", "Bucket C... needs authenticated publish-status confirmation") and exactly what the #318 2026-08-05 comment calls the Phase B gate: `LOCAL_ONLY=1 make draft-queue-audit` + live slug readback needs `WP_USER`/`WP_APP_PASSWORD`. Redacted presence check in this session: **both unset**, so Phase B execution is not possible from here — confirms the gate is still live, not just historically true.
- **Remaining work: real and un-owned.** No other open issue tracks this (#737 is `backup/`-only; #749 is visual-baseline-only). This is #318's own unfinished Phase B.

### 2.3 `docs/` (#749)

- **370 MiB on-disk**, **10.81 MiB / 436 files tracked**. The gap is almost entirely `docs/current-state/reports/visual-baseline/` (359 MiB), of which only 20 JSON/MD files are tracked (the PNGs are correctly gitignored per `!docs/.../visual-baseline/README.md` negation + blanket ignore).
- On **this machine**, only **one** capture directory remains on disk (`20260811T033217Z/`, ~359 MiB), not the seven sets (~2.3 GiB) that #749's 2026-08-15 audit found. That audit's "~2.3GB" figure is stale for this checkout — most of the historical sets are already gone here, whether from a prior manual prune or normal `visual-prune` usage. PR #795's cloud-VM run separately found 0 MiB to free (no PNG dirs there at all), so state genuinely differs by machine/worktree — #749 was written for a specific machine snapshot and needs a fresh per-machine check, not a blanket "still 2.3 GiB" assumption.
- The current on-disk set (`20260811T033217Z`, Aug 10) is **not** the newest manifest (`manifest-20260816T151617Z.json`, Aug 16 — no matching capture dir on disk), so it isn't even the active baseline; it's stale by #749's own logic.
- **#749's doc acceptance criterion is unmet:** "retention note added to the visual-baseline README" — no `README.md` exists on disk in that directory today (the `.gitignore` negation for it is a no-op; nothing to un-ignore). Trivial, doc-only gap.
- Per the issue's own rule ("Never touch tracked files" / "deletion list first, KK approval, then rm"), **no deletion was performed here.** This machine's remaining reclaimable amount is ~359 MiB (one stale set), well under the original ~2.3 GiB estimate — worth a fresh KK-approved delete-list pass, but it is a shrinking, low-priority problem, not the ~2.3 GiB the issue currently states.

---

## 3. What's already done (do not repeat)

- **Phase A** (#318): orphaned `reports/`/`backup/` artifact prune — PR #317, merged 2026-07-12.
- **Reclaim waves 1+2** (#369, closed): PR #558 (~212 MiB, Buckets A+D) + PR #679 (~44 MiB, four safe buckets) — tracked content dropped from ~129.5 MiB to ~85.5 MiB. Bucket B (YCDD photos) and Bucket C (unpublished drafts) explicitly deferred, pending publish-status auth — this is what's left in §2.2.
- **`backup/` ignore-gap close** (#737): `backup/**/*.html` + `*.png`/`*.jpg`/`*.jpeg` rules landed in `f684f17`. JSON-keep decision recorded and archive-copy/cached-rm proposal drafted and merged via [#800](https://github.com/WalksWithASwagger/kriskrug-wp/pull/800). **Not yet executed** (needs KK reply) — see §2.1, this is the one real remaining #737 slice, already fully speced.
- **Phase C decision** (#572, closed 2026-08-03): formally deferred via PR #664. Not blocked — just decided "not now." No new information in this report changes that call; `.git` at 426 MiB is unchanged in status, only in raw size (grows with every commit regardless).
- **#740/#738/#749 execution attempt** ([#795](https://github.com/WalksWithASwagger/kriskrug-wp/pull/795)): **closed, not merged** — held as `CONFLICTING` with `main` after #804/#785 landed, and flagged for archiving 26 files versus the 9-file list KK actually approved. KK's own closing comment: "The 9-plan archive is already on main" (via #785) — so #740's approved slice did land, just not through #795. #738 (branch/worktree sweep) and #749 (visual-baseline prune) from that same PR are **still open and not executed** anywhere else I can find. This report does not attempt #738/#740/#749 execution (already covered by those dedicated issues) and does not duplicate #795's abandoned diff.

---

## 4. Recommendation: keep #318 open, narrow its scope — do not close in favor of #737

**Do not close #318 yet.** #737 only ever covered the `backup/` slice (its own title says "final slice of #318" for `backup/` specifically). Closing #318 in favor of #737 would silently drop **Phase B** (§2.2: 71 tracked images / 55.2 MiB, real, un-owned, gated on `WP_USER`/`WP_APP_PASSWORD` credentials for publish-status confirmation), which has no other tracking issue.

This matches the plan the repo already recorded for itself: the merged #800 proposal doc's own next step is *"After that PR [the #737 cached-rm] lands, update #318 to point at #737 as the closed `backup/` slice (draft-images residue stays on #318)"* — i.e., #318 was always meant to survive #737, just get smaller.

**Recommended disposition:**

1. **#737** — stays open, unchanged scope. It has a fully-speced, low-risk allow-list waiting on one KK reply (§2.1). Nothing here duplicates or supersedes it.
2. **#749** — stays open, but its stated "~2.3GB" figure is stale for at least this machine (§2.3: currently 359 MiB, one stale set). Recommend a fresh per-machine `du -sh docs/current-state/reports/visual-baseline/*` check before any delete-list, and separately closing the doc-only "retention note" gap (no code risk).
3. **#318** — keep open, but **once #737's cached-rm PR lands**, edit the #318 body to: strike Phase A (done) and the `backup/` bullet under Phase B (now #737's), keep only the draft-images publish-status item, and cross-reference #572 for Phase C instead of restating it. That turns #318 into a single, actionable, credential-gated task instead of an umbrella that reads as three separate problems.

No edits to #318/#737/#749 issue bodies were made in this PR — recommendation only, per the "report what to do" scope of this task.

---

## 5. Numbers KK can quote directly

```text
backup/ tracked:        403 files, 15.60 MiB — unchanged, waiting on #737 approval reply
content/drafts/ tracked images: 71 files, 55.20 MiB — Phase B gate, needs WP_USER/WP_APP_PASSWORD
docs/ visual-baseline on disk (this machine): 359 MiB, 1 stale set — down from #749's claimed 2.3 GiB
Tracked working-tree total: 104.2 MiB / 2,249 files — down from 129.5 MiB pre-#679
.git: 426 MiB — Phase C deferred by #572, unchanged status
```
