# Live vs v2 payload — page 2409 /testimonials/ (2026-08-16)

Read-only diagnosis for [#602](https://github.com/WalksWithASwagger/kriskrug-wp/issues/602).
No live write. Do not close #602: live still has the v1 body.

Fetched:

- `GET https://kriskrug.co/wp-json/wp/v2/pages/2409` → id 2409, slug `testimonials`, status `publish`, `modified` `2026-08-01T19:09:19`
- Cache-bypass HTML `https://kriskrug.co/testimonials/?cb=…` HTTP 200
- Live theme `style.css` Version **1.6.5** with `aurora-tstm` rules present
- Payload `content/source-packs/content-architecture-2026/wp-payloads/testimonials.html` (PR #630)

Public REST does not return `content.raw`. Rendered body saved as
[`live-content-rendered-2026-08-16.html`](./live-content-rendered-2026-08-16.html).

## Already shipped

| Surface | Evidence |
|---|---|
| v1 page body (19 cards) | Live REST `modified` 2026-08-01; marker `content-architecture-2026:testimonials`; headline *Proof from the rooms, stages, and cohorts.* |
| Legacy `user-infos` stack removed | 0 hits on live HTML and payload |
| Hard blocks off-page | `William Jordan` and `Stephanie McKay` absent live and in payload |
| Overlapping names still live | Kerris, Landon, Carly, Jai Djwa, Ed Kennedy, David Gloyn-Cox, Fiann, Tavis, Steve Jones, Simon Haworth, Suzy Easton, Rob Cottingham (once), Joshua Dunford, Benjamin Random, Corey Dennis, Claudine Co, Stephanie Vacher, Danie Peace |
| Theme half (#601) | Issue closed 2026-08-10. Live CSS is 1.6.5 and contains `aurora-tstm` (40 hits). Body classes are not using them yet. |
| Curated 40-card payload + page-map markers | On `main` via PR #630 / #599. File exists; not applied. |

## Still waiting (this issue)

| Surface | Live | Payload |
|---|---|---|
| Card count | 19 | 40 |
| Body namespace | `aurora-testimonials-page` only | `aurora-testimonials-page aurora-tstm` plus `aurora-tstm-*` |
| Hero | Proof from the rooms, stages, and cohorts. | Proof with names attached. + six stat chips |
| Press band | absent | Power 50 / CreativeMornings / BC Studies |
| Featured three | Kerris, Landon, Carly | Kerris, Simon (Meetup **#10**), Arno Apeldoorn |
| Simon placement | Meetup **#30** card in rooms-era stack | Featured, Meetup #10; #30 quote benched |
| New sections | none | Rooms (7), extra RAP, Talks extras, Training, Threads, Film extras, Archive Butterfield |
| Threads / WA-10 | absent | Darren Nicholls, Sev Geraskin, Peter Bowles (“Don't fucking stop…”) |
| Stewart Butterfield 2006 rec | absent | Archive only |
| Second Cottingham card (2009 talks rec) | absent | Talks + Archive (two different quotes) |
| Live-only card dropped in v2 | “Audience feedback” | benched (KB-AUD1/AUD2) |

### Section H2s

Live: Proof from the rooms, stages, and cohorts. → The lines that carry the current era. → Stages, classrooms, and design rooms. → Responsible AI Professional — Cohort 1. → Meetups, film club, and the people who show up. → Photography and connector years. → Want a room like these?

Payload: Proof with names attached. → Start with three. → The monthly rooms. → Responsible AI Professional, Cohort 1. → Keynotes and guest sessions. → Workshops that use your real work. → Said in the group chat. → Film Club nights. → The photography and connector years. → Want a room like these?

### Names only in the v2 payload (not on live)

Alex Samur, Arno Apeldoorn, Becky Pallack, Brittney Ashley, Daniel Bashaw, Darren Nicholls, Gus Santos, Harrison Reed, Jesse Benson, Jill Manuel, Joel Solomon, Kaoru Yoshihira, Kristen Hughes, Marty Avery, Pete Young, Peter Bowles, Rachel Krayenhoff, Sev Geraskin, Stewart Butterfield, Tanya Slingsby, Yin Lau.

(Fiann is on both; live cite uses a curly apostrophe in O’Hagan, payload uses ASCII.)

## Recommendation

Keep #602 open. Run [`APPLY-RUNBOOK.md`](./APPLY-RUNBOOK.md) after KK comments the editorial rulings and the exact payload. Closing would strand the 40-card body in the repo.
