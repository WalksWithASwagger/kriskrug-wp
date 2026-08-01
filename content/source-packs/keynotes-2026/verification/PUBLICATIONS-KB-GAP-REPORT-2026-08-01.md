# Publications KB gap report — 2026-08-01

Status: research complete for Aurora paper tear-sheet wave. No live write.

Sources compared:

- `kk-kb/meta/reports/press-clippings.json` (47 rows; last mtime observed 2026-07-31)
- `kk-kb/content/people/kris-krug/sources/press.md`
- `kk-kb/.../press-and-media/press-clippings/README.md` (+ “Coverage tracked elsewhere”)
- `kk-kb/.../press-and-media/power-50-2026-retrospective.md`
- Repo payload `content/source-packs/keynotes-2026/wp-payloads/publications.html`
- Live cache-bypass `https://kriskrug.co/publications/` (2026-08-01): still `.kk-publications`, `#00e5ff` / `#ff6a6a`, essentially zero press graphics

Notion Public Presence sync was not required for this pass; kk-kb inventories were sufficient.

## Verdict

Payload inventory matches the 47-row clippings index (URL form differences only: archive.org wrappers for Popular Science / Vancouver Is Awesome / Vancouver Sun). Live page is the outdated dark neon island and is not the coverage source of truth.

## Vancouver Magazine Power 50 — decision

**Add to the tear sheet as a dated feed row** (recognition, no screenshot this wave).

| Fact | Detail |
|---|---|
| What it is | One civic recognition: Vancouver Magazine Power 50 (2026 list) |
| Public URL | https://vanmag.com/city/power-50/introducing-vancouver-magazines-2026-power-50-list/ |
| Date on page | `2026-02-05` (gala / list unveil; embargo lift Feb 6) |
| Why missing from JSON | By design — kk-kb tracks it under “Coverage tracked elsewhere” / retrospective, not as a `press-clipping` row |
| Why `press.md` says 2025 | Nov 2025 award letter + blurb opener; same recognition (see retrospective year-label note) |
| Individual feature URL | Still TBD in kk-kb — do not invent a deep-link |

**Do not** add a second Power 50 row for “2025”. **Do not** force it into `press-clippings.json` from this WP lane; that is a kk-kb indexing choice.

## Gaps and dispositions

| Item | Evidence | Disposition |
|---|---|---|
| Power 50 (2026) | press.md + retrospective + vanmag list URL | **Add** text row on publications tear sheet |
| CBC BC holiday shopping (~2025-11-28) | Clipping entry `status: verify`, URL `pending:…` | **Defer** until aired URL confirmed; belongs on Media Appearances / broadcast once locatable |
| CBC “Sandboxing AI” Early Edition series | Tracked under broadcast-interviews elsewhere | **Leave** on Media Appearances post; not a publications clipping |
| Bossier Magazine Q&A (2026-02-03) | Tracked elsewhere in kk-kb | **Defer** (interview home elsewhere; no public URL confirmed in this pass) |
| Own-site STORYHIVE recap URL in JSON | `kriskrug.co/2026/06/17/storyhive-…` | **KB-only** companion; tear sheet already links the YouTube primary |
| Issuu Folio.YVR Issue 26 | Related media under press.md Portfolio section | **KB-only**; Portfolio.YVR profile already on tear sheet |
| Portfolio.YVR Web Summit 2026 passim mention | Light web pass hit | **Defer** — name-check inside event roundup, not dedicated coverage |
| CBC Web Summit Vancouver player clip | Light web pass hit | **Candidate only** — confirm air credit/URL before adding; likely Media Appearances |

## Light web pass (2025–2026 candidates only)

Searched for Kris Krug / Kris Krüg / BC + AI coverage on BIV, Tyee, CBC, Portfolio.YVR. Known Tyee / BIV / Portfolio.YVR pieces already inventoried. No new dedicated clip found that is ready to invent into the tear sheet. Candidates above stay candidates until URL + role are verified in kk-kb.

## Live vs payload markers

| Marker | Live 2026-08-01 | Paper tear-sheet payload |
|---|---|---|
| `.kk-publications` | present | forbidden |
| `#00e5ff` / `#ff6a6a` | present | forbidden |
| `--press-night` / dark neon skin | n/a (live uses kk-publications) | removed from draft |
| Press `<img>` count | ~0 content images | 7 with `data-media-key` |

## Follow-up only (not this ship)

Other keynotes payloads still carry cyan/hot leftovers (`about.html`, `work.html`, `services.html`, `podcast-guesting-page-epk.html`, `responsible-ai-professional.html`). Track as a separate Track A cleanup inventory; out of scope for publications tear-sheet PR.

Also: regenerate `press-clippings.json` from kk-kb when CBC holiday (or other `verify` rows) get real URLs — JSON currently omits the pending CBC holiday entry even though the markdown clipping exists.

## Reciprocal links to preserve

- EPK / media kit: `/podcast-guesting-page-epk/`
- Media Appearances: `/2026/07/02/ai-media-appearances-podcast-guesting/`
