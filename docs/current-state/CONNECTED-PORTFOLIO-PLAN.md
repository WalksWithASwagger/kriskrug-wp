# Open Studio: connected portfolio of practice

**Decision:** KK approved the Open Studio successor blueprint on 2026-09-06 and
requested development issues and their ordered agent swarm. This document records
that approved destination. It supersedes only the earlier forward roadmap and
changed non-goals; the original 2026-09-05 approval is retained below.

**Authority:** stop at focused reviewable PRs. Approval of this development plan
is not permission to merge, deploy, publish, contact research participants, use
paid models, expose private sources, or change shared/global configuration.
Implementation completion, human evaluation and live-release authority are
separate gates. The [operations front door](README.md), repository instructions
and fresh readbacks still govern operational work.

Single tracker: [#977](https://github.com/WalksWithASwagger/kriskrug-wp/issues/977).
The issue map below is the first-proof scope, not permission to implement the
whole roadmap. No future experiment is automatically dispatched.

## North star and product decisions

**Real work you can learn from by doing:** see real work, try a method, and leave
with a useful artifact. Each practice connects **public source -> judgment ->
visitor attempt -> usable artifact**. Open Studio describes the experience, not
a separate brand or subscription product. A plain invitation such as "Try a
method" should name the visitor's task and outcome.

The primary audience hypothesis is creative professionals, founders/team leads,
and community organizers facing a concrete task. Bookers can understand Kris's
judgment by trying it. Preserve WordPress, Aurora, documentary photography,
personal voice, cream/ink palette, bold type, rainbow identity, community roots,
experimental projects, and the existing Contact path.

Five product decisions:

1. Organize participation around a task rather than generic service claims.
2. Trace each exercise to real practice; label newly authored teaching examples.
3. Make the useful artifact the primary outcome, without a lead gate.
4. Prove three carefully curated practices before expanding the catalog.
5. Keep expressive presentation around readable, dependable interactions.

The three-practice destination is context-brief preparation from North House;
photography negotiation preparation reusing
[#828](https://github.com/WalksWithASwagger/kriskrug-wp/issues/828) after editorial
approval; and factual human/AI contribution disclosure reusing
[#966](https://github.com/WalksWithASwagger/kriskrug-wp/issues/966) and
[#883](https://github.com/WalksWithASwagger/kriskrug-wp/issues/883) after public-source
and consent review. Existing article material is evidence, not publication consent.

**Hypothesis:** doing a guided exercise helps visitors produce better work and
understand Kris's practice more clearly than reading and contacting alone.
Repeat usefulness and better-informed enquiries are unproven benefits. Neither
working links nor successful exports establish demand or conversion improvement.

## Scope changes and non-goals

The earlier proof's no-form restriction remains intact for #978/#979. The
successor permits one browser-only guided exercise. It introduces no enquiry
form or server collection of answers. The earlier no-homepage-overhaul decision
also remains: a bounded homepage/Work entry is a later evidence-gated milestone.
Optional AI evaluation is now a possible future experiment, not first-proof scope.

No CMS/headless rewrite, new design system, general chatbot or Kris replica,
public community digital twin, vector database, archive-wide ingestion, accounts,
CRM, lead-gated downloads, generated documentary imagery, 3D navigation, automated
article backlog publication, contract generation, automated pricing advice, or
prerequisite site-wide CSS cleanup. Never infer consent to publish private Plaud,
Notion, participant or photo-library material from the existence of an issue.

Reuse existing work; verify consumers before recommending removal. Preserve the
marquee tooling's active consumers and other agents' changes. Design intent in
[#403](https://github.com/WalksWithASwagger/kriskrug-wp/issues/403) and relaunch
context in [#968](https://github.com/WalksWithASwagger/kriskrug-wp/issues/968) remain
useful. [#477](https://github.com/WalksWithASwagger/kriskrug-wp/issues/477) and
[#480](https://github.com/WalksWithASwagger/kriskrug-wp/issues/480) own their separate
CSS/component work. [#976](https://github.com/WalksWithASwagger/kriskrug-wp/issues/976)
owns broad documentation drift; this plan does not revise that lane's README.

## Architecture decisions for the first proof

- Keep WordPress pages/revisions as published truth; Git holds code, reviewed
  packets, tests and decisions. Do not create a second synchronized content store.
- Use one small site plugin with a purpose-built native `kk/context-brief` block,
  WordPress-provided editor facilities and small frontend JavaScript. Aurora owns
  visual tokens. No generic form builder, framework rewrite or production service.
- Capture six fields: **objective, audience, available sources, success conditions,
  privacy/exclusions, and human review**. Do not infer missing answers.
- Keep answers in browser memory only. Offer editable preview, copy, Markdown
  download and print, with selectable-text and no-JavaScript worksheet fallbacks.
  No accounts, autosave, uploads, URL fetching, server persistence or runtime AI.
- Render answers as text. Keep them out of URLs, block attributes, revisions,
  analytics, logs and persistent storage. Verify the route's third-party scripts,
  including the existing delayed loader, before promising browser-only handling.
- Test actual WordPress rendering with a public synthetic fixture. A patched
  public HTML shell is not PHP/plugin proof. Timebox rendering and route-privacy
  spikes before implementation; record limitations rather than widening scope.
- Extend PHP, JavaScript, smoke and CI coverage to include the new files explicitly.
  Existing enumerated paths passing cannot prove new-plugin coverage.

On implementation, verify current official dependency documentation and supported
versions rather than treating the dated blueprint's Playground or model candidates
as permanent requirements. No dependency or model is introduced by this docs change.
If Playground cannot reproduce the required WordPress version, report the blocker
and staging requirement; do not claim an older or static fixture has live parity.

## First-proof ownership and dependency map

| Issue | Owner surface | Start and stop rule |
|---|---|---|
| [#980](https://github.com/WalksWithASwagger/kriskrug-wp/issues/980) | This durable plan; README only if coordinated with #976 | Ready for bounded drafting; one docs PR, no merge. |
| [#981](https://github.com/WalksWithASwagger/kriskrug-wp/issues/981) | Teaching packet and usability protocol | May run beside #980 in disjoint files; one content PR; examples and protocol require review. |
| [#982](https://github.com/WalksWithASwagger/kriskrug-wp/issues/982) | Context-brief plugin and its test/Makefile/PHPCS/CI integration | Starts after accepted #980/#981 handoffs; serialize shared files; one vertical proof PR. |
| [#983](https://github.com/WalksWithASwagger/kriskrug-wp/issues/983) | Separate Track A validation/publication preparation | Depends on #982; exact release payload and human evidence remain separate gates. No automatic live write. |

Use isolated `codex/` branches/worktrees. Never reset, stash, overwrite, synchronize,
merge or delete another lane blindly. Recheck issue labels/dependencies before
starting: an old table or closed dependency does not replace accepted handoffs or
remove a stop label. Parent coordination owns routing; agents do not expand scope.

Retain [#978](https://github.com/WalksWithASwagger/kriskrug-wp/issues/978) and
[PR #979](https://github.com/WalksWithASwagger/kriskrug-wp/pull/979) as the existing
entry proof. At this plan's 2026-09-06 GitHub readback #979 was still draft/open at
`dafe104e64d7aaa765e5d2a147f7447814c36058`. Its three-target writer and authority are
unchanged. Review its own packet for implementation evidence; this successor does
not claim a deployment or completed visitor evaluation.

## Milestones and evidence gates

| Milestone | User-visible outcome | Gate and exclusions |
|---|---|---|
| Existing entry proof, #978/#979 | Events -> North House recap -> Services example -> Contact | Review existing PR, then separate publication permission and readbacks; evaluate comprehension. Do not widen this PR. |
| First practice, #980-#982 | Source -> six-field exercise -> editable, exportable brief in real WordPress | Accepted teaching packet, rendering/privacy spikes and application tests; no AI, server answers or other practices. |
| First release preparation, #983 | Reviewed practice page and contextual source entry, with fallback | Human evidence reported honestly; exact payload, snapshots, identity/conflict guards and rollback before separate live permission. |
| Two further practices | Photography preparation and contribution disclosure artifacts | First-practice usefulness evidence and source/editorial approvals; implement sequentially with only demonstrated utility reuse. |
| Three-practice index and bounded entry | Visitors choose by task, time and outcome from homepage/Work | Three useful practices; preserve Writing, Photography, talks and Contact; no global navigation or CSS rewrite. |
| Optional AI critique | Visitors resolve omissions missed by the existing prompts | Recorded no-AI application baseline, measurable improvement, access/cost/latency/capacity tests, accurate disclosure and checklist fallback. No current implementation authority. |
| Optional multimodal source assistance | Editors find verified excerpts in approved public talks faster | Demonstrated editorial bottleneck and measured time savings; human source verification. No private-corpus ingestion or current implementation authority. |

Later milestones remain tracker notes, not dispatched backlog. AI critique would
be one bounded, explicitly requested review, with no tools, automatic rewriting or
silent provider switch. Test the complete application path, refusals, timeouts,
privacy and budgets. Model output formatting is not factual verification. Reject
an experiment that adds verbosity or expense without improving the artifact.

## Current milestone: exact done conditions

The first practice must show the source and a clearly labeled authored example,
then let a visitor use the six fields and export their own working brief.

1. A real WordPress preview demonstrates the entire journey. Answers survive
   switching between entry and preview; incomplete drafts remain exportable.
2. Missing information is explicit. The proposed 8,000-character total bound is
   explained and never silently truncates. HTML-like text stays literal.
3. Copy failures offer selectable output; download, print and no-JavaScript
   worksheet fallback remain useful. Missing imagery never blocks the exercise.
4. Synthetic canary answers appear in no network request, URL, persistent browser
   storage, analytics or application log on the tested application path.
5. Review keyboard operation, screen-reader labels/status, visible focus,
   320/390/768/1280-pixel layouts, 200% zoom, reduced motion and console output.
6. Proposed incremental asset budget is 20 KB compressed JS/CSS; local preview
   generation targets under 100 ms on an identified test device. Measure both.
7. Run applicable tests, lint, smoke, build/CI and final diff/secret review. Report
   passing, pre-existing failing, newly failing, skipped and unavailable separately.
8. Implementation completion means a reviewable proof PR with evidence, not a
   claim that usability or production publication is complete.

**Human gate:** compare with reading the recap and a blank worksheet. Proposed
initial target: 4/5 representative visitors produce a usable brief within ten
minutes without facilitator intervention. A follow-up target of 3/5 reporting
actual use is a hypothesis. Missing participants or observations remain pending.
A small cohort provides directional evidence, not statistical conversion proof.
No participant outreach is authorized by development dispatch.

**Release gate:** exact reviewed payload, explicit KK permission, snapshots,
identity/conflict guards, rollback and authenticated raw plus anonymous public
readbacks. Install verified capability before dependent content, then publish
entry links last. Roll back links/content first and then plugin version, retaining
a useful public URL fallback. Preserve the separate Track A release lane.

**Decision unlocked:** whether guided participation produces a better usable
artifact than the existing reading journey. If it does, choose the photography
practice after its source review. If it does not, revise the first exercise before
adding a catalog, redesign or model feature.

## Historical approval and receipts: 2026-09-05

The original plan follows verbatim inside a historical block. Its forward roadmap
and changed non-goals are superseded above; its bounded approval and safety
receipts remain valid for #978/#979. The original proof packet is pinned to the
reviewed branch commit because it is not yet on main:
[North House proof packet](https://github.com/WalksWithASwagger/kriskrug-wp/blob/dafe104e64d7aaa765e5d2a147f7447814c36058/content/drafts/2026-09-05-north-house-journey/README.md).
Relative links inside the quoted original resolve in that original PR tree.

```markdown
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
```
