# Gorgeous Ghost combined package: publish gate

**Status: NOT READY.** Do not stage, schedule or publish from this package.

This package combines the #771 art-project package and the #1016 making-of draft, per Kris's 2026-11-12 ruling on #771. Staging moved to the Nov 19 to 30 window. The folder date is the day the package was built, not a post date.

- No WordPress object exists for this package. No WordPress write and no authenticated call was made while building it.
- **No hash pins yet.** Pins are added only after Kris answers the blocking questions in `open-facts-for-kk.md` and approves the final copy. Any edit to `post.md` or `post.html` after that makes the pins stale again.
- The old package `content/drafts/2026-08-12-gorgeous-ghost-art-project/` is untouched. Its #925 pins stay valid until Kris retires it (open-facts question 14). Both packages use slug `gorgeous-ghost`, so only one of them may ever be staged.

## Blocking before any pin

- [ ] Kris answers open-facts questions 1 to 7: post date, slug and canonical, release month, prompt word, tool names, credit line, and the image plan with its rights question.
- [ ] Any copy change from those answers goes into `post.md`, then `post.html` is regenerated from it and both are re-checked.
- [ ] Kris approves the final copy, and the two source hashes are pinned here in a content PR that merges.

## Preflight to rerun on the day of any write

Every item is dated evidence. A pass on another day does not count.

1. **Source hashes.** `shasum -a 256 post.md post.html` match the pins above. If not, stop.
2. **Slug collision.** Authenticated, read-only, all statuses, posts and pages: `FORMAT=json make draft-queue-audit`, then read `slug_matches["gorgeous-ghost"]` (or the slug Kris picked). Required result: 0 posts and 0 pages. Record the UTC time. Never print credentials. The offline publisher dry-run does **not** check the slug; it reports `"slug_check": "skipped_offline"`.
3. **Taxonomy IDs.** Rerun the term check in `seo-meta.md` against public REST. Every name must resolve to an existing ID (1755, 1804, 1682, 1785, 1395) by the `ensure_term()` rule. If any name matches nothing, stop, because `--execute` would create a new term.
4. **Image rights and media plan.** Kris's ruling on question 7 is recorded. A hosted image has passed featured-image-forge multi-ratio crop QC and Kris has approved it. If the package declares no local images, the publisher uploads nothing and leaves `featured_media` unset.
5. **Credits.** Re-read the Credits section on https://gorgeousghost.com/ and confirm it still matches the approved credit line.
6. **Links.** Every URL in `internal-links.md` still returns 200, and the chosen canonical still returns 404.
7. **Voice check.** `make voice-check FILES="content/drafts/2026-11-12-gorgeous-ghost-combined/post.md content/drafts/2026-11-12-gorgeous-ghost-combined/post.html"` reports 0 violations.
8. **Dry-run.** `scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/create_local_wp_draft.py content/drafts/2026-11-12-gorgeous-ghost-combined/post.md` exits 0 and shows the expected title, slug, category, four tags and image list.
9. **Repo gates.** `make verify` and `git diff --check` pass.

## Staging gate (after the preflight, never before)

- [ ] Kris approves one new unpublished WordPress post with status `draft`, built from the pinned hashes. The write set is that one post. No existing post, page, media item or term changes.
- [ ] Run the publisher with `--execute` through Varlock. Record the post ID and the readback `status` and `slug` here.
- [ ] Compare the admin preview with `post.html`: body, single H1 from the title field, the YouTube embed, credits, date, category, tags, canonical, OG metadata, image and every link.

## Rollback

This is a new object, so there is no earlier version to restore. Before the write, the rollback proof is the empty same-day slug check. After it, the default is to leave the post as an unpublished draft and report its ID and the problem. Moving it to trash needs Kris's explicit approval for that post ID, with a readback of ID and status before and after. Never `force=true`.

## Checks run while building this package (2026-11-12)

- `make voice-check` on `post.md` and `post.html`: 2 files scanned, 0 violations, 0 baseline-waived.
- Offline publisher dry-run: exit 0, `slug: gorgeous-ghost`, `slug_check: skipped_offline`, `images: []`, category `Creative Technology & Making`, tags `Gorgeous Ghost`, `Creative AI`, `AI Film Club`, `AI Music`.
- `LOCAL_ONLY=1 FORMAT=json make draft-queue-audit`: exit 0; this package reads 1,353 words, 18 links, 75 blocks, 0 TODO markers, all six expected files.
- Public term check: all five names resolve (see `seo-meta.md`).
- No authenticated slug check was run. That waits for the day of any write.

Until every box above is ticked, this package stays a local `status: draft` and nothing may claim it is published.
