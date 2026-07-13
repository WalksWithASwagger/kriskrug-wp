# Issue #284: Topic Hub Link Review Handoff

**Track:** A - Content + SEO
**Status:** repo-only human-review packet; no live WordPress write
**Manifest:** `fixes/issue-284-topic-hub-links-handoff-2026-07-12.json`

## Decision

This packet prepares the remaining issue #281 candidates for issue #284. It
does not update WordPress, publish content, change Search Console, or claim a
ranking lift.

Read-only WordPress evidence changed the proposed batch:

- Six candidate rows already link to their target hub and are now no-ops.
- Five AI Ethics / AI Tools wrappers remain review-ready across four sources.
- Every Indigenous AI row remains visibly human-review-required.
- The Indigenous candidate that already links the hub remains a no-op unless a
  human explicitly requests a different in-body placement.

The merged issue #328 handoff files and tests remain unchanged.

## Evidence Boundary

Public checks ran on 2026-07-12 America/Vancouver, with the final evidence
capture at `2026-07-13T05:22:19Z`:

1. Look up every source post by exact slug through public WordPress REST.
2. Verify source ID, slug, `publish` status, modified values, and public URL.
3. Look up each target page by exact slug and verify the same identity fields.
4. Fetch every source and target URL and confirm HTTP 200.
5. Count normalized target hrefs in `content.rendered`, ignoring query strings
   and fragments.

This was public, read-only evidence. Authenticated `content.raw` is deliberately
left for a separately approved publisher session and must pass the stale guards
below before any write.

## Target Identity

| Target | ID | Slug | Status | Modified | Modified GMT | HTTP |
|---|---:|---|---|---|---|---:|
| [AI Ethics & Philosophy](https://kriskrug.co/ai-ethics/) | 12318 | `ai-ethics` | `publish` | `2026-07-01T12:27:51` | `2026-07-01T20:27:51` | 200 |
| [Generative AI Tools](https://kriskrug.co/ai-tools/) | 12321 | `ai-tools` | `publish` | `2026-07-01T12:27:55` | `2026-07-01T20:27:55` | 200 |
| [Indigenous & Reconciliation in Tech](https://kriskrug.co/indigenous-ai/) | 12322 | `indigenous-ai` | `publish` | `2026-07-01T12:28:09` | `2026-07-01T20:28:09` | 200 |

## Current Candidate State

The target count is the number of matching hub hrefs in the current public
WordPress body. Every source below is `publish` and returned HTTP 200.

| Map | Source ID | Slug | Modified | Target | Current count | Disposition |
|---:|---:|---|---|---|---:|---|
| 1 | 5723 | `unpacking-ai-ethics-at-american-marketing-associationvisionconf2024` | `2026-06-28T20:34:21` | AI Ethics | 3 | Existing link, no-op |
| 2 | 5489 | `cognitive-ai-creativity-and-ethics-w-professor-steve-dipaola` | `2026-06-28T20:34:50` | AI Ethics | 1 | Existing link, no-op |
| 3 | 4635 | `bridging-innovation-and-ethics-future-proof-creatives-and-the-path-forward-in-ai` | `2026-07-01T16:24:10` | AI Ethics | 2 | Existing link, no-op |
| 4 | 12030 | `canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one` | `2026-06-28T14:14:24` | AI Ethics | 0 | Review-ready, not approved |
| 5 | 12257 | `why-we-built-the-responsible-ai-professional-certification` | `2026-06-28T20:25:58` | AI Ethics | 0 | Review-ready, not approved |
| 6 | 4773 | `creative-toolbox` | `2026-06-14T20:08:44` | AI Tools | 1 | Existing link, no-op |
| 7 | 3275 | `how-ai-tools-like-midjourney-dall%c2%b7e-chatgpt-are-reshaping-the-creative-landscape` | `2026-06-14T20:34:30` | AI Tools | 1 | Existing link, no-op |
| 8 | 2781 | `audio-deep-fakes-ai-chatbots-and-new-web-development-tools` | `2026-06-28T20:39:27` | AI Tools | 0 | Review-ready, not approved |
| 9 | 12030 | `canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one` | `2026-06-28T14:14:24` | AI Tools | 0 | Review-ready, not approved |
| 10 | 12035 | `ai-wont-fix-your-broken-permit-process` | `2026-07-01T16:24:28` | AI Tools | 0 | Review-ready, not approved |
| 11 | 7450 | `indigenomics-now-2024-redefining-the-future-of-indigenous-economic-and-digital-sovereignty-through-ai` | `2026-06-28T20:31:08` | Indigenous AI | 1 | **HUMAN REVIEW REQUIRED**, existing link, no-op |
| 12 | 12030 | `canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one` | `2026-06-28T14:14:24` | Indigenous AI | 0 | **HUMAN REVIEW REQUIRED**, proposed only |
| 13 | 12035 | `ai-wont-fix-your-broken-permit-process` | `2026-07-01T16:24:28` | Indigenous AI | 0 | **HUMAN REVIEW REQUIRED**, proposed only |
| 14 | 12257 | `why-we-built-the-responsible-ai-professional-certification` | `2026-06-28T20:25:58` | Indigenous AI | 0 | **HUMAN REVIEW REQUIRED**, proposed only |
| 15 | 11905 | `sovereign-ai-for-whom` | `2026-07-01T16:24:30` | Indigenous AI | 0 | **HUMAN REVIEW REQUIRED**, proposed only |

The JSON manifest also records `modified_gmt`, internal-link counts, total
anchor counts, exact source URLs, and repo mirrors where they exist.

## Existing Links: No-Op

Do not add another target link to these source/target pairs:

| Source ID | Target | Current exact anchors |
|---:|---|---|
| 5723 | AI Ethics | `AI ethics`, `ethical AI`, `AI Ethics and Philosophy` |
| 5489 | AI Ethics | `AI Ethics and Philosophy` |
| 4635 | AI Ethics | `ethical AI`, `AI Ethics and Philosophy` |
| 4773 | AI Tools | `Generative AI Tools` |
| 3275 | AI Tools | `Generative AI Tools` |
| 7450 | Indigenous AI | `Indigenous and Reconciliation in Tech` in the collection footer |

## Review-Ready Patches

All five ordinary patches wrap current words only. They add no sentence, claim,
or keyword repetition. Priority reduces blast radius: a single exact semantic
wrapper first, then the broader wrapper, with the two-patch and longest source
last.

### Priority 1: Permit Process to AI Tools

- Source ID: `12035`
- Modified guard: `2026-07-01T16:24:28`
- Current target count: `0`
- Exact needle count: `1`, outside any existing anchor

Before:

```html
We train people in AI tools every day.
```

Proposed, not live:

```html
We train people in <a href="https://kriskrug.co/ai-tools/">AI tools</a> every day.
```

### Priority 2: Responsible AI Certification to AI Ethics

- Source ID: `12257`
- Modified guard: `2026-06-28T20:25:58`
- Current target count: `0`
- Exact needle count: `1`, outside any existing anchor

Before:

```html
That gap, between deployment speed and ethical practice, is why we built our new Responsible AI Professional Certification program.
```

Proposed, not live:

```html
That gap, between deployment speed and <a href="https://kriskrug.co/ai-ethics/">ethical practice</a>, is why we built our new Responsible AI Professional Certification program.
```

### Priority 3: Audio Deep Fakes to AI Tools

- Source ID: `2781`
- Modified guard: `2026-06-28T20:39:27`
- Current target count: `0`
- Exact needle count: `1`, outside any existing anchor

Before:

```html
the entire field of AI technology
```

Proposed, not live:

```html
<a href="https://kriskrug.co/ai-tools/">the entire field of AI technology</a>
```

### Priority 4: Better AI Machine to AI Ethics and AI Tools

- Source ID: `12030`
- Modified guard: `2026-06-28T14:14:24`
- Current target counts: AI Ethics `0`; AI Tools `0`
- Each exact needle occurs once and is outside an existing anchor
- Apply both approved wrappers in one body write, never as two sequential writes

AI Ethics before:

```html
AI ethics
```

AI Ethics proposed, not live:

```html
<a href="https://kriskrug.co/ai-ethics/">AI ethics</a>
```

AI Tools before:

```html
community-built tools
```

AI Tools proposed, not live:

```html
<a href="https://kriskrug.co/ai-tools/">community-built tools</a>
```

## Indigenous AI Review Queue

No item in this section is approved for a live write. Each item needs an
independent editorial decision, even if the ordinary patch on the same source
is approved.

### HUMAN REVIEW REQUIRED: Indigenomics Now, ID 7450

Current state: one existing collection-footer link:

```html
<a href="https://kriskrug.co/indigenous-ai/">Indigenous and Reconciliation in Tech</a>
```

Editorial context: this is a collection label, not a new in-body contextual
endorsement.

Decision: keep the footer link as-is, request a separately reviewed in-body
placement, revise the collection label, or remove it in a different approved
scope. This packet proposes no additional link.

### HUMAN REVIEW REQUIRED: Better AI Machine, ID 12030

Proposed, not live:

```html
<a href="https://kriskrug.co/indigenous-ai/">Indigenous data sovereignty and stewardship</a>
```

Editorial context: the phrase summarizes a BC AI JEDI Report claim. Kris's hub
may be useful supplemental context, but must not be presented as the authority
for that report or for Indigenous data governance.

Decision: approve this exact wrapper, choose a different authoritative
destination, revise the placement, or skip it.

### HUMAN REVIEW REQUIRED: Permit Process, ID 12035

Proposed, not live:

```html
<a href="https://kriskrug.co/indigenous-ai/">Indigenous leadership</a>
```

Editorial context: the sentence makes a strong first-person claim and sits
beside references to Coast Salish ceremony, UNDRIP, and a named board member.
Linking it to a general hub could read as self-validation or implied
endorsement.

Decision: confirm the claim, named-person context, and hub destination before
approving the exact wrapper; otherwise revise or skip.

### HUMAN REVIEW REQUIRED: Responsible AI Certification, ID 12257

Proposed, not live:

```html
<a href="https://kriskrug.co/indigenous-ai/">Indigenous ceremony</a>
```

Editorial context: the phrase is followed by a land and territory statement.
Turning ceremony into navigational anchor text may feel instrumental unless
the page owner and relevant community context support it.

Decision: approve only if linking ceremony to this hub is respectful and
contextually appropriate; otherwise revise or skip.

### HUMAN REVIEW REQUIRED: Sovereign AI for Whom, ID 11905

Proposed, not live:

```html
<a href="https://kriskrug.co/indigenous-ai/">host Nation governance</a>
```

Editorial context: the phrase appears in a policy argument about consent, fair
pay, and host Nation authority. Kris's hub must not substitute for Nation-led
sources or imply authority over host Nation governance.

Decision: approve the hub as supplemental context, choose a Nation-led source,
revise the anchor, or skip it.

## Before/After URL Manifest

"After" means projected review state only. No proposed after count has been
verified live.

| Map | Source URL | Target URL | Before | Proposed after | State |
|---:|---|---|---:|---:|---|
| 1 | https://kriskrug.co/2024/05/27/unpacking-ai-ethics-at-american-marketing-associationvisionconf2024/ | https://kriskrug.co/ai-ethics/ | 3 | 3 | No-op |
| 2 | https://kriskrug.co/2024/05/04/cognitive-ai-creativity-and-ethics-w-professor-steve-dipaola/ | https://kriskrug.co/ai-ethics/ | 1 | 1 | No-op |
| 3 | https://kriskrug.co/2024/02/13/bridging-innovation-and-ethics-future-proof-creatives-and-the-path-forward-in-ai/ | https://kriskrug.co/ai-ethics/ | 2 | 2 | No-op |
| 4 | https://kriskrug.co/2026/06/26/canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one/ | https://kriskrug.co/ai-ethics/ | 0 | 1 | Proposed, not live |
| 5 | https://kriskrug.co/2026/06/18/why-we-built-the-responsible-ai-professional-certification/ | https://kriskrug.co/ai-ethics/ | 0 | 1 | Proposed, not live |
| 6 | https://kriskrug.co/2024/03/01/creative-toolbox/ | https://kriskrug.co/ai-tools/ | 1 | 1 | No-op |
| 7 | https://kriskrug.co/2023/10/08/how-ai-tools-like-midjourney-dall%c2%b7e-chatgpt-are-reshaping-the-creative-landscape/ | https://kriskrug.co/ai-tools/ | 1 | 1 | No-op |
| 8 | https://kriskrug.co/2023/07/30/audio-deep-fakes-ai-chatbots-and-new-web-development-tools/ | https://kriskrug.co/ai-tools/ | 0 | 1 | Proposed, not live |
| 9 | https://kriskrug.co/2026/06/26/canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one/ | https://kriskrug.co/ai-tools/ | 0 | 1 | Proposed, not live |
| 10 | https://kriskrug.co/2026/06/24/ai-wont-fix-your-broken-permit-process/ | https://kriskrug.co/ai-tools/ | 0 | 1 | Proposed, not live |
| 11 | https://kriskrug.co/2024/11/14/indigenomics-now-2024-redefining-the-future-of-indigenous-economic-and-digital-sovereignty-through-ai/ | https://kriskrug.co/indigenous-ai/ | 1 | 1 | **HUMAN REVIEW REQUIRED**, no-op |
| 12 | https://kriskrug.co/2026/06/26/canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one/ | https://kriskrug.co/indigenous-ai/ | 0 | 1 | **HUMAN REVIEW REQUIRED**, proposed only |
| 13 | https://kriskrug.co/2026/06/24/ai-wont-fix-your-broken-permit-process/ | https://kriskrug.co/indigenous-ai/ | 0 | 1 | **HUMAN REVIEW REQUIRED**, proposed only |
| 14 | https://kriskrug.co/2026/06/18/why-we-built-the-responsible-ai-professional-certification/ | https://kriskrug.co/indigenous-ai/ | 0 | 1 | **HUMAN REVIEW REQUIRED**, proposed only |
| 15 | https://kriskrug.co/2026/06/16/sovereign-ai-for-whom/ | https://kriskrug.co/indigenous-ai/ | 0 | 1 | **HUMAN REVIEW REQUIRED**, proposed only |

## Separate Publisher Gate

This PR does not approve or execute these steps. In a future session with an
explicit live-write approval:

1. Process sources in deterministic order: `12035`, `12257`, `2781`, `12030`.
2. Before each source, fetch authenticated edit JSON and public HTML. Confirm
   the manifest ID, slug, `publish` status, modified guard, target identity,
   target HTTP 200, exact needle counts, and current href counts.
3. Snapshot each source separately under
   `backup/<UTC>-issue-284-topic-hub-links/source-<id>/`, including
   `before-edit.json`, `before-content.raw.html`, `before-public.html`, hashes,
   and a content-only rollback payload.
4. Stop and regenerate the packet if any identity, modified value, needle, or
   link-count guard is stale. Do not silently adapt the patch.
5. Review the full body diff. The only allowed top-level REST key is
   `content`; `title`, slug, status, dates, taxonomy, meta, excerpt, author,
   featured media, comments, template, format, sticky, and password fields are
   forbidden.
6. Write one source at a time. For source `12030`, include both approved
   ordinary wrappers in one content write.
7. Immediately read back authenticated raw content and cache-busted public
   HTML. Confirm unchanged identity and non-content fields, exact anchor counts,
   and HTTP 200 for source and targets before continuing.
8. If any readback fails, restore only the snapshotted `content.raw` to the same
   guarded source ID, verify the before counts, and stop the entire batch.
9. After the batch, smoke all edited sources, all three hubs, the homepage, and
   `/blog/`. Replace projected manifest values with observed values only after
   public verification.

The future REST body boundary is exactly:

```json
{
  "content": "<full reviewed and stale-guarded content.raw body>"
}
```

## Exact Human Decision

Before a publisher session, the human must provide two independent decisions:

1. Approve, revise, or reject the four ordered ordinary source writes that
   contain five copy-preserving AI Ethics and AI Tools wrappers.
2. For each of the five Indigenous AI rows, choose one: keep the existing link,
   approve the exact wrapper, choose a different destination or anchor, or
   skip.

Even after editorial approval, a fresh explicit go-ahead is required for the
live WordPress batch. This packet does not make the links live and does not
attribute any ranking movement to them.
