# Image alt-text audit packet — top 20 high-visibility images (#176)

**Date:** 2026-06-14 · **By:** read-only REST + visual review of the gap images · **Writes:** NONE
**Scope:** the 20 most-visible images (homepage, About page, recent/flagship post featured images), plus the empty-alt gaps found in a scan of the 40 most-recent posts.
**Action requested:** KK approves/edits the **proposed alt** column. Applying approved alt is a later REST step (`POST /wp/v2/media/{id}` `alt_text`) — gated on this sign-off per #176.

## Headline finding

The alt-text program is **mostly healthy** — the Notion publisher sets descriptive alt on recent posts, and the homepage/About inline images already have good alt. Only a few genuine gaps exist among high-visibility images. The most important is the **About page featured image (the flagship page's social/OG card) which has empty alt.**

## Priority A — real gaps (empty alt on high-visibility images; I viewed each, so proposed alt is high-confidence)

| # | Image (media ID) | Where | Current alt | Proposed alt | Conf |
|---|---|---|---|---|---|
| 1 | **3960** `Copy-of-landback-scaled.jpg` | **About page featured image** (OG/social card) | ∅ empty | `About Kris Krüg banner — a large, diverse crowd at a community gathering, overlaid with the tagline "illuminating communities through creativity and connection."` | High |
| 2 | **7892** | Featured image, post 7781 *system-check-vancouver-ai-community-meetups* | ∅ empty | `Photo collage from the December 2024 Vancouver AI community meetup — smiling attendees, a handwritten brainstorm sign, and the event's circular logo.` | High |
| 3 | **7819** | Featured image, post 7810 *fears-hopes-and-dreams…* | ∅ empty | `Illustration for "Fears, Hopes, and Dreams for Our Relationship with AI" — a calm central figure meditating inside a glowing mandala, ringed by whimsical creatures.` | High |

## Priority B — weak/filename-style alt (improve)

| # | Image (media ID) | Where | Current alt | Proposed alt | Conf |
|---|---|---|---|---|---|
| 4 | **11976** | Featured, post 11936 *you-cant-drink-data* | `sign 01 fuck ai protest sign` (filename-style) | `Hand-lettered protest sign reading "you can't drink data," held at a data-centre demonstration.` | Med — confirm sign wording |

## Priority C — already good, confirm & keep (no change unless KK objects)

| # | Media | Where | Current alt (keep) |
|---|---|---|---|
| 5 | homepage | `bcai-living-ecosystem.webp` | BC + AI community ecosystem graphic |
| 6 | homepage | `image-19.png` | Indigenomics AI visual from Kris Krug's public writing |
| 7 | homepage | `ai-courses-workshops-trainings.png` | The Upgrade AI courses workshops and trainings graphic |
| 8 | About inline | `krug-1.jpg` | Portrait of Kris Krug |
| 9 | About inline | `kk-cmvan-keynote-header.png` | Punk Rock AI CreativeMornings Vancouver keynote banner |
| 10 | About inline | `AI-Immortality-w-Guy-Kawasaki.png` | Developing an AI Mindset graphic |
| 11 | About inline | `9818127715…jpg` | Kris Krug with Jack Dorsey at University of Waterloo |
| 12 | About inline | `5637672371…jpg` | Kris Krug presenting at the UN Global Youth Summit |
| 13 | About inline | `20067931301…jpg` | Kris Krug backstage with Malcolm Gladwell |
| 14 | About inline | `4190423843…jpg` | Kris Krug with Daryl Hannah at COP15 in Copenhagen |
| 15 | Post 11878 | featured 11841 | Both Hands Full — the thesis slide… |
| 16 | Post 11877 | featured 3252 | event and portrait photography - kris krug by asa mathat |
| 17 | Post 12183 | featured 12179 | Hope Code process map showing talk notes, visual references… |
| 18 | Post 12033 | featured 11838 | AI Is a Mirror — slide from KK's WAIFF Brazil keynote… |
| 19 | Post 12149 | featured 12146 | Kris Krüg on stage during a Vancouver AI community event |
| 20 | Post 6348 | featured 6657 | Young Kris Krug standing in front of the Form Media Technologies sign in 2000 |

(Items 8/16 are borderline — "Portrait of Kris Krug" and the asa-mathat one are slightly thin; optional polish, not required.)

## Separate follow-up (NOT alt text — missing featured image entirely)

These recent posts have **no featured image at all** (a different gap than alt; flag for a featured-image pass, not this packet):
`12184` canada-ai-for-all-strategy-skeptical-guide · `11014` vancouver-tech-journal-isnt-journalism · `8856` how-indigenomics-ai-is-flipping-the-script · `8786` a-creative-technologists-ai-age-manifesto

## How to apply after approval (later step, gated)
For each approved row: `POST /wp-json/wp/v2/media/{id}` with `{"alt_text": "<approved>"}`, then readback-verify. Media-library alt propagates to every place the image is used. No theme/plugin deploy required (pure data). Decorative images would get empty alt — none of the 20 above are decorative.
