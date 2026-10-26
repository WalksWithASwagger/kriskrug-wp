# Article 3: source-audio audit, October 25, 2026

Nine spoken quotation passages in published post **12800** were checked against fresh source recordings, including the author's Justine transition and both parts of the Israel quotation. This extends the [version reconciliation](article-1027-reconciliation-2026-10-25.md). Two bounded editorial corrections are prepared; no live write has been made. Issue #1027 remains open for the exact author decisions below.

## Method and limits

The connected Plaud app supplied the original recordings for tapes 1, 3 and 5. Audio was downloaded privately, hashed, clipped and independently transcribed locally using whisper.cpp base and small.en without expected-quote prompts. Tape 5 required a successful raw-Opus decode before inspection. The private packet retains original media hashes, clip offsets/hashes, source transcripts, independent outputs, decode receipts and the exact WordPress snapshot.

This is machine-assisted audio verification, not human ear review or biometric speaker identification. Speaker identities are anchored in introductions and conversational context, not machine diarization labels. Most words are supported across the source and independent transcriptions; uncertain filler is explicitly excluded from the proposed replacement.

## Findings

| Passage | Recording offset | Disposition |
|---|---|---|
| Alexis's heavy-backpack remark | Tape 3, 2:16:44–2:17:09 | Supported as Kris's contemporaneous retelling, not a direct recording of Alexis. Preserve that distinction. |
| Dinner remark about being sold to | Tape 1, 0:51:44–0:52:20 | Context places the remark in Martin's account of EPAM sponsorship approaches. The published attribution to Kris should change. |
| Kris's transition to Justine | Tape 3, 0:31:55–0:31:58 | Supported by audio and ensuing interview context. |
| Justine's talent/compute remark | Tape 3, 0:37:54–0:38:18 | Supported. |
| Justine's model/code remark | Tape 3, 0:39:03–0:39:13 | Core wording supported; opening repetitions differ between machine transcriptions. Use the clear final sentence rather than certify the stutter. |
| Edoardo's camera joke | Tape 3, 2:04:15.7–2:04:19.2 | Supported by an independently transcribed bounded clip. The quieter speaker was missed in longer clips. |
| Edoardo's egg-timer joke | Tape 3, 2:17:08–2:17:12 | Supported. Stage introduction and photo/conversation context support the attribution. |
| Israel's changing-human-state remark | Tape 5, 1:14:03–1:14:23 | Supported. |
| Israel's systems-adapting remark | Tape 5, 1:14:03–1:14:23 | Supported, including its introductory sentence. |

The closing rhetorical phrase about who knows the author is not presented as recorded speech and needs no recording match.

## Prepared correction

1. Replace the dinner paragraph's attribution `I told him` with `Martin said`, keeping its quotation unchanged.
2. Replace Justine's model/code quotation paragraph with `"It's an actual code," she said.` This is a conservative excerpt recommendation; variation among ASR outputs does not prove every existing repetition is false.

Fresh authenticated Varlock readback still matches raw content SHA-256 `93d7136388cbcb9bee3ff467ce94f5b7c09a78c9a754a8578665df6d04a5e0e2`, published status, the intended slug and featured media 12804. Candidate hash: `94a41fc5abb434284a0813c91c7101ad836851683d5f39ca5b4607cce55e97fb`.

Comparison confirms only those two paragraphs differ. All seven body images, every link, headings, paragraph count and featured media are preserved. The payload changes content only. Re-fetch and compare the live source hash before any approved application; preserve the full pre-change snapshot as the rollback source.

## Remaining decisions

The recordings establish that Justine agreed to a written interview and Israel agreed after the blog interview was explained. These are supported by the independently transcribed interview openings.

The September 17 review describes its restored quotes as consent-cleared, but an individual clearance receipt was not recovered for Martin's dinner remark, Alexis's reported remark or Edoardo's two informal jokes. The older post-2 clearance predates these conversations and is not extended to them. Missing evidence does not imply an objection. Kris has been asked only to confirm the scope of that existing clearance and approve the prepared two-line live correction. Do not ask speakers, infer consent from diarization, or mark #1027 complete while these decisions remain pending.

Private evidence is under `.generated/current-state/article-1027-audio-2026-10-25/` in the original checkout. The packet includes a readable decision brief, playable excerpts, exact diff, candidate content-only payload, preservation checks and full live snapshot. Original recordings, private transcripts, model binaries and signed download URLs are not committed; temporary download URLs were removed.

The #1090 monitor remains active. The latest Beehiiv check found zero new active subscriptions after the deployment cutoff, so first organic GA4 delivery is still unproven. No synthetic signup or analytics event was created.
