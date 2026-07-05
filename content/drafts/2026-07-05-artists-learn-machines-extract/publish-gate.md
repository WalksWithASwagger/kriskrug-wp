# Publish Gate

Status:
Local package staged. WordPress draft creation blocked pending credentialed REST dry-run and execute.

Hard boundary:
Create a private WordPress draft only. Do not publish, schedule, syndicate, email, or post to LinkedIn without Kris approving the exact final text.

WordPress draft:
- Post ID: TBD
- Edit URL: TBD
- Status: not created
- Slug: artists-learn-machines-extract
- Featured media: images/artists-learn-machines-extract-card.png

Prewrite evidence:
- Snapshot: backup/20260705T201901Z-artists-learn-machines-extract/
- Public slug check: no published post currently returned for `artists-learn-machines-extract`
- Public blog smoke: https://kriskrug.co/blog/ returned HTTP 200 before the write attempt
- Credential gate: `scripts/notion-to-wp/.env` is missing locally, and WordPress credentials were not available in the current shell environment
- Dry-run result: `ERROR: WP credentials not found in /Users/kk/Code/kriskrug-wp/scripts/notion-to-wp/.env or environment`

Completed local checks:
- Dark Crystal voicecheck: clean, 0 flags
- Draft package quality check: clean, 0 issues
- Guarded review gate: `prepare_review_draft.py --no-write --fail-on-warning` returns `WARN: no markdown image and no featured_media_id`
- WordPress unit tests: 42 passed with `scripts/notion-to-wp/.venv/bin/python -m unittest discover scripts/notion-to-wp/tests`

Required before publish:
- Dark Crystal voicecheck clean on `post.md`
- Upload the intended local featured image or assign a real WordPress `featured_media_id`, then rerun the guarded review gate
- WordPress draft readback confirms `status=draft`
- Readback confirms expected slug and title
- Readback confirms featured media is attached
- Readback body contains no local filesystem paths
- https://kriskrug.co/blog/ returns HTTP 200 after draft creation
- Kris approves exact copy, title, image, and caption
