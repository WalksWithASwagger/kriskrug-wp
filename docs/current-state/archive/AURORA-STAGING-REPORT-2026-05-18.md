# Aurora Staging Report - 2026-05-18

**Lane:** Swarm Lane 4 - Aurora staging QA  
**Track:** Track B only  
**Branch/worktree used:** `codex/aurora-staging-qa-2026-05-18` at `/Users/kk/Code/kriskrug-wp-aurora-staging-qa`  
**Base:** `origin/aurora/v2` at `159ac2a` (`docs: aurora v2 next-session playbook`)  
**Production status:** No production activation or production writes attempted.

## Scope

The goal was to get as close as possible to rendered Aurora validation without disturbing `main` or the locked existing `aurora/v2` worktree.

Inspected:

- `origin/aurora/v2`
- `theme/kk-aurora.zip`
- `demo/index.html`
- `docs/current-state/AURORA-MIGRATION-PLAN.md`
- `docs/current-state/AGENT-SWARM-OPERATING-PLAN-2026-05-18.md`
- Local by Flywheel state for `kriskrug-local`

## Results

Local by Flywheel is installed and has a `kriskrug-local` site registered at:

- Filesystem: `/Users/kk/Local Sites/kriskrug-local/app/public`
- Local domain: `kriskrug-local.local`
- Local HTTP port: `10003`
- Local MySQL port: `10004`
- WordPress version from bundled WP-CLI: `6.9.4`

Aurora is already installed and active in that Local site:

```text
name          status    version
kk-aurora     active    1.0.0
```

The checked-in installable theme zip is structurally valid:

```text
unzip -t theme/kk-aurora.zip
No errors detected in compressed data of theme/kk-aurora.zip.
```

The static demo can be served without WordPress:

```text
python3 -m http.server 8765
curl -I http://127.0.0.1:8765/
HTTP/1.0 200 OK
```

Safari rendered the static demo at `http://127.0.0.1:8765/`. The demo visually matches the expected Aurora direction: dark background, cyan/teal/purple accents, sticky header, large hero type, and visible CTAs.

## Local WordPress Smoke

The Local WordPress site initially reported as `running` in Local's JSON, but no nginx/mysql listener was reachable. After opening Local, its services started successfully. Local logs showed mysql startup retries, then a successful ping:

```text
Database connection attempt 3 over socket
Database responded to ping over socket
```

Smoke-tested paths using the Local host header against `127.0.0.1:10003`:

| Path | Status | Notes |
|---|---:|---|
| `/` | 200 | Aurora theme assets present |
| `/about/` | 200 | Aurora theme assets present |
| `/2026/05/15/your-taste-is-your-moat/` | 200 | Aurora theme assets present |
| `/2026/05/16/make-culture-not-content/` | 200 | Aurora theme assets present |
| `/2026/05/14/calling-us-all-in/` | 200 | Aurora theme assets present |
| `/2026/05/07/web-summit-vancouver-2026/` | 200 | Aurora theme assets present |

Theme assets returned `200`:

- `/wp-content/themes/kk-aurora/assets/css/typography-refined.css`
- `/wp-content/themes/kk-aurora/assets/css/animations.css`
- `/wp-content/themes/kk-aurora/assets/css/bleeding-edge.css`
- `/wp-content/themes/kk-aurora/assets/js/theme.js`
- `/wp-content/themes/kk-aurora/assets/js/micro-interactions.js`
- `/wp-content/themes/kk-aurora/assets/js/aurora-animations.js`

External GSAP assets also returned `200`:

- `https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js`
- `https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js`

## Rendered Findings

Static demo:

- Rendered in Safari.
- Header, hero, nav links, CTA buttons, stat blocks, and footer content were visible.
- Useful as a design reference, but not a WordPress validation surface.

Local WordPress:

- WordPress rendered with Aurora active and the requested real-content URLs reachable.
- Safari showed a problematic desktop render state on the homepage: the responsive navigation overlay/content appeared exposed, including a visible close button, mobile-style menu button, vertical site title/sidebar treatment, and a vertical `Let's Talk` button.
- This means the staging surface is alive, but Aurora is not ready for cutover based on this first render.

Likely issue area:

- FSE navigation/header template state and responsive navigation CSS/markup.
- The theme uses a Navigation block in `theme/kk-aurora/parts/header.html`; the current Local render suggests the navigation overlay may be open or styled incorrectly on desktop.

## Screenshot Attempt

Tried to save screenshots under `docs/current-state/aurora-smoke-2026-05-18/` with macOS `screencapture`, but the command returned:

```text
could not create image from display
```

Computer Use/Safari visual inspection did work, but no screenshot files were committed from this session.

## Blockers

1. **Rendered desktop header/nav is not clean.** The Local WordPress homepage renders real content with Aurora active, but the nav/header state appears broken on desktop.
2. **No automated browser console capture.** The Codex in-app browser surface was unavailable, and this machine does not currently have local `playwright` or `puppeteer` packages installed.
3. **Local startup is manual/flaky.** Local's site status JSON said `running` before nginx/mysql were actually listening. Future agents should verify actual listeners with `lsof` or `curl`.
4. **Host/port mismatch needs care.** WordPress `home` and `siteurl` are `http://kriskrug-local.local`, while the reachable port is `10003`. HTTP checks should use `-H 'Host: kriskrug-local.local' http://127.0.0.1:10003/...` to avoid misleading redirects.

## Recommended Next Steps

1. Fix the desktop header/navigation render on `aurora/v2` before any cutover planning.
2. Re-run the same six URL smoke after the header fix.
3. Add real browser screenshot capture once Browser/Playwright is available, ideally saving desktop homepage, mobile homepage, About page, and two long-form posts.
4. Check Safari/Chrome console errors for Aurora scripts after visual render is clean.
5. Only after clean Local smoke, repeat against Cloudways or Pagely staging with a production-like DB/media copy.

## Commands Worth Reusing

```bash
git worktree add -b codex/aurora-staging-qa-2026-05-18 /Users/kk/Code/kriskrug-wp-aurora-staging-qa origin/aurora/v2
unzip -t theme/kk-aurora.zip
python3 -m http.server 8765
curl -I http://127.0.0.1:8765/
lsof -nP -iTCP:10003 -sTCP:LISTEN
php /Applications/Local.app/Contents/Resources/extraResources/bin/wp-cli/wp-cli.phar --path="$HOME/Local Sites/kriskrug-local/app/public" --allow-root theme list
curl -sS -H 'Host: kriskrug-local.local' http://127.0.0.1:10003/
```
