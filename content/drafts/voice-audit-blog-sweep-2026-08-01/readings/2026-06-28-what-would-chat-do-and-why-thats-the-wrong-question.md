# What Would Chat Do? And Why That's the Wrong Question

**Facet:** The Host, strong Anti-Hero blend (mirror/manifesto register, panel-keynote soul) | **Mechanical flags:** 1 (idiomatic `team`, keep) | **Depth:** deep read (escalated — 3+ structural tells found)

## Verdict (2-4 sentences)

The essay itself is one of the most Kris-sounding pieces in the June batch — "Last night I was vibe coding in the bathtub," "I refuse," both-hands-full held all the way through, credit given by name. But the published page is an assembly accident: after the sign-off bio, raw panel-prep material ("KEY VIRAL QUOTES (From Panelist Call)," "THEME 2: SPEED VS. CRITICAL THINKING," "? Use: Opening provocation") runs for another ~60 lines, complete with corrupted arrow characters and run-together list items. And the prose systematically uses en dashes to do em-dash work, which reads as the banned punctuation with a haircut. Fix the structure and the dashes and this is a keeper.

## What's working (quoted specifics)

- The opener is pure him: "Who is steering: you, your values, or the algorithm wearing your face back at you?" and "Last night I was vibe coding in the bathtub (yes, that's a real thing)."
- Both/and straight from the core: "I'm stoked about the opportunities AND I have real concerns. I walk forward with both in my hands at the same time."
- Credit distributed by name, exactly as the crystal demands: "I teach what I call the CASK Framework (credit to filmmaker Liz Marshall for the original concept)," "Sonali's Multi-Tool Method," Carol Ann Hilton "with real voting power, not a diversity checkbox," Gabriel George, Peter Lucas Jones.
- Receipts: "My 130,000 Creative Commons images? Training data." / "25+ events, 100% consistency" / zip-code proxy variables in financial systems.
- "bias laundering — discrimination that looks like math" is a genuinely great coinage (once the dash is fixed), and "Skepticism — Not cynicism, but 'show me the receipts'" is glossary vocabulary used right.
- Edge intact: Fernanda's quoted "Are you fucking kidding me?" is left unsanitized, which is correct per the register notes.

## Flagged (each: quoted passage -> why -> suggested fix)

### HARD RULE

1. "AI discourse wants you to pick a team: techno-optimist or doomer." -> soft `team` flag; idiomatic (picking sides), not his crew -> keep (confirming Phase 1). "Pick a side" if strictness wins.
2. "Kris Krug is a National Geographic photographer turned AI educator..." (bio block) -> **canonical spelling: the umlaut is not optional** -> "Kris Krüg is a National Geographic photographer turned AI educator." *(checker-verified)* Note the checker has no rule for the umlaut-less form — see checker gaps.

### JUDGMENT CALL

3. **En dashes doing em-dash prose work, systematically:** "It shows you who you've been – your patterns, your biases, your blind spots – and amplifies them at planetary scale." / "That's what I call bias laundering – discrimination that looks like math." / "Curiosity – Wonder and fascination." / "More importantly – who is MISSING?" / "ceremony – 25+ events, 100% consistency" -> the em dash is a hard-never; swapping in U+2013 keeps the identical cadence while dodging the rule -> restructure with colons/periods. Checker-verified rewrites: "It shows you who you've been: your patterns, your biases, your blind spots. Then it amplifies them at planetary scale." / "That's what I call bias laundering: discrimination that looks like math." / "Curiosity: wonder and fascination. Don't lose it." / "Gabriel George (Tsleil-Waututh Nation Elder) opens every event with ceremony: 25+ events, foundational not performative."
4. Redefinition-reveal density (~10 in 1,400 words): "AI isn't a tool. It's a mirror." / "This isn't contradiction. It's reality." / "These aren't technical questions. They're values questions." / "That's not personal branding. That's cultural transmission as technical responsibility." / "That's not inspiration. That's operational." / "That's not a hot take. That's just reality." -> the mirror line is the thesis and earns its shape; the accumulation is formula. Keep 2-3 strongest ("AI isn't a tool. It's a mirror." stays), rewrite or cut the rest — most can simply drop the negation half.
5. Hollow closers stacked at the end: "The choice is ours." / "That's how change happens." -> semantic hollowness, weighty first read, empty second -> cut both; "Steering with intention, wisdom, and collective accountability." already lands the close.
6. "Here's what most people miss:" / "Here's what people don't get:" -> insight-gatekeeping opener used twice -> keep one at most; the second can go straight to the quote.

### NOT-VOICE but reader-visible (structural)

7. **Appended internal prep material published to readers:** everything from "KEY VIRAL QUOTES (From Panelist Call)" through "PANEL QUESTIONS (40-Minute Discussion)" is planning-doc content (with "? Use:" annotation lines), and the second essay fragment "My relationship with AI is non-consensual..." sits orphaned between the bio and the prep notes -> unpublish the prep block from the post (it belongs in drafts/notes); either fold the "non-consensual" fragment into the essay proper (it's good material — arguably the strongest three paragraphs on the page) or cut it.
8. **Corrupted arrow characters:** "Prompt: 'Marketing professor' ? Harvard-blazer man, power pose" and the "? Use:" lines — a "→" mangled to "?" at publish time, same encoding-corruption class as the Ethọ́s posts.
9. **Run-together list items in the rendered HTML:** "Training data reflects societal biases (AI is a mirror to society)Reinforcement learning: The more you interact..." and "Ask the same question to ChatGPT, Claude , and GeminiCompare outputs – where do they differ?" -> list markup lost at publish; rebuild as proper list blocks (Phase 1 noted this; confirmed reader-visible).
10. Unattributed blockquote: "If there are values you have which are not expressed yet in text... dangerously close to won't exist." -> reads as a quote but no speaker named -> attribute it or own it in first person.

## Dodged tells found

- The en-dash-as-em-dash system (Flagged #3) — the single most important dodge in this post.
- Reworded redefinition-reveals (Flagged #4), all dodging the contraction-anchored regex.
- "Here's what most people miss / people don't get" repeated hook (Flagged #6).
- Parallel-binary stack in the close: "extraction or stewardship. Individual optimization or community flourishing. Quarterly thinking or seven-generation wisdom. Innovation theater or actual transformation." — four binaries chained; borderline list-stacking, but it's a deliberate closing riff and mostly earns it. Named, kept.
- No landscape filler, no "in an increasingly..." opener, no manufactured vulnerability (the vulnerability here — non-consensual training data, his own images — is real and specific), no uniform positivity.

## Checker-gap candidates

- **En dash (U+2013) used as prose punctuation** — the anti-glossary only bans the em dash (U+2014). Candidate: flag ` – ` (space-en-dash-space) as a soft rule; date/number ranges ("2024–2025") don't use surrounding spaces, so the spaced form is almost always prose-dash work.
- **Umlaut-less "Kris Krug"** — canonical section lists the spelling but no regex enforces it. Candidate: `Kris Krug\b` (with the space, so URLs/slugs like kriskrug.co don't false-positive).
- **Corrupted-character detector** — "?" where an arrow/diacritic should be ("Prompt: X ? Y", "Eth??s"): candidate `\w\?\?\w` or a mojibake heuristic; encoding corruption currently dodges every literal rule.
- **Uncontracted "That's not X. That's Y." reveal** — sibling of the pattern already noted in god-skills/zero-to-one; recurs here at the highest density of the batch.
