# Aurora visual-regression baseline — runbook (#473)

**Status:** Active. Implements step 1 / §4 of
[`AURORA-STYLESHEET-REBUILD-PLAN.md`](AURORA-STYLESHEET-REBUILD-PLAN.md).

This harness is the gate for the Aurora stylesheet rebuild ([#423](https://github.com/WalksWithASwagger/kriskrug-wp/issues/423)).
Nothing in rebuild steps 2–8 (#474–#481) lands without a green `make visual-diff`
against a frozen baseline.

Implementation: [`scripts/visual_baseline.py`](../../scripts/visual_baseline.py).

---

## The three commands

```bash
make visual-baseline                 # freeze a baseline; prints its run id
make visual-diff BASE=<run-id>       # capture a candidate and compare
make visual-diff-report DIFF=<run-id># markdown table for the PR body
```

Support commands:

```bash
make visual-preflight                # Chromium + routes + storage guard, captures nothing
make visual-guard                    # re-assert "no capture binary is tracked or staged"
make visual-list                     # which manifests exist and which still have PNGs on disk
make visual-prune KEEP=2 DRY_RUN=1   # preview a pair-safe prune; manifests are kept
```

All targets accept `ROUTES="home blog"` and `VIEWPORTS="desktop"` to narrow a run,
and `BASE_URL=` to point at a different origin.

### Capture retention (#749)

PNG capture directories are gitignored and have no gate value once their
window's `diff-*.json` / `report-*.md` is committed. Keep the newest baseline
and the newest pre/post pair; prune the rest after each deploy window closes
with `make visual-prune KEEP=2`. `KEEP` is a minimum: when a retained candidate
has a tracked diff, its baseline is retained too, so the command may keep more
than two directories rather than split a pair. Preview with `DRY_RUN=1` and put
the exact paths and sizes through KK before running the command without it.
Tracked manifests and reports stay. The current approved-or-pending inventory
belongs in a dated proposal; see
[`reports/visual-baseline-prune-proposal-749-2026-08-28.md`](reports/visual-baseline-prune-proposal-749-2026-08-28.md).

## The deploy-step loop

1. **Before** the deploy: `make visual-baseline`. Note the run id and commit the
   manifest. Record the Boost bundle hash it prints.
2. Deploy the step. Purge Pagely + Jetpack Boost.
3. **After** the deploy: `make visual-diff BASE=<run-id>`.
4. `make visual-diff-report` and paste the table into the PR.
5. Every `warn` needs a sentence in the PR saying why it is expected. Every
   `fail` blocks the step until it is either fixed or explicitly approved by KK
   and the baseline re-frozen **in the same PR, called out in the PR body**.
   Never re-freeze silently (§4.4).

If the Boost CSS bundle hash is **unchanged** after a deploy, the deploy did not
reach the edge — that is risk R-2, not "the change had no visual effect". The
diff report says so explicitly.

## What it captures

11 logged-out routes × 3 viewports (375 / 768 / 1440), full-page, device scale 2.

| Route | Template | Expected status |
|---|---|---|
| `/` | `front-page.html` | 200 |
| `/about/` | `page.html` | 200 |
| `/generative-ai-services/` | `page.html` | 200 |
| `/speaking/` | `page.html` | 200 |
| `/work/` | `page.html` | 200 |
| `/photography/` | `page.html` | 200 |
| `/blog/` | `index.html` | 200 |
| `/contact/` | `page.html` | 200 |
| `/2026/07/18/i-am-nomad-ai-film/` | `single.html` | 200 |
| `/definitely-not-a-page-404-probe/` | `404.html` | **404** |
| `/category/vancouver-ai-ecosystem/` | `archive.html` | 200 |

Two deliberate departures from §4.2's list, both verified against live on
2026-07-25:

- **`/services/` → `/generative-ai-services/`.** `/services/` 301s. Capturing the
  canonical target captures a page rather than a redirect.
- **Marquee board post → category archive.** §4.2 wants the marquee board post
  because `parts/marquee-current.html` is the theme's only inline `<style>`.
  `kk-marquee-board` is repo-side only and `/marquee/` returns 404 on live, so
  there is no board post to capture. `archive.html` is otherwise uncovered by the
  other ten routes, so it takes the slot. The marquee route is still declared in
  `ROUTES`' sibling `MARQUEE_ROUTE` with `enabled: False` — flip it on and drop
  the archive route once the plugin is deployed. **Until then, inline marquee CSS
  is not covered by this gate.**

The route list is asserted before every capture: a route whose HTTP status stops
matching aborts the run. A baseline of the wrong page is worse than no baseline.

## Tolerance (§4.4)

| Verdict | Condition |
|---|---|
| **pass** | ≤ 0.1% of pixels differ |
| **warn** | 0.1% – 1.0% — human review required |
| **fail** | > 1.0%, **or** full-page height changed by > 2% |

Per-pixel comparison uses pixelmatch's YIQ delta at threshold 0.2. When the two
PNGs are byte-identical the comparison short-circuits to 0% — which is the path a
stable site takes for most pairs.

## Determinism controls

Risk R-8 is that the harness produces false diffs, the team stops trusting it,
and the gate becomes theatre. These are the controls, each added in response to a
measured false positive between two back-to-back runs against unchanged
production:

| Control | What it fixes | Measured before it existed |
|---|---|---|
| `reducedMotion: reduce`, `colorScheme: light`, frozen animations/transitions | 11 `@keyframes`, 6 reduced-motion blocks, 1 dark-scheme block | — |
| Force `loading=eager` + `decode()` on every image | Lazy images below the fold captured blank in full-page shots | **2.65%** of homepage pixels |
| Strip `srcset`/`sizes` at parse time (MutationObserver init script) | Which srcset candidate wins is a layout-timing race; with `object-fit: cover` a different candidate crops differently | **0.089%** of `/blog/` pixels |
| Drive reveal classes to their end state | `.aurora-fade-up`, `.aurora-scale-in`, `.is-aurora-lux-reveal` start at `opacity: 0` and only reveal when JS fires; content that never intersected is captured invisible | reveal-gated cards captured faded |
| Selector masks for marquee / dates / Beehiiv | Genuinely non-deterministic content | — |
| Scroll-settle, `document.fonts.ready`, `networkidle`, settle delay | Late webfont swap, IntersectionObserver reveals | — |
| Third-party hosts fulfilled with an empty 200 | GTM, social embeds, widgets | — |

Reveal end-states are driven by adding the **theme's own** `is-visible` /
`is-revealed` class, not by overriding `opacity` in CSS — so a real regression in
those rules still shows up in the pixels. A blanket `opacity: 1 !important` would
hide it.

Masks and reveals are **declared in the manifest, not hardcoded into the
comparison** (§4.3). Per-capture match counts are recorded, so a class rename
surfaces as a count of `0` rather than as a diff nobody can explain. Override
both with `--masks <file.json>` (`{"masks": {...}, "reveals": [...]}`).

Every run also records, in the manifest:

- live-vs-repo **md5 per theme CSS file** and both `style.css` `Version:` strings;
- the **Jetpack Boost** CSS and JS bundle hashes;
- per-capture image counts (`painted/total`) and mask/reveal match counts.

## Verification of the gate itself (2026-07-25)

Two consecutive full runs against unchanged production, `BASE1` → `BASE2`,
33 route/viewport pairs:

**33 pass · 0 warn · 0 fail · 0 error.** 31 pairs byte-identical by SHA-256; the
other two (`/photography/` tablet and desktop) differed in PNG bytes but had
**0 differing pixels** above threshold. No full-page height changed at all.

Committed evidence: `reports/visual-baseline/manifest-BASE1.json`,
`diff-BASE2.json`, `report-BASE2.md`. The ~500 MB of PNGs those two runs produced
are not in git and never were.

Also observed and worth knowing:

- The `beehiiv` mask matched **0 elements on all 33 captures**. The Beehiiv
  presence on these routes is a link, not an embed. The mask is declared anyway,
  and its per-capture match count is recorded — so if an embed is added later it
  is masked automatically and visibly.
- The `marquee` mask matches 4 elements on every route including the 404, i.e.
  the site-wide woven marquee, not the (undeployed) board.
- `.is-aurora-lux-reveal` matched 20 elements on `/blog/` and 76 on the single
  post, and 0 elsewhere — those two routes are why the reveal control exists.

## Storage — never commit a PNG (#318)

`.git` is already ~303 MB with 347 tracked images. A naive screenshot harness
would add tens of MB per rebuild step. The rule is enforced by three independent
mechanisms, not by intention:

1. **`.gitignore` denies by default.** `docs/current-state/reports/visual-baseline/*`
   is ignored one level down, so git never descends into a run directory — its
   PNGs, curl cache and generated drivers cannot be added even by `git add -A`.
   Only `manifest-*.json`, `diff-*.json`, `report-*.md` and `README.md` at the top
   level are re-included by name.
2. **The script refuses to write into a tracked path.** Before any capture it runs
   `git check-ignore` on the run directory and aborts if the directory is not
   ignored — so a broken `.gitignore` stops the harness rather than filling the
   repo.
3. **`visual_baseline.py guard` re-asserts it against the index** after every
   capture and every diff, and is exposed as `make visual-guard`. It fails if any
   tracked file under the artifact root is not an allowed manifest, if any binary
   is staged anywhere, or if the ignore rule has stopped working.

Diff images are written only for pairs that **warn or fail**; passing pairs have
their diff PNG deleted at the end of the run. Attach failing diffs to the PR
comment or as CI artifacts — GitHub-hosted, not repo-hosted (§4.5.4).

Losing a baseline costs one `make visual-baseline`, so prune freely.

## Chromium

Chromium is preinstalled at `/opt/pw-browsers`. **Never run `playwright install`.**
The harness fails loudly and exits 2 if `PLAYWRIGHT_BROWSERS_PATH` is unset, does
not exist, contains no `chromium*` directory, or resolves to a missing executable.
Every Node child is spawned with `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1`.

The Python `playwright` package is **not** installed and is not required: the
capture and comparison drivers are Node programs, written into the (ignored) run
directory at runtime and driven by `scripts/visual_baseline.py`. The only Python
dependency is the standard library.

### Why the browser never talks to kriskrug.co directly

Chromium cannot reach the public internet through this environment's agent proxy
(`ERR_CONNECTION_RESET`), while `curl` gets 200. So every request the browser
makes is intercepted by Playwright and fulfilled from a curl fetch, cached on
disk for the run. The page keeps its real origin (`https://kriskrug.co/...`), so
no URL rewriting is needed. `scripts/interaction_state_probe.js` (#424) solves the
same constraint with a rewritten local mirror; this harness uses interception
because screenshots need asset URLs and layout left exactly as production serves
them.

Hosts outside the allowlist (`kriskrug.co`, `s5102.pcdn.co`, `i*.wp.com`) are
fulfilled with an empty 200 rather than fetched.

## Honest limits (§4.7)

- **There is no staging.** Every step compares *post-deploy live* against
  *pre-deploy live*, so a regression is caught minutes after it ships, not
  before. That is why every step's rollback is a pre-built zip (R-1).
- Screenshots cannot see focus, hover or keyboard behaviour. #424's manual
  tab-through remains a separate required gate.
- It cannot see the editor canvas. Step 4 adds a manual editor screenshot pair.
- Inline marquee CSS is not covered while `/marquee/` is 404 on live (above).
- Stripping `srcset` means captures use each image's `src` rather than the 2x
  candidate a real retina visitor gets. Layout is identical; only bitmap
  resolution differs, and it differs identically in baseline and candidate. Pass
  `--keep-srcset` for higher fidelity at the cost of run-to-run stability.
