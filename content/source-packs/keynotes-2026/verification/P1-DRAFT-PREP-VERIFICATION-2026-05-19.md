# P1 Speaking Draft Prep Verification - 2026-05-19

Scope: local draft prep only. No live WordPress writes, no page payload changes, no theme edits.

## Draft Folders Created

- `content/drafts/2026-05-19-horizons-ai-models-future-machine-learning/`
- `content/drafts/2026-05-19-ai-keynote-chaos-creativity-channelnext/`
- `content/drafts/2026-05-19-dear-ai-bass-coast-brain-stage/`

Each folder includes:

- `post.md`
- `post.html`
- `seo-meta.md`
- `internal-links.md`
- `alt-text.md`
- `publish-gate.md`
- local planning thumbnails under `images/`

## Source Packages Used

- `../post-packages/horizons-produced-interview-roundup.md`
- `../post-packages/channelnext-chaos-creativity-keynote.md`
- `../post-packages/dear-ai-bass-coast-brain-stage.md`

## Verification Commands

```bash
git status --short --branch
git rev-list --left-right --count HEAD...origin/main
find content/drafts/2026-05-19-horizons-ai-models-future-machine-learning content/drafts/2026-05-19-ai-keynote-chaos-creativity-channelnext content/drafts/2026-05-19-dear-ai-bass-coast-brain-stage -maxdepth 2 -type f | sort
find content/drafts/2026-05-19-horizons-ai-models-future-machine-learning content/drafts/2026-05-19-ai-keynote-chaos-creativity-channelnext content/drafts/2026-05-19-dear-ai-bass-coast-brain-stage -maxdepth 2 -type f -name '*.jpg' -print0 | xargs -0 file
git diff --check -- content/drafts/2026-05-19-horizons-ai-models-future-machine-learning content/drafts/2026-05-19-ai-keynote-chaos-creativity-channelnext content/drafts/2026-05-19-dear-ai-bass-coast-brain-stage content/source-packs/keynotes-2026 docs/current-state/NEXT-ROUND-WORK-2026-05-19.md
rg -n -i "<standard source-pack sensitive-string pattern>" content/drafts/2026-05-19-horizons-ai-models-future-machine-learning content/drafts/2026-05-19-ai-keynote-chaos-creativity-channelnext content/drafts/2026-05-19-dear-ai-bass-coast-brain-stage
```

## Results

- `main` was even with `origin/main` before this draft-prep lane started: `0 0`.
- Three draft folders were created with 23 tracked files.
- Five local planning thumbnails were added; each is a 1280x720 JPEG.
- Path-scoped `git diff --check` passed for the new draft and source-pack/docs files.
- Sensitive-string scan across the new draft folders returned no matches.
- ASCII scan across the new draft Markdown and verification files returned no matches.
- New draft Markdown support files total 458 lines.

## Publish Gate

Before any of these becomes a live WordPress draft or post:

- choose final WP-hosted featured images or embed-only media treatment,
- confirm Horizons/Compass, ChannelNext, and Bass Coast naming,
- review rights for any public YouTube planning thumbnails,
- avoid transcript dumps,
- take the normal Track A backup or page/post snapshot required for live writes.

## Next Best Move

Keep the CBC/media appearance package research-only until public podcast, CBC, and producer-page sources are collected. After that, prepare one appearance inventory post or refresh the Podcast EPK.
