# Issue #353 — public body-H1 re-probe (14 targets + homepage)

**Captured:** `2026-07-16T03:01:25Z`
**Mode:** public HTML only. Counts are **live rendered** H1s (template title + body).
**No WP writes.** Migration still requires per-target KK approval + secrets.

## Results

| ID | Route | Live H1s | Expected shape | H1 texts (truncated) |
|---:|---|---:|---|---|
| 3930 | `/` | 1 | intentional sole H1 | Authored judgment for generative everyth… |
| 11358 | `/2026/02/20/spa-at-the-end-of-time/` | 10 | template + body (≥2 until migrated) | Spa at the End of Time; What you’re walking into; The images: comfort tech turns into cosm…; The voice: a medium, not a narrator; The AI part: a haunted paintbrush; The dome does something to your body; The room: artists, weirdos, and people w…; Why it landed: it’s a spa, it’s a warnin…; Receipts; Challenger idea |
| 7927 | `/2024/12/31/ais-next-chapter-notes-from-bcs-ai-ecosystem/` | 6 | template + body (≥2 until migrated) | AI’s Next Chapter: Notes from BC’s AI Ec…; The Inside Out Revolution; ChatGPT’s Reality Check; The Growing Pains; The 2025 Vision; AI Education & Adoption in British Colum… |
| 6453 | `/2024/07/28/small-file-rebellion-hacking-the-digital-carbon-footprint-at-our-networks-2024/` | 2 | template + body (≥2 until migrated) | Small File Rebellion: Hacking the Digita…; #SmallFileRebellion #OurNetworks2024 #Di… |
| 6435 | `/2024/07/27/digital-rebellion-w-lori-emersons-at-our-networks-2024/` | 2 | template + body (≥2 until migrated) | Digital Rebellion w/ Lori Emerson’s at O…; #DigitalRebellion #OurNetworks2024 #Unpl… |
| 6344 | `/2024/07/19/fuck-the-status-quo-ais-messy-love-child-with-creativity/` | 10 | template + body (≥2 until migrated) | Fuck the Status Quo: AI’s Messy Love Chi…; SUMMARY; IDEAS:; INSIGHTS:; QUOTES:; HABITS:; FACTS:; REFERENCES:; ONE-SENTENCE TAKEAWAY; RECOMMENDATIONS: |
| 4826 | `/2024/03/05/join-the-future-proof-creatives-community/` | 2 | template + body (≥2 until migrated) | Future Proof Creatives Community & Event…; Appendix: FAQs |
| 4174 | `/2024/01/19/2024-the-year-of-ai-revolution-a-rebels-guide-to-predicting-the-future/` | 2 | template + body (≥2 until migrated) | 2024: The Year of AI Revolution – A Rebe…; Navigating the AI Landscape in 2024 |
| 4372 | `/2023/12/28/building-ai-companions-w-john-anthony-hartman-of-ihaverobots/` | 2 | template + body (≥2 until migrated) | Building AI Companions w/ John Anthony H…; Chasing the Muses: John Anthony Hartman’… |
| 3908 | `/2023/11/01/web3-will-fail-if-it-doesnt-put-people-before-profits-and-technology/` | 2 | template + body (≥2 until migrated) | The Web3 Manifesto: Challenging Tech Tit…; Reimagining Web3’s Foundation |
| 3567 | `/2023/10/15/community-art-project-development-process-guide/` | 2 | template + body (≥2 until migrated) | Community Art Project Development Proces…; Building Community Through Art: A Guide … |
| 3151 | `/2023/09/18/newsletter-002-rebirth-and-revolution/` | 7 | template + body (≥2 until migrated) | Newsletter 002: Rebirth and Revolution; Hello Friends!; Upcoming Events:; Community Shoutouts:; News & Updates:; New MØTLEYKRÜG Podcast Episodes:; New Videoblogs on YOUTUBE: |
| 2857 | `/2023/08/22/through-my-lens-new-projects-and-updates-from-kris-krug/` | 7 | template + body (≥2 until migrated) | Through My Lens: New Projects and Update…; News & Updates:; Upcoming:; Highlight: Generative AI’s Role in Art a…; Shout-Outs:; Lets Work Together: 778.898.3076; Get In Touch: |
| 1547 | `/2009/12/14/photo-essay-inside-the-negotiations-cop15/` | 2 | template + body (≥2 until migrated) | COP15 United Nations Climate Change Summ…; COP15 United Nations Climate Change Summ… |
| 12013 | `/photography/` | 2 | template + body (≥2 until migrated) | Photography; Two decades in the room, with a camera. |

## Summary

- Homepage (`3930` / `/`): live H1 count = **1** (must stay 1 intentional).
- Non-homepage targets still showing ≥2 live H1s: **14 / 14**.
- Confirms #353 migration queue is still live-relevant; do not start writes without per-ID approval.

JSON twin: `issue-353-public-h1-reprobe-20260716.json`

