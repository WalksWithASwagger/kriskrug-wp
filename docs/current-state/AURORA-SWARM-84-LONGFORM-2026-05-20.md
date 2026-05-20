# AURORA Swarm 84 Long-Form Templates - 2026-05-20

Branch: `codex/swarm-84-longform-templates-2026-05-20`
Worktree: `/Users/kk/Code/kriskrug-wp-swarm-84`
Issue: [#84](https://github.com/WalksWithASwagger/kriskrug-wp/issues/84)

## Scope

Track B single-post template lane only:

- `theme/kk-aurora/templates/single.html`
- tightly related Aurora CSS/JS under `theme/kk-aurora/assets/`
- this evidence note

No production WordPress writes. No Track A content payload edits. No Aurora merge to `main`.

## Implementation Summary

### Reading system

- Kept the article content column at a comfortable `720px` while allowing images, galleries, embeds, and pullquotes to breathe wider.
- Added stronger hierarchy and rhythm for long-form `h2`, `h3`, paragraphs, lists, quotes, pullquotes, figures, captions, and embeds.
- Added mobile rules so wide media collapses back inside the viewport instead of forcing horizontal scroll.

### Metadata and proof

- Preserved dynamic WordPress date, category, and author blocks in the post header.
- Added client-side read-time calculation from rendered article body text at 225 words/minute; it stays hidden when the article body is unavailable or too short.
- Added a short proof-trail line in the header to set author/archive context without requiring unreliable custom fields.

### Optional navigation and motion safety

- Added an optional collapsed `Article map` details block populated from rendered `h2`/`h3` headings only when at least three section headings exist.
- Updated anchor scrolling to respect `prefers-reduced-motion`.
- Disabled the reading progress helper and hid the progress bar for reduced-motion users.

## Draft Pack Evidence

Static block-shape checks were run against the locally available issue references:

| Surface | Local evidence | Stressors present |
|---|---|---|
| Web Summit Vancouver 2026 | `content/drafts/2026-05-07-web-summit-vancouver-2026/post.html` | 10 images/figures, 13 headings, 2 quotes, 1 list |
| Calling Us All In | `content/drafts/2026-05-14-calling-us-all-in/post.html` | 6 images/figures, 9 headings, 3 quotes |
| Make Culture | `content/drafts/wp-draft-10594-post-10594/post-body.html` | ~3.4k words, 23 headings, 17 lists, 5 quotes, 1 figure |
| Your Taste / judgment draft | `content/drafts/wp-draft-11178-post-11178/post-body.html` | ~2k words, 9 headings, 2 lists, 2 quotes |

The named published "Your Taste is Your Moat" pack was not present by that title in this worktree; the closest local draft evidence is post `11178`, titled `Why Judgment Beats "Creativity" in the AI Era`, which exercises the same long-form judgment/taste structure but not media-heavy blocks.

## Local QA Setup

Local WordPress was reachable at `http://localhost:10003` during this lane. The local theme directory was a normal directory, not a symlink:

- `/Users/kk/Local Sites/kriskrug-local/app/public/wp-content/themes/kk-aurora`

Before syncing this lane's theme into Local, preserve the existing local theme:

```bash
tar -czf /tmp/kk-aurora-local-before-84-20260520.tgz -C "/Users/kk/Local Sites/kriskrug-local/app/public/wp-content/themes" kk-aurora
```

## Verification Commands

```bash
git diff --check
php -l theme/kk-aurora/functions.php
node --check theme/kk-aurora/assets/js/theme.js
jq empty theme/kk-aurora/theme.json
make validate
```

Status:

- `git diff --check`: passed
- `php -l theme/kk-aurora/functions.php`: passed
- `node --check theme/kk-aurora/assets/js/theme.js`: passed
- `jq empty theme/kk-aurora/theme.json`: passed
- `make validate`: blocked because `phpcs` is not installed in this environment

## Browser / Local WP Status

Final local smoke was run after rebasing onto `origin/aurora/v2` at PR `#103`.

Base URL used during smoke:

`http://localhost:10003`

HTTP results:

```text
200 /2026/05/16/make-culture-not-content/
200 /2026/05/15/your-taste-is-your-moat/
200 /2026/05/14/calling-us-all-in/
200 /2026/05/07/web-summit-vancouver-2026/
```

Rendered checks:

- Article shell, prose region, proof line, read-time node, article map, featured-media block, and reading-progress node were present on all four local posts.
- Read time was visible on all four local posts (`7-10 min read`).
- Article map was visible on all four local posts with `9-12` generated links.
- Desktop overflow heuristic returned `false` for all four local posts.
- Reduced-motion emulation hid the reading progress bar and preserved the prose surface.

Artifacts:

- `docs/current-state/aurora-smoke-2026-05-20/aurora-longform-checks.json`
- `docs/current-state/aurora-smoke-2026-05-20/aurora-longform-makeCulture-desktop.png`
- `docs/current-state/aurora-smoke-2026-05-20/aurora-longform-makeCulture-mobile.png`
- `docs/current-state/aurora-smoke-2026-05-20/aurora-longform-callingUsAllIn-desktop.png`
- `docs/current-state/aurora-smoke-2026-05-20/aurora-longform-callingUsAllIn-mobile.png`

Local media caveat:

- The Local WordPress database contains some hardcoded `http://localhost/...` media URLs without the Local port, and several referenced upload files are unavailable in this local dataset.
- The #84 screenshots therefore prove layout, hierarchy, metadata, article map, read-time, reduced-motion, and no-overflow behavior, but they do not prove final production media availability.
- Final media availability stays in the #86 staging QA gate.
