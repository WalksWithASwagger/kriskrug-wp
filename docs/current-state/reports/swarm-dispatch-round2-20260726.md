# Swarm dispatch round 2 — 2026-07-26

**Orchestrator:** [Sub agent swarm issues](https://cursor.com/agents/bc-019f9ff5-03d9-7811-b160-b82e45b0f196)  
**Command board:** #495  
**Mode:** 10 parallel `best-of-n-runner` subagents; draft PRs only; no live WP publish.

Round 1 covered Lane B home/pages + FP Wave 1 + #369 + #494. Round 2 takes the next agent-safe backlog slice.

## Dispatched and landed

| Issue | Branch | Draft PR | Result |
|---|---|---|---|
| #499 FP-3 story | `cursor/499-futureproof-story-f196` | #518 | ~1103-word em-dash-free post.md/html + SEO side files |
| #402 SEO hubs | `cursor/402-seo-authority-hubs-f196` | #517 | 5 hub outlines + live order |
| #288 a11y statement | `cursor/288-a11y-statement-f196` | #516 | Public-ready `/accessibility/` draft; still 404 live |
| #290 About/bio payload | `cursor/290-about-bio-payload-f196` | #523 | Folds #269/#270; coordinates with #418/#504 |
| #22 land acknowledgment | `cursor/22-land-acknowledgment-f196` | #520 | Footer already present; tone/placement polish options |
| #4 alt text inventory | `cursor/4-alt-text-inventory-f196` | #524 | S0 media 6835 on `/home/`; patch JSON staged |
| #122 undesigned pages | `cursor/122-undesigned-pages-f196` | #515 | ~25 long-tail inventory + priority |
| #249 YCDD measure | `cursor/249-ycdd-seo-measure-f196` | #521 | Recommend About exact-match backlink; GSC pull owed |
| #423 stylesheet decision | `cursor/423-stylesheet-decision-f196` | #522 | **Recommend Path B** (staged repair / aligns with #493) |
| #277 contact CTA | `cursor/277-contact-cta-decision-f196` | #519 | Keep mailto; form stub parked |

## Still not dispatched

- Blocked theme chain: #475–#481, #424, #127 (need #493 pixel gate)
- FP-4 #500 (needs KK voice OK on #518 + WP creds)
- SEO live batch #339 / #331 / #274 (creds + KK gates)
- #385 external `kk-agents#2`
- #276 Jetpack delete (KK deploy gate)

## KK next (round 2)

1. Comment Path B on #423 using brief in #522 (unblocks narrative for 1.5.x)
2. Voice-review #518 then authorize #500 dry-run → draft create
3. Approve #516 a11y statement wording; decide `/accessibility/` publish
4. GSC pull for #249; approve About YCDD backlink
5. Decide #277 keep-mailto (default) after checklist
6. Still owed from round 1: pixel harness for #493, reclaim paths #502

## Safety observed

- No live WP REST writes / media PATCHes
- #499 speakers limited to FP-2 cleared list
- #423 docs-only (no theme behavior change)
