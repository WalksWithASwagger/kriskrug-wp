# Futureproof: what happens after the applause

Manuscript package for [#1165](https://github.com/WalksWithASwagger/kriskrug-wp/issues/1165).
`post.md` contains the manuscript and metadata; `post.html` is the equivalent
Gutenberg body for the existing local draft publisher. Both include the
AI-assistance disclosure. This package has no media attachments.

## Publication metadata

- Author: Kris Krüg, existing WordPress author ID `1`.
- Category: existing **Vancouver AI Ecosystem** (`1662`); no new tags.
- Slug: `futureproof-2026-what-happens-after-the-applause`.
- Status: `draft`. No WordPress draft has been created by this preparation.
- Title, excerpt and SEO description are in `post.md`.
- Date and canonical URL are unset. The intended permalink shape is
  `/YYYY/MM/DD/futureproof-2026-what-happens-after-the-applause/`, using the actual
  publication date returned by WordPress.
- Reuse the site's existing Person and BlogPosting schema, sitemap and feed.
  The body adds no schema or cross-domain canonical.

The two contextual links point to the released festival gallery and program.
They are not described as completed proceedings. Additional editorial links and
photographs require separate selection; this text remains unchanged meanwhile.

## Validation and later publication

Run the existing publisher in dry-run mode:

```sh
python3 scripts/notion-to-wp/create_local_wp_draft.py content/drafts/futureproof-2026-editorial/post.md --dry-run
```

That command validates the local package but reports `slug_check: skipped_offline`.
Before any separately authorized WordPress creation, repeat authenticated
post/page slug checks and review the exact payload. Use create-only draft mode,
record the resulting ID and edit URL, and inspect actual WordPress rendering
before publication. A draft can be returned to trash by its verified ID if
creation must be reversed. Never update a pre-existing post to make this draft.

Publication, media uploads and Events-page changes remain separate operations.
Follow [the publisher runbook](../../../scripts/notion-to-wp/README.md) for
approval, snapshots, rollback and public readback. Keep #1165 open for its
remaining editorial and publication-preparation requirements.
