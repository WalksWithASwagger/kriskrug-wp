# Vancouver World Cup 2026 Hackathon & Design Jam (MADE ON)

**Facet:** The Anti-Hero, Builder blend (protest-art manifesto with a build story and a credits section that's pure Host) | **Mechanical flags:** 0 | **Depth:** standard read

## Verdict (2-4 sentences)

Unmistakably Kris — this is the Anti-Hero facet working exactly as the crystal describes it: sacred and profane held together, righteous edge without punching down, receipts as the actual art form. "Everyone else made a souvenir. We made the receipt." could go straight into the exemplars folder. The only reader-visible problem is not voice: the cross-link list renders "The Eth??s Lab Block Party album" with corrupted diacritics.

## What's working (quoted specifics)

- The thesis line and title move: "Everyone else made a souvenir. We made the receipt." — receipts vocabulary doing conceptual work, not decoration.
- The refusal narrative is the politics-of-tech core, lived: "When somebody asks me to make a celebration jersey for a tournament that lands on stolen ground, the honest answer is no. But no is not a project. So I made the refusal into the work."
- Boundary-drawing with specifics, not virtue-language: "No borrowed sacred imagery. No turning a culture into a costume. The only thing I let myself dress up in was the coloniser's own paperwork, because that is the part I am actually allowed to wear."
- "AI was the brush, not the artist." and "They asked for the Vancouver story. We finished the sentence." — edge with a wink, the Anti-Hero close.
- Receipts throughout: "double silver," "second in the technical hackathon and second in the fashion design challenge, both at the BCIT Tech Collider on June 20," "Made on 729 million dollars of public money," "Formmé is manufacturing five."
- Distributed credit in the outro: "Thanks to Devin by Cognition and Formmé for the tracks, BCIT Tech Collider for the room, and the Young Guns Studio and Students@AI crews for putting it on." — "crews," the preferred vocabulary, used naturally.
- Honest process note instead of hero narrative: "I spent the build fixing what broke, surviving a site-wide redesign, and it still placed twice."
- Kit blurbs have teeth: "Hype the city, bill the public, take the exit. You are the bagholder."

## Flagged (each: quoted passage -> why -> suggested fix)

### HARD RULE

- None mechanical.

### NOT-VOICE but reader-visible

1. Cross-link list: "The Eth??s Lab Block Party album" -> live encoding corruption of "Ethọ́s" (stored content, visible to readers; same corruption class as the block-party post itself) -> restore the diacritics: "The Ethọ́s Lab Block Party album" *(checker-verified — and note the corrupted form also dodges the `Ethos Labs?\b` canonical check)*.

### JUDGMENT CALL

2. "The brief at Vancouver Made was simple. What if Vancouver had its own World Cup kit." -> question phrased without a question mark -> stylistic; reads as deliberate flatness, keep.
3. "Whose cup is it anyway?" as a floating one-line section -> works as the Anti-Hero mic-drop; keep.

## Dodged tells found

None found — and this post is the register calibration for the batch. The contrast structures ("Not kits that celebrate the tournament. Kits that name what it is built on") are the same skeleton flagged elsewhere, but every instance lands with new content, the fragments are protest-cadence rather than filler, there is no list-stacking (the five kit bullets each carry a distinct argument), no filler metaphors, no throat-clearing, and the close adds (the credits + invitation). Uniform positivity is absent by design; the whole piece is built on friction.

## Checker-gap candidates

- **Corrupted-diacritic forms dodge the canonical-spelling regex:** "Eth??s" doesn't match `Ethos Labs?\b`, so the wrongest possible rendering of the name is the one the checker can't see. Candidate: add `Eth\?\?s` (and more generally a `\w\?\?\w` mojibake heuristic) to the anti-glossary regex section. Phase 1 recorded this; confirmed here as reader-visible in a second post.
