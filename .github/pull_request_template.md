## Summary

<!-- What changed and why, in a few lines. -->

Closes #

## Lane

One per PR. Mixing lanes is scope creep (see [`AGENTS.md`](../AGENTS.md)).

- [ ] Track A: content, SEO, posts, pages, media, schema, redirects, snippets
- [ ] Track B: Aurora theme, FSE templates, `theme.json`
- [ ] Docs, tooling or tests only

## Checks run

Paste the result or mark not applicable.

- [ ] `make python-test`
- [ ] `make validate`
- [ ] `make theme-smoke` (theme changes)
- [ ] `make docs-truth-check` (docs changes)
- [ ] `make ruff-changed BASE_REF=origin/main` (Python changes)
- [ ] `make voice-check` (payload copy or theme templates)

## Live-write safety

Skip if nothing touches the live site.

- [ ] Dry run first, and slug/ID verified as the intended target
- [ ] Snapshot or rollback path noted below
- [ ] No secrets, hosts or personal data in this PR (the repo is public)

## Approvals and merge

Merge rules and which PRs need KK first live in the [merge-lane table](../AGENTS.md#merge-lanes). Do not restate them here.

- [ ] This PR needs KK's approval before merge (theme, `plugins/`, `inc/`, `fixes/` snippet sources, or a deploy)
- [ ] `Test PR / summary` is green and the branch is up to date with `main`

Merging is not deploying. A live deploy is a separate act and needs explicit KK approval every time.

## Notes for reviewers

<!-- Rollback path, follow-ups, anything surprising. -->
