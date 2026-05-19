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

## Minimum safety steps before live publish

1. Run connector `--dry-run` first.
2. Confirm slug and title are the intended target.
3. Review excerpt/meta, categories/tags, and internal links.
4. Confirm image rights + alt text quality.
5. Use backup/page-snapshot discipline from `docs/current-state/BACKUP_PLAN.md`.

## Quick readiness checklist (per draft)

- [ ] No placeholder values (`TBD`, draft-status notes, editorial TODO blocks).
- [ ] `seo-meta.md` reflects final title/description intent.
- [ ] `internal-links.md` has intentional internal links (not empty by accident).
- [ ] Images are approved and suitable for live upload.
- [ ] Category mapping is intentional (not silent fallback to `Misc` unless deliberate).

## Related docs

- `scripts/notion-to-wp/README.md`
- `docs/current-state/NEXT-PUBLISHING-PLAN-2026-05-18.md`
- `docs/current-state/POST-DRAFT-BACKLOG-AUDIT-2026-05-18.md`
