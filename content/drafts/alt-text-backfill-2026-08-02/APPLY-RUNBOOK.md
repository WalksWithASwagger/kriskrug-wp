# Alt-text backfill apply runbook (issue #4, batches 0-1)

KK approved batches 0-1 on 2026-08-23, dry-run-first per
`docs/current-state/INCIDENT-2026-05-15-overwritten-post.md`. The ~1,070
archive-scope images (inventory batches 4-6) are parked.

Batch names as approved:

- **Batch 0 — media library `alt_text` writes** (`--batch media`). The
  `media-library-alt_text` surface holds 80 violation rows, but only the 2
  attachments with drafted strings (media 6835 and 12646, from inventory
  batch 2) are apply-ready. The other 76 hero images (inventory batch 3) have
  no drafted strings yet; the script reports them and never writes them —
  a script must not invent alt text. Drafting those 76 strings is the
  follow-up that unlocks the rest of this batch.
- **Batch 1 — 34 `post_content` alt insertions** (`--batch content`) across
  seven pages (2543, 2828, 3899, 6755, 6770, 7610, 7764), strings verbatim
  from `inventory.md` / `inventory.csv` including NCRs.

## Run it (session with WP_USER + WP_APP_PASSWORD in process env)

```bash
cd content/drafts/alt-text-backfill-2026-08-02

# 0. optional freshness check (read-only, ~2 min)
python3 recount_live.py --top-routes-only

# 1. dry-run both batches, read the reports
python3 apply_batches.py --batch media
python3 apply_batches.py --batch content

# 2. apply batch 0, then verify
python3 apply_batches.py --batch media --apply
python3 apply_batches.py --batch media          # expect all already-applied

# 3. apply batch 1, then verify
python3 apply_batches.py --batch content --apply
python3 apply_batches.py --batch content        # expect no-op / already-applied
```

Built-in safety, per write: live slug+ID (or media ID + file) verification
against `inventory.csv` before any PATCH; full pre-write JSON snapshot to
`.generated/alt-text-backfill/<run>/` (gitignored); existing different alt =
CONFLICT, skipped, never overwritten; post-write readback verification.
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

## State as of 2026-08-23 (credential-free dry run, this session)

- Batch 0: both media IDs verified live, `alt_text` still empty, status
  `would-write`. 76 rows reported needs-review (no strings drafted).
- Batch 1: all 7 pages verified slug+ID against live, 34/34 rows matched an
  empty-alt image in the rendered content, 0 conflicts. Unauthenticated runs
  match against `content.rendered`; the apply path edits `content.raw`.
