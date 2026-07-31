# Publications legacy surgical update — BIV 2026-07-31

Status: **applied live** 2026-07-31T22:34:57Z (page 1895). Auth via `~/.agents/env/wordpress` (`WP_API_USERNAME` / `WP_API_PASSWORD`); rollback snapshot under `backup/20260731T223456Z-publications-biv-surgical/`.

## Why surgical (not full redesign)

Live page 1895 still uses `kk-publications-*` (modified 2026-07-23). The `kk-press` redesign in `publications.html` remains a separate approve-and-deploy track (PR #563 / publish gate). This patch only inserts the new BIV card as the first Featured trail card.

## Target

- URL: https://kriskrug.co/publications/
- Page ID: `1895`
- Anchor: insert fragment immediately after `<div class="kk-publications-grid">` and before the Tyee card

## Fragment

See `../wp-payloads/publications-legacy-biv-card-fragment.html`

## Deploy sequence (auth REST)

1. `pnpm exec varlock run --inject vars --` with `WP_USER` + `WP_APP_PASSWORD` present (or `WP_API_*` aliases from `~/.agents/env/wordpress`)
2. Snapshot `GET /wp-json/wp/v2/pages/1895?context=edit` → rollback JSON
3. Patch `content.raw` (or rendered-equivalent block markup) with the fragment
4. Dry-run diff must show **one** new card + URL `12601298`
5. `--apply` PATCH page 1895 only
6. Cache-bypass verify: `curl -sL "https://kriskrug.co/publications/?cb=$RANDOM" | rg 12601298`

## Auth note (resolved 2026-07-31)

`kriskrug-wp/.env.schema` previously looked for `WP_USER` / `WP_APP_PASSWORD` under `~/.agents/env/values/`, which were unset. Working credentials live at `~/.agents/env/wordpress/.env.local` as `WP_API_USERNAME` / `WP_API_PASSWORD` (WordPress MCP / Application Password over HTTPS). Schema now imports those keys; `scripts/common.py` maps them onto the legacy names.

## Related

- kk-kb #2942
- Screenshot assets: kk-kb PR #2957 + `assets/press-2026-07-31-biv-ecosystem-context.jpg`
- Full redesign remains optional follow-up after voice/media gate
