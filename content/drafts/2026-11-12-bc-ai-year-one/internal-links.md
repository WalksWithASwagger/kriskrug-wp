# Internal and network links

Every URL in `post.html` (17 unique, 21 links in all), plus the embedded video, with its logged-out status on 2026-11-13 at 03:13 UTC. Every one returned 200 on the first request, with no redirect. External links carry `target="_blank" rel="noopener noreferrer"` from the shared `wp_blocks.inline()` helper. kriskrug.co links stay plain.

## kriskrug.co (internal)

- https://kriskrug.co/2026/06/30/zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey/ (200): the origin story, the founding tiers and the Core AI switch. Linked twice: "Zero to One" in the lesson section and "Read how it started" at the end
- https://kriskrug.co/2026/07/31/ai-lands-inside-every-profession/ (200): the 300-as-capability argument, linked as "wrote that in July"
- https://kriskrug.co/2026/11/01/futureproof-2026-year-one/ (200): the festival's first year, linked from the video caption

## bc-ai.ca (the receipts)

- https://bc-ai.ca/about (200): members, attendance, events, regions, programs, incorporation date, board and room leads. Linked twice: "bc-ai.ca" in the receipts section and "Check the receipts" at the end
- https://bc-ai.ca/membership (200): $340 individual rate, 25% event discount, "a voice in the association". Linked three times: "membership", "a voice in the association" and "Become a member"
- https://bc-ai.ca/certification (200): the four public programs
- https://bc-ai.ca/faq (200): self-serve cancellation, "No retention scripts", the sliding-scale answer
- https://bc-ai.ca/youth-access-fund (200): scholarships
- https://bc-ai.ca/events/vancouver-ai-meetup-2025-08 (200): Meetup #20, August 27, 2025, the launch night record
- https://bc-ai.ca/news/vancouver-ai-meetup-32-data-for-good-taleeb-noormohamed-recap (200): Kris's recap of the anniversary night, linked on Taleeb Noormohamed's name
- https://bc-ai.ca/news/the-room-that-wrote-to-ottawa (200): the AI Ethical Futures Lab story
- https://bc-ai.ca/communities/film-club (200)
- https://bc-ai.ca/communities/futures-lab (200)
- https://bc-ai.ca/communities/fraser-valley-ai (200)
- https://bc-ai.ca/communities/ai-education (200)
- https://bc-ai.ca/communities/comox-valley (200)
- https://bc-ai.ca/events/2026-12-16-vancouver-ai-community-meetup (200): the December 16 meetup at the Space Centre

## The video

- https://www.youtube.com/watch?v=fPP3-rHzE8o (200): "Don't Abdicate Your Seat: Inside Future Proof Festival | Vancouver AI August 2026" on the Vancouver AI channel, per public oEmbed. Embedded under the opening. bc-ai.ca's clip notes give it as 5:15, recorded at Meetup #32.

## Intended canonical

Open until Kris rules on date and slug (open-facts question 6). With the recommended answers it is `https://kriskrug.co/<publish yyyy>/<mm>/<dd>/bc-ai-year-one/`. `https://kriskrug.co/bc-ai-year-one/` returned 404 on 2026-11-13 03:13 UTC.

## Inbound links to add after publish (separate, approved edits)

Not part of this package and not to be done without Kris's approval for each page:

- Zero to One could add a one-line pointer to this post at the end.
- AI Lands Inside Every Profession could link this post where it says "I wrote the origin arc separately."

## Not linked, on purpose

- The public member directory on bc-ai.ca. Nobody from it is named.
- Individual people's profile pages. The room leads are named with their rooms, which is how bc-ai.ca/about presents them.
- The lab that hosts Ed + AI. Its name carries a combining diacritic outside cp1252, so it stays out of the copy.
- The Luma listing for December 16. The bc-ai.ca event page links to it.
