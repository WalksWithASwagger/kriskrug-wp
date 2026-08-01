# Publications editorial publish gate

Status: **Aurora paper tear-sheet ready in repo** — not approved for public deployment.
July 2026 dark neon `kk-press` / live `.kk-publications` skins are **superseded**.

## Exact target

- Public URL: `https://kriskrug.co/publications/`
- WordPress page ID: `1895`
- Slug: `publications`
- Status: `publish`
- Review branch: `cursor/publications-aurora-tearsheet`
- Payload: `../wp-payloads/publications.html` (Aurora paper tear-sheet)
- Research: `PUBLICATIONS-KB-GAP-REPORT-2026-08-01.md`

## Current live evidence

A cache-bypassed fetch on 2026-08-01 still returned the legacy Publications layout.
The live HTML contains `kk-publications` and neon tokens `#00e5ff` / `#ff6a6a`.
It does **not** contain the paper tear-sheet markers (`kk-press-display` on cream
paper / Aurora tokens). Content images on the live page are effectively absent.

The hash is drift evidence, not a rollback source. An authenticated
`context=edit` snapshot is still required immediately before any write.

## Skin retirement (must be true after deploy)

Public HTML must contain **zero** of:

- `kk-publications`
- `#00e5ff`
- `#ff6a6a`
- `--press-night`

Regression lock: `scripts/tests/test_publications_editorial_payload.py`.

## Proposed media set (7 files — still needs KK approval)

1. `press-2026-07-31-biv-ecosystem-context.jpg` (lead)
2. `press-2026-07-24-the-tyee-context.jpg`
3. `press-2026-06-15-biv-context.jpg`
4. `press-2026-05-20-storyhive.jpg`
5. `press-2026-02-09-tela-viva-context.jpg`
6. `press-2025-07-09-e-channelnews-context.jpg`
7. `press-2025-05-01-portfolio-yvr-context.jpg`

See `../assets/publications-press-media.md` for provenance, exclusions, credits,
and the upload + path-rewrite checklist. Local files are present; **do not
upload or PATCH without KK go-ahead**.

## Voice gate

- Voice source: `/Users/kk/Code/kk-voice/crystal.md` (or sibling `dark-crystal/kk-voice`)
- Dominant facet: The Host
- Secondary facet: The Anti-Hero, used lightly
- Mechanical audit packet: `../wp-payloads/voice-audit/publications-paper-20260801/`
- Prior July packet (dark skin): `../wp-payloads/voice-audit/publications-editorial-20260724/` — historical
- Human voice review: pending Kris

## Required approval

The exact approval needed for the next production step is:

> Approve the seven-file Publications media set and publish the Aurora paper
> tear-sheet payload to WordPress page 1895 (after snapshot + dry-run review).

Layout approval alone does not authorize media upload or public publication.

## Deployment sequence after approval

Use the tear-sheet deploy helper (dry-run first):

```bash
# 1) Snapshot + dry-run diff only (no write)
varlock run --path .env.schema --inject vars -- \
  python3 scripts/deploy_publications_tearsheet.py --dry-run

# 2) After KK reviews the printed diff and approves media + apply:
varlock run --path .env.schema --inject vars -- \
  python3 scripts/deploy_publications_tearsheet.py --upload-media --apply
```

Manual sequence if the helper is unavailable:

1. Authenticated `context=edit` snapshot of page `1895` → `backup/<stamp>-publications-tearsheet/`.
2. Upload only the seven approved media files; set alt/captions/credits.
3. Rewrite every `../assets/` image `src` to the WP Media Library CDN URL.
4. Assert no residual relative paths or third-party hotlinks remain.
5. Dry-run PATCH content (+ SEO meta from `page-meta.json` if still required).
6. `--apply` only after KK go-ahead.
7. Cache-bypass verify: no `kk-publications` / neon tokens; 7 images load; 48 dated
   entries; EPK + Media Appearances links; desktop + ~390px mobile; no overflow.
8. Record rollback JSON + restore command; purge cache if tooling available.

## Rollback

Restore page `1895` from the authenticated pre-write `content.raw` and SEO
metadata snapshot. Do not delete uploaded media during emergency rollback. Media
cleanup is a separate destructive action and requires a later approval.

## Not yet run (blocked on KK approval)

- Authenticated pre-write snapshot
- WordPress Media Library uploads
- Final media URL substitution
- Production write
- Cache purge
- Cache-bypassed production visual verification
