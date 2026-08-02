# Testimonials showpiece v2, page copy (TSTM-4)

**Issue:** [#597](https://github.com/WalksWithASwagger/kriskrug-wp/issues/597), sub-issue of epic [#593](https://github.com/WalksWithASwagger/kriskrug-wp/issues/593).
**Owns:** this file only. No quote bodies here (TSTM-5 owns those). No HTML (TSTM-6). No CSS (TSTM-3).
**Order:** the 11 regions below follow the locked #593 order exactly.
**For TSTM-6:** body headings ship as `h2` (deploy script rejects body `h1`). Kicker / title / intro map onto the `.aurora-tstm-*` class contract on #593.

---

## 1. Hero + stats

### Hero

- **Kicker:** What people say
- **Heading:** Proof with names attached.
- **Support sentence:** What people say after the meetups, the cohorts, and the keynotes, plus the photography years that got me here. Real names, linked sources, nothing invented.

### Stat chips

Ship the six chips. Every number footnoted below.

| Chip | Label | Source |
|---|---|---|
| `300` | paid members, BC + AI Ecosystem Association | [^5] |
| `3,000+` | participants across the ecosystem | [^1] |
| `94+` | documented events | [^1] |
| `31` | monthly Vancouver AI meetups and counting | [^2] |
| `9.5/10` | Responsible AI Professional course rating, Cohort 1 | [^6] |
| `~2,400` | attendees across 2024 events | [^7] |

**Sourcing notes (2026-08-01):**

- Member count updated from the bc-ai.ca `250+` claim to `300` per KK's direct ruling in the #615 reconciliation; the same figure now renders on posts 12034 and 12257. bc-ai.ca/about still says 250+ and needs its own refresh (bc-ai.ca lane, not this repo).
- The RAP rating and 2024 attendee chips ship on KK's direct say-so (session ruling 2026-08-01, recorded on the #597 close). No survey export exists in kk-kb or this repo yet; if one lands, swap the footnote to the file path. kk-kb's keynote framework marks the public ~2,400 trace UNVERIFIED, so KK's confirmation is the source of record.

### Stat sources

[^1]: Live readback of https://bc-ai.ca/about on 2026-08-01: "250+ paid members, 3,000+ participants, 94+ documented events, and recurring rooms". Same three numbers cleared for external use in the kk-kb claim ledger `content/communications/applications/2026-08-creative-bc-board/04-SOURCE-AND-CLAIM-LEDGER.md` (checked 2026-07-29).
[^2]: Vancouver AI Meetup #31 ran 2026-07-29, documented in kk-kb `content/media/meetups/2026-07-29-vancouver-ai-meetup-31/` (recording + podcast files), following the #30 recap at `content/media/meetups/2026-06-24-vancouver-ai-meetup-30-recap.md`. Canonical count of 26 through end of 2025 per kk-kb `content/research-analysis/outputs/meetup-count-standardization-report.md` (issue #1141 there).
[^5]: KK direct ruling, 2026-08-01 live session (issue #615 close): "$340/year, 300 members". Applied the same day to posts 12034 and 12257.
[^6]: KK direct confirmation, 2026-08-01 live session (recorded on the #597 close): Cohort 1 exit-survey average 9.5/10. Internal survey; no export filed yet.
[^7]: KK direct confirmation, 2026-08-01 live session (recorded on the #597 close): approximately 2,400 attendees across 2024 BC + AI events, per internal tracking.

---

## 2. Press band

- **Kicker:** On the record
- **Intro:** Not every receipt is a pull quote. Some of it is recognition, a stage, or peer review.

Descriptive lines only. No invented quotes from these outlets.

| Band item | Descriptive line | Source |
|---|---|---|
| Vancouver Magazine Power 50 | Named to Vancouver Magazine's 2026 Power 50 list. | Live `/publications/` press ledger; https://vanmag.com/city/power-50/introducing-vancouver-magazines-2026-power-50-list/ |
| CreativeMornings | Delivered the Punk Rock AI keynote at CreativeMornings Vancouver, Vancouver Art Gallery, May 2026. Official recording published by CreativeMornings HQ. | kk-kb appearance record `content/projects/05-marketing-and-outreach/press-and-media/appearances/2026-05-01-creativemornings-perils-parallels.md`; https://creativemornings.com/talks/kris-krug |
| BC Studies | Co-authored the peer-reviewed article "Building a Grass Roots AI Community of Practice: A Vancouver-Centered Use Case" with Patrick Pennefather and David Gaertner, BC Studies No. 224, Winter 2024/25. | kk-kb `content/projects/01-vancouver-ai-community/community-resources/publications/bc-studies-grassroots-ai-cop-2024.md`; DOI 10.14288/bcs.no224.199875; live `/publications/` entry https://ojs.library.ubc.ca/index.php/bcstudies/article/view/199875 |

---

## 3. Featured (3)

- **Kicker:** Featured
- **Title:** Start with three.
- **Intro:** Three voices from the current era, quoted at full strength. The rest of the page backs them up.

---

## 4. Rooms

- **Kicker:** Community and rooms
- **Title:** The monthly rooms.
- **Intro:** Vancouver AI at the Space Centre, office hours, and the regulars who keep showing up. Written by people who were in the seats, not by me.

---

## 5. Programs / RAP

- **Kicker:** Programs
- **Title:** Responsible AI Professional, Cohort 1.
- **Intro:** Four weeks of frameworks, hard questions, and a capstone with your name on it. Graduates on what actually stuck.

---

## 6. Talks

- **Kicker:** Talks
- **Title:** Keynotes and guest sessions.
- **Intro:** What hosts and audiences say when a talk lands: language they can reuse and moves they can make the next day.

---

## 7. Training

- **Kicker:** Training
- **Title:** Workshops that use your real work.
- **Intro:** Sessions built on the crew's own tools, data, and deadlines. Less inspiration, more reps.

---

## 8. Threads (T2)

- **Kicker:** From the threads
- **Title:** Said in the group chat.
- **Intro:** Some of the best lines never hit LinkedIn. These came from message threads and DMs, published with permission from the people who wrote them.

Note for TSTM-5/TSTM-6: every card in this region must have a row in the consent log before deploy.

---

## 9. Film

- **Kicker:** Film
- **Title:** Film Club nights.
- **Intro:** Screenings, short technical breakdowns, and a packed room arguing about where the industry goes next.

---

## 10. Archive

- **Kicker:** Archive
- **Title:** The photography and connector years.
- **Intro:** Older public lines from the conference-camera era. Kept because the path matters, not as the lead proof for the AI work.

---

## 11. CTA

- **Title:** Want a room like these?
- **Body:** Keynotes, workshops, briefings, and community design. Tell me the audience, the date, and the question the room is trying to answer.
- **Primary:** Start a booking conversation → `/contact/`
- **Secondary:** See speaking topics → `/speaking/`
- **Tertiary (optional):** BC + AI → `https://bc-ai.ca/`

Both site paths verified live (HTTP 200, 2026-08-01). "Start a booking conversation" matches the button already on `/speaking/`.
