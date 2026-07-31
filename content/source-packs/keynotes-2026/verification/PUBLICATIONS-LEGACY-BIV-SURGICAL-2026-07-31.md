# Publications legacy surgical update — BIV 2026-07-31

Status: **ready to apply** once `WP_USER` + `WP_APP_PASSWORD` resolve via Varlock.

## Why surgical (not full redesign)

Live page 1895 still uses `kk-publications-*` (modified 2026-07-23). The `kk-press` redesign in `publications.html` remains a separate approve-and-deploy track (PR #563 / publish gate). This patch only inserts the new BIV card as the first Featured trail card.

## Target

- URL: https://kriskrug.co/publications/
- Page ID: `1895`
- Anchor: insert fragment immediately after `<div class="kk-publications-grid">` and before the Tyee card

## Fragment

See `../wp-payloads/publications-legacy-biv-card-fragment.html`

## Deploy sequence (auth REST)

1. `pnpm exec varlock run --inject vars --` with `WP_USER` + `WP_APP_PASSWORD` present
2. Snapshot `GET /wp-json/wp/v2/pages/1895?context=edit` → rollback JSON
3. Patch `content.raw` (or rendered-equivalent block markup) with the fragment
4. Dry-run diff must show **one** new card + URL `12601298`
5. `--apply` PATCH page 1895 only
6. Cache-bypass verify: `curl -sL "https://kriskrug.co/publications/?cb=$RANDOM" | rg 12601298`

## Blocker (2026-07-31)

Varlock inject currently reports `WP_USER` / `WP_APP_PASSWORD` unset in this environment. No live write attempted.

## Related

- kk-kb #2942
- Screenshot assets: kk-kb PR #2957 + `assets/press-2026-07-31-biv-ecosystem-context.jpg`
- Full redesign remains optional follow-up after voice/media gate
