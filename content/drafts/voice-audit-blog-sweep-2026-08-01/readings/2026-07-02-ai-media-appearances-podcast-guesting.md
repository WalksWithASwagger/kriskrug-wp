# AI Media Appearances, Podcast Guesting, and Broadcast Commentary

**Facet:** The ED (dominant — a booking shop window, proof-stack structure) + The Host (warmth and weird-edge texture) | **Mechanical flags:** 0 | **Depth:** deep read (escalated: two textbook not-just dodges plus genre-heavy list density)

## Verdict

The most institutional page of the six, and it mostly survives its genre: the receipts do the selling instead of brochure adjectives, credit is unusually dense for a sales page, and the both/and markers keep it off corporate register ("without pretending the weird parts are not weird," "without pretending the risks are fake"). It sounds like Kris running his own shop window rather than a copywriter running it for him. Three real dings: one canonical-spelling miss the checker cannot see (Kris Krug without the umlaut), two decontracted "not just X. It is Y." template sentences, and a collaborator's name spelled two ways on the same page.

Five-question pass by section: all sections pass Q1/Q2/Q3 (every claim carries a named show, outlet, or person); Q4 catches the umlaut miss; Q5 is the one to watch in a page like this, and it holds — the edge markers are present in every major section.

## What's working

- "making machine intelligence understandable, practical, creative, and culturally literate for real people without pretending the weird parts are not weird" — the mission sentence stays his.
- "Not safe as in sanitized. Safe as in honest, curious, critical, and useful…" — definitional correction that adds content instead of performing a reveal.
- "eighty minutes of creative practice, AI, authorship, consent, community, and the both hands full frame without the safe little résumé parade" — "the safe little résumé parade" is exactly the self-aware edge that keeps a booking page from going brochure.
- "The through-line is still the same: make AI usable without pretending the risks are fake."
- "Two rooms, two different versions of the same question: who gets power, and what do we do with it?"
- "the weird cultural edge where the future first becomes visible"
- "This did not start with the current AI cycle." — followed by receipts back to 2008 (Leo Laporte, the 2010 Olympics citizen-media work). Depth as proof, not claimed authority.
- Credit density for a sales page: Michael Running Wolf, Jovian Radheshwar, Stephen Quinn, Jordan Dack, Sharad Kharé, Nessa Palmer, Rob Anthony, Justin Ruckman, Leo Laporte, Rachel Thexton, Stewart Muir, Pennefather and Gaertner.
- "It is useful producer proof because it shows I can bring the same ideas into a compact, high-production format without turning generic." — self-aware about the exact failure mode this page risks.

## Flagged

### HARD RULE

- **Canonical spelling (by eye — no regex exists for it):** L14 "CBC Radio Early Edition's AI Sandbox with Kris Krug" → "…with Kris Krüg". Glossary: "Kris Krüg — the umlaut is not optional." Even if CBC's own CMS renders the segment title without the umlaut, this is link text on his own site and it is his name. (MOTLEYKRUG as an all-caps handle and the kriskrug.co domain are normal ASCII exceptions.) Verified replacement: "The clearest mainstream proof point is CBC Radio Early Edition's AI Sandbox with Kris Krüg."

### JUDGMENT CALL

- **Decontracted not-just template, instance 1:** L18 "Responsible AI is not just a software question. It is a culture, governance, rights, and community question." → why: the exact banned cadence minus the contraction — the checker's confirmed blind spot. → verified fix: "Responsible AI is a culture, governance, rights, and community question, not a software question alone."
- **Decontracted not-just template, instance 2:** L96 "These are not just content feeds. They are archives of a community learning in public: …" → why: same pattern, and here the setup adds nothing — the colon list does all the work. → verified fix (cut the setup): "These are archives of a community learning in public: meetups, experiments, interviews, creative technology, AI ethics, Indigenous tech futurism, and the weird cultural edge where the future first becomes visible."
- **Name consistency:** "Sharad Kharé" (L62) vs "Sharad Khare" (L82) on the same page. Confirm his own preferred rendering (the accented Kharé appears to be his branding), then make both match.
- **Filler intensifier:** "That thread matters a lot." (L18) — the next sentence already says why it matters; cut it and the paragraph gets stronger.
- **Repetition:** "stubbornly human" twice (L58 "the stubbornly human parts of living through an AI shift," L62 "the stubbornly human value of curiosity"). Fine once, a tic twice on one page. Keep the L62 instance; verified variation for L58: "the human parts of living through an AI shift".

## Dodged tells found

- The two decontracted not-just reveals above, plus one borderline comparative ("a good podcast guest does more than deliver talking points. They bring stories, tensions, examples…" — comparative rather than negation, and the list is substantive; keep).
- **List density is high but genre-driven:** the 8-item formats chain (L6) and the 9-item topics chain (L122) are the page doing its actual job (enumerating offerings for bookers); the 9-item one would scan easier as bullets, like the formats list already is. Named either way per the skill.
- **Uniform-positivity check (the genre's biggest risk):** examined hard, and it holds — no banned brochure vocabulary anywhere (checker agrees), every superlative-shaped claim is a receipt ("the clearest mainstream proof point" introduces a named CBC segment, not an adjective pile), and the critical register survives ("critical," "the risks," "the weird parts").
- Explicitly **not** found: "landscape" filler, "in an increasingly" openers, throat-clearing, copula avoidance (plain "is" throughout), bold-header list padding, manufactured vulnerability, conclusion-that-restates (the close is CTA plumbing, correct for the genre), en dashes doing em-dash work, negative-open-forced-upbeat-close.

## Checker-gap candidates

1. **`Kris Krug\b` (umlaut-less, space-separated) has no anti-glossary regex** — this page carried a live instance through a clean checker run. Proposal for `anti-glossary.md` regex section: `Kris Krug\b` → "WRONG, canonical is Kris Krüg". Word boundary keeps kriskrug.co (no space) and MOTLEYKRUG safe; "Krüg" itself cannot match (ü is not u); the checker's case-insensitivity also catches a lowercase "kris krug".
2. **Decontracted not-just reveal** — this page supplies two textbook specimens for the batch-wide soft-flag regex proposed in the ai-lands reading.
