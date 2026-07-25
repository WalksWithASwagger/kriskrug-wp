# Aurora 1.4.3 — e2e spot check (2026-07-24)

## Verdict

**Pass.** R5 left-pinned header + R6 rainbow/riso accents live on cream Revive chrome.

## Deploy

- Zip: `kk-aurora-revive-r5r6-1.4.3-1.4.3-20260725.zip`
- SHA256: `879a17e8cc371ba52f12bec5af3849eab2259e87218a9b45b55c8f57a141e7d4`
- Media **#12636**; one-shot snippet **#20** (inactive); option `kk_aurora_sync_143`
- Public `style.css` Version `1.4.3`; `revive-port.css` contains R5/R6 markers

## Checks

| Check | Result |
|---|---|
| Brand X on ~2535px viewport | **36px** (was ~651 inside centered 1280 shell) |
| Header shell `max-width` | `none` (full-bleed) |
| Rainbow word font-size | **129.6px** (~1.08× of 120px H1) |
| Section-head `::after` riso | 3px gradient present |
| Skip link / cream meta | unchanged from 1.4.2 |

## Rollback

Re-extract prior theme zip (1.4.2 media **#12635**) or restore from git tag/commit before 1.4.3.
