# Links: verified destinations for `#stages`

Checked logged-out HTTP status on 2026-07-26. Prefer owned writeups/portals; YouTube when that is the public record.

## Recommended engagement set (homepage)

| # | Label | Primary href | Status | Fallback | Notes |
|---|---|---|---|---|---|
| 1 | CreativeMornings / Punk Rock AI | `https://www.punkrockai.com/` | 200 | `https://kriskrug.co/2026/05/04/punk-rock-ai/` | Portal is the hero destination; writeup supports SEO |
| 2 | LaSalle / Both Hands Full | `https://www.youtube.com/watch?v=-c7mgY2aSgM` | 200 | `https://www.bothhandsfull.com/` | Full keynote video; portal for world |
| 3 | ChannelNext | `https://www.youtube.com/watch?v=1OcC-0X6Nb8` | 200 | `https://www.e-channelnews.com/interview-with-kris-krug-at-channelnext-central-2025/` | Trade interview as secondary |
| 4 | Vancouver AI Meetup | `https://www.youtube.com/watch?v=T5ANAthZewE` | 200 | `https://vancouver.ai/` | Community stage proof |
| 5 | Web Summit Vancouver | `https://kriskrug.co/2026/05/07/web-summit-vancouver-2026/` | 200 | `https://kriskrug.co/2025/04/13/web-summit-vancouver-2025-survival-guide/` | Published writeup |
| 6 | Whistler Institute | `https://www.youtube.com/watch?v=-XEsqsEbpoo` | 200 | `/speaking/` | Ecosystem keynote tape |
| 7 | Bass Coast Brain Stage | `https://www.youtube.com/watch?v=owtSPcpRinI` | 200 | `/speaking/` | Festival / workshop range |
| 8 | Futureproof | `https://futureproof.website/` | 200 | `/speaking/` | Curator stage world; keep distinct from Work card if both remain |
| 9 | Both Hands Full portal | `https://www.bothhandsfull.com/` | 200 | `https://kriskrug.co/2026/01/24/both-hands-full/` | WAIFF / keynote world |
| 10 | Legacy UN / COP15 (optional) | `https://kriskrug.co/2009/12/14/photo-essay-streets-of-copenhagen-cop15-united-nations-climate-change-summit/` | 200 | omit | Only if KK wants archival depth on the homepage |

## Section chrome links

| Control | Href | Status |
|---|---|---|
| Speaking overview | `https://kriskrug.co/speaking/` | 200 |
| Book / contact | `https://kriskrug.co/contact/` | verify at build |
| Developing an AI Mindset portal | `http://developinganaimindset.com/` | 200 |
| Storyhive / Haus of Owl companion | `https://kriskrug.co/2026/06/17/storyhive-haus-of-owl-jordan-dack/` | 200 |
| Appearances index | `https://kriskrug.co/2026/07/02/ai-media-appearances-podcast-guesting/` | 200 |

## Current strip names: keep / replace

| Current span | Verdict | Replacement |
|---|---|---|
| TED | Replace | Omit, or TEDxOilSpill only with KK-approved URL |
| SXSW | Hold | Omit until a dedicated talk/writeup/video is attached |
| Adobe MAX | Remove | No public destination found |
| Web Summit | Keep (linked) | Use Web Summit Vancouver writeup above |
| FITC | Remove | No public destination found |
| MIT Media Lab | Remove | No public destination found |
| CreativeMornings | Keep (linked) | Punk Rock AI portal |
| UN | Replace | COP15 photo essay if legacy wanted; else omit |

## QA checklist (build time)

- [ ] Every `#stages a[href]` returns 200 logged out
- [ ] No hotlinked third-party images for primary tiles (YouTube thumbs OK only as temporary placeholders; prefer WP media)
- [ ] External links: `rel="noopener noreferrer"` when `target="_blank"` (prefer same-tab for owned sites)
- [ ] Re-run this table after any slug change

## Source inventory

- `content/source-packs/keynotes-2026/video-research/README.md`
- `content/source-packs/keynotes-2026/notion/keynotes-sanitized-snapshot.md`
- `content/source-packs/keynotes-2026/media-appearances/public-source-inventory-2026-05-19.md`
