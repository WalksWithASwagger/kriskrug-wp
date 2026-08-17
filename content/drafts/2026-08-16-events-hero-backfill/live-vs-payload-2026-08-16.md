# Live vs prepared payload — page 2250 `/events/` (2026-08-16)

Read-only diagnosis for [#635](https://github.com/WalksWithASwagger/kriskrug-wp/issues/635).
**No live write.** Do **not** close #635: the hero backfill has not shipped.

Fetched 2026-08-16 (logged out):

- `GET https://kriskrug.co/wp-json/wp/v2/pages/2250` → id **2250**, slug `events`, status `publish`, `modified` **`2026-08-10T10:38:46`** (`2026-08-10T18:38:46Z`)
- `GET https://kriskrug.co/wp-json/wp/v2/pages?slug=events` → exactly one page, id 2250
- Cache-bypass HTML `https://kriskrug.co/events/?cb=…` HTTP **200**
- Live theme `style.css` Version **1.6.5** (repo `main` may differ; do not treat repo Version as production proof)
- Public REST rendered body: [`live-content-rendered-2026-08-16.html`](./live-content-rendered-2026-08-16.html)
  (diagnosis only; not a restore source — public REST has no `content.raw`)

## What the “prepared payload” actually is

There is **no** ready-to-POST HTML that already contains the ledger heroes.

| Artifact | Role | Shipped to live? |
|---|---|---|
| `scripts/events_page/events-catalog.yaml` | SSOT for dated cards | **Yes** — 66 public ids match live, same order |
| `scripts/events_page/render_events_page.py` + `shell-events-2250.html` | Page generator | **Yes** — dry-run HTML matches live cards/images/empties |
| `scripts/events_page/heroes/LEDGER-2024-2025.md` (#632, merged PR #647) | Research ledger, 16 one-off rows | **No uploads** |
| `scripts/events_page/heroes/LEDGER-2026-MEETUP.md` (#633, merged PR #648) | Research ledger, 34 meetup/one-off rows | **No uploads** |
| `scripts/events_page/out/events-2250.generated.html` | Gitignored dry-run of *current* catalog | Matches live; **does not** include ledger heroes |

#592 (archive backfill) closed complete on 2026-08-02. This issue is the **hero** successor. Catalog facts are live. Card art from the ledgers is not.

## Live vs current catalog render (2026-08-16)

Same 66 `data-event-id` values, same order. Generated HTML from `main` and live REST body agree on every id, every empty card, and every image card. The remaining work is **not** a body-swap of a finished file; it is media + catalog `image.media_id` + re-render + POST.

| Check | Live 2250 | Current catalog render | Ledger-backed ship (not rendered yet) |
|---|---|---|---|
| REST `modified` | `2026-08-10T10:38:46` (IIDA Coffee add) | n/a | n/a |
| Public dated cards | **66** | **66** (`trunorth-ai-leadership-summit-2026` stays `proposed`, skipped) | same ids; more `<img>` |
| `aurora-event-compact-media--empty` | **49** | **49** | must drop vs 2026-08-02 baseline of **48** (today is *up* one) |
| Cards with an `<img>` | **16** | **16** | 16 + approved ledger attaches/uploads |
| `file:///` | **0** | **0** | must stay 0 |
| TruNorth speaking claim | **absent** (row not public) | skipped | stay skipped / art-free |
| Upcoming ids | IIDA Coffee, Pitch Night, Sep 30 meetup, Futureproof | same four | Sep 30 may gain a Luma cover if KK approves |
| All 16 live event `<img>` URLs | HTTP **200** | same 16 media ids | new uploads must 200 after apply |

`data-event-end` substring count on the rendered body is **70** because the rolloff script mentions the attribute; there are **66** dated cards, each with the attribute.

## Already shipped (do not redo)

- #592 archive backfill: 66 public cards, no `file://`, no TruNorth claim
- Render-contract tests (#631, closed 2026-08-03): 32/32 pass on this session
- Hero *research* ledgers (#632 / #633, both closed 2026-08-03)
- 16 catalog rows that already have `image.media_id` (12660–12716 range plus Pitch Night 12660) and matching live `<img>`s
- 2026-08-10 exclusive write of `iida-thermador-coffee-conversations-2026` onto page 2250 (`modified` 2026-08-10). That is a catalog-card add, **not** the hero backfill. Do **not** restore from `backup/20260801-events-backfill-ship/` as if it were current live.

## Still waiting (this issue)

Live-empty cards that already have a **sourced** ledger candidate (21 from the 2026 ledger headings, plus the 11 sourced 2024/2025 one-offs). None of those candidates are on live.

Lowest-risk attach-only rows (existing kriskrug.co media, confirm ID before writing catalog):

| Event id | Probable media ID (from public post HTML; confirm via REST) |
|---|---|
| `2025-03-20-data-storytelling-hackathon` | 8675 |
| `bcama-vision-conference-panel-2024` | 5740 |
| `enya-liftoff-keynote-2024` | 6964 |
| `innovate-west-keynote-2024` | 5360 |
| `yorkton-film-festival-panel-2024` | weak `og:image` template; look at media 5682–5687 first |

Skip until KK says otherwise (`NO SOURCE` / no license / TruNorth):

- 2024/2025: Indigenomics, EA keynote, AMD workshop, DAMA Day, ADPList (organizer art, no license)
- 2026: TruNorth, FIRST Tech Challenge, Vibe Working, Sea to Sky gondola, Global AI Summit panel, YVR Welcome Salon, SFU AI panel

KK decision gates that still block a full empty-count drop are listed in `LEDGER-2026-MEETUP.md` § “Blockers and decision gates” (photographer courtesy checks, series-fallback 2024 frames, meetup #24 credit/date, TED2025 fetch path, AEFL wrong-night photo, provisional alts).

## `blocked` label

Repo dependencies named on the issue (#631, #632, #633) are **closed**. The label is stale as a *code* blocker. The remaining gate is KK approval of the hero set, which #635 already records. Keep the issue **open**. Swap `blocked` for human-gated review if the board uses that signal; do not treat the issue as closeable.

## Recommendation

Keep #635 open. Run [`APPLY-RUNBOOK.md`](./APPLY-RUNBOOK.md) only after KK comments the approved row set (and the photographer / series-fallback rulings). Closing now would strand the ledgers with no live apply owner.
