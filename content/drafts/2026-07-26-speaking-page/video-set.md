# Talk video set: Speaking page (#636)

**Mode:** DRAFT ONLY. Curation gate for KK. No page 1887 writes, no embed markup, no media-library uploads from this lane.
**Target:** WP page `1887`, slug `speaking`, https://kriskrug.co/speaking/
**Parent:** #419 (acceptance: "at least 2 embedded or linked talk videos")

## Verification method and date

**All URLs re-verified live on 2026-08-02.** The prior check was 2026-07-26 and was HTTP-status only, which cannot tell you whether a video went unlisted or lost embed permission. This pass used two independent checks per video:

1. `https://www.youtube.com/oembed?url=...&format=json` for reachability and canonical title.
2. `yt-dlp --skip-download --dump-json` for the two fields that actually matter on a booking page: `availability` (public / unlisted / private) and `playable_in_embed`.

**Result: 15 of 15 candidate videos are `availability: public` and `playable_in_embed: True`. Nothing in the July research is dead, private, or unlisted.** Zero dropped for availability. The drops below are editorial calls, not link rot.

## Final ordered set for the page

Three videos. Order is deliberate: outside validation first, signature framework second, short practical keynote third.

### 1. CreativeMornings Vancouver

| Field | Value |
|---|---|
| Canonical URL | https://www.youtube.com/watch?v=hYT-hsml_ds |
| Platform | YouTube, channel `CreativeMornings HQ` (`@Creativemornings`) |
| Title as it should read | Kris Krüg: The perils and parallels of AI's future |
| Event | CreativeMornings Vancouver, Punk Rock AI, Vancouver Art Gallery |
| Event date | 2026-05-01 (uploaded 2026-07-08) |
| Duration | 52:55 |
| Status | Public, embeddable, verified 2026-08-02 |
| Poster frame | Use YouTube's native poster. See the poster-frame note below. |

**Pull quote** (00:30:44): "If the most critical, the most skeptical people out there, I encourage you to roll up your sleeves, learn the vocabulary, and command a seat at the table of the future."

**Why first.** This is the only video in the bank produced and published by an outside organization with a name a booking committee already recognizes. Everything else on this list is either KK's own upload or his own community. A buyer scanning the page needs one piece of proof that somebody else put him on their stage and their channel, and this is it.

### 2. LaSalle College Vancouver

| Field | Value |
|---|---|
| Canonical URL | https://www.youtube.com/watch?v=-c7mgY2aSgM |
| Platform | YouTube, channel `Kris Krüg` (`@feelmoreplants`) |
| Title as it should read | Both Hands Full: What Creatives Actually Need to Know About AI |
| Event | LaSalle College Vancouver |
| Event date | **Unconfirmed, see flag below.** Uploaded 2026-03-05. |
| Duration | 1:19:34 |
| Status | Public, embeddable, verified 2026-08-02. License: Creative Commons Attribution (reuse allowed) |
| Poster frame | `https://i0.wp.com/kriskrug.co/wp-content/uploads/2026/05/kk-laSalle-both-hands-full-25-scaled.jpg` (owned WP media, HTTP 200 verified 2026-08-02) |

**Pull quote** (00:03:57): "AI is trained on the stolen work of mankind without consent, and I'm more creative, productive, and more powerful than I've ever been in my whole life. Both of these things are true."

**Why second.** It is the signature framework, it has its own portal at bothhandsfull.com, and it is the only talk on the list where owned stage photography from the same event already lives in the WP media library. That makes it the one video whose poster frame can be a real photo of KK on that stage rather than a YouTube grab. It is also on KK's own channel under CC-BY, so nothing about it can be pulled out from under the page.

### 3. ChannelNEXT25 Central

| Field | Value |
|---|---|
| Canonical URL | https://www.youtube.com/watch?v=1OcC-0X6Nb8 |
| Platform | YouTube, channel `Kris Krüg` (`@feelmoreplants`) |
| Title as it should read | The Future of Humanity: AI Keynote on Chaos & Creativity |
| Event | ChannelNEXT25 Central, Fallsview Casino Resort, Niagara Falls, ON |
| Event date | 2025-06-03 (uploaded 2025-06-05) |
| Duration | 33:26 |
| Status | Public, embeddable, verified 2026-08-02. License: Creative Commons Attribution (reuse allowed) |
| Poster frame | `content/source-packs/keynotes-2026/video-research/thumbnails/channel-next.jpg` (KK's own upload, so the thumbnail is his to use) |

**Pull quote** (00:01:53): "If there's a correct and right verifiable answer that you produce for your job, you better watch out, because those are the jobs AI is coming for first."

**Why third.** Shortest full keynote in the set and the only one shot for a straight corporate trade audience. It is the sample a procurement-side buyer will actually finish. **Carries an open KK decision, see the profanity flag below.**

## Approved swap

**Bass Coast Festival, Brain Stage** is the sanctioned substitute if KK wants to drop or replace #3.

| Field | Value |
|---|---|
| Canonical URL | https://www.youtube.com/watch?v=owtSPcpRinI |
| Title | Dear AI, Before We Go Any Further... We Need To Talk About Your Soul |
| Event | Bass Coast Festival 2025, Brain Stage workshop, Merritt, BC |
| Event date | 2025-07-11 (uploaded 2025-07-26) |
| Duration | 40:07 |
| Status | Public, embeddable, verified 2026-08-02. License: Creative Commons Attribution (reuse allowed) |
| Poster frame | `content/source-packs/keynotes-2026/video-research/thumbnails/bass-coast-brain-stage.jpg` |

**Pull quote** (00:00:00): "Dear AI, we're not here to stop you. We're here to guide you, to dance with you, to hold you accountable, and to ensure that whatever world we co-create is more human, more just, and more alive."

It shows range past the conference-room booking and it opens on the single best line in the whole bank. Its captions also look human-made rather than auto-generated, so that quote is the most trustworthy of any here.

## Hold: verified public, deliberately not on the page

| Video | URL | Duration | Verified 2026-08-02 | Why held |
|---|---|---|---|---|
| Whistler Institute | https://www.youtube.com/watch?v=-XEsqsEbpoo | 1:33:31 | Public, embeddable | Longest item in the bank and it plays as an ecosystem conversation, not a keynote. Weak "hire this speaker" signal per minute. |
| Vancouver AI Meetup, March 2026 | https://www.youtube.com/watch?v=T5ANAthZewE | 32:43 | Public, embeddable | Good talk, but it is KK's own meetup on KK's own community channel, so as evidence it is circular. 42 views. Also note the real title carries a suffix the July research dropped, see title-drift flag. |
| Horizons, Compass Datacenters (3 clips) | `EBGdM6T9Fr8` 1:09, `pfecN8_1boA` 1:28, `tfXkDhlqnrE` 1:36 | 1 to 2 min each | All three public, embeddable | Produced vendor interview snippets, not stage footage. The series page https://horizons.compassdatacenters.com/... is HTTP 200. Link-out only if a "seen elsewhere" row ever gets built. |

## Dropped from the page

**STORYHIVE On Location: Victoria** (https://www.youtube.com/watch?v=sxDwQRTZfCA, 1:19:50). Public and embeddable as of 2026-08-02, so this is not link rot. Dropped because it is a recorded livestream (`was_live: True`) of a produced interview rather than a talk, it sits on a third-party channel (`Haus of Owl`), and its actual YouTube title is `STORYHIVE On Location: Victoria Kris Krug-LS`. That trailing `-LS` is an internal production tag. Putting a title with a production tag in it on a booking page looks careless, and per the #636 accuracy rule we do not get to quietly rewrite it into something tidier. Keep it in the archive.

## Legacy trio: ruled OUT for the page

The call is **archive only, not page-worthy**. All were re-verified live and all are still public and embeddable, so this is an editorial decision and not a dead-link cleanup.

| Video | URL | Duration | Verified 2026-08-02 |
|---|---|---|---|
| Social Media Camp Victoria keynote (original, `Social Media Camp` channel, 986 views) | https://www.youtube.com/watch?v=5mSbRt8GXYc | 50:10 | Public, embeddable |
| Social Media Camp keynote (KK's own 2021 re-upload, 78 views) | https://www.youtube.com/watch?v=2cH8ICaDm4k | 49:07 | Public, embeddable |
| Pecha Kucha Vancouver, "Open Everything" | https://www.youtube.com/watch?v=QofZEGjFNwc | 7:56 | Public, embeddable |
| TEDxOilSpill, CBC segment "Oil Spill Photographs" | https://www.youtube.com/watch?v=1yQ6t1bG-Ko | 1:57 | Public, embeddable |

**Reasoning.** The page sells AI keynotes in 2026. A 2009 Pecha Kucha and a 2012 social-media keynote prove longevity, but they also date the page and pull the buyer's eye toward work that is two technology cycles old. The TEDxOilSpill item is worse for this purpose: it is a 1:57 CBC news segment *about* KK's photography, not a talk he gave, so it cannot count toward "talk videos" at all.

Two notes if KK ever overrules this: use the **2021 re-upload** (`2cH8ICaDm4k`) rather than the original, because that one is on his own channel and he controls it. And a bonus find from the same sweep, Island Futures Conference 2012 (https://www.youtube.com/watch?v=qI0onxdP-xA, 11:54, public, embeddable), which is not currently tracked in the speaking-page material at all.

## Flags for KK

### 1. ChannelNEXT opens on an expletive at 00:00:01

The literal first words of video #3 are "I'm watching a [expletive] blood bath out there." A buyer who clicks play on a booking page hears that before anything else. This is on-brand and it is also a real risk with a conservative corporate or institutional client. Three options, KK picks:

- Leave it. It is the punk-rock positioning, and the people it filters out were never the right booking.
- Start the embed at a timestamp offset so the video opens after the cold open.
- Swap #3 for Bass Coast, which is already prepped above.

The same line appears in the CreativeMornings talk at 00:17:55 and in Bass Coast at 00:00:42, but in neither case is it the opening frame, so it only needs a decision for #3.

### 2. LaSalle event date does not reconcile

The kk-kb appearance record `2026-01-14-lasalle-college-vancouver-keynote.md` is dated 2026-01-14, is described as an alumni talk, and carries the talk title "How are creatives working with AI?". The repo source-pack slug for this video is `lasalle-college-graduation`, and the YouTube title is "Both Hands Full: What Creatives Actually Need to Know About AI". The video was uploaded 2026-03-05 and opens with "I'm here to talk to you tonight". Those may be the same night or two different LaSalle appearances. Nothing in either repo links the video ID to the appearance record. **Do not print an event date for this video on the page until KK confirms it.** The upload date is verified fact; the event date is not.

### 3. Title drift in the July research

Two titles in `content/source-packs/keynotes-2026/video-research/README.md` and `multimedia-rebuild-plan.md` do not match what YouTube actually returns today:

- Vancouver AI: the real title ends with `| Vancouver AI Meetup March 2026`. The research dropped that suffix.
- STORYHIVE: the research shows a tidied title. The real one is `STORYHIVE On Location: Victoria Kris Krug-LS`.

Neither is on the final page set, so nothing downstream breaks, but the embeds lane should pull titles from oEmbed at build time rather than copying them out of the July docs.

### 4. Poster frame for CreativeMornings is a genuine gap

There is no owned CreativeMornings stage still in the WP media library. `kk-cmvan-keynote-header.png` is verified HTTP 200 but it is promo artwork, not a photo of KK on that stage. Event photography from that morning exists at punkrockai.com/photos/michelle-diamond, but it is Michelle Diamond's work and the kk-kb rights record requires a "Photography by Michelle Diamond" credit, so it cannot be quietly lifted into the media library by this or any other lane.

Recommendation: let the CreativeMornings embed use YouTube's own poster. It requires no import and carries no rights question. If KK wants a real stage still there, that is a licensing conversation with Michelle Diamond first.

### 5. Rights and embed permission, summarized honestly

- **Clean, KK-controlled:** LaSalle, ChannelNEXT, Bass Coast, Whistler. All on `@feelmoreplants`. The first three are published under Creative Commons Attribution (reuse allowed), confirmed in the live metadata today.
- **Third-party channel, embedding sanctioned but not owned:** CreativeMornings, Vancouver AI, Haus of Owl, Compass Datacenters. `playable_in_embed: True` means YouTube permits the embed, which is the sanctioned mechanism, and that is the extent of what it means. It is not a content license. Do not download, re-cut, or re-upload any of these, and do not import their thumbnails into the media library.
- **CreativeMornings carries a live credit requirement.** Per `content/media/talks/2026-05-01-creativemornings-vancouver/rights-and-credits.md`, the required credit is "Originally presented at CreativeMornings Vancouver" with links to the official feature and recording. The embeds lane needs to carry that.
- **One moving part.** That same kk-kb record has `personal_upload_url: null`, `personal_upload_status: pending`, tracking issue 2530. If KK later posts his own cut of the CreativeMornings talk, the canonical URL on the page may need to change. Flagged so the page lane is not surprised.

### 6. No sizzle reel exists. Do not fake one.

`~/Code/kk-kb/content/people/kris-krug/site-export/speaking.md` line 80 has a placeholder under "Watch a talk" reading, in effect, "60 to 90 second reel, coming soon". No such reel exists anywhere in either repo. This is the single highest-leverage missing asset on the whole Speaking page: a booking buyer will watch 90 seconds long before they commit to 52 minutes.

**Recorded as a known gap for KK.** No lane should synthesize one from the existing footage without KK's explicit sign-off, both because the CC-BY talks and the third-party talks have different reuse terms, and because a reel is a positioning decision, not a production task.

### 7. Pull quotes came from captions and need an ear-check

Every quote above carries a real timestamp and is genuinely in the source. But the CreativeMornings, LaSalle, and ChannelNEXT quotes come from YouTube auto-captions, which are demonstrably lossy in these files: they render "Kris Krüg" as "Chris Krug" throughout, and they mangle "Buolamwini" and several other proper nouns. I lightly repaired punctuation and dropped filler for readability. **KK or the embeds lane should ear-check any quote against the audio at its timestamp before it goes on the page.** The Bass Coast quote is the most reliable of the set because that file appears to be human-captioned.

## Facts vs inference

**Verified fact,** checked live 2026-08-02 by oEmbed plus `yt-dlp --dump-json`: every URL, platform, channel, upload date, duration, `availability: public`, `playable_in_embed: True`, and the three Creative Commons licenses. Also HTTP 200 on the four owned WP media stage photos and on the Horizons series page. Also the caption timestamps for every pull quote.

**Sourced from repo records, not independently re-verified:** the event dates and venues for CreativeMornings, ChannelNEXT, Bass Coast, and Whistler, all read from kk-kb appearance frontmatter. The CreativeMornings credit requirement, read from the kk-kb rights record.

**My inference, open to KK overruling:** the ordering rationale, the hold and drop calls, the legacy-trio ruling, and the read that the ChannelNEXT cold open is a booking risk worth a decision.

**Explicitly not established:** the LaSalle event date.

## Handoff

Page-architecture and embeds lanes own everything downstream. Two things they should not have to rediscover: pull live titles from oEmbed at build time rather than from the July docs, and carry the CreativeMornings credit line. Acceptance for #419 is met at two videos; this set proposes three, with a fourth prepped as a swap.
