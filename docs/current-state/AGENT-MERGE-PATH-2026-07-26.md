# Agent merge path — 2026-07-26

## Problem

Cloud agents authenticate to GitHub with the **Cursor GitHub App installation token**. Under this repo's branch protection that token:

- can open PRs, push branches, and read checks
- **cannot** create approving reviews (`addPullRequestReview` → *Resource not accessible by integration*)
- **cannot** merge (`At least 1 approving review is required…`)
- **cannot** enable auto-merge (`allow_auto_merge` is false; API also rejects)

So "review and merge the safe PRs" fails even when CI is fully green. Direct push to `main` is also blocked.

This is a known Cursor Cloud limitation (installation token scopes), not a bug in the PR contents.

## Fix (two paired credentials, one human setup)

### 1. Create a classic PAT as `WalksWithASwagger` (or another write-access user)

Scopes: `repo` (private_repo not required — this repo is public, but `repo` is simplest).

Do **not** use an account that is also the sole required CODEOWNER reviewer if you later add CODEOWNERS self-approve blocks; today there is no CODEOWNERS gate.

### 2. Store the same token in two places

| Where | Name | Used by |
|---|---|---|
| GitHub → Settings → Secrets and variables → Actions | `AGENT_MERGE_TOKEN` | `.github/workflows/agent-safe-merge.yml` |
| Cursor Cloud environment secrets | `GH_TOKEN` | `gh` inside Cloud agent pods |

`gh` prefers `GH_TOKEN` over the installation token when set.

### 3. Merge a safe PR

**From Cloud agent (after `GH_TOKEN` is injected into a new session):**

```bash
gh pr ready <n>
gh pr review <n> --approve --body "CI green; content/docs only"
gh pr merge <n> --squash --delete-branch
```

**From GitHub UI / Actions (no Cloud session needed):**

1. Ensure the PR is not a draft and CI summary is green.
2. Add label `agent-safe-merge`.
3. Workflow approves with the PAT and squash-merges.
4. Or: Actions → *Agent safe merge* → Run workflow → enter PR number.

## Safety rails in the workflow

- Requires label `agent-safe-merge` (or `workflow_dispatch`).
- Refuses drafts.
- Refuses any changed path under `theme/`, `plugins/`, or `inc/`.
- Requires check rollup green (including `summary`).
- Requires `mergeable==MERGEABLE`.

Theme / deploy / pixel-gated PRs (#493, #505, etc.) stay human-merged.

## One-time: create the label

```bash
gh label create agent-safe-merge \
  --color 0E8A16 \
  --description "CI-green content/docs PR; Actions PAT may approve+squash-merge"
```

## Policy note

Repo `allow_auto_merge` stays `false`. This path is **opt-in** (label or Cloud `GH_TOKEN` + explicit agent merge), not blanket auto-merge of every green PR.
