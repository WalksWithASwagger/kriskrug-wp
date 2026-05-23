# Draft Post Staging (`content/drafts/`)

This directory is the Track A staging area for post and page draft packages before live WordPress writes.

## What goes here

Each draft folder is date-and-slug scoped:

- `YYYY-MM-DD-<slug>/`
- Typical artifacts:
  - `post.md`
  - `post.html`
  - `seo-meta.md`
  - `alt-text.md`
  - `internal-links.md`
  - `images/` (when media exists)

This structure is created by the Notion publisher and then edited/reviewed by humans before publication.

## What does not count as published

Files in this directory are draft artifacts only. A folder existing here does not mean the post is live.

For live status, verify against WordPress directly:

```bash
curl -ILs https://kriskrug.co/<path>/ | sed -n '1,8p'
```

## Minimum safety steps before private WP draft creation

1. Run connector/local publisher `--dry-run` first.
2. Confirm the slug is a create-only target and the title is intentional.
3. Review excerpt/meta, categories/tags, and internal links.
4. Keep status as `draft`; do not publish from the first live run.
5. Confirm image rights + alt text quality, or keep the draft image-free.
6. Record the WP post ID and edit URL in the draft package.

## Minimum safety steps before live publish or update

1. KK has reviewed the WordPress draft.
2. Slug, title, excerpt/meta, categories/tags, links, and media are final.
3. Rollback/page-snapshot discipline from `docs/current-state/BACKUP_PLAN.md` is satisfied for the blast radius.

## Quick readiness checklist (per draft)

- [ ] No placeholder values (`TBD`, draft-status notes, editorial TODO blocks).
- [ ] `seo-meta.md` reflects final title/description intent.
- [ ] `internal-links.md` has intentional internal links (not empty by accident).
- [ ] Images are approved and suitable for live upload.
- [ ] Category mapping is intentional (not silent fallback to `Misc` unless deliberate).

## Related docs

- `scripts/notion-to-wp/README.md`
- `scripts/notion-to-wp/create_local_wp_draft.py`
- `docs/current-state/NEXT-PUBLISHING-PLAN-2026-05-18.md`
- `docs/current-state/POST-DRAFT-BACKLOG-AUDIT-2026-05-18.md`
