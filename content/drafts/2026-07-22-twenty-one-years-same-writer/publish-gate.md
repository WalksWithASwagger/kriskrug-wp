# Publish gate

**Current status:** Private WordPress draft created as post ID `12621` on 2026-07-22 at 17:51 PDT. No publish, schedule, social post, theme change, media upload, or sharing change has been made.

## Private WordPress draft receipt

- [x] Kris said to proceed with the private draft.
- [x] Exact post and page slug lookups returned no public collision before the write.
- [x] The guarded publisher dry-run passed before execution.
- [x] Modern-corpus totals use the canonical archive counts rather than the conflicting artifact totals.
- [x] The private Claude artifact remains unlinked.
- [x] WordPress retained the scoped `<style>` block and the `kk-vf-shell` layout marker in both raw and rendered content.
- [x] The saved record reads back as `status=draft`, slug `twenty-one-years-same-writer`, one category, five tags, and no featured media.
- [x] Anonymous REST lookup returns no post, and both the numeric draft permalink and pretty slug return HTTP 404.
- [x] The public blog index still returns HTTP 200.
- [x] Proposed archive links and related-post links returned the intended public pages during packet validation.
- [ ] Run a private-draft render check on desktop and mobile. Confirm the comparison table scrolls instead of clipping.

## Required before publication

- [ ] Regenerate the comparative score table from named corpus inputs and save the machine-readable export beside this packet.
- [ ] Resolve the numeric drift documented in `source-manifest.md`; do not copy conflicting artifact totals into WordPress.
- [ ] Re-run `voicecheck.py` on the final WordPress body after any manual edits.
- [ ] Check heading order, keyboard focus, table caption, link contrast, and reduced-motion behavior.
- [ ] Confirm the featured-image rights and alt text.
- [ ] Reconfirm the final slug and exact post ID before any publish or update write.
- [ ] Snapshot post ID `12621`, dry-run the exact update, and preserve a rollback receipt before publication.
- [ ] Keep the cadence retraction and provenance correction visible. They are part of the article, not production notes.
- [ ] Confirm the statement about the Dark Crystal 97-rule sync against the deployed or cited version, not only a local checkout.

## Rollback path

The local `post.md` and `post.html` remain the source rollback copy. Before any edit to post ID `12621`, capture an authenticated REST snapshot. If the styled payload causes a rendering problem, restore the plain Markdown-derived body or keep the post private and move it to Trash only with Kris's approval. Do not change theme files as part of this Track A packet.
