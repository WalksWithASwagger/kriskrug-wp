# Email Onboarding Draft v1 - 2026-06-17

**Issue lane:** child issue #230, split from parent issue #51.
**Status:** Draft-only, repo-safe planning artifact.
**Scope:** Sequence structure, email-by-email purpose, subject options, draft body copy, conceptual trigger/tag map, and required decisions before sending.
**Out of scope:** ESP/CRM setup, contact import, subscriber data handling, form publishing, tracking pixels, automation activation, public launch, and email sending.

## Working Assumptions

- Parent #51 remains the full production email onboarding system.
- Child #230 is satisfied when v1 copy and a non-executing automation map are ready for human review.
- This draft prioritizes one shared lead-magnet nurture sequence because #229 is the active child lane for lead-magnet content.
- The broader parent #51 sequence set remains parked until platform, consent, and audience decisions are made.
- All copy below requires brand, legal/privacy, and deliverability review before use.

## Sequence Structure

### V1 Sequence: Lead Magnet Download

**Use case:** A visitor requests one of the five guides from #229.

**Length:** 7 emails over 21 days.

**Goal:** Deliver the guide, build trust, segment the reader by interest, and invite the right next action without pretending an email sequence is a relationship.

**Cadence:**

| Email | Timing | Purpose |
|---|---:|---|
| 1 | Immediate | Deliver the guide and set expectations. |
| 2 | Day 2 | Share Kris's human-first AI frame and ask for the reader's context. |
| 3 | Day 5 | Offer a practical worksheet or exercise from the guide. |
| 4 | Day 8 | Show applied proof through a story, case study, or field note. |
| 5 | Day 12 | Route by segment and invite a specific next step. |
| 6 | Day 16 | Address skepticism, risk, and trust directly. |
| 7 | Day 21 | Make the clear ask: book, reply, attend, or keep reading. |

### Later Parent #51 Sequences

These remain conceptual until the full parent issue is resumed:

- New subscriber: 5 emails over 14 days.
- Lead magnet download: 7-10 emails over 21-30 days.
- Event attendee: 5 emails over 30 days.
- Workshop inquiry: 7 emails over 14 days.
- Blog subscriber: weekly editorial dispatch.
- Re-engagement: 4 emails to inactive subscribers.

## Email 1: Guide Delivery

**Purpose:** Deliver the requested guide, acknowledge the reader's interest, and set a low-pressure expectation for follow-up.

**Subject options:**

- Your guide is here: {{guide_title}}
- Here is the {{guide_title}} field guide
- Download: {{guide_title}}

**Body copy:**

Hi {{first_name}},

Here is the guide you asked for:

{{guide_download_link}}

I made this for people who want to work with AI without surrendering their judgment, voice, community, or ethics to the tool stack.

Over the next couple of weeks, I will send a few short notes that help you turn the guide into something practical: a conversation with your team, a workshop idea, a safer workflow, or a clearer next decision.

No breathless hype. No fake certainty. Just useful field notes from the messy middle of creative technology, community building, and responsible AI adoption.

Start here: read the first section and write down one AI question your team keeps circling but has not named clearly yet.

Kris

**Primary CTA:** Download the guide

**Secondary CTA:** Reply with the AI question your team is circling.

## Email 2: The Human-First Frame

**Purpose:** Establish Kris's point of view and encourage the reader to define their context.

**Subject options:**

- The better AI question
- Start with people, not tools
- Before you pick a tool

**Body copy:**

Hi {{first_name}},

Most AI conversations start in the wrong place.

People ask: "Which tool should we use?"

The better question is: "What human work are we trying to support, and what would make that work more trustworthy, creative, accessible, or useful?"

That question changes the room.

It moves the conversation away from demos and toward people: staff, artists, students, members, audiences, communities, clients, sources, partners, and the folks who carry the risk when a system goes sideways.

Try this with your guide:

1. Pick one workflow or decision your team cares about.
2. Name the people affected by it.
3. Name one thing AI might improve.
4. Name one thing AI could make worse.
5. Decide who needs to be in the conversation before anything ships.

That is the start of a better AI strategy.

Kris

**Primary CTA:** Bring this conversation to your team.

## Email 3: One Practical Exercise

**Purpose:** Move the reader from passive download to action.

**Subject options:**

- A 15-minute AI exercise
- Try this before your next AI meeting
- The smallest useful AI audit

**Body copy:**

Hi {{first_name}},

Here is a simple exercise you can run in 15 minutes.

Open a blank page and make three columns:

- Work we repeat
- Work that needs judgment
- Work that creates trust

Now list five tasks under each column.

The first column is where AI may save time.

The second column is where AI may help with drafts, options, or synthesis, but humans still own the decision.

The third column is where you move slowly. Trust work needs consent, context, relationship, and accountability. Automation can support it, but it should not quietly replace it.

If you only do one thing after reading the guide, do this map. It will tell you more than another tool demo.

Kris

**Primary CTA:** Book a working session.

## Email 4: Field Proof

**Purpose:** Show how Kris turns ideas into practice without exposing private client details.

**Subject options:**

- What practical AI work looks like
- From messy notes to useful systems
- The work behind the workshop

**Body copy:**

Hi {{first_name}},

The most useful AI work I do rarely starts with a model.

It starts with source material: interviews, workshops, event notes, transcripts, photos, messy docs, half-formed strategy, and the lived context that never fits neatly inside a prompt box.

From there, the job is to build a system that helps people think better:

- Turn scattered knowledge into a usable archive.
- Make the language sound like the humans behind the work.
- Build reusable assets instead of one-off campaigns.
- Keep review, consent, and accountability visible.
- Use automation to support trust, not bypass it.

That is the pattern behind the strongest projects: the knowledge is the asset, the tools are the scaffolding, and the humans still own the meaning.

Kris

**Primary CTA:** See how this could apply to your team.

## Email 5: Segment Routing

**Purpose:** Invite the reader to self-identify and route future follow-up by interest.

**Subject options:**

- Which AI conversation are you actually having?
- Pick your lane
- What brought you here?

**Body copy:**

Hi {{first_name}},

People arrive at AI from very different doors.

Some are trying to lead a team through uncertainty. Some are artists trying to protect their voice while learning new tools. Some are community organizers trying to build trust. Some are media people trying to move faster without breaking verification. Some are working through sovereignty, consent, and governance questions that deserve more care than a vendor deck can provide.

Which conversation are you having right now?

Choose the closest fit:

- I am leading a team or organization.
- I am building creative workflows.
- I am organizing community or ecosystem work.
- I work in media, journalism, or communications.
- I am focused on Indigenous AI, governance, sovereignty, or partnership.

Your answer helps shape what I send next and where a real conversation might be useful.

Kris

**Primary CTA:** Reply with your lane.

**Implementation note:** In a live ESP, these choices should become tracked links or preference-center options only after consent and platform decisions are approved.

## Email 6: Trust and Risk

**Purpose:** Address the reader's likely objections and reinforce a careful operating model.

**Subject options:**

- The AI risk nobody fixes with a prompt
- Trust is the adoption layer
- Move slower where trust is involved

**Body copy:**

Hi {{first_name}},

The hardest AI problems are not prompt problems.

They are trust problems.

Does the team understand what the system is doing? Did people consent to how their material is being used? Can someone explain the decision? Is there a rollback path? Are we making work better, or just making bad process move faster?

That is why I like small, legible pilots.

Pick a real workflow. Limit the blast radius. Keep humans in the loop. Make review visible. Write down what is allowed and what is not. Test the output against reality. Then decide whether it deserves more responsibility.

AI adoption works better when people can see the guardrails.

Kris

**Primary CTA:** Plan a safer AI pilot.

## Email 7: Clear Next Ask

**Purpose:** Convert attention into a next step while leaving a respectful non-buyer path.

**Subject options:**

- Want help turning this into a plan?
- The next useful step
- Bring Kris into the room

**Body copy:**

Hi {{first_name}},

If the guide helped, there are a few good next steps.

If your team needs shared language, bring me in for a keynote.

If you need practical momentum, book a workshop.

If you are already experimenting and want safer systems, start with a workflow audit.

If you are building community around AI, I can help design the room, facilitate the conversation, document the learning, and turn the work into assets that keep serving people after the event ends.

And if now is not the moment, that is fine too. Keep the guide, share it with the person who keeps asking the hard questions, and stay close to the work.

Kris

**Primary CTA:** Book a conversation.

**Secondary CTA:** Keep reading the blog.

## Conceptual Trigger and Tag Map

This is a planning map only. Do not configure these tags or triggers until the platform, consent model, and privacy language are approved.

### Entry Triggers

| Trigger | Source | Intended Action |
|---|---|---|
| `form_submit_lead_magnet_general` | Humanizing Tech landing page | Send guide, enter lead-magnet sequence, tag general AI. |
| `form_submit_lead_magnet_creative` | Creative Technologist landing page | Send guide, enter lead-magnet sequence, tag creative workflow. |
| `form_submit_lead_magnet_community` | Community Building landing page | Send guide, enter lead-magnet sequence, tag community builder. |
| `form_submit_lead_magnet_media` | AI for Media landing page | Send guide, enter lead-magnet sequence, tag media professional. |
| `form_submit_lead_magnet_indigenous_ai` | Indigenous AI landing page | Send guide, enter lead-magnet sequence, tag Indigenous AI interest. |

### Conceptual Tags

| Tag | Meaning |
|---|---|
| `source:kriskrug_site` | Subscriber came through kriskrug.co. |
| `intent:lead_magnet` | Subscriber requested a guide. |
| `segment:general_ai` | Interested in human-first AI leadership. |
| `segment:creative_tech` | Interested in creative AI workflows. |
| `segment:community_building` | Interested in community, ecosystem, or event work. |
| `segment:media_ai` | Interested in journalism, media, production, or communications. |
| `segment:indigenous_ai` | Interested in Indigenous AI, governance, sovereignty, or partnership. |
| `interest:keynote` | Clicked keynote or speaking CTA. |
| `interest:workshop` | Clicked workshop CTA. |
| `interest:strategy` | Clicked strategy or audit CTA. |
| `status:needs_human_reply` | Replied or requested contact; requires manual handling. |

### Suppression and Safety Rules

- Never enroll a contact without clear consent.
- Never import old contacts into this sequence without a separate consent and list-hygiene decision.
- Suppress unsubscribed, bounced, complained, or manually excluded contacts.
- Do not send Indigenous AI follow-up that implies endorsement, authority, or partnership without human review.
- Do not infer sensitive identity from guide interest. Treat segment tags as content-interest signals only.
- Stop automation if a person replies with a direct inquiry, complaint, correction, or consent concern.

## Required Decisions Before Sending

- ESP/CRM platform owner and implementation path.
- Consent language for each form.
- Privacy-policy alignment and data retention expectations.
- Physical mailing address and sender identity requirements.
- From name, reply-to address, and monitored inbox owner.
- Unsubscribe and preference-center behavior.
- Whether old newsletter subscribers can receive any part of this sequence.
- Which guide download files exist and where they are hosted.
- Whether each guide has its own thank-you page.
- Whether link tracking, open tracking, UTM tags, or analytics events are acceptable.
- Accessibility and plain-language review.
- Review owner for Indigenous AI language.
- Manual response workflow for replies and high-intent clicks.
- Rollback process for pausing sends, disabling forms, and removing public CTAs.

## Ready-for-Implementation Checklist

- [ ] KK approves the sequence length and cadence.
- [ ] KK approves subject lines and body copy direction.
- [ ] #229 guide titles and landing-page CTAs are approved.
- [ ] ESP/CRM platform is selected.
- [ ] Consent, privacy, unsubscribe, and data-retention language is approved.
- [ ] Sender identity and monitored reply workflow are confirmed.
- [ ] No automation or send occurs until the above decisions are complete.
