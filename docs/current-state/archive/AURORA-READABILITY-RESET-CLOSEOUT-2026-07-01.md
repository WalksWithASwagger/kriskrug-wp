# Aurora Readability Reset Closeout - 2026-07-01

**Status:** live on production
**Track:** Track B - Aurora theme
**Branch:** `codex/aurora-readability-reset`
**PR:** [#272](https://github.com/WalksWithASwagger/kriskrug-wp/pull/272) - draft, checks green, source parity pending review
**Live theme:** `kk-aurora` `1.3.27`

## Verdict

The readability reset is what we wanted for the first pass, and a bit more.
The site still feels visual and photographic, but the primary text contract now
has teeth: standard page titles do not collapse under content headings, body
copy is no longer tiny, cards are more legible, and mobile overflow/tap-target
issues found during the live pass were fixed before closeout.

This is not "done forever." It is the foundation that lets the next work be
content and information design instead of repeatedly fighting broken CSS
hierarchy.

## Fresh Test Pass

Commands and evidence used after the live deploy:

```bash
curl -fsSL https://kriskrug.co/wp-content/themes/kk-aurora/style.css \
  | rg 'Version:|--aurora-readable-measure|font-size: var\(--aurora-page-title-size\)'
gh pr view 272 --json number,title,isDraft,state,mergeStateStatus,reviewDecision,headRefName,statusCheckRollup,url
make status-readonly
```

Results:

- Live CSS reports `Version: 1.3.27`.
- Live CSS contains `--aurora-readable-measure`.
- Live CSS contains the page title override:
  `font-size: var(--aurora-page-title-size) !important`.
- PR #272 is open as draft, merge state `CLEAN`, with validation, security,
  PHP, docs truth, summary, and Trivy checks passing.
- `make status-readonly` passed public WordPress smoke with `0` failures and
  `0` warnings.
- Open queue at the latest read-only pass: `1` PR and `16` open issues.

Full live readability evidence:

- `docs/current-state/reports/readability-audit-20260701-post-live.md`
- `docs/current-state/reports/readability-audit-20260701-post-live.json`
- `failureCount: 0`
- Pages audited: Home, Blog, article, Work, About, Vancouver AI category,
  Contact.
- Viewports audited: `1440x1100`, `768x900`, `390x844`, `360x740`.

Performance evidence:

- `docs/current-state/reports/performance-audit-20260701-post-readability-live.md`
- `docs/current-state/reports/performance-audit-20260701T185544Z-cold-ttfb-cleanup-after.md`

Latest post-cleanup route sample:

| Route | Cold TTFB p50 | Warm TTFB p50 | Redirects | Final URL |
|---|---:|---:|---:|---|
| `/` | `3.654s` | `0.521s` | `0` | `/` |
| `/about/` | `3.807s` | `0.527s` | `0` | `/about/` |
| `/blog/` | `0.839s` | `0.522s` | `0` | `/blog/` |
| `/projects/` | `1.039s` | `0.808s` | `1` | `/work/` |
| `/work/` | `4.183s` | `0.518s` | `0` | `/work/` |

## What Improved

- Standard page H1 hierarchy is now stable across desktop, tablet, and mobile.
- The readable measure contract is live: prose is constrained around the
  `680-740px` target instead of sprawling across the viewport.
- Body text and card text now meet the minimum-size contract, with captions and
  meta remaining secondary.
- Work, About, Contact, Blog, article, and category surfaces now pass the live
  computed-style audit.
- The homepage image quick win is preserved: the heavy Vancouver AI source PNG
  is no longer loaded directly by the homepage card.
- `/work/` now returns `200` directly; `/projects/` remains a one-hop redirect
  to `/work/`.

## Remaining Blockers

- Jetpack Boost Critical CSS completed one generation pass after the first
  deploy, then remained stuck at `Generating Critical CSS...` after the final
  `1.3.27` deploy. Keep issue #125 open.
- Lighthouse or PageSpeed LCP, INP, CLS, and TBT are not captured yet.
- Cold-cache TTFB remains high on `/`, `/about/`, and `/work/` even though warm
  cache behavior is acceptable.
- Many content pages still carry one-off `kk-*` or `kkp-*` structures. The CSS
  foundation is ready, but the content architecture is not fully migrated.
- The current-state docs still contain older historical truth lines; use this
  closeout plus the newest `make status-readonly` output before acting.

## Roadmap From Here

1. **Source closeout for PR #272**
   - Review the draft PR against production truth.
   - Merge only after human review agrees that the live `1.3.27` package should
     become source truth on `main`.
   - Keep rollback package paths documented in
     `PERFORMANCE-RECOVERY-2026-07-01.md`.

2. **Critical CSS and performance truth**
   - Re-check Jetpack Boost Critical CSS status.
   - If it is still stuck, capture the exact UI state and treat #125 as a
     plugin/cache workflow issue, not a theme-readability blocker.
   - Capture Lighthouse or PageSpeed metrics for homepage, Blog, Work, About,
     and one article: LCP, INP, CLS, and TBT.
   - Investigate cold TTFB on `/`, `/about/`, and `/work/` separately from CSS
     and image work.

3. **Page information architecture**
   - Use issue #122 as the next main design lane.
   - Migrate Work, About, Speaking, Contact, and the highest-value generic pages
     toward Aurora-owned primitives: page lead, section kicker, display heading,
     proof/stat block, media card, and readable card grid.
   - Keep the rule: one dominant display heading per page.
   - Snapshot before live WordPress page writes and keep body-only payloads when
     preserving user-authored titles.

4. **Blog and archive rhythm**
   - Keep image-forward modules, but prefer fewer, stronger repeated units over
     dense small-text grids.
   - Review category/tag archives after the main Blog surface, especially
     Vancouver AI and high-volume topic pages.
   - Keep dates/meta secondary but readable.

5. **Accessibility and mobile QA**
   - Fold this readability work into #127 and #86.
   - Run keyboard, focus, reduced-motion, contrast, overflow, and screen-reader
     checks on the same page set used for the readability audit.
   - Advance #48 and #4 as separate Track A accessibility work, not bundled into
     theme CSS.

6. **Publishing/media defaults**
   - Revisit `scripts/notion-to-wp/wp_blocks.py` once the content primitives are
     stable.
   - Bound inline images by default unless explicitly wide or full.
   - Preserve the existing block helper API.

## Next Work Session

Start with:

```bash
git fetch --prune
git status --short --branch
gh pr view 272 --json number,title,isDraft,state,mergeStateStatus,statusCheckRollup,url
make status-readonly
```

Then choose one lane:

1. Review and merge PR #272 if the production-source parity still matches.
2. Finish the #125 Critical CSS / Lighthouse evidence gate.
3. Start #122 with one page family, preferably Work/About/Speaking, using
   screenshots and page snapshots before any live writes.
