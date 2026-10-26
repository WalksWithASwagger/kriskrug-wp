# Prompt Victoria Events closeout — October 25, 2026

#1018's requested card is already live on page 2250. A fresh read of
`https://kriskrug.co/events/` confirms its title, November 5 date, 11:15 a.m.
start, Main Theatre / Victoria Conference Centre venue, Speaker role, portrait
and working speaker-page destination. Catalog preparation landed in #1108;
the current page was preserved in the approved #1134 release.

The [official speaker page](https://promptvictoria.ca/speaker/kris-krug/), read
October 25, lists **11:15 a.m.–noon**, and links to
[conference registration](https://members.viatec.ca/event-calendar/Details/2026-prompt-victoria-ai-conference-1845004).
The existing Speaker page CTA remains appropriate. Its destination was fetched
successfully; no registration was submitted.

One catalog-only correction replaces the stale 12:15 p.m. end with noon,
using the runtime's `America/Vancouver` offset for November 5. The renderer
keeps cards until the following local midnight; it does not roll them off at
the session's end time. Rendering before and after this correction with the
same fixed clock produces identical HTML, so no WordPress write is needed.

The existing Events contract and catalog suites pass. Private public-page,
official-source and identical-render receipts are retained under
`.generated/current-state/kriskrug-closeout-2026-10-25/` in the original checkout.
This closes the already-delivered card request without changing the wider
Events catalog, maintenance policy or backfill scope.
