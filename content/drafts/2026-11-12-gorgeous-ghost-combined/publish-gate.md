# Gorgeous Ghost combined package: publish gate

**Status: READY TO STAGE, pending only two things:** Kris's approval of the featured image crop, and the same-day preflight below (authenticated all-status slug check, taxonomy IDs and the rest of the list). Do not stage before both. Never schedule or publish from this package.

This package combines the #771 art-project package and the #1016 making-of draft, per Kris's 2026-11-12 combine ruling on #771. Staging moved to the Nov 19 to 30 window. The folder date is the day the package was built, not a post date.

- Kris ruled on all 14 open facts on 2026-11-12, and the copy follows every ruling (`open-facts-for-kk.md`).
- No WordPress object exists for this package. No WordPress write and no authenticated call was made while building it or applying the rulings, and no `.env` file was read.
- The old package `content/drafts/2026-08-12-gorgeous-ghost-art-project/` is untouched. Kris's combine ruling makes this package the one to stage under `gorgeous-ghost`. Retiring the old package follows in its own content PR (open-facts question 14).

## Pinned source hashes (2026-11-12, after Kris's rulings)

| File | SHA-256 |
|---|---|
| `post.md` | `da46ab33b2578dd1d11be55d29e509790109a75ef98d9d7d28eed4857e9210bd` |
| `post.html` | `45e2462bef9b7def4e6d1fddb01c6c73c71f9729d171eccde02e2ca5bfee1e57` |

Any edit to either file makes these pins stale. Then stop, rerun the preflight and pin again in a content PR that merges before any write.

## Featured image: awaiting Kris's crop approval

- **Pick:** the film's reveal art, a lightning-painted eye in a jeweled star field, from Kris's own film site. Source `https://gorgeousghost.com/experience/reveal-hero-1600.webp`, 1600x893, SHA-256 `3a4f8fc7b5e4f063d712771cdbbef8b42ff889112e1731d61c95b3dc8ea70831`, which matches the site's asset manifest. Kris ruled on 2026-11-12 that his film art is his to reuse.
- **Master:** a 1600x900 JPEG, made by mirroring 4 rows at the top and 3 at the bottom of the source. No resampling, so every source pixel is kept. The mirrored rows are star field and the seam does not show at 8x zoom. This build's master hashes to `83de184cb2ffe9ced7fd0ad53e55b129171ab16879a0e2bb284cc0b976aa6b14`. Upload name: `gorgeous-ghost-reveal-eye-1600x900.jpg`. Alt text: `alt-text.md`.
- **Status: awaiting Kris's crop approval.** He gets the QC contact sheet with the approval ask. The master and the sheet are kept outside this public repo, and nothing has been uploaded.
- **Crop QC, 2026-11-13 UTC.** featured-image-forge `hero_qc.py` mechanical gates pass: landscape, at least 1200x630, aspect 1.778. Then a visual pass on every crop the theme and the social cards use:

| Crop | Where it shows | Verdict |
|---|---|---|
| 16:9 | embeds, proof cards, the master itself | pass |
| 1.91:1 | `og:image` in social cards | pass |
| 1.95:1, 760x390 | single post hero on desktop (`.aurora-journal-featured`, max-height 390, cover) | pass |
| 3:2 | single post hero on phones, journal thumbnails, front-page Recent writing | pass |
| 1:1 | square thumbnails | pass |
| 300 px wide | legibility floor | pass, the eye and the bolt still read |
| 94x80 (1.18:1) | journal thumbnail on phones | pass, small but recognizable |

- **Rejected:** the title-card frame from the public YouTube cut (`maxresdefault.jpg`, 1280x720, the same frame as the site's `title-card.webp`) and the share image (`og/share.jpg`, 1200x630). Both sit under the 1600x900 master size and would need upscaling. Both lose letters of GORGEOUS at 3:2 and 1:1. Both slice the BC + AI Film Club Prompt Challenge line at 1.91:1 and in the 760x390 hero, and the share image already cuts that line in its own frame.

## Media plan (nothing uploaded yet)

The publisher sets `featured_media` only from images it uploads out of the package folder. This package declares none, because no image goes into the public repo. So the featured image is its own step after staging, and each write needs Kris's approval:

1. The staging write (`--execute`) creates the draft with `featured_media` unset.
2. After Kris approves the crop, upload the approved master once, with the alt text from `alt-text.md`, through the repo's WordPress client under Varlock. Before uploading, confirm the file still hashes to the approved master and that no media item already carries its file name. Record the new media ID.
3. Read back the new draft's ID, slug `gorgeous-ghost` and status `draft`, then PATCH `featured_media` on that draft only. Read `featured_media` back.

The whole write set is one new post and one new media item. No existing post, page, media item or term changes.

## Preflight to rerun on the day of any write

Every item is dated evidence. A pass on another day does not count.

1. **Source hashes.** `shasum -a 256 post.md post.html` match the pins above. If not, stop.
2. **Slug collision.** Authenticated, read-only, all statuses, posts and pages: `FORMAT=json make draft-queue-audit`, then read `slug_matches["gorgeous-ghost"]`. Required result: 0 posts and 0 pages. Record the UTC time. Never print credentials. The offline publisher dry-run does **not** check the slug; it reports `"slug_check": "skipped_offline"`.
3. **Taxonomy IDs.** Rerun the term check in `seo-meta.md` against public REST. Every name must resolve to an existing ID (1755, 1804, 1682, 1785, 1395) by the `ensure_term()` rule. If any name matches nothing, stop, because `--execute` would create a new term.
4. **Image.** Kris's crop approval is recorded here with its date, and the file to upload hashes to the master he approved.
5. **Credits.** Re-read the transcript Credits segment on https://gorgeousghost.com/ and confirm it still names the Scallywags as Kevin Friel, Magenta Rune and Mayumi Rawlings, "Created by Kris Krüg", and special thanks to Kaoru Yoshihira and Floyo.ai, as the post does.
6. **Links.** Every URL in `internal-links.md` still returns 200, and the dated canonical still returns 404.
7. **Voice check.** `make voice-check FILES="content/drafts/2026-11-12-gorgeous-ghost-combined/post.md content/drafts/2026-11-12-gorgeous-ghost-combined/post.html"` reports 0 violations.
8. **Dry-run.** `scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/create_local_wp_draft.py content/drafts/2026-11-12-gorgeous-ghost-combined/post.md` exits 0 and shows the expected title, slug, category, four tags and an empty image list.
9. **Repo gates.** `make verify` and `git diff --check` pass.

## Staging gate (after the preflight, never before)

- [ ] Kris approves the featured image crop. Record the date and the approved master's SHA-256 here.
- [ ] Kris approves one new unpublished WordPress post with status `draft`, built from the pinned hashes.
- [ ] Run the publisher with `--execute` through Varlock. Record the post ID and the readback `status` and `slug` here.
- [ ] Run media plan steps 2 and 3, each with its readback, and record the media ID here.
- [ ] Compare the admin preview with `post.html`: body, single H1 from the title field, the YouTube embed, credits, date, category, tags, canonical, OG metadata, featured image and every link.

## Rollback

This is a new post, so there is no earlier version to restore. Before the write, the rollback proof is the empty same-day slug check. After it, the default is to leave the post as an unpublished draft and report its ID and the problem. Moving it to trash needs Kris's explicit approval for that post ID, with a readback of ID and status before and after. Never `force=true`. If the featured image step goes wrong, unset `featured_media` on the draft. Media trash is off on kriskrug.co, so deleting the uploaded media item would be permanent; leave that to Kris.

## Checks run for this PR (2026-11-12 Pacific, 2026-11-13 UTC)

- `make voice-check` on `post.md` and `post.html`: 2 files scanned, 0 violations, 0 baseline-waived.
- Offline publisher dry-run: exit 0, title `I Made a Gorgeous Ghost`, `slug: gorgeous-ghost`, `slug_check: skipped_offline`, `images: []`, category `Creative Technology & Making`, tags `Gorgeous Ghost`, `Creative AI`, `AI Film Club`, `AI Music`. Neither legacy env file the publisher can fall back to exists on this machine, so the dry-run read no `.env`.
- `LOCAL_ONLY=1 FORMAT=json make draft-queue-audit`: exit 0, 104 local packages. This one reads 1,355 words, 18 markdown links, 18 html links, 75 blocks, 0 images, 0 TODO markers and all six expected files.
- Public term check rerun at 02:59 UTC: all five names resolve (see `seo-meta.md`).
- Image fetch and crop QC as above.
- No authenticated slug check was run. That waits for the day of any write.

Until every box above is ticked, this package stays a local `status: draft` and nothing may claim it is published.
