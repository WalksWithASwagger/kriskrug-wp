# #402: consolidate the existing ALL IN series path

**Repository closeout approved October 25. The article changes remain an
unpublished editorial proposal; this package records no WordPress apply.**

Fresh authenticated and public inspection on October 25 found that #1030's
series blocks already exist on all three posts. All three also link separately
to the September 18 final dispatch. Post 12800 retains an additional older
“Continue the series” block. Adding the September paste package again would
duplicate navigation. This packet supersedes only its three ALL IN navigation
instructions for a future review; it does not redeploy its wider cross-site matrix.

| Target | Current state | Draft delta |
|---|---|---|
| 12783, `headed-east-for-all-in-montreal` | Two-link series list, west-coast sources, separate final-dispatch link | Put the final dispatch in the existing list; add a relevant Speaking next step |
| 12788, `all-in-montreal-robot-mirror` | Two-link list, regional sources, separate final-dispatch link | Put the final dispatch in the existing list; add a workshop next step |
| 12800, `all-in-montreal-day-two-uncle-evan-and-the-extremely-suspicious-backpack` | Two duplicate series blocks, policy sources, festival promo, separate final-dispatch link | Retain one list with the final dispatch; replace the appended festival promo with a project-enquiry next step |

Each is a published WordPress post whose article source is `content.raw`.
Full canonical URLs, IDs, slugs, modification timestamps, source/candidate hashes
and exact single-match replacements are in `patches.json`. No theme ownership
or template modification is needed. The September 18 article is a verified
destination only; this packet does not edit it.

## Review

Read `copy.md`, the three `*-section.html` previews and the three unified diffs.
The essays' reported scenes, quotations, existing contextual links, photographs,
captions and credits are preserved. The removed festival link is the appended
“Next room” promotion on post 12800, not its reported invitation in the essay.
The retained west-coast and policy source paragraphs remain byte-for-byte intact.

The new next steps are evergreen and describe the existing Speaking, Services
and Contact destinations. They make no claim about availability, ticket stock,
bookings or a closed call for talks. Source reading included the current posts,
the existing #1030 packet and Kris's local Voice Patterns & Style Guide.

## Verification completed

- Read-only authenticated ID/slug/status checks and public canonical readback.
- All seven article/next-step destinations return direct 200 with exact
  self-canonicals; results in `verification.json`.
- Every old fragment matches exactly once against its captured raw source.
- Draft candidates retain all figures, images, video/audio/iframe elements,
  captions and blockquotes. One three-item series list remains in each targeted
  section, and the final dispatch appears once in each post's content.
- Repository voice hard-rule scan: zero violations, no waivers. Manual review
  kept the new language short, specific and conversational. The canonical local
  voice checker was found under `kk-kb/content/reference/kk-voice/`; its soft
  “team” finding was resolved to “crew” in the new workshop invitation.
- No production form submissions, analytics events, schema changes or live writes.

## Future apply and rollback

1. Obtain approval of this exact copy and the three live post targets. Shipping
   this repository package preserves the proposal; it does not publish it.
2. Re-read each post by ID and verify its slug, type, status and full raw-content
   hash. If the source changed, re-cut and review its diff rather than forcing
   the old patch. Snapshot the full current object privately before any write.
3. Run a content-only dry-run for one post. Apply each listed `before` fragment
   exactly once to produce the candidate hash. Never render the whole article
   through an HTML serializer or send title/date/taxonomy/status fields.
4. Apply one object at a time. Verify stored content, bare and uncached public
   output, media/captions and the intended links before proceeding.
5. Roll back by restoring the full exact private `content.raw` snapshot after
   confirming current content equals the applied candidate. A third hash means
   another edit and requires reconciliation. Read back after restoration.

Private October 25 source snapshots and full candidates remain in the local
operator packet under `.generated/current-state/sunday-2026-10-25/all-in/`.
They are not committed. No auto-closing keyword is used for parent #402.

## Measurement proposal

Use only `kriskrug.co` traffic and these exact paths. The issue's September 9–
October 6 page-view counts (222 / 206 / 201) are historical prioritization
evidence, not this change's baseline. Current analytics were not retrieved.

Before publication, capture the four complete Monday–Sunday weeks ending before
the publication date. Compare against four complete Monday–Sunday weeks starting
on the first Monday after publication, excluding the partial launch week.
For an October 26 publication, that means baseline September 28–October 25 and
follow-up November 2–29. Record publication time and any overlapping campaign.

Report article views and engaged sessions, then within-series navigation and
destination visits where existing measurement supports them. Internal link
clicks are not assumed to be automatically tracked. If the required sequence or
click measurement is unavailable, mark it unavailable; implementation belongs
to #1090 and must not be invented in this draft.

Proposed downstream outcome: attributable qualified talk/workshop/project
enquiries. This is a review proposal, not a change to the site's conversion
definition. Link clicks and destination visits are separate from an enquiry,
newsletter signup, booking or sale. Use aggregate counts only; no visitor or
enquirer identifiers belong in this packet. Small samples and festival-week
traffic make causal attribution weak; do not promise uplift.
