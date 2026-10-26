# Publications alignment repair — October 25, 2026

The #1115 audit found horizontal overflow on Publications page **1895**. Its
full-width press panel started inside the constrained content column, extending
230 px past a 1440 px viewport and 16 px past a 390 px viewport. WordPress's
automatic margins overrode the panel's intended full-width positioning.

Under Kris's instruction to continue the remaining site repairs, a two-line
content-only change was applied through Varlock at **5:30:50 p.m. PDT**
(`2026-10-26T00:30:50Z`): add `alignfull` to `.kk-press`, then scope its existing
layout rule to `.kk-press.alignfull` so it takes precedence over the nested
global-padding rule. No shared theme file or CSS value changed.

## Verification

- Before each write: exact page ID, slug, publish status and raw-content match.
  After: exact saved body and unchanged title, dates, author, template, featured
  image, permalink and metadata.
- Text, all **69 links**, **40 images** and **40 figures** are unchanged.
- Normal and fresh public GETs returned 200 with identical HTML at 5:32 p.m. PDT.
- Actual post-save HTML rendered at 1440, 768 and 390 px with document width
  equal to viewport width. Desktop height remains 11,070 px; mobile is 19,229 px,
  four pixels shorter than the original. Keyboard focus remains visible as a
  solid 2 px outline. Desktop and mobile viewport captures were inspected.
- The seven content-payload checks and 20 Publications/media/neon-island checks
  pass. No new implementation-mirroring test was added for this two-line repair.

The [verification receipt](publications-layout-verification-2026-10-25.json)
contains source hashes, preserved-content counts and rendered geometry.
The canonical [payload](../../../content/source-packs/keynotes-2026/wp-payloads/publications.html)
has the same two surgical replacements; unrelated source/live differences were
not republished.

## Recovery

Private packet in the original checkout:
`.generated/current-state/kriskrug-closeout-2026-10-25/`. It contains the
authenticated snapshot, exact diff, dry-run/apply/readback receipts, public
HTML and before/preview/live screenshots. Run `apply-publications.py --rollback`
through Varlock to restore the original body only after the final source and
metadata guards pass. A later content edit stops the restore.
