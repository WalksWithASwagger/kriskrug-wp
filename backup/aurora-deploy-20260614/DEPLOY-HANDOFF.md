# Aurora 1.3.18 deploy package — 2026-06-14

Staged for KK's manual wp-admin upload (no SFTP/SSH on Pagely). Covers issues #204 (deploy 1.3.18) and #189 (verify GSAP CDN gone). Prod was **1.3.12** as of 2026-06-09 morning-truth.

## Artifacts

| File | Version | SHA-256 |
|---|---|---|
| `kk-aurora-1.3.18.zip` | 1.3.18 (deploy) | `101713f918a6347e6744a0828265dec952326eca984d30058855251488045613` |
| `kk-aurora-1.3.12-gitrebuild.zip` | 1.3.12 (rollback, see caveat) | `3864e6eb53c9be6fdb3eeed0add51dfcafd10ea809b3986084be08f171ff1e9d` |

Both zips have `kk-aurora/` at the archive root (correct for wp-admin theme upload). Verified version strings inside each.

## Pre-flight (already done by agent)
- `make test` → 25 tests pass; `make validate` → 0 phpcs violations.
- Version is consistent at 1.3.18 across `style.css` + `functions.php`.
- Changelog backfilled for 1.3.16 (synthetic.ai restraint/grain/self-hosted fonts, PR #185), 1.3.17 (QA cleanup), 1.3.18 (stagger-reveal visibility fix).

## ⚠️ Rollback caveat — KK decision before deploy
The true production 1.3.12 zip was never retained. `kk-aurora-1.3.12-gitrebuild.zip` is **reconstructed from git commit `0cab1a9`** — it matches the repo's 1.3.12, but **NOT verified against the live site** (live may carry Customizer "Additional CSS", hotfixes, or drift not in git). Pick one before deploying:
- **(A) Accept the git-rebuilt 1.3.12** as the rollback artifact (fast; small residual risk if live drifted).
- **(B) Export the current live theme first** via Pagely admin/file manager for a true byte-accurate rollback, then deploy.

Recommendation: (B) if a Pagely export path is reachable in a few minutes; otherwise (A) is an acceptable safety net for a theme-only change.

## Deploy steps (KK, in wp-admin)
1. Appearance → Themes → Add New → Upload → choose `kk-aurora-1.3.18.zip` → **"Replace current with uploaded"** (this is the step missed in prior attempts).
2. Confirm active theme version shows **1.3.18**.
3. Remove any Customizer → Additional CSS force-visible safety net if present (it masks reveal bugs — see [[homepage-reveal-safety-net]]).
4. Purge Pagely cache (see [[pagely-page-cache-purge]]).

## Post-deploy verification (agent will run on your signal — closes #189)
- `curl -sL https://kriskrug.co/ | grep -i "gsap\|scrolltrigger"` → expect **no matches**.
- `curl -sL https://kriskrug.co/ | grep -i "Version: 1.3.18\|kk-aurora"` and confirm asset version bump.
- Logged-out spot-check: homepage, `/blog/`, one real post — render correct, reveals fire, no blank sections.
- `make status-readonly` to capture the GSAP check; cross-post evidence to #189 / #204 / #125 / #127.

## Rollback (if needed)
Re-upload the chosen 1.3.12 zip via the same wp-admin flow → purge Pagely cache → re-verify logged out.
