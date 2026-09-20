# Owned distribution + backlink checklist

Reusable per-article launch record for substantial [kriskrug.co](https://kriskrug.co/) posts. Copy this file into the draft package as `content/drafts/<YYYY-MM-DD-slug>/owned-distribution.md`, then fill the article fields, platform URLs, UTM notes, and verification rows.

Owner issue: #1026. Parent: #1025. This is process infrastructure, not a publish, social, newsletter, or outreach mandate. Do not post, email, submit Search Console URLs, or edit live WordPress from this template. KK-gated steps stay gated.

This checklist is the **owned-channel launch path** after a canonical essay is public. It does not replace the batch indexing runbook in [`SEO-INDEXING-RUNBOOK.md`](../SEO-INDEXING-RUNBOOK.md). Strategy context (not a second checklist): [`marketing/content-syndication-strategy-v1-2026-06-17.md`](../marketing/content-syndication-strategy-v1-2026-06-17.md) and [`marketing/social-amplification-system-v1-2026-06-17.md`](../marketing/social-amplification-system-v1-2026-06-17.md).

## How to use

1. Confirm the post is a substantial essay worth a launch pass (skip thin notes, utility pages, and already-distributed archives unless KK names them).
2. Copy this template into the draft package as `owned-distribution.md`. Keep this file in `docs/current-state/templates/` as the blank source.
3. Fill **Article record** first. Leave a platform or partner row as `n/a` with a one-line reason when the topic does not fit. Do not invent relevance.
4. Draft copy and link asks here. KK approves wording and sends, posts, or publishes.
5. After KK ships a channel, record the public URL, date, and the exact UTM URL used.
6. Capture GSC query / impressions / clicks at 7, 28, and 90 days. Leave metric cells blank until those dates exist.

First-wave usage after this template lands: the next three substantial posts each get a completed copy of this record (URLs + dates). This file itself is the blank; it is not those three records.

## Guardrails

- No full duplicate cross-posts. If a full reprint is unavoidable, canonicalize to the chosen source and keep a visible original-publication note plus the clean `kriskrug.co` URL.
- No bulk directory spam, reciprocal-link schemes, or paid link packages.
- Use descriptive anchors. Do not repeat the same exact-match keyword on every outbound or internal link.
- Deep-link BC + AI or Futureproof only when the topic actually touches that work. Homepage-only dumps are not a deep link.
- Partner link-asks need KK wording approval before anyone sends them.
- Do not put UTM parameters on the WordPress canonical URL, on internal `kriskrug.co` links, or on share/tracking copies that should stay clean. UTM lives only on the outbound distribution URL that points **to** the clean canonical.

## Article record

| Field | Value |
|---|---|
| Title | |
| Slug | |
| Canonical URL (clean, no UTM) | `https://kriskrug.co/.../` |
| WordPress ID | |
| Publish date (YYYY-MM-DD) | |
| Draft package | `content/drafts/<YYYY-MM-DD-slug>/` |
| Topic touches BC + AI? (yes/no + why) | |
| Topic touches Futureproof? (yes/no + why) | |
| Owner / approver | KK |

## Canonical article (`kriskrug.co`)

Agent-safe to draft and list. Live body edits stay KK-gated.

- [ ] Canonical essay is public on `kriskrug.co` (logged-out URL, not a draft preview).
- [ ] 2-4 descriptive internal links to older relevant essays or hubs (anchors + target URLs below).
- [ ] One contextual deep link to BC + AI when the topic touches association work, policy, programs, or community. Else `n/a`.
- [ ] One contextual deep link to Futureproof when the topic touches festival themes, speakers, participation, or program. Else `n/a`.
- [ ] Slug / ID match verified before any later PATCH. See [`INCIDENT-2026-05-15-overwritten-post.md`](../INCIDENT-2026-05-15-overwritten-post.md).

| Kind | Anchor text | Target URL | In live body? (yes / draft / n/a) |
|---|---|---|---|
| Internal 1 | | | |
| Internal 2 | | | |
| Internal 3 | | | |
| Internal 4 (optional) | | | |
| BC + AI deep link | | | |
| Futureproof deep link | | | |

## Owned platforms

Write original copy for each surface. Do not paste the full article. Canonical URL goes **after** the useful text.

| Platform | When to use | Format | Agent-safe | KK-gated |
|---|---|---|---|---|
| LinkedIn | Every substantial essay | Native 150-300 word post, one sharp idea, one image or carousel, then the canonical URL | Draft the post + image note | Publish the LinkedIn post |
| Newsletter | Every substantial essay | Original 80-150 word setup plus the canonical URL | Draft the blurb | Send / schedule the issue |
| BC + AI | Only a distinct institutional angle | 150-300 words linking to both the canonical essay and the relevant BC + AI hub | Draft the angle + both URLs | Publish on BC + AI |
| Futureproof | Only when genuinely relevant | Distinct festival angle and a deep link to the right festival page | Draft the angle + page URL | Publish on Futureproof |

### LinkedIn

- [ ] Draft 150-300 words around one idea (not a summary dump).
- [ ] One image or carousel noted (rights + alt text).
- [ ] Canonical URL after the useful text, with UTM (see below).
- [ ] Posted. Public URL + date recorded.

Draft / URL / date:

```text
Posted URL:
Date:
UTM URL used:
```

### Newsletter

- [ ] Draft 80-150 word setup. Do not paste the full article.
- [ ] Canonical URL with UTM after the setup.
- [ ] Sent or scheduled. Issue URL or archive link + date recorded.

Draft / URL / date:

```text
Issue / archive URL:
Date:
UTM URL used:
```

### BC + AI (skip unless the institutional angle is real)

- [ ] Distinct association / policy / program / community angle, 150-300 words.
- [ ] Links to the canonical essay **and** the relevant BC + AI hub (not only `https://bc-ai.ca/`).
- [ ] Published. Public URL + date recorded.

Draft / URL / date:

```text
Posted URL:
BC + AI hub URL:
Date:
UTM URL used:
```

### Futureproof (skip unless the festival angle is real)

- [ ] Distinct festival angle.
- [ ] Deep link to the matching Futureproof page (not only the homepage).
- [ ] Published. Public URL + date recorded.

Draft / URL / date:

```text
Posted URL:
Festival page URL:
Date:
UTM URL used:
```

## UTM notes

Use UTM only on outbound distribution links that send a reader to the clean canonical. Suggested pattern, matching [`content-syndication-strategy-v1-2026-06-17.md`](../marketing/content-syndication-strategy-v1-2026-06-17.md):

```text
https://kriskrug.co/<path>/?utm_source=<platform>&utm_medium=<medium>&utm_campaign=<post-slug>
```

| Platform | `utm_source` | `utm_medium` | `utm_campaign` |
|---|---|---|---|
| LinkedIn | `linkedin` | `social` | post slug |
| Newsletter | `newsletter` | `email` | post slug |
| BC + AI excerpt | `bc-ai` | `syndication` | post slug |
| Futureproof excerpt | `futureproof` | `syndication` | post slug |
| Partner / source ask | `partner` | `referral` | post slug |

- Do not replace the WordPress canonical with a tracking URL.
- Do not mint internal `?share=`, `nb=1`, or UTM copies. Those are crawl waste under #1025.
- If a platform strips query strings, still record the intended UTM URL here and note `stripped`.
- Full-text syndication (Medium, Dev.to, and similar) is **not** a default owned-channel step. If KK later authorizes one, follow the #52 syndication playbook and log it as an extra row, not a substitute for LinkedIn or the newsletter.

Filled UTM URLs for this article:

```text
linkedin:
newsletter:
bc-ai:
futureproof:
partner:
```

## Backlink / partner asks

Ask named sources or partners for a link only when the article materially features their work. Personalize each ask. Get outgoing wording approved before anyone sends it.

| Partner / source | Why they are in the piece | Desired target + descriptive anchor | Draft ask (KK approves) | Sent? (date) | Resulting URL |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |

- [ ] No ask drafted where the person or org is only mentioned in passing.
- [ ] KK approved the outgoing wording (or marked the row `n/a`).
- [ ] Resulting live URL recorded, or `declined` / `no reply` with the date checked.

## Verification

Agent-safe: draft the URL list and leave metric cells blank. KK-gated: Search Console submission, live cache purge, sending outreach.

- [ ] Public canonical returns the expected title (logged-out readback after any KK publish).
- [ ] Internal and deep-link hrefs in the live body match the table above.
- [ ] GSC URL Inspection drafted for the clean canonical (KK submits).
- [ ] Platform URLs and dates filled for every shipped channel; skipped channels say `n/a`.
- [ ] 7 / 28 / 90 day GSC rows captured (queries, impressions, clicks).

| Window | Date captured | Indexed? | Top queries | Impressions | Clicks | Notes |
|---|---|---|---|---|---|---|
| Publish day | | | | | | |
| 7 days | | | | | | |
| 28 days | | | | | | |
| 90 days | | | | | | |

Do not claim a live change from this record. Agents draft and verify public read-only state. KK posts, sends, submits, and purges.
