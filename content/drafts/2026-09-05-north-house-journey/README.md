# North House proof: review packet

**State:** implemented locally, not merged or deployed. Tracking: [#977](https://github.com/WalksWithASwagger/kriskrug-wp/issues/977).
Proof issue: [#978](https://github.com/WalksWithASwagger/kriskrug-wp/issues/978).
The approved [product plan](../../../docs/current-state/CONNECTED-PORTFOLIO-PLAN.md)
owns the north star, roadmap, non-goals and milestone acceptance criteria.

## Reviewed change and sources

- Events page 2250: one `recap_url` and compact-card label. The host URL stays intact.
- Published recap 12744: `recap-link.html` after the take-home challenge. The existing
  package's `post.html` and Markdown body contain the same change. Its draft
  frontmatter remains historical publisher input, not current publication status.
- Services page 2666: `services-insert.html` before "Proof in motion", using its
  existing section/grid/button classes. Its image alone has `max-width:100%` and
  `height:auto` so sizing works without theme JavaScript. Existing CSS and proof
  cards are unchanged.

Copy comes from the [published recap package](../2026-09-02-north-house-show-and-tell/STATUS.md)
and its [editorial rulings](../2026-09-02-north-house-show-and-tell/publish-gate.md).
Photo 12742 is the existing 1152 x 1536 original, with approved alt text, natural
aspect ratio, and no invented photographer credit. No new outcome or testimonial.

The three Services replacement packs remain untouched: the architecture pack
uses a different visual system, the keynotes candidate was never deployed, and
#480's pack removes CSS. This packet does not authorize any of them.

## Baseline and technology decision

Revalidated 2026-09-05 from clean main `295108a`, then isolated in
`codex/north-house-proof`. No overlapping content PR; #973/#974 change dependencies
and CI. Live WordPress 7.0.4 / Aurora 1.6.11, authenticated raw hashes unchanged
from the audit. `manifest.json` records those raw UTF-8 hashes and UTC modification
times, not private metadata or credentials.

Baseline: 98 focused operational tests plus 7 publisher update-guard tests passed;
Events Ruff and recap voice checks passed. Doctor resolved Varlock; direct process
credentials were absent, then authenticated reads succeeded under Varlock. The
status report's retired `origin/aurora/v2` comparison failed as before; it is not
a blocker for this Track A change. Broad active-document drift remains #976.

No new runtime dependency, API service, framework or application model. Official
API/tool documentation is linked in the product plan. The only material spike is
the rendered Services insertion: use public shells/assets in a private local
preview, retaining server-added author content and existing links. This does not
prove WordPress filters, public caches or post-deployment behavior.

## Prepare and check (no WordPress writes)

Use the existing Python environment. In a worktree, point `PYTHON` at the original
checkout's venv rather than installing another copy. Resolve secrets from the
root schema with Varlock; never inspect value files. Run from the checkout that
contains this packet, with absolute private paths outside Git for artifacts.

```bash
varlock run --inject vars -- "$PYTHON" scripts/apply_north_house_journey.py check
varlock run --inject vars -- "$PYTHON" scripts/apply_north_house_journey.py prepare --output /private/tmp/north-house-candidate
"$PYTHON" scripts/preview_north_house_journey.py --output /private/tmp/north-house-browser
NODE_PATH="$HOME/.local/pw/node_modules" PLAYWRIGHT_BROWSERS_PATH="$HOME/Library/Caches/ms-playwright" node scripts/tests/north_house_journey_browser.cjs /private/tmp/north-house-browser
```

`check` never writes files or WordPress. `prepare` only saves private artifacts,
mode 0600, without overwriting existing files. Preview generation only GETs public
pages and saves private HTML. It changes the three approved regions in the public
shell and localizes journey links; existing server-rendered content is preserved.
The browser harness compares baseline/candidate under the same network policy.

## Future release and rollback: separate approval required

This PR is the review boundary. Do not run `--execute` now. Before a future apply,
re-run doctor/status/check, review the precise payload and local screenshots, and
obtain approval for these three content fields. Hash or modified-time drift stops
the helper; do not blindly refresh hashes to bypass a stop.

`apply --target services`, then `recap`, then `events` are dry-runs unless both
`--execute` and a private `--snapshot-dir` are supplied. Each write snapshots first,
re-reads identity/body/metadata immediately before POST, writes only `content`,
and requires exact raw and unchanged-metadata readback. There are no automatic
write retries or automatic rollbacks. Already-applied bodies are no-ops.

These are three separate REST writes. A competing editor can still race the last
read. Stop on any failure; after an uncertain response run `check` and inspect the
saved snapshot/readback rather than retrying blindly. Public cached HTML must be
checked separately after each approved write, including the Services anchor.

`restore --snapshot <private-file>` previews rollback; `--execute` additionally
requires `--snapshot-dir`. Restore requires the exact recorded after body and
unchanged metadata, saves its own snapshot, and verifies the exact restored body.
Restore in reverse order (Events, recap, Services) if a full rollback is approved.
If content has changed, stop and review the conflict. Do not use the generic page
deployer, draft updater, or #832's writer for this packet.

## Validation and remaining decisions

Validated 2026-09-05 UTC. Local Python 3.14.6, Node 24.19.0, Playwright 1.62.1;
CI retains its existing Python 3.12 / Node 20 configuration. No dependency upgrade.

| Check actually run | Result / acceptance evidence |
|---|---|
| `make python-test PYTHON=<existing-venv-python>` | 935 passed: 179 publisher, 676 operations, 12 SEO inventory, 68 SEO backfill. Includes exact preservation, three-target identity/drift refusal, snapshot-before-write, uncertain response, no-op reapply, ordered release and conflict-safe restoration. |
| `ruff check --no-cache` on both new helpers, renderer and their tests | Passed. |
| `make javascript-syntax plugin-smoke theme-smoke docs-truth-check` | Passed, including the browser harness syntax and existing PHP/JS smoke contracts. |
| `make validate` | Initial worktree attempt could not find PHPCS. Rerun with the original checkout's `vendor/bin` on command-local `PATH` passed: 45 PHP syntax checks and PHPCS on 7 files. No installation or global configuration change. |
| `voice_check.py --files` on the two fragments and recap HTML/Markdown | Passed; fragment voice and public-safety checks also run in the Python gate. |
| `make voice-check` | Passed across 166 files with zero violations; 214 pre-existing baseline waivers, none added or changed. |
| `north_house_journey_browser.cjs` | 18 baseline/candidate renders at 1280, 768 and 390 px. Zero horizontal overflow, one H1, loaded original-ratio photo after its reveal animation. Complete keyboard journey with JavaScript on and off; each contextual link has a visible 2 px focus outline. Contact's existing email link is present; no enquiry was sent. |
| Blocked proof-image request | Copy, alt text and enquiry remain usable at 390 px without overflow. Existing Events empty/fallback/archive contracts pass; this static insertion adds no new asynchronous application state. |
| Final authenticated `prepare` | All three original bodies and timestamps still match the manifest; exact candidate hashes verified. Private snapshots/payloads created, zero WordPress writes. |

[Desktop Services proof](review-services-desktop.png) · [Mobile Services proof](review-services-mobile.png).
These are local public-shell candidate captures, not deployed screenshots. The
private browser report also records Events/recap screenshots and both keyboard journeys.

The console comparison exposed two measurement issues, corrected without ignoring
errors: use one localhost origin for both states, and expose the existing lazy
Services proof images in both. Final result: **zero new console errors**. Both
states report a 403 for the existing `bcai-living-ecosystem.webp` image and CORS
errors for the CDN-hosted WordPress `interactivity` and image-view modules. The
latter are localhost-preview limitations, not confirmed production defects.
The existing image failure is outside this slice; retain it as follow-up evidence
for the Services work rather than replacing an unrelated asset here.

Browser waits use explicit stylesheet/font/image/focus conditions rather than
[`networkidle`](https://playwright.dev/docs/api/class-page#page-goto-option-wait-until),
which was unreliable with public third-party assets. The new photo's two sizing
declarations are the only product adjustment from the initial markup proposal;
they fix the observed JavaScript-disabled overflow without changing existing CSS.

The private review directory holds authenticated snapshots; none are committed.
Only public content fragments, hashes and the two reviewed UI captures enter Git.
Final secret scan, diff review and GitHub check results are recorded in the PR.

The 4/5 visitor comprehension evaluation is **pending**; automated checks cannot
answer it. Screen-reader/physical-device testing and WordPress-filter/cache
readback after publication have **not run**. No AI behavior changed, so AI evals,
a new frontend build and a type-check pipeline are not applicable to this slice.
No claim of increased enquiries or production success is made by this proof PR.

This proves the proposed journey is implementable within the existing content
system and usable by keyboard in a responsive preview. The next decision is
whether to approve this copy/layout for a separately authorized, bounded live
release and the five-person evaluation. Select another example only after that
evaluation supports the hypothesis; do not create the future backlog now.
