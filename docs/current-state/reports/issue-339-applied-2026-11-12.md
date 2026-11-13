# #339 applied, 2026-11-12

**Issue:** [#339](https://github.com/WalksWithASwagger/kriskrug-wp/issues/339), reopened 2026-11-12 (re-verification in #1221).
**Lane:** Track A content only. No theme, template, snippet or cache change.
**Approval:** Kris approved the five changes in chat on 2026-11-12, with his own wording for #249, and then approved running the ten writes in the orchestrating session.
**Window:** 2026-11-13T03:19:13Z to 2026-11-13T03:24:31Z (evening of 2026-11-12, Pacific).
**Packet:** [`content/drafts/339-recut-2026-11-12/`](../../../content/drafts/339-recut-2026-11-12/README.md) holds the targets, guards, markers and rollback steps.

## Preflight

- Guard check (packet step 1): all ten objects `ready` before the first write. Both SEO lines were `ready` again right before the SEO writes.
- About dry run: `DRIFT bytes=+185 first_diff_line=559`, payload SHA-256 `f826de25e0c9`, the reviewed payload.
- Post dry runs: every candidate hash equalled the packet's `after_sha256`.
- SEO dry run: `planned=2 failed=0`. The backfill ran from a checkout with no local env file and no sibling fallback, so it could only use the Varlock credentials.

## Applied objects

| Issue | Object | Tool | Result |
|---|---|---|---|
| #249 | page 1208 `about` | `content_architecture_deploy.py --page about --execute` | updated; marker readback passed |
| #328 | post 2950 | packet step 3 snippet (`apply_issue_834_brand_links.update`) | applied; exact readback |
| #328 | post 2665 | same | applied; exact readback |
| #335 | post 35 | same | applied; exact readback |
| #335 | post 58 | same | applied; exact readback |
| #336 | post 9774 | same | applied; exact readback |
| #336 | post 12327 | same | applied; exact readback |
| #342 | post 11171 | same | applied; exact readback |
| #335 | post 35 SEO title and description | `backfill_meta.py --from-file ... --execute` | written; readback matched |
| #336 | post 8802 SEO title and description | same | written; readback matched |

Each body write sent only `content`. The tool re-read the post after the snapshot, refused if anything had moved, and checked afterwards that categories, tags, featured media, excerpt and meta were unchanged. The SEO writes sent only the two allowlisted meta keys, behind a slug guard.

## Readback

- Guard check after the last write: all ten objects `applied`.
- Logged-out public check, cache-busted and on the plain URL, both passed:
  - `/about/` has one link to You Can't Drink Data.
  - Posts 2950 and 2665 link the approved words to the Most Benevolent Outcomes prayer (post 3814).
  - The "See also" lines on posts 35 and 58 point at each other, and the category archive link is still there.
  - Posts 9774 and 12327 link the approved words to post 8802.
  - Post 11171 links "both hands full" to `https://www.bothhandsfull.com`, and no `keynote-both-hands-full` link is left.
  - The `<title>` on post 35 is `The Lord of the Rings Drinking Game: 4 Original Rules` and on post 8802 it is `Build an AI Second Brain That Actually Works for You`.
- No cache purge was needed. The plain URLs already served the new HTML.
- Posts 35 and 58 still show a link to the 2023 Building AI Companions post (post 4372). It comes from the single template's related-posts list, because post 4372 is filed under Web & Early Blog. It is not in either post body any more.

## Rollback

The snapshots are local only, because this repository is public. They sit under `.generated/current-state/339-recut-2026-11-12/` in the main checkout:

| Object | Snapshot | SHA-256 |
|---|---|---|
| page 1208 | `about/page-1208-about-before.json` | `b45888d7e2d32a3b8a5967861f30a82b42c452f1ae91ec4158d9342d12181f1b` |
| post 2950 | `apply/2950-before-20261113T032233925244Z.json` | `56829204c303204b47fae84421206f9da1f3de8ff23b77c175c6421a37ef8c73` |
| post 2665 | `apply/2665-before-20261113T032238260741Z.json` | `8618ad1b0598874e9ff430ed66ecbcf10c8239dddcb372191783c5080b955d0e` |
| post 35 | `apply/35-before-20261113T032241929144Z.json` | `72176727791b08a139f686e5120f05ee939306a716b0bd702497b65b8054aa5a` |
| post 58 | `apply/58-before-20261113T032245395950Z.json` | `d64f6c3a9de6f6bea75e80e0435d83620734eb8ea19ca16c361bf775a77a29e2` |
| post 9774 | `apply/9774-before-20261113T032248514044Z.json` | `068db3edc5d4dc1addc939a318d28f5cbc6679fb95ade5ac7a303bd5e1330838` |
| post 12327 | `apply/12327-before-20261113T032252868839Z.json` | `4f9249c336912b28556713929f37f573990c8e771c1c86de3122db53e8906f96` |
| post 11171 | `apply/11171-before-20261113T032256566667Z.json` | `8dd8c5e753f8e65fea8fc506f4bb3c49bf36d20bdbc8d7332d9f84c6a567787a` |

The restore commands are in the packet README's Rollback section. The prior SEO values are the packet's `live_before` entries and are also listed in [`seo-overwrite-20261113-032432Z.md`](seo-overwrite-20261113-032432Z.md).
