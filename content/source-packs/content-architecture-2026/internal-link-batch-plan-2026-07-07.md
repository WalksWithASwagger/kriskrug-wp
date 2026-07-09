# Internal-link batch plan — topic hubs (2026-07-07 / refreshed 2026-07-08)

Status: agent-safe planning packet for #305. Supports #278 and #284.  
No WordPress write was performed.

## Goal

Add a small, editorially natural set of body-only internal links from existing posts into the live topic hubs, without stuffing, circular links, or Indigenous AI links that need human review first.

## Live hub targets (verified 2026-07-08)

| Hub | URL | HTTP |
|---|---|---|
| AI Ethics | https://kriskrug.co/ai-ethics/ | 200 |
| AI Tools | https://kriskrug.co/ai-tools/ | 200 |
| AI Conversations | https://kriskrug.co/ai-conversations/ | 200 |
| AI for Journalists | https://kriskrug.co/ai-for-journalists/ | 200 |
| Vancouver AI | https://kriskrug.co/vancouver-ai/ | 200 |
| Indigenous AI | https://kriskrug.co/indigenous-ai/ | 200 |
| AI for Creatives | https://kriskrug.co/ai-for-creatives/ | 200 |
| AI Events | https://kriskrug.co/ai-events/ | 200 |

## Autonomous-safe batch (body-only REST candidates)

Use only after: authenticated slug/ID/status check, before/after snapshot, dry-run payload review, and body-only update (no `title` field).

| # | Source post | Source URL | Target hub | Suggested anchor | Rationale | Risk |
|---|---|---|---|---|---|---|
| 1 | Artists Learn. Machines Extract. | https://kriskrug.co/2026/07/06/artists-learn-machines-extract/ | `/ai-ethics/` | AI ethics | Direct ethics/extraction thesis | Low |
| 2 | AI Media Appearances | https://kriskrug.co/2026/07/02/ai-media-appearances-podcast-guesting/ | `/ai-conversations/` | AI conversations | Media/interview surface | Low |
| 3 | AI Media Appearances | https://kriskrug.co/2026/07/02/ai-media-appearances-podcast-guesting/ | `/ai-for-journalists/` | AI for journalists | Journalism/media audience overlap | Low |
| 4 | Zero to One | https://kriskrug.co/2026/06/30/zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey/ | `/vancouver-ai/` | Vancouver AI | Origin story for the local ecosystem | Low |
| 5 | What Would Chat Do? | https://kriskrug.co/2026/06/28/what-would-chat-do-and-why-thats-the-wrong-question/ | `/ai-ethics/` | AI ethics | Agency/ethics framing | Low |
| 6 | Canada Does Not Need a Bigger AI Machine | https://kriskrug.co/2026/06/26/canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one/ | `/ai-ethics/` | AI ethics | Policy/ethics critique | Low |
| 7 | AI Will Not Fix Your Broken Permit Process | https://kriskrug.co/2026/06/24/ai-wont-fix-your-broken-permit-process/ | `/ai-ethics/` | AI ethics | Governance/responsibility | Low |
| 8 | The Great Canadian Proximity Game | https://kriskrug.co/2026/06/22/the-great-canadian-proximity-game/ | `/vancouver-ai/` | Vancouver AI | Local ecosystem / proximity thesis | Low |
| 9 | Why We Built RAP | https://kriskrug.co/2026/06/18/why-we-built-the-responsible-ai-professional-certification/ | `/ai-ethics/` | AI ethics | Responsible AI certification | Low |
| 10 | STORYHIVE / Jordan Dack | https://kriskrug.co/2026/06/17/storyhive-haus-of-owl-jordan-dack/ | `/ai-conversations/` | AI conversations | Long-form conversation | Low |
| 11 | STORYHIVE / Jordan Dack | https://kriskrug.co/2026/06/17/storyhive-haus-of-owl-jordan-dack/ | `/ai-tools/` | AI tools | Workflow/tooling discussion | Low |
| 12 | Speak It Into Existence | https://kriskrug.co/2026/06/13/speak-it-into-existence-ai-voice-first-workflows/ | `/ai-tools/` | AI tools | Voice-first workflow tools | Low |
| 13 | AI Keynote Slides Need Taste Before Prompts | https://kriskrug.co/2026/06/04/ai-keynote-slides-visual-workflow/ | `/ai-tools/` | AI tools | Visual workflow / tooling | Low |
| 14 | You Cannot Drink Data | https://kriskrug.co/2026/05/23/you-cant-drink-data/ | `/ai-ethics/` | AI ethics | Infrastructure ethics / protest | Low |

## Human-review queue before any Indigenous AI links

Do **not** auto-add `/indigenous-ai/` links from these posts without KK editorial review:

- AI Media Appearances
- Zero to One
- What Would Chat Do?
- Canada Does Not Need a Bigger AI Machine
- AI Will Not Fix Your Broken Permit Process
- You Cannot Drink Data

Rationale: Indigenous AI hub linking needs cultural/editorial judgment, not just topical keyword overlap. Track under #284.

## Implementation checklist (follow-up issue / publisher mode)

1. Authenticated fetch of each source post by slug/ID; confirm `status=publish`.
2. Snapshot `content.raw` before edit under `backup/<timestamp>-topic-hub-internal-links/`.
3. Insert one natural contextual sentence or phrase with the hub link; avoid nav dumps and footer-style link piles.
4. Skip if the post already links the same hub URL.
5. Body-only REST update (no `title`, no taxonomy changes).
6. Cache-busted public smoke: source URL returns 200 and contains the hub href.
7. Record before/after URL list in the follow-up issue.

## Stop rules

- Do not run `scripts/content_architecture_deploy.py --execute`.
- Do not publish or update WordPress content from this planning issue.
- Stop if a target hub returns non-200 or a source post is not publicly published.

## Verification recorded

- Hub URLs checked 2026-07-08 (all 200 after retry for `/ai-tools/`).
- Source post URLs resolved via public WP REST by slug.
- Payload tests for architecture packs remain the existing `scripts.tests.test_content_architecture_payloads` suite; no payload files were changed in this packet.
