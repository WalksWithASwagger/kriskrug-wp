# StoryHive Review-Ready Drafts - 2026-05-22

**Purpose:** current review packet after the first weak draft pass was rebuilt.
**Status:** WordPress drafts are ready for KK review, not scheduled, not published.

## Process Fixes Applied

- Rewrote the three StoryHive idea posts from the source spine instead of polishing the weak first pass.
- Added `scripts/notion-to-wp/prepare_review_draft.py` so local review drafts generate Gutenberg block HTML before WordPress update.
- The prep script now checks minimum word count, links, images or featured media, private/source markers, weak AI-copy phrases, and WordPress block generation.
- Updated existing WordPress drafts only after slug, draft status, and title-similarity checks.
- Selected existing WordPress media as featured/inline imagery for each draft.

## Drafts

| WP ID | Title | Status | Words | Links | Images | Blocks | Featured Media | Edit |
|---:|---|---|---:|---:|---:|---:|---:|---|
| 11876 | The 75% Rule: Send AI After The Art-Adjacent Work | draft | 1,745 | 8 | 1 | 110 | 11838 | <https://kriskrug.co/wp-admin/post.php?post=11876&action=edit> |
| 11877 | I Won't Fake The People Who Showed Up | draft | 1,421 | 5 | 1 | 127 | 3252 | <https://kriskrug.co/wp-admin/post.php?post=11877&action=edit> |
| 11878 | Speak It Into Existence: Voice-First AI Workflows | draft | 1,548 | 6 | 1 | 151 | 11841 | <https://kriskrug.co/wp-admin/post.php?post=11878&action=edit> |

## Review Order

1. `The 75% Rule` - strongest first publish candidate.
2. `I Won't Fake The People Who Showed Up` - review documentary boundary language and image fit.
3. `Speak It Into Existence` - review whether naming WhisperFlow is acceptable/current enough.

## Still Human-Gated

- KK voice approval.
- Any final image swap from Flickr or a stronger documentary archive image.
- Preview QA in WordPress on desktop/mobile.
- Public scheduling decision.
- Rollback note before publish.
