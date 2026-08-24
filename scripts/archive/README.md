# Archived one-off publisher scripts

These scripts ran once against a specific post or page. The matching live URLs
are recorded in the #742 PR. **Do not re-run them against production.**

Convention: spent per-article publishers live here (`scripts/archive/`), not
under `scripts/notion-to-wp/` or mixed in with reusable `scripts/` tooling.

Shared publisher code stays in `scripts/notion-to-wp/`: `publish_common.py`,
`wp_blocks.py`, `wp_client.py`, `create_local_wp_draft.py`,
`prepare_review_draft.py`, and the other tested generic entry points.

## Root fossils (deleted 2026-08-22)

`customize-for-kriskrug.sh` (spent bc-ai → kk tree rewrite) and
`monitor-agents.sh` (decommissioned auto-implement swarm poller) were deleted
from the repo root after KK approved. Recover from git history if needed:
`21e9463`.

## Left in place on purpose

- `scripts/notion-to-wp/publish_context_creators.py` — public readback is 404;
  repo evidence is WP draft 12404 with an open fact-check, not a live post.
- `scripts/notion-to-wp/sync_futureproof_polish_v2.py` and
  `verify_futureproof_polish_v2.py` — imported by
  `scripts/notion-to-wp/tests/test_sync_futureproof_polish_v2.py`.
- `scripts/stage_both_hands_power_cord.py`,
  `scripts/update_both_hands_power_cord.py`, and
  `scripts/update_publications_media_link.py` — imported by
  `scripts/tests/test_*.py` siblings. Moving them would break those imports.
