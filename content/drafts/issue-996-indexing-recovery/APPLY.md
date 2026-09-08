# #996 APPLY: five-URL indexing-recovery batch

**Prepared, not applied. Do not PATCH until KK says go, and not until ranks 2–5 are confirmed against the current GSC Crawled-not-indexed examples.**

Parent investigation: #996. This pack does not recategorize, retitle public post titles, or touch other-lane write surfaces.

Do not close #996 from an apply. Indexing is not guaranteed.

## Identity (slug check before any write)

Abort if any ID's live slug, status, or `modified` differs from `manifest.json`. Never PATCH on ID alone.

| ID | Required slug | `modified` guard | `modified_gmt` guard |
|---:|---|---|---|
| 4539 | `exploring-the-intersection-of-photography-and-generative-ai` | `2026-06-28T20:36:28` | `2026-06-29T04:36:28` |
| 3082 | `exploring-the-world-of-ai-image-generation-with-artist-frank-yu` | `2026-06-28T20:38:45` | `2026-06-29T04:38:45` |
| 4372 | `building-ai-companions-w-john-anthony-hartman-of-ihaverobots` | `2026-07-24T14:39:51` | `2026-07-24T22:39:51` |
| 4359 | `generative-ai-future-proof-creatives-online-training-workshops-2024` | `2026-07-01T16:24:12` | `2026-07-02T00:24:12` |
| 4826 | `join-the-future-proof-creatives-community` | `2026-07-24T14:39:53` | `2026-07-24T22:39:53` |

Public `content.rendered` SHA-256 values in `manifest.json` are **session evidence** from 2026-09-08. Some rendered bodies include embed/share chrome that can drift without an editor save. Apply uses authenticated `content.raw` plus the FIND needle, not the rendered hash, as the abort condition.

## What would be written

Content and allowlisted SEO meta only. Slugs, dates, status, featured media, tags, and categories stay untouched.

Suggested order (one object at a time): 4539 → 3082 → 4372 → 4359 → 4826. 4539 first so its outbound hrefs exist before the inbound wraps are judged.

| ID | Fields | Find (exactly once) | Change |
|---:|---|---|---|
| 4539 | `content`, `advanced_seo_description` | first residency paragraph; Hartman Notion href | Insert answer-first paragraph linking 3082; retarget inaugural-artist href to 4372; overwrite present-tense February description |
| 3082 | `content`, `jetpack_seo_html_title` | `Keep generating!` | Append one 4539 sentence; set a short SEO title (field is empty now) |
| 4372 | `content` | `opening new creative horizons.` | Append one 4539 sentence |
| 4359 | `content` | hashtag paragraph | Insert one paragraph linking 4539 and 4826 |
| 4826 | `content` | opening `feel left behind` paragraph | Append one sentence linking 4539 and 4359 |

Skip a row if that exact href + anchor already exists.

## Snapshot-first apply

1. Authenticated `GET /wp/v2/posts/{id}?context=edit` plus public HTML plus SHA-256 under `backup/<UTC>-issue-996/`. Mode 0600 on the JSON.
2. Confirm ID + slug + publish + `modified`.
3. Confirm FIND occurs once in `content.raw`.
4. PATCH that one object.
5. Authenticated readback + cache-busted public HTML + ordinary cached-page HTML.
6. KK purges Pagely PressCACHE. Agents cannot.
7. Next object.

## Rollback

Re-POST the snapshotted `content.raw` and the prior `jetpack_seo_html_title` / `advanced_seo_description` values. Keep the snapshot until the 14-day measurement window ends.

## Must not

- Request indexing, submit or remove sitemaps, or click Validate Fix from an agent session. KK may submit **4539** in URL Inspection after purge.
- Edit page 12316 or any #830 / #339 / #994 / #995 / #997 file.
- Recategorize 4372.
- Rewrite luma URLs as if the 2024 seats are still for sale.

## Commands (future session)

There is no apply script in this pack. Use the existing snapshot-first REST flow KK already uses for Track A content writes, with `manifest.json` as the field list. Dry-run GET first. `--apply` is a later human decision.
