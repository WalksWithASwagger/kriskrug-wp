# KRÜG letter, issue one (December 2026)

**Status: DRAFT for Kris's edit.** It is not loaded into Beehiiv. Nothing was created, scheduled or sent there, and nobody was contacted. The send is Kris's alone.

Refs [#1278](https://github.com/WalksWithASwagger/kriskrug-wp/issues/1278), step 3. KRÜG is the publication at `vancouver.beehiiv.com`. Its public archive showed "No posts found" on 2026-11-12, so this is the first issue it will ever send.

This repo is public, so the draft can be read before it goes out. Everything in it comes from public pages.

## Files

| File | What it is |
|---|---|
| `letter.md` | The letter, about 660 words with seven links, ready to paste into a new Beehiiv post once you've edited it |
| `subject-lines.md` | Three subject lines, each with a preview line, and the one I'd pick |
| `sources.md` | Every claim, the public page it comes from, and the date it was checked |

## Your calls

1. **Why monthly.** "So here's a promise I can keep" is my guess at the reason. If yours is different, say it your way.
2. **Subject line.** I'd go with "Who gets a say". If you pick another, change the `# Who gets a say` title at the top of `letter.md` to match.
3. **The AI-assistance line** at the bottom matches the one on your November posts. Keep it, change it or cut it.
4. **Anything published after November 12.** The letter covers the four posts that were live then. If another one lands first (the Gorgeous Ghost and Both Things Are True packages are both ready to stage), add a short section and check that "Every post I wrote in November came back to one question" still holds. If the new post went up in December, reword that line so it doesn't only say November.
5. **The November 25 meetup** is left out because it hasn't happened yet. If you want two lines on it, write them from the room. The public billing is in `sources.md`, and Ashley Smith is on it, so it could close the Canada Now section.

## Send window

Best between December 1 and 9, while both December rooms are still ahead.

- After December 10, cut the Film Club entry, and change "two December rooms" in preview 1 to "the December meetup".
- On December 16 or 17, swap the December section for a few lines on the rooms and a pointer to January.

## In Beehiiv, before you send

- **Reply-to.** The letter's only ask is "hit reply", so make sure replies reach you.
- **Audience.** The send check's never-engaged exclusion doesn't fit issue one: KRÜG has never sent, so no subscriber has had a chance to engage yet. Pick the audience yourself.
- **Sender name and web title.**
- **Test send.** Send yourself a test and click all seven links.

## Checks run on 2026-11-12

**Beehiiv send check.** The skill reads a Beehiiv post or pasted copy. There is no Beehiiv post, so I ran its checks by hand on these files.

| Check | Result | Notes |
|---|---|---|
| 1. Placeholders | PASS | All three subject lines and previews are real, and the letter has none of the placeholder tokens the check lists. |
| 2. Audience | NOT CHECKED | Nothing is in Beehiiv yet. See "Audience" above. |
| 3. Speaker embargo | PASS | The festival is over. People are named only as your own published posts and the public event pages already name them. No attendance numbers, no out-of-town framing, no member code. |
| 4. Voice | PASS | No em or en dashes, and nothing from the check's trope list: no antithesis turns, no negation fragments, none of the LLM vocabulary set and none of the filler words. |
| 5. Claims | PASS | Every claim is traced in `sources.md`. Nothing is asserted that a public page doesn't say. |
| 6. Links | PASS | 7 of 7 return HTTP 200 logged out, and every link has label text. The check's early-bird link rule was for the festival's early-bird emails and doesn't apply here. The two RSVP links match the ones on kriskrug.co/events and the BC + AI Film Club page. |
| 7. Send | NOT SENT | Copy: ready for your edit. Send: NO-GO until it's in Beehiiv and you've checked the audience, the reply-to and a test send. |

**Repo and voice checks:**

- `make voice-check FILES='content/drafts/2026-12-krug-letter-01/*.md'`: 4 files, 0 violations.
- `make voice-check` (default payload and theme scan): 185 files, 0 violations, 214 baseline-waived. Its default scan only covers `post.md`, `post.html`, `post-body.html` and `copy.md`, so this package needs the `FILES=` run above.
- `make docs-truth-check`: passed.
- The full kk-voice checker (`voicecheck.py`) on `letter.md` and `subject-lines.md`: 0 flags.

Run the same checks again after you edit.

## How it was made

An agent drafted it on 2026-11-12 from the four posts published on kriskrug.co between November 1 and 9, the public Events, Film Club and Luma pages, and the site's own newsletter wording. No subscriber data, no Beehiiv account data and no private sources.
