# Backup Plan — Getting a Full Local Copy of kriskrug.co

**Goal:** before any modification touches production, we have a local archive sufficient to rebuild the site from scratch.

## 2026-05-21 gate status

The repo has a local UpdraftPlus archive set from 2026-05-16 in `backup/2026-05-16/` with database, plugins, themes, mu-plugins, and other `wp-content` files. That set has checksums and a tracked manifest, but it is **not enough to reopen production writes** because:

- the 13 GB uploads archive was skipped and is only accounted for in the manifest;
- no `restore-notes.md` exists yet proving a local restore drill.

Use this command to inspect an archive set without claiming the production-write gate is satisfied:

```bash
make backup-check BACKUP_DIR=backup/2026-05-16
```

Use strict mode for the actual gate before live WordPress changes:

```bash
make backup-check BACKUP_DIR=backup/YYYY-MM-DD STRICT=1
```

Strict mode must pass before `/llms.txt`, robots, homepage H1/alt, Work metadata, sidebar promo deploy, schema migration, or Notion-to-WP production writes.

## The four pieces of a real WordPress backup

| Piece | What it contains | Have it locally? | How to get it |
|---|---|---|---|
| **Database dump** | Every post, page, comment, user, option, plugin setting | Partial: 2026-05-16 archive exists | `wp db export` (SSH) or AIO-WP-Migration / UpdraftPlus (plugin) |
| **`wp-content/themes/`** | Active theme + child theme + any others | Partial: 2026-05-16 archive exists | rsync over SSH, or plugin archive |
| **`wp-content/plugins/`** | All installed plugins | Partial: 2026-05-16 archive exists | rsync over SSH, or plugin archive |
| **`wp-content/uploads/`** | All media files (likely the largest piece — could be many GB) | Missing locally; 2026-05-16 manifest accounts for the gap | rsync over SSH, Pagely backup export, or plugin archive |

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
4. Note any breakage in `backup/<date>/restore-notes.md`.
5. Run `make backup-check BACKUP_DIR=backup/<date> STRICT=1`.

Until step 4 is done, the backup is unverified.

## Cadence going forward

| Trigger | Action |
|---|---|
| Before any plugin install / activate on production | Run backup (full set) |
| Before any theme code change | Run backup (DB + themes at minimum) |
| Before any database-affecting operation (cleanup, migration, large delete) | Run backup (DB only is acceptable) |
| Weekly during active modification work | Full backup, dated |
| Quiet weeks (no changes) | Skip — Pagely keeps off-site backups, don't accumulate duplicates locally |

## Pagely's own backups

Pagely keeps server-side backups automatically. **Don't** rely on these as our only line of defense — restoring from a managed-host backup typically means filing a ticket and waiting. Our local archive exists so we can verify changes against a known-good copy without needing the host's help.
