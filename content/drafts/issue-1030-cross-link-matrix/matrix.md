# #1030 matrix — source, target, anchor, placement

Live-checked 2026-09-18 (logged-out GET). Every included target returned **200** on its public URL. `https://kriskrug.co/?p=12800` 301s to the ALL IN 03 canonical; **do not paste that query URL**.

Canonical ALL IN 03 (public 200):
`https://kriskrug.co/2026/09/17/all-in-montreal-day-two-uncle-evan-and-the-extremely-suspicious-backpack/`

## Series navigation (`ALL IN Montréal 2026` rail)

Visible rail near the end of each live post, before generic related / rabbit-hole lists. Do not self-link.

| Source | Target | Anchor | Placement | Live now |
|---|---|---|---|---|
| ALL IN 01 | ALL IN 02 | Day one: champions, saplings, and chalk | New rail after the YVR closing figure, before the author panel | Missing |
| ALL IN 01 | ALL IN 03 | Day two: Uncle Evan and the suspicious backpack | Same rail | Related-posts widget uses the post title only. Need specified anchor |
| ALL IN 02 | ALL IN 01 | The road east to ALL IN Montréal | New rail after "I will be there with the recorder, asking first." and before `Further down the rabbit hole` | Body + rabbit hole already link 01 under other anchors. Still add specified-anchor rail |
| ALL IN 02 | ALL IN 03 | Day two at ALL IN Montréal | Same rail | Missing |
| ALL IN 03 | ALL IN 01 | Start with the road to Montréal | Replace the live `Continue the series` numbered titles | Live titles, not specified anchors |
| ALL IN 03 | ALL IN 02 | Day one at the Palais | Same replacement | Live titles, not specified anchors |
| `/blog/` (page 2316) | all three public posts | ALL IN Montréal 2026 | Optional intro on the empty posts page. `/events/` is the hosted-room hub, not this reporting series. Do not put ALL IN on `/events/` | Archive already lists the three posts as the latest cards. Page 2316 `content.rendered` is empty |

## Contextual outbound

| Source | Target | Anchor | Placement | Live now |
|---|---|---|---|---|
| ALL IN 01 | https://bc-ai.ca/conferences | the rooms BC + AI is watching | After the accredited-media / national-conference setup sentence | Missing |
| ALL IN 01 | https://bc-ai.ca/ai-community-british-columbia | British Columbia's AI community | After the west-coast vantage sentence in `Why I am headed east` | Missing |
| ALL IN 01 | https://www.futureproof.website/festival/ | Futureproof Festival of AI in Vancouver | Wrap the hometown-festival sentence (`Futureproof Festival runs October 28 to 30`) | Bare text. Earlier homepage `futureproof.website/` link stays |
| ALL IN 02 | https://bc-ai.ca/news/futureproof-festival-regional-story-national-invitation | the regional story behind Futureproof | After the Hanna east-coast / west-coast paragraph | Missing on 02. 03 already uses this URL on a different "Futureproof" wrap; leave 03 alone |
| ALL IN 02 | https://www.futureproof.website/festival/ | Futureproof's Vancouver conversation | Short clause after the existing homepage Futureproof closer | Homepage `futureproof.website` already on that closer. Add the `/festival/` deep link; do not rewrite the existing homepage CTA |
| ALL IN 03 | https://bc-ai.ca/news/bc-ai-s-platform-for-canada-s-ai-task-force | BC + AI's platform for Canada's AI Task Force | New clause after `So I am pulling them.` | Missing |
| ALL IN 03 | https://bc-ai.ca/news/bcs-response-to-the-canada-s-ai-task-force | BC's response to the AI Task Force | Same clause. Unwrap the live long-phrase wrap so the href appears once with the specified anchor | Live href present on `four of the thirty-three submissions...` |
| ALL IN 03 | https://www.futureproof.website/speakers/kris-krug/ | Kris Krüg at Futureproof | Next-room rail after the series rail. Not inside reported copy | Missing. Reported copy links `/speakers/` lineup only |
| January essay | https://kriskrug.co/ai-for-creatives/ | AI for creative professionals | After Workflow 3 guardrail, before The Human Moat | Related-card only. Need body contextual |
| January essay | https://bc-ai.ca/communities/vancouver-ai | Vancouver AI community | After `Get in the room...` in The Call | Bio still points at `vancouver.bc-ai.net`. Do not rewrite the bio |
| January essay | https://www.futureproof.website/festival/ | Futureproof Festival of AI | After `Both hands full. Keep walking.` | Missing |
| AI Second Brain | https://kriskrug.co/ai-tools/ | generative AI tools and workflows | After the four-step setup list | Related/category chrome only |
| AI Second Brain | https://kriskrug.co/2026/09/03/what-i-showed-founders-about-ai-workflows/ | the workflow I showed a room of founders | After the course/membership practical paragraph | Missing |
| AI Second Brain | January essay | keep both hands on the work | After the authenticity / ethics caveat | Missing |

## Inbound to AI Second Brain

One descriptive link per source page. Prefer the specified anchor. Do not add a second href if one already exists; retitle or keep a single contextual insert.

| Source | Target | Anchor | Placement | Live now |
|---|---|---|---|---|
| `/ai-tools/` | Second Brain | build an AI second brain that works for you | Retitle the existing Personal-systems card `h3` | Card already links the canonical. Title is `Build an AI second brain` |
| Founders workflows | Second Brain | my full AI second-brain setup | After `That is a second brain, scoped to one project.` | Missing |
| Speak it into existence | Second Brain | the larger second-brain workflow | After step 4 of `A Simple Voice-First Workflow`. Retitle the existing Related item so the URL appears once | Related list already uses the post title |
| God Skills | Second Brain | the personal context layer behind the agents | After the `knowledge-signal` row / "reusable context" idea | Missing |

## Identity (slug check before any future write)

Abort if any live slug differs. Never PATCH on ID alone. Never send `?p=12800`.

| ID | Kind | Required slug | Public URL |
|---:|---|---|---|
| 12783 | post | `headed-east-for-all-in-montreal` | https://kriskrug.co/2026/09/15/headed-east-for-all-in-montreal/ |
| 12788 | post | `all-in-montreal-robot-mirror` | https://kriskrug.co/2026/09/16/all-in-montreal-robot-mirror/ |
| 12800 | post | `all-in-montreal-day-two-uncle-evan-and-the-extremely-suspicious-backpack` | https://kriskrug.co/2026/09/17/all-in-montreal-day-two-uncle-evan-and-the-extremely-suspicious-backpack/ |
| 11171 | post | `both-hands-full` | https://kriskrug.co/2026/01/24/both-hands-full/ |
| 8802 | post | `how-to-build-an-ai-second-brain-that-actually-works-for-you` | https://kriskrug.co/2025/04/01/how-to-build-an-ai-second-brain-that-actually-works-for-you/ |
| 12744 | post | `what-i-showed-founders-about-ai-workflows` | https://kriskrug.co/2026/09/03/what-i-showed-founders-about-ai-workflows/ |
| 11878 | post | `speak-it-into-existence-ai-voice-first-workflows` | https://kriskrug.co/2026/06/13/speak-it-into-existence-ai-voice-first-workflows/ |
| 12263 | post | `god-skills-agentic-loop-workflows` | https://kriskrug.co/2026/06/20/god-skills-agentic-loop-workflows/ |
| 12321 | page | `ai-tools` | https://kriskrug.co/ai-tools/ |
| 12316 | page | `ai-for-creatives` | https://kriskrug.co/ai-for-creatives/ |
| 2316 | page | `blog` | https://kriskrug.co/blog/ |
