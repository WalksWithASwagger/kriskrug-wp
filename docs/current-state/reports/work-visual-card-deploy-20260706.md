# Work Visual Cards Deploy Closeout - 2026-07-06

**Status:** live on production before this closeout branch
**Track:** Track A page content
**Issue:** #302
**Page:** Work, page ID `2672`, `/work/`

## Summary

The Creative AI Human Lab section on `/work/` now uses project-native visual cards for Both Hands Full, Punk Rock AI, Ethos and MADE ON, and the Photography archive. The final polish pass also removed default link underlines from the existing media-card anchors so the page reads as a consistent card grid.

This branch packages the already-live deploy into a reviewable repo change. No new live WordPress write is required for review or merge.

## Source And Evidence

- Source payload: `content/source-packs/content-architecture-2026/wp-payloads/work.html`
- Final deploy report: `backup/20260706T191550Z-content-architecture/deploy-report.json`
- Final snapshots: `backup/20260706T191550Z-content-architecture/page-snapshots/`
- Earlier visual-card write snapshots: `backup/20260706T190831Z-content-architecture/page-snapshots/`

The two snapshot directories form the deploy chain. `190831Z` captured the first visual-card write; `191550Z` captured the final no-underline polish write.

## Auth Note

The live closeout needed `WP_AUTH_MODE=login` in the gitignored `scripts/notion-to-wp/.env` because the available credential behaved as a wp-admin login rather than a WordPress Application Password. `WPClient` still defaults to Basic application-password auth; `login` mode is opt-in and uses the logged-in admin session nonce for REST calls.

## Verification

Required packaging checks:

```bash
python3 -m unittest scripts.tests.test_common scripts.tests.test_content_architecture_payloads
git diff --check -- scripts/common.py scripts/tests/test_common.py content/source-packs/content-architecture-2026/wp-payloads/work.html
```

Read-only orientation smoke was also run:

```bash
make status-readonly
```

Rollback pattern if production ever needs to be restored from the final snapshot:

```bash
python3 scripts/content_architecture_deploy.py \
  --restore \
  --snapshot-dir backup/20260706T191550Z-content-architecture/page-snapshots \
  --page work
```
