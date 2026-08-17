# Issue close pass 2 — 2026-08-17

**Lane:** docs only. No live WordPress write.
**Why:** #799 closed the first leftover set. A second wave of PRs merged with `Refs` instead of `Fixes`, so the issues stayed open after the work landed. This session still cannot `gh issue close` (GitHub App 403).

## Closes on merge of this PR

| Issue | Merged PR | Why it can close |
|---|---|---|
| #418 About | #798 | Payload rebuilt. Live PATCH is a later apply session. |
| #419 Speaking | #798 | Payload rebuilt around the six-talk bank. |
| #420 Services | #798 | Payload rebuilt. |
| #639 Speaking architecture (W2) | #798 | Same payload as #419. |
| #730 FV+AI Sept-9 | #791 | Go/no-go recorded. Luma + welcome stay KK calendar work, not an open engineering issue. |

## Already wired to close when their open PRs merge

#411–#413 → #796. #414–#416 → #797. #585 → #812 (keyword switched to `Fixes`). #690 → #801. #735 → #806. #738/#740/#749 → #795. #745 → #810. #756 → #789.

## Left open (not tracking dupes)

Live apply still owed: #729, #764, #771, #706, #767, #480, #612, #709, #731, #635, #602.
Incomplete grooming: #744 (fossils on #742 also stay; KK parked deleting `customize-for-kriskrug.sh` / `monitor-agents.sh`).
Epics and human gates: #403, #477, #593, #603, #642, #274, #276, #277, #4, #122, #331, #424, #640, #641, #737, #402, #481, #318.
