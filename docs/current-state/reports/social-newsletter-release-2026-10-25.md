# Social attribution and KRÜG newsletter routing

Applied October 25, 2026, under Kris's instruction to finish #1024 and fix the
newsletter links to his KRÜG list. Related conversion work remains in #1090.

## Exact release

- At 22:45 UTC, changed the two Aurora `twitter:site` values to `@kriskrug`
  and the shared footer link to `https://x.com/kriskrug`. Authenticated inventory
  confirmed snippet 12 is inactive; it was left inactive and unchanged.
- At 22:47 UTC, changed 13 personal signup destinations from the old Beehiiv
  hostname to `https://vancouver.beehiiv.com`, preserving `/subscribe` where
  present. Provider readback identifies that host as **KRÜG**; the old
  `kriskrug.beehiiv.com` host belongs to **BC + AI Ecosystem**.
- The newsletter write set was five theme files (header, footer, front-page,
  home and utility pattern), custom front-page template 12661, pages
  **2418, 2828, 3603**, and posts **2950, 3219, 6896**. Only destination strings
  changed. Slugs, status, copy, media and historical `/p/...` article links
  were preserved. The Contact source payload now agrees with live.
- No signup submission, analytics event, GA4 configuration or Beehiiv provider
  mutation occurred. This does not complete #1090's conversion implementation.

The legacy `/subscribe/` page (2808) contains an iframe with embed ID
`552dc13c-76df-4a0b-9663-b7e668042177`. The provider's current form lookup does
not resolve it and its HTTP endpoint challenges automated requests. This does
not prove the legacy form is broken or identify its publication. It remains
unchanged pending a supported ownership check; all corrected navigation and
signup links go directly to the verified KRÜG host.

## Verification

- The social rendering regression failed with `@feelmoreplants` before the
  change and passed afterward, including exactly one attribution tag.
- Publisher/operational/SEO Python suites: **1,106 passed**. JavaScript
  behavior, theme and plugin smoke tests passed. All 54 PHP files passed syntax.
- Docs truth, changed Python Ruff checks and `git diff --check` passed.
- PHPCS passed using the original checkout's existing Composer installation.
  The initial `make verify` run reached this gate but could not find PHPCS in
  the new worktree; `PATH=/Users/kk/Code/kriskrug-wp/vendor/bin:$PATH make
  validate` completed it. Initial sandbox-only fixture failures were rerun
  with worktree write access and passed.
- Live visual comparison: **8 PASS, 0 WARN, 0 FAIL**, Home, Writing, Contact
  and Speaking at mobile/desktop sizes. Heights unchanged. Baseline
  `20261025T224434Z`, comparison `20261025T224804Z`; the Writing desktop
  difference is 0.0255%, within the existing tolerance.
- All ten checked URLs returned 200 for both bare and fresh requests. Fresh
  responses have one `@kriskrug` tag, the corrected footer, and no old signup
  links. At the first post-release check, bare Speaking, Writing and the
  sample ALL IN article still carried earlier cached links. Application and
  cache delivery are separate; no manual cache purge is claimed.

## Recovery

The private operator packet is retained in the original checkout at
`.generated/current-state/social-newsletter-2026-10-25/`, outside the managed
worktree. It contains complete before snapshots, exact diffs, SHA-256 manifests,
apply receipts and `apply-social.py` / `apply-newsletter.py` with `--rollback`.
Every write verifies identity and the expected source hash; SFTP replacements
use verified temporary files and atomic rename. REST updates recheck slug/ID
and round-trip the exact body. Roll back newsletter before social because both
touch the footer. A third source hash is a concurrent edit, not permission to
overwrite it.

The live Aurora header remains 1.6.12. These bounded edits are not a full
deployment of the repository's 1.6.13 theme line.
