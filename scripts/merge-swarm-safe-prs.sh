#!/usr/bin/env bash
# Squash-merge the 2026-07-26 swarm docs/content PRs (CI-green, no theme/).
# Requires a write-access PAT (not the Cursor GitHub App token).
#
# Usage:
#   export GH_TOKEN=ghp_...   # classic PAT with repo scope (WalksWithASwagger)
#   ./scripts/merge-swarm-safe-prs.sh
#
# Skip theme holds: #493 (pixel gate), #505 (theme newsletter — merge separately after review).

set -euo pipefail

if [[ -z "${GH_TOKEN:-}" ]]; then
  echo "Set GH_TOKEN to a write-access classic PAT (repo scope), then re-run." >&2
  exit 1
fi

need_cmd() { command -v "$1" >/dev/null || { echo "missing $1" >&2; exit 1; }; }
need_cmd gh
need_cmd jq

REPO="${REPO:-WalksWithASwagger/kriskrug-wp}"
export GH_REPO="$REPO"

echo "==> Ensure label agent-safe-merge exists"
gh label create agent-safe-merge \
  --color 0E8A16 \
  --description "CI-green content/docs PR; PAT may approve+squash-merge" \
  2>/dev/null || true

merge_one() {
  local pr="$1"
  echo
  echo "======== PR #$pr ========"
  local meta
  meta=$(gh pr view "$pr" --json number,state,isDraft,mergeable,title,files,statusCheckRollup,url)

  echo "$meta" | jq -r '"\(.title)\n\(.url)\ndraft=\(.isDraft) state=\(.state) mergeable=\(.mergeable)"'

  if [[ "$(echo "$meta" | jq -r .state)" != "OPEN" ]]; then
    echo "skip: not OPEN"
    return 0
  fi

  # Refuse theme/plugins/inc
  local blocked
  blocked=$(echo "$meta" | jq -r '
    [.files[].path
     | select(startswith("theme/") or startswith("plugins/") or startswith("inc/") or .=="functions.php")]
    | unique | .[]
  ')
  if [[ -n "$blocked" ]]; then
    echo "REFUSE theme/plugins/inc paths:"
    echo "$blocked"
    return 1
  fi

  # Undraft if needed
  if [[ "$(echo "$meta" | jq -r .isDraft)" == "true" ]]; then
    gh pr ready "$pr"
  fi

  # Re-fetch checks after ready
  meta=$(gh pr view "$pr" --json mergeable,statusCheckRollup,files,state,isDraft)

  local bad
  bad=$(echo "$meta" | jq -r '
    [.statusCheckRollup[]?
     | select((.status!="COMPLETED")
           or (.conclusion!="SUCCESS" and .conclusion!="SKIPPED" and .conclusion!="NEUTRAL"))]
    | map("\(.name)=\(.status)/\(.conclusion // "null")") | .[]
  ')
  if [[ -n "$bad" ]]; then
    echo "CI not green:"
    echo "$bad"
    return 1
  fi

  if [[ "$(echo "$meta" | jq -r .mergeable)" != "MERGEABLE" ]]; then
    echo "not MERGEABLE yet — resolve conflicts / wait"
    return 1
  fi

  gh pr review "$pr" --approve --body "swarm cleanup: CI green, no theme/plugins/inc. Approved via GH_TOKEN."
  gh pr merge "$pr" --squash --delete-branch
  echo "MERGED #$pr"
}

# 1) Unlock path first (this PR adds the Actions workflow for later)
echo "==> Phase 0: unlock #506"
merge_one 506 || echo "WARN: #506 merge failed (merge it in UI if needed); continuing"

# Ordered safe queue (Futureproof folder order first, then rest)
PRS=(
  # Futureproof
  501 503 518 535
  # Lane B / pages
  504 507 508 509 510 511 512 513
  # Round 2
  515 516 517 519 520 521 522 523 524
  # Round 3
  526 527 528 529 530 531 532 533 534
  # Ops / closeouts / remainders
  502 538 539 540 541 542
  514 525 536 537
)

echo "==> Phase 1: squash-merge ${#PRS[@]} safe PRs"
failed=()
for pr in "${PRS[@]}"; do
  if ! merge_one "$pr"; then
    failed+=("$pr")
  fi
done

echo
echo "==> Done. Failed (if any): ${failed[*]:-none}"
echo "HOLD (do not merge here): #493 pixel gate, #505 theme newsletter (human review)"
echo
echo "Next: close issues #48 #95 #269 #270 #360 #366 #379 #384 #222 #363 using paste comments in PRs #529 #528 #541 #540"
