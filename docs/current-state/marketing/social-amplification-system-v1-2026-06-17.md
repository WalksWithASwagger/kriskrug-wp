# Social Amplification System v1 - 2026-06-17

**Lane:** Track A marketing/content strategy
**Scope:** docs-only v1 for GitHub issue #56. No public posting, account setup, API configuration, outbound messages, private data handling, or production deploy.
**Issue:** [#56 - [MARKETING] Social Media Amplification System](https://github.com/WalksWithASwagger/kriskrug-wp/issues/56)

## Assumptions and Success Criteria

- Every amplification package starts from a published, approved `kriskrug.co` post.
- The system creates reusable assets and approval gates, not automatic public distribution.
- Buffer, Canva, or equivalent tooling may be used later, but this doc does not configure tools or accounts.
- Success for issue #56 means future publishers have a platform-by-platform workflow, templates, gates, privacy constraints, metrics, and a checklist for turning one post into 10-15 derivative assets.

## Platform Workflow

| Platform | Output per canonical post | Best use | Timing | Review focus |
|---|---|---|---|---|
| LinkedIn feed | 3-4 short posts | Professional framing, lessons, event/community proof, service relevance | Publish over 1-2 weeks | Claims, tone, CTA, no private client details |
| LinkedIn article | 1 adapted article or excerpt | High-signal long-form professional reuse | After canonical post and before or during feed run | Canonical link, overlap with syndication plan #52 |
| X/Twitter | 1 thread of 5-10 posts plus optional single quote post | Sharp thesis, useful list, event recap, link back | Same week as canonical post | Thread coherence, no context collapse, no stale handles |
| Instagram feed | 1 carousel or image post | Visual storytelling, event/photo context, concise takeaways | Same week or weekend | Image rights, captions, alt text, tags |
| Instagram Stories | 3-5 frames | Lightweight reminders, behind-the-scenes, recap prompts | 24-72 hours after publish | Publicity consent, no private screenshots |
| TikTok/Reels | 1-3 short clips | Spoken insight, field note, one practical takeaway | Within 2 weeks if video source exists | Consent, captions, no unapproved music/media |
| Pinterest | 2-3 pins | Evergreen visuals, photography, keynote/resource content | Within 2 weeks | Destination URL, image ownership, title readability |
| Email snippet | 1 short newsletter block | Curated note and canonical link | Next newsletter cycle | Subscriber relevance, no overclaiming |

## v1 Tool Roles

| Tool | Role | v1 boundary |
|---|---|---|
| Canva | Design reusable visual templates for carousels, story frames, quote cards, short-video covers, and Pinterest pins | Use only approved source media and reviewed copy; no account setup in this doc |
| Buffer or equivalent scheduler | Hold approved posts in a visible calendar and prevent same-day platform pileups | Schedule only after explicit approval; no account/API configuration in this doc |
| Campaign log | Track canonical URL, derivative asset, platform URL, publish date, UTM, owner, and metrics | Can start as a spreadsheet or repo-safe markdown table before any tool migration |

## Asset Packaging Workflow

### 1. Source

- Confirm canonical URL, title, excerpt, publish date, hero/primary image, author, and target CTA.
- Pull 3-5 core ideas, 2-3 quotable lines, and any proof points from the post.
- Note any source media, people, clients, venues, or sponsors that require approval.

### 2. Split

- Turn the post into:
  - one thesis post,
  - one practical lesson post,
  - one personal/context post,
  - one visual/carousel concept,
  - one thread outline,
  - one email snippet,
  - optional short-video prompts if source footage exists.

### 3. Design

- Use Canva or existing brand templates only after the visual claim, image rights, and platform dimensions are checked.
- Keep text overlays short enough to read on mobile.
- Preserve alt text or write fresh alt text for each image asset.

### 4. Schedule

- Keep a 4-week working calendar with statuses: `drafted`, `review`, `approved`, `scheduled`, `published`, `measured`.
- Do not schedule public posts before approval.
- Avoid posting every derivative on the same day; let each platform breathe.

### 5. Measure

- Capture native analytics after 48 hours, 7 days, and 30 days.
- Keep platform URL, canonical URL, asset type, date, CTA, and metrics in the campaign log.

## Reusable Post Templates

### LinkedIn Thesis Post

```text
I used to think [common assumption].

After [event/project/post context], I think the sharper question is:
[core thesis].

Three things this changes:
1. [point]
2. [point]
3. [point]

Full note: [canonical URL with UTM]
```

### LinkedIn Practical Lesson

```text
One practical takeaway from [post topic]:

[specific lesson in 1-2 sentences]

What worked:
- [detail]
- [detail]
- [detail]

What I would watch next:
[risk/open question]

Source note: [canonical URL with UTM]
```

### X/Twitter Thread

```text
1/ [Hook: specific claim, tension, or lesson]

2/ [Context]

3/ [Point one]

4/ [Point two]

5/ [Point three]

6/ [Concrete example or useful step]

7/ [Why it matters]

8/ Full post: [canonical URL with UTM]
```

### Instagram Carousel

```text
Slide 1: [short title]
Slide 2: [problem/tension]
Slide 3: [lesson one]
Slide 4: [lesson two]
Slide 5: [lesson three]
Slide 6: [question or CTA]

Caption:
[2-4 sentence setup]

Read the full piece at kriskrug.co: [canonical URL or profile-link instruction]
```

### Short-Video Prompt

```text
Opening line: [one sentence hook]
Middle: [one story, example, or lesson]
Close: [one question or CTA]
Caption: [canonical URL or profile-link instruction]
Required on-screen text: [short phrase]
Required captions: yes
```

### Pinterest Pin

```text
Pin title: [clear evergreen title]
Pin description: [1-2 sentence summary with search phrase]
Destination URL: [canonical URL with UTM]
Image: [owned/approved visual]
Alt text: [specific visual description]
```

### Email Snippet

```text
Subject/section line: [short topic label]

[One paragraph that frames why this post matters now.]

Read: [post title] - [canonical URL with UTM]
```

## Approval Gates

Public amplification may proceed only when all gates pass:

- Canonical post is public and stable.
- Platform package uses a reviewed CTA and canonical URL.
- Any names, faces, venues, client references, sponsor references, or attendee context are approved for public reuse.
- Images, clips, logos, screenshots, and music are owned, licensed, or explicitly approved.
- Claims, numbers, dates, and affiliations are current or clearly time-bound.
- Accessibility basics are complete: captions for video, alt text for images, readable text overlays.
- Platform preview has been checked manually.
- KK or delegated publisher approves the final package before scheduling.

## Privacy and Publicity Constraints

- Do not expose attendee identities, private conversations, emails, DMs, Slack/Notion screenshots, form submissions, or unpublished client material.
- Do not imply sponsor, employer, client, or community endorsement unless the relationship is explicit and approved.
- Do not reuse event photos where a person is the subject without checking consent or public-event expectations.
- Do not use platform-native AI expansion tools on private source material.
- Do not post AI-generated imagery as event documentation or factual proof.
- Do not publish crisis, legal, health, or personally sensitive material through this workflow without a separate human review path.

## Metrics

| Metric | Goal signal | Cadence |
|---|---|---|
| Assets created per canonical post | Issue #56 target: 10-15 pieces when the post warrants it | Per package |
| Social reach | Directional target: 3-5x baseline reach after pilot | 7 and 30 days |
| Engagement rate | Saves, comments, replies, shares, profile clicks | 48 hours, 7 days |
| Referral sessions | Clicks to canonical `kriskrug.co` post | 7 and 30 days |
| Leads or inquiries | Clear-source contact, reply, booking, or newsletter signal | Monthly |
| Calendar health | 4 weeks of reviewed or scheduled content, not just drafts | Weekly |
| Quality guardrails | Corrections, takedowns, privacy flags, negative feedback | Continuous |

## Launch Checklist

- [ ] Canonical post URL verified.
- [ ] Source facts, quotes, and media extracted.
- [ ] Privacy/publicity screen passed.
- [ ] Platform package drafted.
- [ ] Image/video rights checked.
- [ ] Alt text and captions prepared.
- [ ] CTA and UTM links reviewed.
- [ ] Platform preview checked.
- [ ] Approval captured before scheduling.
- [ ] Calendar status updated.
- [ ] Published URLs logged.
- [ ] 48-hour, 7-day, and 30-day metric readbacks scheduled.

## Stop Conditions

Pause amplification for a post or platform if:

- Approval is missing or ambiguous.
- A package depends on private or consent-sensitive context.
- Public comments reveal factual confusion that needs correction.
- Platform reach is improving only through low-quality engagement or off-brand framing.
- The calendar is full of drafts but lacks review capacity.
- Tool access, account ownership, or delete/rollback ability is unclear.

## Closeout Criteria for #56

Issue #56 can be treated as strategy-complete when this doc is accepted as the v1 playbook and a future execution issue owns tool selection, template implementation, calendar setup, first package approval, and metric logging.
