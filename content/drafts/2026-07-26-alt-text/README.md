# Alt-text remediation drafts — 2026-07-26 (#4)

Agent-safe packet only. **Do not apply** without KK approval + `WP_USER` / `WP_APP_PASSWORD`.

## Files

| File | Purpose |
|---|---|
| `proposed-alts.md` | Human-readable worst-offender proposals |
| `media-alt-patch.json` | Exact payload for `scripts/public_image_audit.py --execute --media-alt-file …` |

## Apply (later)

```bash
# 1) Snapshot (manual or scripted GET of media IDs)
# 2) KK edits proposed strings if needed
# 3) Execute:
python3 scripts/public_image_audit.py --execute \
  --media-alt-file content/drafts/2026-07-26-alt-text/media-alt-patch.json
# 4) Verify:
make public-image-audit URLS="/home/,/flickr-photographr-badge/" CHECK_URLS=1 \
  OUTPUT=docs/current-state/reports/alt-text-verify-YYYYMMDD.md
```

Full inventory: `docs/current-state/reports/alt-text-inventory-20260726.md`.
