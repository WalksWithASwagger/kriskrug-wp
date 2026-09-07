# Source manifest and claim ledger

**Prepared:** 2026-09-07
**Subject:** theBreaker.news Podcast edition 460, "thePodcast: A peek inside B.C.'s Artificial Intelligence ecosystem"

## Primary sources

### S1. theBreaker.news episode page (canonical)

- URL: `https://thebreaker.news/opinion/podcast-460/`
- Published: 2026-08-09. Author byline: `thebreaker`. Sections: News, Opinion.
- Host: Bob Mackin, publisher of theBreaker.news.
- Guests: Kris Krüg (executive director, BC + AI Ecosystem Association) and Dave Olson.
- Runtime: 23:16. Format: m4a.
- Enclosure captured 2026-09-07: `https://episodes.castos.com/theBreaker-Podcast/2562476/c1e-jzdc4p8p3cpo3gm-6z089n5oi8d6-fnz2hv.m4a` (20,118,358 bytes).
- Player and download routes: `https://thebreaker.news/podcast-download/15764/podcast-460.m4a`, `https://thebreaker.news/podcast-player/15764/podcast-460.m4a`.

### S2. Substack episode post

- URL: `https://bobmackin.substack.com/p/thepodcast-a-peek-inside-bcs-artificial`
- Published: 2026-08-08 (one day ahead of the site edition; paid subscribers get early access).
- Same show notes as S1.

### S3. Substack preview post

- URL: `https://bobmackin.substack.com/p/podcast-preview-will-ai-sway-bcs`
- Published: 2026-08-07. Title: "Podcast Preview: Will AI sway B.C.'s local elections?"
- States the full edition "premieres Aug. 9."

### S4. YouTube preview clip

- URL: `https://www.youtube.com/watch?v=fSbIJO0K-8o`
- Channel: Bob Mackin. Uploaded 2026-08-07. Duration: 96 seconds.
- Title: "Podcast Preview: Dave Olson and Kris Krug".
- This is the preview, **not** the full episode. Do not describe it as the interview.
- Publisher captions available (`en-orig`), pulled 2026-09-07.

### S5a. Supplied clean transcript (primary)

- `transcript-clean.txt` in this packet. 4,174 words.
- Supplied by KK 2026-09-07 and ingested to the knowledge base at
  `kk-kb/content/media/interviews/2026-08-09-thebreaker-460-bob-mackin-transcript.md`
  with analysis at `...-recap.md`.
- Better punctuation and turn structure than the machine pass. **This is the quoting source**, as reconciled below.

### S5. Local transcript of the full episode (cross-check)

- `transcript-raw.txt` and `transcript-timestamped.vtt` in this packet.
- Produced 2026-09-07 from S1's enclosure with `whisper.cpp` (`ggml-small.en`), 3,944 words.
- Retained because it resolves several places where the supplied transcript drops out. See the reconciliation table in the kk-kb recap.
- **Machine transcript, not a publisher transcript.** Every quote used in `post.md` was re-checked against the audio region before use. Known ASR artifacts are listed below.

## Known ASR artifacts in S5

| Heard as | Actual | Basis |
|---|---|---|
| "Chris Krug" | Kris Krüg | Name spelling, house rule |
| "West Bank lands" | Westbank lands | Westbank Corp sites at 150 West Georgia St and M3 Mount Pleasant |
| "detector spots" | detector bots | Context |
| "tech pros" | tech bros | Kris's established phrasing |
| "two vaunting of tasks" | too daunting of tasks | Context |
| "Yifka had a long history" | "And you've got a long history" | Bob Mackin's question to Dave Olson |
| "Fagiana" | Fagiano Okayama | J-League club, promoted to J1. Colour only, not used in post |

### S8. The Tyee, "Where Do Vancouver Parties Stand on AI?"

- URL: `https://thetyee.ca/News/2026/08/11/Where-Vancouver-Parties-Stand-AI/`
- Katie Hyslop, 2026-08-11. **Two days after the episode published.**
- Party-by-party AI positions: COPE, Vote Vancouver, Green Party of Vancouver, ABC, TEAM, Vancouver Liberals, OneCity.
- Kris and BC + AI are **not** mentioned. The post says so explicitly rather than implying he was part of the coverage.

### S9. The Tyee, "Vancouver's Growing Anti-AI Movement"

- URL: `https://thetyee.ca/News/2026/07/10/Vancouver-Growing-Anti-AI-Movement/`
- Isaac Phan Nay, 2026-07-10.
- Source for the protest scale: ~500 at the first (late May), ~1,000 at the second (late June), 100+ at a Russian Hall town hall, COPE petition past 8,000 signatures.
- Kris is not mentioned here either.

## Claim ledger

| Claim in `post.md` | Status | Evidence |
|---|---|---|
| Episode is edition 460, published Aug 9, 2026, runtime 23:16 | Verified | S1 |
| Recorded outside the H.R. MacMillan Space Centre after the July 29 meetup | Verified | S1 show notes and S5 audio |
| Dave Olson was the July 29 featured speaker, in from Okayama, Japan | Verified | S1, S5 |
| BC + AI has 300 members | Verified | Kris says "300 people" in S5; matches his 2026-08-01 ruling |
| "600 startups" ecosystem figure | Not used in post | Kris attributes it to "other organizations" in S5. Left out of `post.md` rather than repeated second-hand |
| Council sent the data centre back to city planners, so it lands in the campaign | Verified | S5 plus Daily Hive, "Telus-Westbank AI data centre decision punted until after Vancouver election" |
| Westbank sites are 150 West Georgia St (beside BC Place) and M3 in Mount Pleasant | Verified | Daily Hive coverage of the Telus and Westbank data centre projects |
| No further public consultation between August and October 2026 | Verified | Daily Hive reporting on city staff timeline |
| Kris saw "the COPE people" at the demonstrations | Verified | His own words in S5a and S5. COPE's data centre organizing is corroborated by S9 |
| ~500 at the first protest, ~1,000 at the second | Verified, attributed to The Tyee in the post | S9 |
| Seven parties had an AI position two days after the episode | Verified | S8. Post names the parties and links the scorecard |
| Kris is not quoted in either Tyee piece | Verified | S8 and S9. The post states this as a self-criticism, which is accurate |
| Hollywood North asset pipelines have moved to token-based production | Kris's own claim | S5a. His assertion as an industry observer, presented as his view |

## Open flags for KK

1. **Meetup number.** On the recording Kris says "Vancouver AI Community Meetup number 32 in a row." Repo and kk-kb records call the July 29 event **Meetup #31**, and Dave Olson says "number 31" twice in the same episode. Re-checked the audio at 00:00:46 with two whisper models; both hear "32." The public Luma listing (`https://luma.com/july-ai`) also says **#31**, July 29, 2026, H.R. MacMillan Space Centre, with Dave Olson and Dorothy Pang. So every written record says 31 and only the spoken intro says 32. `post.md` deliberately says "the July Vancouver AI Community Meetup" and carries no number. **Rule on which is correct before any copy uses a number.**
2. **Bob Mackin's AI-lab premise.** Around 00:12:00 Bob paraphrases a headline about an AI bot that "escaped from its lab and attacked a competitor's lab." That premise is not verified and is not repeated in `post.md`. Kris's answer is used; Bob's framing is not.
3. **Dave Olson's "repositize."** Transcribed as heard. Confirm the spelling with Dave before quoting it in public copy. Not used in `post.md`.

### S6. Vancouver AI Community Meetup listing

- URL: `https://luma.com/july-ai`
- Confirms Meetup **#31**, July 29 2026, 6:00 PM to 10:00 PM PDT, H.R. MacMillan Space Centre, 1100 Chestnut St.
- Featured: Dave Olson and Dorothy Pang. Host: Kris Krüg.

### S7. Data centre reporting (context, not quoted)

- Daily Hive, "Telus-Westbank AI data centre decision punted until after Vancouver election".
- Daily Hive, `https://dailyhive.com/vancouver/150-west-georgia-street-720-beatty-street-vancouver-westbank-allied-data-centre-proposal`.
- Used only to confirm the council deferral, the two site locations, and the consultation timeline.

## Link check

All external links in `post.md` returned HTTP 200 on 2026-09-07. Note: `daveolson.ca` is a **different Dave Olson** (a theologian) and must never be used. The correct archive is `https://daveostory.com/`, which is also the 5,600 post WordPress archive he describes in the episode.
