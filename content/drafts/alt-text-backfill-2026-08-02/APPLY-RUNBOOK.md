# Alt-text backfill apply runbook (issue #4, batches 0-3)

KK approved the original media and content batches on 2026-08-23,
dry-run-first per
`docs/current-state/INCIDENT-2026-05-15-overwritten-post.md`. Those writes
were applied and verified on 2026-08-24. Batch 3 then completed with 73 safe
media writes and two protected shared-context skips (6481 and 8211). The
~1,070 archive-scope images (inventory batches 4-6) are parked and were not
part of that approval.

Batch names as approved:

- **Media library `alt_text` lane** (`--batch media`). The
  corrected `media-library-alt_text` surface holds 77 violation rows across 75 unique
  attachments. Media 6835 and 12646 were applied and verified on 2026-08-24.
  Batch 3 adds 73 applied attachments. The broad authenticated dry run now
  selects 75 total targets and returns 75 `already-applied`; no media write
  remains in this lane. Three historical rows involving attachments 6481 and
  8211 are `investigate-shared-media-context`, not media-write targets.
- **Batch 1 — 34 `post_content` alt insertions** (`--batch content`) across
  seven pages (2543, 2828, 3899, 6755, 6770, 7610, 7764). Applied one page at
  a time and independently verified as 34/34 `already-applied` on 2026-08-24.

## Run it (session with WP_USER + WP_APP_PASSWORD in process env)

```bash
cd content/drafts/alt-text-backfill-2026-08-02

# 0. optional freshness check (read-only, ~2 min)
python3 recount_live.py --top-routes-only

# 1. Re-check current state; both commands are read-only without --apply.
#    The media dry run should return 75 already-applied targets.
python3 apply_batches.py --batch media
python3 apply_batches.py --batch content

# 2. Historical one-item procedure; use only for an approved future correction.
python3 apply_batches.py --batch media --only-media-id <id>
python3 apply_batches.py --batch media --only-media-id <id> --apply
python3 apply_batches.py --batch media --only-media-id <id>
```

Do not use the broad media `--apply` command for Batch 3. Apply one attachment
at a time, inspect its snapshot and readback, then continue only while the
results remain exact.

Built-in safety, per write: live slug+ID (or media ID + file) verification
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

`--only-page-id` / `--only-media-id` stage one target at a time if wanted.

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
```

Restore requires WordPress credentials even for its dry run. Never restore a
whole batch blindly; inspect and restore only the target whose readback failed.

## State as of 2026-08-24

- Media 6835 and 12646: applied with private mode-0600 snapshots and verified
  by authenticated readback plus cache-bypassed public GET.
- Content Batch 1: all seven pages applied one at a time with private snapshots;
  an independent authenticated dry run returned 34/34 `already-applied`.
- Inventory Batch 3: 73 attachments applied and exact. All 73 pre-write
  snapshots are mode 0600. The five canary reports showed cached false
  mismatches, but authenticated edit-context, cache-bypassed public REST, and
  rendered-page checks were exact; PR #900 corrected the readback surface.
- Media 5375 was the only reviewed filename-style replacement. PR #901 permits
  it only while the live value exactly matches the recorded inventory baseline;
  its write was exact and snapshotted.
- Media 6481 and 8211 were not written. Their existing meaningful library alts
  serve other contexts, so three inventory rows are now investigation-only.
- Final authenticated media dry run: 75/75 targets `already-applied`, zero
  identity failures. Full recount: 216/216 routes, zero fetch errors, 1,078
  violation occurrences / 1,077 unique page-source violations.
- Inventory batches 4-6 remain parked.
