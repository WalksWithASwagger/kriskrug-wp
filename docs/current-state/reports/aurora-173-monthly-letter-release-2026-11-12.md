# Monthly KRÜG letter release: 2026-11-12

Kris ruled on 2026-11-12 that KRÜG becomes a monthly letter starting in
December (#1278) and approved each step below in chat. After this release no
public page promises a weekly email.

## Aurora 1.7.3 (theme)

- Merged as #1293. Footer tile, homepage newsletter band (theme file) and the
  `/blog/` eyebrow say monthly.
- Deployed over Pagely SFTP with the atomic swap at 18:29 America/Vancouver
  (2026-11-13 01:29 UTC). 67 files staged and swapped. The 1.7.2 rollback seat
  is `kk-aurora.bak-1794533392`; the 1.7.1 seat `kk-aurora.bak-1794531136` is
  also kept.
- Public `style.css` reads 1.7.3. `make check-live-parity` passes; `make wp7-smoke` 0 FAIL.

## Homepage database template

The live homepage uses a saved template (`kk-aurora//front-page`, wp_id 12661,
source custom) that overrides the theme file, so the theme deploy alone left
the band saying weekly. With Kris's approval of the exact change, four
single-occurrence swaps were written, identical to the 1.7.3 theme file:

| Before | After |
|---|---|
| `"ariaLabel":"Weekly email"` | `"ariaLabel":"Monthly letter"` |
| kicker `Weekly email` | `Monthly letter` |
| `Once a week on AI, creativity, and the rooms where...` | `Once a month on AI, creativity, and the rooms where...` |
| button `Get the weekly email` | `Get the monthly letter` |

The write was guarded: the live template hash had to equal the earlier
snapshot (`c9463d83761a`) before the POST. Sent and stored hashes both read
`23d22c9ccd23`. Before and after JSON are kept locally under the ignored
`.generated/current-state/aurora-173-release-2026-11-12/`. Rollback: POST the
before body back to `templates/kk-aurora//front-page`.

## Contact page (2418)

`scripts/content_architecture_deploy.py --page contact --execute` wrote the
#1289 payload. The dry run showed one line changing by +3 bytes ("a weekly
note" became "a monthly letter"). Snapshots, checksums and the deploy report
are in `backup/20261113T020650Z-content-architecture/` (the only email in them
is the public Contact address already on the page).

## Public check (logged out, canonical and cache-busted)

| Page | Newsletter wording |
|---|---|
| `/` | Monthly letter, Once a month (band), once a month (footer) |
| `/contact/` | monthly letter (body), once a month (footer) |
| `/blog/` | monthly letter |
| `/work/` | once a month (footer) |

No page returned "weekly email", "once a week" or "weekly note".

## Not done

- The pixel gate did not run (the cached Chromium build no longer matches the
  installed Playwright module; see the 1.7.2 receipt). Changes here are copy
  only.
- The first KRÜG send by December 17 stays with Kris (#1278).
