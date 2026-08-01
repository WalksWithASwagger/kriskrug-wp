# A Practical Guide to Agentic Workflows (god-skills)

**Facet:** The Builder (teaching/operator), trace of Anti-Hero ("the older Punk Rock AI instinct") | **Mechanical flags:** 6 (all table-separator syntax, not prose) | **Depth:** deep read (mandatory)

## Verdict (2-4 sentences)

The prose voice is substantially Kris-as-Builder: first person, deliverables-not-dreams, real edge ("an enthusiastic mess," "a rail, not a maze," "drifting into theatre"). Two things hold it back from fully sounding like him: it leans on one rhetorical move — the "X is not A. It is B." redefinition skeleton — roughly a dozen times in 2,170 words, which is an AI-drafting cadence even when individual instances land; and it fails the Builder facet's receipts test, with no named people (one Karpathy nod), no student wins, and explicitly "sanitized examples" where his voice would say "here's what I actually did this morning." Separately, the two tables are a live rendering bug (raw markdown gibberish to readers) that matters more than any word choice. Voice grade: recognizably him, running at about 80%.

## What's working (quoted specifics)

- The opening move is genuinely his both/and: "Not because the models got worse. The opposite. They got good enough that a sloppy request could produce something that looked finished."
- "a routing system for AI builders who want agents to help without turning the whole project into an enthusiastic mess" — edge, humor, precision in one line.
- "The agentic loop should feel like a rail, not a maze." and "If a direct file edit solves the problem, do not invent a workflow engine." — Builder facet at its best: anti-ceremony, pro-simplicity.
- The "A Note On The Name" section is honest self-stewardship, not defensiveness: "If that framing ever starts to feel like spectacle instead of stewardship, the public version should use the neutral phrase 'canonical skills' and leave the mythology at the door."
- The close adds instead of restating: "Ask the right skill first. Keep the loop small. Prove what changed. Leave the system easier to trust than you found it. That is the whole game."
- Section-by-section 5Q: sounds-natural mostly passes; banned words clean in prose; edge present throughout. The two failures are credit (Q2) and specific example (Q3) — see Flagged #3.

## Flagged (each: quoted passage -> why -> suggested fix)

### HARD RULE

1. All 6 mechanical em-dash hits are markdown table separators ("| Skill | Codename | Use it when | Output | |—|—|—|—| ...") in the Ten Canonical Skills table and the routing cheat-sheet table -> **NOT-VOICE but reader-visible**: two markdown tables were pasted into plain WP paragraph blocks and render as run-together pipe/dash gibberish on the live page -> rebuild both as real WP table blocks (or styled lists). One structural edit clears all 6 flags; punctuation-level fixes do not apply. This is the post's fix-first item.

### JUDGMENT CALL

2. **Redefinition-reveal density** — the "not A. It is B." skeleton ~12 times: "repo-onboard does not exist to write code. It exists to understand the repo..." (same shape x3 in one paragraph), "The point is not to create a skill for every mood. The point is...", "The important part is not that these exact names are perfect... The important part is...", "The answer is not to make the agent less capable. The answer is...", "Done does not mean 'the model produced an answer.' Done means...", "The output is not code. The output is orientation.", "The point is not fear. The point is consent and reversibility.", "A lot of AI workflow failures are not technical failures. They are boundary failures.", "Shipping is not just movement. Shipping is accountable movement." -> each one individually reads fine; a dozen of them is a template, and "Shipping is not just movement" is the literal banned "not just X, it's Y" cadence reworded past the regex -> keep the strongest third, vary the rest. Checker-verified alternatives: "Shipping is movement with a paper trail." / "verify-evaluate has one job: evidence."
3. **Receipts gap for the Builder facet** — examples are explicitly "a few sanitized examples," no named people, no student discoveries, no morning-build story. The facet is defined by "real examples from his own work, credits students' discoveries" -> not a sentence-level fix; add one real, named incident (a specific repo, a specific save-by-safety-review) and the post jumps a grade. Flagging as the main voice debt, no rewrite supplied (would require facts I don't have).
4. Title-case headers on every word ("A Note On The Name," "From Prompting To Operating," "Where The Engineering Discipline Shows Up") -> mild AI-formatting scent; his other June posts use sentence case -> optional normalization, low priority.

## Dodged tells found

- The redefinition-reveal density above (the post's one real tell — Flagged #2).
- "Shipping is not just movement. Shipping is accountable movement." — dodges `it'?s not just .+ it'?s` by dropping the contraction and repeating the subject.
- Anaphora blocks ("The wrong move is to... The routed version starts with..." x4) — deliberate parallel teaching structure, and it works; named, not flagged.
- No landscape filler, no "increasingly/rapidly" openers, no throat-clearing "ultimately/at its core," no manufactured vulnerability, no uniform positivity (friction is real throughout), conclusion adds rather than restates. En dashes: none doing em-dash work (handoff paths use ASCII "->").

## Checker-gap candidates

- **Uncontracted redefinition-reveal** (shared with zero-to-one): "X is not just movement. X is accountable movement." / "does not exist to A. It exists to B." — candidate soft regex: `\b(is|does) not (just |only )?(exist to )?[^.]{3,60}\. (It|That|The \w+) (is|exists|means)\b`; needs tuning against false positives, but the shape recurs across the June batch.
- **Markdown-table syntax in rendered WP content**: `\|\s*[-—:]+\s*\|` inside post HTML would catch pasted-markdown tables (this exact bug) as a structural lint, distinct from the em-dash word rule.
