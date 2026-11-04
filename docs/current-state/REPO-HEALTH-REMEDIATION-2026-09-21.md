# Repository Health Remediation: September 2026 Audit

**Status:** Complete as of 2026-09-30. This is the closeout record for the
2026-09-20 repository audit. It is not a live WordPress, theme deployment,
branch cleanup, or workflow-settings authorization.

Audit baseline: `f5a2dd01f6537d29dbc2b2803da6c7802637a719`. Completion
readback: `main` at `edeac1e2e842dba7e46bed0fe668037fb4e742a2`, equal to
`origin/main` on 2026-09-30. The active live-content procedures remain in
[`WORK-PLAN-2026-09-09.md`](WORK-PLAN-2026-09-09.md).

## Outcome

| Priority | Issue | Result | Delivery |
|---|---|---|---|
| P1 | [#1034](https://github.com/WalksWithASwagger/kriskrug-wp/issues/1034) | SFTP verifies an explicitly trusted host key before password authentication; unknown, changed, and untrusted fallback hosts fail closed | PR #1079, `d2cb2cf` |
| P1 | [#1035](https://github.com/WalksWithASwagger/kriskrug-wp/issues/1035) | Events restore is preview-first, validates snapshot and live identity, requires the reviewed current-content SHA, snapshots current state, and verifies readback | PR #1079, `d2cb2cf` |
| P1 | [#1036](https://github.com/WalksWithASwagger/kriskrug-wp/issues/1036) | Shared WordPress reads retain bounded retries; writes are attempted once and surface ambiguous outcomes for reconciliation | PR #1079, `d2cb2cf` |
| P1 | [#1037](https://github.com/WalksWithASwagger/kriskrug-wp/issues/1037) | The JavaScript syntax target fails when any checked file fails, including an early file in the loop | PR #1079, `d2cb2cf` |
| P2 | [#1038](https://github.com/WalksWithASwagger/kriskrug-wp/issues/1038) | Startup truth preserves valid failure JSON and separates failed checks from unavailable data | PR #1092, `7ebf362` |
| P2 | [#1039](https://github.com/WalksWithASwagger/kriskrug-wp/issues/1039) | Dependabot now owns one weekly root npm update lane without changing package versions in that PR | PR #1093, `740fc44` |
| P2 | [#1040](https://github.com/WalksWithASwagger/kriskrug-wp/issues/1040) | Current docs distinguish configured and enabled workflows, verified and missing backup material, browser-test prerequisites, and dated theme deployment evidence | PR #1112, `609516d` |
| P2 | [#1041](https://github.com/WalksWithASwagger/kriskrug-wp/issues/1041) | Backlog reconciliation reports ancestry merges and exact same-repository squash-head matches with PR/SHA evidence while remaining report-only | PR #1113, `c966c05` |

All eight issues were closed by 2026-09-30. No production deployment,
WordPress write, workflow enablement, branch deletion, or worktree removal was
part of this remediation.

## Verification contract

The focused regression set covers the original negative cases:

- `scripts/tests/test_deploy_theme_sftp.py`: trusted, unknown, mismatched,
  fallback, port-qualified, missing-file, and failed-auth host-key paths.
- `scripts/tests/test_deploy_events_page.py`: wrong snapshot/live identity,
  preview-only restore, missing or stale expected hash, successful restore,
  readback failure, filtered content, and concurrent edits.
- `scripts/tests/test_common.py`: safe-method retries, single-attempt writes,
  4xx behavior, and ambiguous write failures.
- `scripts/tests/test_javascript_syntax_gate.py`: invalid-first,
  invalid-middle, and all-valid JavaScript lists.
- `scripts/tests/test_morning_truth_report.py`: exit-1 valid smoke JSON,
  malformed output, and unavailable data.
- `scripts/tests/test_reconcile_backlog.py`: normal merge, exact squash head,
  post-merge commits, reused names, checked-out work, pagination, and API
  failure.

Repository gates remain:

```sh
make verify
make status-readonly
make docs-truth-check
npm audit --json
python3 scripts/reconcile_backlog.py --stale-days 90
```

`make status-readonly` on 2026-09-30 preserved the valid WordPress-version
failure payload: it reported eight passing public-route checks and the exact
7.0.5 expected versus 7.0.6 observed version drift. It did not mislabel the
smoke result as unavailable.

## Remaining external gates

- A future SFTP session still requires a Pagely host key enrolled from a
  trusted out-of-band source. Repository tests use synthetic keys; they do not
  prove the provenance of a local `known_hosts` entry or authorize a real
  connection.
- The May 16 local backup has verified manifest/checksum metadata but its five
  named archive payloads are absent. Pagely retention and full restore
  readiness remain unverified; [`BACKUP_PLAN.md`](BACKUP_PLAN.md) is the
  current source of truth.

## Repeatable audit checks

Future repo-health passes should automate these five read-only checks:

1. Run `make doctor`, `make status-readonly`, and the public theme-version
   readback, preserving structured failure output.
2. Run the full local/CI gate plus the negative safety regressions above.
3. Compare GitHub workflow file presence with Actions API enablement and recent
   run state.
4. Reconcile open issues, PRs, remote branches, merged PR heads, worktrees, and
   divergence without deleting anything.
5. Audit dependency manifests, secrets/config boundaries, backup evidence,
   deployment receipts, and active-doc claims against current provider state.
