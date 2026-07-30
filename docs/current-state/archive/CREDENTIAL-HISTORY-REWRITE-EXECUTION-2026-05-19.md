# Credential History Rewrite Execution - 2026-05-19

**Scope:** Execute the preflighted git-history credential cleanup.  
**Source plan:** `CREDENTIAL-HISTORY-REWRITE-PREFLIGHT-2026-05-19.md`  
**Status:** Completed for affected remote branches.

## Why this was run

A revoked WordPress application password was removed from the current tree, but reachable git history still contained leaked credential material in historical raw HTML snapshots.

## Safety setup used

- Local backup refs created before rewrite:
  - `backup/pre-credential-rewrite-main-20260519`
  - `backup/pre-credential-rewrite-aurora-v2-20260519`
  - `backup/pre-credential-rewrite-aurora-redesign-20260519`
- Isolated mirror backup:
  - `/tmp/kriskrug-wp-pre-credential-rewrite-20260519-105819.git`
- Isolated rewrite mirror:
  - `/tmp/kriskrug-wp-history-rewrite-20260519-105819.git`

## Rewrite method

Executed in isolated mirror clone:

1. Ran `gitleaks git` report against history.
2. Generated a private `git filter-repo --replace-text` map from detected secret strings.
3. Rewrote history with `git filter-repo --replace-text`.
4. Re-ran `gitleaks git --redact` to validate history was clean.

Post-rewrite validation in rewrite mirror:

- `post_findings 0`
- historical commit `add42367ae5058793a4126b657941348cb87d7eb` no longer present

## Remote branches force-updated

Affected branch updates:

- `main`: `a0467e8` -> `cd5d8e6`
- `aurora/v2`: `159ac2a` -> `3283202`
- `codex/aurora-redesign-2026-05-18`: `96a1a6b` -> `d37b884`

Push mode used: force update of these specific branches from isolated rewrite mirror.

## Side effects observed

1. Open PRs tied to rewritten branches moved to closed state:
   - PR `#77` (`codex/aurora-redesign-2026-05-18` -> `aurora/v2`) is now `CLOSED`.
   - PR `#73` (`claude/automate-sidebar-graphics-55OBU` -> `main`) is now `CLOSED`.
2. Existing local worktrees that were still on pre-rewrite history now diverge from rewritten remotes.

## Immediate follow-up checklist

1. Decide PR policy:
   - reopen PR `#77` for Aurora review context, or replace with a fresh PR from rewritten branch;
   - reopen PR `#73` only if that parked lane is still active.
2. Reconcile local worktrees onto rewritten remotes before new commits:
   - `main`
   - `aurora/v2`
   - `codex/aurora-redesign-2026-05-18`
3. Keep this rewrite isolated in history:
   - do not cherry-pick pre-rewrite commits by hash from stale local refs.
4. Keep the preflight doc as companion evidence:
   - `CREDENTIAL-HISTORY-REWRITE-PREFLIGHT-2026-05-19.md`

## Verification commands

```bash
gh pr list --state open --limit 20
gh pr list --state all --limit 30 --json number,title,state,headRefName,baseRefName
git fetch --prune origin
git rev-list --left-right --count main...origin/main
gitleaks git --no-banner --redact --log-level error .
```
