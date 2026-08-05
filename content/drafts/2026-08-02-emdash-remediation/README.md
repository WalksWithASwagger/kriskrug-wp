# Em dash remediation: post 12653, AI Lands Inside Every Profession

**Issue:** #603 (voice sweep epic). The live-apply child for this post is VOICE-5, [#609](https://github.com/WalksWithASwagger/kriskrug-wp/issues/609).
**Lane:** Track A, repo-only. Nothing here touched the live site. No REST writes, no deploys, no connector runs.
**Date:** 2026-08-02.

## Which post, and why this one

**Post 12653**, `ai-lands-inside-every-profession`, published **2026-07-31T17:40:55**.

It is the newest post in the sweep window (2026-06-18 through 2026-07-31) per `content/drafts/voice-audit-blog-sweep-2026-08-01/manifest.json`, and it is the post the audit calls the em dash blowout. Three independent confirmations that it is the right target:

1. `00-summary.md`, P1 item 1: "AI Lands: 26 prose em dashes (rank 1 offender)... Post ID 12653."
2. The tally table in the same file: "em dash (32 of 44; **26 prose in ai-lands** + 6 table syntax in god-skills)."
3. Direct count on the stored snapshot: `snapshots/2026-07-31-ai-lands-inside-every-profession.txt` contains exactly **26** U+2014 characters, and `voicecheck.py` on that file returns 27 flags (26 em dash, 1 soft `team`).

**It is not post 12034.** Zero to One (`zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey`, 2026-06-30) is the third-person rewrite job, VOICE-8 / [#612](https://github.com/WalksWithASwagger/kriskrug-wp/issues/612), and it is owned by another lane running right now. Its audit finding is 6 mechanical flags and a person-shift problem, not a dash blowout, and its date is a month earlier than 12653. Nothing in this directory touches 12034. The one place it comes up is the `origin arc separately` link inside 12653, which is left exactly as it is.

## Before and after

| Metric | Before | After |
|---|---|---|
| Em dashes (U+2014) in body | **26** | **0** |
| `voicecheck.py` flags | 27 (26 em dash, 1 soft `team`) | 1 (the same soft `team`) |
| `voicecheck.py` exit | 1 | 1, on the documented keep only |
| En dashes (U+2013) | 2, both date ranges | 2, unchanged |
| Redefinition-reveal instances | ~8 | 5, with the two flagship instances intact |

The one remaining flag is `judgment is a team sport`. Both audit phases ruled it a keep: it is an idiomatic set phrase, not a reference to his own crew, and "crew sport" is not a thing. Left alone deliberately.

Every dash is rewritten, never swapped. No hyphens, no en dashes, no spaced hyphens standing in for the old dash. Twelve became colons, eight became a period plus a new sentence, three became commas, one became a comma with the clause inverted, and one matched pair became parentheses around a link aside. The full site-by-site record is in `dash-ledger.md`.

## What else got fixed

**The redefinition-reveal house tic.** The audit flagged this as the post's real voice risk after the dashes, and specifically because it dodges the checker: `voicecheck.py` anchors on the contraction `it's not just`, so a decontracted split like "The failure mode is not departure. The failure mode is a province with no serious pathway home." sails straight through with zero flags. Eight of them in 2,247 words turns a cadence into a template.

Three were varied, per the audit's instruction to keep the two named flagship instances and vary two or three of the rest:

- L60 "That is not a romance about grit, it is a design choice" became "That is a design choice, not a romance about grit." This one does double duty since it was also dash site 8.
- L103 "The failure mode is not departure. The failure mode is a province with no serious pathway home." became "What kills a region is having no serious pathway home."
- L135 "The point is not to cheerlead AI. The point is to build enough shared practice..." became "I am not asking you to cheer for AI. I am asking you to help build enough shared practice..."

Kept on purpose: the Space Centre venue-rental line (L38) and "Ecosystem is not a vibe. It is repeated contact with consequences." (L99), both named keeps in the audit; the origin thesis at L36; the researchers' finding at L97; the fragment ladder at L115; and the pull quote at L14, which is quoted as printed in Business in Vancouver. Rationale per instance is in the ledger.

**Typography matched to the stored post.** `remediated-body.md` uses the same curly apostrophes and paired curly quotes the live post already stores, so the applying agent can swap whole paragraphs without introducing an encoding diff. Relevant given the latin1 database behaviour documented for this site.

## What was deliberately left alone

| Thing | Why |
|---|---|
| Festival spelling ("Futureproof" x3) | VOICE-10 / [#614](https://github.com/WalksWithASwagger/kriskrug-wp/issues/614) owns that decision. Glossary says FUTURE PROOF, the July 28 sibling says Future Proof, this post says Futureproof. Not mine to pick. |
| `judgment is a team sport` | Documented keep in both audit phases. |
| The "no X, no Y, just Z" ladder at L30 to L32 | Works locally, and "A drumbeat" pays off again at L129. The audit flagged it only as a cross-post template watch item. |
| Images, alt text, links, embed IDs, headings, block order | Out of scope. The lane is dashes plus reveal density. |
| Post 12034, and every other post in the sweep | Other lanes own them. |

## One thing I could not resolve, flagged not fixed

L115 reads: "We took the community **a platform built from those rooms**, and then I read all thirty-two expert reports." That sentence looks like it is missing a word or a preposition (took the community *to Ottawa*? took *to* the Task Force?). It is preserved verbatim in `remediated-body.md` because fixing it is a content decision, not a punctuation one, and it is outside this lane. Worth a look from whoever applies #609, or from KK directly.

## Files

| File | What it is |
|---|---|
| `README.md` | this |
| `remediated-body.md` | full corrected body, block markers included, ready for a snapshot-first apply |
| `dash-ledger.md` | all 26 sites with original phrasing, rewrite, and the move used |

## How to verify

Zero em dashes in every file in this directory:

```
python3 -c "import pathlib;[print(p.name, p.read_text(encoding='utf-8').count(chr(0x2014))) for p in sorted(pathlib.Path('content/drafts/2026-08-02-emdash-remediation').glob('*.md'))]"
```

Expect `0` for all three. The check is written with `chr(0x2014)` rather than a literal `grep` pattern so that running the verification does not reintroduce the character into this file. `dash-ledger.md` writes the original character as the literal token `{EMDASH}` precisely so the ledger can quote the originals without carrying them.

Mechanical voice check on the corrected body:

```
python3 ~/Code/kk-voice/scripts/voicecheck.py content/drafts/2026-08-02-emdash-remediation/remediated-body.md
```

Expect exactly 1 flag, the soft `team` at the "team sport" line, and nothing else.

Baseline for comparison:

```
python3 ~/Code/kk-voice/scripts/voicecheck.py \
  content/drafts/voice-audit-blog-sweep-2026-08-01/snapshots/2026-07-31-ai-lands-inside-every-profession.txt
```

Expect 27 flags.

## Still open

- Live apply against 12653 has not happened and is not authorized from this lane. #609 owns it: snapshot first, slug and ID check, cache-bypass curl after.
- Festival naming decision is blocked on #614.
- The checker gap that let this density through is #616's work in `~/Code/kk-voice/anti-glossary.md`. The candidate regex from the audit is `\b(is|are|was) not (just|only|simply) [^.]{3,80}\. (It|That|They|These) (is|are)\b`, soft flag, judged on density rather than per instance. Not touched here, different repo.
- The L115 missing-word question above.
