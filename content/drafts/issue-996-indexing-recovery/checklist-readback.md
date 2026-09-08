# #996 post-approval readback and measurement

Run only after KK approves a write and after Pagely purge. This file is a checklist, not permission to write.

## Per applied URL

- [ ] `curl -sSIL --max-time 30` on the pretty permalink: HTTP 200, no extra hop
- [ ] `?p={id}` still 301s to that permalink
- [ ] Plain and `?cb=<epoch>` HTML: one self-canonical, robots still `max-image-preview:large`, no `googlebot` noindex
- [ ] `<title>` and `<meta name="description">` match the approved strings (public HTML is authoritative)
- [ ] Each new href is present once; FIND leftovers are gone; 3820 and 3219 footers still point at 4539
- [ ] Slug, status, date, featured media, categories, tags unchanged
- [ ] URL still in `wp-sitemap-posts-post-1.xml`
- [ ] `make seo-publisher-smoke` still PASS

## Manual indexing (KK only)

- [ ] URL Inspection on `https://kriskrug.co/2024/01/31/exploring-the-intersection-of-photography-and-generative-ai/`
- [ ] Request indexing for 4539 only if Inspection still says crawled-not-indexed or discovered-not-indexed
- [ ] Ranks 2–5: same, and only if those URLs were confirmed in the current GSC example list
- [ ] Do not click Validate Fix from an agent session
- [ ] Do not submit or remove sitemaps from this pack (#274 owns sitemap follow-through)

## Measurement

Wait at least 14 full days after purge/recrawl, then pull Performance → Search results for each exact page over a 28-day window.

Record clicks, impressions, CTR, average position. Success is "we can see whether Google recrawled and whether the page entered the index," not a promised rank.

URL Inspection still missing from the 2026-09-08 prep session; fill those cells on apply day, do not backfill them into the triage report as if they were measured then.
