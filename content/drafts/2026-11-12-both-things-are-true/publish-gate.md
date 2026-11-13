# Both Things Are True: publish gate

**Status: SCHEDULED.** WordPress post **13004**, status `future`, publishes **Tue 2026-11-24 at 09:00 Vancouver time (16:00 UTC)**. Featured image: media **11831**. Receipt: `docs/current-state/reports/scheduled-posts-2026-11-19-24.md`.

This package stages #959, step 1 of the Q1 2027 keynote pipeline (#1277): the Both Hands Full keynote in writing, for 2027 bookers. The folder date is the day the package was built, not a post date.

- Kris ruled on all 14 open facts on 2026-11-12. Every ruling matched the draft's recommendation, so the body copy did not change (`open-facts-for-kk.md`).
- After seeing the crop QC sheet, Kris approved in chat on 2026-11-12: media 11831 as the featured image, its alt text rewritten without the em dash with the same meaning, and scheduling for 2026-11-24 at 09:00 Vancouver time. The orchestrator session relayed those approvals to the lane that did the writes.
- WordPress draft 11881 stays untouched until this post is live (open-facts question 6).

## Pinned source hashes (2026-11-12, after Kris's rulings)

| File | SHA-256 |
|---|---|
| `post.md` | `15be26d451a1eed4b523a8d5ee9d788b303fbc5bf061007b63f6cfa45279c666` |
| `post.html` | `06bf1ce8ffabe8eb7e294b6fe19385c91fc5b0caa8006f7ee2d2a66210fa0945` |

The scheduled post was built from these exact files. Its stored `content.raw` hashes to the same `06bf1ce8...0945`. Any later edit to either file is not on WordPress until a reviewed update pushes it.

## What was written (2026-11-13 UTC)

| Time (UTC) | Write | Readback |
|---|---|---|
| 03:18:13 | `create_local_wp_draft.py --execute` created post 13004 | `status: draft`, `slug: both-things-are-true`, content equal to `post.html` |
| 03:18:54 | `alt_text` on media 11831 rewritten without the em dash, after a context=edit snapshot | new alt text stored; source URL, parent, slug, sizes, title and caption unchanged |
| 03:19:10 | one guarded update on 13004: `status: future`, `date_gmt: 2026-11-24T16:00:00`, `featured_media: 11831` | `status: future`, `date_gmt` as sent, `featured_media: 11831` |

Final context=edit readback: `status: future`, `date_gmt: 2026-11-24T16:00:00`, slug `both-things-are-true`, featured media 11831, category 1665, tags 1683, 1696, 89 and 1667, title, excerpt and both SEO meta fields as in the package, and `content.raw` byte-identical to the pinned `post.html`. Logged out, the dated URL, the bare slug and `?p=13004` all return 404, and REST refuses to show the post.

**Clock note.** WordPress shows the date as 08:00 because the site's timezone setting is a fixed UTC-8 offset. Vancouver is on UTC-7 on 2026-11-24 (tz database 2026f), so `date_gmt` 16:00 UTC is 09:00 in Vancouver. Changing the site setting is Kris's call and was not done.

## Featured image

- Media 11831, `kk-laSalle-both-hands-full-10-scaled.jpg`, 2560x1440, already in the library. Nothing was uploaded.
- Alt text now: `Kris Krüg presenting Both Hands Full keynote at LaSalle College Vancouver, frame 10`. The old value is in the receipt for rollback.
- Crop QC (2026-11-13 UTC): featured-image-forge gates pass, and frame 10 passed the visual check at every crop the theme and social cards use: 16:9, 1.91:1, the 760x390 desktop hero, 3:2, 1:1, 300 px and the 94x80 phone thumbnail. Frame 20 (media 11833) failed at 300 px and below.

## Before 2026-11-24

- Nothing else is needed for the post to go live on time. WordPress publishes it at 16:00 UTC.
- After it is live: read back the public canonical URL (200), `og:image`, the featured image crop, category, tags and every link, and record the result in the receipt.
- After it is live: draft 11881 can go to trash only with Kris's explicit approval for that ID, never `force=true`.
- Optional follow-ups from `internal-links.md`, each needing its own approval: link this post from the Both Hands Full card on `/speaking/` and from the two related posts.

## Rollback

Never delete. To stop the publish, move post 13004 back to `draft` with a guarded update (slug `both-things-are-true` must resolve to 13004) and read back `status: draft`. To undo the alt text, write the old value from the receipt back to media 11831 and read it back. Moving 13004 to trash needs Kris's explicit approval for that ID, with a readback of ID and status before and after.

## Preflight run before the writes (2026-11-13 UTC)

1. **Source hashes:** `post.md` and `post.html` matched the pins above.
2. **Quote:** the pull quote matches the caption wording Kris confirmed, word for word.
3. **Slug collision (authenticated, 03:14 UTC):** `draft_queue_audit.py --format json` under Varlock, `slug_matches["both-things-are-true"]` was empty: 0 posts and 0 pages in any status.
4. **Taxonomy (02:59 UTC, public REST):** category 1665 by name, tags 1683, 1696, 89 and 1667 by slug. No new term was created.
5. **Image:** Kris's crop approval recorded above. Media 11831 served 2560x1440 at its public URL.
6. **Links (03:15 UTC):** all 21 URLs in `post.html` returned 200. The dated canonical and the bare slug returned 404.
7. **Voice check:** 0 violations on `post.md` and `post.html`.
8. **Dry-run:** exit 0, slug `both-things-are-true`, `images: []`, category `AI for Creatives`, four tags.
9. **Repo gates:** `git diff --check` clean; CI on the PR runs the full suite. `make verify` was not run in this worktree, which has no Python venv or PHPCS install.

Nothing here claims the post is published. It is scheduled, and it is not public until 2026-11-24 16:00 UTC.
