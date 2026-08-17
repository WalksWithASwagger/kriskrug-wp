# Issue label hygiene audit (#570)

**Status:** audit only. No label was applied by this lane.
**Audited:** 2026-08-03T03:20Z UTC (2026-08-02 local session), against 59 open issues.
**Apply script:** [`scripts/ops/relabel-2026-08-02.sh`](../../scripts/ops/relabel-2026-08-02.sh). It refuses to run without `CONFIRM=1`.

Applying labels without KK approval is a HITL violation in this repo, so this lane produced the audit and the script and stopped. A human runs the script.

## What was already done before this audit

A sweep ran on 2026-08-02 and a correction pass ran on 2026-08-03, both recorded in comments on #570 and #642. Between them they removed 13 stale wave labels, removed `blocked` from #566, removed and then restored `blocked` on #572, and appended explicit "Blocked by" notes to eight issue bodies. That pass also overwrote #640's body by accident and restored it from revision history seven minutes later.

This audit re-verified all of that from scratch rather than trusting it. The wave map and all 17 `blocked` labels check out. What the earlier passes did not look at was label contradictions, unlabeled issues, and the missing decision label on #423. That is where every proposed change below comes from.

## How it was checked

```
gh issue list --state open --limit 200 --json number,title,labels,body
gh issue list --label swarm-wave-1 --state open --json number      # 637, 638
gh issue list --label swarm-wave-2 --state open --json number      # 635, 639, 640
gh issue list --label swarm-wave-3 --state open --json number      # 641
gh issue list --label blocked --state open --json number           # 17 issues
gh pr list --state open --limit 50 --json number,title,headRefName # 10 open drafts
gh issue view 2 --repo WalksWithASwagger/kk-agents --json state    # CLOSED 2026-07-17T06:10:13Z
```

Open PRs at audit time: #652, #653, #654, #655, #656, #657, #658, #659, #660, #662. All drafts. They cover issues #4, #46, #122, #249, #423, #566/#549, #637, #638, plus #661 (PR #660) and a morning-truth fix (PR #662). An issue with an open PR is in progress, not blocked, and none of those eight carry `blocked`.

## 1. Wave labels: nothing to retire

Six open issues carry a wave label. All six match the dependency wave block on board #642 (2026-08-02). Zero carry a wave from the finished #495 dispatch (2026-07-26) or from #573 (2026-07-31).

| Issue | Wave label | #642 wave | Verdict |
|---|---|---|---|
| #637 stage photography | `swarm-wave-1` | WAVE A | Correct, keep |
| #638 keynote taxonomy | `swarm-wave-1` | WAVE A | Correct, keep |
| #635 events hero ship | `swarm-wave-2` | WAVE B | Correct, keep |
| #639 speaking payload | `swarm-wave-2` | WAVE B | Correct, keep |
| #640 embed hygiene | `swarm-wave-2` | WAVE B | Correct, keep |
| #641 schema and links | `swarm-wave-3` | WAVE C | Correct, keep |

Wave 1 is two merges from empty. #637 and #638 both have open draft PRs (#657, #653). When those land, wave 1 clears and #639's named blockers go with it.

**Open judgment call from the earlier sweep, now resolved.** That sweep removed `swarm-wave-2` from #612 and flagged it as the one call it was unsure about. Board #642 settles it: "Plus two independent KK-gated items outside this order: #500 (Futureproof draft creation) and #612 (Zero to One rewrite, staged and awaiting approval)." #612 sits outside the wave order, so no wave label is right. No action.

## 2. Blocked labels: all 17 still name a live blocker

None clear today. Seven trace back to decision #423, whose recommendation memo is sitting in **draft PR #655** right now. Those are marked PENDING, not cleared: a memo in an unmerged draft is not a recorded decision, #423's own acceptance box "KK decision recorded" is unchecked, and each of the seven also has a direct predecessor issue that is independently open.

| Issue | Named blocker in body | Blocker state (03:20Z) | Verdict |
|---|---|---|---|
| #127 mobile QA | #479 breakpoint consolidation | OPEN | Keep |
| #424 hover and focus | #476, root gate #423 | both OPEN | Keep, pending #423 |
| #476 primitives | #475, #423 | both OPEN | Keep, pending #423 |
| #477 component migration | #476, #423 | both OPEN | Keep, pending #423 |
| #478 dead CSS | #477, #423 | both OPEN | Keep, pending #423 |
| #479 breakpoints | #423 | OPEN | Keep, pending #423 |
| #480 Track A page CSS | #475, #423 | both OPEN | Keep, pending #423 |
| #481 class rename | #477, #423 | both OPEN | Keep, pending #423 |
| #500 Futureproof draft | KK authorization plus credentials | Both acceptance boxes unchecked | Keep |
| #572 history rewrite | PR queue draining | 10 open PRs | Keep |
| #593 testimonials epic | #601, #602 human gates | both OPEN | Keep |
| #601 theme deploy | KK pixel gate plus SFTP creds | Unrecorded | Keep |
| #602 page body deploy | #601 | OPEN | Keep |
| #635 events hero ship | KK approval only | Repo deps #631, #632, #633 all CLOSED | Keep |
| #639 speaking payload | #637, #638 | both OPEN (PRs #657, #653) | Keep |
| #640 embed hygiene | #639 | OPEN | Keep |
| #641 schema and links | #638, #639, #640 | all OPEN | Keep |

#635 is worth calling out: every repo-side dependency is closed and the only thing left is KK's approval of the hero set. It is the first item in the live-write serialization order on #642.

## 3. Proposed changes

Seven label edits across six issues, plus two judgment calls. Every one is reversible with the inverse `gh` command.

| Issue | Current labels | Proposed labels | Reason |
|---|---|---|---|
| #476 | `priority:high, track-b, swarm-ready, refactor, blocked` | drop `swarm-ready` | `swarm-ready` means "safe for autonomous execution now"; #573 lists #476 under "do NOT dispatch yet". The two labels contradict each other. |
| #477 | `priority:medium, track-b, swarm-ready, roadmap, refactor, blocked` | drop `swarm-ready` | Same contradiction. Blocked on #476, which is itself blocked. |
| #478 | `priority:medium, track-b, swarm-ready, tech-debt, blocked` | drop `swarm-ready` | Same contradiction. Blocked on #477. |
| #479 | `priority:medium, mobile, track-b, swarm-ready, refactor, blocked` | drop `swarm-ready` | Same contradiction. Blocked on decision #423. |
| #423 | `priority:high, track-b, tech-debt, refactor` | add `needs-decision` | Titled `[DECISION]`, listed on #573 under "Needs a KK decision", and it gates seven `blocked` issues. It was the only decision issue without the label; #571, #572 and #638 all carry it. |
| #369 | none | add `tech-debt` | Unlabeled since 2026-07-16, so it is invisible to every label query. Parent #318 carries `tech-debt`. |
| #385 | none | add `tech-debt` | Same invisibility. Also its blocker resolved: kk-agents#2 closed 2026-07-17T06:10:13Z, which board #495 never reflected. |

**#424 is deliberately left alone** even though it carries the same `swarm-ready` plus `blocked` pair. Its body says the audit half "can start now to produce the gap list", and #476's body says "the gap-inventory half of #424 should run in parallel and feed this issue". That is a documented split, not a contradiction. Removing `swarm-ready` there would suppress genuinely dispatchable work.

## 4. Judgment calls for KK

Both live behind `INCLUDE_JUDGMENT_CALLS=1` in the script. Default off.

1. **`swarm-ready` on #495.** Board #495 is the finished 2026-07-26 dispatch. #573 says it "supersedes the wave labels from the #495 dispatch" and #642 supersedes chunks of #573. A superseded board is not a bounded task safe to hand an agent. Proposal: drop `swarm-ready`, keep `roadmap` so it stays findable. **#573 keeps its `swarm-ready`** because #642 only supersedes its events and testimonials sections; its Futureproof, rebuild chain and ops lanes are still live.
2. **`swarm-ready` on #385.** Its only dependency closed 17 days ago, and it has acceptance criteria, verification commands and agent instructions already written. It looks dispatchable. Calling it so is still a scheduling decision, not a hygiene fact.

## 5. Checked, no action

- **`auto-implement`:** zero open issues carry it. The label description already reads "Historical". Do not delete the label definition; deleting strips it from closed-issue history where it is real evidence of the parked agent-pr-generator era.
- **`swarm-parked`:** zero open issues. Nothing to sweep.
- **#402** has a `[swarm]` title prefix and no swarm label, carried over from #495 Lane C. Cosmetic. Left alone rather than inventing a wave for a board that no longer dispatches.
- **#411 through #420** keep `swarm-ready`. #642 does not supersede that lane, and #573 still lists #418, #419 and #420 as dispatchable when KK picks.
- **#612** keeps `swarm-ready` while awaiting KK approval. The work is staged, and #642 tracks it as an independent gate rather than parked.
- **#369** may want closing rather than labelling: PR #558 already reclaimed roughly 212 MB of tracked binaries against it. This lane does not close issues. Flagging it for KK.

## 6. Verification

The eval line in #570's body names `make morning-truth`. That instrument cannot see this work, and the reason is in the code: `build_label_counts()` at `scripts/morning_truth_report.py:90-105` iterates a hard-coded dict of seven label names, and neither `swarm-wave` nor `blocked` appears anywhere in that file. Confirmed by grep at audit time. That defect was already retracted in a #570 comment; this doc restates it so the next reader does not walk into it again.

What does verify the sweep:

```
gh issue list --label swarm-wave-1 --state open --json number   # expect 637, 638
gh issue list --label swarm-wave-2 --state open --json number   # expect 635, 639, 640
gh issue list --label swarm-wave-3 --state open --json number   # expect 641
gh issue list --label blocked --state open --json number        # expect 17
gh issue list --label swarm-ready --state open --json number    # 22 now, 18 after the script
gh issue list --label needs-decision --state open --json number # 3 now, 4 after (adds 423)
```

The `swarm-ready` count is the one number `morning_truth_report.py` does track, because `swarm-ready` is in that hard-coded dict. So a morning-truth run after the script should show `swarm-ready: 18`, or 17 if the judgment-call block runs too. That is a prediction about a counter this audit actually read, not an assumption about one it did not.

The script prints all six commands after it finishes.

## 7. Standing conditions

Three of these labels come off on a condition, not on a decision. Whoever next touches label hygiene should recheck them first.

- **#572** loses `blocked` when `gh pr list --state open` genuinely returns zero. It was 10 at audit time.
- **#639** loses `blocked` when #637 and #638 close, which is when PRs #657 and #653 merge.
- **The #423 chain** (#127, #424, #476, #477, #478, #479, #480, #481) unwinds in dependency order after KK records a decision on #423, not when PR #655 merges. Merging the memo produces a recommendation. #423's acceptance criteria want a recorded decision.
