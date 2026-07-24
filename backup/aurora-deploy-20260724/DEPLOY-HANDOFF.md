# Aurora 1.4.0 Revive port — deploy handoff (2026-07-24)

## Status

**Live:** Aurora **1.4.0** with Revive cream/ink chrome + homepage.  
Public `style.css` Version readback matches. Cream contrast hardening fix applied to live theme files.

## Packages

- **Full theme (cream-fix):** `/Users/kk/Desktop/kk-aurora-revive-1.4.0-creamfix-1.4.0-20260724.zip`  
  SHA256: `17160188a7c8399807a1218700921edd7703e944703dcc66c782afbde63a4519`  
  Also copied to `backup/aurora-deploy-20260724/`.
- **Earlier theme zip (pre cream-fix):** `/Users/kk/Desktop/kk-aurora-revive-1.4.0-1.4.0-20260724.zip`  
  SHA256: `2d0b19850467a265ca94a07d38c7af11eea5bcb4bb8e8169fed81b649e4ef757`
- **Rollback 1.3.41:** `/Users/kk/Desktop/kk-aurora-rollback-1.3.41-20260724.zip`  
  SHA256: `57b298eaa8fbc21f0a2d1a1a8d855c80da506c2cd2ad950fdd2c80c56425a94f` (first package) / rebuild may differ by allow-dirty packaging

## How cream-fix landed after first zip

1. First 1.4.0 zip was uploaded (manual wp-admin replace).
2. Dark-theme `#090c11` contrast hardening still painted black type panes on cream.
3. Cream-fix CSS (`style.css` + `revive-port.css`) packaged as media zip **#12631**, applied once via Code Snippet **#14** (now **inactive**), option `kk_aurora_creamfix_140=done`.
4. Jetpack Boost rebuilt its concatenated CSS (new hash; `#090c11` count 0).

Optional cleanup: delete media **12631**, delete/retire snippet **#14**, purge PressCACHE if edge lags.

## Contract

See [docs/current-state/REVIVE-AURORA-PORT-2026-07-24.md](../../docs/current-state/REVIVE-AURORA-PORT-2026-07-24.md).

## Verify

```bash
curl -sL "https://kriskrug.co/wp-content/themes/kk-aurora/style.css?cb=$RANDOM" | head -20
# expect Version: 1.4.0 and cream contrast comment, no #090c11 opaque panes
```

Spot-check `/`, `/services/` (or `/generative-ai-services/`), `/contact/`, `/speaking/` — cream paper, woven marquee, **Work with me → `/services/`**, Beehiiv newsletter, no Field notes/Dispatch chrome labels.

Screenshots under `backup/aurora-deploy-20260724/screenshots/`.

## Rollback

Re-upload the 1.3.41 rollback zip via Appearance → Themes → Upload → Replace, purge caches.
