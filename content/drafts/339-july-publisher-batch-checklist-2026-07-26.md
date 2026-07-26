# #339 July publisher batch — operator checklist

**Status:** PREP ONLY — no live run without KK ticks + dry-run proof.  
**Full report:** [`docs/current-state/reports/publisher-batch-prep-339-20260726.md`](../../docs/current-state/reports/publisher-batch-prep-339-20260726.md)  
**Captured:** 2026-07-26

## Before anything live

- [ ] KK edits #339: drop obsolete 1.3.39/1.3.40 zip approval; acknowledge live Aurora **1.4.8**
- [ ] KK ticks all content lines (titles, descriptions, #249 sentence, #328/#336 wraps, #342 href, #335 footers)
- [ ] KK explicitly ticks **overwrite** for post **8802** (live title/desc already differ)
- [ ] KK acknowledges refreshed `modified` for page **1208** and post **12327** after raw reconfirm
- [ ] Secrets present (`WP_USER` / `WP_APP_PASSWORD`); July-14 401 gate cleared via `FORMAT=json make seo-audit`
- [ ] Dry-run outputs reviewed; snapshot dir created: `backup/<UTC>-july-publisher/`

## Credential-free preflight (done / re-run anytime)

```bash
make status-readonly
make seo-publisher-smoke
make verify
```

## Authenticated dry-run (after secrets)

```bash
FORMAT=json make seo-audit
scripts/notion-to-wp/.venv/bin/python scripts/seo-backfill/backfill_meta.py \
  --ids 35,8802 --kind post --fields seo_title,meta_desc
# Then KK-approved --from-file overwrite JSON for 8802 (and 35 if preferred), still without --execute
```

## Apply order (only after ticks + snapshot)

1. SEO meta: post **35**, then **8802**
2. Body: **#249** (page 1208) → **#328** (2950, 2665) → **#335** footers (35, 58) → **#336** (9774, 12327) → **#342** (11171)
3. Each step: identity guard → write minimal payload → authenticated + public readback
4. Schedule measurement; no GSC indexing burn in-session

## Slug / payload hard rules (INCIDENT-2026-05-15)

- Match **ID + slug + status + modified** before every PATCH
- Body: `{"content": ...}` only; meta: allowlisted Jetpack keys only
- No Notion connector `--update` for these surgical patches
- Retain snapshots as rollback; do not rely on Pagely revisions

## Out of scope

#331 · #353 · #340 bc-ai.net · schema/DNS/GA4 · live run in this prep PR
