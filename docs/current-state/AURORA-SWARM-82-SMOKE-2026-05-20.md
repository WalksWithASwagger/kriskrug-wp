# AURORA Swarm 82 Smoke — 2026-05-20

Branch: `codex/swarm-82-media-homepage-2026-05-20`  
Worktree: `/Users/kk/Code/kriskrug-wp-swarm-82`  
Issue: [#82](https://github.com/WalksWithASwagger/kriskrug-wp/issues/82)

## Scope

Track B homepage lane only (`#82`):

- media-led first viewport
- CTA hierarchy
- responsive crop + fallback behavior
- smoke artifacts

No `#83` template work and no Track A publishing changes.

## What Changed

1. Updated hero media markup in both homepage templates to use a responsive `<picture>` source set (`w=900`, `w=1400`, `w=2200`) with meaningful alt text.
2. Added a first-viewport pathway row (`Work`, `Speaking`, `Writing`, `Project network`) to keep key routes visible without nav bloat.
3. Extended CTA hierarchy with a dedicated reel pathway (`Watch keynote reel`) while keeping `Book a keynote` as the primary action.
4. Added explicit hero media-source caption text and style support.
5. Added mobile crop tuning (`object-position: 62% 30%`) and supporting path-row/button styles in `style.css`.
6. Kept heavy autoplay off by design (no `autoplay` usage in homepage templates).

Changed files:

- `theme/kk-aurora/templates/home.html`
- `theme/kk-aurora/templates/front-page.html`
- `theme/kk-aurora/style.css`

## Local QA Setup

Local WordPress theme path:

- `/Users/kk/Local Sites/kriskrug-local/app/public/wp-content/themes/kk-aurora`

Backup before syncing this branch theme into Local:

- `/tmp/kk-aurora-local-before-82-20260519-190109.tgz`

For same-origin smoke/screenshots, local options were temporarily switched:

- `home`: `http://localhost:10003`
- `siteurl`: `http://localhost:10003`

They were restored after QA:

- `home`: `http://kriskrug-local.local`
- `siteurl`: `http://kriskrug-local.local`

## Smoke Matrix

Base URL used during smoke: `http://localhost:10003`

Command:

```bash
for path in / /about/ /speaking/ /recent-projects-include/ /2026/05/16/make-culture-not-content/ /2026/05/15/your-taste-is-your-moat/ /2026/05/14/calling-us-all-in/ /2026/05/07/web-summit-vancouver-2026/; do
  /usr/bin/curl -sSL -o /dev/null -w "%{http_code} ${path}\n" "http://localhost:10003${path}"
done
```

Output:

```text
200 /
200 /about/
200 /speaking/
200 /recent-projects-include/
200 /2026/05/16/make-culture-not-content/
200 /2026/05/15/your-taste-is-your-moat/
200 /2026/05/14/calling-us-all-in/
200 /2026/05/07/web-summit-vancouver-2026/
```

## Homepage Acceptance Checks

### Markup/pathway/CTA checks

Command:

```bash
home_html="$(
  /usr/bin/curl -sSL http://localhost:10003/
)"
for token in 'class="aurora-hero-2026"' 'class="aurora-hero-media"' 'class="aurora-path-row"' 'href="/work/"' 'href="/speaking/"' 'href="/blog/"' 'href="/recent-projects-include/"' 'class="aurora-button aurora-button-primary"' 'class="aurora-button aurora-button-secondary aurora-button-reel"' 'Photo: CreativeMornings Vancouver' 'Source: Punk Rock AI media archive'; do
  if print -r -- "$home_html" | /Applications/Codex.app/Contents/Resources/rg -q "$token"; then
    echo "PASS $token"
  else
    echo "FAIL $token"
  fi
done
```

Output:

```text
PASS class="aurora-hero-2026"
PASS class="aurora-hero-media"
PASS class="aurora-path-row"
PASS href="/work/"
PASS href="/speaking/"
PASS href="/blog/"
PASS href="/recent-projects-include/"
PASS class="aurora-button aurora-button-primary"
PASS class="aurora-button aurora-button-secondary aurora-button-reel"
PASS Photo: CreativeMornings Vancouver
PASS Source: Punk Rock AI media archive
```

### No autoplay default + responsive media sources in templates

Command:

```bash
for file in theme/kk-aurora/templates/home.html theme/kk-aurora/templates/front-page.html; do
  if /Applications/Codex.app/Contents/Resources/rg -q 'autoplay' "$file"; then
    echo "FAIL ${file} autoplay present"
  else
    echo "PASS ${file} no autoplay"
  fi
done
```

Output:

```text
PASS theme/kk-aurora/templates/home.html no autoplay
PASS theme/kk-aurora/templates/front-page.html no autoplay
```

### Responsive/behavior CSS markers

Command:

```bash
/usr/bin/curl -sSL http://localhost:10003/wp-content/themes/kk-aurora/style.css | /Applications/Codex.app/Contents/Resources/rg -n "aurora-path-row|aurora-button-reel|object-position: 62% 30%|@media \(max-width: 700px\)|@media \(max-width: 1180px\)|overflow-x: auto"
```

Output:

```text
761:.aurora-path-row {
768:.aurora-path-row a {
784:.aurora-path-row a:hover {
793:.aurora-button-reel {
1284:@media (max-width: 1180px) {
1324:@media (max-width: 700px) {
1347:    overflow-x: auto;
1396:    object-position: 62% 30%;
1412:  .aurora-path-row {
1416:  .aurora-path-row a {
```

## Screenshot + JSON Artifacts

- Desktop screenshot: `docs/current-state/aurora-smoke-2026-05-20/aurora-home-desktop.png`
- Mobile screenshot: `docs/current-state/aurora-smoke-2026-05-20/aurora-home-mobile.png`
- Metrics: `docs/current-state/aurora-smoke-2026-05-20/aurora-home-metrics.json`
- Accessibility/behavior checks: `docs/current-state/aurora-smoke-2026-05-20/aurora-accessibility-checks.json`

Metrics JSON currently records:

- desktop capture width `1440`, height `1000`, overflow heuristic `false`
- mobile capture width `390`, height `844`, overflow heuristic `false`

## Required Verification Commands

```bash
git diff --check
jq empty theme/kk-aurora/theme.json
php -l theme/kk-aurora/functions.php
```

Result: all passed.

## Lane Result

- Homepage now has explicit first-viewport identity, media-led hero behavior with responsive fallbacks, clear CTA hierarchy, and visible Work/Speaking/Writing/Project pathways.
- Evidence artifacts are present for review and PR gating.
- Track B scope boundaries were preserved.
