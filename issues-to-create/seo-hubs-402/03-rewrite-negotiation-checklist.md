# [CONTENT] Rewrite post 1210 into the real photographer negotiation checklist

**Parent:** [#402](https://github.com/WalksWithASwagger/kriskrug-wp/issues/402)
**Child:** 3 of 9. Only writing task in the split.
**Suggested labels:** `content`, `seo`, `needs-human-review`, `priority:high`, `enhancement`
**Lane:** Track A
**Research:** `content/drafts/2026-08-02-seo-authority-hubs/hub-plan.md` term 10, `link-matrix.csv` data rows 34-37
**Blocked by:** child 2 (photography hub wired first so 1210 can point at a hub that already routes inward)

---

## Context

Post **1210** (`/2007/04/10/checklist-of-model-photographer-negotiation-items/`) is 84 words. It is a 2007 link-blog stub whose only substantive href is `http://modelmayhem.com/posts.php?thread_id=138265`. That URL **404s**. Wayback has no snapshot (`archived_snapshots: {}`). A term in #402 (`negotiation equipment for photographers`) lands on a page that promises a checklist and delivers a dead link.

PR #670 priority 2: write the actual checklist in KK voice from twenty years of shooting, remove the 404, keep one honest line about where the original lived, then wire it.

This child owns the rewrite **and** the four matrix rows that mention 1210. Child 2 must already have added the archive + 1056 sentences on page 12013 block 23; this child adds the third sentence (row 34) beside them.

KK reviews the rewritten body before any live PATCH. Do not publish a first-draft checklist without that read.

## Owns (write)

- Full body of post **1210** (content only: keep title, slug, date, status).
- Page **12013** block 23: checklist sentence only (row 34).
- Post **1222** checklist sentence (row 35).
- Post **1056** checklist sentence (row 36).
- Closing line of rewritten 1210 → `/photography/` (row 37).

## Must not touch

- Rows 11-14 (already child 2). Do not redo the archive or fashion-years links.
- Category of 1210 unless a live readback shows it is wrong; default is leave taxonomy alone.
- ModelMayhem member-profile link on post 1056 (that outbound stays).
- Theme, schema, titles of 12013 / 1222 / 1056.

## Acceptance Criteria

- [ ] Child 2's four links are live (or re-verified) before this child PATCHes 12013, 1222, or 1056.
- [ ] KK has approved the rewritten 1210 body in a repo payload (under `content/drafts/2026-08-02-seo-authority-hubs/` or a sibling apply folder) before live write.
- [ ] Post 1210 no longer contains `modelmayhem.com/posts.php?thread_id=138265`.
- [ ] Post 1210 contains a real checklist covering all of: usage rights and territory; licence duration; model release and limits; nudity and implied nudity spelled out; third-party and stock sale; retouching and approval; raw ownership; credit format; TFP versus paid and what each costs both sides; escort policy; call / wrap / overtime; travel and parking; wardrobe / hair / makeup supply; cancellation and weather; gear the model should not be asked to carry.
- [ ] One honest line remains about the original ModelMayhem thread (dead, no Wayback snapshot). No fake "still up at" URL.
- [ ] Closing line before the collection footer links `/photography/` with exact anchor `twenty years of shooting since I wrote this` (row 37).
- [ ] Row 34: page 12013 block 23 links 1210 with exact anchor `the negotiation checklist I wrote in 2007 and still stand behind`.
- [ ] Row 35: post 1222 links 1210 with exact anchor `the checklist version of this rant`.
- [ ] Row 36: post 1056 links 1210 with exact anchor `the one useful thing I posted over there`.
- [ ] No em dashes. Voice is KK, not a legal template. No keyword stuffing of `negotiation equipment`.
- [ ] Title of 1210 unchanged unless KK explicitly asks. Slug unchanged.

## Tests/Evals

- Word count of 1210 `content.rendered` (stripped) is far above 84. A useful floor: at least 400 words of checklist, not padding.
- `grep -F 'thread_id=138265'` on the live post returns 0.
- `grep -F` each of the four exact anchors after apply.
- Checklist topical coverage: a fixture or PR checklist that maps each required topic to a heading or list item in the payload. Reject a payload that drops any topic.
- `assert_minimal_diff` does **not** apply to the 1210 rewrite (the body is supposed to change). It **does** apply to the three spoke inserts on 12013, 1222, and 1056.

## Verification

```bash
curl -s -o /dev/null -w '%{http_code}\n' -L https://kriskrug.co/2007/04/10/checklist-of-model-photographer-negotiation-items/
curl -s -o /dev/null -w '%{http_code}\n' -L 'http://modelmayhem.com/posts.php?thread_id=138265'   # expect 404; documenting the hole

# After apply
curl -sL "https://kriskrug.co/2007/04/10/checklist-of-model-photographer-negotiation-items/?cb=$RANDOM" | grep -c 'thread_id=138265'   # 0
curl -sL "https://kriskrug.co/photography/?cb=$RANDOM" | grep -F 'the negotiation checklist I wrote in 2007 and still stand behind'
```

Live PATCH: slug `checklist-of-model-photographer-negotiation-items`, ID 1210, content-only, dry-run then KK `--execute`.

## Agent Instructions

- Draft the checklist in-repo first. Stop for KK voice review. Do not Notion-connector UPDATE this 2007 post.
- Re-fetch 1210, 12013, 1222, 1056 by ID. Abort on slug mismatch.
- On 12013, append the checklist sentence to the **same** closing paragraph child 2 edited. Do not create a second closing section. Do not strip child 2's two links.
- On 1222 and 1056, add only the 1210 sentence. Child 2 already added the 1056 / photography sentences.
- Remove the 404 href. Do not replace it with a guessed forum URL.
- Insert row 37 as the last authored paragraph of 1210, **before** `kk-collection-footer`.
- Do not close #402.

### Data rows 34-37

| # | source_url | target_url | anchor_text | section_hint |
|---|---|---|---|---|
| 34 | `https://kriskrug.co/photography/` | `https://kriskrug.co/2007/04/10/checklist-of-model-photographer-negotiation-items/` | the negotiation checklist I wrote in 2007 and still stand behind | Block 23, closing section, alongside the archive links |
| 35 | `https://kriskrug.co/2007/04/27/to-all-you-wannabe-fashion-photographers/` | `https://kriskrug.co/2007/04/10/checklist-of-model-photographer-negotiation-items/` | the checklist version of this rant | Final paragraph, before the collection footer |
| 36 | `https://kriskrug.co/2006/10/23/kk-on-modelmayhemcom/` | `https://kriskrug.co/2007/04/10/checklist-of-model-photographer-negotiation-items/` | the one useful thing I posted over there | Block 2, trailing sentence |
| 37 | `https://kriskrug.co/2007/04/10/checklist-of-model-photographer-negotiation-items/` | `https://kriskrug.co/photography/` | twenty years of shooting since I wrote this | Closing line of the rewritten post, before the collection footer |

## Out of Scope

- Child 2's four photography-hub rows.
- Recategorizing 1067 (child 1). No title change for `hardcore photoshoot`.
- Legal review / actual contract templates. This is practical checklist copy, not a TOS.
- Schema FAQPage for the checklist (parent #402 schema lane).
