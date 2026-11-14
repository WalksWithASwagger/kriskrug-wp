# Current State Snapshot - 2026-11-13

**Snapshot:** Friday, November 13, 2026, 17:20 America/Vancouver
(2026-11-14 00:20 UTC), from `make varlock-run CMD='make status-readonly'`
after the November 12 and 13 pass had finished. This is the declared drift
baseline, not a promise that counters stay unchanged. Run
`make status-readonly` for current observations. Supersedes
[October 25](CURRENT-STATE-2026-10-25.md). Kris waived the November 18 date
gate in #1214. The zero-open-PR gate held at the readback.

## Verified state

- Open PRs: `0` at the readback, before this snapshot PR opened.
- Open issues: `0` once #1214 closes with this PR. The readback counted 1 open, #1214 itself.
- Production still publicly reports WordPress `7.0.8`. Public smoke: 0 failures, 0 warnings.
- WordPress draft queue: `2` scheduled posts, `69` draft posts, `4` draft pages.
  The scheduled posts are Gorgeous Ghost (13003, November 19) and Both Things
  Are True (13004, November 24).
- Public Aurora `style.css`: `1.7.3`. Fetched `origin/main`: `1.7.3`.
  `make status-readonly` reports live and `origin/main` in sync.
- Canonical main at the readback: `07cfeee69a98566649d5a3de7b0c23ecc31bd618`.
  Use this PR and a fresh GitHub readback for its merge SHA.
- `/projects/` redirects to `/work/`.

## Completed and remaining work

The [November 12 roadmap](ROADMAP-2026-11-12.md) holds Kris's direction for the
quarter, what was delivered on November 12 and 13, the agent lane, the dated
checklist and the decisions still waiting on him. This snapshot does not
restate it.

Live changes finished before this readback, each with its own receipt:

- Aurora 1.7.2, deployed November 12 at 17:52 America/Vancouver
  ([receipt](reports/aurora-172-deploy-2026-11-12.md)).
- Aurora 1.7.3, the homepage database template and Contact now promise a
  monthly KRÜG letter; 1.7.3 deployed November 12 at 18:29 America/Vancouver
  ([receipt](reports/aurora-173-monthly-letter-release-2026-11-12.md)).
- The December 16 Vancouver AI meetup on `/events/`, page 2250
  ([receipt](reports/events-dec16-release-2026-11-12.md)).
- The TIDEPOOL.ING and Little Supercluster entries on Work, page 2672 (#1298).
- Code Snippet 5 with `JSON_HEX_TAG` and `JSON_HEX_AMP`
  ([receipt](reports/snippet-5-hextag-release-2026-11-12.md)).
- The #339 publisher updates on page 1208 and eight posts
  ([receipt](reports/issue-339-applied-2026-11-12.md)).
- The #828 negotiation checklist on post 1210
  ([receipt](reports/issue-828-applied-2026-11-12.md)).
- Two scheduled posts with their featured images
  ([receipt](reports/scheduled-posts-2026-11-19-24.md)).
- `/ai-policy/`, page 13005, published November 13
  ([receipt](reports/ai-policy-publish-2026-11-13.md)).

## Operating references

- [September 9 live-lane procedures](WORK-PLAN-2026-09-09.md), retained for their
  identity, snapshot and approval requirements, not as today's issue queue.
- [Two-track model](TWO-TRACK-MODEL.md): separate content, theme and ops changes.
- [Runtime reference](AGENT-RUNTIME-REFERENCE.md) and `.env.schema`: Varlock and
  existing trusted access; no plaintext secret reads.
- The dated checklist in the roadmap replaces the weekly tracker issues. Six
  one-time, read-only checks are scheduled in the Claude app for November 16,
  19, 24 and 27 and December 1 and 18.

This snapshot authorizes no live write, deploy, cache purge or workflow change.
Auto-Triage Issues and Marquee Weekly Scan were deleted on 2026-11-12 (#1220).
