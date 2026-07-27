# Aurora 1.5.0 cascade-layers deploy handoff — 2026-07-26

**PR:** #493 (`theme/474-cascade-layers-scaffold`) — implements #474 / rebuild plan step 2  
**Why now:** rebase onto `main` (live 1.4.8), CSS budget waiver for +18 layer wrappers, frozen visual baseline captured against live 1.4.8.

## Packages (gitignored under this directory)

| Role | File | SHA-256 |
|---|---|---|
| Deploy | `kk-aurora-cascade-layers-1.5.0-1.5.0-20260726.zip` | `54904cc082121cb6ed914a0abd84cdbe322677ddf02a6c07f0b66d9d6183b1ce` |
| Rollback | `kk-aurora-live-1.4.8-1.4.8-20260726.zip` | `3f03487ebcab3a2daa5fcac5d0ecb8a95f64f4aafd1330de275bbcbce961b6cb` |

Source tip packaged: see `theme-package-report-*.json` in this directory (run_id `20260726T1955*`).

## Preflight (R-3 / #474 AC)

Before uploading 1.5.0:

1. In wp-admin → Code Snippets, confirm snippet **#14** (`kk_aurora_force_cream_media_frame`) is **Inactive**.
2. Confirm no other cream-frame / `!important` media-frame snippets are active.
3. Keep rollback zip ready.

## Deploy steps (Pagely wp-admin)

1. Appearance → Themes → Add New → Upload Theme → select **deploy** zip above.
2. Activate `kk-aurora` 1.5.0.
3. Purge Pagely / CDN cache.
4. Hard-refresh homepage + one post + `/newsletter/` + `/work/` + `/speaking/`.

## Post-deploy gates (this Cloud agent can run after live shows 1.5.0)

```bash
# theme header must read 1.5.0
curl -sL https://kriskrug.co/wp-content/themes/kk-aurora/style.css | head -20

export NODE_PATH=$HOME/.local/pw/node_modules
export PLAYWRIGHT_BROWSERS_PATH=$HOME/.local/pw-browsers
export PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1
make visual-diff BASE=20260726T194734Z
make visual-diff-report DIFF=<run-id-from-diff>
```

Merge #493 only when:

- `css-ratchet` CI green (budget waived to 7397 for #474)
- `make visual-diff` vs baseline `20260726T194734Z` is green (or intentional diffs documented + KK ack)
- live theme header = 1.5.0

## Rollback

Upload + activate the **rollback** zip (1.4.8), purge cache, re-check homepage.

## Why Cloud agent cannot finish upload alone

- Pagely theme upload needs authenticated wp-admin (Cloud Desktop login), or SFTP via `scripts/deploy_theme_sftp.py` (macOS Keychain / `WP_SFTP_PASSWORD` — not present in this pod).
- REST Application Password ≠ wp-login session for Appearance → Themes upload.
