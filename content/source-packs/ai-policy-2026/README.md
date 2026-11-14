# AI Policy 2026 Source Pack

Kris Krüg's public AI use policy for `https://kriskrug.co/ai-policy/`. Epic #883.

## Status

- Track A page content.
- `policy.md` is the approved copy. Kris approved it on 2026-11-12 (#885).
- `wp-payloads/ai-policy.html` is the final page body, with the publish edits applied and the date 2026-11-13.
- Kris approved publication on 2026-11-13 (#886): "Drop the scope line, then publish". `publish_approval` in `page-meta.json` holds the record.
- The orchestrating session writes this body to WordPress page 13005 and publishes it after that ruling. The publish time and the public checks are in `wordpress_page` in `page-meta.json` and in the [publish receipt](../../../docs/current-state/reports/ai-policy-publish-2026-11-13.md).

## Files

- `policy.md`: the approved copy and the source of truth for every word on the page.
- `SOURCE-MATRIX.md`: the research and local evidence behind each claim.
- `wp-payloads/ai-policy.html`: the body-only payload, one `wp:html` block.
- `page-meta.json`: title, slug, status target, WordPress ID, what the page holds, the excerpt, the proposed SEO meta, readback markers, the text that must not be in the body, source hashes, the approval and ruling records, and the publish edits.
- `scripts/tests/test_ai_policy_payload.py`: the contract tests.

## How the payload follows the copy

- The `#` title line becomes the WordPress title. The page template renders it as the only H1, so the body starts at H2.
- The review note at the top of `policy.md` is out of the body. See "The review note" below.
- Every other word matches `policy.md`. The tests strip both to plain text and compare them word for word, along with the headings, list items and links.
- `policy.md` has no em dashes and no `--`, so no punctuation changed. The tests refuse both in the copy and in the payload, because WordPress turns `---` and a spaced `--` into an em dash on the public page.
- Each `##` section is an `aurora-proof-section`. "I use AI a lot." is the `aurora-page-lead`. The disclosure sits in an `aurora-card` aside. There are no other classes, no inline CSS, no scripts and no images.
- Headings carry short ids (for example `#what-i-will-not-fake`) so other pages can link to a section.

## The review note

The note at the top of `policy.md` has two sentences: "Draft for Kris Krüg's review." and the scope sentence, "This is a proposed public transparency statement, not legal terms, a privacy policy, or a client contract."

The first was never in the body. The second stayed in the payload through review, because #883's architecture decision says the page is a public transparency statement and nothing on record removed the sentence. The final body staged for Kris's preview still had it.

Kris then ruled on 2026-11-13: "Drop the scope line, then publish". The whole review note is now out of the body by his decision. `review_note_ruling` in `page-meta.json` holds his words. The tests fail if the sentence comes back, and they fail if that record is missing while the sentence is gone.

## The publish edits

Three placeholders waited for the publish yes, and all three are filled:

- `Last updated: YYYY-MM-DD` is now `Last updated: 2026-11-13`.
- The disclosure heading "Proposed AI-assistance disclosure" is now "AI-assistance disclosure".
- The disclosure prefix "Pending Kris Krüg's review and approval:" is gone.

`publish_edits` in `page-meta.json` keeps the exact replacements, and `publish_absent_markers` lists the pending-only text that must not be in the body.

The tests pass in both states and check a different thing in each:

- With `publish_approval` recorded, as it is now, they require the date to equal `publish_approval.date`, and they refuse any `YYYY-MM-DD`, "Pending" or "Proposed" text and every entry in `publish_absent_markers`.
- With `publish_approval` null, they refuse a filled date and a disclosure that reads as approved.

In either state they build the other one from the committed files and check that too.

## What was written to WordPress

- **Body.** The final body was staged in draft 13005 on 2026-11-13 at 23:56:49 UTC so Kris could preview exactly what would go public: SHA-256 `f8a1ef5be855e9b8ba44a0b2bf7191d1a797caad467056fa0994406384b0e70d`, 14,667 bytes. After his ruling, the scope paragraph came out. The body the page carries is this payload: SHA-256 `97e97a43e33158fb42dac99fac335df20a02ddec2ae76cb8ba8e44b905bb53fd`, 14,562 bytes, which is the staged body minus that one line.
- **Excerpt.** Written with the final body.
- **SEO title and description.** Not written. Pages do not expose `jetpack_seo_html_title` or `advanced_seo_description` over REST, and Kris ruled: "Leave the defaults". The values under `meta` in `page-meta.json` are proposals only.

The orchestrating session made those writes and the publish. `wordpress_page` in `page-meta.json` records the hashes, and a test fails if `matches_payload` says anything other than what the payload's own hash shows.

## Changing the copy

Change `policy.md` first and get Kris's approval. Then update the payload, `source.policy_sha256` and the `wordpress_page` hash in `page-meta.json`. The tests fail until they agree. A change to the live page is a separate write and needs Kris's approval each time.

## Verification

```bash
python3 -m json.tool content/source-packs/ai-policy-2026/page-meta.json >/dev/null
python3 -m pytest scripts/tests/test_ai_policy_payload.py -q
```

The crawler sentence ("open to search and AI crawlers") is checked against `fixes/robots.txt`.

## Rollback

Return page 13005 to `draft`. Do not delete it.
