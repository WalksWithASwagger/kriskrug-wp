# Rollback Playbook — If We Break Production

A blunt, pre-written sequence for when something on kriskrug.co goes wrong because of a change we made.

## Stop the bleeding first (≤ 5 minutes)

Before anything else:

1. **Stop making changes.** Don't try to "fix forward" until we know what broke.
2. **Capture the failure.** Screenshot the broken page. Note the URL, the exact error message, what we changed in the last 30 minutes.
3. **Open the site in an incognito window.** If it works there, the issue may be a logged-in / cached state rather than a true outage.
4. **Check Pagely status:** https://atomic.pagely.com → server health. If Pagely is degraded, sometimes "our" breakage is actually theirs.

## Then categorize the failure

| Symptom | Likely cause | Rollback path |
|---|---|---|
| White screen of death / "critical error" | Bad PHP — usually a recently edited theme/plugin file | A. Code rollback |
| Layout broken, content intact | Bad CSS or missing asset | B. CSS/asset rollback |
| Specific page returns 404 / wrong content | Bad page edit, slug change, or redirect rule | C. Content rollback |
| Settings missing / plugin not working | Bad plugin update or settings change | D. Plugin rollback |
| Site won't load at all from any browser | Host-level issue OR bad `.htaccess` / `wp-config.php` | E. Server-level rollback |

## A. Code rollback (theme / custom plugin / snippet)

**If the change was made via SSH / git:**
```bash
ssh <pagely-user>@<pagely-host>
cd /path/to/site
git log --oneline -5
git revert <bad-commit>   # or git reset --hard <good-commit> on a deploy branch
```

**If the change was made via wp-admin Appearance > Editor or Plugins > Editor:**
- This is the most fragile path. There's no version control on the server.
- Replace the file's contents from the most recent backup in `backup/<latest-date>/`.
- If we have no backup, contact Pagely support and request a snapshot rollback.

**If the change was via a code-snippets plugin (e.g. Code Snippets):**
- wp-admin → Snippets → deactivate the offending snippet (toggle off, don't delete) → site recovers immediately.

## B. CSS / asset rollback

Usually safe to do live:
- wp-admin → Appearance → Customize → Additional CSS → restore previous CSS from `backup/<date>/customizer-additional-css.txt` if we captured it, or empty the field as a quick test.
- For plugin-injected CSS (e.g. Popup Maker styles), disable the specific popup or rule rather than editing the plugin.

## C. Content rollback (a page or post is wrong)

WP keeps post revisions by default. Per page:
- wp-admin → edit the page → right sidebar → **Revisions** → restore the last good one.

If a page was deleted: wp-admin → Pages → **Trash** → restore.

If a slug changed and external links now 404: re-edit the page to the original slug (or add a redirect via Yoast/Rank Math/.htaccess).

## D. Plugin rollback

| Situation | Action |
|---|---|
| Plugin update broke things | wp-admin → Plugins → Deactivate the plugin. If still broken: install **WP Rollback** plugin → roll the offender back to the previous version. |
| New plugin install broke things | Deactivate + Delete. |
| Plugin **settings** changed but plugin works | Most plugins store settings in `wp_options`. Without a DB backup, restoring settings manually means recreating them. With a DB backup, see (E). |

## E. Server-level / nuclear options

In rough order of preference:

1. **Pagely snapshot restore.** Pagely takes nightly snapshots. File a support ticket: *"Please restore kriskrug.co to <date> snapshot."* They'll confirm before doing it. Production data created since the snapshot will be lost — list anything important first (recent posts, form submissions, orders).

2. **Restore from our local backup.** Requires:
   - The local archive in `backup/<date>/` (see `BACKUP_PLAN.md`)
   - SSH access to upload it
   - Either `wp db import` for the DB and rsync for files, or a backup-plugin restore from the same plugin that exported it (UpdraftPlus → UpdraftPlus, AIO → AIO)

3. **Roll back `wp-config.php` or `.htaccess`.** If we edited either of these and the site won't load:
   - SSH in (or use Pagely's file manager) → restore from the snapshot or replace with a known-good version. We should keep canonical copies in `backup/<date>/wp-config.php.txt` and `.htaccess.txt` (gitignored — wp-config has secrets).

## After the rollback

1. **Verify.** Hit the broken page, the homepage, an admin page, and at least one form. Run `curl -sS -I https://kriskrug.co/` and check status 200.
2. **Document.** Add a note to `docs/incidents/YYYY-MM-DD-summary.md`: what we did, what broke, how we rolled back, what we'll do differently. (Create the `incidents/` folder when first needed.)
3. **Make the lesson durable.** If we broke something because we lacked a backup, the next change pauses until backup is in place. If we broke it because we skipped a preview step, write the preview step into the relevant playbook.

## Tools to install proactively

Before any real modification work, these should be present on production:

- ✅ **UpdraftPlus** (or AIO-WP-Migration) — for the backup pipeline. Install once, schedule for safety.
- ✅ **WP Rollback** — one-click plugin/theme version rollback.
- ⚠️ **Health Check & Troubleshooting** (official WP plugin) — lets us run with all plugins disabled / default theme on a per-user basis for debugging without affecting visitors. Very useful when something breaks.
- ⚠️ **Query Monitor** — diagnostic when something is slow or throwing errors (dev-only; disable when not actively debugging).

The two ⚠️ tools are optional but make recovery dramatically easier. Worth considering for the first batch of changes.

## What we **do not** do

- ❌ Edit `wp-config.php` or `.htaccess` through wp-admin's file editor. Always SSH / SFTP these.
- ❌ Modify core WordPress files (`/wp-includes/`, `/wp-admin/`). Ever.
- ❌ "Try something" on production to see what happens. If we don't know the outcome, that's a dev-server experiment.
- ❌ Apply a plugin or theme update during a high-traffic window without a current backup.
