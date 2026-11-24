# Data-centre reading guide redesign (page 13069)

Status: preview only. Not applied to the live page.

- Live page: https://kriskrug.co/data-centres-public-compute-and-the-public-interest/ (page 13069)
- Preview draft: page 13079, `https://kriskrug.co/?page_id=13079&preview=true` (draft, needs a logged-in session)
- Share graphic: Canva design `DAHb2eq1NCQ` (1200 x 630), photo 12629 as a full-height right panel. Edits are held in an open Canva transaction until Kris approves.

## What changed

The page content is rebuilt from the live content with no factual edits:

- Dark full-bleed hero with the H1, the intro text and portrait 12629 (arms crossed, cap, teal glasses) as a plain rounded photo. Kris chose this photo over portrait 2682 and asked for no arch frame. The theme's own page title is hidden on this page only (`body:has(.dc-guide)`), so there is still one visible H1.
- "The ask, in three parts" strip. Its wording is taken from the first card's summary and the intro.
- Eight cards in three colour-coded chapters (rust, blue, pink). Each card has a number, a source and date line, a "Start here" badge where the live page had one, the existing screenshot (media 13071 to 13078) in a browser-frame treatment, the title link and the summary. The whole card is clickable through the title link, so each card has one link.
- The Watch section keeps the YouTube embed, its caption and both recording links, in a dark band.
- The JSON-LD block is byte-identical. All ten links are unchanged. Slug, SEO title, meta description and canonical are untouched because only `content` is replaced.

The CSS is inline in a `wp:html` block and scoped to `.dc-guide`. No theme, snippet or plugin change.

## Theme gotchas found

- kk-aurora forces paragraph colour with `!important` through `--aurora-ink-soft` and `--revive-ink-soft`. The CSS sets those variables per element instead of fighting specificity.
- Heading colour is set inside a cascade layer, which outranks unlayered `!important`. Light headings on dark bands use `-webkit-text-fill-color`.
- The REST client refuses characters outside cp1252. Arrows, ticks and the play triangle are CSS escapes.

## Checks run on the preview (2026-11-24)

- All 86 blocks load as valid in the block editor.
- Heading order: one visible H1, H2 chapters, H3 cards.
- Every image has alt text, a srcset and Photon resizing. Cards below the fold lazy-load. The portrait gets `fetchpriority="high"` and loads at the 682 x 1024 size with a srcset, instead of the 2000 px original the live page uses.
- WCAG contrast: every text pair passes AA. The lowest is 4.86:1.
- At 390 px wide there is no horizontal scroll and the cards stack to one column.

## Files

- `content.raw.html`: the live content of page 13069 as of 2026-11-24 17:07 UTC. This is the rollback copy and the input to `build.py`.
- `guide.css`, `build.py`: source. `python3 build.py` writes `content.new.html`.
- `content.new.html`: the proposed page content.
- `share-graphic-preview.png`: preview of the Canva graphic.

## Apply (after Kris approves)

1. Replace the `content` of page 13069 with `content.new.html` (REST `POST /wp/v2/pages/13069`).
2. After the share graphic is approved, export it from Canva as a 1200 x 630 JPG, upload it, and set it as the page's `featured_media`. That replaces media 12908 as the og:image.
3. Purge the page cache and check the live page, then trash draft 13079.

Rollback: post `content.raw.html` back to page 13069 and set `featured_media` to 12908.
