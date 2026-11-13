# AI Policy 2026 Source Pack

Kris Krüg's public AI use policy for `https://kriskrug.co/ai-policy/`. Epic #883.

## Status

- Track A page content. Publishing is a separate yes from Kris (#886).
- `policy.md` is the approved copy. Kris approved it on 2026-11-12 (#885).
- `wp-payloads/ai-policy.html` is the page body built from that copy (#885).
- WordPress holds the page as an unpublished draft. Its ID is `wordpress_id` in `page-meta.json`.
- The draft is one step behind this pack. See "What draft 13005 holds".

## Files

- `policy.md`: the approved copy and the source of truth for every word on the page.
- `SOURCE-MATRIX.md`: the research and local evidence behind each claim.
- `wp-payloads/ai-policy.html`: the body-only payload, one `wp:html` block.
- `page-meta.json`: title, slug, status target, WordPress ID, what the draft holds, proposed excerpt and SEO meta, readback markers, the text that must be gone after publishing, source hashes, approval records and the publish edits.
- `scripts/tests/test_ai_policy_payload.py`: the contract tests.

## How the payload follows the copy

- The `#` title line becomes the WordPress title. The page template renders it as the only H1, so the body starts at H2.
- The review note at the top of `policy.md` has two sentences. The first, "Draft for Kris Krüg's review.", stays out of the body. The second, the scope sentence, is the first paragraph of the body: "This is a proposed public transparency statement, not legal terms, a privacy policy, or a client contract."
- Every other word matches `policy.md`. The tests strip both to plain text and compare them word for word, along with the headings, list items and links.
- `policy.md` has no em dashes and no `--`, so no punctuation changed. The tests refuse both in the copy and in the payload, because WordPress turns `---` and a spaced `--` into an em dash on the public page.
- Each `##` section is an `aurora-proof-section`. "I use AI a lot." is the `aurora-page-lead`. The disclosure sits in an `aurora-card` aside. There are no other classes, no inline CSS, no scripts and no images.
- Headings carry short ids (for example `#what-i-will-not-fake`) so other pages can link to a section.

## Open decision for Kris: keep or drop the scope sentence

#883's architecture decision reads: "The page is a public transparency statement, not legal terms, privacy policy, client contract, or claim of ethical purity." The scope sentence is the only place the page says the first part of that.

An earlier version of this payload removed the whole review note, scope sentence included. Kris's approval on record is "Approve the draft, build it". It does not rule on that sentence either way, so the payload keeps it until he does.

- Keep it: nothing to do. The publish step drops the word "proposed".
- Drop it: remove the paragraph from the payload, its entry in `publish_edits`, its entry in `readback_markers` and its entry in `publish_absent_markers`, then update the tests. Record Kris's words in the PR that does it.

## Four placeholders wait for the publish yes

- `Last updated: YYYY-MM-DD`
- "proposed" in the scope sentence
- The disclosure heading "Proposed AI-assistance disclosure"
- The disclosure prefix "Pending Kris Krüg's review and approval:"

`publish_edits` in `page-meta.json` lists the exact replacements. `publish_absent_markers` lists the pending-only text that must be gone afterwards.

The tests pass in both states and check a different thing in each:

- While `publish_approval` is null, they refuse a filled date, a disclosure that reads as approved, and a scope sentence without "proposed".
- Once `publish_approval` is recorded, they require the date to equal `publish_approval.date`, and they refuse any `YYYY-MM-DD`, "Pending" or "Proposed" text and every entry in `publish_absent_markers`.

In either state they build the other one from the committed files and check that too.

## Publish order (#886)

1. Kris approves the final copy for publication. Record his words and the date in `publish_approval`, set `status_target` to `publish`, and apply `publish_edits` to the payload with that date. Run the tests.
2. Stage that final body in draft 13005 while it is still a draft, together with the excerpt and SEO meta once he approves those. Read it back, and record the new hash and size in `wordpress_draft`. The preview Kris checks is then exactly what goes public.
3. After his yes on that exact preview (#886 step 8), publishing is a status-only flip of that same ID, from `draft` to `publish`. No slug, title or body change happens at that point. This is #886 step 9.
4. Read the public page back logged out. It must contain every entry in `readback_markers` and none in `publish_absent_markers`.

Do not flip the status while the draft still holds a body with placeholders.

## What draft 13005 holds

Draft 13005 still holds the earlier body, staged on 2026-11-13 at 03:24 UTC: SHA-256 `ef5c4fcaebc015713b410cd1eca64dbc0118dddda1a85f5a3287a847cd2597f3`, 14,630 bytes. That is the payload as it stood at commit `7e8a883`, without the scope sentence.

The payload in this pack changed after review and no longer matches the draft. No WordPress call was made for that change. The draft gets the current payload in step 2 of the publish order, when the final body is staged before publishing.

`wordpress_draft` in `page-meta.json` records this, and a test fails if `matches_payload` says anything other than what the two hashes show.

## Changing the copy

Change `policy.md` first and get Kris's approval. Then update the payload and `source.policy_sha256` in `page-meta.json`. The tests fail until all three agree.

## Verification

```bash
python3 -m json.tool content/source-packs/ai-policy-2026/page-meta.json >/dev/null
python3 -m pytest scripts/tests/test_ai_policy_payload.py -q
```

The crawler sentence ("open to search and AI crawlers") is checked against `fixes/robots.txt`. Recheck the live `https://kriskrug.co/robots.txt` before publishing.

## Rollback

The draft is not public. To withdraw it, move that exact page ID to the trash in wp-admin or with a REST `DELETE` without `force`. Never force-delete it. After publication, rollback returns the same ID to `draft`.
