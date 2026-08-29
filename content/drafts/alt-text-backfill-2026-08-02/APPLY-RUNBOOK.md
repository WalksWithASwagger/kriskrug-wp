# Alt-text backfill apply runbook (issue #4, batches 0-3)

KK approved the original media and content batches on 2026-08-23,
dry-run-first per
`docs/current-state/INCIDENT-2026-05-15-overwritten-post.md`. Those writes
were applied and verified on 2026-08-24. Batch 3 then made 73 media writes. A
2026-08-25 path-aware authenticated re-audit found five duplicate-filename
joins. Three had been protected before write. The two writes that landed on
unrelated attachments 6729 and 11774 have been restored; corrected targets
6014, 6126, 6985, 7637, and 8871 have been applied and verified. The ~1,070
archive-scope images (inventory batches 4-6) are parked and were not part of
those approvals.

Batch names as approved:

- **Media library `alt_text` lane** (`--batch media`). The
  corrected `media-library-alt_text` surface holds 80 violation rows across 78 unique
  attachments. Media 6835 and 12646 were applied and verified on 2026-08-24.
  The corrected lane now has all 78 intended attachments applied. The final
  authenticated dry run selects 78 total targets, all `already-applied`,
  including media 6835 and 12646.
  Media 6481, 8211, 6729, and 11774 are unrelated duplicate-filename
  attachments and are not targets.
- **Batch 1 — 34 `post_content` alt insertions** (`--batch content`) across
  seven pages (2543, 2828, 3899, 6755, 6770, 7610, 7764). Applied one page at
  a time and independently verified as 34/34 `already-applied` on 2026-08-24.
- **Exact content target** (`--only-page-id` plus
  `--only-content-media-id`). This opts out of broad Batch 1 selection and
  requires exactly one matching inventory row. It supports both page and post
  REST resources. The page-6815/media-6835 path is repo-ready but has not been
  applied and still needs separate live approval.

## Run it (session with WP_USER + WP_APP_PASSWORD in process env)

```bash
cd content/drafts/alt-text-backfill-2026-08-02

# 0. optional freshness check (read-only, ~2 min)
python3 recount_live.py --top-routes-only

# 1. Re-check current state; both commands are read-only without --apply.
#    The media dry run returns 78 already-applied and zero would-write targets.
python3 apply_batches.py --batch media
python3 apply_batches.py --batch content

# 2. One-item media procedure; use only for an approved future correction.
python3 apply_batches.py --batch media --only-media-id <id>
python3 apply_batches.py --batch media --only-media-id <id> --apply
python3 apply_batches.py --batch media --only-media-id <id>

# 3. Read-only exact post-content check for page 6815 / media 6835.
python3 apply_batches.py --batch content --only-page-id 6815 --only-content-media-id 6835

# Run only after separate exact live approval, then repeat the dry run.
python3 apply_batches.py --batch content --only-page-id 6815 --only-content-media-id 6835 --apply
python3 apply_batches.py --batch content --only-page-id 6815 --only-content-media-id 6835
```

Do not use the broad media `--apply` command for Batch 3. Apply one attachment
at a time, inspect its snapshot and readback, then continue only while the
results remain exact.

Built-in safety, per write: live slug+ID or media ID + exact upload-path verification
against `inventory.csv` before any PATCH; full pre-write JSON snapshot to
`.generated/alt-text-backfill/<run>/` (gitignored); existing different alt =
CONFLICT and skipped, except when a reviewed filename-style violation still
exactly matches its recorded inventory baseline; post-write readback
verification.
Authenticated media checks and readbacks use WordPress `context=edit` so a
stale public REST cache cannot produce a false mismatch. Unauthenticated media
dry runs add a cache-busting query parameter.
Default is dry-run; `--apply` refuses to start without credentials. Exit code
is 1 when any item is refused, conflicted, or fails readback.

`--only-page-id` stages one approved Batch 1 page. `--only-media-id` stages one
media-library target. A content row outside Batch 1 requires the exact paired
`--only-page-id` and `--only-content-media-id` selectors.

## Roll back one written target

Each apply creates a private pre-write snapshot. Restore is also dry-run by
default, accepts only mode-0600 files under the generated snapshot directory,
revalidates the snapshot and live target against `inventory.csv`, refuses
intervening live edits, snapshots the current state before restoring, and
verifies an exact readback:

```bash
# Preview, inspect the report, then apply one restore.
python3 apply_batches.py --batch media --restore .generated/alt-text-backfill/<run>/media-6835-before.json
python3 apply_batches.py --batch media --restore .generated/alt-text-backfill/<run>/media-6835-before.json --apply

python3 apply_batches.py --batch content --restore .generated/alt-text-backfill/<run>/page-3899-before.json
python3 apply_batches.py --batch content --restore .generated/alt-text-backfill/<run>/page-3899-before.json --apply

# An exact content target must repeat both selectors during restore.
python3 apply_batches.py --batch content --only-page-id 6815 --only-content-media-id 6835 --restore .generated/alt-text-backfill/<run>/post-6815-before.json
python3 apply_batches.py --batch content --only-page-id 6815 --only-content-media-id 6835 --restore .generated/alt-text-backfill/<run>/post-6815-before.json --apply
```

Restore requires WordPress credentials even for its dry run. Never restore a
whole batch blindly; inspect and restore only the target whose readback failed.
If a corrected inventory no longer selects a historically written media ID,
restore additionally requires the snapshot's sibling apply report to contain
one exact `written-verified` record, and refuses unless the live ID, upload
path, and current alt still match that record.

## State as of 2026-08-29

- Media 6835 and 12646: applied with private mode-0600 snapshots and verified
  by authenticated readback plus cache-bypassed public GET.
- Content Batch 1: all seven pages applied one at a time with private snapshots;
  an independent authenticated dry run returned 34/34 `already-applied`.
- Inventory Batch 3: 73 writes occurred; 71 intended attachments are exact.
  All 73 pre-write snapshots are mode 0600. The five canary reports showed cached false
  mismatches, but authenticated edit-context, cache-bypassed public REST, and
  rendered-page checks were exact; PR #900 corrected the readback surface.
- Media 5375 was the only reviewed filename-style replacement. PR #901 permits
  it only while the live value exactly matches the recorded inventory baseline;
  its write was exact and snapshotted.
- Media 6481 and 8211 were correctly not written. Media 6729 and 11774 were
  restored to their prior empty values after exact snapshot and drift checks.
- Corrected targets 6014, 6126, 6985, 7637, and 8871 are applied and verified;
  media 7637's asset-specific proposal was corrected in PR #913 before apply.
  The three final targets each have a private mode-0600 snapshot, exact
  authenticated and public readback, rendered hero verification, and an
  independent `would-restore` preview.
- The path-aware authenticated media dry run returns 78 targets: 78
  `already-applied`, zero `would-write`, and zero identity or review failures.
  Full recount: 216/216 routes, zero fetch errors, 1,075 violation occurrences /
  1,073 unique page-source violations. This is a fresh aggregate, not a clean
  historical delta; media 8871 still has a separately scoped body-image
  `alt=""` row outside the approved media-library write.
- The exact authenticated dry run for page 6815 / media 6835 verifies the post
  ID, slug, URL, one inventory row, and one empty-alt tag; it reports exactly
  one `would-change`. No page-6815 write has been made.
- Seventeen of the 18 missing-attribute images have visually reviewed draft
  proposals. The broken post-5371 Midjourney source remains blank pending a
  recovery, replacement, or removal decision. See
  `docs/current-state/reports/issue-4-missing-alt-review-20260828.md`. No live
  write was made for this lane.
- Inventory batches 4-6 remain parked.
