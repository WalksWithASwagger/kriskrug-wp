# Gorgeous Ghost combined package: publish gate

**Status: SCHEDULED.** WordPress post 13003 publishes Thu 2026-11-19 at 09:00 Vancouver time (16:00 UTC), with media 13006 as its featured image. The lane that staged the draft could not upload the image. Kris had approved the orchestrating session running these writes itself if that happened, and it finished them at 03:31 UTC on 2026-11-13. Receipt: `docs/current-state/reports/scheduled-posts-2026-11-19-24.md`.

This package combines the #771 art-project package and the #1016 making-of draft, per Kris's 2026-11-12 combine ruling on #771. The folder date is the day the package was built, not a post date.

- Kris ruled on all 14 open facts on 2026-11-12, and the copy follows every ruling (`open-facts-for-kk.md`).
- After seeing the crop QC sheet, Kris approved in chat on 2026-11-12: the reveal-eye master as the featured image, and scheduling for 2026-11-19 at 09:00 Vancouver time. The orchestrator session relayed those approvals.
- The old package was archived to `content/drafts/archive/2026-08-12-gorgeous-ghost-art-project/` by Kris's ruling (open-facts question 14).

## Pinned source hashes (2026-11-12, after Kris's rulings)

| File | SHA-256 |
|---|---|
| `post.md` | `da46ab33b2578dd1d11be55d29e509790109a75ef98d9d7d28eed4857e9210bd` |
| `post.html` | `45e2462bef9b7def4e6d1fddb01c6c73c71f9729d171eccde02e2ca5bfee1e57` |

Draft 13003 was built from these exact files. Its stored `content.raw` hashes to the same `45e2462b...1e57`. `post.md` still names the old package's pre-archive path under `sources.base_package`; it was left alone so the pin stays valid.

## What was written (2026-11-13 UTC)

| Time (UTC) | Write | Readback |
|---|---|---|
| 03:17:17 | `create_local_wp_draft.py --execute` created post **13003** | `status: draft`, `slug: gorgeous-ghost`, category 1755, tags 1804, 1682, 1785 and 1395, title, excerpt and both SEO meta fields as in the package, `content.raw` byte-identical to the pinned `post.html` |
| 03:31:15 | upload of the approved master as media **13006**, then its alt text | 1600x900, `image/jpeg`, alt text as approved, stored as `gorgeous-ghost-reveal-eye-1600x900-1.jpg` |
| 03:31:17 | post 13003: `status: future`, `date_gmt: 2026-11-19T16:00:00`, `featured_media: 13006` | `future`, `date_gmt` as sent, `date` 2026-11-19T08:00:00 (the site's fixed UTC-8 clock), featured 13006, category and tags unchanged, `content.raw` still the pinned `post.html` |

Logged out after scheduling, the dated URL `https://kriskrug.co/2026/11/19/gorgeous-ghost/` and `?p=13003` return 404.

## Featured image: media 13006

- **Approved by Kris on 2026-11-12:** the film's reveal art, a lightning-painted eye in a jeweled star field. Source `https://gorgeousghost.com/experience/reveal-hero-1600.webp`, 1600x893, SHA-256 `3a4f8fc7b5e4f063d712771cdbbef8b42ff889112e1731d61c95b3dc8ea70831`. His film art is his to reuse.
- **Master:** 1600x900 JPEG (quality 92, no chroma subsampling), made by mirroring 4 rows at the top and 3 at the bottom of the source, with no resampling. The approved build hashes to `83de184cb2ffe9ced7fd0ad53e55b129171ab16879a0e2bb284cc0b976aa6b14`. Upload name: `gorgeous-ghost-reveal-eye-1600x900.jpg`. Alt text: `A lightning-painted eye floating in a jeweled star field` (`alt-text.md`). The file is kept outside this public repo.
- **Uploaded** 2026-11-13T03:31:15Z as media 13006. WordPress added `-1` to the file name. No file with the plain name existed (that URL returns 404); WordPress does this for file names that end in a size such as `-1600x900`.
- **Crop QC (2026-11-13 UTC):** featured-image-forge gates pass, and the master passed the visual check at every crop the theme and social cards use: 16:9, 1.91:1, the 760x390 desktop hero, 3:2, 1:1, 300 px and the 94x80 phone thumbnail. The YouTube title-card frame and the share image failed (letters of GORGEOUS clipped at 3:2 and 1:1, credit line sliced at 1.91:1, both under the master size).

## Finishing steps (all approved by Kris; done 2026-11-13 UTC)

Run in this order, each step passing before the next: the media search found nothing, the master hash matched, the slug resolved only to 13003, and 13003 was still an unchanged draft when the schedule was sent.

1. Authenticated media search for `gorgeous-ghost-reveal-eye`: expect nothing. Check the master still hashes to `83de184c...6b14`.
2. Upload the master once, with the alt text above, through the repo's WordPress client under Varlock. Read back the media ID, 1600x900 and the alt text.
3. One guarded update on post 13003 (slug `gorgeous-ghost` must resolve to 13003, status must still be `draft`): `status: future`, `date_gmt: 2026-11-19T16:00:00`, `featured_media: <new media ID>`. Do not send `date`: the site's timezone setting is a fixed UTC-8 offset, so a local `date` of 09:00 would land at 10:00 Vancouver time.
4. Context=edit readback: `status: future`, `date_gmt` as sent, featured media, category, tags, and `content.raw` still equal to the pinned `post.html`. Logged out, the dated URL `https://kriskrug.co/2026/11/19/gorgeous-ghost/` must still return 404.
5. Record the media ID and the readback in the receipt, and switch this gate to SCHEDULED.

If any step fails, stop and leave 13003 as a draft.

## Admin preview

The staging checklist on `main` asked for a comparison of the wp-admin preview with `post.html`. It was not done: agents cannot see the signed-in preview. In its place, the context=edit readback showed `content.raw` byte-identical to the pinned `post.html`, and a read-only logged-out readback (HTTP 200, title, `og:image`, canonical) is scheduled for 10:00 on 2026-11-19. Kris can still open the preview before then.

## Rollback

Never delete. Draft 13003 can stay a draft indefinitely. Once scheduled, move it back to `draft` with a guarded update and read back `status: draft`. Moving it to trash needs Kris's explicit approval for that post ID, with a readback before and after. If the featured image is wrong, unset `featured_media`. Media trash is off on kriskrug.co, so deleting an uploaded media item is permanent; leave that to Kris.

## Preflight run before the writes (2026-11-13 UTC)

1. **Source hashes:** `post.md` and `post.html` matched the pins above.
2. **Slug collision (authenticated, 03:14 UTC):** `draft_queue_audit.py --format json` under Varlock, `slug_matches["gorgeous-ghost"]` was empty: 0 posts and 0 pages in any status.
3. **Taxonomy (02:59 UTC, public REST):** 1755, 1804, 1682, 1785 and 1395 all resolve by slug. No new term was created.
4. **Image:** Kris's approval recorded above.
5. **Credits (02:56 UTC):** the film site's transcript credits still match the post.
6. **Links (03:15 UTC):** all 14 URLs in `post.html` returned 200. The dated canonical and the bare slug returned 404.
7. **Voice check:** 0 violations on `post.md` and `post.html`.
8. **Dry-run:** exit 0, slug `gorgeous-ghost`, `images: []`, category `Creative Technology & Making`, four tags.
9. **Repo gates:** `git diff --check` clean; CI on the PR runs the full suite. `make verify` was not run in this worktree, which has no Python venv or PHPCS install.

The post is scheduled, not published. It goes live at 2026-11-19 16:00 UTC unless someone moves it back to draft first.
