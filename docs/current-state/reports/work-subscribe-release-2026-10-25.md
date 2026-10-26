# Work card and KRÜG Subscribe repair

Applied October 25, 2026, under Kris's instruction to fix the Work card image/contrast and make Subscribe feed his KRÜG list. Follow-up to the findings in #1115; delivery PR #1144.

## Live result

- **Work, page 2672:** the BC + AI card now uses the existing 1200×800 site-hosted JPEG. WordPress serves it through its image proxy, and the rendered image decodes successfully. The card's title and description use cream text on an opaque dark panel; compact typography leaves the image visible on mobile. All added CSS targets `#kk-work-bcai-card`, using the theme's existing color variables so its layered color rules remain consistent. The destination, wording and other cards are unchanged.
- **Subscribe, page 2808:** the unidentified legacy iframe is replaced with the existing Aurora primary button to [KRÜG's hosted signup](https://vancouver.beehiiv.com/subscribe). The previously empty WordPress title is now “Subscribe to KRÜG”; the template renders the page's single H1. The body contains only the introduction and button.
- Beehiiv provider readback identifies `vancouver.beehiiv.com` as KRÜG. Clicking the button on the live [Subscribe page](https://kriskrug.co/subscribe/) opened the KRÜG-branded email signup form in the browser. No subscription was submitted, and no provider or analytics configuration changed.

Work's write was content-only. Subscribe's final write changed content and its empty title. Both retained their ID, slug, published status, featured media, template, original date, author and permalink. No shared theme file was deployed.

## Verification

- Varlock-injected authenticated slug/ID and SHA-256 preflight passed before each write. Exact content readback and unchanged-field assertions passed after each write.
- Final public check: **October 25, 5:01 p.m. PDT** (`2026-10-26T00:01:21Z`): both normal and fresh requests to both pages returned 200 with the intended content. Work's normal request was already a cache hit. No manual cache purge was needed.
- Four live browser cases: Work and Subscribe at 1440×1050 and 390×844. Both pages fit their viewport and preserve visible keyboard focus. Work text contrast is **14.88:1**. The Subscribe button is over 49 px high at both widths. Work's full-page height is unchanged on desktop and 4 px shorter on mobile after the card typography repair.
- `make python-test PYTHON=/Users/kk/Code/kriskrug-wp/scripts/notion-to-wp/.venv/bin/python`: **1,107 passed** (184 publisher, 843 operations, 12 inventory, 68 SEO). The seven focused content-payload tests, changed-file Ruff, docs truth, scoped voice check and `git diff --check` passed.
- The initial CI run rejected a body-owned H1. The correction puts the heading in the existing WordPress title field and preserves the body-only contract. Work's narrow inline-style allowance is paired with a check that every selector stays inside its one card; the broader public-content checks remain intact.

[Rendered browser evidence](work-subscribe-verification-2026-10-25.json) records the final geometry, image dimensions, computed colors, destination and focus results. Screenshots and full authenticated snapshots remain private.

## Recovery

The original checkout retains `.generated/current-state/work-subscribe-2026-10-25/`: before/after snapshots, exact diffs, manifests, dry-run and apply receipts, final title-correction receipt, public HTML and screenshots. `apply.py --rollback` restores both original pages, including Subscribe's original empty title; `--page 2672` or `--page 2808` selects one. Run through Varlock with the existing Python runtime. Rollback verifies the current final content hash and title first, so it will refuse to overwrite a later edit.

Canonical sources: [Work](../../../content/source-packs/content-architecture-2026/wp-payloads/work.html) and [Subscribe](../../../content/source-packs/content-architecture-2026/wp-payloads/subscribe.html). The Work source change is surgical; unrelated differences between its historical package and today's live page were not republished.
