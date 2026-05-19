# Podcast EPK Refresh Package

Status: deployed on 2026-05-19 after KK's `proceed`, with Track A page snapshot and verification.

## Target Surface

Live target: `/podcast-guesting-page-epk/`

Reason: this is already the producer-facing URL linked from Speaking. Refreshing it is cleaner than creating a new top-level nav item.

## Proposed Page Title

`Podcast Guest, AI Commentator, And Event Host`

## Proposed SEO Fields

| Field | Recommendation |
| --- | --- |
| SEO title | `Podcast Guest, AI Commentator, Event Host | Kris Krug` |
| Meta description | `Book Kris Krug for podcasts, interviews, broadcasts, panels, hosting, and event emcee work on AI, creativity, community, media, ethics, and the future of work.` |
| Primary CTA | `/contact/` |
| Secondary CTA | `/speaking/` |

## Recommended Page Structure

1. **Hero** - one sentence positioning: AI speaker, podcast guest, broadcast commentator, host, moderator, and emcee.
2. **What Kris Brings** - practical AI fluency, creative technology, community stories, photography/media background, warmth, and useful tension.
3. **Best Topics** - AI for creatives, responsible AI, BC/Vancouver AI, human-centered tools, media futures, creator rights, community building, AI in daily life.
4. **Featured Appearances** - CBC AI Sandbox, Horizons, Human Biography, Rachel Thexton, E-ChannelNews, Kurty D, Teen2Life.
5. **Formats** - podcast guest, broadcast explainer, panelist, moderator, host/emcee, live interview, produced video series.
6. **Producer Notes** - bio, pronunciation, headshot/media asset needs, technical setup, availability, contact CTA.
7. **Internal Links** - Speaking, About, Work, BC + AI, Both Hands Full, Punk Rock AI, Horizons roundup.

## Source Links

- CBC AI Sandbox: `https://kriskrug.co/2024/07/03/new-segment-on-cbc-radio-early-edition-ai-sandbox-with-kris-krug/`
- IndigiGenius/CBC: `https://www.indigigenius.org/media-appearances/michaelandkrisinterview`
- Horizons: `https://horizons.compassdatacenters.com/series/exploring-ai-models-the-future-of-machine-learning/`
- Human Biography: `https://www.iheart.com/podcast/338-the-human-biography-podcas-108140410/episode/kris-krug-live-with-curiosity-256487014/`
- Rachel Thexton: `https://music.amazon.com/es-ar/podcasts/efb24614-5724-4412-a377-755e3b3ebdd4/episodes/cd1d024c-e3d4-496f-ace3-2901c89c3882/rachel-thexton-connects-03x08-kris-kr%C3%BCg-one-of-canada%27s-leading-ai-voices-talks-tech-and-tells-his-story`
- E-ChannelNews: `https://www.e-channelnews.com/interview-with-kris-krug-at-channelnext-central-2025/`
- Kurty D: `https://podcasts.apple.com/us/podcast/053-widen-the-lens-with-kris-krug/id1575595225?i=1000634160006`
- Teen2Life: `https://music.amazon.com/es-us/podcasts/ba75295d-60de-4701-8eb6-12e17e49838a/teen2life-experience`

## Publish Gate

- [x] Snapshot existing page ID for `/podcast-guesting-page-epk/`.
- [x] Confirm page ID and slug before any REST write.
- [x] Remove or replace outdated direct contact details from body content.
- [x] Choose WP-hosted headshot and stable owned-site images.
- [x] Confirm final list from public-source inventory and KK-provided Horizons link.
- [x] Curl-check all source links in the live payload.
- [x] After publish, verify `/speaking/` still returns `200`.

Deploy verification: `../verification/PODCAST-EPK-DEPLOY-VERIFICATION-2026-05-19.md`.
