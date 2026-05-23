# StoryHive Image Candidate Pass - 2026-05-22

**Purpose:** first image/archive pass after the StoryHive draft rebuild.
**Status:** documented candidates only. No media swap performed in this pass.

## Decision

Keep the current WordPress media in the three review drafts for now. They are stable, already in the media library, and good enough for editorial review.

Do a deliberate Flickr/archive upgrade before scheduling, especially for `I Won't Fake The People Who Showed Up`.

## Sources Checked

- Kris Krug Flickr profile: <https://www.flickr.com/photos/kk/>
- Flickr photo: <https://www.flickr.com/photos/kk/55121266130>
- Flickr album: <https://www.flickr.com/photos/kk/sets/72177720332384821>
- Flickr photo: <https://www.flickr.com/photos/kk/55132944075>
- Existing WordPress media already assigned in drafts:
  - `11838` / `12-ai-is-a-mirror.jpg`
  - `3252` / `asa-mathat-2-scaled.jpg`
  - `11841` / `03-both-hands-full-thesis.jpg`

## Current Draft Images

| Draft | Current image | Verdict |
|---|---|---|
| `the-75-percent-rule-ai-art-adjacent-work` | WP media `11838`, "AI Is a Mirror" slide | Keep for review. Strong conceptual fit and already aligns with the archive-as-mirror argument. |
| `i-wont-fake-the-people-who-showed-up` | WP media `3252`, Asa Mathat portrait/event strip | Acceptable for review, but should get a stronger real-community/documentary image before scheduling. |
| `speak-it-into-existence-ai-voice-first-workflows` | WP media `11841`, Both Hands Full thesis slide | Keep for review. Could later swap to a real speaking/mic/workflow image if available. |

## Flickr Candidates

| Candidate | Source | Use |
|---|---|---|
| `AI as a mirror of identity` | <https://www.flickr.com/photos/kk/55121266130> | Alternate or supporting image for `The 75% Rule`; works as a conceptual mirror/identity visual. |
| `Vancouver AI Community Meetup Feb 2026` album | <https://www.flickr.com/photos/kk/sets/72177720332384821> | Best source pool for a real community/documentary replacement on `I Won't Fake The People Who Showed Up`. |
| `AIMeetUp_Feb2026_MichelleDiamond-259` | <https://www.flickr.com/photos/kk/55132944075> | Candidate for documentary/community presence; needs KK consent/fit review before upload/use. |

## Pre-Schedule Image Gate

Before scheduling any StoryHive post:

1. Choose final featured image.
2. Confirm image rights/source and whether the subject context is appropriate.
3. Upload to WordPress if not already in the media library.
4. Set `featured_media`.
5. Use one inline image only if it materially improves the post.
6. Write natural alt text.
7. Re-run `prepare_review_draft.py --wp-id <id> --fail-on-warning`.
8. Re-read WordPress draft content and featured media through REST.

## Recommendation

Publish order should not wait on perfect image curation for all three posts.

Do this instead:

1. Use `The 75% Rule` as the proof post with current WP media `11838`.
2. Run a focused Flickr/community image selection for `I Won't Fake The People Who Showed Up`.
3. Keep `Speak It Into Existence` in review until the first proof post survives preview QA and scheduling.
