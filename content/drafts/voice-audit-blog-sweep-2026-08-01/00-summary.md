# Voice + slop sweep: 15 recent blog posts (2026-08-01)

**Verdict:** The voice underneath is mostly yours. Damage concentrates in two places: (1) the June content-pipeline batch shipped assembled documents without a human read-through (internal memo and panel-prep notes live on the public site, mojibake, broken tables), and (2) the July 31 post has a 26-em-dash blowout plus the house tic both readers found independently, the decontracted "X is not A. It is B." redefinition-reveal. Eight of fifteen posts were mechanically clean; several of those are also voice-clean. Fix path for live posts is snapshot-first `wp-live-edit`. Originals untouched. Advisory only.

Scope: 15 live posts, 2026-06-18 through 2026-07-31. Audited against live `content.rendered` (see `snapshots/`). Tooling: `~/Code/kk-voice/scripts/voicecheck.py` + `crystal.md` facets + manual dodged-tell scan. Full per-post record: [`voice-alignment-report.md`](voice-alignment-report.md). Per-post deep notes: [`readings/`](readings/).

---

## P0 — NOT VOICE, ACT NOW

These are reader-visible assembly/encoding failures, not style nits. Do these first.

1. **Internal strategy memo live on the Canada post**
   - Post: [Canada Doesn't Need a Bigger AI Machine](https://kriskrug.co/2026/06/26/canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one/) (ID 12030)
   - Problem: essay ends; then a full internal memo ships ("Cohen White Paper Critique: BC+AI West Coast Alternative," alignment scores, "BC+AI Voice Profile and Worldview documentation," "KK Worldview," Notion/file artifacts). Confirmed in `snapshots/2026-06-26-…txt` at lines 174, 408, 420.
   - Fix: snapshot-first trim. Keep the essay. Unpublish everything from "Cohen White Paper Critique…" through the References block. Reading: `readings/2026-06-26-canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one.md`.

2. **Panel-prep notes live on What Would Chat Do**
   - Post: [What Would Chat Do?](https://kriskrug.co/2026/06/28/what-would-chat-do-and-why-thats-the-wrong-question/) (ID 12032)
   - Problem: after the bio, raw prep material ("KEY VIRAL QUOTES (From Panelist Call)," "? Use: Opening provocation," panel questions) plus run-together list items and corrupted arrows.
   - Fix: snapshot-first trim of the prep block. Optionally fold the orphaned "My relationship with AI is non-consensual…" fragment into the essay or cut it. Reading: `readings/2026-06-28-what-would-chat-do-and-why-thats-the-wrong-question.md`.

3. **Ethọ́s renders as `Eth??s` (reader-visible mojibake)**
   - Posts: [Ethos Lab Block Party](https://kriskrug.co/2026/06/23/ethos-lab-block-party/) (ID 12357, x7 in body/credits) and [Vancouver Made World Cup](https://kriskrug.co/2026/06/23/vancouver-made-world-cup/) (ID 12363, cross-link list).
   - Problem: stored content, not a pipeline artifact of our fetch. Corrupted form also dodges the checker's `Ethos Labs?` regex.
   - Fix: re-save correct UTF-8 "Ethọ́s" / "Ethọ́s Lab" via snapshot-first edit. Also fix block-party title to canonical Ethọ́s Lab (P1 below).

4. **God Skills: two markdown tables render as gibberish**
   - Post: [A Practical Guide to Agentic Workflows](https://kriskrug.co/2026/06/20/god-skills-agentic-loop-workflows/) (ID 12263)
   - Problem: pasted markdown tables show as run-together literal text; source of all 6 of its mechanical "em dash" flags (table separators, not prose).
   - Fix: rebuild as proper WP table/list blocks. Clears the mechanical flags without touching voice. Reading: `readings/2026-06-20-god-skills-agentic-loop-workflows.md`.

---

## P1 — HARD-RULE VOICE FIXES

1. **AI Lands: 26 prose em dashes (rank 1 offender)**
   - Post: [AI Lands Inside Every Profession](https://kriskrug.co/2026/07/31/ai-lands-inside-every-profession/) (ID 12653)
   - Fix: 23 verified edits ready in `readings/2026-07-31-ai-lands-inside-every-profession.md` (colon / period / comma / parentheses). Batch re-checked through `voicecheck.py`: 0 flags. While in there, thin reveal density to the two keep-instances named below (P2).

2. **Ethos Lab title → Ethọ́s Lab**
   - Post 12357 title uses non-canonical "Ethos Lab." Pair with the P0 encoding fix.

3. **Umlaut misses: "Kris Krug" without ü**
   - [What Would Chat Do?](https://kriskrug.co/2026/06/28/what-would-chat-do-and-why-thats-the-wrong-question/) bio block; [AI Media Appearances](https://kriskrug.co/2026/07/02/ai-media-appearances-podcast-guesting/) link text (L14). Checker has no rule for the umlaut-less form (see checker-gap candidates).

4. **Kharé / Khare inconsistency**
   - Same person spelled both ways on the media-appearances page. Pick one, fix the other.

---

## P2 — VOICE PROJECTS (bigger than a hotfix)

1. **Zero to One: rewrite, not polish**
   - Post: [Zero to One](https://kriskrug.co/2026/06/30/zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey/) (ID 12034)
   - Worst voice-alignment in the sweep: third-person case study about "Krüg," stale Nov-2025 vantage published June 2026 with future tense, internal date contradictions, 6 mechanical flags.
   - Work: person-shift to first person, tense/date pass, fix mechanical hits. Sample first-person rewrites already checker-verified in the reading.
   - Also reconcile membership numbers with the June 18 cert post: Zero-to-One says `$240/year` and `130 paid members`; cert post says `$340/year` and `99+ paying members`. Public site currently disagrees with itself.

2. **Reveal-density thinning (batch house tic)**
   - Decontracted "X is not (just) A. It is B." appears across the sweep; worst density in ai-lands (~8), god-skills (~12), what-would-chat-do (~10), artists-learn (textbook specimen at L38-40).
   - Keep-instances named by readers:
     - ai-lands: "That is not a venue rental. That is a city deciding…" and "Ecosystem is not a vibe. It is repeated contact with consequences."
     - what-would-chat-do: "AI isn't a tool. It's a mirror."
     - artists-learn: thin the literal "not just" specimen; keep manifesto ladders that earn payload.
   - Vary or cut the rest during the same edit sessions as P0/P1.

3. **What Would Chat Do: en-dash-as-em-dash cleanup**
   - Systematic U+2013 doing em-dash prose work. Restructure with colons/periods (verified rewrites in the reading). Pair with the P0 prep-notes trim.

---

## P3 — JUDGMENT CALLS / KEEPS

| Item | Call |
|---|---|
| Proximity-game "stakeholder alignment" | **Keep.** Quoted satirical committee-speak; hollowness is the joke. |
| Cheer-is-a-cap-table "buckle-up" | **Keep.** Hyphenated irony mocking the banned hype voice. Prior "ships clean" reconfirmed (drift 1.0000). |
| I Am Nomad closing line | **Fix (content accuracy).** Closing line inverts the film's premise (she gains time; close says she arrived with more than she left with). One-line verified fix in reading. |
| Futureproof / Future Proof / FUTURE PROOF | **Decide.** Glossary says FUTURE PROOF; Jul 28 says "Future Proof"; Jul 31 says "Futureproof." Pick official festival rendering, then align posts + glossary. |
| Soft `team` hits (4 across sweep) | **Keep** as idiomatic/quoted/other-org (team sport, pick a team, Team BC, Tyler's team). Prefer-vocab note only. |

---

## CHECKER-GAP CANDIDATES

Proposal only. Do not edit `~/Code/kk-voice/anti-glossary.md` in this pass. Concrete candidates from the 15 readings:

1. **Decontracted redefinition-reveal (soft flag)** — highest priority gap. Specimens in ai-lands, artists-learn (cleanest live hit), god-skills, what-would-chat-do, no-one-knows.
   - Candidate: `\b(is|are|was) not (just|only|simply) [^.]{3,80}\. (It|That|They|These) (is|are)\b`
   - Soft because his exemplar cadence ("A portrait is not an image of a face…") matches; flag density, not each instance.

2. **One intervening word defeats "it's not just"** — canada specimen: "It's also not just quantity. It's format:"
   - Candidate: `it'?s (\w+ )?not (just|only) `

3. **Corrupted Ethọ́s / mojibake** — `Eth\?\?s` and a general in-word `\?\?` heuristic. Primary: block-party; secondary: world-cup cross-link.

4. **Umlaut-less "Kris Krug"** — `Kris Krug\b` → "WRONG, canonical is Kris Krüg". Word boundary keeps `kriskrug.co` and MOTLEYKRUG safe.

5. **Inflected banned stems** — `empower(s|ed|ing)?`, `foster(s|ed|ing)?` (zero-to-one). Soft `teams?` if crew-not-team stays soft.

6. **En-dash-in-prose heuristic** — U+2013 doing aside/reveal work outside date/number ranges (what-would-chat-do). Harder to regex cleanly; start as a lint note.

7. **Third-person self-reference on this site** — soft: `(As )?Krüg (stated|said|notes|explains)`. Usually means a pipeline wrote it (zero-to-one).

8. **Source-manager residue** — `\bPDF-[A-Za-z]`, long hex Notion IDs, "Voice Profile" / "KK Worldview" in public post body (canada memo). Structural lint, not voice.

9. **Hyphenated compounds dodge space-anchored bans** — `buckle-up` vs `buckle up`. Low urgency; live specimen was intentional irony keep.

10. **Markdown table syntax in rendered WP HTML** — `\|\s*[-—:]+\s*\|` catches the god-skills bug as a structural lint.

---

## CLEAN BILL

Posts that passed voice (or near-passed) so the good work is visible:

| Post | Notes |
|---|---|
| [AI Won't Fix Your Broken Permit Process](https://kriskrug.co/2026/06/24/ai-wont-fix-your-broken-permit-process/) | Strongest long-form June voice. Negative control for earned contrast. |
| [Vancouver Made World Cup](https://kriskrug.co/2026/06/23/vancouver-made-world-cup/) | Exemplar-grade Anti-Hero. Only issue: Eth??s in cross-link (P0). |
| [Ethos Lab Block Party](https://kriskrug.co/2026/06/23/ethos-lab-block-party/) | Best Host writing in the batch. Encoding + title only (P0/P1). |
| [The Great Canadian Proximity Game](https://kriskrug.co/2026/06/22/the-great-canadian-proximity-game/) | Clean Anti-Hero. Satire keep confirmed. |
| [Watch Who's Smiling](https://kriskrug.co/2026/07/10/the-cheer-is-a-cap-table/) | Prior "ships clean" reconfirmed. Drift 1.0000. |
| [No One Knows What to Call Us Yet](https://kriskrug.co/2026/07/28/no-one-knows-what-to-call-us-yet/) | Clean Builder+Host. Reveal density watch only. |
| [I AM NOMAD](https://kriskrug.co/2026/07/18/i-am-nomad-ai-film/) | Best July voice. One content-logic close fix (P3). |
| [Artists Learn. Machines Extract.](https://kriskrug.co/2026/07/06/artists-learn-machines-extract/) | Near-clean manifesto. One de-template judgment fix. |
| [Why We Built the RAIP Certification](https://kriskrug.co/2026/06/18/why-we-built-the-responsible-ai-professional-certification/) | Clean-ish ED. Membership numbers conflict with zero-to-one (P2). |
| [AI Media Appearances](https://kriskrug.co/2026/07/02/ai-media-appearances-podcast-guesting/) | Low severity: umlaut + Kharé spelling (P1). |

---

## Tally

| Bucket | Count | Posts |
|---|---|---|
| Clean / near-clean | 10 | permit, world-cup, block-party, proximity, cheer, no-one-knows, i-am-nomad, artists-learn, cert, ai-media |
| Flagged minor | 1 | god-skills (structural tables + reveal density) |
| Flagged major | 4 | ai-lands (em dashes), canada (memo leak), what-would-chat-do (prep leak + en dashes), zero-to-one (third-person rewrite) |

Mechanical pass: **44 flags / 15 posts / 8 mechanically clean**. Dominant type: em dash (32 of 44; 26 prose in ai-lands + 6 table syntax in god-skills).

---

## Footer

- Originals and live posts untouched. This audit is advisory.
- Live fix path: `wp-live-edit` skill, snapshot-first, slug/ID checks, KK approval for risky trims (especially the memo leak: confirm before cutting).
- Skill doc path is stale: `voice-slop-audit/SKILL.md` still points at `~/Code/dark-crystal/kk-voice/`; actual tooling is `~/Code/kk-voice/`. Update when convenient.
- Report generated 2026-08-01. Ground truth: `snapshots/` fetched that day via REST.
