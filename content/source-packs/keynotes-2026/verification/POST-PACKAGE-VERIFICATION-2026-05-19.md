# Speaking Post Package Verification - 2026-05-19

Scope: source-pack only. No live WordPress writes, no page payload changes, no theme edits.

## What Changed

Created `../post-packages/` as a review-ready companion-post queue for the speaking authority network.

Packages created:

- `both-hands-full-lasalle-college.md`
- `inside-vancouvers-ai-boom-whistler-institute.md`
- `vancouver-ai-march-2026-both-hands-full.md`
- `dear-ai-bass-coast-brain-stage.md`
- `channelnext-chaos-creativity-keynote.md`
- `horizons-produced-interview-roundup.md`
- `cbc-ai-sandbox-and-appearance-queue.md`
- `README.md`

The source-pack index, video-research index, and next-round command sheet now point to the package directory.

## Safety Verification

Commands run from repo root:

```bash
git status --short --branch
git rev-list --left-right --count HEAD...origin/main
git diff --check
rg -n -i "<standard source-pack sensitive-string pattern>" content/source-packs/keynotes-2026/post-packages
find content/source-packs/keynotes-2026/post-packages -maxdepth 1 -type f | sort
wc -l content/source-packs/keynotes-2026/post-packages/*.md
```

Results:

- `main` was even with `origin/main` before edits: `0 0`.
- `git diff --check` passed.
- Sensitive-string scan returned no matches.
- Package directory contains 8 Markdown files, 509 total lines.

## Publish Gate

Before any package becomes a WordPress draft:

- choose a final WP-hosted image or approved embed,
- review named people, audience comments, client/event claims, and public-source links,
- avoid raw transcript dumps,
- create or update the WP draft only after the normal Track A slug checks and snapshot/rollback notes are satisfied.

## Best Next Move

Turn the P0 packages into actual local draft folders first:

1. `both-hands-full-lasalle-college.md`
2. `inside-vancouvers-ai-boom-whistler-institute.md`
3. `vancouver-ai-march-2026-both-hands-full.md`

Those three create the strongest immediate authority spine for `/speaking/`: creative keynote, BC ecosystem keynote, and community-stage proof.
