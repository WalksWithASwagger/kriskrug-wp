---
title: AI Won't Fix Your Broken Permit Process
slug: ai-wont-fix-your-broken-permit-process
post_date: '2026-05-24'
status: draft
post_type: post
author_wp_id: 1
categories:
- AI Ethics & Philosophy
tags:
- AI Governance
- Civic Tech
- Government AI
- Public Sector
- Responsible AI
featured: false
excerpt: AI will not repair broken civic systems by itself. Permit reform needs better process, public accountability, and human judgment before automation can help.
seo:
  meta_title: AI Won't Fix Your Broken Permit Process | Kris Krüg
  meta_description: AI will not repair broken civic systems by itself. Permit reform needs better process, public accountability, and human judgment before automation can help.
notion_source:
  page_id: 2e3c6f79-9a33-808c-a0cb-c37539a8fb4e
  fetched: '2026-05-24T21:14:17.000959+00:00'
---

## ***But Here's What It Can Actually Do***

There's a pitch deck making the rounds in every provincial capital right now. It has the same slides. An AI company, usually based somewhere far from here, promising to "magically fix government services" and "promise impossible efficiency." The demo is slick. The timeline is aggressive. The ROI projections have the confidence of a racetrack tout with a laser pointer.

I've seen this movie before. And I'm tired of watching government officials buy tickets to it.

Let me be clear about where I'm coming from. I run the BC AI Ecosystem Association. We've built the largest grassroots AI community in Western Canada. We train people in AI tools every day. I vibe code something almost every morning. I believe in this technology deeply.

And precisely because I believe in it, I'm going to tell you where it works, where it doesn't, and why most government AI projects are set up to fail before they start.

## **The Three-Headed Problem Nobody Wants to Name**

When people talk about AI for government services, particularly permitting and regulatory work, they usually frame it as one type of problem. The rules are complex, so let's use AI to interpret them. The data is messy, so let's use AI to clean it up. The process is slow, so let's use AI to speed it up.

Here's the thing. It's all three. And pretending it's just one is how you end up with a $20 million project that makes things worse.

Permitting, licensing, regulatory approvals. These are fundamentally **coordination problems** that manifest as rules interpretation and data quality issues. The rules are written. They're not mysterious. What's broken is that different departments interpret them differently, the data lives in seventeen systems that don't talk to each other, and the applicant has no visibility into where their file is stuck or why.

I've been in rooms with municipal staff in Vancouver and Surrey. I've heard the frustration. Someone submits a permit application, it bounces between three departments over six months, and when it finally gets rejected, the reason is something that could have been caught on day one. That's not a knowledge problem. That's a communication problem wearing a bureaucratic disguise.

AI doesn't fix institutional dysfunction. It amplifies whatever's already there. If your process is a mess, AI gives you a faster mess. If your departments don't coordinate, AI won't magically make them start. If your data is scattered across incompatible systems, AI will just hallucinate connections that don't exist.

You have to diagnose before you prescribe. And most AI vendors skip the diagnosis entirely.

## **Where AI Actually Delivers Value**

Okay, so I've told you what doesn't work. Let me tell you what does.

There are specific, bounded tasks where current AI systems can genuinely help government operations. These aren't the flashy demos. They're not going to get you on the cover of a tech magazine. But they're real, they're reliable, and they can save significant time for both staff and applicants.

**Pre-submission completeness checks.** Before an application even enters the queue, AI can scan it against requirements and flag what's missing, what's in the wrong format, what additional documents are needed. This is pattern matching against a checklist. LLMs do this reliably. It catches the obvious errors that currently clog up staff time for weeks before someone sends an email saying "you forgot to attach page 3."

**Document summarization.** A complex development application might include a 200-page environmental assessment, traffic studies, engineering reports. AI can pull out the key compliance points and present them in a digestible format for reviewers. That's hours saved. That's a reviewer who can focus on judgment calls instead of hunting through PDFs.

**Cross-referencing against regulations.** "Based on the zoning code, this application appears to require a variance for setback." Note the word "appears." The AI is flagging, not deciding. It's saying "hey, you might want to look at this." That's useful. That's appropriate scope.

The common thread here: AI is most reliable when the task has a clear right answer that exists in the source documents. When you're asking "is this document attached?" or "what does section 4.2 say about setbacks?" the AI can answer that. When you're asking "is this development appropriate for this neighborhood?" you've crossed into judgment territory. That's not an AI question. That's a human question, often a political one, and pretending otherwise is dangerous.

## **Where It Gets Dangerous**

Let me name three areas where deploying AI without strong human oversight is asking for trouble.

**Discretionary decisions.** Anything involving competing interests, value judgments, or interpreting "community standards." Does this building fit the neighborhood character? Is this business use compatible with the residential feel of the area? Is "adequate" parking actually adequate? These words are doing political work. They're encoding decades of community negotiation and compromise into bylaw language. An AI doesn't know that. It sees patterns. It doesn't understand context. Keep humans in the loop for anything discretionary. Full stop.

**Edge cases and novel situations.** LLMs are trained on what exists. They're pattern matchers. If someone submits an application for something genuinely new, a building type that doesn't fit existing categories, a use case nobody anticipated, the AI will confidently give you an answer based on the nearest pattern match. That confidence is the dangerous part. It doesn't know what it doesn't know. When the situation is novel, you need human judgment. The AI should flag "I haven't seen something like this before" not invent an answer.

**Anything with equity implications.** This is the one that keeps me up at night. Who gets approved. Who gets rejected. Whose application moves fast. Whose gets buried. If historical data shows certain neighborhoods or certain types of applicants got rejected more often, the AI might learn that pattern as "normal." It encodes the bias and calls it optimization. You need human oversight specifically watching for this. And you need to measure it, not just hope for the best. Hope is not a strategy in regulated environments.

The rule I'd advocate for: **AI should never be the last word on anything that affects someone's property rights, livelihood, or access to services.** Flag, summarize, recommend. But a human signs off. Every single time.

## **What Trust Actually Looks Like**

Here's where most government AI projects go wrong. They focus on the technology and skip the governance. The AI is actually the easy part. The hard part is building systems that are trustworthy in regulated environments.

If someone pitched me an AI system for government services, here's what I'd demand before I'd trust it:

**Show me accuracy metrics against ground truth.** Not "we tested it on 10 applications and it seemed good." Precision and recall on a meaningful sample. How often does it flag something that's actually fine? How often does it miss something that's actually wrong? Both matter. False positives waste staff time. False negatives let problems through. Quantify it or you're not ready.

**Show me citations to source.** Every flag, every recommendation, needs to point to the specific rule, bylaw, or requirement it's referencing. "This may violate Section 4.2.3" not "this seems non-compliant." If the AI can't show its work, don't trust it. Traceability isn't optional in regulated environments.

**Show me confidence bounds.** The system needs to know what it doesn't know. "High confidence: missing required document" is different from "Moderate confidence: possible issue, recommend human review." If everything comes back with the same confidence level, the calibration is broken. You can't triage effectively if everything looks the same.

**Show me how it handles edge cases.** What happens when someone submits something weird? What happens when someone tries to game the system? Does it fail gracefully or does it confidently make things up? Test the boundaries explicitly. The failure modes matter more than the success cases.

**Show me the audit trail.** Every AI interaction needs to be logged, reversible, and overridable by a human. If a reviewer disagrees with the AI, that needs to be captured and used to improve the system. The disagreements are your learning opportunities.

**Show me the equity auditing.** Before deployment and ongoing. Does this system treat applications from different neighborhoods, demographics, or applicant types equitably? If you're not measuring it, you're not managing it.

Most of what I just described isn't even AI-specific. It's what you'd want from any decision-support system in a regulated environment. The technology is the easy part. Governance is hard. And governance is where projects fail.

## **Community-Driven, Not Top-Down**

Here's where BC has an opportunity to do something different.

Most government AI initiatives start with a vendor demo and work backwards. Someone in procurement sees a slick presentation, gets excited, and suddenly there's a pilot project. The community the system is supposed to serve? They find out about it when it's already built.

We're advocating for something different. Community-driven AI development means starting with the people who actually interact with government services, both staff and applicants, and asking: what's actually broken here? What would actually help? Is AI even the right tool, or would a better form or clearer guidelines solve this faster?

At BC AI, we've been building a Government Relations Committee. Fifteen members, including people with federal political experience, policy backgrounds, and direct connections to municipal decision-makers. We're not just talking about AI governance. We're actively engaging with policymakers at municipal, provincial, and federal levels to bring a community voice to these conversations.

We're also the only AI community I know of that integrates Indigenous leadership into our governance. Coast Salish ceremony opens our events. UNDRIP alignment guides our policy positions. Carol Ann Hilton sits on our board. This isn't tokenism. It's structural commitment. When we talk about AI governance, we're bringing perspectives that corporate vendors simply don't have.

The question isn't "how can government use AI?" The question is "what's actually broken in this process, and would AI help or just add complexity?" Sometimes the answer is a better PDF form. Sometimes it's clearer guidelines. Sometimes it's fixing the coordination problem before you automate anything. And yes, sometimes it's AI. But you have to diagnose before you prescribe.

## **The Flag We're Planting**

Here's where BC + AI stands:

We believe AI can genuinely help government serve people better. Document checks, summarization, pre-submission review, flagging likely issues. These are real use cases that can save time for staff and reduce frustration for applicants.

We believe human oversight is non-negotiable. AI should flag, summarize, and recommend. Humans should decide. Every time.

We believe trust requires measurement. Accuracy metrics, citations, confidence bounds, equity audits. If you can't quantify it, you're not ready for deployment.

We believe community voice matters. The people who use government services should have a say in how those services are automated. Top-down AI adoption without community input is innovation theater.

We believe governance is harder than technology. Most AI projects fail not because the tech didn't work, but because nobody thought through the human systems around it.

And we believe BC has an opportunity to lead. Not by being first to deploy AI in government, but by being first to do it right. Community-driven. Human-centered. Accountable. Measurable.

That's the flag we're planting. If you want to help plant it with us, you know where to find us.

*Kris Krüg is Executive Director of the [BC + AI Ecosystem](https://bc-ai.ca/) Association and founder of [The Upgrade AI](https://www.theupgrade.ai/) Training. He has been building and training AI systems since 2022 and leads Western Canada's largest grassroots AI community.*

## Receipts and next rooms

- [BC + AI](https://bc-ai.ca/) for the community-governance layer.
- [Responsible AI Professional Certification](https://bc-ai.ca/certification/responsible-ai-professional/) for practical governance training.
- [Contact me](https://kriskrug.co/contact/) if your civic AI project needs a sharper diagnosis before the vendor demo eats the room.
