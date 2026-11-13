# /ai-policy/ staged as a WordPress draft

Created November 12, 2026, under Kris's approval in chat after he read `policy.md`: "Approve the draft, build it". That covered building the payload (#885) and creating the page as one unpublished draft. Publishing is #886 and needs his separate yes. Epic #883.

## Update, November 13, 2026: the repo payload moved on, the draft did not

Review of PR #1316 found that the first payload dropped the scope sentence ("not legal terms, a privacy policy, or a client contract") with no ruling from Kris on record. The payload in the repo now keeps that sentence as its first paragraph, so it no longer matches what WordPress holds.

- Draft 13005 still holds the earlier body: SHA-256 `ef5c4fcaebc015713b410cd1eca64dbc0118dddda1a85f5a3287a847cd2597f3`, 14,630 bytes. That is the payload as it stood at commit `7e8a883`.
- No WordPress call, read or write, was made for the review fixes. The hash above is the readback from staging and has not been re-read since.
- The draft gets the current payload when the final body is staged before publishing. The order is in the [pack README](../../../content/source-packs/ai-policy-2026/README.md): Kris approves the final copy, the final body goes into the draft so his preview is exact, and publishing is then a status-only flip (#886 step 9).
- `wordpress_draft` in `page-meta.json` records the draft's hash with `matches_payload: false`.

Everything below describes the draft as it was staged on November 12.

## What exists now

- Page **13005**, slug `ai-policy`, status `draft`, title "How I Use AI (And Where I Draw the Line)".
- Body: the payload as it stood at commit `7e8a883`, SHA-256 `ef5c4fcaebc015713b410cd1eca64dbc0118dddda1a85f5a3287a847cd2597f3`, 14,630 bytes. The edit-context readback of `content.raw` at staging had the same hash. The current [`ai-policy.html`](../../../content/source-packs/ai-policy-2026/wp-payloads/ai-policy.html) differs from it by the scope sentence.
- Comments and pings closed, no parent, default page template. Not scheduled and not in any menu: no menu or navigation write was made, and the header parts do not list pages automatically.
- Excerpt and SEO meta were not written. The proposals sit in [`page-meta.json`](../../../content/source-packs/ai-policy-2026/page-meta.json) for the publish step.
- Created 2026-11-13 03:24 UTC (7:24 p.m. Pacific, November 12).

## Preflight

Authenticated `context=edit` lookups found nothing for slug `ai-policy` in pages or posts in any of publish, future, draft, pending, private or trash. They also found nothing for `ai-policy__trashed` in the trash, and no media with that slug. Logged-out `https://kriskrug.co/ai-policy/` returned 404 with no redirect.

The write used the repo's `WPClient.from_env()` through `make varlock-run`. `storable_payload` from `cp1252_text` confirmed the body needed no character references. The one-off staging script was session scratch and is not committed.

## Readback and public checks

- id 13005, type page, slug `ai-policy`, status `draft`, raw title matches, raw content equals the sent payload byte for byte. All ten checks passed.
- `make status-readonly`: `draft_pages` went from 4 to 5. The same run showed `draft_posts` 69 to 70 and `future_posts` 0 to 1. Those came from other sessions; this lane wrote no posts.
- Logged out: `/ai-policy/` 404, `/?page_id=13005` 404, `/?page_id=13005&preview=true` 404, REST `pages?slug=ai-policy` returns `[]`, REST `pages/13005` returns 401.

## How Kris previews it

- Edit screen: `https://kriskrug.co/wp-admin/post.php?post=13005&action=edit`
- Signed-in preview: `https://kriskrug.co/?page_id=13005&preview=true`
- Or wp-admin, Pages, Drafts, "How I Use AI (And Where I Draw the Line)".

The body is one Custom HTML block, so editing text in WordPress means editing HTML. Copy changes belong in `policy.md` and the payload, where the tests keep them in step (see the [pack README](../../../content/source-packs/ai-policy-2026/README.md)).

Two things in the preview are placeholders on purpose:

- `Last updated: YYYY-MM-DD`
- "Proposed AI-assistance disclosure" with the "Pending Kris Krüg's review and approval:" prefix

The current payload has a third: the word "proposed" in the scope sentence. The preview does not show that sentence yet, because the draft holds the earlier body.

`publish_edits` in `page-meta.json` lists the exact replacements. They are applied to the payload after Kris approves the final copy, and that final body is staged in the draft before the status flip.

## Tracking

`wordpress_id` in `page-meta.json` now records 13005, as #886 step 6 asks. The page is not in `content-architecture-2026/wp-payloads/page-map.json`. That map feeds the snapshot-gated deploy for published pages, and its target check refuses any status other than `publish`.

## Links

Eight of the nine links returned 200 with no redirect on November 12. The Government of Canada guide stalls for scripted clients. In a browser it loads, but at a moved path: `.../responsible-use-ai/generative-ai/guide-use-generative-ai.html`. The link still works. Pointing it at the new path means changing `policy.md` first.

## Render check

Before the write, the payload was rendered client-side inside a live page that uses the same default page template, at 694px and 390px. Paper and ink skin, no horizontal overflow at 390px, body text about 17 to 18px. The disclosure card text measures about 7.6:1 contrast. Aurora's H2 scale (about 37px at 390px) wraps the longest heading to four lines on a phone. That is the theme's heading size, and this body-only payload does not override it.

## Rollback

The draft is not public. To withdraw it, move page 13005 to the trash in wp-admin or with REST `DELETE /wp/v2/pages/13005` without `force`. Never force-delete it. After publication, rollback returns 13005 to `draft`.

## Verification

At staging, November 12:

- `python3 -m unittest scripts.tests.test_content_architecture_payloads scripts.tests.test_payload_neon_islands scripts.tests.test_ai_policy_payload`: 29 tests OK.
- `make python-test`: 280 publisher, 1,008 operational and photo-library, 12 SEO inventory and 68 SEO backfill tests passed.
- `make voice-check` on the new files, `make voice-check`, `make docs-truth-check`, `make ruff-changed BASE_REF=origin/main` and `git diff --check`: clean.

After the review fixes, November 13, with no WordPress call:

- `python3 -m pytest scripts/tests/test_ai_policy_payload.py -q`: 19 passed, 43 subtests passed, on the committed pending state.
- The same suite in a scratch copy with a fake `publish_approval`, `status_target` set to `publish` and the four `publish_edits` applied: 19 passed, 43 subtests passed. Before the fixes that state gave 6 failures. The approved state was not committed.
- In that scratch copy, each single fault failed the suite: a date that differs from the approval, a leftover placeholder date, a leftover "proposed", a leftover pending prefix, a leftover pending heading, approval recorded with the body untouched, and a `--` in the body.
- `make python-test`: 280 publisher, 1,027 operational and photo-library, 12 SEO inventory and 68 SEO backfill tests passed.
- `make voice-check`, `make docs-truth-check`, `make ruff-changed BASE_REF=origin/main` and `git diff --check`: clean.
