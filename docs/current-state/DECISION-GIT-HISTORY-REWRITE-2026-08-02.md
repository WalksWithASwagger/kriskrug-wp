# Decision: git history rewrite (filter-repo) - 2026-08-02

**Issue:** #572
**Sizes cited from:** #318 (that lane owns the byte measurement). Numbers below are my own sanity reading taken 2026-08-02 against `/Users/kk/Code/kriskrug-wp` at `dd87d4a`. If they disagree with #318, #318 wins.
**Nothing in this doc executes anything.** No rewrite, no force-push, no `gc`, no worktree removal.

---

## Recommendation: DEFER

Do not run `filter-repo` now. Do not schedule it. Two zero-risk actions this week reclaim about 3.45 GB, which is roughly ten times what the rewrite would reclaim, and neither one can lose work:

1. **Prune finished worktrees.** `.claude/worktrees/` is 3.4 GB across 26 side worktrees, each carrying a 134 MB checkout. Ten of them are locked by live agent processes right now, so this is a "when the swarm is idle" job, not a "right now" job. The `cleanup-worktrees` skill already exists for this.
2. **Run `git gc --prune=now` on the main clone.** There are 51.1 MB of unreachable objects sitting in `.git` across 1,536 objects, plus 3,084 loose objects in 9 unconsolidated packs. This is leftover garbage, not history. `gc` does not rewrite anything and does not invalidate a single clone, worktree, or PR branch.

The rewrite stays available. It is not a no-go on the merits, the 277 MB is real. It is a defer because the precondition it needs (an empty PR queue and no live worktrees) does not currently exist in this repo and will not exist until the swarm stops, and because #318 Phase B has to land first or the rewrite gets scoped wrong.

The condition that flips this to **go** is at the bottom.

---

## What the rewrite actually buys

Reachable object weight in history, by path bucket (disk size, deduped, all refs):

| Bucket | Size | Blobs |
|---|---:|---:|
| `content/drafts/**/images/` | 216.8 MB | 124 |
| `content/source-packs/` | 35.0 MB | 326 |
| `docs/current-state/reports/` | 25.2 MB | 286 |
| `content/drafts/` (non-image) | 22.5 MB | 891 |
| `backup/` | 11.7 MB | 451 |
| `docs/` (everything else) | 9.9 MB | 627 |
| `theme/` | 1.5 MB | 362 |
| everything else | 1.4 MB | 800 |
| **all blobs** | **323.9 MB** | **3,867** |
| all trees | 1.3 MB | 3,884 |
| all commits | 0.6 MB | 972 |

So the entire reachable history is about 326 MB, and 99.6 percent of it is blobs. Strip the top three buckets and you remove about 277 MB. A fresh clone would drop from roughly 326 MB to roughly 50 MB.

The local `.git` is 403 MB, which is larger than the reachable 326 MB because of the 51.1 MB of unreachable objects and pack slack. That 77 MB gap is `gc` territory, not `filter-repo` territory. Anyone cloning fresh from GitHub today already gets the 326 MB number, not 403 MB.

**Put that against total disk.** The full checkout at `/Users/kk/Code/kriskrug-wp` is 4.6 GB:

- 3.4 GB is `.claude/worktrees/` (26 side worktrees x 134 MB)
- 403 MB is `.git`
- the rest is the main working tree, 129.5 MB of it tracked

A perfect rewrite takes 4.6 GB to about 4.25 GB. That is a 7 percent win on the disk you actually feel, bought with the single most destructive operation available in git. Removing the finished worktrees is a 74 percent win bought with `git worktree remove`.

**And the bleeding already stopped.** `.gitignore` line 98 blocks `content/drafts/**/images/` (landed with #369). Lines 68 to 87 block the `reports/` PNG/HTML/CSV captures. Line 89 blocks the `backup/` visual captures. The 277 MB is a fixed historical cost that is no longer compounding. There is no clock on this.

---

## What it actually costs (the issue body understates this badly)

Issue #572 says the rewrite invalidates "`.worktrees/2940-ai-lands-essay` plus the Aurora side-worktrees." That description is stale by months. Here is `git worktree list` against `/Users/kk/Code/kriskrug-wp` on 2026-08-02:

**27 registered worktrees.** One is the main checkout. 26 are side worktrees under `.claude/worktrees/`. **Ten of them are `locked`**, which means a live agent process is holding them mid-write.

They fall into three groups:

- `wf_2b664e20-3ae-*` (8 worktrees), each on a named feature branch: `content/637-speaking-photo-rights`, `content/638-keynote-taxonomy`, `docs/423-stylesheet-decision`, `docs/566-front-door-refresh`, `docs/46-wcag-audit`, `content/4-alt-text-inventory`, `docs/249-striking-distance`, `docs/122-undesigned-pages`. Every one of these has an open PR.
- `wf_b221ae10-775-*` (10 worktrees), all locked, all at `dd87d4a`. This is the currently running swarm. Two are on real lanes (`content/402-seo-authority-hubs`, `docs/125-perf-probes`), the rest on scratch branches. This memo is being written from `wf_b221ae10-775-7`.
- `wf_d3299f01-624-*` (8 worktrees), five of them on **detached HEAD** at commits that are not on any branch: `304330e`, `3aee2ac`, `26306e6`, `61ab506`, `130be35`. Detached-HEAD work is the most fragile thing in the repo. A rewrite orphans those commits with no branch pointing at them, and unlike a branch there is no ref to reconcile afterward. If any of those five carry uncommitted-to-a-branch work, it is gone.

**Open PRs: 10**, not the zero the issue's unblock condition wants:

`#652`, `#653`, `#654`, `#655`, `#656`, `#657`, `#658`, `#659`, `#660`, `#662`. All ten opened between `2026-08-03T01:25:00Z` and `2026-08-03T02:47:45Z`, so within about 80 minutes.

**Remote branches: 23.** Every one either gets force-updated or deleted.

---

## The freeze window is the real blocker, and it is structural

The issue frames the unblock as "the open PR queue draining," as if it is a scheduling problem. It is not.

The #570 correction comment on #572 already documents what happens: the 2026-08-02 sweep removed the `blocked` label citing `gh pr list --state open` returning zero at `01:22:45Z`. PR #652 opened at `01:25:00Z`. The queue was empty for three minutes. By `02:39:53Z` it was at 8. By `02:47:45Z` it was at 10.

A `filter-repo` run plus mirror backup plus verification plus force-push plus 27 worktree reconciliations is a multi-hour operation, and it needs the queue to stay at zero for the whole thing. The way this repo is currently worked, that window does not occur. Ten agents spawning lanes in 80 minutes is the normal operating mode, not an anomaly.

So the honest precondition is not "wait for the queue to drain." It is **"declare a swarm freeze, land or close all 10 PRs, remove all 26 side worktrees, then run it."** That is a deliberate day where no content or theme work ships. Pricing it that way is what makes the answer obvious: a day of frozen throughput to reclaim 277 MB of disk that nothing is currently complaining about is a bad trade.

---

## The #318 Phase B gate is not satisfied, so the scope is not knowable yet

#318 sequences this deliberately: Phase A (orphaned captures, done in PR #317), Phase B (decide published status per draft, then strip images for published ones), Phase C (the history rewrite). Phase B's checkboxes are all still unchecked.

That ordering is not bureaucratic. `filter-repo --path` removes a path from **every** commit including HEAD. The current HEAD tree still tracks:

- **27 files** under `content/drafts/**/images/`
- **211 files** under `content/source-packs/`
- **7 binary captures** under `docs/current-state/reports/`

Stripping those buckets from history also strips them from the working tree. That is a content decision wearing a history-hygiene costume. Until Phase B establishes which drafts are published (and therefore whose images are safely recoverable from WP media), you cannot write a correct `filter-repo` path spec. You would either delete source material for an unpublished draft or leave the biggest blobs behind and reclaim far less than 277 MB.

Running Phase C before Phase B means either doing Phase B's judgment work under time pressure inside a freeze window, or guessing.

---

## What breaks in docs

Pinned commit SHAs in `docs/`, verified by extracting every 7-to-40 character hex token from every tracked `.md` and testing each against `git cat-file -t`:

- **401 distinct hex tokens resolve to real commits in this repo.**
- They appear across **58 markdown files**: 35 under `docs/current-state/reports/`, 18 under `docs/current-state/archive/`, and 5 top-level `docs/current-state/` docs including `CURRENT-STATE-2026-07-30.md`, `SESSION-CLOSEOUT-2026-07-24.md`, `AURORA-STYLESHEET-REBUILD-PLAN.md`, `PERFORMANCE-RECOVERY-2026-07-01.md`, and `WORK-PLAN-2026-07-16.md`.
- **Zero pinned SHAs outside `docs/`.** Checked `.md`, `.py`, `.yml`, `.sh` across the repo. No CI workflow, no Makefile target, no connector script pins a commit hash. That is the one piece of good news here.

After a rewrite all 401 stop resolving. Nothing crashes, since these are prose references in reports, but the audit trail goes dead. Every "verified at `abc1234`" line in every morning-truth report becomes unverifiable. Given how much of this repo's operating model is "the newest committed morning-truth report is the source of truth," burning the ability to check those receipts is a real cost, not a rounding error.

Worth noting: one 40-character SHA in `docs/` is **already dangling**. `7776f971380a037a6ea15ea55c754d1c0e5186b5` is cited as `HEAD` in three archived morning-truth reports (`morning-truth-20260604-055806Z.md`, `-20260604-062927Z.md`, `-20260607-185349Z.md`) and no longer exists. So the decay has already started on its own. A rewrite takes it from 1 dead pin to 401.

---

## Precedent: this repo already did one, in May, and it cost PRs

`docs/current-state/archive/CREDENTIAL-HISTORY-REWRITE-EXECUTION-2026-05-19.md` records a completed `filter-repo --replace-text` run on 2026-05-19 to strip a leaked WordPress app password from history. The playbook was sound: local backup refs, an isolated mirror backup in `/tmp`, an isolated rewrite mirror, `gitleaks` before and after, force-update of three specific branches.

Two things from that run matter here.

**It auto-closed open PRs.** From the execution doc's own "Side effects observed" section: PR #77 and PR #73 both moved to `CLOSED` because their head branches were rewritten. That was with a queue of 2. Today's queue is 10, and eight of those PRs have a live worktree attached.

**Its own backup refs are gone.** `git for-each-ref | grep -i backup` returns nothing today. The `backup/pre-credential-rewrite-*` refs listed in that doc no longer exist, and the `/tmp` mirrors are long gone. The pre-rewrite commit `add42367ae5058793a4126b657941348cb87d7eb` still resolves locally only because it is an unreachable object nobody has `gc`'d yet, which is part of that 51.1 MB. The rollback path from the May rewrite has quietly expired. If a mirror backup is the rollback plan for the next one, the plan has to include where that mirror lives for longer than a `/tmp` directory survives, and who is responsible for keeping it.

The May rewrite was also *justified*, because a leaked credential in reachable history is a security problem with no alternative fix. Disk usage is not that. Same blast radius, much weaker reason.

---

## Who re-clones

Smaller list than it looks, which is the only argument in the rewrite's favour:

- Kris's laptop (the `/Users/kk/Code/kriskrug-wp` clone).
- Any Cursor Cloud pod with a checkout. Long-lived pods survive across sessions, so a pod that started before the rewrite keeps a pre-rewrite `.git` and will fail to push. Per `AGENTS.md` these pods already have a history of stale state.
- GitHub Actions checkout caches for `test-pr.yml`.

No other humans have write access. The re-clone burden is genuinely low. It just does not offset the freeze window or the Phase B gate.

---

## The condition that flips this to GO

Revisit when **either** of these is true:

1. **A secret lands in reachable history again.** Then it is a security rewrite, not a hygiene rewrite, there is no alternative fix, and the cost calculus inverts completely. Run the 2026-05-19 playbook. Do not wait for a convenient window.
2. **Clone or fetch time becomes an actual complaint** from a real workflow, not a hypothetical. 326 MB clones in well under a minute on any normal connection. If a Cloud pod cold-start starts timing out on checkout, that is a measurable trigger. Nobody has reported one.

Two conditions that specifically do **not** flip it: the number getting quoted in another audit doc, and the queue happening to hit zero for a few minutes.

If one of those triggers fires, the runbook issue should cover, in this order:

1. #318 Phase B closed first, with published status proven per draft, so the `--path` spec is correct rather than guessed.
2. Announced swarm freeze. No new worktrees, no new PRs, for the duration.
3. All 10 (or however many) open PRs merged or closed. Verified by `gh pr list --state open --limit 100 --json number` returning `[]`, re-checked immediately before the force-push, not once at the start.
4. All 26 side worktrees removed, not just unlocked. `git worktree list` shows one entry. Special handling for the five detached-HEAD worktrees: every one gets its commit put on a named branch and pushed, or explicitly written off in the runbook, before removal.
5. `git clone --mirror` to a durable location outside `/tmp`, with the path and the retention owner named in the runbook. The May run's `/tmp` mirror is the counterexample.
6. Local backup refs plus a dated tag on pre-rewrite `main`.
7. `filter-repo` in an isolated mirror, never in the working clone.
8. Verify before pushing: markdown and code history intact, HEAD tree byte-identical for every tracked non-binary file, `.git` measurably smaller, `make validate` and `make python-test` pass in a fresh clone of the rewritten mirror.
9. KK-gated force-push.
10. Re-clone checklist for laptop, Cloud pods, Actions cache.
11. A dated `docs/current-state/` execution record, same shape as the 2026-05-19 one, including a decision on whether to fix or annotate the 401 stale SHA references.

---

## How these numbers were taken

Read-only, on 2026-08-02, against `/Users/kk/Code/kriskrug-wp` at `dd87d4a`.

```bash
git worktree list                                  # 27 entries, 10 locked
gh pr list --state open --limit 100 --json number  # 10 open
git ls-remote --heads origin | wc -l               # 23
du -sh .git .claude/worktrees .                    # 403M / 3.4G / 4.6G
git count-objects -vH                              # in-pack 7551, size-pack 346.63 MiB,
                                                   # loose 3084 / 45.70 MiB, 9 packs
git ls-tree -r -l HEAD | awk '{s+=$4} END{print s}' # 129.5 MB tracked at HEAD

# per-bucket history weight
git rev-list --objects --all \
  | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize:disk) %(rest)' \
  | awk '$1=="blob"'

# unreachable weight (the gc-able 51.1 MB)
git rev-list --objects --all | awk '{print $1}' | sort -u > reach.txt
git cat-file --batch-all-objects --batch-check='%(objectname) %(objecttype) %(objectsize:disk)' \
  | awk 'NR==FNR{r[$1]=1;next} !($1 in r){s+=$3;n++} END{print s, n}' reach.txt -

# pinned SHAs
grep -rEoh '\b[0-9a-f]{7,40}\b' docs/ --include='*.md' | sort -u \
  | while read h; do [ "$(git cat-file -t "$h" 2>/dev/null)" = commit ] && echo "$h"; done
```

## Not verified

- Whether any Cursor Cloud pod currently holds a checkout. Not observable from here.
- Whether the five detached-HEAD worktrees under `wf_d3299f01-624-*` contain work not reachable from any branch. Determining that means inspecting worktrees owned by other live lanes, which is out of scope for this one. **The runbook must resolve this before any rewrite.**
- Post-rewrite `.git` size. The ~50 MB figure is arithmetic from the bucket table, not a measured `filter-repo` dry run. #318 owns the measurement.
