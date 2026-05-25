# Draft Queue Audit - 2026-05-22

**Purpose:** durable inventory for the kriskrug.co draft queue after the StoryHive/keynote draft quality reset.
**Track:** Track A content + SEO.
**Status:** active publishing triage artifact.
**2026-05-25 addendum:** `sovereign-ai-for-whom` exists as WordPress draft `11905` with featured media `11899`. `make draft-queue-audit` now reports 0 future posts, 71 draft posts, and 5 draft pages.

## Verdict

There is no scheduled release queue in WordPress right now. There is a draft pile.

Authenticated read-only WordPress REST checks normalized on 2026-05-25 show:

| Surface | Future | Draft | Pending | Private |
|---|---:|---:|---:|---:|
| Posts | 0 | 71 | 0 | 0 |
| Pages | 0 | 5 | 0 | 0 |

The strongest near-term publishing path is:

1. Review `Sovereign AI for Whom?` as WP draft `11905`; do not create a duplicate.
2. Schedule only one proof post after KK review, likely `The 75% Rule`.
3. Prep `Comox Valley AI Is Becoming Its Own Thing` after image/category cleanup.
4. Hold the RAP post until duplicate/replacement positioning is decided.
5. Rebuild the best speaking-authority posts from the May 19 source drafts, starting with LaSalle, Whistler Institute, and Vancouver AI March 2026.

## Refresh Command

Run this read-only command before changing the publishing queue:

```bash
scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/draft_queue_audit.py
```

For local package metrics only:

```bash
scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/draft_queue_audit.py --local-only
```

The audit command checks local `content/drafts/` packages, live WP draft/future/pending/private counts, existing WP draft metrics, and exact slug matches across published and draft posts/pages.

## Local Draft Packages

| Package | WP match | State | Needed |
|---|---|---|---|
| `sovereign-ai-for-whom` | WP post `11905` draft | Reviewable heavyweight draft: 4,110 local words, 80 links, 6 images, 110 blocks | KK source/voice review, desktop/mobile preview QA, no duplicate draft |
| `the-75-percent-rule-ai-art-adjacent-work` | WP post `11876` draft | Reviewable StoryHive draft: 1,793 local words, 9 links, 1 image, 110 blocks | KK title/frame approval, preview QA, stronger image pass, schedule decision |
| `i-wont-fake-the-people-who-showed-up` | WP post `11877` draft | Reviewable StoryHive draft: 1,462 local words, 6 links, 1 image, 127 blocks | Decide standalone vs merge, documentary-boundary review, preview QA |
| `speak-it-into-existence-ai-voice-first-workflows` | WP post `11878` draft | Reviewable StoryHive draft: 1,597 local words, 7 links, 1 image, 151 blocks | Tool-specific vs evergreen decision, CTA check, neurodivergent framing review |
| `comox-valley-ai-is-becoming-its-own-thing` | no WP slug match | Strong body, no media: 3,105 words, 7 links, 105 blocks | Clean draft-status copy, add images/internal links, category/meta cleanup, fact check |
| `why-we-built-the-responsible-ai-professional-certification` | no WP slug match | Useful but duplicate-risk: 1,282 words, 11 links, 13 images, 71 blocks | Compare against existing RAP post, remove/replace private links, category/meta/alt pass |
| `web-summit-vancouver-2026` | WP post `11826` published | Already live | Do not duplicate; use for backlinks/source context |
| `calling-us-all-in` | WP post `11765` published | Already live | Do not duplicate; use for backlinks/source context |
| `ai-media-appearances-podcast-guesting` | WP post `11879` draft | Thin WP support draft: 759 local words, 19 links, no images/blocks in WP | Featured image or embeds-only decision, source-link check, speaking/EPK alignment |
| `ai-keynote-chaos-creativity-channelnext` | WP post `11880` draft | Thin source draft: 486 words, 4 links, 1 source image, no blocks in WP | Expand, image, block rebuild |
| `both-hands-full-ai-creatives-lasalle-college` | WP post `11881` draft | High-priority speaking post, but thin: 749 words, 4 links, 1 source image, no blocks in WP | Expand, image, block rebuild |
| `both-hands-full-vancouver-ai-march-2026` | WP post `11882` draft | High-priority speaking post, but thin: 554 words, 4 links, 1 source image, no blocks in WP | Expand, image, block rebuild |
| `dear-ai-bass-coast-brain-stage` | WP post `11883` draft | Hold: 424 words, 4 links, 1 source image, no blocks in WP | Expand only after media/event naming are cleared |
| `horizons-ai-models-future-machine-learning` | WP post `11884` draft | Produced-interview proof: 488 words, 4 links, 3 source images, no blocks in WP | Confirm embeds/images; likely support post |
| `inside-vancouvers-ai-boom-whistler-institute` | WP post `11885` draft | High-priority speaking post, but thin: 644 words, 4 links, 1 source image, no blocks in WP | Expand, fact-check, image, block rebuild |
| `accessibility-statement-2026-05` | WP page `11886` draft | Page project, not blog queue | Accessibility/legal/editorial review, QA, footer-link gate |
| `ai-glossary-2026-05` | WP page `11887` draft | Page project, not blog queue | Sensitive-term review, search/filter decision, accessibility/mobile QA |

## WordPress Draft Queue Notes

Newer WP drafts:

| WP ID | Slug | Words | Links | Images | Blocks | Featured media | Status |
|---:|---|---:|---:|---:|---:|---:|---|
| 11876 | `the-75-percent-rule-ai-art-adjacent-work` | 1,719 | 8 | 1 | 110 | 11838 | Reviewable, not schedule-ready |
| 11877 | `i-wont-fake-the-people-who-showed-up` | 1,414 | 5 | 1 | 127 | 3252 | Reviewable, not schedule-ready |
| 11878 | `speak-it-into-existence-ai-voice-first-workflows` | 1,530 | 6 | 1 | 151 | 11841 | Reviewable, not schedule-ready |
| 11879 | `ai-media-appearances-podcast-guesting` | 647 | 19 | 0 | 0 | 0 | Needs media/layout |
| 11880 | `ai-keynote-chaos-creativity-channelnext` | 471 | 4 | 0 | 0 | 0 | Needs expansion/media |
| 11881 | `both-hands-full-ai-creatives-lasalle-college` | 733 | 4 | 0 | 0 | 0 | Needs expansion/media |
| 11882 | `both-hands-full-vancouver-ai-march-2026` | 539 | 4 | 0 | 0 | 0 | Needs expansion/media |
| 11883 | `dear-ai-bass-coast-brain-stage` | 408 | 4 | 0 | 0 | 0 | Hold until stronger |
| 11884 | `horizons-ai-models-future-machine-learning` | 470 | 4 | 0 | 0 | 0 | Needs embeds/image decision |
| 11885 | `inside-vancouvers-ai-boom-whistler-institute` | 629 | 4 | 0 | 0 | 0 | Needs expansion/fact-check/media |
| 11886 | `accessibility` | 632 | 1 | 0 | 0 | 0 | Page QA required |
| 11887 | `glossary` | 1,755 | 24 | 0 | 0 | 0 | Page QA/search review required |
| 11905 | `sovereign-ai-for-whom` | 3,706 | 80 | 6 | 110 | 11899 | Reviewable, high-stakes source/voice review required |

Older admin draft rescue candidates:

| WP ID | Title | Current signal | Before promotion |
|---:|---|---|---|
| 6348 | `The AI Mindset: Adapting to the New Creative Paradigm` | 1,933 words, 11 links, 12 images | Slug/category/featured image, voice review, duplicate check |
| 8021 | `End of the Tech Bro Kingdom: How AI Might (Finally) Let Us All Code` | 2,466 words, 9 links | Slug/category/featured image, freshness check |
| 6386 | `Future Proof Creatives: The No-BS Guide to Mastering AI Trends & Tools` | 2,461 words, 148 blocks | Links/media, title/style review |
| 8661 | `THE AI-POWERED JOURNALIST: LEADING THE 2025 GNI AI JOURNALISM LAB` | 2,215 words, 60 blocks | Slug/category/featured image, date relevance |
| 6183 | `AI Mastery: It's About the Ears, Not the Years` | 1,903 words, 56 blocks | Links/media/category, title polish |
| 2749 | `Future In Review Podcast` | 1,540 words, 34 links, 118 blocks | Media, category, current relevance |
| 11061 | `From Google News Initiative to TheUpgrade.ai: The Origin Story We Never Told` | 1,304 words, 86 blocks | Links/media/category, strategic positioning |

Everything else in the older admin draft pile should stay rescue-later, hold, or kill until it gets a separate editorial decision.

## Promotion Gate

Do not schedule a draft until it passes all of this:

1. **Voice:** strong KK opening, no generic recap framing, clear first-screen argument.
2. **Format:** Gutenberg block-clean body, no markdown artifacts, no orphan headings, no accidental walls of micro-paragraphs.
3. **Links:** at least 3 deliberate internal links for normal posts, checked source links, no Notion/private/local URLs.
4. **Media:** featured image or explicit text-only decision, alt text, source/credit note, and media-library ID after upload.
5. **Taxonomy/meta:** deliberate title, slug, excerpt, meta description, category, and tags; no accidental `Misc`.
6. **Safety:** exact slug/ID/status check before any WP update; no public publish without KK approval.
7. **Preview:** wp-admin preview opened on desktop and mobile before schedule.

## Recovery Order

1. **Sovereign AI for Whom?**
   - Local prep pass completed: opening, meta, category, alt text, and HTML alt bug fixed.
   - Fact-check and publish gates added in `content/drafts/2026-05-13-sovereign-ai-for-whom/`.
   - Guarded WordPress draft `11905` now exists with featured media `11899`.
   - Remaining gate: verify direct stage quotes before restoring them, 150 West Georgia municipal status before stronger wording, TELUS sustainability paperwork, and BC + AI internal metrics.
   - Do not create another draft; review `11905` in wp-admin and schedule only after KK approval.

2. **StoryHive proof post**
   - Recommended first proof: `The 75% Rule`.
   - Upgrade image candidate from WP/Flickr/archive if a stronger match exists.
   - Preview and schedule only this one post first.

3. **Comox Valley AI**
   - Replace draft-status copy with real excerpt/meta.
   - Add imagery and internal links.
   - Confirm attendance, names, and local chapter framing.

4. **RAP certification**
   - Compare against the existing live RAP/certification post.
   - Decide replacement, update, or distinct follow-up before creating a new WP draft.

5. **Speaking authority rebuilds**
   - Expand and rebuild LaSalle, Whistler Institute, and Vancouver AI March first.
   - Treat Horizons as produced-interview proof.
   - Hold Bass Coast until media/event naming is cleared.

## Verification Commands

Completed during this implementation pass:

```bash
git fetch --prune
git rev-list --left-right --count HEAD...@{upstream}
scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/draft_queue_audit.py
scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/draft_queue_audit.py --local-only --format json
scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/create_local_wp_draft.py --dry-run content/drafts/2026-05-13-sovereign-ai-for-whom/post.md
scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/create_local_wp_draft.py --execute content/drafts/2026-05-13-sovereign-ai-for-whom/post.md
scripts/notion-to-wp/.venv/bin/python -m unittest scripts/notion-to-wp/tests/test_draft_queue_audit.py
scripts/notion-to-wp/.venv/bin/python -m unittest discover scripts/notion-to-wp/tests
```

Acceptance notes:

- Local `main` was even with `origin/main` before implementation.
- The audit command is read-only.
- Published collisions are surfaced, including `web-summit-vancouver-2026` and `calling-us-all-in`.
- The command tolerates imperfect draft frontmatter with unquoted colons.
- `Sovereign AI for Whom?` WP readback verified status `draft`, slug `sovereign-ai-for-whom`, 6 images, 110 blocks, no local image paths, and no restored high-risk stale phrases.
- Unrelated WP7 working-tree files were left untouched.
