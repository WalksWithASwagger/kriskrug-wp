# AURORA Swarm 83 Templates — 2026-05-20

Branch: `codex/swarm-83-work-speaking-templates-2026-05-20`  
Worktree: `/Users/kk/Code/kriskrug-wp-swarm-83`  
Issue: [#83](https://github.com/WalksWithASwagger/kriskrug-wp/issues/83)

## Scope

Track B template lane only:

- Work and Speaking media template surfaces
- reusable module structure via template parts
- mobile-safe hierarchy
- artifact proof

No Track A publishing actions. No homepage lane changes for `#82`.

## Implementation Summary

### Template surfaces

- Added `page-speaking.html` (speaking-specific template shell).
- Added `page-work.html` and page-id fallback `page-2672.html` for current Work canonical page.
- Added `page-recent-projects-include.html` to align with current URL strategy.

### Reusable components (template parts)

- Added `parts/work-proof-grid.html`:
  media-rich project modules with source captions, tags, and CTA rows.
- Added `parts/speaking-proof-grid.html`:
  reel module, keynote topic grid, testimonial cards, and event-format row.

### Shared styling (single CSS surface)

- Extended `theme/kk-aurora/style.css` with reusable classes for:
  - `.aurora-proof-grid`, `.aurora-proof-module`, `.aurora-proof-media`, `.aurora-proof-actions`
  - `.aurora-speaking-reel`, `.aurora-topic-grid`, `.aurora-quote-grid`, `.aurora-logo-row`
  - Work/Speaking hero shells and responsive collapses
- No large inline CSS was added to templates/parts.

### Theme registration

- Registered new template parts in `theme.json`:
  - `work-proof-grid`
  - `speaking-proof-grid`

## URL Strategy Note

Current local canonical Work page is `/recent-projects-include/` (page ID `2672`), while `/work/` is not a standalone page object in this Local dataset.  
This lane keeps URL behavior unchanged and implements Work modules on the current canonical page path, matching issue guidance to respect existing URL strategy until redirect decisions are approved.

## Local QA Setup

Local theme path:

- `/Users/kk/Local Sites/kriskrug-local/app/public/wp-content/themes/kk-aurora`

Backup before syncing lane theme:

- `/tmp/kk-aurora-local-before-83-20260519-190938.tgz`

Temporary same-origin host switch for smoke:

- set `home` + `siteurl` to `http://localhost:10003`
- restored to `http://kriskrug-local.local` after QA

## HTTP Smoke

Base URL used: `http://localhost:10003`

Command:

```bash
for path in / /work/ /speaking/ /about/ /recent-projects-include/ /2026/05/16/make-culture-not-content/ /2026/05/15/your-taste-is-your-moat/ /2026/05/14/calling-us-all-in/ /2026/05/07/web-summit-vancouver-2026/; do
  /usr/bin/curl -sSL -o /dev/null -w "%{http_code} ${path}\n" "http://localhost:10003${path}"
done
```

Output:

```text
200 /
200 /work/
200 /speaking/
200 /about/
200 /recent-projects-include/
200 /2026/05/16/make-culture-not-content/
200 /2026/05/15/your-taste-is-your-moat/
200 /2026/05/14/calling-us-all-in/
200 /2026/05/07/web-summit-vancouver-2026/
```

## Module Presence Checks

Validated via:

- `docs/current-state/aurora-smoke-2026-05-20/aurora-work-speaking-checks.json`

Current results:

- Work (`/recent-projects-include/`): template class present, proof grid present, source captions present, module actions present
- Speaking (`/speaking/`): speaking template class + reel/topic/quote/logo modules present
- CSS: reusable module styles, mobile collapse rules, reduced-motion guard present

## Screenshot + JSON Artifacts

All artifacts are in `docs/current-state/aurora-smoke-2026-05-20/`:

- `aurora-work-desktop.png`
- `aurora-work-mobile.png`
- `aurora-speaking-desktop.png`
- `aurora-speaking-mobile.png`
- `aurora-work-speaking-metrics.json`
- `aurora-work-speaking-checks.json`

Metrics currently show:

- desktop captures at `1440x1000`
- mobile captures at `390x844`
- overflow heuristic `false` for all four captures

## Verification Commands

```bash
git diff --check
jq empty theme/kk-aurora/theme.json
php -l theme/kk-aurora/functions.php
```

All passed.

## Lane Result

- Work and Speaking surfaces now have reusable media-first modules with explicit proof/source treatment and mobile-safe layouts.
- Template parts are registered and shared across the page templates.
- URL strategy was preserved by targeting the current Work canonical path (`/recent-projects-include/`) without introducing redirect changes.
