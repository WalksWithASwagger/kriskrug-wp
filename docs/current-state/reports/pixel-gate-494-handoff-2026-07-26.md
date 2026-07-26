# Pixel-gate handoff — #494 / PR #493 (Aurora 1.5.0)

**Date:** 2026-07-26 (updated)  
**PR:** https://github.com/WalksWithASwagger/kriskrug-wp/pull/493  
**Branch:** `theme/474-cascade-layers-scaffold`  
**Refs:** #474, #493, #494, #473

## Verdict

| Gate | Status |
|---|---|
| Merge conflicts vs `main` | **Resolved** (version → 1.5.0 on top of Aurora 1.4.8) |
| css-ratchet | **Green** — budget `front_end_lines` **7458** (waiver #494) |
| `!important` code-only | **160** unchanged; front-end gated metric **159** |
| CI (`Test PR`) | **All green** on tip `d6f46a3` |
| Visual harness | **Ready in this Cloud pod** (`PLAYWRIGHT_BROWSERS_PATH=~/.local/pw-browsers`) |
| Baseline freeze | **Done** — run id `20260726T194734Z` (live 1.4.8, 33 PNGs on disk) |
| Deploy 1.5.0 | **Blocked** — needs wp-admin Desktop login or `WP_SFTP_PASSWORD` |
| `make visual-diff` vs baseline | **Blocked on deploy** (harness compares post-deploy live vs pre-deploy live) |
| Ready for KK merge? | **No** until green visual-diff after 1.5.0 is live |

## What already landed on the branch

1. Merged onto current `main` (1.4.8); version conflicts kept **1.5.0**.
2. Inventory/coverage/visual file lists include `02-tokens.css` + `09-late.css`.
3. `.css-budget.json` rebaselined **7379 → 7458** under waiver **#494**.
4. Baseline manifest committed: `docs/current-state/reports/visual-baseline/manifest-20260726T194734Z.json`.

### Commits (tip)

- `a614f4f` — merge + conflict resolve to 1.5.0
- `cc6041c` — css-ratchet rebaseline
- `d6f46a3` — earlier handoff (harness missing; superseded by this update)

## Deploy packages (gitignored zips; handoff tracked)

Under `backup/aurora-deploy-20260726/`:

| Role | File | SHA-256 |
|---|---|---|
| Deploy | `kk-aurora-cascade-layers-1.5.0-1.5.0-20260726.zip` | `54904cc082121cb6ed914a0abd84cdbe322677ddf02a6c07f0b66d9d6183b1ce` |
| Rollback | `kk-aurora-live-1.4.8-1.4.8-20260726.zip` | `3f03487ebcab3a2daa5fcac5d0ecb8a95f64f4aafd1330de275bbcbce961b6cb` |

Details: `backup/aurora-deploy-20260726/DEPLOY-HANDOFF.md`.

## Preflight R-3 (KK / wp-admin only)

Before upload: confirm Code Snippet **#14** (`kk_aurora_force_cream_media_frame`) is **Inactive**, then delete snippet + media #12631 per #474.

## Post-deploy commands (this pod)

```bash
export NODE_PATH=$HOME/.local/pw/node_modules
export PLAYWRIGHT_BROWSERS_PATH=$HOME/.local/pw-browsers
export PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1

# confirm live header
curl -sL https://kriskrug.co/wp-content/themes/kk-aurora/style.css | head -20

make visual-diff BASE=20260726T194734Z
make visual-diff-report DIFF=<run-id>
```

Any flip: fix **only** via `theme/kk-aurora/assets/css/09-late.css` (unlayered, no new `!important`).

## Why deploy is still human-gated here

- REST Application Password ≠ wp-login session for Appearance → Themes upload.
- `scripts/deploy_theme_sftp.py` reads Pagely SFTP password from **macOS Keychain** only (no Cloud env fallback yet).
- This pod has `wordpress_test_cookie` only — not authenticated.

## Local checks

| Check | Result |
|---|---|
| Brace balance / inventory `--check` | Green |
| `python3 -m unittest scripts.tests.test_aurora_css_literal_contrast` | 12 OK |
| `make visual-preflight` | OK (Chromium via `~/.local/pw-browsers`) |
| `make css-inventory-check` | Green at 7458 |
| CI php/python/css-ratchet | Green on PR |
