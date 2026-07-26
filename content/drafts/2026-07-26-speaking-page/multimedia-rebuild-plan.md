# Multimedia rebuild plan - Speaking page (#419)

**Mode:** DRAFT ONLY. Curation gate for KK before any live apply.  
**Target:** page ID `1887`, slug `speaking`, URL https://kriskrug.co/speaking/

## Goals mapped to acceptance

| Acceptance | Plan |
|---|---|
| Media inventory documented for KK curation | Tables below |
| Stage photo or video visible without scroll at 1440 and 390 | Hero band: full-width stage photo **or** primary talk embed + booking CTA in first viewport |
| At least 2 embedded or linked talk videos | Primary embed in Watch section + secondary embed (or linked card pair with embeds) |
| Booking CTA above fold and at page end | Hero button + terminal CTA card, both → `/contact/` pending CTA-issue confirmation |

## Recommended page stack (media-first)

1. **Hero (above fold)** - stage photo (eager) + short claim + primary booking CTA  
2. **Watch** - two lazy YouTube embeds (no autoplay) with short labels  
3. **On stages** - 3 to 4 owned stage stills (library) as proof strip  
4. **Formats** - keep the four format cards (compressed)  
5. **Signature topics** - keep four topic cards; swap hotlinked images for library assets where possible  
6. **Book** - end CTA card

Optional later (out of scope for first apply unless KK asks): venue logo row, transcript pull-quotes, homepage Speaking section sync (#414 is Track B / separate).

## Video inventory (public, verified HTTP 200 on 2026-07-26)

Source index: `content/source-packs/keynotes-2026/video-research/README.md`.

| Rank | Pick | Title | URL | Duration | Why |
|---|---|---|---|---|---|
| **P0 embed** | Vancouver AI March 2026 | We Trained AI on Stolen Work... And I'm More Creative Than Ever | https://www.youtube.com/watch?v=T5ANAthZewE | 32:43 | Stage talk, high-response, creator-rights proof; already flagged P1 in media inventory |
| **P0 embed** | ChannelNext | The Future of Humanity: AI Keynote on Chaos & Creativity | https://www.youtube.com/watch?v=1OcC-0X6Nb8 | 33:26 | Clear "keynote" framing for buyers; shorter than LaSalle/Whistler |
| P1 alt | Bass Coast Brain Stage | Dear AI, Before We Go Any Further... We Need To Talk About Your Soul | https://www.youtube.com/watch?v=owtSPcpRinI | 40:07 | Festival / culture stage energy |
| P1 alt | LaSalle College | Both Hands Full: What Creatives Actually Need to Know About AI | https://www.youtube.com/watch?v=-c7mgY2aSgM | 1:19:34 | Strong talk; long for above-fold embed (better as linked secondary or Watch #3) |
| P2 | Whistler Institute | Inside Vancouver's AI Boom (and why it matters) | https://www.youtube.com/watch?v=-XEsqsEbpoo | 1:33:31 | Ecosystem depth; too long for primary embed |
| P2 | STORYHIVE / Haus of Owl | STORYHIVE On Location: Victoria - Kris Krug | https://www.youtube.com/watch?v=sxDwQRTZfCA | 1:19:50 | Produced interview, not a keynote stage; good EPK, weaker "hire the keynote" signal |
| Archive | Horizons series | Exploring AI Models... | https://horizons.compassdatacenters.com/series/exploring-ai-models-the-future-of-machine-learning/ | clips | Produced interview; link-out, not Speaking hero |

**Default embed pair for Option A payload:** Vancouver AI March 2026 + ChannelNext.  
**Swap rules:** KK may replace either with Bass Coast or LaSalle; keep at least two on-page.

### Embed implementation rules (evals)

- YouTube privacy-enhanced or standard embed with `loading="lazy"` on iframe.
- **No autoplay.** No muted-loop hero video that competes with LCP.
- Prefer a **still hero image** as LCP candidate; embeds sit in Watch (second band) so LCP stays on owned JPEG.
- Title each iframe accessibly (talk name + event).
- Do not import YouTube thumbnails into the media library unless rights are confirmed; embed or link is safer (same rule as media-appearances inventory).

## Stage photo inventory (owned library, verified HTTP 200 on 2026-07-26)

| Rank | Asset | URL | Suggested use | Alt (draft) |
|---|---|---|---|---|
| **P0 hero** | LaSalle stage wide | `https://i0.wp.com/kriskrug.co/wp-content/uploads/2026/05/kk-laSalle-both-hands-full-25-scaled.jpg` | Hero (eager) | Kris Krüg on stage delivering a Both Hands Full keynote at LaSalle College Vancouver |
| P0 strip | LaSalle stage mid | `https://i0.wp.com/kriskrug.co/wp-content/uploads/2026/05/kk-laSalle-both-hands-full-10-scaled.jpg` | On-stages strip / Responsible AI card | Kris Krüg presenting an AI keynote at LaSalle College Vancouver |
| P0 strip | Vancouver AI meetup (Michelle Diamond) | `https://i0.wp.com/kriskrug.co/wp-content/uploads/2024/09/AI_Meetup_August2024_MichelleDiamond-184-scaled.jpg` | On-stages strip | Kris Krüg speaking at a Vancouver AI community event |
| P1 strip | Vancouver AI hosting | `https://i0.wp.com/kriskrug.co/wp-content/uploads/2024/09/AI_Meetup_August2024_MichelleDiamond-195-scaled.jpg` | On-stages strip / hosting proof | Kris Krüg hosting a Vancouver AI Community Meetup |
| P2 art | CreativeMornings header | `https://i0.wp.com/kriskrug.co/wp-content/uploads/2026/05/kk-cmvan-keynote-header.png` | Topic card art only (not hero) | Punk Rock AI CreativeMornings Vancouver keynote artwork |

**Not recommended as hero:** OG image `5156893053_e4e246abb4_k.jpg` (current social share) and Both Hands Full / Punk Rock AI portal hotlinks.

### Photo gaps for KK

- Additional Bass Coast / ChannelNext / Futureproof stage stills may exist off-repo. Drop filenames or library IDs here before apply if they should replace Michelle Diamond frames.
- Prefer media-library attachment IDs at apply time so Jetpack/`i0.wp.com` crops stay consistent.

## Layout notes for above-fold (1440 / 390)

**1440:** Hero is a single composition: stage photo as dominant visual plane (full content width), overlay or adjacent column with H2 + one sentence + CTA. Formats do **not** enter the first viewport.

**390:** Stack photo on top (min-height ~42vh or aspect ~16/10), then claim + CTA. Watch embeds stack full-bleed under that. No autoplay.

Screenshot gate after apply: `docs/...` or PR attachments at **1440** and **390** confirming media + CTA without scroll.

## What stays from live copy

- H2 spine: `AI keynotes that make the room braver.` (unless KK picks a copy option that swaps it)
- Formats four-up meanings
- Signature topic destinations (Both Hands Full, Punk Rock AI, Developing an AI mindset, Responsible AI)
- End booking CTA pattern → `/contact/`
- Pack marker `<!-- content-architecture-2026:speaking -->`

## Coordination

| Issue | Relationship |
|---|---|
| #419 (this) | Speaking **page** multimedia rebuild (Track A) |
| #414 | Homepage Speaking **section** art direction (Track B / separate) |
| CTA decision issue | Final booking URL / label; draft uses `/contact/` + `Start a booking conversation` |

## KK curation checklist

- [ ] Approve P0 embed pair (or write replacements)
- [ ] Approve hero still (`…-25-scaled.jpg` or substitute)
- [ ] Approve on-stages strip (3 to 4 frames)
- [ ] Confirm booking CTA label + `/contact/` (or CTA-issue target)
- [ ] Sign copy option in `copy-options.md`
- [ ] Authorize live apply after authenticated snapshot
