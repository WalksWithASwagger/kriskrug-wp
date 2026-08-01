# Canada Doesn't Need a Bigger AI Machine. It Needs a Better One.

**Facet:** The ED with Anti-Hero spice (policy response with edge) — for the first half; the second half is an internal strategy memo in no public facet | **Mechanical flags:** 2 | **Depth:** deep read (escalated — 3+ structural tells found)

## Verdict (2-4 sentences)

This is two documents published as one. The essay (from "Rainy Vancouver night" through "That's the West Coast contribution... it's just a faster leak") is strong ED-with-edge: fair to Cohen, receipt-dense, and voiced ("Not vibes-trouble. Measurable-trouble.", "we should steal shamelessly"). Then a full internal strategy memo follows — "Executive Summary," alignment scores ("8/10 alignment"), "Section 1-6," and a References block citing internal documents ("BC+AI Voice Profile and Worldview documentation," "KK Worldview") plus raw file/Notion artifacts ("PDF-FinalReport-AISymposium", "BC AI JEDI Report 16cc6f799a338…") — none of it written for readers. The essay should stand alone; the memo should be unpublished from the page.

## What's working (quoted specifics)

- The cold open is him: "Rainy Vancouver night. Somebody's laptop is open. Somebody else is asking the kind of question that makes a room go quiet: Who owns the data in an AI future?"
- Fairness-first both/and, exactly the ED move: "He's not wrong." and "So yeah. Diagnosis is solid." before the critique; "We don't dunk on it. We remix it into something Canada can own."
- Receipts throughout: 0.7% global compute share, 12.2% enterprise adoption, 46% compensation premium, "three-quarters of British Columbians do not trust tech companies," 74% want regulation — all attributed (Cohen, SFU Wosk Centre, BC Studies).
- "trust is the limiting reagent" — chemistry metaphor with actual content; "compute just scales conflict"; "a 'move fast and break things' import with a Canadian flag sticker slapped on top."
- The close has real edge and adds: "scale, yes. But stewarded. Or it's not progress, it's just a faster leak."
- The synthesis riff earns its parallel structure: "Cohen says Canada needs scale. I'm saying: fine, but only with stewardship." (x3, each with different content).

## Flagged (each: quoted passage -> why -> suggested fix)

### HARD RULE

1. "He also correctly calls for coordination across stakeholders and faster commercialization mechanics." -> banned `stakeholders` (bureaucratic; it's Kris's paraphrase, not a Cohen quote) -> "He also correctly calls for coordination across governments, industry, and researchers, plus faster commercialization mechanics." *(checker-verified)*
2. "Montreal: Deep learning heritage + Responsible AI thought leadership + French ecosystem positioning" (in the memo half) -> banned `thought leadership`; name the work -> "Montreal: deep learning heritage, Mila-anchored responsible-AI research, French ecosystem positioning." *(checker-verified)*

### NOT-VOICE but reader-visible (structural — the real story of this post)

3. **Internal memo published verbatim after the essay** — everything from "Cohen White Paper Critique: BC+AI West Coast Alternative / Subject: Strategic Analysis..." to the References block -> not written for readers: alignment scores ("Brain Drain Crisis (8/10 alignment)"), consultant scaffolding ("The Integration:", "Effect:", "Gap:", "What Cohen Misses:" repeated as bold-header inline list padding), fragment cadence ("Not charity. Strategic difference." / "Neither alone sufficient. Together, powerful."), and repeated stats ("212% growth" three times) -> unpublish the memo half; anything worth keeping is already in the essay.
4. **Internal document names leaked into public References:** "BC+AI Voice Profile and Worldview documentation; core principle of non-extractive economics," "BC+AI Worldview document, 'Insider/Outsider Positioning' section," "KK Worldview: 'AI as Mirror, Not Tool'" -> internal corpus/strategy docs cited on a public page; also quotes the voice profile in body text ("The voice profile captures this: 'Insider/outsider is where I operate best.'") -> remove with the memo (hygiene, not just voice).
5. **Raw citation artifacts in body text:** "OCAP/UNDRIP-aligned data governance pathways for sensitive datasets. PDF-FinalReport-AISymposiumLow-carbon infrastructure requirements..." (a filename mashed mid-sentence), "will require 'trust re-building' efforts. Public_Opinion_Research-British…" (truncated filename), "BC AI JEDI Report 16cc6f799a338…" (Notion page-ID fragment) -> source-manager artifacts pasted through to the live page -> delete the fragments; link the actual sources.
6. **Duplicated section:** "1) Publish the feature: 'We Agree on the Diagnosis. Our Cure Is Different.' / This long-form piece..." appears twice — once orphaned under "The part Cohen nails" (where it doesn't belong), once in its proper place under "The plan" -> delete the first occurrence.
7. Run-together list items (same rendering bug class as what-would-chat-do): "U.S. dominates frontier models (GPT, Claude ) but faces recurring AI ethics crisesEU leads on regulation..." and "Assumes 'raising Canadian GDP' benefits allTreats AI as neutral productivity tool..." -> rebuild as proper list blocks.

### JUDGMENT CALL

8. "we don't just lack compute. We lack consent architecture." -> reworded redefinition-reveal — but it's the thesis of the piece and "consent architecture" is a real coinage -> keep. Named for the record.
9. "It's also not just quantity. It's format:" -> the literal banned cadence with "also" wedged in, which is what dodged the regex -> "The format matters as much as the head count: open mic, demos, rapid iteration..." or simply drop "It's also not just quantity."
10. Essay-half redefinition density is moderate ("And trust is not a PR issue. It's an adoption ceiling." / "That's not a meetup anecdote. That's an adoption mechanism." / "That's not a vibe. That's the blueprint...") -> each carries content; keep the strongest, but if the batch-wide pattern is being thinned, "That's not a vibe. That's the blueprint" is the most cuttable.

## Dodged tells found

- "It's also not just quantity. It's format:" — the banned cadence dodging via one inserted word (Flagged #9).
- Uncontracted redefinition-reveals at moderate density in the essay, very high density in the memo ("Positioning: Not critique. Integration." / "Not charity. Strategic difference.").
- Bold-header inline list padding throughout the memo ("The Integration:", "Effect:", "Gap:") — textbook instance of the pattern.
- Score-theater ("8/10 alignment," "9/10 disagreement") — quantification that encodes no method; an AI-memo tell.
- Conclusion of the memo restates its own executive summary ("necessary but insufficient" appears in both).
- No landscape filler; no "increasingly" openers; essay half's positivity is properly uneven (real friction with Cohen).

## Checker-gap candidates

- **"It's also not just X. It's Y."** — one inserted word defeats `it'?s not just .+,? it'?s`. Candidate: `it'?s (\w+ )?not (just|only) ` to allow one intervening word.
- **Filename/ID artifacts in rendered content:** candidate regexes for `\bPDF-[A-Za-z]`, `\w_Research-\w`, and 12+ char hex fragments (`\b[0-9a-f]{12,}\b`) as a "source-manager residue" structural lint — this exact residue class appears twice in the June batch (here and the corrupted arrows/diacritics elsewhere).
- **Internal-doc leakage:** soft flag for "Voice Profile," "Worldview document," "KK Worldview" appearing in public post content — names of internal corpus files should never render on the live site.
