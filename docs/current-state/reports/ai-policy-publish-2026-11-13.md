# /ai-policy/ publish ruling and final copy

November 13, 2026. Release record for #886, epic #883. The draft's own record is the [staging receipt](ai-policy-draft-2026-11-12.md).

This file records Kris's rulings and the final copy in the repo. The lane that wrote it made no WordPress call. The orchestrating session made the live writes and the publish, and fills in the two places marked for it below: the publish time and the public checks.

## Kris's rulings, in chat on 2026-11-13

1. On how to review the final copy: "Stage final copy, I'll preview".
2. After previewing it, on the scope sentence and publishing: "Drop the scope line, then publish".
3. On the SEO title and description: "Leave the defaults".

## Sequence

- PR #1316 merged at 23:46 UTC with the pending payload, which still had the scope sentence and three other placeholders.
- 23:56:49 UTC: the final body was staged in draft 13005 for his preview. It was the merged payload with all four publish edits applied and the date 2026-11-13: SHA-256 `f8a1ef5be855e9b8ba44a0b2bf7191d1a797caad467056fa0994406384b0e70d`, 14,667 bytes. The excerpt was written with it.
- Kris previewed that draft and gave ruling 2.
- The scope paragraph came out of the body. The final body is the staged one minus that single line and its newline: SHA-256 `97e97a43e33158fb42dac99fac335df20a02ddec2ae76cb8ba8e44b905bb53fd`, 14,562 bytes. It is [`ai-policy.html`](../../../content/source-packs/ai-policy-2026/wp-payloads/ai-policy.html) in this repo, byte for byte.
- 2026-11-14 00:06:34 UTC: the scope paragraph was removed from draft 13005 with a content-only write, after a snapshot. The readback matched the final body exactly and the page was still a draft.
- 2026-11-14 00:06:55 UTC (November 13, 17:06 in Vancouver): page 13005 published with a status-only write, after another snapshot. Slug, title and body did not change.

## What the scope ruling changes

The review note at the top of `policy.md` reads "Draft for Kris Krüg's review. This is a proposed public transparency statement, not legal terms, a privacy policy, or a client contract." Its first sentence was never in the body. Its second was kept through review because nothing on record removed it. By ruling 2 the whole note is out of the body.

`review_note_ruling` in [`page-meta.json`](../../../content/source-packs/ai-policy-2026/page-meta.json) holds his words. The contract tests fail if the sentence returns, and fail if that record is missing while the sentence is gone. `policy.md` itself is unchanged, and its hash still matches the reviewed copy.

## What was and was not written

- Body: the final body above.
- Excerpt: written with the final body. The text is `excerpt` in `page-meta.json`.
- SEO title and description: not written. Pages do not expose `jetpack_seo_html_title` or `advanced_seo_description` over REST, and Kris chose the defaults (ruling 3). The values under `meta` in `page-meta.json` stay as proposals only.
- Slug `ai-policy` and the title did not change.

## Public checks

Logged out at 00:08 UTC on 2026-11-14, on a cache-busted URL and on the plain URL, with the same result both times:

- `https://kriskrug.co/ai-policy/` returns 200. The canonical tag is the same URL, and there is one `h1`.
- The `<title>` is `How I Use AI (And Where I Draw the Line) | Kris Krüg` and the meta description is the excerpt, both WordPress defaults.
- Present: "The short version: Both Hands Full", "What I will not fake", "I own what ships", "AI-assistance disclosure" and "Last updated: 2026-11-13".
- Absent: `YYYY-MM-DD`, "Pending Kris", "Proposed AI-assistance", "public transparency statement" and "not legal terms". No em dash is in the page text.
- The page is listed in `wp-sitemap-posts-page-1.xml`, it is not `noindex`, and public REST returns it with `status: publish`.
- The authenticated readback of `content.raw` after the flip hashes to `97e97a43e33158fb42dac99fac335df20a02ddec2ae76cb8ba8e44b905bb53fd`, the payload in this repo.

Rollback: three edit-context snapshots (before the final body, before the scope removal, before the publish) are kept locally under the ignored `.generated/current-state/ai-policy-draft-2026-11-12/` in the main checkout. To unpublish, set the page back to `draft` with a status-only write and read it back. Never delete the page.

## Repo state after this record

- `publish_approval` is recorded with the date 2026-11-13, and `status_target` is `publish`.
- `publish_edits` keeps the three remaining edits, already applied. The fourth, which dropped "proposed" from the scope sentence, left with the sentence.
- `wordpress_page` replaces `wordpress_draft`. It holds both hashes, `matches_payload: true` for the final body, and the two fields the orchestrating session fills.

## Rollback

Return page 13005 to `draft`. Do not delete it.

## Verification

No WordPress call was made for this record.

- `python3 -m pytest scripts/tests/test_ai_policy_payload.py -q`: 21 passed, 45 subtests passed, on the committed approved state.
- The same suite in a scratch copy put back into the pending state (edits reversed, `publish_approval` null, `status_target` draft): 21 passed, 45 subtests passed.
- Rebuilding the staged body from the merged payload gives the staged hash and size above, and removing the one paragraph line gives the final hash and size.
- `make python-test`: 280 publisher, 1,076 operational and photo-library, 12 SEO inventory and 68 SEO backfill tests passed.
- `make voice-check`, `make docs-truth-check`, `make ruff-changed BASE_REF=origin/main` and `git diff --check`: clean.
