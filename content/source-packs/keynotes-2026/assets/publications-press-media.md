# Publications press media

Status: proposed review set for the Publications page overhaul. The payload uses
local relative paths so the branch is self-contained and cannot hotlink publisher
servers. It is not ready to paste into WordPress.

## Proposed publication set

These are contextual screenshots of the coverage, plus one published interview
thumbnail. They show the outlet and editorial context instead of presenting a
third-party photograph as if it were a KrisKrug.co asset.

| Local file | Published source | Context and credit | Decision |
|---|---|---|---|
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

## Publication gate

1. Kris approves the six-file media set above.
2. Upload only the approved files to the KrisKrug.co WordPress Media Library.
3. Preserve outlet and photographer credits in attachment captions where visible.
4. Replace every relative image `src` with its uploaded WordPress media URL.
5. Confirm that no `../assets/` paths or third-party image URLs remain.
6. Snapshot page `1895` through authenticated `context=edit` before writing.
7. Review an exact dry-run diff against the current published page.
8. Apply only after exact target and publish approval.
9. Verify the cache-bypassed public page on desktop and mobile.
10. Keep the page snapshot as the rollback source.

All 47 coverage links were rechecked during the July 2026 review pass. Media
approval is separate from layout approval and public-publish approval.
