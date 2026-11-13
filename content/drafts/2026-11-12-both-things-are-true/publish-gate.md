# Both Things Are True: publish gate

**Status: NOT READY.** Do not stage, schedule or publish from this package.

This package stages #959, step 1 of the Q1 2027 keynote pipeline (#1277): the Both Hands Full keynote in writing, for 2027 bookers. The folder date is the day the package was built, not a post date.

- No WordPress object exists for this package. No WordPress call of any kind was made while building it, and no `.env` file was read.
- **No hash pins yet.** Pins are added only after Kris answers the blocking questions in `open-facts-for-kk.md` and approves the final copy. Any edit to `post.md` or `post.html` after that makes the pins stale again.
- WordPress draft 11881 covers older, thinner ground (open-facts question 6). Nothing here touches it.

## Blocking before any pin

- [ ] Kris answers open-facts questions 1 to 6: the LaSalle line by ear, the photo count, São Paulo, date and slug, the image and its rights, and draft 11881.
- [ ] Any copy change from those answers goes into `post.md`, then `post.html` is regenerated from it and both are re-checked.
- [ ] Kris approves the final copy, and the two source hashes are pinned here in a content PR that merges.

## Preflight to rerun on the day of any write

Every item is dated evidence. A pass on another day does not count.

1. **Source hashes.** `shasum -a 256 post.md post.html` match the pins above. If not, stop.
2. **Quote.** The pull quote in `post.md` and `post.html` matches the wording Kris confirmed in question 1, character for character.
3. **Slug collision.** Authenticated, read-only, all statuses, posts and pages: `FORMAT=json make draft-queue-audit`, then read `slug_matches["both-things-are-true"]` (or the slug Kris picked). Required result: 0 posts and 0 pages. Record the UTC time. Never print credentials. The offline publisher dry-run does **not** check the slug; it reports `"slug_check": "skipped_offline"`.
4. **Taxonomy.** Read-only REST lookups for the category and the four tags in `seo-meta.md`. Every name must resolve to an existing term by the `ensure_term()` rule. `AI for Creatives` can only resolve by name, because its live slug is `ai-creatives`. If any name matches nothing, stop, because `--execute` would create a new term.
5. **Image.** Kris's ruling on question 5 is recorded, with rights and credit. A chosen frame has passed featured-image-forge multi-ratio crop QC and Kris has approved it. If the image is an existing media item (the recommended option), the publisher will not attach it: setting `featured_media` is a second write that needs its own approval and readback. If the package declares no local images, the publisher uploads nothing and leaves `featured_media` unset.
6. **Links.** Every URL in `internal-links.md` still returns 200, and the chosen canonical still returns 404.
7. **Voice check.** `make voice-check FILES="content/drafts/2026-11-12-both-things-are-true/post.md content/drafts/2026-11-12-both-things-are-true/post.html"` reports 0 violations.
8. **Dry-run.** `scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/create_local_wp_draft.py content/drafts/2026-11-12-both-things-are-true/post.md` exits 0 and shows the expected title, slug, category, four tags and an empty image list.
9. **Repo gates.** `make verify` and `git diff --check` pass.

## Staging gate (after the preflight, never before)

- [ ] Kris approves one new unpublished WordPress post with status `draft`, built from the pinned hashes. The write set is that one post. No existing post, page, media item or term changes.
- [ ] Run the publisher with `--execute` through Varlock. Record the post ID and the readback `status` and `slug` here.
- [ ] Compare the admin preview with `post.html`: body, single H1 from the title field, the YouTube embed and its caption link, both pull quotes, category, tags, canonical, OG metadata, image and every link.

## Rollback

This is a new object, so there is no earlier version to restore. Before the write, the rollback proof is the empty same-day slug check. After it, the default is to leave the post as an unpublished draft and report its ID and the problem. Moving it to trash needs Kris's explicit approval for that post ID, with a readback of ID and status before and after. Never `force=true`.

## Checks run while building this package (2026-11-12 Pacific, 2026-11-13 UTC)

- `make voice-check` on `post.md` and `post.html`: 2 files scanned, 0 violations, 0 baseline-waived.
- Offline publisher dry-run: exit 0, `slug: both-things-are-true`, `slug_check: skipped_offline`, `images: []`, category `AI for Creatives`, tags `Both Hands Full`, `Keynotes`, `speaking`, `taste`. Neither legacy env file the publisher can fall back to exists on this machine, so the dry-run read no `.env`.
- `LOCAL_ONLY=1 FORMAT=json make draft-queue-audit`: exit 0. 104 local packages. This one reads 1,177 words, 21 markdown links, 21 html links, 60 blocks, 0 images, 0 TODO markers.
- No em dashes, en dashes or curly quotes in any file of this package, and every file encodes to cp1252.
- `make verify`: the Python suites (274, 993, 12 and 68 passed), JavaScript syntax, plugin and theme smokes, docs truth check and `php -l` on 58 files all passed. It then stopped at PHPCS because this worktree has no `vendor/` (`phpcs not found`). That gate does not read content drafts; CI runs the required check.
- No authenticated slug check and no REST term check were run. Both wait for the day of any write.

Until every box above is ticked, this package stays a local `status: draft` and nothing may claim it is published.
