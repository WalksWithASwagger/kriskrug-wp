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

WordPress draft result:
The draft was created through the logged-in WordPress editor session after the REST script credential gate blocked. WordPress saved post ID `12473` at `https://kriskrug.co/wp-admin/post.php?post=12473&action=edit`.

Local verification:
- Dark Crystal voicecheck passed with 0 flags.
- Draft package quality check returned 0 issues.
- Browser editor readback at 2026-07-05T20:41:04Z showed title, draft status, slug, AI Ethics & Philosophy category, 7 tags, excerpt, featured-image preview, opening body, final line, and receipts.
- Body safety readback found no `/Users/`, `content/drafts/`, or local image path leakage in the editor body.
- Published slug lookup still returned `[]`, and `https://kriskrug.co/blog/` returned HTTP 200 after draft creation.
- Pre-publish follow-up: WordPress currently reports no alternative text on the uploaded featured-image media item.
- WordPress unit tests passed: 42 tests.
