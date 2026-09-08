# SEO metadata

**Post title:** AI Is Already a Campaign Issue in Vancouver

**Slug:** `ai-already-campaign-issue-vancouver`

**SEO title (60 char target):** AI Is Already a Campaign Issue in Vancouver | Kris Krüg
**Length:** 55 characters.

**Meta description (155 char target):**
Bob Mackin asked if AI would sway B.C.'s civic elections. Council had already answered by sending the Telus and Westbank data centre back to city planners.
**Length:** 153 characters.

**Excerpt:**
Bob Mackin asked whether AI would sway B.C.'s local elections. Council had already answered the question by sending the data centre back to city planners.

**Primary keyword:** AI Vancouver civic election
**Secondary:** Vancouver data centre, Westbank Telus data centre, BC + AI Ecosystem Association, theBreaker.news podcast, Dave Olson

**Schema recommendation:** `Article` with `about` referencing the podcast episode, plus a `citation` to `https://thebreaker.news/opinion/podcast-460/`. Do not mark this up as `PodcastEpisode`. Kris is a guest, not the publisher, and the episode is theBreaker's asset.

## Shipped

REST-set and verified live 2026-09-07 on post **12747**. The earlier concern that Jetpack was deactivated and REST writes would no-op **did not hold**:

- Authenticated `context=edit` readback matched both fields exactly.
- Logged-out render returned `<title>AI Is Already a Campaign Issue in Vancouver | Kris Krug</title>` and the matching `<meta name="description">`.

No manual editor step was needed. Keep verifying the public render rather than trusting the REST 200.
