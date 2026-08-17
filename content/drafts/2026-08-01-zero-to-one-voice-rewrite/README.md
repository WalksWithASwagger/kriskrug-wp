# Zero to One first-person rewrite (issue #612, WP post 12034)

**Status: draft only. Nothing has been written to WordPress. Live apply is gated
on KK approval on #612, then the snapshot-first steps in `APPLY-RUNBOOK.md`.**

Live target: WP post **12034**,
https://kriskrug.co/2026/06/30/zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey/

Fetched 2026-08-16 (logged out, public REST): still third person, `modified`
2026-08-01T18:44:59. `content.raw` is not public; diagnosis used
`content.rendered` plus the 2026-08-01 authenticated raw snapshot already in
this directory.

## Membership ruling (one line)

KK, #615, 2026-08-01: publish **$340/year** and **300 members** as the current
figures. This payload recasts the leftover 130 / $240 lines so the post no
longer contradicts itself.

## Files in this directory

| File | What it is |
|---|---|
| `proposed-content-raw.html` | WordPress block markup. This is what would ship as `content.raw`. |
| `rewritten-body.md` | The same body in readable markdown. Kept in lockstep with the HTML. |
| `before-after.md` | Scannable live vs proposed for the opening, membership figures, and third-person "Kris" narration. |
| `APPLY-RUNBOOK.md` | Snapshot-first apply + rollback. Not executed. |
| `diff-notes.md` | First-pass paragraph map (2026-08-01). Historical relative to the figure recast. |
| `rewrite-notes.md` | First-pass section rationale. Historical relative to the figure recast. |
| `live-content-raw-2026-08-01.html` | Last authenticated `content.raw` snapshot in-repo. |
| `live-content-rendered-2026-08-16.html` | Public REST `content.rendered` from 2026-08-16. |
| `README.md` | This file. |

## What this round does

PR #667 already landed a first-person draft in this directory. Live never got
it. The 2026-08-15 readback (#734) still FAILed 12034 on mixed membership
figures. This round:

1. Keeps the first-person rewrite (frame, tense, dates, mechanical flags).
2. Reconciles membership copy to **$340/year** and **300 members**.
3. Adds a snapshot-first apply/rollback runbook.
4. Does not PATCH WordPress.

The May 24 package
(`content/drafts/2026-05-24-zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey/`)
is stale: third person, Individual $240/year, closer still 130. Live is already
a later rewrite of that source. This payload starts from live, not from May 24.

## Figure recast (this round)

KK instruction 3 on #615: prefer one clear current figure per page. Do not
claim 300 members arrived in 2.5 months (that would be a new falsehood). Recast:

| Live | This payload |
|---|---|
| 130 founding members (lede) | 300 members |
| enrolled 130 paid members in 2.5 months | 34 first-night signups kept; "Membership now sits at 300." |
| new membership cost just $240 annually | new membership cost $340/year |
| Reaching 130 paid members within 2.5 months | Reaching 300 paid members |
| Individual $340/year | unchanged (already correct) |
| closer 300 paid members | unchanged (already correct) |

`$200` stays as the one-time Core AI ticket-holder conversion offer, not the
list price.

## What was not touched

- Post title, slug, excerpt, featured image, categories, tags.
- Cert post **12257**.
- The live site. No REST writes from this lane.
- Theme.

## If KK approves

Follow `APPLY-RUNBOOK.md`. Identity check on ID 12034 + slug before any PATCH.
Snapshot `context=edit` to a dated `backup/` dir first. Dry-run the diff.
Content-only POST. Cache-bypass verify. Rollback is the snapshot `content.raw`.
