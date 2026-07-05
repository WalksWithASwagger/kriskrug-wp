# Prewrite Evidence Snapshot

Draft:
Artists Learn. Machines Extract.

Slug:
artists-learn-machines-extract

Timestamp:
20260705T201901Z

Intent:
Create a guarded WordPress draft only. No publish, schedule, newsletter, or social repost.

Local package:
content/drafts/2026-07-05-artists-learn-machines-extract/

Media intended for upload:
content/drafts/2026-07-05-artists-learn-machines-extract/images/artists-learn-machines-extract-card.png

Media intentionally not uploaded:
Raw LinkedIn screenshot from the Dark Crystal source packet. Keep it as local evidence only unless Kris explicitly asks for upload.

Public slug check before write:
`GET https://kriskrug.co/wp-json/wp/v2/posts?slug=artists-learn-machines-extract&status=publish&_fields=id,slug,status,link,title` returned `[]`.

Draft queue signal:
`make status-readonly` could not inspect authenticated draft counts because `scripts/notion-to-wp/.env` is missing locally.

Public smoke before write:
`https://kriskrug.co/blog/` returned HTTP 200.

Credential state:
WordPress credentials were not available from the expected local env file or shell environment at snapshot time.

Dry-run result:
`scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/create_local_wp_draft.py content/drafts/2026-07-05-artists-learn-machines-extract/post.md` stopped before any write with `ERROR: WP credentials not found in /Users/kk/Code/kriskrug-wp/scripts/notion-to-wp/.env or environment`.

Local verification:
- Dark Crystal voicecheck passed with 0 flags.
- Draft package quality check returned 0 issues.
- Guarded review gate later returned `WARN: no markdown image and no featured_media_id`; the local featured image still needs a credentialed WordPress media upload or real `featured_media_id` before publish.
- WordPress unit tests passed: 42 tests.
