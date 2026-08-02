# Image alt text

Source of truth for roles and source URLs: `asset-manifest.md` (#644 update). Alts below match frontmatter + in-body placement in `post.md` / `post.html`, rewritten 2026-08-02 for #645.

- **vanai-meetup31-stage-kris-futureproof-slide.webp** (lead / hero) — alt: "Kris Krüg speaks on stage at Vancouver AI Meetup #31, in front of a Futureproof slide reading Vancouver, we need to talk about AI, with salmon and skyline artwork behind him." Credit: Photo: Michael Caswell. Edited: Kris Krüg.
- **vanai-meetup31-audience-wide-shot.webp** (community-room) — alt: "A wide shot from the back of the room, a full silhouetted audience facing the lit Futureproof stage and screen during Vancouver AI Meetup #31." Credit: Photo: Michael Caswell.
- **futureproof-honest-conversation-poster.png** (official-graphic, was hero) — alt: "Futureproof Festival poster with silhouetted figures walking toward a golden-lit portal under ornate arches. White type reads The most honest AI conversation happening anywhere this year. Dates Vancouver Oct 28-30, 2026."
- **manifesto-01-future-cultural-question.webp** (gallery) — alt: "Hand-painted Futureproof poster reading The Future Is a Cultural Question over an aurora above a forested shoreline with salmon and painted eyes."
- **manifesto-06-who-shapes-us.webp** (gallery) — alt: "Hand-painted Futureproof poster reading Who Gets to Shape What Shapes Us over rivers running through open hands."
- **manifesto-14-places-to-think.webp** (gallery) — alt: "Hand-painted Futureproof poster reading The Future Needs Places to Think over a quiet tidepool reflecting stars."
- **futureproof-salmon-starfield-share-20260527.jpg** (gallery + optional OG landscape) — alt: "Futureproof launch key art with coral salmon swimming toward a bright portal under aurora and stars. Title type FUTUREPROOF FESTIVAL, October 28-30, 2026, presented by BC+AI."

## Dropped from this rewrite

- **futureproof-wordmark-white-transparent.png** — was inline after the FATALE/dream beat in the July 26 draft. That beat (the FATALE renaming saga) isn't in the #645 rewrite, since it's already told in full in *The Long Road to Futureproof* and repeating it would duplicate that post's section-level argument. The wordmark file is still staged in `images/` and listed in `asset-manifest.md`'s July 26 set if a later draft wants it back.

## Placement (current, #645)

1. Meetup #31 stage photo immediately after the opening two paragraphs (the "last month I stood on a stage" scene).
2. Meetup #31 audience photo after "What twenty years behind the lens actually teaches you," closing that section before the "why Futureproof" heading.
3. Official-graphic poster after "The H.R. MacMillan Space Centre... is home," closing the "why Futureproof, why now, why Vancouver" section.
4. Four-image manifesto gallery after "I'm asking you to help hold a room that can stay honest," inside "The bat signal" section (`[[GALLERY-MANIFESTO]]` marker in `post.md`).

Binaries for the two new meetup photos are staged locally under `images/` (see `asset-manifest.md`), matching the July 26 set's staging pattern. `post.html` still hotlinks the public R2 and futureproof.website URLs directly, same convention as the original package, so #500 can swap to uploaded media IDs without rewriting alts.
