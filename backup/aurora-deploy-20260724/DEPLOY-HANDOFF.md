# Aurora Revive port — deploy handoff (2026-07-24)

## Status

**Live:** Aurora **1.4.3** (R5 left-pin header + R6 rainbow/riso).  
Public `style.css` Version `1.4.3`. Full theme sync media **#12636** (snippet **#20**, inactive).  
E2E: [e2e/E2E-REPORT-1.4.3-2026-07-24.md](e2e/E2E-REPORT-1.4.3-2026-07-24.md). Prior: 1.4.2 media **#12635** / 1.4.1 media **#12633**. Revisions: [../../docs/current-state/REVIVE-AURORA-REVISIONS-2026-07-24.md](../../docs/current-state/REVIVE-AURORA-REVISIONS-2026-07-24.md).

## Packages

- **1.4.1 a11y polish:** `/Users/kk/Desktop/kk-aurora-revive-a11y-1.4.1-1.4.1-20260725.zip`  
  SHA256: `725a88ab8f1e2f141169d1b16bfc56ee47e06423da9d745a4b52f067620fbd84`  
  Also in `backup/aurora-deploy-20260724/`. Media **#12633**.
- **Full theme 1.4.0 (cream-fix):** `/Users/kk/Desktop/kk-aurora-revive-1.4.0-creamfix-1.4.0-20260724.zip`  
  SHA256: `17160188a7c8399807a1218700921edd7703e944703dcc66c782afbde63a4519`  
  Media **#12632** (snippet **#15**, inactive).
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
# expect Version: 1.4.1 and cream contrast comment, no #090c11 opaque panes
curl -sL "https://kriskrug.co/wp-content/themes/kk-aurora/assets/css/revive-port.css?cb=$RANDOM" | head -20
# expect 1.4.1 banner + --revive-accent-text
```

Spot-check `/`, `/services/` (or `/generative-ai-services/`), `/contact/`, `/speaking/` — cream paper, woven marquee, **Work with me → `/services/`**, Beehiiv newsletter, no Field notes/Dispatch chrome labels. Confirm one Skip link and visible focus rings on header links.

Screenshots under `backup/aurora-deploy-20260724/screenshots/`.

## Rollback

Re-upload the 1.3.41 rollback zip via Appearance → Themes → Upload → Replace, purge caches.
