# Both Things Are True: publish gate

**Status: READY TO STAGE, pending only two things:** Kris's approval of the featured image crop, and the same-day preflight below (authenticated all-status slug check, taxonomy IDs and the rest of the list). Do not stage before both. Never schedule or publish from this package.

This package stages #959, step 1 of the Q1 2027 keynote pipeline (#1277): the Both Hands Full keynote in writing, for 2027 bookers. The folder date is the day the package was built, not a post date.

- Kris ruled on all 14 open facts on 2026-11-12. Every ruling matched the draft's recommendation, so the body copy did not change (`open-facts-for-kk.md`).
- No WordPress object exists for this package. No WordPress write and no authenticated call was made while building it or applying the rulings, and no `.env` file was read. The only WordPress reads were logged-out public REST and page GETs.
- WordPress draft 11881 stays untouched until this post is live (open-facts question 6).

## Pinned source hashes (2026-11-12, after Kris's rulings)

| File | SHA-256 |
|---|---|
| `post.md` | `15be26d451a1eed4b523a8d5ee9d788b303fbc5bf061007b63f6cfa45279c666` |
| `post.html` | `06bf1ce8ffabe8eb7e294b6fe19385c91fc5b0caa8006f7ee2d2a66210fa0945` |

Any edit to either file makes these pins stale. Then stop, rerun the preflight and pin again in a content PR that merges before any write.

## Featured image: awaiting Kris's crop approval

- **Pick: LaSalle frame 10, media ID 11831**, already in the media library, so nothing is uploaded. `https://kriskrug.co/wp-content/uploads/2026/05/kk-laSalle-both-hands-full-10-scaled.jpg`, 2560x1440, served file SHA-256 `33fe33a3f2d241feea41695f822046cdf2ee7a0558d040465878903015ce436d`, not attached to any post. Kris ruled on 2026-11-12 that the frame is his to reuse, with no credit line.
- **Status: awaiting Kris's crop approval.** He gets the QC contact sheet with the approval ask. The sheet stays outside this public repo.
- **Crop QC, 2026-11-13 UTC.** featured-image-forge `hero_qc.py` mechanical gates pass for both frames: landscape, at least 1200x630, aspect 1.778. Then a visual pass on every crop the theme and the social cards use:

| Crop | Where it shows | Frame 10 (11831) | Frame 20 (11833) |
|---|---|---|---|
| 16:9 | embeds, proof cards, the frame itself | pass | pass |
| 1.91:1 | `og:image` in social cards | pass | pass |
| 1.95:1, 760x390 | single post hero on desktop (`.aurora-journal-featured`, max-height 390, cover) | pass | pass |
| 3:2 | single post hero on phones, journal thumbnails, front-page Recent writing | pass | pass |
| 1:1 | square thumbnails | pass | pass, the yellow sign on the right is cut to its first letter |
| 300 px wide | legibility floor | pass, face and mic read | fail, the speaker is a speck and the slide is unreadable |
| 94x80 (1.18:1) | journal thumbnail on phones | pass, a person on stage | fail, nothing reads |

- **Why frame 10:** Kris is the subject, grinning with the mic, and his face, hands and mic stay whole in every crop down to the 94 px phone thumbnail. Frame 20 is the better room shot, a packed house facing the reflection slide, but it falls apart below about 600 px, and his head covers the n in "never", so the slide question misreads. It would work as an in-body image, not as the featured image.
- **Alt text:** the live alt on 11831 has an em dash and a frame number. The proposed replacement is in `alt-text.md`. Changing it is a write to an existing media item and needs Kris's approval on its own. Without that approval the post shows the current alt.

## Media plan (no upload)

The publisher sets `featured_media` only from images it uploads out of the package folder, and this package declares none. Attaching the existing frame is its own step after staging, and each write needs Kris's approval:

1. The staging write (`--execute`) creates the draft with `featured_media` unset.
2. After Kris approves the crop, read back the new draft's ID, slug `both-things-are-true` and status `draft`, then PATCH `featured_media` to 11831 on that draft only. Read `featured_media` back.
3. Only if Kris approves it separately: update `alt_text` on media 11831 to the line in `alt-text.md`, with a readback of the old and new values.

The write set is one new post, plus at most the alt text field on media 11831. No other existing post, page, media item or term changes.

## Preflight to rerun on the day of any write

Every item is dated evidence. A pass on another day does not count.

1. **Source hashes.** `shasum -a 256 post.md post.html` match the pins above. If not, stop.
2. **Quote.** The pull quote in `post.md` and `post.html` matches the wording Kris confirmed in question 1 (the public caption wording, "mankind" included), character for character.
3. **Slug collision.** Authenticated, read-only, all statuses, posts and pages: `FORMAT=json make draft-queue-audit`, then read `slug_matches["both-things-are-true"]`. Required result: 0 posts and 0 pages. Record the UTC time. Never print credentials. The offline publisher dry-run does **not** check the slug; it reports `"slug_check": "skipped_offline"`.
4. **Taxonomy IDs.** Rerun the term check in `seo-meta.md` against public REST. Every name must resolve to an existing ID (category 1665, tags 1683, 1696, 89, 1667) by the `ensure_term()` rule. `AI for Creatives` resolves by name only, because its live slug is `ai-creatives`. If any name matches nothing, stop, because `--execute` would create a new term.
5. **Image.** Kris's crop approval is recorded here with its date. Media 11831 still exists, still serves the approved frame and is still 2560x1440.
6. **Links.** Every URL in `internal-links.md` still returns 200, and the dated canonical still returns 404.
7. **Voice check.** `make voice-check FILES="content/drafts/2026-11-12-both-things-are-true/post.md content/drafts/2026-11-12-both-things-are-true/post.html"` reports 0 violations.
8. **Dry-run.** `scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/create_local_wp_draft.py content/drafts/2026-11-12-both-things-are-true/post.md` exits 0 and shows the expected title, slug, category, four tags and an empty image list.
9. **Repo gates.** `make verify` and `git diff --check` pass.

## Staging gate (after the preflight, never before)

- [ ] Kris approves the featured image crop. Record the date and the media ID here.
- [ ] Kris approves one new unpublished WordPress post with status `draft`, built from the pinned hashes.
- [ ] Run the publisher with `--execute` through Varlock. Record the post ID and the readback `status` and `slug` here.
- [ ] Run media plan step 2, and step 3 only if approved, each with its readback.
- [ ] Compare the admin preview with `post.html`: body, single H1 from the title field, the YouTube embed and its caption link, both pull quotes, category, tags, canonical, OG metadata, featured image and every link.

## Rollback

This is a new post, so there is no earlier version to restore. Before the write, the rollback proof is the empty same-day slug check. After it, the default is to leave the post as an unpublished draft and report its ID and the problem. Moving it to trash needs Kris's explicit approval for that post ID, with a readback of ID and status before and after. Never `force=true`. If the featured image step goes wrong, unset `featured_media` on the draft. If the alt text update goes wrong, write back the old value from its readback.

## Checks run for this PR (2026-11-12 Pacific, 2026-11-13 UTC)

- `make voice-check` on `post.md` and `post.html`: 2 files scanned, 0 violations, 0 baseline-waived.
- Offline publisher dry-run: exit 0, title `Both Things Are True`, `slug: both-things-are-true`, `slug_check: skipped_offline`, `images: []`, category `AI for Creatives`, tags `Both Hands Full`, `Keynotes`, `speaking`, `taste`. Neither legacy env file the publisher can fall back to exists on this machine, so the dry-run read no `.env`.
- `LOCAL_ONLY=1 FORMAT=json make draft-queue-audit`: exit 0, 104 local packages. This one reads 1,177 words, 21 markdown links, 21 html links, 60 blocks, 0 images, 0 TODO markers and all six expected files.
- Public REST term check at 02:59 to 03:00 UTC: all five names resolve (see `seo-meta.md`).
- Pull quote re-checked against the committed caption file: every word matches.
- Image reads and crop QC as above.
- No authenticated slug check was run. That waits for the day of any write.

Until every box above is ticked, this package stays a local `status: draft` and nothing may claim it is published.
