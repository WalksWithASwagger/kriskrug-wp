#!/usr/bin/env bash
# Apply the #570 label hygiene sweep audited on 2026-08-02.
#
# Audit and reasoning: docs/current-state/LABEL-HYGIENE-2026-08-02.md
#
# This script only adds and removes labels. It never closes an issue, edits a
# body, posts a comment, or touches the live WordPress site.
#
# Usage:
#   CONFIRM=1 ./scripts/ops/relabel-2026-08-02.sh
#   CONFIRM=1 INCLUDE_JUDGMENT_CALLS=1 ./scripts/ops/relabel-2026-08-02.sh
#
# Idempotent: every action re-reads the issue's current labels first and skips
# work that is already done, so a second run is a no-op.

set -euo pipefail

# Hard guard. Label edits on this repo are KK-gated, so an accidental
# invocation (tab completion, a stray agent, a shell history recall) must do
# nothing at all.
if [[ "${CONFIRM:-}" != "1" ]]; then
  cat >&2 <<'GUARD'
REFUSING TO RUN.

This script changes GitHub issue labels on WalksWithASwagger/kriskrug-wp.
Read docs/current-state/LABEL-HYGIENE-2026-08-02.md first, then re-run with:

  CONFIRM=1 ./scripts/ops/relabel-2026-08-02.sh

Optional, for the two calls the audit flagged as KK judgment rather than fact:

  CONFIRM=1 INCLUDE_JUDGMENT_CALLS=1 ./scripts/ops/relabel-2026-08-02.sh
GUARD
  exit 1
fi

need_cmd() { command -v "$1" >/dev/null || { echo "missing $1" >&2; exit 1; }; }
need_cmd gh
need_cmd jq

REPO="${REPO:-WalksWithASwagger/kriskrug-wp}"
export GH_REPO="$REPO"

# Returns "true" or "false". Used by every action below so the script can be
# re-run safely and so it reports what it skipped instead of failing.
has_label() {
  gh issue view "$1" --json labels --jq --arg l "$2" '[.labels[].name] | index($l) != null'
}

add_label() {
  local issue="$1" label="$2" why="$3"
  if [[ "$(has_label "$issue" "$label")" == "true" ]]; then
    echo "skip  #$issue already has '$label'"
    return 0
  fi
  echo "ADD   #$issue +$label :: $why"
  gh issue edit "$issue" --add-label "$label"
}

remove_label() {
  local issue="$1" label="$2" why="$3"
  if [[ "$(has_label "$issue" "$label")" != "true" ]]; then
    echo "skip  #$issue does not have '$label'"
    return 0
  fi
  echo "DROP  #$issue -$label :: $why"
  gh issue edit "$issue" --remove-label "$label"
}

# The four swarm-ready removals below are only correct while the issue is still
# blocked. If a blocker cleared between the audit and this run, the label is no
# longer a contradiction and must stay.
retire_swarm_ready_if_still_blocked() {
  local issue="$1" why="$2"
  if [[ "$(has_label "$issue" blocked)" != "true" ]]; then
    echo "SKIP  #$issue no longer carries 'blocked'; the contradiction is gone, leaving 'swarm-ready' alone"
    return 0
  fi
  remove_label "$issue" swarm-ready "$why"
}

echo "==> Repo: $REPO"
echo "==> Audit: docs/current-state/LABEL-HYGIENE-2026-08-02.md (2026-08-03T03:20Z)"
echo

echo "==> Block 1: resolve the 'swarm-ready' plus 'blocked' contradiction"
# Both labels on one issue tell an agent opposite things. Board #573 lists all
# four under "Blocked, do NOT dispatch yet". #424 carries the same pair on
# purpose and is deliberately absent from this list: its body and #476's body
# both say the gap-inventory half runs in parallel.
retire_swarm_ready_if_still_blocked 476 "blocked on #475 and decision #423; #573 says do not dispatch"
retire_swarm_ready_if_still_blocked 477 "blocked on #476 and decision #423; #573 says do not dispatch"
retire_swarm_ready_if_still_blocked 478 "blocked on #477 and decision #423; #573 says do not dispatch"
retire_swarm_ready_if_still_blocked 479 "blocked on decision #423; #573 says do not dispatch"
echo

echo "==> Block 2: label the decision that gates the whole Track B chain"
# #423 is titled [DECISION], is listed on #573 under "Needs a KK decision", and
# gates seven issues that carry 'blocked'. It was the only decision issue in the
# backlog without 'needs-decision'; #571, #572 and #638 all have it. Its memo is
# in draft PR #655, which makes the label more useful now, not less.
add_label 423 needs-decision "titled [DECISION], gates the #127/#424/#476-#481 blocked chain, memo pending in PR #655"
echo

echo "==> Block 3: give the two unlabeled issues a signal"
# An issue with zero labels answers no label query, so it never appears in a
# dispatch sweep or a morning-truth signal table. These two have been invisible
# since 2026-07-16 and 2026-07-17.
add_label 369 tech-debt "unlabeled since 2026-07-16; parent #318 carries tech-debt"
add_label 385 tech-debt "unlabeled since 2026-07-17; repo hygiene work, blocker kk-agents#2 closed 2026-07-17"
echo

if [[ "${INCLUDE_JUDGMENT_CALLS:-}" == "1" ]]; then
  echo "==> Block 4 (opt-in): the two calls the audit left to KK"
  # #495 is the finished 2026-07-26 dispatch board. #573 supersedes its wave
  # labels and #642 supersedes parts of #573. A superseded board is not a
  # bounded task an agent should pick up. 'roadmap' stays so it remains
  # findable. #573 is intentionally not touched: #642 only supersedes its
  # events and testimonials sections.
  remove_label 495 swarm-ready "finished 2026-07-26 dispatch board, superseded by #573 and #642; keeps roadmap"
  # #385's only dependency, kk-agents#2, closed 2026-07-17T06:10:13Z. Board #495
  # still describes it as blocked on that issue, which is stale. Whether it is
  # ready to dispatch is a scheduling call, not a hygiene fact.
  add_label 385 swarm-ready "dependency kk-agents#2 closed 2026-07-17; has acceptance criteria and verification commands"
  echo
else
  echo "==> Block 4 skipped. Set INCLUDE_JUDGMENT_CALLS=1 to also drop 'swarm-ready'"
  echo "    from board #495 and add it to #385. See section 4 of the audit."
  echo
fi

echo "==> Verify"
# make morning-truth cannot check wave or blocked counts: build_label_counts()
# at scripts/morning_truth_report.py:90-105 counts a hard-coded seven labels and
# neither string appears in that file. These are the checks that do work.
echo "-- swarm-wave-1 (expect 637, 638)"
gh issue list --label swarm-wave-1 --state open --json number --jq '[.[].number] | sort | join(", ")'
echo "-- swarm-wave-2 (expect 635, 639, 640)"
gh issue list --label swarm-wave-2 --state open --json number --jq '[.[].number] | sort | join(", ")'
echo "-- swarm-wave-3 (expect 641)"
gh issue list --label swarm-wave-3 --state open --json number --jq '[.[].number] | sort | join(", ")'
echo "-- blocked (expect 17, unchanged by this script)"
gh issue list --label blocked --state open --json number --jq 'length'
echo "-- swarm-ready (22 before, expect 18, or 17 with judgment calls)"
gh issue list --label swarm-ready --state open --json number --jq 'length'
echo "-- needs-decision (3 before, expect 4)"
gh issue list --label needs-decision --state open --json number --jq '[.[].number] | sort | join(", ")'
echo
echo "Done. Nothing was closed, no body was edited, no comment was posted."
echo "#570 asks for a summary on the current dispatch board (#642). Post it by hand,"
echo "so the wording is yours and the audit stays the only machine-written record."
