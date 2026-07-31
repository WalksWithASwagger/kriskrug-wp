# StoryHive Draft Audit - 2026-05-22

**Purpose:** fine-toothed audit of the rebuilt StoryHive draft pipeline after KK flagged the first drafts as weak.
**Track:** Track A content + SEO.
**Verdict:** review-ready, not schedule-ready.

## Assumptions

- These posts are evergreen idea posts grown from the StoryHive interview, not a recap of the broadcast.
- WordPress drafts are allowed for review, but no public publish or schedule happens without KK approval.
- Existing WordPress media is acceptable for review placeholders; a stronger Flickr/archive image pass can still happen before scheduling.

## Findings

No publish blockers remain for draft review.

Issues found during this audit and fixed:

- The local `source_pack` frontmatter still carried stale absolute `/Users/...` KB paths from the first pass. Replaced with `WalksWithASwagger/kk-kb` plus portable repo-relative paths.
- The draft-prep gate only checked public body copy for private/source markers. Tightened it to also fail if frontmatter contains absolute local paths.
- Live WordPress readback showed draft `11876` still contained stale source-note text after the first rebuild. Re-ran the guarded updater and confirmed the live WP body is now clean.

## Live WordPress Queue Truth

Authenticated REST check on 2026-05-22:

| Surface | Future | Draft | Pending | Private |
|---|---:|---:|---:|---:|
| Posts | 0 | 42 | 0 | 0 |
| Pages | 0 | 5 | 0 | 0 |

There is still no scheduled release queue. These are review drafts only.

## Rebuilt Draft Readback

Authenticated WordPress readback after the guarded update:

| WP ID | Title | Status | Words | Links | Images | Blocks | Featured media | Markers |
|---:|---|---|---:|---:|---:|---:|---:|---|
| 11876 | The 75% Rule: Send AI After The Art-Adjacent Work | draft | 1,745 | 8 | 1 | 110 | 11838 | none |
| 11877 | I Won't Fake The People Who Showed Up | draft | 1,421 | 5 | 1 | 127 | 3252 | none |
| 11878 | Speak It Into Existence: Voice-First AI Workflows | draft | 1,548 | 6 | 1 | 151 | 11841 | none |

All three are in category `AI for Creatives` and remain `draft`.

## Local Package Truth

Each StoryHive draft package now contains:

- `post.md` - source markdown with portable provenance.
- `post.html` - generated Gutenberg block HTML.
- `alt-text.md` - selected media and alt text.
- `internal-links.md` - link audit.
- `seo-meta.md` - title, meta, excerpt, category, tags, search intent, and checks.
- `publish-gate.md` - WP ID, readback, human review, source safety, WP safety, and media gate.

The current review packet is:

- [review-ready-drafts-2026-05-22.md](../../content/source-packs/storyhive-2026/review-ready-drafts-2026-05-22.md)

## Process Gate

`scripts/notion-to-wp/prepare_review_draft.py` is now the required local path for markdown-origin review drafts.

It does this before WordPress review:

- parses frontmatter and body;
- generates block-clean `post.html`;
- checks minimum words, links, image/featured-media presence, weak AI-copy phrases, draft-local links, private/source body markers, and absolute local frontmatter paths;
- optionally updates an existing WordPress draft only after slug, draft status, and title-similarity checks.

## Verification

Commands run:

```bash
git fetch --prune
git status --short --branch
git rev-list --left-right --count HEAD...@{upstream}
scripts/notion-to-wp/.venv/bin/python -m unittest discover scripts/notion-to-wp/tests
scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/prepare_review_draft.py content/drafts/2026-05-21-the-75-percent-rule-ai-art-adjacent-work/post.md --no-write --fail-on-warning
scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/prepare_review_draft.py content/drafts/2026-05-21-i-wont-fake-the-people-who-showed-up/post.md --no-write --fail-on-warning
scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/prepare_review_draft.py content/drafts/2026-05-21-speak-it-into-existence-ai-voice-first-workflows/post.md --no-write --fail-on-warning
git diff --check
scripts/notion-to-wp/.venv/bin/python -m py_compile scripts/notion-to-wp/prepare_review_draft.py
```

Results:

- `main` was synced with `origin/main` before audit work began.
- Connector/review-draft tests: 14 passed.
- All three draft packages passed the review gate.
- `git diff --check` passed.
- `prepare_review_draft.py` compiled cleanly.
- Live WordPress readback confirmed clean draft status, featured media, body counts, block counts, and no public-body private/source markers.

## Roadmap From Here

1. **KK editorial review**
   - Review the three WordPress drafts in this order: `11876`, `11877`, `11878`.
   - Mark each as approve, revise, kill, or merge.

2. **Image upgrade pass**
   - Use existing WP media as acceptable review placeholders.
   - Before scheduling, do a stronger Flickr/archive search for each keeper post, especially the documentary ethics piece.

3. **Preview QA**
   - Open each WP preview on desktop and mobile.
   - Check hero image crop, in-body image, headings, links, excerpt, category, tags, and CTA.

4. **Schedule one proof post**
   - Recommended first scheduled post: `The 75% Rule`.
   - Schedule only one post first so the improved pipeline proves itself end to end.

5. **Backlink and internal-link pass**
   - After the first post is live, replace any future cross-draft references with live URLs.
   - Add backlinks from `Both Hands Full`, `Make Culture, Not Content`, and relevant speaking/workshop pages.

6. **Draft queue triage**
   - Keep the broader WordPress draft pile out of the schedule until each candidate passes this same gate.
   - Next best candidates remain `Sovereign AI for Whom?`, RAP follow-up, and Comox Valley after their own fact-check/image/link passes.

7. **Release cadence**
   - Once the first proof post survives preview and review, move to one or two scheduled posts per week.
   - Do not batch-create more WP drafts until the end-to-end review -> preview -> schedule loop is boring.
