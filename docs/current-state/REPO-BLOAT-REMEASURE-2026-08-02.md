# Repo Bloat Remeasure (issue #318, Phase B)

**Measured:** 2026-08-02
**Subject:** the main checkout at `/Users/kk/Code/kriskrug-wp`, HEAD `dd87d4a` (`origin/main`, clean tree)
**Supersedes the numbers in:** [`REPO-HYGIENE-AUDIT-2026-07-12.md`](REPO-HYGIENE-AUDIT-2026-07-12.md) §3
**Scope:** read-only measurement. No deletes, no `gc`, no history rewrite, no live-site calls.

The 2026-07-12 audit's headline (`working tree ~332M`, `.git ~295M`, `627M total`) is now wrong in both
directions. The working tree shrank a lot more than the audit expected. `.git` grew. This doc replaces
those numbers and hands the history-rewrite figures to issue #572 without making that call.

---

## 0. The three numbers, kept separate

Conflating these is exactly the mistake this doc exists to prevent. A naive `du -sh` of the repo root
right now returns **4.6 GiB**, and roughly three quarters of that is other agents' scratch space.

| # | Number | Value | What it actually is |
|---|---|---:|---|
| 1 | **Tracked content** | **129.5 MiB** (2,146 files) | Sum of every blob in the `HEAD` tree. The thing Phase B can delete. |
| 2 | **`.git`** | **403 MiB** | The object store plus per-worktree admin. Only a history rewrite moves the bulk of it. |
| 3 | **Worktree overhead** | **3.4 GiB** (26 live worktrees) | `.claude/worktrees/`. Transient. Not repo bloat. Not anybody's Phase B target. |

Supporting figure: the working tree on disk excluding `.git` and `.claude` is **806.5 MiB**, of which only
129.5 MiB is tracked. The other **~677 MiB is gitignored working material** (§6). It has never been in git
and a Phase B delete pass cannot reclaim it, because there is nothing to delete from the index.

Arithmetic check on the naive root `du`: 3.41 GiB (`.claude`) + 0.394 GiB (`.git`) + 0.787 GiB (working
tree) = 4.59 GiB. That accounts for the whole 4.6 GiB.

---

## 1. Method (exact commands)

Every number below is reproducible. Run these from `/Users/kk/Code/kriskrug-wp`, not from a worktree.

```bash
# 1. Naive root du, plus the two things that must be subtracted from it
du -sk .                       # 4,814,072 KB  = 4.59 GiB
du -sk .git .claude            #   413,100 KB  = 403.4 MiB  /  3,575,132 KB = 3.41 GiB
du -sh .claude/worktrees       # 3.4G
ls -1 .claude/worktrees | wc -l   # 26

# 2. .git internals
git count-objects -vH
du -sh .git/*

# 3. Tracked content at HEAD (sum of blob sizes, not du, so block slack does not inflate it)
git ls-tree -r -l HEAD | awk '{s+=$4} END {printf "%.1f MiB\n", s/1048576}'
git ls-files | wc -l

# 4. Same at any past commit, for the timeline in §3
git ls-tree -r -l <sha> | awk '{s+=$4} END {printf "%.1f MiB\n", s/1048576}'

# 5. Largest tracked files still in the tree
git ls-files -z | xargs -0 stat -f '%z %N' | sort -rn | head -30

# 6. Largest blobs anywhere in the history that a fresh clone would download
git rev-list --objects origin/main \
  | git cat-file --batch-check='%(objecttype) %(objectsize) %(objectsize:disk) %(rest)' \
  | awk '$1=="blob" && NF>3' | sort -k3 -rn | head -30

# 7. What a fresh `git clone` actually costs
git rev-list --objects origin/main | awk '{print $1}' \
  | git cat-file --batch-check='%(objecttype) %(objectsize) %(objectsize:disk)' \
  | awk '{raw[$1]+=$2; disk[$1]+=$3; n[$1]++} END {for(k in raw) print k, n[k], raw[k], disk[k]}'
```

Two measurement notes that matter:

- `%(objectsize:disk)` is the packed, delta-compressed, zlib size. That is the number that predicts what a
  rewrite reclaims. `%(objectsize)` (raw) overstates it for text and understates nothing. For the PNG-heavy
  buckets the two are nearly identical, because PNGs do not delta or deflate.
- `git ls-tree -r -l` sums logical file sizes. `du` sums 4 KiB block allocations plus untracked files. For a
  2,146-file tree the block slack is a few MiB. Where this doc quotes a `du` figure it says so.

---

## 2. `.git`: 403 MiB, and it grew

```
count: 3084            size: 45.70 MiB      (loose objects)
in-pack: 7551          size-pack: 346.63 MiB (9 packs)
prune-packable: 160    garbage: 0
```

| Component | Size | Note |
|---|---:|---|
| `.git/objects/pack` | 347 MiB | One 334 MiB pack written 2026-08-01 19:38, plus 8 small packs totalling ~12 MiB |
| `.git/objects` loose | 45.7 MiB | 3,084 loose objects, 160 already prune-packable. Churn from 26 concurrent agent worktrees. |
| `.git/worktrees` | 8.3 MiB | Per-worktree index and admin files, one set per live worktree |
| `.git/cursor` | 1.5 MiB | Cursor tooling state |
| `.git/logs`, `index`, `refs`, rest | ~1.1 MiB | |

**Fresh clone cost** (everything reachable from `origin/main`, which is what a new machine downloads):

| Object type | Count | Raw | Packed |
|---|---:|---:|---:|
| blob | 3,676 | 361.8 MiB | **314.6 MiB** |
| tree | 3,422 | 4.3 MiB | 1.0 MiB |
| commit | 804 | 0.7 MiB | 0.5 MiB |
| **total** | **7,902** | **366.8 MiB** | **316.1 MiB** |

So the honest "what does this repo cost to clone" number is **316 MiB**, and 314.6 MiB of that is blobs.
The 403 MiB local `.git` is 316 MiB of real history plus ~87 MiB of local churn (loose objects, redundant
packs, worktree admin) that a `git gc` would mostly fold away without touching history.

### Why it grew when the tree shrank

The audit measured 295 MiB on 2026-07-12. It is 403 MiB now, a gain of ~108 MiB, in the same three weeks
that PR #558 deleted 212.7 MiB of tracked binaries. That is not a contradiction, it is the entire premise
of Phase C: **`git rm` removes a file from the tree and leaves the blob in the pack forever.** Every byte
#558 reclaimed from the working tree is still sitting in `.git/objects/pack`.

The +108 MiB itself breaks down as roughly: 45.7 MiB of loose objects and 8.3 MiB of worktree admin created
by the concurrent-agent workflow, ~1.5 MiB of Cursor state, and the rest from three weeks of ordinary commits
plus the 2026-08-01 repack changing how much redundancy sits across the 9 packs. None of it is content the
repo needs to carry.

---

## 3. Tracked-content timeline, and the reconciliation

| Commit | Date | Tracked files | Tracked bytes | Event |
|---|---|---:|---:|---|
| `c69465f` | 2026-07-13 | 1,600 | **321.1 MiB** | Nearest `main` commit to the 2026-07-12 audit |
| `c369eef` | 2026-07-31 | 1,960 | **332.9 MiB** | Parent of the reclaim commit |
| `d8d5e44` | 2026-07-31 | 1,797 | **120.2 MiB** | PR #558 `ops(#369): reclaim A+D binaries` |
| `dd87d4a` | 2026-08-02 | 2,146 | **129.5 MiB** | HEAD, today |

**PR #558 removed exactly 212.7 MiB across 163 deleted files** (97 under `content/drafts/`, 82 under
`docs/current-state/`, plus 3 added `.gitignore` lines and stub `ASSETS.md` files). Verified by summing
`git cat-file -s` over every `D` path in `git diff-tree -r --name-status d8d5e44`. The PR title's "~212 MB"
is accurate to the byte.

### Reconciling the audit's `332M` / `295M`

The audit's `332M` was a `du` figure. At the nearest commit the tracked content was 321.1 MiB, and the audit-era
tracked buckets were `content/drafts` 235.7 MiB, `content/source-packs` 34.9 MiB, `docs` 31.7 MiB, `backup`
16.7 MiB. Those line up with the audit's own per-folder claims (`content/drafts` 238M, `docs` 38M, `backup` 19M)
once you allow for `du` block slack and a small amount of untracked spill folded into each folder's number.
**The audit's 332M was essentially a tracked-content measurement, and it was correct at the time.**

The gap between then and now is fully explained:

```
321.1 MiB  tracked at 2026-07-13
 +11.8 MiB  net additions through 2026-07-31 (source-packs assets, reports, drafts)
=332.9 MiB  tracked immediately before PR #558
-212.7 MiB  PR #558 reclaim (buckets A + D from the #369 list)
=120.2 MiB  tracked immediately after PR #558
  +9.3 MiB  additions 2026-07-31 to 2026-08-02 (see §7)
=129.5 MiB  tracked at HEAD dd87d4a
```

No unexplained residual. The post-#558 expectation was 332.9 minus 212.7, which is 120.2, and that is what
landed. The stated Phase B target of "up to ~238M working tree" was met in the sense that the largest and
best-verified 189 MiB slice of it (bucket A, published-draft images) is gone.

---

## 4. What is already done

Do not re-plan any of this.

| Item | Status | Evidence |
|---|---|---|
| Phase A orphan prune (~6.9 MiB) | Done | PR #317, 2026-07-12 |
| Ranked reclaim inventory | Done | `reports/repo-reclaim-list-20260726.md` (#369), `reports/repo-bloat-318-next-steps-20260726.md` (#539) |
| Bucket A: published-draft `images/` (~189 MiB) | **Done** | PR #558 / `d8d5e44`, 97 files under `content/drafts/` |
| Bucket D: report screenshot captures (~24 MiB) | **Done** | PR #558 / `d8d5e44`, 82 files under `docs/current-state/` |
| Go-forward ignore for draft images | **Done** | `.gitignore:98` `content/drafts/**/images/`, added by #558 |
| Go-forward ignore for report captures | Done | `.gitignore:71-74` (screenshots, `*.png`, `*.html`, `*.csv`) |
| Go-forward ignore for `backup/` captures | Done | `.gitignore:93-95` (`backup/**/*.png|jpg|jpeg`) |
| Go-forward ignore for visual-baseline artifacts | Done | `.gitignore:83-87`, deny-by-default with named re-includes |

The `.gitignore` policy question in the issue's Phase B checklist ("decide the go-forward policy for
`content/drafts/**/images/`") is **closed**. The rule is in place. It stops new images entering the index.
It does not, and cannot, untrack the 83 image files that were already tracked when it landed.

Residual proof that the deletes did not overreach: `docs/current-state/reports/` now carries 181 tracked
files totalling 3.61 MiB, and the largest non-markdown survivor is a 0.19 MiB CSV. Every
`morning-truth-*.md` and report `.md` is intact.

---

## 5. What Phase B still has (the real remaining targets)

Tracked bytes at HEAD, grouped:

| Bucket | Tracked | Files |
|---|---:|---:|
| `content/drafts/**/{images,photos}/` | **49.31 MiB** | 83 |
| `content/source-packs/**/verification/` | **30.88 MiB** | 53 |
| `backup/**` | **23.39 MiB** | 449 |
| `content/source-packs/**` (other) | 9.99 MiB | 158 |
| `docs/**` (excluding `reports/`) | 5.02 MiB | 196 |
| `content/drafts/**` (markdown and text) | 3.76 MiB | 626 |
| `docs/current-state/reports/**` | 3.61 MiB | 181 |
| `scripts/**` | 1.59 MiB | 166 |
| everything else | 1.10 MiB | 185 |
| `theme/**` | 0.85 MiB | 49 |
| **total** | **129.5 MiB** | **2,146** |

### 5a. Draft image dirs still tracked (49.31 MiB)

| Path | Tracked | Files | #369 bucket |
|---|---:|---:|---|
| `content/drafts/2026-05-24-human-element-shane-loki-talk/images/` | 18.32 MiB | 7 | C (unpublished / not-found) |
| `content/drafts/2026-05-23-you-cant-drink-data/photos/gallery/` | 10.26 MiB | 27 | B |
| `content/drafts/2026-05-23-you-cant-drink-data/photos/best/` | 7.14 MiB | 22 | B |
| `content/drafts/2026-07-26-futureproof-festival-announcement/images/` | 4.32 MiB | 6 | none (post-dates the list) |
| `content/drafts/2026-05-23-you-cant-drink-data/photos/inbody/` | 3.33 MiB | 7 | B |
| `content/drafts/2026-05-24-how-we-did-it-behind-the-scenes-of-the-sfu-siat-microcredential-project/images/` | 2.75 MiB | 2 | C |
| `content/drafts/2026-05-25-cotton-underwear-paradox/images/` | 2.22 MiB | 4 | C |
| six single-file `2026-05-19-*/images/` dirs | 0.99 MiB | 6 | residual |

Cross-check against the #369 list: bucket B was quoted at 20.7 MB and the three `you-cant-drink-data/photos/`
subdirs sum to 20.73 MiB. Bucket C was quoted at 23.3 MB and the three C dirs sum to 23.29 MiB. Both match,
which confirms #558 took A and D cleanly and left B and C untouched as instructed.

The one genuinely new item is `2026-07-26-futureproof-festival-announcement/images/` (4.32 MiB, 6 files). That
draft was created on 2026-07-26 and its images were committed before the `.gitignore:98` rule landed on
2026-07-31, so the rule never saw them. This is the leak the ignore rule now closes, caught once.

### 5b. `content/source-packs/**/verification/` (30.88 MiB, 53 files)

This is now the **second largest tracked bucket and it has never been scoped into any Phase B wave.** The
#369 reclaim list did not cover it, and the issue text mentions it only in the Phase C rewrite bullet. It is
plain screenshot evidence from May 2026 page-QA runs, including the single largest tracked file in the repo:

```
5.97 MiB  content/source-packs/keynotes-2026/verification/screenshots-polish-20260518-123159-scrolled/contact-sheet-full.png
3.04 MiB  content/source-packs/keynotes-2026/verification/screenshots/about-desktop.png
2.34 MiB  content/source-packs/keynotes-2026/verification/screenshots-horizons-20260518-215912/contact-sheet-full.png
2.29 MiB  content/source-packs/keynotes-2026/verification/screenshots-appearances-20260518-214007/contact-sheet-full.png
2.17 MiB  content/source-packs/keynotes-2026/verification/screenshots/speaking-desktop.png
```

Note that no `.gitignore` rule covers `content/source-packs/**`, so this folder can still grow. If a future
wave takes it, the ignore rule should land in the same PR.

### 5c. `backup/**` (23.39 MiB, 449 files)

Mostly already protected by the hard-deny list in `reports/repo-bloat-318-next-steps-20260726.md` §3
(deploy handoffs, issue #76 rollback dirs, content-architecture snapshots). The only #369 bucket E candidates
are the two May-25 QA visual dirs:

| Path | Tracked | Files |
|---|---:|---:|
| `backup/20260525-qa-visual-134/` | 4.45 MiB | 26 |
| `backup/20260525-qa-visual/` | 4.29 MiB | 23 |

That is 8.74 MiB against the 9.5 MB the #369 list quoted for bucket E. The remainder of `backup/` is
handoff and rollback evidence that stays.

### 5d. Ceiling for the whole of Phase B

| Wave | Tracked reclaim | Note |
|---|---:|---|
| B (`you-cant-drink-data/photos/`) | 20.73 MiB | KK call: outtakes vs WP media vs LFS |
| C (three unpublished draft `images/`) | 23.29 MiB | Needs authenticated publish-status confirm |
| Futureproof announcement `images/` | 4.32 MiB | Post-dates the #369 list, needs its own status check |
| E (two May-25 QA visual dirs) | 8.74 MiB | Confirm no May-25 doc cites them |
| `source-packs/**/verification/` (new) | 30.88 MiB | Never scoped, needs a fresh KK pass |
| residual `2026-05-19-*` image dirs | 0.99 MiB | Trivial, fold into whichever wave runs |
| **Phase B remaining ceiling** | **~88.9 MiB** | |

If every remaining Phase B target is approved and deleted, tracked content drops from 129.5 MiB to
**~40.6 MiB**, and `.git` does not move by a single byte.

---

## 6. What is on disk but has never been in git

The working tree excluding `.git` and `.claude` is 806.5 MiB on disk against 129.5 MiB tracked. The
~677 MiB difference is gitignored working material. It is worth naming because it is what makes a naive
`du content/` look catastrophic (`content/` reads 728 MiB, and 675 MiB of that git has never seen):

| Path | On disk | Ignored by |
|---|---:|---|
| `content/drafts/2026-05-23-you-cant-drink-data/photos-raw/` | 560 MiB | `.gitignore:59` |
| `content/drafts/2026-07-31-both-hands-on-the-power-cord/images/` | 43 MiB | `.gitignore:98` (the new rule, working as intended) |
| `scripts/notion-to-wp/.venv/` | 36 MiB | `.gitignore:53` |
| `content/drafts/2026-05-23-you-cant-drink-data/contact-sheets/` | 20 MiB | `.gitignore:60` |
| `content/drafts/2026-07-24-contact-421/screenshots/` | 6.5 MiB | nested `content/drafts/2026-07-24-contact-421/.gitignore:1` |
| `.ruff_cache`, `.pytest_cache`, `__pycache__` | ~0.5 MiB | `.gitignore` |

`git status --porcelain --untracked-files=all` returns nothing on the main checkout, so the ignore coverage
is complete: everything on disk is either tracked or deliberately ignored. There is no untracked spill
waiting to be accidentally committed.

**The 43 MiB `both-hands-on-the-power-cord/images/` entry is the proof the new rule works.** That draft
landed on 2026-07-31 with 43 MiB of images and none of them entered the index.

---

## 7. Regrowth watch

Between `d8d5e44` (2026-07-31) and `dd87d4a` (2026-08-02), tracked content went from 120.2 MiB to 129.5 MiB,
a gain of **9.3 MiB across 349 new files in two days**. Largest contributors:

```
0.15 MiB  scripts/events_page/heroes/one-offs-2025/2025-07-11-bass-coast-brain-stage-youtube.jpg
0.14 MiB  content/source-packs/keynotes-2026/assets/press-2026-02-05-vanmag-power50-context-v2.jpg
0.13 MiB  content/source-packs/keynotes-2026/assets/press-2026-07-24-the-tyee-context-v2.jpg
0.13 MiB  content/source-packs/keynotes-2026/assets/press-2025-05-01-portfolio-yvr-context-v2.jpg
0.12 MiB  content/source-packs/keynotes-2026/assets/press-2024-08-22-techcouver-context.jpg
```

No single file is large. The pattern is `content/source-packs/keynotes-2026/assets/` press thumbnails and
`scripts/events_page/heroes/` hero images accumulating at roughly 100 KiB each. At the observed rate the
repo re-adds the entire Phase B remaining ceiling in about 19 days. Neither path has a `.gitignore` rule.

This is not urgent, and these files are legitimately referenced content rather than capture spill. It is
noted so that whoever runs the next wave decides deliberately whether these paths get a policy or stay
free-form. **Recommend a threshold check rather than a blanket rule**, since the images are real assets.

---

## 8. Handoff to issue #572 (numbers only, no decision)

Issue #572 owns the `git filter-repo` decision. It is not made here. These are the figures it needs.

**Baseline: a fresh clone of `origin/main` downloads 316.1 MiB.** Blob bytes by path, packed
(`%(objectsize:disk)`, reachable from `origin/main`):

| Path bucket | Packed | Raw | Blobs | Share of the 314.6 MiB blob total |
|---|---:|---:|---:|---:|
| `content/drafts/**/{images,img,photos,photos-raw,contact-sheets}/` | **237.3 MiB** | 238.7 MiB | 179 | **75.4%** |
| `content/source-packs/**/verification/` | **28.5 MiB** | 29.0 MiB | 70 | 9.1% |
| `docs/current-state/reports/**` | **25.2 MiB** | 33.0 MiB | 281 | 8.0% |
| `backup/**` | 11.6 MiB | 22.3 MiB | 448 | 3.7% |
| `content/source-packs/**` (other) | 6.7 MiB | 10.1 MiB | 249 | 2.1% |
| `content/drafts/**` (text) | 1.5 MiB | 5.1 MiB | 820 | 0.5% |
| `theme/**` | 1.3 MiB | 9.1 MiB | 307 | 0.4% |
| `docs/**` (other) | 1.2 MiB | 8.4 MiB | 543 | 0.4% |
| `scripts/**` | 0.6 MiB | 3.3 MiB | 347 | 0.2% |
| everything else | 0.8 MiB | 2.7 MiB | 432 | 0.3% |

Within `docs/current-state/reports/**`, the 25.2 MiB packed splits as 23.51 MiB of `.png` (82 blobs),
1.18 MiB of `.json` (37), 0.46 MiB of `.md` (158), and 0.08 MiB of `.html`/`.csv`/`.css`. **The 158 report
markdown blobs, the whole committed audit trail, cost 0.46 MiB.** Nothing about protecting them constrains
a rewrite.

Ten largest individual blobs in `origin/main` history, all PNGs, all already deleted from the working tree
by PR #558 except where noted:

```
7.79 MiB  content/drafts/2026-05-13-sovereign-ai-for-whom/images/01-sovereign-ai-for-whom.png
5.97 MiB  content/source-packs/keynotes-2026/verification/screenshots-polish-20260518-123159-scrolled/contact-sheet-full.png   [STILL TRACKED]
5.27 MiB  content/drafts/2026-05-13-sovereign-ai-for-whom/images/03-sovereign-ai-for-whom.png
4.21 MiB  content/drafts/2026-05-13-sovereign-ai-for-whom/images/04-sovereign-ai-for-whom.jpg
3.93 MiB  content/drafts/2026-06-07-god-skills-agentic-loop-workflows/images/99-optional-from-intent-to-ship-review-required.png
3.72 MiB  content/drafts/2026-05-23-data-center-protest-signs/images/03-my-position-yes-also-help.png
3.66 MiB  content/drafts/2026-06-07-god-skills-agentic-loop-workflows/images/04-canonical-skill-routing-dashboard.png
3.61 MiB  content/drafts/2026-06-07-god-skills-agentic-loop-workflows/images/05-skill-dispatch-matrix.png
3.55 MiB  content/drafts/2026-06-07-god-skills-agentic-loop-workflows/images/03-god-skills-invocation-cheat-sheet.png
3.52 MiB  content/drafts/2026-05-23-data-center-protest-signs/images/06-who-s-a-thirsty-little-data-center.png
```

Sensitivity, for whatever path filter #572 lands on:

| Filter | Blob bytes left | Clone cost after | Reclaimed |
|---|---:|---:|---:|
| none (today) | 314.6 MiB | 316.1 MiB | 0 |
| drafts image dirs only | 77.3 MiB | 78.8 MiB | **237.3 MiB (75%)** |
| + `source-packs/**/verification/` | 48.8 MiB | 50.3 MiB | 265.8 MiB (84%) |
| + `reports/**/*.png` | 25.3 MiB | 26.8 MiB | 289.3 MiB (92%) |
| + `backup/**` binaries | ~14 MiB | ~15 MiB | ~300 MiB (95%) |

Two things #572 should know before choosing:

1. **Roughly 87 MiB of the local 403 MiB `.git` is local churn, not history.** 45.7 MiB loose objects
   (160 already prune-packable), 8.3 MiB of worktree admin across 26 live worktrees, 1.5 MiB of Cursor
   state, plus redundancy across 9 packs. A plain `git gc` folds most of that away with zero history risk
   and zero force-push. **That was deliberately not run in this lane.** It is the cheapest available
   experiment and it should be measured before anyone force-pushes anything, if only to establish a clean
   baseline for the rewrite's before-and-after.
2. **26 live agent worktrees are attached to this object store right now.** A history rewrite invalidates
   every one of them. The coordination cost here is not "everyone re-clones", it is "every in-flight agent
   lane dies". Sequence accordingly.

---

## 9. Corrections to the 2026-07-12 audit

For anyone reading the older doc:

| Audit §3 claim | Status 2026-08-02 |
|---|---|
| working tree 332M | Was accurate as a tracked-content figure. Now **129.5 MiB**. |
| `.git` 295M | Now **403 MiB** locally, **316 MiB** as clone cost. Grew, did not shrink. |
| 627M total | Meaningless as a single number. See §0. |
| `content/drafts/` images 238M | Now **49.31 MiB** tracked. 189 MiB removed by PR #558. |
| `reports/` non-md captures 31M | Now **0.6 MiB** tracked (JSON/HTML/CSV only). Screenshots gone. |
| `backup/` 19M | Now **23.39 MiB** tracked, of which 8.74 MiB is bucket E candidate. |
| "gitignore added this pass prevents future accumulation only" | Still true and still the key caveat. |

The audit's structural conclusions all held up. Branches were and are clean. The dated docs were and are
intentional. Only the numbers moved.

---

## 10. What this pass did not verify

- **Publish status of any draft.** No live-site calls were made from this lane. The bucket B/C publish
  question in the issue checklist is still open and still needs authenticated WP confirm before any delete.
- **Whether the two May-25 QA visual `backup/` dirs are cited by any doc.** Not re-grepped here.
- **What `git gc` would actually reclaim.** Deliberately not run. Estimated at ~87 MiB from
  `count-objects -vH` plus the `.git` subdirectory breakdown, not measured.
- **Whether the `source-packs/**/verification/` screenshots are referenced by tracked markdown.** The
  Phase A grep methodology (grep every basename across the tracked corpus) was not re-run for this folder.
  Do that before proposing it as a wave.

---

**Sources:** `REPO-HYGIENE-AUDIT-2026-07-12.md`, `reports/repo-reclaim-list-20260726.md` (#369),
`reports/repo-bloat-318-next-steps-20260726.md` (#539), PR #558 / commit `d8d5e44`, `.gitignore` at
`dd87d4a`. Measured against the main checkout at `/Users/kk/Code/kriskrug-wp`, HEAD `dd87d4a`, 2026-08-02.
