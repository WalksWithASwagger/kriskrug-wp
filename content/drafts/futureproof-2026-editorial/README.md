# Futureproof: Year One

Published November 1, 2026: [read the feature](https://kriskrug.co/2026/11/01/futureproof-2026-year-one/).
This package records the final published article for [#1165](https://github.com/WalksWithASwagger/kriskrug-wp/issues/1165), replacing the earlier short recap. Kris authorized the editorial refinement, publication and indexing submissions in the publication session, then requested repository closeout.

## Source of truth

- `post.html` is the exact Gutenberg body read back from WordPress post **12934**.
- `post.md` is a Markdown rendering of that body with the publication metadata.
- `media.json` records the twelve existing public WordPress images, credits, captions and alt text. Nine photographs are by Michelle Diamond / Diamond’s Edge Photography; three presentation images are from Amber Case and Jacob Ortiz. No image binaries or private source material are included.
- Featured image: existing media **12935**. Author: **1**, Kris Krüg. Category: **1662**, Vancouver AI Ecosystem. No new tags.
- Slug: `futureproof-2026-year-one`. Publication: `2026-11-01T14:52:04` local / `2026-11-01T22:52:04Z`.
- Body SHA-256: `a972362c4c0a22e74edf70dfe73cefb1e60f72da800f9de37701652c42ac9fc3`.

The exact saved body includes the AI-assistance disclosure, five contextual internal links, the released festival gallery and program, and a linked photography credit. The current body links separately to the 2026 proceedings. The post uses its own canonical URL and the existing BlogPosting/Person schema.

## Release verification

November 1 provider and public readback confirmed:

- Status `publish`, matching post ID, slug, body, author, category and featured media.
- HTTP 200, one H1, correct canonical, SEO title and description, and social-preview image.
- All twelve images have alt text, dimensions and responsive sources. Slides link to full-size images.
- Article included in the WordPress post sitemap and RSS feed.
- `make seo-publisher-smoke` passed, including the new article's required BlogPosting fields.
- Google Search Console confirmed **Indexing requested** and a priority crawl queue entry.
- The IndexNow global endpoint accepted the URL with **HTTP 200** after the existing ownership key was verified.

Submission is confirmed; completed search-engine indexing is not yet confirmed. Do not repeat submissions solely because indexing is pending.

## Future maintenance

This is a published snapshot, not a create-new-draft input. Do not run the create-only draft publisher against it or upload these images again. Any later authorized update must verify that the slug still resolves uniquely to post **12934**, capture a fresh private rollback snapshot, review the body diff, and verify both authenticated and public readback afterward.

Private quote/source checks, before/after snapshots, screenshots and submission receipts remain in the publication session's evidence package outside this repository. The release changed content and media metadata only; it did not deploy theme, plugin or snippet code.
