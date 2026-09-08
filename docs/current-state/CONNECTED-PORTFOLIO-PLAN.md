# Connected portfolio of practice

**Decision:** KK approved this direction and its first proof slice on 2026-09-05.
Implementation is authorized through one reviewable PR. Merge and live deployment
are not authorized. This is the product plan for this transformation, not a
replacement for the operations runbook or live-state readbacks.

## North star

Help a visitor move from a real example of Kris's work, through the judgment and
useful takeaway behind it, to a relevant conversation about their own work.
The site becomes a connected portfolio of practice: evidence people can explore,
learn from, and use to decide whether to work with Kris.

The audience for the first proof is a founder, team lead, or event organizer
trying to understand what a practical AI workflow session with Kris involves.
Broader audiences remain part of the site; this is the first journey to prove.

Preserve the personal voice, real photography, cream and ink palette, bold type,
rainbow identity, community roots, and experimental projects. Keep WordPress and
Aurora. Prefer deliberate connections between existing work over more content.

**Hypothesis:** an example plus a useful takeaway and contextual enquiry path
communicates the offer better than generic service claims alone. Conversion
improvement is unproven; a link working is not evidence of increased demand.

## Level of intervention and non-goals

Polish alone cannot connect the existing evidence to the offer. A platform rewrite
would add cost without testing that connection. Use bounded content and workflow
changes first; earn larger architecture changes through observed reuse.

No site rewrite, new CMS, new design system, chatbot, model integration, content
graph, new forms, pricing, invented results/testimonials, homepage overhaul, or
repository-wide cleanup. No automatic conversion of TODOs or old plans into work.
Subtraction means avoiding competing CTAs and redundant systems, not deleting
unverified assets, consumer-backed scripts, or other agents' work.

## Transformation roadmap

| Phase | Purpose | Gate before expanding |
|---|---|---|
| 1: North House proof | Connect Events, the published recap, and one Services example. Necessary foundations: content identity, exact preservation, reviewable preview, safe release/restore. | One reviewed PR; then separate live approval and a small comprehension evaluation. |
| 2: Curate a small set | If phase 1 helps visitors, apply the same example/takeaway/enquiry pattern to a few existing talks, projects or articles. This is the differentiator: Kris's practice and judgment, not a larger catalog. | Choose the next strongest existing example using reader feedback; define scope before creating issues. |
| 3: Make the pattern maintainable | Standardize only repeated authoring work that phase 2 demonstrates. Reuse existing content packs and event tooling. | Evidence of repeated effort; no general component framework by anticipation. |
| Optional experiments | Test a clearer entry point or a different contextual CTA if observed journeys warrant it. | Explicit experiment, baseline and stopping condition; no new backlog now. |

Reuse #403's design intent and #968's relaunch context. #960 is a distinct article,
not a replacement for the published North House recap. #480's CSS retirement and
#477's component work remain separate; #976 owns broad active-document drift.

## Current milestone: North House proof

Before: the North House Events card's "Recap / details" link goes to the host's
impact page; the recap has a takeaway but no contextual Services link; Services
offers workshops without this concrete example.

After: **Events -> Read the recap -> useful take-home challenge -> workflow-session
example on Services -> existing Contact enquiry path.** Visitors arriving directly
at Services can inspect the recap as evidence.

Only three published bodies are in scope: Events page 2250 (`events`), recap post
12744 (`what-i-showed-founders-about-ai-workflows`), Services page 2666
(`generative-ai-services`). Preserve the host URL, all other event records, article
argument, images, author section, Services layout/CSS, and all non-content fields.
Reuse approved photo 12742 without recropping or inventing a credit.

### Architecture and decisions

- An optional `recap_url` on this past catalog record changes its compact-card
  destination. The existing `url` remains the host/hero-source URL.
- One small Services fragment uses existing markup and a plain caption outside
  image overlays. Cut the insertion from fresh live `content.raw`; none of the
  older Services replacement packs is current. Do not unblock #480 by accident.
- A bounded three-target publisher helper reuses `scripts/common.py` and existing
  snapshot/hash patterns. Do not relax the draft-only updater or #832's target
  restrictions. No generic migration framework or dependency changes.
- Produce a private browser preview with the actual public page shell/assets and
  proposed bodies. It is a pre-deployment simulation, not WordPress server-side
  rendering or proof that public caches have updated.
- No application AI behavior changes, so model/API evals are not applicable.
- Browser spike decision: the new photo needs two local sizing declarations
  (`max-width:100%;height:auto`) to work without theme JavaScript. This preserves
  its natural ratio and all existing CSS; no stylesheet migration is involved.

### Done when

1. The entire proposed journey is browser-reviewable with named internal links.
2. Only approved body patches differ; Services CSS and unrelated content are exact.
3. Missing/ambiguous anchors, wrong ID/type/slug/status, stale hashes, missing
   snapshots, uncertain writes and wrong readbacks stop safely. Reapplication is
   a no-op; restoration refuses a conflicting live body.
4. Existing Events fallback, empty-state, merge, archive and escaping contracts pass.
5. New copy passes explicit voice checks; desktop/mobile, keyboard, console,
   image loading, fallback and JavaScript-disabled checks are recorded honestly.
6. The final diff passes relevant tests/lint and secret/scope review. One focused
   PR is open, with no merge or deployment.

After separate publication approval: authenticated raw readback must match the
reviewed payload; anonymous readback must show the expected journey. Serialize
Services -> recap -> Events and stop on failure. These writes are not a
transaction; there is a residual race between the final read and each write.

The product evaluation is pending: ask five representative visitors to find the
example, explain one useful takeaway, and locate a relevant enquiry within 90
seconds. Target 4/5. Record observations without treating this small sample as
conversion proof. Passing unlocks choosing the next example, not a site-wide roll-out.

## Technology verification and baseline

Official sources checked on 2026-09-05: WordPress [page updates](https://developer.wordpress.org/rest-api/reference/pages/)
and [post updates](https://developer.wordpress.org/rest-api/reference/posts/) support
the existing REST content update path; Python's [urllib.request](https://docs.python.org/3/library/urllib.request.html)
supports the existing client; Playwright's [network interception](https://playwright.dev/docs/network)
supports a local review without a WordPress mutation. Keep the installed versions;
this slice is not a framework or dependency upgrade.

Tracking issue: [#977](https://github.com/WalksWithASwagger/kriskrug-wp/issues/977).
Proof issue: [#978](https://github.com/WalksWithASwagger/kriskrug-wp/issues/978).
The [proof packet](../../content/drafts/2026-09-05-north-house-journey/README.md)
records baseline, implementation decisions, runbook and actual validation.
Fresh readback, not this dated plan, controls any future live operation.
