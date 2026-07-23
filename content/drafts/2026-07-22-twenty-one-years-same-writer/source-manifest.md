# Source manifest and claim ledger

**Prepared:** 2026-07-22

**Public boundary:** The draft uses Kris's own archived writing, aggregate measurements already shown in the linked Claude artifact, and local public-repository evidence. It does not publish the private modern corpus or any unapproved third-party messages.

## Primary sources

### S1. Claude artifact: Classic Blogger KK, A Voice Forensics Report

- User-supplied private artifact. Its URL and organization identifier are intentionally omitted from this public repository.
- Inspected in the authenticated browser on 2026-07-22.
- Visibility at inspection: `Share, private`.
- Supports the experiment narrative, selected aggregate rates, two visible retractions, the generated-pastiche disclosure, and the current thesis that the checker detects unedited output rather than human authorship.
- Do not link from the public post until the artifact's sharing state is intentionally changed.

### S2. Recovered kriskrug.com archive

- Local canonical path: `/Users/kk/Code/kk-kb/content/archives/kriskrug-com-blog/README.md`
- Recovery commit: `a0791f0861987703db5a2217a2fb60eed2c22663` (`feat: recover kriskrug.com blog archive from Wayback Machine (2003-2017) (#2475)`).
- Verified facts:
  - 1,274 unique recovered posts, 2003 to 2017.
  - 1,332 of 1,348 attempted pages recovered, or 98.9 percent.
  - 57 duplicate migration-era files removed.
  - 851 posts and 147,893 Kris-authored words in the voice corpus.
  - Comment threads, blockquotes, and 423 link-drop posts under 40 words excluded from that corpus.
- Public article uses 1,274 for the recovered archive and avoids presenting a conflicting total word count as a measured result.

### S3. Verified 2005 archive excerpts

- `content/archives/kriskrug-com-blog/2005/2005-05-24-photographers.md`
  - Title: `My New Favorite Photographers`
  - Source URL: `http://www.kriskrug.com:80/2005/05/24/photographers/`
  - Wayback URL recorded in source frontmatter.
- `content/archives/kriskrug-com-blog/2005/2005-10-28-yvr-lhr-lgw-edi-lhr-yvr.md`
  - Title: `Breaking The Curse`
  - Source URL: `http://www.kriskrug.com/2005/10/28/yvr-lhr-lgw-edi-lhr-yvr/`
  - Wayback URL recorded in source frontmatter.
- Quotes in `post.md` were checked verbatim against these files.

### S4. Current Kris voice rules

- `/Users/kk/Code/kk-voice/VOICE.md`
- `/Users/kk/Code/kk-voice/anti-glossary.md`
- Supports the voice formula, the ban on em dashes, and the instruction not to sanitize authentic informal profanity.

### S5. Current Dark Crystal checker

- Repository: `/Users/kk/Code/dark-crystal`
- Current fetched `origin/main` on 2026-07-22: `c3b1d460b08fb46ae576ac472cdfb5d3f02920e2`.
- `tools/voicecheck/voicecheck.py` parses the Markdown rule files deterministically.
- Parsed rule count: 97 total, 74 banned terms and 23 regex rules.
- The source and vendored anti-glossary files had the same SHA-256 at verification: `b8c4b6e7b88e56dff6a5a5740d4a535783a27b4b0d2d763a021a58de63fcc57c`.
- This supersedes the artifact's live-gap claim. The older 54-versus-97 gap is described in the draft as a finding that has since been fixed.

## Aggregate metrics used from the artifact

| Measure | Classic Blogger | Kris typing | Sent as Kris, AI-assisted | Machine-Kris, unedited |
| --- | ---: | ---: | ---: | ---: |
| Slop score | 2 | 2 | 1 | 12 |
| Flags per 1,000 words | 1.66 | 1.11 | 0.77 | 8.86 |
| Em dashes per 1,000 | 0.86 | 0.74 | 0.00 | 8.20 |
| Profanity per 1,000 | 0.43 | 5.53 | 0.77 | 0.95 |
| “I” per 1,000 | 15.66 | 27.77 | 3.83 | 8.20 |

The public draft rounds these rates to one decimal place. The final publish pass should attach or regenerate the derived machine-readable score export.

## Numeric drift found in the artifact

The current visible artifact mixes values from more than one analysis iteration:

- Classic corpus size appears as 159,294 words in the scorecard, 156,699 words in Method, and 147,893 words in the canonical archive record.
- Recent typed Kris appears as 8,139 words in the scorecard and 8,004 words in the surrounding narrative.
- AI-assisted sent writing appears as two documents and 1,307 words in one place, then three documents and 1,611 words in the limitation note.
- Machine-Kris appears as 10,494 words in the scorecard and 10,471 words in Method.
- The archive's `dc-analysis-pack/README.md` currently says 234 longform posts, while the parent archive README says 222. The public draft does not use either count.

The article deliberately omits the conflicting modern-corpus word totals. The rate table remains gated on regenerating its score export from named inputs.

## Quote and privacy ledger

- The two 2005 excerpts are public archived Kris writing.
- The two short profanity excerpts are Kris's own typed words and are labeled in the artifact as published with permission. Treat that artifact approval as prior context, not final publish authorization. Kris should confirm them again at the article review gate.
- No raw working-session corpus, filenames, paths, or third-party content is included in the article.
- All Exhibit C pastiche is omitted from the article except for aggregate scores and the disclosure that all three registers were model-generated.

## Claim status

| Claim | Status |
| --- | --- |
| Archive recovery and canonical corpus counts | Verified from committed primary source |
| 2005 quotations | Verified verbatim from committed primary source |
| Current Dark Crystal rule count and file parity | Verified from fetched current source |
| Comparative score and rate table | Supported by artifact, raw export still required for reproducible publication |
| Authorship conclusion | Editorial inference from the experiment and its retractions |
| Profanity and first-person as future signals | Suggestive only, explicitly register-confounded |
