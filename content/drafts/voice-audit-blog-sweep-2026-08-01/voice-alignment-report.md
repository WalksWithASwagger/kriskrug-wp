# Voice alignment report — 15-post blog sweep (2026-08-01)

## Scope

Fifteen live posts on [kriskrug.co](https://kriskrug.co/), published 2026-06-18 through 2026-07-31. Audited against live `content.rendered` (WP REST snapshots in `snapshots/`), not local drafts. Punch list: [`00-summary.md`](00-summary.md). Mechanical detail: [`slop-check-findings.md`](slop-check-findings.md). Per-post deep notes: [`readings/`](readings/).

## Method

1. Snapshot rendered HTML + stripped text for all 15 posts.
2. Mechanical pass: `~/Code/kk-voice/scripts/voicecheck.py --json` (44 flags; 8 posts clean).
3. Facet routing from `crystal.md` (audience/channel → ED / Host / Builder / Anti-Hero / Friend).
4. Dodged-tell manual scan on every post (redefinition-reveals, list-stacking, copula avoidance, conclusion restates, manufactured vulnerability, en-dash-as-em-dash, etc.).
5. Full five-question deep reads on worst offenders: ai-lands (mandatory), zero-to-one, god-skills, canada (escalated), what-would-chat-do (escalated), plus several July escalations.
6. Drift check: Jul 10 live post vs prior clean draft audit (similarity 1.0000).

Suggested rewrites in the reading files were batch-verified through `voicecheck.py` (exit 0) before being recorded.

## Facet distribution

| Facet (dominant) | Posts |
|---|---|
| ED | ai-lands, canada (essay half), permit, responsible-ai-cert, ai-media |
| Host | ethos-lab-block-party, what-would-chat-do (essay) |
| Builder | god-skills, no-one-knows-what-to-call-us-yet |
| Anti-Hero | artists-learn, cheer-is-a-cap-table, i-am-nomad, proximity-game, vancouver-made-world-cup |
| No facet / wrong frame | zero-to-one (third-person about "Krüg"); canada/what-would-chat-do appended halves (internal docs, no public facet) |

---

## Per-post (newest first)

### 2026-07-31 — AI Lands Inside Every Profession

- **Facet:** ED + Host, Anti-Hero close | **Depth:** deep read | **Mechanical:** 27 (26 prose em dashes + soft team)
- **Verdict:** Under the punctuation, genuinely Kris in ED mode: receipts dense, credit distributed by name, both/and held. Dragged by em-dash infestation (more than the other 14 posts combined) and ~8 redefinition-reveals turning cadence into template.
- **Working:** "Ecosystem is not a vibe. It is repeated contact with consequences." / planetarium-dome venue-rental line / "Retention slogans are cheap. Return pathways are policy." / Daisy Xiong credited through the close.
- **Hard rules:** 26 prose em dashes. Full 23-edit verified fix table in [`readings/2026-07-31-ai-lands-inside-every-profession.md`](readings/2026-07-31-ai-lands-inside-every-profession.md).
- **Judgment:** Keep two reveals (venue rental; ecosystem-is-not-a-vibe); thin the rest. Soft `team sport` keep. Futureproof naming consistency decision needed.

### 2026-07-28 — No One Knows What to Call Us Yet

- **Facet:** Builder + Host | **Depth:** deep read (escalated) | **Mechanical:** 0
- **Verdict:** Sounds like Kris the whole way. Taxonomy of responsibilities over buzzwords; wins credited by name. Zero hard-rule items. Reveal density (~5) is a watch note, every instance individually defensible.
- **Working:** Timestamped community question credited; Daniela Gamarra, Kevin Friel, Luke Minaker, Mayumi Rollings named; labour-politics section has edge.
- **Flagged:** judgment-only reveal watch. No hard fixes.
- **Reading:** [`readings/2026-07-28-no-one-knows-what-to-call-us-yet.md`](readings/2026-07-28-no-one-knows-what-to-call-us-yet.md)

### 2026-07-18 — I AM NOMAD

- **Facet:** Anti-Hero + Builder | **Depth:** standard | **Mechanical:** 0
- **Verdict:** Most alive voice in the July batch. Failure held without flinching; field-guide half is Builder at full generosity. One content catch, not slop: closing line inverts the film's premise.
- **Working:** "Suzy and I made the project. The AI helped us build it." / Down/Up arc earned with sync-drift and four-word-note specifics.
- **Flagged:** closing-line logic fix (verified one-liner in reading). One reveal keep ("lyric grid isn't decoration. It's the spine.").
- **Reading:** [`readings/2026-07-18-i-am-nomad-ai-film.md`](readings/2026-07-18-i-am-nomad-ai-film.md)

### 2026-07-10 — Watch Who's Smiling (the-cheer-is-a-cap-table)

- **Facet:** Anti-Hero + Friend | **Depth:** prior-audit reconfirm | **Mechanical:** 0
- **Verdict:** Prior "ships clean" stands. Drift check: word-level similarity **1.0000** vs audited draft; 0 em dashes either side. Fresh dodged-tell skim changes nothing.
- **Working:** money spine, named critics, dense receipts (~$3B, Inflection, XPRIZE figures).
- **Flagged:** "buckle-up" hyphenated irony keep (dodges space-anchored regex; intentional).
- **Reading:** [`readings/2026-07-10-the-cheer-is-a-cap-table.md`](readings/2026-07-10-the-cheer-is-a-cap-table.md) · drift: [`drift-check-the-cheer-is-a-cap-table.md`](drift-check-the-cheer-is-a-cap-table.md)

### 2026-07-06 — Artists Learn. Machines Extract.

- **Facet:** Anti-Hero + ED | **Depth:** deep read (escalated) | **Mechanical:** 0
- **Verdict:** Manifesto register done mostly right. Morgane Oger centered from sentence one; real legal receipts (CCH, Cinar, Copyright Act, EU AI Act). One passage is the literal confirmed checker blind spot.
- **Working:** mine/classroom/compost imagery; anaphora ladders that earn payload.
- **Flagged:** L38-40 decontracted "That is not just X. It is Y." (judgment de-template). Open/close "Not A. Not B. C." ladders named as cross-post template risk.
- **Reading:** [`readings/2026-07-06-artists-learn-machines-extract.md`](readings/2026-07-06-artists-learn-machines-extract.md)

### 2026-07-02 — AI Media Appearances, Podcast Guesting…

- **Facet:** ED + Host | **Depth:** standard | **Mechanical:** 0
- **Verdict:** Low severity. Clean mechanical run; hand-caught canonical miss and spelling inconsistency.
- **Hard rules (manual):** "Kris Krug" without umlaut (L14 link text); Kharé/Khare both ways on one page.
- **Judgment:** two decontracted not-just templates.
- **Reading:** [`readings/2026-07-02-ai-media-appearances-podcast-guesting.md`](readings/2026-07-02-ai-media-appearances-podcast-guesting.md)

### 2026-06-30 — Zero to One: From Meetup to Movement

- **Facet:** expected ED; **reads as no facet** (third-person about "Krüg") | **Depth:** deep read | **Mechanical:** 6
- **Verdict:** Worst voice-alignment in the sweep. Unedited AI research-report frame under his byline: "Krüg stated," newsy headers, uniform triumphant tone, Nov-2025 vantage published June 2026 with future tense. Raw material (names, numbers, values) is excellent; the frame is wrong.
- **Working:** distributed credit (Gabriel George Sr., Carol Ann Hilton, Lorraine Lowe, Matthew Schwartzman, et al.); receipt density; OCAP/Indigenomics substance.
- **Hard rules:** seamless, cutting-edge, pivotal, "no X, no Y, just Z," soft team x2 (one keep-as-quoted, one needs Tyler introduced).
- **Judgment / structural:** person-shift required; stale future tense; internal date contradictions (Aug 2024 vs Aug 2025 registration); membership price/count conflict with June 18 cert post ($240/130 vs $340/99+).
- **Reading:** [`readings/2026-06-30-zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey.md`](readings/2026-06-30-zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey.md)

### 2026-06-28 — What Would Chat Do?

- **Facet:** Host + Anti-Hero (essay); appended half has no public facet | **Depth:** deep read | **Mechanical:** 1 (idiomatic team, keep)
- **Verdict:** Essay itself is among the most Kris-sounding June pieces. Published page is an assembly accident: panel-prep notes after the bio, systematic en-dash-as-em-dash, umlaut miss in bio.
- **Working:** bathtub vibe-coding opener; both-hands-full; CASK/Liz Marshall credit; "bias laundering" coinage; Fernanda quote left unsanitized.
- **NOT-VOICE:** prep block from "KEY VIRAL QUOTES…" through panel questions; corrupted arrows (`→`→`?`); run-together list items.
- **Judgment:** en-dash prose cleanup; thin ~10 reveals (keep the mirror thesis); cut hollow closers ("The choice is ours.").
- **Reading:** [`readings/2026-06-28-what-would-chat-do-and-why-thats-the-wrong-question.md`](readings/2026-06-28-what-would-chat-do-and-why-thats-the-wrong-question.md)

### 2026-06-26 — Canada Doesn't Need a Bigger AI Machine…

- **Facet:** ED + Anti-Hero (essay); memo half is internal strategy, no public facet | **Depth:** deep read | **Mechanical:** 2
- **Verdict:** Two documents published as one. Essay is strong ED-with-edge, fair to Cohen, receipt-dense. Then a full internal strategy memo (alignment scores, Voice Profile / KK Worldview citations, Notion/file artifacts) ships to every reader.
- **Working:** rainy-Vancouver cold open; "He's not wrong" before critique; "trust is the limiting reagent"; "faster leak" close.
- **Hard rules:** stakeholders; thought leadership (memo half).
- **NOT-VOICE (the real story):** unpublish memo from "Cohen White Paper Critique…" through References; remove Voice Profile / KK Worldview leaks; delete filename/Notion residue; fix duplicated section and run-together lists.
- **Reading:** [`readings/2026-06-26-canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one.md`](readings/2026-06-26-canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one.md)

### 2026-06-24 — AI Won't Fix Your Broken Permit Process

- **Facet:** ED + Builder | **Depth:** standard | **Mechanical:** 0
- **Verdict:** Strongest long-form voice in the June batch. Grounded, measured, evidence-front-loaded, still vivid. Negative control for what earned contrast looks like when a lived civic incident is at the core.
- **Working:** concrete city-hall / permit process receipts; plain copulas; edge without doom.
- **Flagged:** none material.
- **Reading:** [`readings/2026-06-24-ai-wont-fix-your-broken-permit-process.md`](readings/2026-06-24-ai-wont-fix-your-broken-permit-process.md)

### 2026-06-23 — Vancouver Made World Cup

- **Facet:** Anti-Hero + Builder | **Depth:** standard | **Mechanical:** 0
- **Verdict:** Unmistakably Kris. Sacred and profane held together; receipts as the art form. "Everyone else made a souvenir. We made the receipt." is exemplar-grade.
- **NOT-VOICE:** `Eth??s` in cross-link list (same encoding class as block-party).
- **Reading:** [`readings/2026-06-23-vancouver-made-world-cup.md`](readings/2026-06-23-vancouver-made-world-cup.md)

### 2026-06-23 — The Ethos Lab Block Party Album

- **Facet:** Host (+ Friend close, Anti-Hero sign-off) | **Depth:** standard | **Mechanical:** 1 (title spelling)
- **Verdict:** Fully him. Warm, specific, consent-centered, funny; credit flows to people who gave the songs. Voice test passes every section. Broken rendering only.
- **Hard rules:** title "Ethos Lab" → Ethọ́s Lab.
- **NOT-VOICE:** `Eth??s` x7 in body/player/credits (stored content).
- **Reading:** [`readings/2026-06-23-ethos-lab-block-party.md`](readings/2026-06-23-ethos-lab-block-party.md)

### 2026-06-22 — The Great Canadian Proximity Game

- **Facet:** Anti-Hero | **Depth:** standard | **Mechanical:** 1 (satirical dialogue — keep)
- **Verdict:** Fully him. Precise anger, satire that punches at institutions not down. "You can delete a comment off your page. You cannot delete the work off mine."
- **Flagged:** "stakeholder alignment" inside quoted committee-speak. Keep confirmed (hollowness is the joke).
- **Reading:** [`readings/2026-06-22-the-great-canadian-proximity-game.md`](readings/2026-06-22-the-great-canadian-proximity-game.md)

### 2026-06-20 — A Practical Guide to Agentic Workflows (god-skills)

- **Facet:** Builder | **Depth:** deep read | **Mechanical:** 6 (all table-separator syntax)
- **Verdict:** Prose ~80% him-as-Builder. Two tables are a live rendering bug that matters more than word choice. Redefinition skeleton ~12 times; fails Builder receipts test (no named student wins; "sanitized examples").
- **Working:** "enthusiastic mess," "a rail, not a maze," "drifting into theatre."
- **NOT-VOICE:** rebuild two markdown tables as proper blocks (clears all 6 mechanical flags).
- **Judgment:** thin reveal density; add real named receipts when rewritten.
- **Reading:** [`readings/2026-06-20-god-skills-agentic-loop-workflows.md`](readings/2026-06-20-god-skills-agentic-loop-workflows.md)

### 2026-06-18 — Why We Built the Responsible AI Professional Certification

- **Facet:** ED + Builder | **Depth:** standard | **Mechanical:** 0
- **Verdict:** Sounds like Kris in ED mode. Evidence-front-loaded; instructors credited; enough edge ("'neutral' is a position too"). Voice dips where redefinition-reveal stacks in the back half. Membership numbers contradict zero-to-one.
- **Working:** opening anecdote; program mechanics concrete; "'neutral' is a position too."
- **Flagged:** reveal stack (judgment); cross-post price/count conflict ($340/yr, 99+ members vs zero-to-one's $240/yr, 130).
- **Reading:** [`readings/2026-06-18-why-we-built-the-responsible-ai-professional-certification.md`](readings/2026-06-18-why-we-built-the-responsible-ai-professional-certification.md)

---

## Cross-post patterns

### 1. The anti-glossary was dodged, not absent

Three workaround families across the June pipeline batch (and July density echoes):

- En dashes doing em-dash work (what-would-chat-do).
- Em dashes apparently search-replaced into comma splices (zero-to-one's pervasive splice rhythm).
- Decontracted / split "X is not A. It is B." reveals at high density (god-skills ~12, what-would-chat-do ~10, ai-lands ~8, artists-learn textbook specimen). The contraction-anchored checker regex never sees these.

### 2. Assembled-document publishing

Internal or half-built material shipped verbatim:

- Canada: full strategy memo with Voice Profile / KK Worldview / Notion residue.
- What Would Chat Do: panel-prep notes ("? Use:" lines).
- God Skills: pasted markdown tables as gibberish.
- Encoding mangles: Ethọ́s→Eth??s (two posts); arrows→`?` (what-would-chat-do).

Nothing got a human read-through between source pack and publish.

### 3. Voice splits on lived incident

Posts built on a real first-person moment (block-party, world-cup, proximity, permit, i-am-nomad, cheer) are fully him. Content-calendar / assembled pieces (zero-to-one, leaked halves, em-dash-heavy ai-lands) carry the tells and the factual drift.

### 4. House tic: redefinition-reveal density

Same rhetorical move, batch-wide. Individually it often matches his exemplar cadence. The problem is ration. Thin to the keep-instances named in `00-summary.md` P2; propose soft regex for `anti-glossary.md` (see checker-gap candidates there).

### 5. Canonical hygiene in low-attention spots

Umlaut-less "Kris Krug," Ethos vs Ethọ́s, Kharé/Khare, Futureproof naming variants. Checker misses several of these today.

---

## Notes

- Originals untouched. Advisory only.
- Skill tooling path is stale (`~/Code/dark-crystal/kk-voice/` → actual `~/Code/kk-voice/`).
- Generated 2026-08-01 from live REST snapshots.
