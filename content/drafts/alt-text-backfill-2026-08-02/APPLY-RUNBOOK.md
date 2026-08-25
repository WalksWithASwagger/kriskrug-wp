# Alt-text backfill apply runbook (issue #4, batches 0-3)

KK approved the original media and content batches on 2026-08-23,
dry-run-first per
`docs/current-state/INCIDENT-2026-05-15-overwritten-post.md`. Those writes
were applied and verified on 2026-08-24. The 76 inventory Batch 3 rows were
then drafted from visual review. Five Batch 3 canary attachments were applied
and independently verified on 2026-08-24; KK then approved proceeding with
the remaining 70 reviewed attachments. The ~1,070 archive-scope images
(inventory batches 4-6) are parked and are not part of that approval.

Batch names as approved:

- **Media library `alt_text` lane** (`--batch media`). The
  `media-library-alt_text` surface holds 80 violation rows across 77 unique
  attachments. Media 6835 and 12646 were applied and verified on 2026-08-24.
  The remaining 76 rows cover 75 unique attachments in inventory Batch 3;
  their strings were drafted from visual review. Five canaries are live and
  verified; 70 approved attachments remain.
  **The broad `--batch media --apply` command now selects all 77 attachments.**
  Do not run it for Batch 3; the approved procedure still requires one exact
  `--only-media-id` at a time.
- **Batch 1 — 34 `post_content` alt insertions** (`--batch content`) across
  seven pages (2543, 2828, 3899, 6755, 6770, 7610, 7764). Applied one page at
  a time and independently verified as 34/34 `already-applied` on 2026-08-24.

## Run it (session with WP_USER + WP_APP_PASSWORD in process env)

```bash
cd content/drafts/alt-text-backfill-2026-08-02

# 0. optional freshness check (read-only, ~2 min)
python3 recount_live.py --top-routes-only

# 1. Re-check current state; both commands are read-only without --apply.
#    The media dry run includes the 75 unapproved Batch 3 attachments.
python3 apply_batches.py --batch media
python3 apply_batches.py --batch content

# 2. After explicit approval, stage exactly one Batch 3 attachment.
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
CONFLICT, skipped, never overwritten; post-write readback verification.
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
- Inventory Batch 3: 76 rows / 75 unique attachments drafted after inspecting
  every rendered image; CSV and target-loader checks pass. Media 12597, 12593,
  12541, 12536, and 12528 are live and exact by authenticated and cache-bypassed
  public readback. Their original apply reports showed false mismatches because
  the old helper read a stale public REST response immediately after writing;
  this helper now binds both media reads to authenticated edit context.
- KK approved proceeding one attachment at a time with the remaining 70
  reviewed Batch 3 IDs. That approval does not include inventory batches 4-6.
- Inventory batches 4-6 remain parked.
