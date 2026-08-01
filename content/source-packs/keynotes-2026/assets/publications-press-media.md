# Publications press media

Status: **Aurora paper tear-sheet media checklist** (2026-08-01).
The July 2026 dark neon draft skin is **superseded**. Local relative paths keep
the branch self-contained; they must be rewritten to WordPress Media Library
URLs before any live paste/PATCH. Not ready to paste into WordPress until KK
approves the media set and the dry-run diff.

## Local asset confirmation (2026-08-01)

All seven press files exist under this directory:

| Local file | Bytes (approx) |
|---|---|
| `press-2026-07-31-biv-ecosystem-context.jpg` | 245070 |
| `press-2026-07-24-the-tyee-context.jpg` | 78954 |
| `press-2026-06-15-biv-context.jpg` | 87250 |
| `press-2026-05-20-storyhive.jpg` | 91465 |
| `press-2026-02-09-tela-viva-context.jpg` | 50314 |
| `press-2025-07-09-e-channelnews-context.jpg` | 51972 |
| `press-2025-05-01-portfolio-yvr-context.jpg` | 105581 |

## Proposed publication set

These are contextual screenshots of the coverage, plus one published interview
thumbnail. They show the outlet and editorial context instead of presenting a
third-party photograph as if it were a KrisKrug.co asset.

| Local file | Published source | Context and credit | Decision |
|---|---|---|---|
| `press-2026-07-31-biv-ecosystem-context.jpg` | [Business in Vancouver](https://www.biv.com/news/technology/bc-groups-push-to-build-a-stronger-ai-ecosystem-12601298) | Article-page screenshot; the visible article photograph is credited to Rob Kruyt / BIV | Captured 2026-07-31; pending Kris media approval (not auto-approved) |
| `press-2026-07-24-the-tyee-context.jpg` | [The Tyee](https://thetyee.ca/News/2026/07/24/Who-Gets-Say-AI-Adoption/) | Article-page screenshot showing The Tyee masthead, headline, byline, and story context | Proposed after explicit media approval |
| `press-2026-06-15-biv-context.jpg` | [Business in Vancouver](https://www.biv.com/news/economy-law-politics/bc-lawyers-face-ai-driven-shakeups-in-legal-work-12415161) | Article-page screenshot; the visible article photograph is credited to Rob Kruyt / BIV | Proposed after explicit media approval |
| `press-2026-05-20-storyhive.jpg` | [TELUS STORYHIVE / Haus of Owl](https://www.youtube.com/watch?v=sxDwQRTZfCA) | Published interview thumbnail | Proposed after explicit media approval |
| `press-2026-02-09-tela-viva-context.jpg` | [Tela Viva News](https://telaviva.com.br/09/02/2026/festival-waiff-aborda-o-uso-da-inteligencia-artificial-no-mercado-audiovisual/) | Article-page screenshot showing the headline and credited WAIFF artwork | Proposed after explicit media approval |
| `press-2025-07-09-e-channelnews-context.jpg` | [E-ChannelNews](https://www.e-channelnews.com/interview-with-kris-krug-at-channelnext-central-2025/) | Article-page screenshot showing the outlet masthead and interview headline | Proposed after explicit media approval |
| `press-2025-05-01-portfolio-yvr-context.jpg` | [Portfolio.YVR](https://portfolioyvr.com/2025/05/kris-krug-taking-ai-and-art-to-new-heights-with-future-proof-creatives/) | Article-page screenshot showing the published profile context | Proposed after explicit media approval |

## Excluded from the publication set

- The Tyee protest photograph sourced through Facebook
- The standalone Rob Kruyt / BIV portrait
- The CBC illustrative story image
- Standalone Portfolio.YVR and FOLIO.YVR photographs
- The Compass portrait until ownership is confirmed
- The Tyee-submitted Kris photograph until its photographer and reuse rights are confirmed

The raw copies above were removed from this branch. Contextual screenshots still
contain copyrighted source material. Their use on a press-clippings page requires
Kris's explicit editorial approval and appropriate attribution.

## WP upload + path rewrite checklist (prepare only until KK approves)

1. Kris approves the seven-file media set above (**explicit media approval**).
2. Upload only those seven files to the KrisKrug.co WordPress Media Library.
3. Preserve outlet and photographer credits in attachment captions where visible.
4. Record each `attachment_id` + CDN `source_url` beside the local filename.
5. Replace every relative image `src` (`../assets/press-…`) with its uploaded URL.
6. Confirm every `<img>` still has matching `data-media-key`, `alt`, `width`, `height`.
7. Confirm that no `../assets/` paths or third-party image URLs remain in page raw.
8. Snapshot page `1895` through authenticated `context=edit` before writing.
9. Review an exact dry-run diff against the current published page.
10. Apply only after exact target and publish approval.
11. Verify the cache-bypassed public page on desktop and mobile.
12. Keep the page snapshot as the rollback source.

**Do not upload or PATCH in this lane without KK go-ahead.** Helper:

`varlock run --path .env.schema --inject vars -- python3 scripts/deploy_publications_tearsheet.py --dry-run`

Coverage inventory was reconciled 2026-08-01 (see
`../verification/PUBLICATIONS-KB-GAP-REPORT-2026-08-01.md`). Media approval is
separate from layout approval and public-publish approval.
