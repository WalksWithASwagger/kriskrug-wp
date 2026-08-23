# Agent merge path — 2026-07-26

> **STATUS 2026-08-23: DELETED. The workflow this describes no longer exists.**
>
> `.github/workflows/agent-safe-merge.yml` was removed on 2026-08-23 after 33 runs and 0
> successes. The `agent-safe-merge` label is now inert. This file is kept as the record of
> why, and what a real fix would require.
>
> Verified today:
> 1. Actions secret `AGENT_MERGE_TOKEN` was never set. Every `Agent safe merge` run
>    fails at the first step with `Repo secret AGENT_MERGE_TOKEN is missing.`
>    The workflow has never merged anything.
> 2. The fix below, as written, would still not work. It says to create the PAT as
>    `WalksWithASwagger`, but that account authors the agent PRs in this repo, and
>    GitHub refuses `Can not approve your own pull request`. The PAT must belong to a
>    **different** write-access account, not the PR author.
>
> **What actually works today:** `main` has `enforce_admins: false` and KK holds admin,
> so `gh pr merge <n> --squash --admin` goes through. Required checks are `strict: true`,
> so branches read `BEHIND`; check file overlap against `main` before an admin merge
> rather than assuming the stale base is safe. Dependabot PRs have a different author
> and take a normal approve plus merge.
>
> Fixing this properly means step 1 below on a second account. Until then the queue
> drains by admin override only.

## Problem

Cloud agents authenticate to GitHub with the **Cursor GitHub App installation token**. Under this repo's branch protection that token:

- can open PRs, push branches, and read checks
- **cannot** create approving reviews (`addPullRequestReview` → *Resource not accessible by integration*)
- **cannot** merge (`At least 1 approving review is required…`)
- **cannot** enable auto-merge (`allow_auto_merge` is false; API also rejects)

So "review and merge the safe PRs" fails even when CI is fully green. Direct push to `main` is also blocked.

This is a known Cursor Cloud limitation (installation token scopes), not a bug in the PR contents.

## Fix (two paired credentials, one human setup)

### 1. Create a classic PAT on a write-access account that is NOT the PR author

Scopes: `repo` (private_repo not required — this repo is public, but `repo` is simplest).

The account must not be the one that authors the agent PRs. GitHub blocks self-approval
outright, so a PAT owned by the PR author cannot satisfy the 1-review requirement no
matter what scopes it carries. Today that means a second user or a machine account
added as a collaborator with write access.

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
