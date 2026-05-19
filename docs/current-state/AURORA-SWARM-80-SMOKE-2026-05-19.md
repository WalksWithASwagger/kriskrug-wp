# AURORA Swarm 80 Smoke — 2026-05-19

Branch: `codex/swarm-80-header-nav`  
Worktree: `/Users/kk/Code/kriskrug-wp-swarm-80`  
Issue: [#80](https://github.com/WalksWithASwagger/kriskrug-wp/issues/80)

## Scope

Track B header/nav stabilization only:

- `theme/kk-aurora/style.css` (header/nav sections and related media-query behavior)
- No Track A payload edits

## What Changed

1. Locked desktop header layout to a stable three-zone grid (`brand`, `primary nav`, `actions`) with `minmax(0, 1fr)` behavior to prevent cross-zone overflow pressure.
2. Added a controlled mid-width breakpoint (`max-width: 1180px`) that shifts header into a two-row layout (`brand + actions`, then nav) instead of letting desktop widths collapse into a mobile-looking state.
3. Converted sub-700px nav to a compact horizontal scroll lane (single row) to avoid stacked/vertical CTA pressure and reduce first-viewport header density.
4. Added explicit reduced-motion header fallback by removing blur effects under `prefers-reduced-motion`.

## Lightweight Local Smoke

Local base URL used for checks: `http://127.0.0.1:10003`

### 1) Six-page HTTP smoke

Command:

```bash
for path in / /about/ /2026/05/16/make-culture-not-content/ /2026/05/15/your-taste-is-your-moat/ /2026/05/14/calling-us-all-in/ /2026/05/07/web-summit-vancouver-2026/; do
  /usr/bin/curl -sSL -o /dev/null -w "%{http_code} ${path}\n" "http://127.0.0.1:10003${path}"
done
```

Output:

```text
200 /
200 /about/
200 /2026/05/16/make-culture-not-content/
200 /2026/05/15/your-taste-is-your-moat/
200 /2026/05/14/calling-us-all-in/
200 /2026/05/07/web-summit-vancouver-2026/
```

### 2) Header/nav IA and utility CTA presence on home

Command:

```bash
home_html="$(
  /usr/bin/curl -sSL http://127.0.0.1:10003/
)"
for token in 'class="aurora-header aurora-header-2026"' 'class="aurora-primary-nav"' 'href="/about/"' 'href="/work/"' 'href="/generative-ai-services/"' 'href="/speaking/"' 'href="/events/"' 'href="/blog/"' 'href="/contact/"' 'class="aurora-utility-link"' 'class="aurora-button aurora-button-primary aurora-header-cta"'; do
  if print -r -- "$home_html" | /Applications/Codex.app/Contents/Resources/rg -q "$token"; then
    echo "PASS $token"
  else
    echo "FAIL $token"
  fi
done
```

Output:

```text
PASS class="aurora-header aurora-header-2026"
PASS class="aurora-primary-nav"
PASS href="/about/"
PASS href="/work/"
PASS href="/generative-ai-services/"
PASS href="/speaking/"
PASS href="/events/"
PASS href="/blog/"
PASS href="/contact/"
PASS class="aurora-utility-link"
PASS class="aurora-button aurora-button-primary aurora-header-cta"
```

### 3) No responsive-overlay navigation controls in rendered markup

Command:

```bash
for path in / /about/; do
  html="$(
    /usr/bin/curl -sSL "http://127.0.0.1:10003${path}"
  )"
  if print -r -- "$html" | /Applications/Codex.app/Contents/Resources/rg -q 'wp-block-navigation__responsive-container-open|wp-block-navigation__responsive-container-close|wp-block-navigation__responsive-container'; then
    echo "FAIL ${path} contains responsive overlay controls"
  else
    echo "PASS ${path} no responsive overlay controls"
  fi
done
```

Output:

```text
PASS / no responsive overlay controls
PASS /about/ no responsive overlay controls
```

### 4) Live theme CSS includes the new header/nav rules

Command:

```bash
/usr/bin/curl -sSL http://127.0.0.1:10003/wp-content/themes/kk-aurora/style.css | /Applications/Codex.app/Contents/Resources/rg -n "@media.*1180|prefers-reduced-motion|grid-template-areas|overflow-x: auto|backdrop-filter: none"
```

Output:

```text
78:@media (prefers-reduced-motion: reduce) {
1251:@media (max-width: 1180px) {
1254:    grid-template-areas:
1314:    overflow-x: auto;
1398:@media (prefers-reduced-motion: reduce) {
1400:    backdrop-filter: none;
1401:    -webkit-backdrop-filter: none;
```

### 5) Static hygiene check

Command:

```bash
git -C /Users/kk/Code/kriskrug-wp-swarm-80 diff --check
```

Output:

```text
[no output]
```

## Lane Result

- Header/nav render behavior is now explicitly controlled across desktop, mid-width, and mobile breakpoints.
- Required nav IA links and utility CTA are present in the rendered home markup.
- No responsive overlay control markup was detected on sampled pages.

## Remaining Follow-Up Before Closing #80

- Capture fresh desktop/mobile screenshots in a dated `docs/current-state/aurora-smoke-YYYY-MM-DD/` folder and attach to the issue thread.
- Run a quick keyboard-tab visual pass in browser (focus ring is globally defined; this smoke run verified structure, not visual focus traversal).
