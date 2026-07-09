# WordPress Auth Client Inventory - 2026-07-08

Scope: issue #306, stacked on PR #308 (`codex/issue-302-work-visual-cards`). This was a read-only platform/tooling refactor. No `.env` values were changed, no secrets were printed, and no live WordPress writes were run.

## Summary

`scripts/common.py` is now the shared stdlib WordPress REST client for low-risk read-only ops scripts. This pass normalized application-password spacing at the shared credential boundary and migrated the read-only queue-count/audit paths that were most likely to report false zeroes after generic HTTP 400s.

## Migrated This Pass

| File | Previous auth pattern | New path | Risk | Notes |
|---|---|---|---|---|
| `scripts/morning_truth_report.py` | Parsed `scripts/notion-to-wp/.env`, built Basic auth inline, returned `0` on any HTTP 400 queue-count response | `WPClient.from_env(env_path)` + `wp_queue_counts()` | Low | Read-only startup truth. Queue errors now render as unavailable with stderr instead of zero. |
| `scripts/check_current_state_drift.py` | Same inline Basic-auth queue counter as morning truth | `WPClient.from_env(env_path)` + `wp_queue_counts()` | Low | Keeps the morning-truth drift table aligned with the same shared read-only count source. |
| `scripts/notion-to-wp/draft_queue_audit.py` | Imported the Notion connector's requests client and skipped HTTP 400 responses while listing queue items / slug matches | `WPClient.from_env()` for read-only list/get calls | Low | Removes the Notion token dependency from draft audit collection and lets HTTP errors surface. |

## Remaining Duplicated Callsites

| File or family | Pattern | Risk | Suggested next step |
|---|---|---|---|
| `scripts/wp_post_ia_rollout.py` | Requests session with inline Basic auth | High | Write-capable `--execute` path for media alt text and excerpts; migrate only with dry-run/snapshot tests preserved. |
| `scripts/notion-to-wp/wp_client.py`, `kk_notion_to_wp.py`, one-off `publish_*.py` scripts | Package-specific requests client and direct media/post/term writes | High | Keep separate until a dedicated publisher-client design covers uploads, terms, slug guards, and update safety. |
| `scripts/notion-to-wp/publish_keep_the_machine_strange.py` | Uses `WPClient` but reaches into private `c._auth` for raw media upload | High | Add a shared media upload method or explicit auth-header helper before migrating other publish scripts. |
| `scripts/seo-backfill/*.py` | Inline Basic auth in write-capable metadata/category backfills | High | Treat as a separate SEO backfill safety pass with dry-run fixtures and rollback notes. |
| `scripts/marquee/wp_sync.py`, `scripts/marquee/sync.py` | Requests session / env credential gate for sync execution | Medium-high | Migrate after confirming execute/dry-run boundaries and existing tests. |
| `scripts/public_image_audit.py` | Requests auth session for authenticated image/media audit | Medium | Likely safe once caller expectations around `requests.Session` are separated from auth creation. |
| `scripts/jetpack_feedback_audit.py` | Inline Basic auth for authenticated feedback reads | Medium | Privacy-sensitive read-only audit; migrate with tests that avoid dumping feedback payloads. |
| `scripts/wp7-admin-readiness.py`, `scripts/wordcamp-mcp-smoke.py` | Inline Basic auth for admin/readiness probes | Medium | Good future low-risk candidates, but keep separate from this queue-count fix. |
| `scripts/mcp-wordpress-remote.sh` | Shell env export from WP credentials into MCP vars | Medium | Leave as shell-specific unless the MCP launch path is refactored. |
| `scripts/seo-audit/inventory.py` | Credential gate against `WP_USER` / `WP_APP_PASSWORD` | Low-medium | Review with the rest of the SEO audit tooling. |

## Verification Notes

- Added unit coverage for shared app-password normalization and read-only queue-count targets.
- Added regression coverage that HTTP 400 from the migrated queue counters is reported as an error rather than converted to zero.
- Added draft-audit tests confirming `WPClient.from_env()` is used and HTTP 400 is not swallowed.
- `python3 -m unittest scripts.tests.test_common` passed: 22 tests.
- `python3 -m unittest discover -s scripts/tests -v` passed: 82 tests.
- `scripts/notion-to-wp/.venv/bin/python -m unittest discover -s scripts/notion-to-wp/tests -v` passed: 44 tests.
- `make status-readonly` passed and reported draft queue truth as `0` future posts, `64` draft posts, `4` draft pages; no live writes were run.

## Follow-Up Boundary

The next safe slice is either the admin/readiness probes (`wp7-admin-readiness.py`, `wordcamp-mcp-smoke.py`) or a dedicated write-client design for publisher/media uploads. Do not fold write-capable publish/backfill scripts into `WPClient` casually; they need explicit dry-run, slug/ID, rollback, and media-upload tests.
