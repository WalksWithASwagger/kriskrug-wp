# The Ethos Lab Block Party Album *(title as published; canonical: Ethọ́s Lab)*

**Facet:** The Host (community storytelling, people hyped by name), with Friend warmth in the parking-garage close and an Anti-Hero sign-off ("Do not let the machine have the last word.") | **Mechanical flags:** 1 (canonical spelling in the title) | **Depth:** standard read

## Verdict (2-4 sentences)

Fully him — warm, specific, consent-centered, funny, and the credit flows to the people who gave the songs. The voice test passes in every section; what's broken is the rendering: "Ethọ́s" is corrupted to "Eth??s" seven-plus times through the body, player name, and credits, and the post title itself uses the non-canonical "Ethos Lab." Fix the encoding and the title and this post is done; no prose surgery needed.

## What's working (quoted specifics)

- The pitch, in his cadence: "Sit down, tell me something real, and I will turn it into a song before you leave." and "One booth. One afternoon. A line of people willing to tell the truth."
- People hyped by name with their actual lines, the Host move exactly: Chris ("Nobody talks about Vancouver, but there's a lot of cool things going on"), Bobby ("You don't eat until they do. You open the doors for them."), Maurice, and Anthonia — who "built the room" — closing the record.
- The rule stated as lived practice, not slogan: "The person is the hero. The technology is never the hero." backed by an actual editorial decision: "If a track started feeling like an AI demo instead of like somebody's actual life, it was wrong, and I changed it or cut it."
- Consent as the story, with receipts: "We cleared all of it on June 14, the day after the party, person by person." / "Minors are first name only and never shown as a face." / "nothing about them shipped without a guardian saying yes."
- The reframe question: "People ask me how the AI worked. The harder and better question is how the consent worked."
- The Friend-facet close is the best writing in the June batch: "somebody in the parking garage had a dead battery. Ribbon skirt, stranded under the fluorescent lights. I had cables in the back. You give somebody a jump and somehow you are the one who feels revived." and "I did not have to chase the signal. For once I was standing in it."
- Genre inventory that earns its stack: "Ghanaian highlife. Afro-soul. Caribbean soca. Deep vocal house. Indie folk singalong. A cottage-core chanson in French. A nineties summer hip-hop track. The record sounds like the room sounded." — seven fragments, then a landing line that justifies them.
- Sign-off in full voice: "Bring both hands. Keep your taste on. Do not let the machine have the last word."

## Flagged (each: quoted passage -> why -> suggested fix)

### HARD RULE

1. Post title: "The Ethos Lab Block Party Album" -> canonical spelling is **Ethọ́s Lab** (diacritics not optional; slug staying ASCII `ethos-lab` is normal) -> "The Ethọ́s Lab Block Party Album" *(checker-verified)*.

### NOT-VOICE but reader-visible

2. **Encoding corruption throughout the stored content:** "at the Eth??s Lab block party" (caption), "I set up a booth at the Eth??s Lab open house" (opener), "the Eth??s Lab Block Party album" (link), "a little ETH??S·FM player" (x2), "the lyrics got written through the Eth??s brand voice," "Produced by Kris Krüg for Eth??s Lab" (credits) -> "Ethọ́s" mangled to literal "Eth??s" at publish time; verified reader-visible in Phase 1 (REST payload and rendered page) -> restore the proper characters in the stored post content, then re-verify live. Checker-verified target forms: "The Ethọ́s Lab Block Party album" / "There is a little ETHỌ́S·FM player on the page that I am stupidly proud of."

### JUDGMENT CALL

- None. The two contrast constructions present ("That is not a slogan I put on a slide. It is the thing that decided every call I made all day." / "The music is made with AI. The people are not. The day was not.") both carry real decisions; keep.

## Dodged tells found

None found. Scanned explicitly: no reworded redefinition-reveals without payload, the one long list (genres) is earned inventory with a landing line, no filler metaphors, no throat-clearing, no bold-header padding, conclusion adds (the go-listen invitation plus the sign-off), copulas plain, positivity warm but not uniform (fear, being fried, a dead battery all live in it), and the vulnerability is actual events rather than "I'll be honest" performance.

## Checker-gap candidates

- Same as vancouver-made-world-cup: **the corrupted "Eth??s" form dodges `Ethos Labs?\b`**, so the canonical-spelling rule misses its own worst case. Candidate anti-glossary regex: `Eth\?\?s` plus a general in-word `\?\?` mojibake flag. (This post is the primary instance; the cross-link list in vancouver-made-world-cup is the secondary.)
- **All-caps stylized forms:** if ETHỌ́S·FM is going to recur as a brand, the canonical list may want the stylized form recorded so future checks don't flag or mangle it.
