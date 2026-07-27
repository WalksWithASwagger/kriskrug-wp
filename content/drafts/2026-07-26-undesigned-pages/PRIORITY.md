# PRIORITY — Undesigned pages (#122)

**Date:** 2026-07-26  
**Inventory:** [`docs/current-state/reports/undesigned-pages-inventory-20260726.md`](../../../docs/current-state/reports/undesigned-pages-inventory-20260726.md)  
**Constraint:** No live WP writes in this packet. No theme stylesheet rebuild ([#474](https://github.com/WalksWithASwagger/kriskrug-wp/issues/474)+).

## How to read this

| Tag | Meaning |
|---|---|
| **BESPOKE** | Dedicated content redesign packet (Aurora primitives in page body). Avoid new hardcoded `page-*.html` unless layout cannot live in content. |
| **TEMPLATE** | Stay on generic `page.html`; benefit from floor polish + light content tidy. |
| **TRIAGE** | Ops/redirect/archive decision before design. |
| **TRACKED** | Owned by another issue — do not duplicate here. |

---

## P0 — Tracked elsewhere (do not fold into #122 execution)

| Path | Tag | Issue | Note |
|---|---|---|---|
| `/generative-ai-services/` | TRACKED | **#420** | Language, layout, scroll rethink |
| `/about/` | TRACKED | **#418** | Backgrounds / column widths / double public trail |
| `/speaking/` | TRACKED | **#419** | Multimedia rebuild that sells keynotes |
| `/contact/` | TRACKED | **#421** (closed) | Portrait + newsletter language shipped; only reopen if regression |

---

## P1 — Bespoke content packets (high value, still feel unfinished)

Ship as Track A body payloads using Jul 1 primitives (`aurora-proof-*`, `aurora-page-lead`, `aurora-display-heading`, cards/grids). One page (or family) per PR.

| Rank | Path | Why | Depends / pairs with |
|---:|---|---|---|
| 1 | `/testimonials/` | Legacy `user-infos`; social proof for home + offers | Homepage **#415** |
| 2 | `/publications/` | Has `kk-publications*` but still archive-shaped; proof trail | About / Speaking CTAs |
| 3 | `/photography/` | Gallery-heavy identity surface; weak page chrome | Media rights / alt lane |
| 4 | `/events/` | Long history blob; needs upcoming vs archive | Luma / speaking funnel |
| 5 | `/podcast-guesting-page-epk/` | Booking surface; already primitivized — multimedia pass | **#419** |
| 6 | `/work/` | Already primitivized — visual/proof refresh only if KK wants | Nav proof |
| 7 | `/the-kk-worldview/` | Authority page; short and plain | Brand / About |
| 8 | `/motleykrug-podcast/` | Legacy media page | Conversations hub |
| 9 | `/reconciliation-indigenous-land-acknowledgement/` | Short; should match site voice | **#22** |

---

## P2 — Template polish (generic `page` floor + light content)

Do **after** or **beside** #474 scaffold — not a parallel CSS rebuild. Content tidy can start now.

| Family | Paths | Treatment |
|---|---|---|
| Topic hubs (maintain) | `/vancouver-ai/`, `/ai-for-creatives/`, `/ai-events/`, `/ai-ethics/`, `/ai-tools/`, `/ai-for-journalists/`, `/ai-conversations/`, `/indigenous-ai/` | Already Aurora-primitivized; only shared hero/title suppress when template floor lands |
| Multilingual intros | 8 intros + optional Swahili welcome merge | **One shared pattern** (lede + embed + CTA to English About/Speaking) |
| Policy / utility | `/privacy-policy/`, `/product-review-policy-instructions/`, `/glossary/` | Prose rhythm only; no heroes |
| RAP | `/responsible-ai-professional/` | Maintain; offer copy refresh only if cohort dates change |
| Sponsor deck | `/sponsor-deck/` | Shipped 2026-07-24; maintain |

### Template floor backlog (theme — post-#474)

When stylesheet scaffold is safe:

1. Optional suppress of `.aurora-page-title` when body opens with `.aurora-display-heading` (kills double-title feel on About/Work/Speaking/Services).
2. Optional featured-image / media band above content.
3. Shared end-of-page CTA strip (Contact / Speaking / Services) as a pattern, not per-page CSS.

---

## P3 — Marketing long-tail (template polish **or** triage)

| Path | Default | Triage question |
|---|---|---|
| `/ai-upgrade-for-creative-professionals/` | TEMPLATE or TRIAGE | Cohort still running? Else redirect → Services / RAP |
| `/ai-upgrade-for-modern-media-leaders/` | TEMPLATE or TRIAGE | Same |
| `/ai-upgrade-community-coaching-w-kris-krug-peter-bittner/` | TEMPLATE or TRIAGE | Same |
| `/generative-ai-workshop-for-artists-creatives/` | TEMPLATE or TRIAGE | Evergreen workshop vs archive |
| `/sponsor-cyberpunk-chronicles-newsletter/` | TEMPLATE | Keep as newsletter sponsor pitch; do not confuse with `/sponsor-deck/` |
| `/art-island-perspectives-from-a-creative-community/` | TRIAGE | Keep as project archive or fold into Work |
| `/cinematic-podcasts-agencia-grade-storytelling-meets-generative-ai/` | TRIAGE | Keep vs fold into podcast / Work |
| `/news/` | TRIAGE | Redirect → Publications or About press section |

---

## P4 — Ops triage before any design

| Path | Problem | Suggested disposition (KK) |
|---|---|---|
| `/subscribe/` | Empty main in public readback | Point to homepage newsletter / Contact, or restore form |
| `/home/` | Overlaps `/blog/` “recent posts” | 301 → `/blog/` or unpublish |
| Swahili intro + Swahili welcome | Two near-duplicate URLs | Keep one canonical; 301 the other |

---

## Suggested wave plan

| Wave | Scope | Lane |
|---|---|---|
| **Wave 1** | KK approve this PRIORITY + triage P4 | Human |
| **Wave 2** | Testimonials + Publications + Photography content packets | Track A |
| **Wave 3** | Events + Worldview + Reconciliation (+ #22) | Track A |
| **Wave 4** | Multilingual shared pattern roll-out | Track A |
| **Wave 5** | `page.html` floor (title suppress / media / CTA) | Track B — **after #474** |
| **Parallel** | Services #420, About #418, Speaking #419 | Existing PAGE issues |

## Out of scope for this draft folder

- Theme CSS / `theme.json` / FSE template rebuilds
- Live REST updates
- Closing #122 (needs Waves 2–5 + #420 progress)
