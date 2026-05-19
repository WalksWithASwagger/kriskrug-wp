# Credential History Rewrite Preflight - 2026-05-19

**Scope:** Git history cleanup planning only.
**Status:** No rewrite performed. No force-push performed. No secret values printed or committed.
**Reason:** A revoked WordPress application password was removed/rotated in the current tree, but reachable git history still needs a controlled rewrite.

## Current Safety State

Current tracked tree scans clean with gitleaks. The remaining risk is reachable git history.

Commands run:

```bash
gitleaks git --no-banner --redact --report-format json --report-path /tmp/kriskrug-history-gitleaks.json --log-level warn .
jq '[.[] | {RuleID,File,StartLine,Commit,Fingerprint,Secret}]' /tmp/kriskrug-history-gitleaks.json
git branch --all --contains add42367ae5058793a4126b657941348cb87d7eb
git tag --contains add42367ae5058793a4126b657941348cb87d7eb
git worktree list --porcelain
```

Redacted history scan found 4 findings:

| Rule | File | Lines | Original commit |
|---|---|---:|---|
| `generic-api-key` | `docs/current-state/raw/pages/ai-upgrade-for-creative-professionals.html` | 318, 535, 628 | `add42367ae5058793a4126b657941348cb87d7eb` |
| `jwt` | `docs/current-state/raw/pages/contact.html` | 287 | `add42367ae5058793a4126b657941348cb87d7eb` |

Related credential cleanup commit:

- `f82fe11ff58a5082c276033b0eeff68c37a6dac3 docs: record credential rotation`

Notes:

- The exact secret values are intentionally absent from this doc.
- The redacted gitleaks findings are from raw HTML snapshot artifacts, not from the current tracked tree.
- Treat the gitleaks findings as the minimum proven rewrite scope; rerun history scanning after any rewrite.

## Refs Impacted

Branches containing `add42367ae5058793a4126b657941348cb87d7eb`:

- `main`
- `aurora/v2`
- `codex/aurora-redesign-2026-05-18`
- `codex/aurora-staging-qa-2026-05-18`
- `origin/main`
- `origin/aurora/v2`
- `origin/codex/aurora-redesign-2026-05-18`

Tags containing the commit:

- none found

Active worktrees:

| Worktree | Branch | Rewrite note |
|---|---|---|
| `/Users/kk/Code/kriskrug-wp` | `main` | Primary checkout. Must be clean before rewrite. |
| `/Users/kk/Code/kriskrug-wp-aurora-redesign` | `codex/aurora-redesign-2026-05-18` | PR #77 branch. Coordinate before rewriting. |
| `/Users/kk/Code/kriskrug-wp-aurora-staging-qa` | `codex/aurora-staging-qa-2026-05-18` | Local staging QA branch. Can likely be recreated after rewrite. |
| `/Users/kk/Code/kriskrug-wp/.claude/worktrees/agent-aec50fddbd7207f80` | `aurora/v2` | Locked agent worktree. Do not disturb until lock is cleared. |

Remote branches to review before force-push:

- `origin/claude/automate-sidebar-graphics-55OBU`
- `origin/claude/setup-wordpress-rebuild-KVLxh`

They were not listed by `git branch --all --contains add42367...`, but should still be reviewed before cleanup because they are open/archival branches in the same repo.

## Recommended Rewrite Strategy

Use a standalone credential-cleanup session. Do not combine with content, theme, or GitHub issue work.

Preferred approach:

1. Freeze repo writes and tell any active agents/humans to stop pushing.
2. Confirm all worktrees are clean or intentionally disposable.
3. Create local safety refs:

```bash
git branch backup/pre-credential-rewrite-main-2026-05-19 main
git branch backup/pre-credential-rewrite-aurora-v2-2026-05-19 aurora/v2
git branch backup/pre-credential-rewrite-aurora-redesign-2026-05-19 codex/aurora-redesign-2026-05-18
```

4. Create an offline mirror backup outside the working repo:

```bash
git clone --mirror https://github.com/WalksWithASwagger/kriskrug-wp.git /tmp/kriskrug-wp-pre-credential-rewrite.git
```

5. Rewrite locally with `git filter-repo`.

Conservative option A: remove disposable raw HTML snapshot files from all history, then re-add current sanitized snapshots if still needed.

```bash
git filter-repo \
  --path docs/current-state/raw/pages/ai-upgrade-for-creative-professionals.html \
  --path docs/current-state/raw/pages/contact.html \
  --invert-paths
```

Option B: replace exact secret values with redaction markers using a private replacement file.

```bash
chmod 600 /tmp/kriskrug-secret-replacements.txt
git filter-repo --replace-text /tmp/kriskrug-secret-replacements.txt
shred -u /tmp/kriskrug-secret-replacements.txt
```

Do not commit the replacement file. Do not paste its contents into chat, docs, issues, or PRs.

6. Re-scan rewritten history before push:

```bash
gitleaks git --no-banner --redact --log-level warn .
gitleaks dir --no-banner --redact --log-level warn .
```

7. Force-push only after the scan is clean and KK explicitly approves:

```bash
git push --force-with-lease origin main
git push --force-with-lease origin aurora/v2
git push --force-with-lease origin codex/aurora-redesign-2026-05-18
```

8. After push:

```bash
git fetch origin --prune
git rev-list --left-right --count main...origin/main
gh pr list --state open --limit 30
gitleaks git --no-banner --redact --log-level warn .
```

## Stop Rules

Stop and ask KK before:

- force-pushing any public branch,
- rewriting PR #77's branch while review is active,
- deleting old Claude branches,
- publishing any unredacted scanner output,
- treating current-tree cleanliness as proof that history is clean.
