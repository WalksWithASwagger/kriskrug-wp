# Consent outreach shortlist (TSTM-7, #600)

Sub-issue of epic [#593](https://github.com/WalksWithASwagger/kriskrug-wp/issues/593). Read-only inputs: [`consent-log.md`](consent-log.md), [`linkedin-gaps.md`](linkedin-gaps.md), [`curated-set-v2.md`](curated-set-v2.md).

**Nothing here has been sent.** This file is a shortlist and a set of drafts. Sending is a human action, and KK does the sending in his own words.

## Who is on the list and why

The epic ruling for Tier 2 quotes is *ship it, log it, pull on request*: T2 material came from places where people spoke publicly-ish (member WhatsApp threads, cohort feedback, the Notion Master Directory) but never explicitly said "put this on your website." They are live on the page under that ruling. This outreach closes the loop after the fact rather than gating the ship.

Every person below is a `T2-shipped-logged` row in `consent-log.md`. That is the whole list: 8 people, no one else.

| ID | Person | Where the quote came from | Best channel | Template |
|---|---|---|---|---|
| SAT-01 | Pete Young | Ed + AI WhatsApp thread | WhatsApp, or [LinkedIn](https://www.linkedin.com/in/pete-young-8a7a89a5) | standard-ask |
| TR-01 | Jill Manuel | Notion Master Directory, training cohort bank | [LinkedIn](https://www.linkedin.com/in/jillannmanuel/) | standard-ask |
| TR-02 | Harrison Reed | Notion Master Directory, training cohort bank | **No LinkedIn on file** (`MISSING` in linkedin-gaps). Needs an email or cohort contact from KK. | standard-ask |
| OH-02 | Becky Pallack | Coaching-session feedback capture (`TESTIMONIAL_20251018_002.txt`) | Not resolved. Coaching-session contact, likely email. | standard-ask |
| WA-01 | Darren Nicholls | BC + AI Members WhatsApp | WhatsApp, or [LinkedIn](https://www.linkedin.com/in/darren-nicholls) | standard-ask |
| WA-09 | Sev Geraskin | BC + AI Members WhatsApp | WhatsApp (no LinkedIn resolved) | standard-ask |
| WA-10 | Peter Bowles | BC + AI Members WhatsApp, 2025-07-31 | WhatsApp (no LinkedIn resolved) | **profanity-check** |
| SAT-03 | Kaoru Yoshihira | Film Club WhatsApp / Notion Master Directory | [LinkedIn](https://jp.linkedin.com/in/kaoruyoshihira) (JP) | standard-ask |

Three of the eight (Harrison Reed, Becky Pallack, Sev Geraskin) have no resolved public channel. Those need a contact from KK's own records before anything can be sent.

## Templates

Short, plain, no marketing voice. The ask is genuinely easy to say no to, because "pull on request" only means something if declining is frictionless.

### `standard-ask`

> Hey [name]. I pulled together a testimonials page for the site and used something you said about [thing] on it, with your name on it. It came from [where], which wasn't exactly a "can I quote you" moment, so I wanted to tell you rather than let you find it.
>
> Here it is: https://kriskrug.co/testimonials/
>
> If you'd rather it wasn't up there, say the word and I'll pull it today. No explanation needed. If you want the wording tweaked or your title fixed, tell me what it should say.

### `profanity-check` (Peter Bowles, WA-10)

Same as above, plus:

> Fair warning, I left your swearing in, because cleaning it up would have made it sound like someone else. Happy to bleep it or pull it entirely, your call.

### `already-public` (not needed for this list, kept for reuse)

For T1 rows if any ever need a courtesy note: same opener, but the "wasn't a can-I-quote-you moment" line comes out, since those came from public posts or named event feedback forms.

## Handling replies

- **Yes / no reply:** nothing to do, the card stays.
- **Pull it:** flip that row in `consent-log.md` from `T2-shipped-logged` to `pulled`, remove the card from `curated-set-v2.md` and the payload, then redeploy under [#602](https://github.com/WalksWithASwagger/kriskrug-wp/issues/602)'s snapshot gate. Same day.
- **Reword / fix my title:** update the quote or role in `curated-set-v2.md` and the payload, keep the log row, note the change and the date.
- **No answer:** the card stays. That is the ruling, not an oversight.

## Also worth a note (not consent, identity)

Two people are deliberately *out* of the curated set as `requested` in `consent-log.md`, and they need a different conversation:

- **Aynsley Vogel (MT-30)** answered a survey anonymously and was identified later by cross-reference. Publishing her name on a previously-anonymous line needs her explicit yes first. Ask before shipping, not after.
- **Ishtar Beck (MT-24)** has no consent problem at all. The blocker is that the LinkedIn URL carries a "confirm logged-in before public use" flag, so the *cite* is unverified. KK confirming the profile is enough to ship her.
