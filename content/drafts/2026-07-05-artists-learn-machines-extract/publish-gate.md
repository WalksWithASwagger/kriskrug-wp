# Publish Gate

Status:
Local package staged. WordPress draft created, enriched, saved, and verified through the logged-in WordPress editor session.

Hard boundary:
Create a private WordPress draft only. Do not publish, schedule, syndicate, email, or post to LinkedIn without Kris approving the exact final text.

WordPress draft:
- Post ID: 12473
- Edit URL: https://kriskrug.co/wp-admin/post.php?post=12473&action=edit
- Status: draft
- Slug: artists-learn-machines-extract
- Featured media: uploaded from images/artists-learn-machines-extract-card.png
- Featured media URL: https://i0.wp.com/kriskrug.co/wp-content/uploads/2026/07/artists-learn-machines-extract-card.png?fit=1024%2C538&ssl=1

Prewrite evidence:
- Snapshot: backup/20260705T201901Z-artists-learn-machines-extract/
- Public slug check: no published post currently returned for `artists-learn-machines-extract`
- Public blog smoke: https://kriskrug.co/blog/ returned HTTP 200 before the write attempt
- Credential gate: `scripts/notion-to-wp/.env` is missing locally, and WordPress credentials were not available in the current shell environment
- REST script dry-run result: `ERROR: WP credentials not found in /Users/kk/Code/kriskrug-wp/scripts/notion-to-wp/.env or environment`
- Browser editor creation result: draft saved in WordPress as post `12473`
- Rich-content rollback snapshot: `/tmp/wp-12473-body-before-rich-content-20260706-102126.html`

Completed local checks:
- Dark Crystal voicecheck: clean, 0 flags
- Draft package quality check: clean, 0 issues
- WordPress unit tests: 42 passed with `scripts/notion-to-wp/.venv/bin/python -m unittest discover scripts/notion-to-wp/tests`
- Browser editor readback at 2026-07-05T20:41:04Z: post ID `12473`, post type `post`, draft status, title, slug, AI Ethics & Philosophy category, 7 tags, excerpt, featured-image preview, opening body, final line, and receipts were visible in the editor
- Body safety readback: no `/Users/`, `content/drafts/`, or `images/artists-learn-machines-extract-card.png` path leaked into the editor body
- Public post-write checks: published slug lookup still returned `[]`; https://kriskrug.co/blog/ returned HTTP 200
- Rich-content local body check at 2026-07-06T10:23:06-07:00: `post.md` and `post.html` include the Morgane Oger inline link, inline image block, YouTube embed, internal links, expanded receipt links, and no local path leakage
- WordPress draft rich-content readback at 2026-07-06T10:23:06-07:00: copied saved blocks from the editor to `/tmp/wp-12473-body-after-rich-content-20260706-102306.html`; checks passed for Morgane link, image block, YouTube embed, internal links, expanded receipts, and no local path leakage
- WordPress editor status after rich-content pass: `Draft saved.`; no publish/schedule/syndication action taken

Required before publish:
- Add WordPress media alt text for the uploaded featured image; the editor currently reports no alternative text on the media item
- Kris approves exact copy, title, image, and caption
