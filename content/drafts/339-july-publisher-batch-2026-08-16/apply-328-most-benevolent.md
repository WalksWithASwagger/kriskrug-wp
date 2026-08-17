# #328 Most Benevolent copy-preserving wraps

**Verdict:** STILL OPEN
**Link target (do not PATCH):** post `3814`, slug `the-power-of-most-benevolent-outcomes-a-prayer-for-blessings-for-all-living-things`, modified `2026-06-28T20:37:13`
**Target href:** `https://kriskrug.co/2023/11/04/the-power-of-most-benevolent-outcomes-a-prayer-for-blessings-for-all-living-things/`
**Evidence:** post 3814 still has exactly two kriskrug.co body links, both auto-footer (category archive + AI companions). Sources 2950 and 2665 still contain the needles once and have **0** hrefs to the target.

Do not add a post-specific theme override. Wrap existing phrases only. Leave surrounding em dashes in the live source copy untouched.

## Patch 1: post 2950

- Slug: `community-weaving-how-digital-interactions-shape-our-physical-world`
- URL: `https://kriskrug.co/2023/09/01/community-weaving-how-digital-interactions-shape-our-physical-world/`
- Modified guard: `2026-06-28T20:38:58`
- Live needle count: 1
- Live target-href count: 0

**FIND:**

```html
Most Benevolent Outcomes
```

**REPLACE:**

```html
<a href="https://kriskrug.co/2023/11/04/the-power-of-most-benevolent-outcomes-a-prayer-for-blessings-for-all-living-things/">Most Benevolent Outcomes</a>
```

Abort if FIND is not exactly one unlinked occurrence. Do not wrap a heading or an already-linked instance.

## Patch 2: post 2665

- Slug: `embracing-the-future-my-journey-with-generative-ai-and-building-a-learning-community-on-discord`
- URL: `https://kriskrug.co/2023/07/09/embracing-the-future-my-journey-with-generative-ai-and-building-a-learning-community-on-discord/`
- Modified guard: `2026-06-28T20:39:43`
- Live needle count: 1
- Live target-href count: 0

**FIND:**

```html
cultivating the most benevolent outcomes
```

**REPLACE:**

```html
<a href="https://kriskrug.co/2023/11/04/the-power-of-most-benevolent-outcomes-a-prayer-for-blessings-for-all-living-things/">cultivating the most benevolent outcomes</a>
```

Context (rendered, for the publisher's eye; apply against `content.raw`):

```html
I&#8217;m committed to cultivating the most benevolent outcomes in humanity&#8217;s association with AI.
```

## Snapshot-first apply

1. Snapshot each source with `GET /wp-json/wp/v2/posts/{id}?context=edit&_fields=id,slug,status,modified,title,content`.
2. Confirm ID, slug, `publish`, and modified guard.
3. Confirm FIND count is 1 and target href count is 0 in `content.raw`.
4. POST `{"content": ...}` only, one post at a time, 2950 then 2665.
5. Public readback: each source returns 200, self-canonical, the wrapped phrase appears once, target 3814 still 200.

## Rollback

Re-POST each snapshotted `content.raw`. Payload key `content` only.
