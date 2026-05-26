# Aurora Homepage Role-Proof Polish - 2026-05-26

## Scope

Issue #12 needed the homepage hero to stop underselling the current work. Aurora `1.3.4` already fixed the old empty/duplicate H1 problem, so this pass stays surgical: preserve the keynote-first homepage and add the explicit role proof, metrics, and initiative links the issue asked for.

No WordPress REST writes were made in this pass. The homepage is theme-owned.

## Live Baseline

Public fetch of `https://kriskrug.co/?issue12=20260526` before edits returned:

- Status `200`.
- One H1: `Authored judgment in the age of generative everything.`
- Homepage markers included Indigenomics, The Upgrade, Vancouver AI, keynote, and photographer.
- Exact `BC+AI` marker was absent because the live page used `BC + AI`.
- The visible homepage did not yet carry the full issue #12 metric spine: `2,000+ members`, `$200B`, and `Fortune 500 training`.

The only missing image alt detected was a hidden Facebook tracking pixel, not a visible homepage image.

## Aurora 1.3.5 Changes

- Bumped `theme/kk-aurora/style.css` and `theme/kk-aurora/functions.php` from `1.3.4` to `1.3.5`.
- Updated `theme/kk-aurora/templates/front-page.html` hero copy to foreground:
  - Executive Director, BC+AI.
  - CTO, Indigenomics.ai.
  - Co-founder, The Upgrade AI.
  - 2,000+ BC+AI members.
  - $200B Indigenous economy work.
  - Fortune 500 training.
- Added Indigenomics.ai to the current-work card set with a direct CTA.
- Changed The Upgrade card copy/image to carry the co-founder and training proof more clearly.

## Verification

- `git diff --check` passed.
- Visible homepage card image URLs returned `200` image responses.
- Local template marker check found one `<h1>`, all new role/metric markers, and no visible `<img>` missing `alt`.
- `make wp7-smoke EXPECT_VERSION=6.9.4` passed against the currently live Aurora site before the `1.3.5` upload.
- Built `/Users/kk/Desktop/kk-aurora-homepage-role-proof-1.3.5.zip`.
- `unzip -t /Users/kk/Desktop/kk-aurora-homepage-role-proof-1.3.5.zip` passed.

## Remaining Live Gate

Issue #12 should close only after Aurora `1.3.5` is uploaded, caches are purged, and the public homepage is checked for:

- One visible H1.
- Hero proof links to BC+AI, Indigenomics.ai, and The Upgrade AI.
- Metrics visible in rendered source/text.
- Desktop and mobile layout without overflow.
- No broken visible images.
