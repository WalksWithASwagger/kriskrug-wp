# Publish Gate

Status: private WordPress draft created as a standalone support post; do not publish without KK review.

## WordPress Draft

- WP draft ID: `11879`
- Edit URL: <https://kriskrug.co/wp-admin/post.php?post=11879&action=edit>
- Verified readback: status `draft`, slug `ai-media-appearances-podcast-guesting`

## WP draft attempt - 2026-05-19

- [x] Confirmed `main` was clean and even with `origin/main`.
- [x] Confirmed WordPress REST credentials are present locally without printing them.
- [x] Confirmed connector venv dependencies are available.
- [x] Confirmed exact target slug has zero authenticated WordPress matches.
- [x] Confirmed all links in `post.html` returned `200`.
- [x] Confirmed sensitive-string privacy scan had no matches.
- [x] WordPress draft created after backup gate retirement and fresh slug check.

Status: the earlier backup blocker is retired. See `../../source-packs/keynotes-2026/verification/APPEARANCES-ROUNDUP-WP-DRAFT-BLOCKED-2026-05-19.md` for the older stopped attempt.

## Editorial decision

- [x] `/podcast-guesting-page-epk/` is the primary producer-facing page and was deployed on 2026-05-19.
- [x] This draft is now positioned as a supporting authority/archive post, not a replacement for the EPK.
- [x] The draft includes the user-requested Vancouver AI March 2026 video: `https://www.youtube.com/watch?v=T5ANAthZewE`.

## Required review

- [ ] Confirm final featured appearances and order.
- [ ] Choose final featured image or embed-only treatment.
- [ ] Check every public source link before live use.
- [ ] Confirm no third-party endorsement is implied beyond the public appearances.
- [ ] If creating a WP draft, check the target slug before any live WordPress write.
- [ ] If publishing publicly, add backlinks from `/speaking/`, `/about/`, and `/podcast-guesting-page-epk/` after the post URL exists.

## Safety notes

- Public source links only.
- No private Notion material copied into the post body.
- No private contact details included.
- No third-party transcript dumps included.
- No third-party podcast cover art, CBC art, Horizons art, or YouTube thumbnails should be imported as the featured image until rights are confirmed.
