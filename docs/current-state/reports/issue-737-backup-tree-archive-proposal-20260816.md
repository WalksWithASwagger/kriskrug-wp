# #737 backup/ tracked-tree archive proposal

**Status:** proposal only. **No `git rm --cached`, no deletes, no history rewrite.**
**Issue:** [#737](https://github.com/WalksWithASwagger/kriskrug-wp/issues/737) (final live `backup/` slice of [#318](https://github.com/WalksWithASwagger/kriskrug-wp/issues/318))
**Measured:** 2026-08-16 against `origin/main` `90552de`
**HTML ignore rule:** already on `origin/main` (commit `f684f17`, 2026-08-16). Probe: `git check-ignore -v backup/test.html` → `.gitignore:backup/**/*.html`.

This is the KK-approval packet for the existing 403-file tree. Do not execute the move until KK pastes an explicit allow-list.

---

## 1. Current tracked counts (`origin/main`)

`git ls-tree -r -l origin/main backup/` — **403 files, 15,432,097 bytes (14.72 MiB)**. Same headcount as the 2026-08-15 audit; bytes are ~14.7 MiB vs the audit's rounded 16 MB.

| Ext | Count | Bytes | MiB | Role |
|---|---:|---:|---:|---|
| `json` | 224 | 6,913,549 | 6.59 | REST readbacks, rollback payloads, deploy reports |
| `html` | 129 | 6,430,734 | 6.13 | Public page captures (new files already gitignored) |
| `png` | 2 | 1,848,073 | 1.76 | Leftover Aurora 1.4.0 home screenshots (new files already gitignored) |
| `txt` | 28 | 189,009 | 0.18 | `manifest-checksums.txt`, per-set `sha256sums.txt`, voice-sweep raw text |
| `md` | 18 | 39,997 | 0.04 | Handoffs, rollback notes, snapshot manifests |
| `diff` | 1 | 10,363 | 0.01 | Voice-sweep proposed.diff |
| `headers` | 1 | 372 | 0.00 | One HTTP headers capture |
| **Total** | **403** | **15,432,097** | **14.72** | |

JSON is **not** a tiny index. 106 files under `page-snapshots/` (4.12 MiB) embed full rendered content inside WP REST payloads. Rollback JSON is small: 28 files, 0.31 MiB. Nine `deploy-report.json` files total ~25 KiB.

---

## 2. What `make backup-check` actually needs

`Makefile` `backup-check` calls `scripts/verify-backup-set.sh [--allow-incomplete] backup/YYYY-MM-DD`. The script does **not** read any `.json`. It requires, inside that dated directory:

| Path / glob | Tracked today? | Notes |
|---|---|---|
| `manifest.md` | yes — `backup/2026-05-16/manifest.md` | Required |
| `manifest-checksums.txt` | yes — `backup/2026-05-16/manifest-checksums.txt` | Required; checksums the archives |
| `restore-notes.md` | **missing** even now | Warn in default mode; fail if `STRICT=1` |
| `*.wpress` **or** `*-db.gz`, `*-plugins.zip`, `*-themes.zip`, `*-mu-plugins.zip`, `*-others.zip` | **no** — already gitignored | Local-only; this checkout does not have them, so `make backup-check BACKUP_DIR=backup/2026-05-16` already fails on missing archives |
| uploads zip / dir | no | Manifest already records uploads as skipped |

The only dated backup-check set on `main` is `backup/2026-05-16/`. Other `manifest.md` files under `page-snapshots/` are QA snapshot indexes, not backup-check input.

**JSON decision (this PR records it, does not untrack anything):** keep `backup/**/*.json` **tracked**. They are the REST rollback / readback trail. They are not backup-check input, so a blanket `backup/**/*.json` ignore with Makefile negations would be the wrong shape — the Makefile needs zero JSON files, and ignoring them would also block future `rollback-*.json` commits. `.gitignore` comment updated to say this explicitly. A later KK pass may untrack bulky `page-snapshots/*.json` only; that is out of scope here.

---

## 3. Recommended keep vs `git rm --cached`

Execute **only** after KK approval and after the archive copy in §4 exists.

### Keep tracked (272 files, ~6.83 MiB)

- All **18** `*.md` (deploy handoffs, rollback notes, QA reports, snapshot manifests).
- `backup/2026-05-16/manifest.md` and `manifest-checksums.txt` (backup-check).
- All **224** `*.json` (rollback payloads + REST readbacks + deploy reports).
- All **28** `*.txt` (checksum sidecars + voice-sweep evidence).
- `backup/20260801-voice-sweep/what-would-chat-do-12032/proposed.diff`
- `backup/20260623-163028Z/homepage.headers`

### `git rm --cached` (131 files, ~7.89 MiB) — files stay on disk

Already ignored for **new** adds; this only stops the historical copies from occupying the working tree on every clone.

| Path glob | Count | MiB |
|---|---:|---:|
| `backup/**/*.html` | 129 | 6.13 |
| `backup/aurora-deploy-20260724/screenshots/aurora-140-home-1440.png` | 1 | 0.90 |
| `backup/aurora-deploy-20260724/screenshots/aurora-140-home-375.png` | 1 | 0.86 |

Expected after that PR: `git ls-files backup/ | wc -l` → **272**. HTML/PNG remain on disk if they were checked out; they will not re-enter the index.

### Do not do in that PR

- `git rm` (working-tree delete) of anything still useful as local rollback evidence.
- History rewrite / `git filter-repo` (deferred by #572).
- Ignoring or untracking JSON.

---

## 4. Out-of-git archive location

Workspace policy: non-git recovery material lives under `/Users/kk/Code/_archive/<repo>/`, not inside this public repo.

**Destination:** `/Users/kk/Code/_archive/kriskrug-wp/backup-tracked-tree-2026-08-16/`

Suggested copy **before** `git rm --cached` (run from a clean `main` checkout):

```bash
mkdir -p /Users/kk/Code/_archive/kriskrug-wp/backup-tracked-tree-2026-08-16
git -C /Users/kk/Code/kriskrug-wp ls-files backup/ \
  | rsync -a --files-from=- /Users/kk/Code/kriskrug-wp/ \
      /Users/kk/Code/_archive/kriskrug-wp/backup-tracked-tree-2026-08-16/
```

That snapshot is the rollback if a later clone needs the HTML/PNG without digging through git history. History still retains the blobs until #572.

---

## 5. KK reply template

```text
#737 approve shape: git rm --cached HTML + 2 leftover PNGs only
Allow-list = §3 "git rm --cached" in
docs/current-state/reports/issue-737-backup-tree-archive-proposal-20260816.md
Keep all md / json / txt / diff / headers.
Archive copy to /Users/kk/Code/_archive/kriskrug-wp/backup-tracked-tree-2026-08-16/
before the cached-rm PR. No filter-repo / force-push. No JSON ignore.
```

After that PR lands, update #318 to point at #737 as the closed `backup/` slice (draft-images residue stays on #318).
