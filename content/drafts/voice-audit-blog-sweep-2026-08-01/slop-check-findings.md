# Mechanical slop check — 15-post blog sweep (fetched 2026-08-01)

Tool: `~/Code/kk-voice/scripts/voicecheck.py --json` run against the 15 stripped
snapshots in `snapshots/` (live `content.rendered`, fetched read-only via WP REST —
see `fetch_snapshots.py` and `manifest.json`). Raw output: `slop-check-raw.json`.

**Total: 44 flags across 15 posts. 8 posts fully clean.** Line references (`L__`)
point into the corresponding `snapshots/<date>-<slug>.txt` file. Word counts are
body words (title/link header lines excluded). Scope: mechanical hits only —
facet routing, manual dodged-tell scan, and deep reads are later phases.

## Ranking — worst first by flag density

| Rank | Post slug | Date | Words | Flags | /1000w | Top flag types |
|---|---|---|---|---|---|---|
| 1 | ai-lands-inside-every-profession | 2026-07-31 | 2,247 | 27 | 12.0 | em dash x26, team x1 |
| 2 | god-skills-agentic-loop-workflows | 2026-06-20 | 2,170 | 6 | 2.8 | em dash x6 (all table syntax in two broken markdown tables) |
| 3 | zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey | 2026-06-30 | 3,668 | 6 | 1.6 | team x2, seamless x1, cutting-edge x1, pivotal x1, "no X, no Y, just Z" x1 |
| 4 | the-great-canadian-proximity-game | 2026-06-22 | 883 | 1 | 1.1 | stakeholder alignment x1 (satirical dialogue) |
| 5 | ethos-lab-block-party | 2026-06-23 | 976 | 1 | 1.0 | "Ethos Lab" wrong canonical spelling x1 (post title) |
| 6 | what-would-chat-do-and-why-thats-the-wrong-question | 2026-06-28 | 1,401 | 1 | 0.7 | team x1 (idiomatic) |
| 7 | canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one | 2026-06-26 | 3,952 | 2 | 0.5 | stakeholders x1, thought leadership x1 |
| 8 | no-one-knows-what-to-call-us-yet | 2026-07-28 | 2,377 | 0 | 0.0 | — (clean) |
| 9 | i-am-nomad-ai-film | 2026-07-18 | 2,297 | 0 | 0.0 | — (clean) |
| 10 | the-cheer-is-a-cap-table | 2026-07-10 | 1,520 | 0 | 0.0 | — (clean) |
| 11 | artists-learn-machines-extract | 2026-07-06 | 1,155 | 0 | 0.0 | — (clean) |
| 12 | ai-media-appearances-podcast-guesting | 2026-07-02 | 1,197 | 0 | 0.0 | — (clean) |
| 13 | ai-wont-fix-your-broken-permit-process | 2026-06-24 | 1,963 | 0 | 0.0 | — (clean) |
| 14 | vancouver-made-world-cup | 2026-06-23 | 789 | 0 | 0.0 | — (clean) |
| 15 | why-we-built-the-responsible-ai-professional-certification | 2026-06-18 | 1,131 | 0 | 0.0 | — (clean) |

Flag-type totals across the sweep: em dash x32 (26 prose + 6 table-syntax),
`\bteam\b` x4 (all soft/idiomatic — see per-post notes), and one each of:
stakeholder alignment, stakeholders, thought leadership, seamless, cutting-edge,
pivotal, "no X, no Y, just Z" cadence, "Ethos Lab" canonical-spelling.

---

## 1. ai-lands-inside-every-profession (2026-07-31, post 12653) — 27 flags

26 em dashes (hard rule: never; fix with a comma, colon, or two sentences) plus
one soft `team` hit. This is the post that triggered the sweep. Em dashes below
in reading order; several are pairs wrapping an aside (fix as one edit).

1. **L18** "Here is the rest of the story — the part that does not fit in a news brief."
   → Colon: "…the rest of the story: the part that does not fit in a news brief."
2. **L28** "…making the case … since the very first weeks of this project — the entry-level jobs that built those talent pipelines are exactly what AI is dissolving first…"
   → Period + new sentence: "…since the very first weeks of this project. The entry-level jobs…"
3. **L36 (pair, cols 166+225)** "I had spent a year deep in the machine — testing tools, talking to labs, watching the ground move — and the conclusion kept getting louder: …"
   → Comma + period split: "…deep in the machine, testing tools, talking to labs, watching the ground move. And the conclusion kept getting louder: …"
4. **L44 (bullet)** "11 community subgroups — an AI Film Club run by Kevin Friel…"
   → Colon: "11 community subgroups: an AI Film Club…"
5. **L46 (bullet)** "weekly programming, not just a monthly flagship — the events calendar does not take weeks off"
   → Period: "…not just a monthly flagship. The events calendar does not take weeks off."
6. **L54 (bullet)** "Futureproof Festival, October 28–30, 2026, at the Space Centre — the long-dreamed homegrown annual gathering…"
   → Period (sentence is already comma-heavy): "…at the Space Centre. The long-dreamed homegrown annual gathering…"
7. **L60** "That is not a romance about grit — it is a design choice."
   → Period: "That is not a romance about grit. It is a design choice." (Also a
   "not X — it is Y" redefinition-reveal shape; splitting it defuses both.)
8. **L62 (caption)** "Vancouver AI Turns One — the room, one year in."
   → Colon: "Vancouver AI Turns One: the room, one year in."
9. **L64 (caption)** "Futureproof Festival — October 28–30, 2026 · Space Centre."
   → Colon: "Futureproof Festival: October 28–30, 2026 · Space Centre."
10. **L70** "…started feeling like civic infrastructure — a room people can come back to…"
    → Colon: "…started feeling like civic infrastructure: a room people can come back to…"
11. **L72 (caption)** "AI Ethical Futures Lab at Parker Street Studios, July 2026 — the room got real."
    → Period: "…July 2026. The room got real."
12. **L74 (pair, cols 165+209)** "…he calls this the orchestration era — not one model, but a pipeline you conduct — and gives away every shortcut he knows…"
    → Colon + period split: "…he calls this the orchestration era: not one model, but a pipeline you conduct. And he gives away every shortcut he knows…"
13. **L74 (col 417)** "…a thirty-second commercial he had made for about a hundred dollars — work that would have carried a six-figure budget at his old studio."
    → Period: "…for about a hundred dollars. Work that would have carried a six-figure budget at his old studio."
14. **L76** "About sixty-five showed up — farmers, teachers, local government folks, software people, artists, retirees."
    → Colon: "About sixty-five showed up: farmers, teachers…"
15. **L78 (caption)** "Comox Valley AI in Courtenay — becoming its own thing."
    → Colon: "Comox Valley AI in Courtenay: becoming its own thing."
16. **L82** "…trustworthy enough for patient outcomes — for the responsibility that used to live entirely in the hands of doctors?"
    → Comma: "…trustworthy enough for patient outcomes, for the responsibility that…"
17. **L84** "That is why we built the Responsible AI Professional certification — because in every room, hands go up for deployment and down for governance…"
    → Colon (drop "because"): "…certification: in every room, hands go up for deployment and down for governance…"
18. **L86 (pair, cols 99+201)** "AI amplifies whatever process it lands in — I watched this play out in city halls and wrote about it in AI Won't Fix Your Broken Permit Process — and 'ask the chatbot' is not a governance plan."
    → Parentheses around the aside (it's a link reference): "AI amplifies whatever process it lands in (I watched this play out in city halls and wrote about it in AI Won't Fix Your Broken Permit Process), and 'ask the chatbot' is not a governance plan."
19. **L97** "…published the result with me as a peer-reviewed case study in BC Studies — 'Building a Grass Roots AI Community of Practice' (No. 224, April 2025)."
    → Colon: "…case study in BC Studies: 'Building a Grass Roots AI Community of Practice'…"
20. **L115** "…645 British Columbians answered — a fifth of every response in the country, second only to Ontario."
    → Colon: "…645 British Columbians answered: a fifth of every response in the country…"
21. **L117** "…hydropower data centres as a counterpoint to extractive defaults — if communities help write the terms instead of rubber-stamping blank cheques…"
    → Comma: "…as a counterpoint to extractive defaults, if communities help write the terms…"
22. **L123** "Then she did the thing good journalists do — she put an industry association, a grassroots community, and an ethics-and-measurement foundation on the same page…"
    → Colon: "Then she did the thing good journalists do: she put an industry association…"
23. **L127** "Advocacy work, recurring community, ethics and measurement, research pipelines, capital — a healthy region needs all of those layers…"
    → Flip the sentence so the list follows a colon: "A healthy region needs all of those layers: advocacy work, recurring community, ethics and measurement, research pipelines, capital."

- **L86 `team`** "Professions adopting AI need judgment, and judgment is a team sport."
  Rule: soft flag ("Kris says crew, not team — judge by context"). "Team sport"
  is an idiomatic set phrase, not a reference to his own crew. Suggested call:
  keep; if strictness wins, "judgment is a group sport" (weaker — keeping it is defensible).

## 2. god-skills-agentic-loop-workflows (2026-06-20, post 12263) — 6 flags

All 6 em dashes are **table syntax, not prose**: two markdown tables were pasted
into plain WP paragraph blocks and render as literal run-together text on the
live page (pipes and all), with the markdown `---` separator rows autocorrected
to em dashes.

- **L76 (x4)** "| Skill | Codename | Use it when | Output | |—|—|—|—| | skill-registry | Saraswati | …"
  (the Ten Canonical Skills table)
- **L122 (x2)** "| If the request sounds like… | Start with… | |—|—|— | 'What skills do we have?' | skill-registry | …"
  (the routing table)

→ Fix (one structural edit, clears all 6): rebuild both as real WP table blocks
(or styled lists). This is a live formatting bug over and above the em dashes —
readers currently see raw pipe/markdown gibberish where the tables should be.
Punctuation-level fixes don't apply here.

## 3. zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey (2026-06-30, post 12034) — 6 flags

1. **L10 — pattern "no X, no Y, just Z"** "…From seasoned researchers to budding artists, from tech enthusiasts to curious students.' No pitches, no pyramid schemes, just genuine peer-to-peer learning."
   The flagged sentence sits just outside the quoted event description. If it is
   part of the original 2024 listing, pull it inside the quotation marks and
   attribute it; if it's post prose, rephrase off the template: "Nobody pitched.
   Nobody recruited. People taught each other."
2. **L50 `team`** "Tyler and his team saw Surrey AI as essential infrastructure…"
   Soft flag; refers to someone else's company team, where "crew" would
   misdescribe. Suggested call: keep.
3. **L118 `seamless`** "The nonprofit formation wasn't seamless."
   Banned marketing filler even when negated. → "The nonprofit formation wasn't smooth."
4. **L136 `cutting-edge`** "These partnerships ensured BC + AI remained connected to cutting-edge research while maintaining its community-first approach."
   → "…remained connected to the research frontier…" (or name the labs/programs).
5. **L162 `pivotal`** "Certain moments proved pivotal in BC + AI's evolution:"
   → "Certain moments changed BC + AI's trajectory:" (or plain "mattered most").
6. **L190 `Team`** "…Web Summit Vancouver offers opportunity for BC + AI to be 'Team BC home base'…"
   Soft flag; quoted brand phrase ("Team BC"). Suggested call: keep as quoted.

## 4. the-great-canadian-proximity-game (2026-06-22, post 12190) — 1 flag

- **L12 `stakeholder alignment`** "'Let's collaborate. Strategically.' A table of beaming directors. 'Your impact is transformational.' 'Your stakeholder alignment is visionary.' The Federal Funding Machine roaring to life…"
  Rule reason: committee theater. Here it is **deliberately quoted committee
  theater** — satirical dialogue inside the Federal Funding Machine tableau; the
  phrase being hollow is the joke. Suggested call: keep (intentional irony).
  Mechanical hit recorded; checker can't see context.

## 5. ethos-lab-block-party (2026-06-23, post 12357) — 1 flag

- **L1 (post title) pattern `Ethos Labs?\b`** "The Ethos Lab Block Party Album"
  Canonical spelling is **Ethọ́s Lab**. → Fix the live post title (and slug is
  fine; slug staying ASCII is normal).
- **Related, not checker-visible:** the post body's diacritics are corrupted on
  the live site — "Ethọ́s" renders as literal "Eth??s" (two ASCII question
  marks) in body text, the "ETH??S·FM" player mention, and the credits line.
  Verified in both the REST payload and the live rendered page, so readers see
  it. The same corruption appears in the vancouver-made-world-cup post's
  cross-link list ("The Eth??s Lab Block Party album"). Because the corrupted
  variant no longer matches `Ethos Labs?\b`, it also dodges the canonical-
  spelling check — worth a checker-gap note in the later summary phase.
  → Fix: restore the proper "Ethọ́s" characters in the stored post content
  (encoding got mangled at publish time), then re-verify the live page.

## 6. what-would-chat-do-and-why-thats-the-wrong-question (2026-06-28, post 12032) — 1 flag

- **L30 `team`** "AI discourse wants you to pick a team: techno-optimist or doomer."
  Soft flag; "pick a team" is idiomatic (picking sides), not Kris's own crew.
  Suggested call: keep. ("Pick a side" works if strictness wins.)

## 7. canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one (2026-06-26, post 12030) — 2 flags

1. **L38 `stakeholders`** "He also correctly calls for coordination across stakeholders and faster commercialization mechanics."
   → Name them: "coordination across governments, industry, and researchers…"
   (or "across the people involved").
2. **L336 `thought leadership`** "Montreal: Deep learning heritage + Responsible AI thought leadership + French ecosystem positioning"
   → Name the actual work: "Responsible AI research leadership" or "Mila-anchored
   responsible-AI research + French ecosystem positioning".

## 8–15. Fully clean posts (0 mechanical flags)

Explicitly confirmed clean by the checker — no banned words, no em dashes, no
flagged patterns:

- no-one-knows-what-to-call-us-yet (2026-07-28, post 12638)
- i-am-nomad-ai-film (2026-07-18, post 12612)
- the-cheer-is-a-cap-table (2026-07-10, post 12479) — also drift-checked against
  its pre-publish audited draft, see `drift-check-the-cheer-is-a-cap-table.md`
- artists-learn-machines-extract (2026-07-06, post 12473)
- ai-media-appearances-podcast-guesting (2026-07-02, post 11879)
- ai-wont-fix-your-broken-permit-process (2026-06-24, post 12035)
- vancouver-made-world-cup (2026-06-23, post 12363) — clean mechanically, but
  carries the Eth??s encoding corruption in its cross-link list (see §5)
- why-we-built-the-responsible-ai-professional-certification (2026-06-18, post 12257)

Mechanically clean ≠ voice-clean: the manual dodged-tell scan and facet reads
happen in the next phase.

## Observations for later phases (recorded, not acted on)

- The `Title:`/`Link:` header lines in each snapshot .txt are audit metadata;
  the only flag that landed on one (Eth**o**s Lab, §5) is on the real rendered
  post title, so it stands. No flags landed on `Link:` lines.
- En dashes (–) appear in several posts (e.g. what-would-chat-do's "compare
  outputs – where do they differ?") and are not in the anti-glossary; whether
  they're em-dashes-in-disguise is a judgment call for the manual pass.
- what-would-chat-do has a live formatting bug unrelated to voice: list items
  run together with no separator ("…ChatGPT, Claude, and GeminiCompare outputs…",
  "Why?Synthesize yourself…") in the rendered HTML itself.
- All four `team` hits in the sweep are idiomatic/quoted/other-org uses — the
  soft flag behaved as designed; none look like real voice violations.
