# Mechanical slop check — Keep the Machine Strange (post.md)

Run: 2026-08-10, `voicecheck.py` from `~/Code/kk-voice/scripts/` (note: the corpus moved from `~/Code/dark-crystal/kk-voice/` to `~/Code/kk-voice/`; the voice-slop-audit skill doc still points at the old path).

**Result: exit 0. Zero hard failures.** No em dashes, no banned vocabulary, no chatbot leakage, canonical spellings intact. Three soft warnings, all in the same rhetorical family.

## Soft flags

### 1. Line 49 — reveal ladder (KEEP)
> "Not a luddite. Not a guy jamming his boot into the gears."

Rule: reveal-ladder template, soft flag, earned when each rung carries new payload. Verdict: earned. Rung one is the concept, rung two is a vivid image. This is the sentence doing its job.

### 2. Line 107 — decontracted redefinition-reveal (FIX, optional but recommended)
> "So responsible AI is not only bias testing and red teaming, important as those are. It is responsibility tracking."

Rule: the "is not only X. It is Y" cadence with the contraction stripped, the exact dodge pattern the audit skill warns about. This one is the weakest instance in the piece because two pull quotes nearby already run the same antithesis move, so the density argument (see alignment report) says this is the one to cash in.

Suggested rewrite, re-verified clean through voicecheck.py (0 flags):
> "So responsible AI runs deeper than bias testing and red teaming, important as those are. It is responsibility tracking."

### 3. Line 186 — reveal ladder (KEEP)
> "Not to flee the machine. Not to worship it."

Verdict: earned. The two rungs are distinct verbs of failure (flight vs worship) and it lands the Anti-Hero close. Keep.
