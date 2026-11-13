# AI Policy 2026 Source Pack

Kris Krüg's public AI use policy for `https://kriskrug.co/ai-policy/`. Epic #883.

## Status

- Track A page content. Publishing is a separate yes from Kris (#886).
- `policy.md` is the approved copy. Kris approved it on 2026-11-12 (#885).
- `wp-payloads/ai-policy.html` is the page body built from that copy (#885).
- WordPress holds the page as an unpublished draft. Its ID is `wordpress_id` in `page-meta.json`.

## Files

- `policy.md`: the approved copy and the source of truth for every word on the page.
- `SOURCE-MATRIX.md`: the research and local evidence behind each claim.
- `wp-payloads/ai-policy.html`: the body-only payload, one `wp:html` block.
- `page-meta.json`: title, slug, status target, WordPress ID, proposed excerpt and SEO meta, readback markers, source hashes, approval records and the publish edits.
- `scripts/tests/test_ai_policy_payload.py`: the contract tests.

## How the payload follows the copy

- The `#` title line becomes the WordPress title. The page template renders it as the only H1, so the body starts at H2.
- The review note at the top of `policy.md` stays out of the body.
- Every other word matches `policy.md`. The tests strip both to plain text and compare them word for word, along with the headings, list items and links.
- `policy.md` has no em dashes, so no punctuation changed.
- Each `##` section is an `aurora-proof-section`. "I use AI a lot." is the `aurora-page-lead`. The disclosure sits in an `aurora-card` aside. There are no other classes, no inline CSS, no scripts and no images.
- Headings carry short ids (for example `#what-i-will-not-fake`) so other pages can link to a section.

## Two placeholders wait for the publish yes

- `Last updated: YYYY-MM-DD`
- The disclosure heading "Proposed AI-assistance disclosure" and its "Pending Kris Krüg's review and approval:" prefix.

`publish_edits` in `page-meta.json` lists the exact replacements. While `publish_approval` is null, the tests refuse a filled date or a disclosure that reads as approved. They also prove the edits produce a passing page once approval is recorded.

The excerpt and SEO meta in `page-meta.json` are proposals. They go to WordPress with the publish step, after Kris approves them.

## Changing the copy

Change `policy.md` first and get Kris's approval. Then update the payload and `source.policy_sha256` in `page-meta.json`. The tests fail until all three agree.

## Verification

```bash
python3 -m json.tool content/source-packs/ai-policy-2026/page-meta.json >/dev/null
python3 -m unittest scripts.tests.test_ai_policy_payload
```

The crawler sentence ("open to search and AI crawlers") is checked against `fixes/robots.txt`. Recheck the live `https://kriskrug.co/robots.txt` before publishing.

## Rollback

The draft is not public. To withdraw it, move that exact page ID to the trash in wp-admin or with a REST `DELETE` without `force`. Never force-delete it. After publication, rollback returns the same ID to `draft`.
