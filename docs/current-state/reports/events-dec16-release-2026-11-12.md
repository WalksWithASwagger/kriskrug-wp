# December 16 Vancouver AI Events release: November 12, 2026

Kris approved one live write to add the December 16 Vancouver AI meetup to /events/ ([#1102](https://github.com/WalksWithASwagger/kriskrug-wp/issues/1102)). The catalog row merged in [#1266](https://github.com/WalksWithASwagger/kriskrug-wp/pull/1266). Page **2250**, exact slug **events**, was updated through Varlock at **2026-11-13 01:34:03 UTC** (November 12, 18:34 Vancouver). It was one content-only POST. Title, slug, status, template and featured media were not sent.

## Published entry

- **Vancouver AI Community Meetup: December 2026**, December 16, 2026, Host & MC, linking to [the public Luma listing](https://luma.com/dec-vanai). There is no edition number, photograph or clock time, because none was given.

## What changed

Two fragments went into fresh authenticated `content.raw` and nothing else changed. The diff is 15 added lines and 0 removed lines:

1. The Upcoming card (14 lines), right after the November 25 card, which was the last card in `kk-ev-next-grid`. It is visible, card 3 of the 4-card limit.
2. The record row (1 line), first in the 2026 group, right before the November 25 row. It stays `hidden` until the browser passes 2026-12-17 00:00 Vancouver.

Counter values did not change. Rooms only count past events, and the row has no edition and no image.

The live body before the write was byte-identical to a render of the `main` catalog (at `352ddc0`) without the December 16 row. The body after the write is byte-identical to a render of the full `main` catalog. Both renders used a clock before the November 24 cutoff.

| Stored content | Before | After |
|---|---:|---:|
| Unique `data-event-id` | 86 | 87 |
| Upcoming cards (`kk-ev-next`) | 2 | 3 |
| Record rows (`kk-ev-rec`) | 86 | 87 |
| Contact sheet tiles | 41 | 41 |
| `<img>` elements | 42 | 42 |
| Year groups | 6 | 6 |
| Rooms / editions / frames | 84 / 33 / 41 | 84 / 33 / 41 |

## Hashes

- Before, `content.raw` SHA-256: `d354166f8b9746f33651ad3d0faeb65c798c23364b95e2eb2991485e8bd77100` (`modified_gmt` 2026-11-11T05:23:30).
- After, sent and stored, SHA-256: `454cbf2a526a95432372d51d6eb1f7c1cf6dc7e526f07418fdde58de6f15be03` (`modified_gmt` 2026-11-13T01:34:03).
- Pre-write snapshot: `page-2250-events-20261113T013245Z.json`, held privately and not committed.

## Verification

- Before the POST, page 2250 was read again. Its `content.raw` SHA-256 and `modified_gmt` still matched the snapshot, so no concurrent edit had happened.
- The authenticated readback equals the sent content exactly, with no normalization. The POST response stored the same hash.
- Logged-out public GETs of `https://kriskrug.co/events/` and `https://kriskrug.co/events/?cb=<epoch>` both returned 200. Both show the December 16 card once, visible, with date Dec 16 (`datetime="2026-12-16"`), the title above, role "Host & MC" and a Register link to `https://luma.com/dec-vanai`. The record row is present once and hidden.
- Public page: 87 unique event IDs (86 before, none missing, one added), 43 images, 41 tiles, counters 84 / 33 / 41. The canonical URL served the new HTML right away (gateway cache MISS), so no manual purge was needed.
- Not run in this lane: Chromium viewport checks against the live URL.

## Expected rollover

Rollover happens in the browser. The stored HTML does not change at the cutoffs.

| Browser clock (Vancouver) | Rooms | Visible Upcoming cards |
|---|---:|---|
| before 2026-11-24 00:00 | 84 | AMPA, Nov 25, Dec 16 |
| from 2026-11-24 00:00 | 85 | Nov 25, Dec 16 |
| from 2026-11-26 00:00 | 86 | Dec 16 |
| from 2026-12-17 00:00 | 87 | none, empty state with the Luma link |

## Rollback

Rolling back means posting the snapshot body back to page 2250. It is a live write and needs Kris's go-ahead. Run the preview first, then the guarded restore:

```
varlock run --inject vars -- python3 scripts/deploy_events_page.py --restore <page-2250-events-20261113T013245Z.json>
# preview: identity check, prints the live content sha256, no write
varlock run --inject vars -- python3 scripts/deploy_events_page.py --restore <same snapshot> --execute --expect-current-sha256 <sha from the preview>
```

The restore stops if the live hash changed after the preview. Once restored, the stored SHA-256 should be `d354166f...77100` again. If the snapshot is lost, a render of the catalog at `352ddc0` without the December 16 row, with `--now` before 2026-11-24, gives the same body. Check its hash before using it.
