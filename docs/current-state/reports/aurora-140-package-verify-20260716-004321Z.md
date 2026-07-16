# Aurora 1.3.40 package verify — pre-upload (#362)

**Captured:** `2026-07-16T00:43:21Z`  
**Issue:** #362 (supports #351)  
**Live theme (public `style.css`):** `1.3.37`  
**Repo theme:** `1.3.40`

## Acceptance checklist (agent-safe portion)

| Item | Result |
|---|---|
| Read `backup/aurora-deploy-20260716/DEPLOY-HANDOFF.md` | yes |
| Deploy SHA-256 `8e1c1321f94b1caf5d899697f5ddef6256d1274c74a67cd64d84645b1c24fad5` | **match** on `kk-aurora-seo-search-titles-1.3.40-1.3.40-20260716.zip` |
| Rollback SHA-256 `cfa1307e68db77c9bd8b9423fbd35be984a1d98b6d4f6829b3a540b701a1d1b4` | **match** on `kk-aurora-live-1.3.37-1.3.37-20260716.zip` |
| Live still `1.3.37` until upload | **yes** |
| Pre-deploy baseline retained | `aurora-140-predeploy-public-baseline-20260716.md` |
| KK upload approval | **not recorded** — stop |
| Live `1.3.40` + post-deploy smoke report | **blocked** on KK upload |

## Rebuild note

A second `make aurora-package` in a dirty workspace can rewrite zip *filenames* / `package-report.json` prose; treat the handoff table SHA values as the source of truth. Re-hash before KK upload:

```bash
sha256sum backup/aurora-deploy-20260716/kk-aurora-seo-search-titles-1.3.40-1.3.40-20260716.zip
sha256sum backup/aurora-deploy-20260716/kk-aurora-live-1.3.37-1.3.37-20260716.zip
```

Do **not** upload any 2026-07-13 **1.3.39** zip.

## Public SEO sample (still pre-deploy gaps)

| Path | og:title present | canonical present |
|---|---|---|
| `/` | no | yes |
| `/blog/` | yes | no |
| `/blog/page/2/` | yes | no |
| `/about/` | yes | yes |

Full matrix: `aurora-140-predeploy-public-baseline-20260716.md`.

## Post-upload smoke (do after KK confirms upload)

1. Public `style.css` → Version `1.3.40`
2. Smoke `/`, `/blog/`, `/blog/page/2/`, `/about/`, `/speaking/`, one article (+ crawler UAs where practical)
3. Home `og:title` present; Blog page-1/page-2 canonical + `og:url` agree
4. Search-title sample from `docs/current-state/AURORA-SEO-TITLES-1.3.40-HANDOFF-2026-07-14.md`
5. Commit a dated post-deploy report under `docs/current-state/reports/`
6. Update #351 with evidence; close companions only when evidence supports
