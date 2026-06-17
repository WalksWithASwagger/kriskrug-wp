# Content Syndication Strategy v1 - 2026-06-17

**Lane:** Track A marketing/content strategy
**Scope:** docs-only v1 for GitHub issue #52. No public posting, account setup, API configuration, outbound messages, private data handling, or production deploy.
**Issue:** [#52 - [MARKETING] Create Content Syndication Strategy](https://github.com/WalksWithASwagger/kriskrug-wp/issues/52)

## Assumptions and Success Criteria

- `kriskrug.co` remains the canonical home for original long-form posts.
- Syndication expands reach only after a post is already published, QA'd, and intentionally selected for reuse.
- This v1 defines the operating system; it does not claim that Medium, LinkedIn, Dev.to, or Substack accounts are configured.
- Success for issue #52 means future publishers have channel rules, SEO safeguards, a packaging workflow, measurement, and stop conditions before any public reposting begins.

## Channels and Surfaces

| Surface | Best fit | Default format | Publish timing | Required safeguards |
|---|---|---|---|---|
| Medium | Narrative essays, culture/AI field notes, travel/photo essays with broad audience appeal | Full or lightly edited republication | 7-14 days after canonical post | Canonical link back to `kriskrug.co`, original-post note, no unverified claims added |
| LinkedIn Articles | Professional AI strategy, facilitation, speaking, community leadership, case-study posts | Edited article or excerpt with CTA to original | 3-10 days after canonical post | Link to canonical original, remove private/client-sensitive details, factual proofread |
| Dev.to | Practical AI workflow, tooling, web, automation, and maker notes | Technical adaptation with code/process focus | 7-21 days after canonical post | Canonical URL if supported, developer-first headline, no duplicate low-fit essays |
| Substack | Newsletter-style dispatches, curated reflections, subscriber updates | Excerpt plus commentary or newsletter edition | Weekly or biweekly batch | Link to canonical post, avoid paywalling the canonical article, preserve consent on media |
| Internal cross-link surfaces | Related `kriskrug.co` posts, Work/Speaking/About references | Contextual internal links | Same day as canonical publish or during content QA | Slug/ID verification before any WordPress edit |

## Republishing Rules

1. Publish on `kriskrug.co` first.
2. Wait at least 72 hours before any duplicate full-text republication unless there is a campaign-specific reason.
3. Prefer excerpts or adapted versions when the target platform has a different reader intent.
4. Keep the canonical URL visible near the top or bottom of every syndicated copy.
5. Do not syndicate posts with unresolved editorial review, draft claims, private event context, unapproved sponsor/client references, or media-rights uncertainty.
6. Do not rewrite the factual substance for a platform unless the edited version gets its own approval pass.
7. Do not use automation to post publicly until account ownership, preview rendering, and rollback/delete access are confirmed.

## Canonical-Link and SEO Safeguards

- Canonical source: the final public `kriskrug.co` post URL.
- Required note for full republication:

```text
Originally published at kriskrug.co: [canonical URL]
```

- Use a platform canonical URL field when available. If a platform does not support canonical metadata, use the visible original-publication note.
- Do not change the WordPress slug, title, excerpt, or metadata as part of syndication packaging.
- Do not publish the same full article to all platforms on the same day. Staggering supports measurement and reduces duplicate-content confusion.
- Use UTM-tagged links only for outbound links from syndicated copies back to `kriskrug.co`; never replace the canonical URL itself with a tracking redirect.
- Suggested UTM pattern:

```text
?utm_source=<platform>&utm_medium=syndication&utm_campaign=<post-slug>
```

## Packaging Workflow

### 1. Select

- Confirm the canonical post is public and stable.
- Confirm the post fits at least one syndication surface.
- Capture the canonical URL, title, excerpt, publish date, primary image, and owner-approved CTA.

### 2. Screen

- Check for private names, emails, event attendee details, unpublished client details, sponsor claims, or media where publicity rights are unclear.
- Check for claims that need current numbers or external proof.
- Confirm the post does not rely on site-specific embeds that will break on another platform.

### 3. Adapt

- Create one platform package at a time.
- Adjust headline, deck, intro, CTA, and tags for the platform.
- Keep the core argument intact.
- Preserve image alt text where the platform supports it.

### 4. Approve

- Reviewer verifies: canonical link, original-publication note, privacy screen, factual claims, media rights, CTA, and platform fit.
- KK or delegated publisher gives explicit go/no-go before any public posting.

### 5. Publish and Log

- Publish manually for v1.
- Record platform URL, date, canonical URL, UTM campaign, post owner, and any edits made from the canonical version.
- Add performance metrics after 7, 30, and 90 days.

## Measurement Plan

| Metric | Source | Cadence | Notes |
|---|---|---|---|
| Syndicated posts shipped | Manual log | Monthly | Target from issue #52: 2-3 reposts/month after pilot approval |
| Referral sessions to `kriskrug.co` | Analytics/UTM reports | 7, 30, 90 days | Track per platform and per post |
| Leads or inquiries | Contact/source notes | Monthly | Attribute only when source is clear |
| Backlinks | SEO/backlink tool or manual search | Monthly | Count live links back to canonical source |
| Platform reach | Native platform analytics | 7 and 30 days | Treat issue #52's 100K+ reach as an aspirational benchmark, not a v1 proof claim |
| Subscriber/follower growth | Native platform analytics | Monthly | Keep Substack growth separate from social reach |

## Pilot Plan

Start with four already-public, low-risk posts:

1. One AI/community strategy post for LinkedIn Articles.
2. One practical AI/tooling post for Dev.to if it has genuine technical substance.
3. One broad narrative essay for Medium.
4. One newsletter-friendly dispatch for Substack.

The pilot is complete when each platform has one approved package, one manual publish decision, and one 30-day metric readback.

## Stop Conditions

Pause syndication if any of these occur:

- Canonical link cannot be represented clearly on the target platform.
- A platform package includes private, client, sponsor, attendee, or media-rights-sensitive material without explicit approval.
- The adapted version introduces unverified claims or stale numbers.
- Referral traffic is low and bounce/engagement quality is poor for two consecutive monthly cycles.
- A platform account, permissions model, or deletion/rollback path is unclear.
- Duplicate-content or indexing issues appear for canonical posts.
- The workflow starts cannibalizing editorial quality on `kriskrug.co`.

## Launch Gate Checklist

- [ ] Canonical `kriskrug.co` post URL verified.
- [ ] Platform selected and rationale noted.
- [ ] Privacy/publicity screen passed.
- [ ] Canonical/original-publication link included.
- [ ] CTA and UTM links reviewed.
- [ ] Media rights and alt text reviewed.
- [ ] Platform preview checked.
- [ ] Publisher approval captured.
- [ ] Public URL and metric dates logged after posting.

## Closeout Criteria for #52

Issue #52 can be treated as strategy-complete when this doc is accepted as the v1 playbook and a future execution issue or checklist owns account setup, first-package approval, and pilot measurement.
