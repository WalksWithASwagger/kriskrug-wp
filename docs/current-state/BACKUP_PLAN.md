# Backup Plan — Getting a Full Local Copy of kriskrug.co

**Goal:** keep a practical backup and rollback discipline for kriskrug.co without blocking ordinary publishing work on strict restore-drill proof.

## 2026-05-22 operating status

The strict backup/restore proof gate is retired. Do not use missing restore proof as a blanket blocker for drafts, publish work, small page edits, or other bounded Track A work.

For ordinary Track A work, use the smallest reliable rollback path: draft-first publishing, exact slug/ID/status checks, page/post snapshots before overwriting existing content, reversible snippets, and live readback after the change. Use a full backup when the blast radius justifies it. Targeted rollback snapshots under `backup/` are not a substitute for a complete WordPress archive.

## 2026-09-30 recheck of `backup/2026-05-16/`

`make backup-check BACKUP_DIR=backup/2026-05-16` failed with 6 errors and 2 warnings. That nonzero result is expected evidence, not a problem this issue is allowed to "fix" by creating archives. Missing local files do not prove Pagely backups are absent.

| Class | What this checkout actually has |
|---|---|
| **Verified local files** | Tracked `backup/2026-05-16/manifest.md` and `manifest-checksums.txt` (the checksum list names five archives). |
| **Missing local archives** | `*-db.gz`, `*-plugins.zip`, `*-themes.zip`, `*-mu-plugins.zip`, and `*-others.zip` are not on disk. Checksums cannot be verified. `restore-notes.md` is still absent. The 13 GB uploads archive was already recorded as skipped in the May 16 manifest. |
| **Unverified host retention** | Pagely's product includes host-side backups. This session did not inspect Pagely retention, restore windows, or ticket SLAs. Do not treat host backups as confirmed or as absent. |

Use this command to re-inspect the set. A failing run that reports missing archives is truthful:

```bash
make backup-check BACKUP_DIR=backup/2026-05-16
```

Use strict mode only when a task specifically needs restore-drill proof, such as theme activation, bulk destructive cleanup, or a high-blast-radius migration:

```bash
make backup-check BACKUP_DIR=backup/YYYY-MM-DD STRICT=1
```

## The four pieces of a real WordPress backup

| Piece | What it contains | Have it locally? (2026-09-30) | How to get it |
|---|---|---|---|
| **Database dump** | Every post, page, comment, user, option, plugin setting | Missing local archive; only the May 16 checksum name is tracked | `wp db export` (SSH) or AIO-WP-Migration / UpdraftPlus (plugin) |
| **`wp-content/themes/`** | Active theme + child theme + any others | Missing local archive; only the May 16 checksum name is tracked | rsync over SSH, or plugin archive |
| **`wp-content/plugins/`** | All installed plugins | Missing local archive; only the May 16 checksum name is tracked | rsync over SSH, or plugin archive |
| **`wp-content/uploads/`** | All media files (likely the largest piece — could be many GB) | Missing locally; May 16 manifest already recorded the skip | rsync over SSH, Pagely backup export, or plugin archive |

Plus, optionally: `wp-config.php` (gitignore — has secrets), mu-plugins, drop-ins, root `.htaccess`.

## Two paths, depending on SSH availability

### Path A — SSH on Pagely (preferred, when ready)

When you have SSH credentials, this is the clean, scriptable version. We add a `backup/` directory (gitignored except for the script + a manifest), and the script becomes the source of truth:

```bash
# Run from /Users/kk/Code/kriskrug-wp on a Mac with SSH key uploaded to Pagely
./scripts/backup-from-pagely.sh
# → backup/2026-05-14/
#     db.sql.gz
#     wp-content-themes.tar.gz
#     wp-content-plugins.tar.gz
#     wp-content-uploads.tar.gz   (large — may be gitignored or stored elsewhere)
#     manifest.txt   (sizes, checksums, WP version, plugin/theme list)
```

The script will use `wp db export` for the DB and `tar` over SSH for the wp-content pieces, with checksums recorded in a manifest. This becomes runnable before each modification session.

### Path B — Backup plugin (works today, no SSH needed)

Recommended plugin: **UpdraftPlus** (free version is enough for one-off backups; remote-storage Premium is nice-to-have but not required).

Steps:
1. wp-admin → Plugins → Add New → search **UpdraftPlus** → Install + Activate
2. Settings → UpdraftPlus Backups → **Backup Now**
3. Tick all options (DB + plugins + themes + uploads + others)
4. When the archive set finishes, download all 5 files to `~/Downloads/kriskrug-backup-YYYY-MM-DD/`
5. Move that folder into `kriskrug-wp/backup/2026-05-14/` (gitignored)
6. Record what we got in `backup/<date>/manifest.md`
7. Run `make backup-check BACKUP_DIR=backup/<date>` to verify checksums and surface any missing restore proof.

Alternative plugin: **All-in-One WP Migration** — one `.wpress` file, simpler but a single proprietary format. Fine if UpdraftPlus has trouble.

> ⚠️ If the uploads directory is large, the plugin may time out. Pagely usually handles this OK, but if it fails, fall back to backing up DB + code separately and pulling uploads later via SSH.

## What "good" looks like

A backup is acceptable when **all four** of these are true:

1. We have a fresh `db.sql` (or `.wpress`) that opens in MySQL / Local-by-Flywheel and produces a functioning copy of the site.
2. We have **catch-responsive** theme files at the same version as production (2.8.7), and a way to confirm whether the production copy has any local modifications vs. upstream.
3. We have the plugin folder, with at least Jetpack, Popup Maker, Zero BS CRM, Site Kit, Akismet present.
4. We have the uploads folder — or, if too large for the plugin path, an explicit decision to defer it until SSH is available and a list of what's missing.

Each backup gets a manifest like:

```
backup/2026-05-14/manifest.md
  wordpress_version: 6.9.4
  active_theme: catch-responsive 2.8.7
  total_pages: 34
  total_posts: ~868
  plugins_detected: jetpack 15.8, popup-maker 1.22.0, zero-bs-crm <unknown>, site-kit 1.178.0, akismet <unknown>
  files:
    db.sql.gz            (sha256: ...)  XX MB
    wp-content.tar.gz    (sha256: ...)  XX MB
    uploads.tar.gz       (sha256: ...)  XX GB   [or "deferred"]
```

## Restore drill (we should do one)

A backup that's never been restored is a hope, not a backup. After the first archive lands:

1. Spin up **Local by Flywheel** (or Docker) — see `docs/local-development-setup.md`.
2. Restore the archive into the local instance.
3. Confirm: homepage renders, an arbitrary recent post renders, wp-admin opens, plugin settings are intact.
4. Note the result in `backup/<date>/restore-notes.md`.
5. Run `make backup-check BACKUP_DIR=backup/<date> STRICT=1`.

Until step 4 is done, the backup is unverified.

Strict mode requires the restore notes to include one of these markers:

```yaml
restore_status: passed
```

or:

```yaml
production_write_gate: passed
```

Use `failed` or omit the marker when the restore is incomplete.

## Cadence going forward

| Trigger | Action |
|---|---|
| Before any plugin install / activate on production | Run backup (full set) |
| Before any theme code change | Run backup (DB + themes at minimum) |
| Before any database-affecting operation (cleanup, migration, large delete) | Run backup (DB only is acceptable) |
| Weekly during active modification work | Full backup, dated |
| Quiet weeks (no changes) | Skip — Pagely keeps off-site backups, don't accumulate duplicates locally |

## Pagely's own backups

Pagely advertises server-side backups. Host retention is **unverified** in this checkout: no current snapshot list, restore window, or ticket SLA was read back on 2026-09-30. Do not treat that product feature as a confirmed local copy, and do not treat missing local archives as proof the host has none. Restoring from a managed-host backup typically means filing a ticket and waiting. Targeted page/post snapshots under `backup/` remain the ordinary rollback path until a verified archive set exists.
