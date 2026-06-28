# Deploying KK Marquee Board to kriskrug.co

This plugin lives in the repo because the live WordPress install isn't version-controlled here.
It makes `/marquee/` a real WordPress route. **Deployment is gated** (live writes require KK
approval + a WP application password). Nothing here runs automatically.

## Order of operations (the gated go-live)

1. **Deploy the plugin** (Path A or B below) → activate. Activation flushes rewrite rules.
2. **Deploy the theme templates** `theme/kk-aurora/templates/archive-marquee_board.html` and
   `single-marquee_board.html` on the next theme cutover (Track B). Until then WordPress falls
   back to `index.html`/`single.html`, which still work (plainer).
3. **Verify routing**: visit `/marquee/` (archive; empty until boards are synced) — should be 200,
   not 404. If 404, re-flush: **Settings → Permalinks → Save** (or `wp rewrite flush`).
4. **Add credentials**: create a WP application password (Users → Profile → Application Passwords)
   and put `WP_BASE_URL`, `WP_USER`, `WP_APP_PASSWORD` in `scripts/notion-to-wp/.env`.
5. **Dry-run the sync**, review payloads, then execute:
   ```bash
   python3 scripts/marquee/sync.py            # dry-run (default) — prints payloads, writes nothing
   python3 scripts/marquee/sync.py --execute  # live (KK approval) — creates boards, uploads OG images
   ```
6. **Verify**: a board page renders the LED board, `og:image` resolves to the uploaded card, and the
   board appears in `/sitemap.xml` (Jetpack auto-includes public CPTs).

## Path A — Upload via WP admin (fastest)

```bash
cd plugins && zip -r kk-marquee-board.zip kk-marquee-board
```
**Plugins → Add New → Upload Plugin** on kriskrug.co. Upload the zip and activate.

## Path B — SFTP / SSH

Upload `kk-marquee-board/` to `/wp-content/plugins/`, then activate **KK Marquee Board** in WP admin.

## Pre-deploy checks (run locally before zipping)

```bash
php plugins/kk-marquee-board/tests/smoke.php
find plugins/kk-marquee-board -name '*.php' -print0 | xargs -0 -n1 php -l
python3 -m unittest discover scripts/tests   # includes the offline REST-sync tests
```

## Safety (the sync follows the post-2026-05-15 rules)

- **Create-by-default.** An existing board with the same slug is NOT overwritten unless `--update`
  is passed, and even then a title-similarity guard (≥ 0.5) aborts on a wild mismatch.
- **Dry-run is the default.** Live writes require `--execute` AND credentials in `.env`.
- **Post-write readback** verifies slug/title/status after each write.
- **Source of truth stays the repo** (`content/marquee/marquee.json`); a bad sync is recoverable by
  re-running from the JSON.

## Rollback

Deactivate the plugin (deactivation flushes rewrite rules). `/marquee/` stops resolving; the boards
remain in the DB as drafts/published posts and can be trashed from **Marquee Boards** in wp-admin.
