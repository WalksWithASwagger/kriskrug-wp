# UpdraftPlus backup — 2026-05-16

**Source:** kriskrug.co (Pagely production)
**Triggered:** 2026-05-16 06:46 PT via wp-admin → UpdraftPlus → Backup Now
**Backup ID:** 741dbfb20abd
**Downloaded:** 2026-05-16 08:42-08:44 PT via Chrome MCP browser automation
**Method:** wp-admin UpdraftPlus UI → "Press here to download" → "Download to your computer" → ~/Downloads → moved here

## Files

| Part | Size | Notes |
|---|---|---|
| `…-db.gz` | 4.7 MB | MySQL dump (full database) |
| `…-plugins.zip` | 62 MB | All active + inactive plugins |
| `…-themes.zip` | 15 MB | Catch Responsive + any other themes |
| `…-mu-plugins.zip` | 52 KB | Must-use plugins |
| `…-others.zip` | 1.5 MB | wp-content/upgrade, wp-content/languages, etc. |
| `uploads` | 13 GB **SKIPPED** | Too large for browser dl. Available on Pagely live + the next backup cycle. For restore: re-sync from production via SSH/SCP or rebuild from media library. |

## Checksums (SHA-256)

See `manifest-checksums.txt`.

## Restore procedure

1. Spin up fresh WP install (Local by Flywheel, Cloudways dev, or production)
2. Install UpdraftPlus on the new install
3. Upload these 5 archive parts via UpdraftPlus → Existing Backups → Upload backup files
4. UpdraftPlus auto-detects the set; click Restore → tick all 5 components
5. After restore: pull `uploads/` from a recent Pagely backup, or re-sync from a live mirror
6. Run `wp search-replace` if restoring to a different domain
7. Re-deploy schema snippet (Code Snippet id 5) if missing — file is at [`fixes/schema-snippets-deployed.php`](../../fixes/schema-snippets-deployed.php)

## Coverage gap

The 13 GB uploads archive is the only component not in this set. If the live server is lost, uploads must be sourced from:

- **Pagely** — their nightly backup snapshot (contact support)
- **Wayback Machine** — for hero images, post-attached photos
- **KK's local archive** — `/Users/kk/Pictures/` originals where they exist
- **Re-attaching media** — slowest path, manual

For a partial-recovery scenario (DB/plugin/theme corruption, hack rollback), this 5-part set is fully sufficient.

## Provenance

This backup was triggered by Claude Code as part of [`docs/current-state/FIX_QUEUE.md`](../../docs/current-state/FIX_QUEUE.md) P0.1 ("Have a backup before we touch anything else"). It's the first full local backup of kriskrug.co since the May 15 2026 connector incident.

The backup is gitignored (see [`.gitignore`](../../.gitignore)) — these files are not pushed to GitHub. Manifest + checksums ARE tracked.
