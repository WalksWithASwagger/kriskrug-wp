# Deploying KK Sidebar Promos to kriskrug.co

This plugin lives in the issue-tracking repo because the live WordPress install isn't version-controlled here. Two install paths — pick whichever is easier.

## Path A — Upload via WP admin (fastest)

1. Zip the plugin folder:
   ```bash
   cd plugins
   zip -r kk-sidebar-promos.zip kk-sidebar-promos
   ```
2. **Plugins → Add New → Upload Plugin** on kriskrug.co. Upload the zip and activate.
3. **Sidebar Promos → Settings** in the admin sidebar. Paste your Luma iCal URL (see below).
4. Click **Run Luma sync now** to verify the first event imports.
5. **Appearance → Editor** (or **Appearance → Widgets** for the classic widget area). Add the **KK Sidebar Promos** block to the sidebar template part. Remove the four old hard-coded image blocks.

## Path B — SFTP / SSH

1. Upload the `kk-sidebar-promos/` directory to `/wp-content/plugins/` on the server.
2. **Plugins** in WP admin → activate **KK Sidebar Promos**.
3. Continue from step 3 above.

## Finding your Luma iCal URL

1. On lu.ma, open the calendar you want to sync (e.g. `lu.ma/vancouver-ai`).
2. Click the calendar settings (gear icon).
3. Look for **Subscribe via iCal** — copy that URL.
4. Paste into **Sidebar Promos → Settings → Luma iCal URL**.

If Luma changes the URL format and the sync starts failing, the plugin logs an admin notice on the settings page; just refresh the iCal URL there.

## What gets created on activation

- Custom post type **Sidebar Promos** in the admin menu.
- 4 published Pillar promos: Animation Accelerator, RAP Certification, BC+AI Membership, Vancouver AI Community.
- Two daily WP-Cron jobs: `kk_sp_expire_featured` and `kk_sp_luma_sync`.

## Pre-deploy checks

Run these locally before zipping or uploading the plugin:

```bash
php plugins/kk-sidebar-promos/tests/smoke.php
find plugins/kk-sidebar-promos -name '*.php' -print0 | xargs -0 -n1 php -l
```

The smoke test covers limit normalization, the no-promos empty state, featured-image alt handling, featured-promo expiry behavior, and the Luma iCal parser without requiring a full WordPress install.

## Replacing the existing sidebar graphics

Once the block is rendering, edit each of the seeded Pillar promos and:

1. Set a featured image (square or 4:3 — see `assets/img-templates/SPECS.md`).
2. Confirm the link URL is right.
3. Tweak the excerpt copy if needed.

The four old image blocks in the sidebar template can then be removed.

## Adding a time-bound Featured promo

1. **Sidebar Promos → Add New**.
2. Title, excerpt, featured image as normal.
3. In the **Promo Settings** sidebar: set **Type** to "Featured" and **Active until** to the last day it should appear.
4. Publish. It takes the top slot until the end date passes, then auto-moves to draft.

If two Featured promos overlap, the most recently published one wins. The other waits in the queue (still published, still not expired) — it just doesn't render.

## Uninstall

Deactivating clears the cron schedules. The CPT and existing promo posts stay until you delete the plugin entirely.

## Rolling back

Deactivate the plugin and re-add the old image blocks. Promo posts remain in the database; reactivating restores the system without losing data.
