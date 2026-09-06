# KK Practice: context-brief proof

Issue #982, transformation #977. This is a draft implementation, not a deployed feature. It consumes the exact teaching packet accepted from PR #991 at `4694f059dbc6c930373cb4c194268f2fffb74195`. The approved direction is recorded in PR #990. Method wording keeps its accepted `0.1-draft` identifier; changing that identifier needs a separate editorial decision.

## Scope and decisions

One purpose-built native block, `kk/context-brief`, collects six answers and creates an editable Markdown brief. Visitors can copy, download or print incomplete drafts. No model, account, database entry, upload, email submission or browser autosave is introduced. Copy permission failure leaves selectable output. The total answer limit is 8,000 Unicode code points; over-limit text remains visible and must be shortened before preview. Edited output has a separate 10,000-character export bound including headings; nothing is truncated.

The block saves an ordinary six-question worksheet in post content. Dynamic rendering provides the interaction; deactivation restores that saved worksheet. Synced-pattern/template/archive placement fails closed to saved content because the privacy policy is established only for a direct block on a singular page. Multiple insertion is disabled in the editor. No generic form engine or content registry is introduced.

The exercise uses Aurora surface, ink and accent tokens. Its outer element is a named region rather than a section because legacy Aurora CSS forces dark backgrounds on direct page-content sections. This avoids editing the theme or adding an `!important` override.

## Privacy boundary

On a consuming page, the plugin dequeues other scripts before the actual #706 script-diet capture (priority 999), suppresses other registered script tags, and makes inline scripts emitted through WordPress inert. A per-response nonce authorizes only the exercise script. CSP denies connections, forms, frames and unapproved script execution; Referrer-Policy is `no-referrer`. Other pages retain their script behavior. No global analytics settings change.

Inputs are memory-only; output is text, not executable HTML. Source URLs entered by visitors are not fetched. Copy, download and print are explicit data exits. Contact receives no answers. Reload discards the brief; exporting to another application applies that application's privacy rules.

CSP is defense in depth, not production certification. Raw third-party injection is denied and can produce a CSP console error; the dedicated adversarial test expects that error while normal operation requires a clean console. Production plugins, Pagely caching and headers must be checked separately before publication. In particular, nonce headers and HTML must remain coherent through caching. The fixture does not contain production secrets, databases, mu-plugins or CDN configuration.

## Reproduce

Run from this repository/worktree, with its local manifest present. Use Node 24 and PHP for smoke checks:

```sh
npm --prefix "$PWD" ci --ignore-scripts
node node_modules/playwright/cli.js install chromium
make practice-test
make practice-preview
make practice-browser-test
make practice-package
```

`practice-preview` prints the actual WordPress version, source URL and practice URL. It mounts only this plugin and Aurora into a disposable WordPress 7.0.4/PHP 8.2 SQLite/WASM fixture. It installs the repository's actual #706 snippet with synthetic gtag registration, approved public teaching copy, and the approved public North House photograph. Internet access is required to obtain runtime files and that photograph. A failed setup download is unavailable setup, not a passing test. Runtime image failure is tested separately.

The CLI's supported options do not expose a host binding. It initially binds its default interface, then the harness rebinds loopback before fixture content is created. Use only trusted development machines; the fixture has no private data. Stop the owned process with Ctrl-C. Do not expose the fixture as a public server. No persistent CLI `start`, shared installation, Docker or production access is needed.

`PRACTICE_PORT` changes the manual preview port (default 9832). Browser tests use 9833 and close their fixture. `PRACTICE_CHROME` can select a local Chrome executable; CI installs pinned Playwright Chromium with the same job-scoped browser path for installation and execution. The first CI run found no executable in the inherited browser directory; the job now uses its own runner-temporary directory and explicit local installer, without skipping browser tests. `PRACTICE_EVIDENCE` selects screenshot/report output (default `/tmp/kk-practice-evidence`). Evidence uses synthetic answers only. Do not submit participant text in issues, logs or screenshots.

## Dependency evidence

Checked official sources on 2026-09-06:

- [Playground CLI API](https://wordpress.github.io/wordpress-playground/guides/programmatic-playground-cli/): programmatic version selection, mounts, blueprint and disposal. npm current version is pinned to 3.1.52; actual runtime readback verified WordPress 7.0.4.
- [WordPress block metadata](https://developer.wordpress.org/block-editor/reference-guides/block-api/block-metadata/): native editor registration, frontend-only view script and PHP rendering.
- Playwright test 1.63.0 is pinned as a development dependency. The production ZIP contains no npm packages.
- npm initially reported four moderate transitive advisories through Playground's `qs` parser. A scoped development override to patched `qs` 6.16.0 removes them; npm audit reports zero vulnerabilities. [Maintainer advisory](https://github.com/advisories/GHSA-4mjr-xmp4-gh2g). Revisit the override when upstream updates its range.
- [GitHub branch filters](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax): the existing workflow targets only main/develop. The exact accepted teaching branch is additionally enabled so this stacked feature PR receives the same checks.

## Done when and verification

`practice-test` checks six exact approved questions/help/example strings, actual `editor.save` output, and a 20 KB compressed JS/CSS budget. The browser suite exercises real WordPress, not a patched HTML shell: empty and complete drafts, literal adversarial input, answer preservation, edited output, copy denial, exact downloaded bytes, printing, Unicode bounds, four viewport widths, 200% CSS zoom, reduced motion, computed text contrast, keyboard operation, image failure, JavaScript-off worksheet, normal console, request/storage/cookie canaries, #706 positive control, CSP nonce/header and raw-script denial, nested fail-closed placement, real editor save/reopen, and actual plugin deactivation.

The editor-save fixture executes the production save function. Browser validation additionally loads the real WordPress editor, checks validity and registration, saves with core/editor, reloads, and checks validity again. No editor attribute contains a visitor answer.

Baseline: 913 Python tests (179 publisher, 654 operational, 12 SEO inventory, 68 backfill), JavaScript checks, existing plugin/theme smoke, docs truth and 45 tracked PHP lint checks passed. The isolated worktree initially lacked PHPCS; rerunning with the existing root vendor bin on PATH passed. This is an unavailable dependency resolved locally, not a code failure. Voice and changed-file Ruff passed. Final evidence is recorded in the PR and generated report; new PHP files must be staged before the tracked-file lint gate can count them.

Local checkpoint (2026-09-06): final `make verify` passes all 913 Python tests, JS/smoke/docs checks; staged PHP lint covers 48 files and PHPCS covers 8. `make voice-check`, changed-file Ruff, explicit Ruff for the package builder, and diff whitespace checks pass. Local browser: Chrome on macOS arm64, Node 24.19.0. Normal text contrast is 14.88:1; a synthetic preview measured 0.5–0.6 ms (one device, not a performance distribution). Compressed view JS/CSS is 2,984 bytes. The generated browser report and synthetic screenshots/PDF are local review evidence, not participant data or a production pixel-gate substitute.

Manual screen-reader speech testing and browser-native 200% zoom are not claimed by CSS zoom or accessibility-tree review. The 4/5 ten-minute visitor outcome and follow-up evaluation remain pending under #983. A green CI run cannot satisfy that human gate.

## Package and rollback

`make practice-package` produces `/tmp/kk-practice-0.1.0.zip` and prints SHA-256. The deterministic archive contains only the bootstrap and block production files; no tests, dependencies, credentials or fixtures. Rebuild and verify its hash against the reviewed commit before installation.

No deployment is authorized by this PR. Before any release, snapshot the exact dependent page identities and content, confirm no intervening edits, install the reviewed artifact, verify the live privacy/cache boundary, then publish approved content and links last. Roll back links/content first with conflict checks, preserving public URLs, then restore the prior plugin artifact or deactivate it. The saved worksheet remains meaningful after deactivation; do not replace a post with a self-closing dynamic block. Never overwrite later edits or delete published URLs to simplify rollback.
