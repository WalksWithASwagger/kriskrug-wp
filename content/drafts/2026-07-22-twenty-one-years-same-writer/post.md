---
title: "Twenty-One Years, and I Write Exactly the Same"
slug: twenty-one-years-same-writer
post_date: '2026-07-22'
status: draft
post_type: post
author_wp_id: 1
categories:
- AI Ethics & Philosophy
tags:
- AI Writing
- Authorship
- Digital Archives
- Creative Process
- Artificial Intelligence
featured: false
excerpt: "I scored 1,274 recovered blog posts against the words I type today. The surprising result was not that AI sounds different. It was that a voice checker can catch an unedited machine, but cannot prove a human was ever there."
source_manifest: source-manifest.md
styled_payload: post.html
---

# Twenty-One Years, and I Write Exactly the Same

## What 1,274 recovered blog posts taught me about AI voice, authorship, and the limits of a clean score

We recovered 1,274 posts from my old blog, written between 2003 and 2017, from the Wayback Machine. Then we measured the useful part of that archive against the words I type today and the words machines write under my name.

The first result was almost too neat.

2005 Kris scored **2** on my anti-slop scale. 2026 Kris, typing unguarded to his agents, also scored **2**.

Then an AI-assisted newsletter that went out under my name scored **1**.

The machine was cleaner than I was.

That is not a compliment to the machine. It is a failure of the instrument, and it became the most useful finding in the whole experiment.

Two things in the first analysis were wrong. I am leaving both in the record because how the study broke taught me more than the clean result did.

1. A finding about sentence rhythm turned out to be a statistics error.
2. A supposedly hand-written 2026 corpus turned out to be mostly AI words after all.

The experiment did not prove that a detector can find the human. It proved something narrower and stranger:

> A voice checker can catch a machine that nobody edited. It cannot tell you whether a person was ever there.

## Exhibit A: The experiment that broke

The knowledge base held an agent's draft of a Vancouver AI newsletter. Beehiiv held the version that actually went out. Same event. Nearly the same length. Very different scores.

| Version | Slop score | Flags | Em dashes |
| --- | ---: | ---: | ---: |
| Agent draft, unsent | 20 | 10 | 10 |
| Version that shipped | 0 | 0 | 0 |

I first read this as a human beating a machine.

Then I corrected the provenance. The sent version was mostly AI words too. A person had selected, rewritten, cut, and scrubbed them, but this was not a clean human-versus-machine comparison.

It was an **edited-versus-unedited** comparison.

That distinction matters. The checker caught the model when nobody had bothered to fight it. The moment someone did the editorial work, the score dropped to zero, the same result the checker gives some of my real writing.

The em dash still separated the two drafts cleanly, ten against zero. It remains a useful check because I almost never reach for one and models love the damn thing. But it catches an unedited model. It does not prove authorship.

## Exhibit B: Four corpora and one awkward ruler

The analysis used the same offline, deterministic checker across four writing sets:

- **Classic Blogger:** pre-AI posts I published from 2003 to 2017.
- **Kris typing:** my own user turns in working sessions with agents, separated structurally from model output.
- **Sent as Kris:** AI-assisted newsletters that went out under my name.
- **Machine-Kris:** unedited model output filed under my name.

The checker reads a 97-rule anti-glossary. No model judges the writing. No API call decides whether I sound like myself.

| Measure | Classic Blogger | Kris typing | Sent as Kris, AI-assisted | Machine-Kris, unedited |
| --- | ---: | ---: | ---: | ---: |
| Slop score | **2** | **2** | **1** | **12** |
| Flags per 1,000 words | 1.7 | 1.1 | 0.8 | 8.9 |
| Em dashes per 1,000 | 0.9 | 0.7 | 0.0 | 8.2 |
| Profanity per 1,000 | 0.4 | 5.5 | 0.8 | 1.0 |
| “I” per 1,000 | 15.7 | 27.8 | 3.8 | 8.2 |

Read the first row twice.

A blog written in 2005 and prompts typed in 2026 land on the same slop score, from the same person, in two registers that could hardly be less alike. Then the AI-assisted newsletter scores even better.

The detector is inverted at the clean end. It rates the machine's polished prose as more authentically me than me, because real writing occasionally reaches for an awkward phrase, an unfashionable word, or a sentence that falls over.

A tool that punishes a writer for his own imperfections and rewards a model for having none cannot find the human. It finds the tidy.

## Two tells worth testing

Once we had a recent corpus I could actually vouch for, two gaps opened up that the anti-glossary did not measure.

### I swear more than the machine

In my unguarded working messages, profanity appeared about 5.5 times per 1,000 words. Machine-Kris landed around 1.0. The AI-assisted newsletters came in around 0.8.

That direction matches my own voice guide: profanity is authentic in informal writing, so do not sanitize it out.

The machine sanitizes it out.

Real me, typing to an agent:

> “come up with 10 fucking way better ones”

> “Yeah, but make them fucking hilarious or funny or scathing.”

Set that beside a polished line that went to the mailing list under my name:

> “We need better conversations. We need stranger experiments.”

Both are mine in the loose sense that I approved the output. Only one is me in the documentary sense that I typed the words.

### I say “I.” The machine hides in “we.”

My working messages used “I” about 27.8 times per 1,000 words. Machine-Kris used it 8.2 times. The sent AI-assisted writing used it 3.8 times.

That is a sevenfold gap at both ends, and it is interesting. It is not proof.

Prompts to an agent are naturally first-person and imperative. A newsletter often speaks as “we.” The registers are different, so profanity and first-person language need to be tested against matched kinds of writing before they become gates.

This is where the project kept trying to teach the same lesson: a large difference can still have a boring explanation.

## The rhythm finding was wrong

The first version of the analysis claimed the sharpest tell was sentence-length spread. The story was seductive: real Kris varies rhythm wildly, while the machine flattens language into a hum.

The numbers were real. The interpretation was wrong.

The calculation had pooled hundreds of documents into one long string. That measured variation **between** 851 different blog posts, not rhythm **within** any one post. When measured per document, the effect collapsed and partly reversed.

A cadence gate built on that result would have flagged some of my own writing as robotic.

So the cadence claim is withdrawn.

This is not a footnote to hide. It is the point. A number can be reproducible and still mean nothing. If a clean chart cannot survive a second question, the chart goes, not the question.

## Exhibit C: The machine can pass the gate when you teach it the gate

We also generated five pieces in three different registers: Classic Blogger, Kris-Now, and generic Machine-Kris. Every passage was generated pastiche. None of it was real Kris writing.

The two Kris registers averaged a slop score of **0**. Machine-Kris averaged **38** and used thirteen em dashes.

That result does not mean the model failed to imitate me. It means the model was given two different jobs.

When told to write like a generic smart internet person, it produced portentous endings, empty tension, and phrases that could belong to anybody. When given concrete voice constraints and real examples, it cleared the gate completely.

The gate was not measuring whether a human wrote something. It was measuring whether anyone tried.

## Exhibit D: The genuine article is messier

The archive gives us something rare: writing that is provably pre-AI because of its date.

Here is me in 2005, unedited:

> “Nearly every time I go out to shoot I’m confronted with the cold hard fact that I don’t know a damn thing about photography. One day recently I realized the only ‘famous’ photographer whose work I could name and was more than superficially familiar with was Ansel Adams.”

[*My New Favorite Photographers*, 24 May 2005](https://web.archive.org/web/20080418131940/http://www.kriskrug.com:80/2005/05/24/photographers/)

And again, before leaving North America for the first time:

> “Tomorrow I’m finally going to break the curse and leave North America. I’m 28 years old have traveled lots and lots around the States and Canada but have never left the continent.”

[*Breaking The Curse*, 28 October 2005](https://web.archive.org/web/20080516094738/http://www.kriskrug.com/2005/10/28/yvr-lhr-lgw-edi-lhr-yvr/)

Missing commas. A run-on. “Lil” shows up two sentences later. The technically correct move would be to fix it.

The technically correct move would also remove evidence.

The old writing is not better because it is rough. It is valuable because nobody can plausibly claim a language model wrote it. In 2026, that kind of provenance is becoming a rare and appreciating asset.

The archive is an excellent style source and a terrible knowledge source. Twenty-year-old me will state things I no longer believe with total confidence. Train voice on it. Never train facts on it.

## What changed because of this

### 1. Record provenance when the words are made

Both big errors were provenance errors. We could not tell from the finished artifact who had written it. We had to ask, and the answer overturned the result.

No score can repair missing authorship history after the fact. If the difference matters, record who typed, generated, edited, and approved the words while those events are happening.

### 2. Keep the checker, but name its job correctly

The anti-slop gate is useful. It catches lazy output, repeated model habits, banned language, and the em dash infestation. It makes the work better.

It is a lint tool, not an authorship detector.

The first analysis also found that Dark Crystal was scoring against an older 54-rule copy of the anti-glossary while the source had 97 rules. That gap has since been fixed in the current code. The source and vendored copies are now byte-for-byte identical, and the checker loads all 97 rules.

That is exactly what an audit should do: find the boring operational bug and get it fixed.

### 3. Preserve the ugly parts

Typos, odd phrasing, profanity, abandoned sentences, and a person changing his mind are not defects to sprinkle into generated prose as decoration.

They are consequences of a real process.

Synthetic imperfection is still synthetic. The useful move is not to tell a model to make three typos. It is to keep enough of the human process visible that everything does not get polished into the same tasteful grey paste.

### 4. Keep the retractions on the page

The cadence claim was wrong. The “hand-written” corpus was not hand-written. Leaving those failures visible makes the final claim smaller and stronger.

The finding that survived is not that I beat the machine. It is that a machine can score better than I do once somebody edits it hard enough.

That is funny, useful, and a little alarming.

## A checker can remove the slop. It cannot add a person.

I started this project hoping to measure the distance between my old voice, my current voice, and the machines that write beside me.

The archive did show continuity. Twenty-one years apart, across a blog and a command line, I still score like me.

But the bigger result is about the instrument.

A checker can remove banned words. It can catch lazy cadence. It can stop the model from throwing an em dash every 122 words. It can make an AI draft less annoying.

It cannot prove authorship. It cannot recover provenance. It cannot tell you whether a person was ever there.

If your content system cannot answer **who wrote this, who changed it, and who stands behind it**, before the score appears, you do not have a voice system yet.

You have lint.

And lint does not get a byline.

## Related

- [Both Hands Full](https://kriskrug.co/2026/01/24/both-hands-full/)
- [Punk Rock AI](https://kriskrug.co/2026/05/04/punk-rock-ai/)
