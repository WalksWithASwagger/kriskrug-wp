# Links and media

All checked live 2026-09-07 on the published post. Every URL returned HTTP 200.

## Internal (kriskrug.co) — 17 article links on the page

| Anchor | URL |
|---|---|
| meetup | `/2026/06/30/zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey/` |
| both hands full | `/2026/01/24/both-hands-full/` |
| You Can't Drink Data | `/2026/05/23/you-cant-drink-data/` |
| Both Hands Full at the Data Center | `/2026/05/23/data-center-protest-signs/` |
| Both Hands on the Power Cord | `/2026/08/03/both-hands-on-the-power-cord/` |
| Canada Doesn't Need a Bigger AI Machine | `/2026/06/26/canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one/` |
| Sovereign AI for Whom? | `/2026/06/16/sovereign-ai-for-whom/` |
| Canada's AI for All Strategy | `/2026/06/04/canada-ai-for-all-strategy-skeptical-guide/` |
| Keep the Machine Strange | `/2026/08/10/keep-the-machine-strange/` |
| AI Lands Inside Every Profession | `/2026/07/31/ai-lands-inside-every-profession/` |
| publications page | `/publications/` |

## External — BC + AI (7 links)

The association site is **`bc-ai.ca`**. `bc-ai.net` 301s to a Notion ecosystem page and must never be used as the association link. That was a live bug in the first published version, fixed 2026-09-07.

| Anchor | URL |
|---|---|
| BC + AI Ecosystem Association | `https://bc-ai.ca/` |
| BC Public Compute Project | `https://bc-ai.ca/public-compute` |
| Both Hands on the Grid | `https://bc-ai.ca/news/both-hands-on-the-grid` |
| Rocks, Racks and Rights | `https://bc-ai.ca/news/rocks-racks-rights-canadas-blueprint-for-the-ai-energy-wars` |
| Building Sovereign AI Infrastructure in BC | `https://bc-ai.ca/news/building-sovereign-ai-infrastructure-for-what-comes-next` |
| What Kind of AI Province Should BC Build? | `https://bc-ai.ca/news/what-kind-of-ai-province-do-we-want-to-build` |
| BC's AI Crossroads | `https://bc-ai.ca/news/bcs-ai-crossroads` |

## Other external

| Anchor | URL | Note |
|---|---|---|
| edition 460 | `https://thebreaker.news/opinion/podcast-460/` | Used three times |
| Tyee party scorecard | `https://thetyee.ca/News/2026/08/11/Where-Vancouver-Parties-Stand-AI/` | Katie Hyslop |
| Tyee anti-AI movement | `https://thetyee.ca/News/2026/07/10/Vancouver-Growing-Anti-AI-Movement/` | Isaac Phan Nay, protest counts |
| Dave Olson | `https://daveostory.com/` | **Correct** Dave Olson. `daveolson.ca` is a theologian |
| 150 West Georgia | Daily Hive | Westbank site detail |
| H.R. MacMillan Space Centre | `https://www.spacecentre.ca/` | 403 to bare curl, 200 with a browser UA |
| bobmackin.substack.com | Substack episode post | Newsletter plug |

## Media on the post

| Slot | Media ID | Asset | Source |
|---|---|---|---|
| Featured | **12098** | Data centre protest crowd, KK in frame | KK's own, already published in the protest-signs post |
| Body 1 | **12748** | Dave Olson and KK laughing on the grass at Vanier Park | **Photo by Bob Mackin / theBreaker.news.** Their episode image, used editorially with a visible credit caption linking back to the episode |
| Body 2 | **12100** | "Software Engineers and SREs Against AI Data Centres" sign | KK's own |
| Body 3 | **12746** | Meetup #31 sumi-e poster | KK's own, from the kk-kb meetup archive |
| Body 4 | **12745** | theBreaker episode article clip | Screenshot of their article page, captioned |

## Embeds

**Audio.** `<!-- wp:audio -->` pointed at `https://thebreaker.news/podcast-player/15764/podcast-460.m4a`, theBreaker's own Seriously Simple Podcasting stream route and the exact URL their own page's player uses. Nothing is rehosted: the bytes come off their server and the play counts on their tracker. Verified live in the browser: `readyState` 4, `duration` 1395.52s, matching the published 23:16.

**Video.** `<!-- wp:embed -->` of `https://www.youtube.com/watch?v=fSbIJO0K-8o`, Mackin's 96 second preview of the election exchange. Resolves to the YouTube oEmbed iframe, so the view counts on their channel. The video download was 403 by design, so no frames were scraped; the embed serves their thumbnail natively.

## Open courtesy item

The Bob Mackin photo is theBreaker's asset, used with credit. It is a photo **of Kris**, taken at Kris's own event, by the outlet being written about, and it carries a visible byline plus a link back. That is ordinary editorial practice, but it was Claude's judgment call and not KK's. If Bob would rather it came down, it is one `--update` away.

## Public Compute hub link (handoff, 2026-09-07)

Added one in-body link to `https://bc-ai.ca/public-compute` in the council-calendar paragraph, immediately after the two sites are named:

> Both sites are tracked in the [BC Public Compute Project](https://bc-ai.ca/public-compute), an independent BC + AI registry that asks who owns them, what they consume, who pays for the load, and what stays in B.C.

One sentence, one link, no link block or buttons, per the handoff.

**Verified before publishing:**

- The hub returns 200 with `<meta name="robots" content="index, follow">` and a self-canonical, so it is cleared for public linking.
- `/public-compute/registry`, `/evidence` and `/status` all carry `noindex`, and `robots.txt` disallows `/public-compute/decision-toolkit`. None of them are linked. A `no_public_compute_subpages` check in the publish script enforces that.
- The claim "both sites are tracked" was checked against the registry itself: 150 West Georgia and Mount Pleasant are both present, alongside Kamloops (TELUS) and Cedar.
- The description matches the hub's own words: "an independent BC + AI public-interest framework and pilot registry." It is never called official, government, a regulator, a utility, or a decision authority.
- Reciprocals were already live on the BC + AI side: the hub links to this post, and `both-hands-on-the-grid` links to both this post and the hub. This closed the loop rather than opening it.

**On the `bc-ai.net` note in the handoff.** Correct, there is none on the live page. An earlier published revision of this post did link it, and it was repointed to `bc-ai.ca` before the handoff was written. The `no_bcai_net` check keeps it from coming back.

**Fixed in passing.** The voice checker caught `Kris Krug` without the umlaut in the body image alt text and in the SEO title. Both now read `Kris Krüg`, matching the site convention that `test_publications_editorial_payload.py` already asserts. Media 12748's library alt text was corrected too. Four non-umlaut instances remain on the rendered page and were deliberately left alone: the Person schema `alternateName` (a correct ASCII alternate), the YouTube oEmbed iframe title (theBreaker's own video title), the Aurora theme author bio, and media 12098's alt text. The last two are pre-existing and site-wide, and are filed as separate work.
