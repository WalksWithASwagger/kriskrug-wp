# Draft Quality Reset - 2026-05-22

**Purpose:** correct the draft-publishing workflow after the first StoryHive/keynote WP draft pass produced reviewable artifacts, not publish-ready posts.
**Scope:** Track A content + SEO only. No theme work.
**Status:** active quality gate before any scheduling or publish run.

## Live WordPress Queue Truth

Authenticated REST check on 2026-05-22:

| Surface | Future | Draft | Pending | Private |
|---|---:|---:|---:|---:|
| Posts | 0 | 42 | 0 | 0 |
| Pages | 0 | 5 | 0 | 0 |

There is no scheduled release queue in WordPress right now. The site has a draft pile.

Current meaning of the WP drafts:

- 10 draft posts and 2 draft pages were created during the May 21-22 create-only draft pass.
- The older 32 draft posts and 3 draft pages remain an admin rescue/backlog pile, not a release calendar.
- No draft should be scheduled until it passes the quality gate below.

## What Failed

The May 21-22 draft pass treated "WP draft exists" as too much of a win.

Actual failures:

- Drafts were created as raw HTML, with zero Gutenberg block comments.
- StoryHive posts were converted from markdown without a proper block-rendering or visual QA pass.
- Keynote/media posts had source-pack context, but the media plan was not carried into WordPress.
- No WP draft has an image or featured image from this pass.
- The internal-link files were not treated as a mandatory in-body linking pass.
- The quality gate checked create-only safety and slug/status basics, not editorial readiness.
- There was no schedule decision layer after draft creation.

This means the drafts are allowed to exist as workbench objects, but they are not release-ready.

## Newly Created WP Drafts

Authenticated REST metrics on 2026-05-22:

| WP ID | Slug | Words | Links | Images | Embeds | Headings | Blocks | Status |
|---:|---|---:|---:|---:|---:|---:|---:|---|
| 11876 | `the-75-percent-rule-ai-art-adjacent-work` | 1621 | 5 | 0 | 0 | 7 | 0 | Needs rebuild |
| 11877 | `i-wont-fake-the-people-who-showed-up` | 1403 | 5 | 0 | 0 | 7 | 0 | Needs rebuild |
| 11878 | `speak-it-into-existence-ai-voice-first-workflows` | 1469 | 5 | 0 | 0 | 8 | 0 | Needs rebuild |
| 11879 | `ai-media-appearances-podcast-guesting` | 663 | 19 | 0 | 1 | 6 | 0 | Needs media/layout |
| 11880 | `ai-keynote-chaos-creativity-channelnext` | 476 | 4 | 0 | 1 | 5 | 0 | Needs expansion/media |
| 11881 | `both-hands-full-ai-creatives-lasalle-college` | 736 | 4 | 0 | 1 | 6 | 0 | Needs expansion/media |
| 11882 | `both-hands-full-vancouver-ai-march-2026` | 540 | 4 | 0 | 1 | 5 | 0 | Needs expansion/media |
| 11883 | `dear-ai-bass-coast-brain-stage` | 410 | 4 | 0 | 1 | 5 | 0 | Needs expansion/media |
| 11884 | `horizons-ai-models-future-machine-learning` | 474 | 4 | 0 | 3 | 5 | 0 | Needs expansion/media |
| 11885 | `inside-vancouvers-ai-boom-whistler-institute` | 638 | 4 | 0 | 1 | 6 | 0 | Needs expansion/media |
| 11886 | `accessibility` | 645 | 1 | 0 | 0 | 7 | 0 | Page QA required |
| 11887 | `glossary` | 1776 | 24 | 0 | 0 | 22 | 0 | Page QA required |

The counts prove the main issue: body copy exists, but the posts do not yet have visual treatment, block-native formatting, or enough editorial polish to schedule.

## Draft Quality Gate

Before any WP draft is scheduled, it must pass all of this:

1. **Editorial voice pass**
   - Strong KK opening.
   - No filler recap framing unless the post intentionally needs it.
   - Thought-leadership argument is clear in the first screen.
   - Sassy/swagger lines are earned, not pasted in.

2. **Formatting pass**
   - Gutenberg-compatible blocks or clean block editor rendering verified in wp-admin.
   - No markdown artifacts.
   - No weird line wrapping, orphan headings, or accidental walls of short paragraphs.
   - Headings form a skimmable argument.

3. **Link pass**
   - At least 3 intentional internal links for normal posts.
   - External links are purposeful and checked.
   - Supporting source links are attached to claims, names, projects, videos, or events.
   - No Notion/private/local-only links.

4. **Image/media pass**
   - Every publish candidate has a featured image unless there is an explicit text-only decision.
   - Documentary/community/talk posts should prefer Kris-owned images, Flickr, WP media, or source-pack media over generic generated imagery.
   - Generated images are acceptable for abstract idea posts only when documentary truth is not implied.
   - Every image needs alt text, credit/source notes where needed, and a media-library ID after upload.

5. **SEO/meta/taxonomy pass**
   - Slug, title, excerpt, meta description, category, and tags are deliberate.
   - No accidental `Misc`.
   - No empty slug.
   - No duplicate/conflicting live post without a decision.

6. **Preview pass**
   - Preview opened in WordPress.
   - Mobile/desktop visual scan done.
   - Featured image, embeds, headings, links, and CTA checked.
   - Publish date chosen only after preview passes.

## Image Sourcing Pipeline

Use this order for draft imagery:

1. Search existing WP media by event/person/project keywords.
2. Search repo source packs and local draft `images/` folders.
3. Search Kris's Flickr/public photo archive for matching documentary or event images.
4. Use YouTube thumbnails only when the post is clearly about the talk/video and the thumbnail has enough quality.
5. Generate an image only for abstract posts where a generated visual will not be mistaken for documentary evidence.

Required output per post:

- featured image candidate,
- optional inline image candidates,
- alt text,
- source/credit note,
- upload/set-featured plan,
- backup option if the image fails licensing, quality, or fit.

## Queue Status

### Not Scheduled

No posts or pages are currently scheduled in WordPress.

### Workbench Drafts

The May 21-22 StoryHive/keynote drafts are useful as raw material only. They should be rebuilt or updated in place after passing the gate.

### Local Review Packs

Local draft packs with stronger prep still exist under `content/drafts/`, including:

- `2026-05-13-sovereign-ai-for-whom/`
- `2026-05-16-why-we-built-the-responsible-ai-professional-certification/`
- `2026-05-06-comox-valley-ai-is-becoming-its-own-thing/`
- `2026-05-19-*` keynote/media packs
- `2026-05-21-*` StoryHive idea packs

The May 18 plan still applies:

- `sovereign-ai-for-whom` is the strongest local next candidate, but needs fact-check, category, formatting, links, and image review.
- the RAP follow-up needs duplicate/conflict review against the live RAP post.
- the Comox Valley piece needs TODO removal, images, internal links, and category cleanup.

### Admin Backlog

The older WordPress admin draft queue remains untriaged. Do not treat it as a schedule. It needs a separate rescue audit before any item is promoted.

## Recommended Rescue Order

1. Pick one StoryHive post to rebuild properly, not all three at once. Recommended first rescue: `the-75-percent-rule-ai-art-adjacent-work`.
2. Add real internal/external links and a strong image plan.
3. Rebuild/update the WP draft with block-clean formatting.
4. Open the WP preview and capture QA notes.
5. Only then schedule one post.
6. Repeat for the next StoryHive post after the first one proves the improved pipeline.

Do not batch-create more WP drafts until one draft has gone all the way from local source to preview-approved schedule.
