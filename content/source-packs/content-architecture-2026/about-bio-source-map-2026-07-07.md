# About / bio source map — 2026-07-07 (refreshed 2026-07-08)

Status: agent-safe research packet for #307. Feeds #290, #270, #269.  
No WordPress write or About payload edit was performed.

## Baseline (source of truth)

Current live About page and the architecture payload should remain the baseline:

- Live: https://kriskrug.co/about/ (HTTP 200)
- Payload: `content/source-packs/content-architecture-2026/wp-payloads/about.html`

Current public sections:

1. About / lead
2. The rooms I am in now (BC + AI, keynotes, visual storytelling, Creative AI systems)
3. Public trail
4. Start with the work / Contact

Do **not** treat older keynotes About payloads as source of truth. Use them as an idea bank only.

## Claim inventory

| Claim / story | Source | Confidence | Suggested placement | Notes |
|---|---|---|---|---|
| Photographer, creative technologist, community builder, speaker | Live About + `about.html` | Confirmed | Keep in lead | Already live |
| Two decades documenting technology, art, activism, conferences | Live About + `about.html` | Confirmed | Keep in lead | Already live |
| BC + AI Ecosystem work | Live About card + https://bc-ai.ca/ | Confirmed | Keep in rooms grid | Already live |
| AI keynotes / workshops / CreativeMornings Vancouver | Live About + Punk Rock AI portal | Confirmed | Keep in rooms grid | Already live |
| Visual storytelling / photography archive | Live About + `/photography/` | Confirmed | Keep in rooms grid | Already live |
| Creative AI systems / Both Hands Full | Live About + https://www.bothhandsfull.com/ | Confirmed | Keep in rooms grid | Already live |
| Public trail names: National Geographic, CBC, TEDxOilSpill, Midway Journey, SXSW, Olympics | Live About Public trail card | Confirmed as currently published | Keep; do not expand into long lists in first slice | Already live; avoid new unverified client lists |
| Musqueam, Squamish, and Tsleil-Waututh land acknowledgment in site chrome/footer bio | Live About page chrome text | Confirmed as currently published site language | **Not** for first About body slice; #22 / #290 decide placement later | Do not invent new acknowledgment wording |
| 2013 pilot school story | https://kriskrug.co/2013/09/14/pilot-school-flying-in-the-direction-of-my-dreams/ (WP ID 1975) | Confirmed story exists | Candidate “From the archive” module | Use as story material; do not invent credentials |
| Exact recurring credential “licensed private pilot” | Not re-verified from a current primary bio source in this pass | Needs KK review | Only if KK confirms exact wording | Marked needs-KK-review |
| 2015 aerial photography bridge | https://kriskrug.co/2015/09/08/aerial-photography-combining-my-loves-for-flying-and-making-photos/ (WP ID 2213) | Confirmed story exists | Pair with pilot-school story | Tool learning + human eye bridge |
| COP15 / climate movement media | https://kriskrug.co/2009/12/14/photo-essay-inside-the-negotiations-cop15/ (WP ID 1547); streets essay WP ID 1558 | Confirmed archive posts | Optional “Movement media” proof point | Keep focused; one or two links max |
| TEDxOilSpill as movement media | Named on live About Public trail | Confirmed as currently published name | Optional proof point | Prefer linking only if a stable public URL is chosen by KK |
| Early web/community organizing → Vancouver AI → BC + AI | Live About + Zero to One post https://kriskrug.co/2026/06/30/zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey/ | High for narrative arc; details need editorial trim | Candidate “Before AI, there was community” module | Do not invent founding dates/titles |
| LaSalle / Both Hands Full teaching room | Draft/local packs + keynote assets | Medium | Later slice, not first | Avoid until KK picks the exact proof post/page |
| Long publication/client/person lists | Archive mining temptation | Discard/avoid for first slice | — | Inflates bio; conflicts with “Receipts over adjectives” |

## Buckets

### Confirmed facts (safe to keep / lightly extend)

- Current About lead and rooms grid.
- Public trail framing already live.
- Pilot-school post (2013) and aerial-photography post (2015) exist and are public.
- COP15 photo essays exist and are public.
- Zero to One / Vancouver AI community arc is public.

### Needs KK review

- Any “licensed private pilot” or similar credential phrasing.
- Whether Indigenous land acknowledgment belongs in the About body vs remaining in site chrome (#22).
- Whether TEDxOilSpill / COP15 should become linked proof cards or stay named-only.
- Any new stats, titles, client names, or award claims not already on the live About page.

### Discard / avoid in first slice

- Author-bio REST field edits.
- REST `title` changes.
- Long archive dumps, client lists, or publication bibliographies.
- Rewriting the rooms grid from scratch.
- Land acknowledgment rewrite without KK.

## Smallest next implementation slice for #290

Add one compact **“From the archive”** module after `Public trail` and before `Start with the work`, body-only:

1. **Flying in the direction of the work** — pilot school + aerial photography, framed as tool learning plus human eye. Link the two archive posts above.
2. **Before AI, there was community** — early web/community organizing → Vancouver AI → BC + AI. Link Zero to One and/or BC + AI.
3. **Movement media** — TEDxOilSpill and COP15 as focused proof points, not a gallery dump.

Keep the existing title. Snapshot `/about/` before any write. Dry-run the payload. No publish without KK approval.

## Verification commands / URLs used

```bash
curl -sI https://kriskrug.co/about/
curl -fsSL https://kriskrug.co/wp-json/wp/v2/posts/1975?_fields=id,slug,link,status
curl -fsSL https://kriskrug.co/wp-json/wp/v2/posts/2213?_fields=id,slug,link,status
curl -fsSL https://kriskrug.co/wp-json/wp/v2/posts/1547?_fields=id,slug,link,status
curl -fsSL https://kriskrug.co/wp-json/wp/v2/posts/12034?_fields=id,slug,link,status
```

Local files reviewed:

- `content/source-packs/content-architecture-2026/wp-payloads/about.html`
- `docs/current-state/CATEGORY-MAPPING-MISC-2026-06-14.md`
- `content/source-packs/keynotes-2026/` (idea bank only)
