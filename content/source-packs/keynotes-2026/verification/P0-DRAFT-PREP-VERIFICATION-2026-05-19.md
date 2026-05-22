# P0 Speaking Draft Prep Verification - 2026-05-19

Scope: local draft prep only. No live WordPress writes, no page payload changes, no theme edits.

## Draft Folders Created

- `content/drafts/2026-05-19-both-hands-full-ai-creatives-lasalle-college/`
- `content/drafts/2026-05-19-inside-vancouvers-ai-boom-whistler-institute/`
- `content/drafts/2026-05-19-both-hands-full-vancouver-ai-march-2026/`

Each folder includes:

- `post.md`
- `post.html`
- `seo-meta.md`
- `internal-links.md`
- `alt-text.md`
- `publish-gate.md`
- one local planning thumbnail under `images/`

## Source Packages Used

- `../post-packages/both-hands-full-lasalle-college.md`
- `../post-packages/inside-vancouvers-ai-boom-whistler-institute.md`
- `../post-packages/vancouver-ai-march-2026-both-hands-full.md`

## Verification Commands

```bash
git status --short --branch
git rev-list --left-right --count HEAD...origin/main
find content/drafts/2026-05-19-* -maxdepth 2 -type f | sort
find content/drafts/2026-05-19-* -maxdepth 2 -type f -name '*.jpg' -print0 | xargs -0 file
git diff --check
rg -n -i "<standard source-pack sensitive-string pattern>" content/drafts/2026-05-19-*
```

## Results

- `main` was even with `origin/main` before this draft-prep lane started: `0 0`.
- Three draft folders were created with 21 tracked files.
- Three local planning thumbnails were copied from the public video intake; each is a 1280x720 JPEG.
- Path-scoped `git diff --check` passed for the new draft and source-pack/docs files.
- Sensitive-string scan across the new draft folders returned no matches.
- New draft Markdown support files total 489 lines.
- Drafts remain local and intentionally gated for KK/image/fact-check review.

## Publish Gate

Before any of these becomes a live WordPress draft or post:

- choose final WP-hosted featured images,
- confirm event naming and title tone,
- review ethical, environmental, public-official, and ecosystem claims,
- avoid transcript dumps,
- take the normal Track A page/post snapshot or other rollback note required for live writes.

## Next Best Move

Prepare the P1 support drafts:

1. Horizons produced-interview roundup.
2. ChannelNext live AI synthesis keynote recap.
3. Bass Coast Brain Stage recap.

The CBC/media appearance queue should remain research-only until public podcast and CBC sources are collected.
