# Publish gate

**Current status:** Local Track A draft only. No WordPress draft, upload, publish, schedule, social post, or sharing change has been made.

## Required before a private WordPress draft

- [ ] Kris approves the title, thesis, and the two profanity quotations from his working-session corpus.
- [ ] Regenerate the comparative score table from named corpus inputs and save the machine-readable export beside this packet.
- [ ] Reconcile or remove every modern-corpus word total. Do not copy the conflicting artifact totals into WordPress.
- [ ] Decide whether the private Claude artifact should remain private. The article does not require a public artifact link.
- [ ] Decide whether the embedded `<style>` block in `post.html` is acceptable for the private draft. If WordPress strips it, move the identical scoped rules to an approval-gated Custom CSS or Code Snippets path.
- [ ] Run a private-draft render check on desktop and mobile. Confirm the comparison table scrolls instead of clipping.
- [ ] Verify the two proposed archive links and any related-post links return the intended public pages.

## Required before publication

- [ ] Re-run `voicecheck.py` on the final WordPress body after any manual edits.
- [ ] Check heading order, keyboard focus, table caption, link contrast, and reduced-motion behavior.
- [ ] Confirm the featured-image rights and alt text.
- [ ] Confirm the final slug does not collide with an existing WordPress post before any write.
- [ ] Create a pre-write snapshot and use the normal dry-run, slug-match, then publish sequence.
- [ ] Keep the cadence retraction and provenance correction visible. They are part of the article, not production notes.
- [ ] Confirm the statement about the Dark Crystal 97-rule sync against the deployed or cited version, not only a local checkout.

## Rollback path

For a private draft, retain the pre-edit REST snapshot and local `post.md`/`post.html`. If the styled payload causes a rendering problem, restore the plain Markdown-derived body or delete the private draft after recording its ID and slug. Do not change theme files as part of this Track A packet.
