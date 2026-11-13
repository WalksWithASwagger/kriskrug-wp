# The First 300: publish gate

**Status: NOT READY.** Do not stage, schedule or publish from this package.

This package stages #967, third in the editorial order of `docs/current-state/ROADMAP-2026-11-12.md`: the BC + AI year-one post, timed to the AGM, using only figures already public. The folder date is the day the package was built, not a post date.

- No WordPress object exists for this package. No WordPress call of any kind was made while building it, and no `.env` file was read.
- **No hash pins yet.** Pins are added only after Kris answers the blocking questions in `open-facts-for-kk.md`, every placeholder is filled, and he approves the final copy. Any edit to `post.md` or `post.html` after that makes the pins stale again.
- `post.md` and `post.html` still carry four bold `[KK: ...]` placeholders. A draft staged with any of them would show the bracket text to readers of the preview, so none may survive into a WordPress object.

## Blocking before any pin

- [ ] Kris answers open-facts questions 1 to 7: launch-night signups, the renewal story, the founding price rule, the price lines and the founding individual price, "300 to 600", the AGM details and date, and the image and its rights.
- [ ] Every `[KK: ...]` placeholder is replaced with Kris's words or removed, in `post.md` first. `post.html` is then regenerated from it with the shared `wp_blocks` helpers and both are re-checked.
- [ ] Kris approves the final copy, and the two source hashes are pinned here in a content PR that merges.

## Preflight to rerun on the day of any write

Every item is dated evidence. A pass on another day does not count.

1. **Source hashes.** `shasum -a 256 post.md post.html` match the pins above. If not, stop.
2. **Placeholders.** `grep -n "\[KK:" post.md post.html` prints nothing.
3. **Figures.** Every number in the copy matches Kris's answers to questions 1 to 5, and the public pages still say the same thing that day: bc-ai.ca/about (300+ members, 3 regions, 4 programs, 94+ events, 3,000+ attendance), bc-ai.ca/membership ($340 individual, $115 student, $850 five-person pack, 25% off events) and bc-ai.ca/faq (self-serve cancel, no retention scripts). If a public figure moved, stop and update the copy first.
4. **Dates.** The AGM line matches the date and place Kris gave in question 6. If the publish date is after December 16, 2026, the December 16 meetup line has been changed or removed.
5. **Slug collision.** Authenticated, read-only, all statuses, posts and pages: `FORMAT=json make draft-queue-audit`, then read `slug_matches["bc-ai-year-one"]` (or the slug Kris picked). Required result: 0 posts and 0 pages. Record the UTC time. Never print credentials. The offline publisher dry-run does **not** check the slug; it reports `"slug_check": "skipped_offline"`.
6. **Taxonomy.** Read-only REST lookups for the category and the four tags in `seo-meta.md`. Every name must resolve to an existing term by slug. If any matches nothing, stop, because `--execute` would create a new term. Never add `BC + AI` to the frontmatter tags: it slugifies to `bc-ai` and attaches the `bc ai` tag instead (see `seo-meta.md`).
7. **Image.** Kris's ruling on question 7 is recorded, with Michelle Diamond's permission and credit line if it is her photograph. The chosen frame has passed featured-image-forge multi-ratio crop QC and Kris has approved it. If it is an existing media item, the publisher will not attach it: setting `featured_media` is a second write that needs its own approval and readback. If the package declares no local images, the publisher uploads nothing and leaves `featured_media` unset.
8. **Links.** Every URL in `internal-links.md` still returns 200, and the chosen canonical still returns 404.
9. **Voice check.** `make voice-check FILES="content/drafts/2026-11-12-bc-ai-year-one/post.md content/drafts/2026-11-12-bc-ai-year-one/post.html"` reports 0 violations.
10. **Dry-run.** `python3 scripts/notion-to-wp/create_local_wp_draft.py content/drafts/2026-11-12-bc-ai-year-one/post.md` (or the package venv's Python) exits 0 and shows the expected title, slug, category, four tags and image list.
11. **Repo gates.** `make verify` and `git diff --check` pass.

## Staging gate (after the preflight, never before)

- [ ] Kris approves one new unpublished WordPress post with status `draft`, built from the pinned hashes. The write set is that one post. No existing post, page, media item or term changes.
- [ ] Run the publisher with `--execute` through Varlock. Record the post ID and the readback `status` and `slug` here.
- [ ] Compare the admin preview with `post.html`: body, single H1 from the title field, the YouTube embed and its caption link, both pull quotes, the three separators, the room-lead list, category, tags, canonical, OG metadata, image and every link.

## Rollback

This is a new object, so there is no earlier version to restore. Before the write, the rollback proof is the empty same-day slug check. After it, the default is to leave the post as an unpublished draft and report its ID and the problem. Moving it to trash needs Kris's explicit approval for that post ID, with a readback of ID and status before and after. Never `force=true`.

## Checks run while building this package (2026-11-12 Pacific, 2026-11-13 UTC)

- `make voice-check` on `post.md` and `post.html`: 2 files scanned, 0 violations, 0 baseline-waived. The full `make voice-check`: 187 files scanned, 0 violations, 214 baseline-waived.
- `make docs-truth-check`: passed.
- Offline publisher dry-run with system `python3` (3.14.6; this worktree has no package venv): exit 0, `slug: bc-ai-year-one`, `slug_check: skipped_offline`, `images: []`, category `Vancouver AI Ecosystem`, tags `bc ai`, `bc ai ecosystem`, `vancouver ai`, `Community Building`. Neither legacy env file the publisher can fall back to exists on this machine, and both fallback paths were pointed at a nonexistent file for the run, so it read no `.env`.
- `LOCAL_ONLY=1 FORMAT=json make draft-queue-audit`: exit 0. 105 local packages. This one reads 952 words, 21 markdown links, 21 html links, 49 blocks, 0 images, 0 TODO markers. The audit does not count `[KK: ...]` placeholders; preflight step 2 does.
- `make python-test PYTHON=python3`: 280, 993, 12 and 68 passed.
- `post.html` was generated from `post.md` with the shared `wp_blocks` helpers. The same generator reproduces the #959 package's `post.html` byte for byte.
- No em dashes, en dashes or curly quotes in any file of this package, and every file encodes to cp1252.
- Links: all 17 unique URLs and the embedded video returned 200 logged-out at 03:13 UTC, and `https://kriskrug.co/bc-ai-year-one/` returned 404.
- No authenticated slug check and no REST term check were run. Both wait for the day of any write.

Until every box above is ticked, this package stays a local `status: draft` and nothing may claim it is published.
