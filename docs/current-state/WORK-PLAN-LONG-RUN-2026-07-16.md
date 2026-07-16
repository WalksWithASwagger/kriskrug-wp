# Long-run work day queue — agent issues to file (2026-07-16)

Use this when KK can take actions again (secrets + approvals). Ordered by leverage. Prefer filing as GitHub issues (or confirming the existing numbers) before starting.

## Paste to a fresh agent

```text
Long-run day. Secrets may or may not be present — check env first.
1) If open: finish/merge PR #367 hygiene/orchestra stack, then delete its branch.
2) Work existing Monday queue live gates in order: #362 → #363 → #364 → #365.
3) If those are blocked, pick the next filed long-run issue below — one lane per PR.
No live WP writes without exact KK approval of the artifact/checklist.
```

## Ordered day issues (file or already exist)

| Order | Title | Exists? | Track | Needs |
|---:|---|---|---|---|
| L1 | Deploy Aurora 1.3.40 + post-deploy public smoke | #362 / #351 | B | KK checksum upload |
| L2 | Refresh #339 checklist to 1.3.40 hashes, then run publisher batch | #339 / #363 | A | live 1.3.40 + ticks + secrets |
| L3 | Apply KK-approved #284 hub-link wraps (non-Indigenous first) | #364 / #284 | A | patch_id list + secrets |
| L4 | Accessibility statement → WP **draft** only | #365 / #288 | A | human gates + secrets |
| L5 | Deploy schema identity snippet (retire Generative AI Tools wording) | #316 | A/ops | KK + secrets |
| L6 | Align `blogname` / OG site name; verify home OG + blog canonicals live | #345 / #346 / #347 | A/ops | KK + secrets / post-deploy |
| L7 | Migrate remaining body-H1 routes one target at a time | #353 | A | secrets + per-target confirm |
| L8 | Decide + implement taxonomy sitemap / archive indexability | #331 | A/ops | human policy first |
| L9 | Repo bloat reclaim — execute KK-approved prune from hygiene report | #318 / **#369** | ops | KK approval of delete list |
| L10 | Keep/kill leftover remote branches after prune | **#368** | ops | KK call |

## Agent-safe fillers if everything live is blocked

1. #256 CSS dead-code + schema-snippets repo reconcile  
2. #46 public pa11y five-route refresh  
3. #4 public image-alt inventory refresh (no media PATCH)  
4. Closeout docs for #254 / #361 / #36 once KK closes in UI  

Draft mirror of this file also lives for filing: `issues-to-create/long-run-workday-2026-07-16.md`.
