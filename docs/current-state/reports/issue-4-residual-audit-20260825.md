# Issue #4 residual identity and surface audit — 2026-08-25

Track A, read-only live evidence. No WordPress write was made. The audit used
cache-bypassed public HTML plus authenticated `context=edit` GETs; credential
values were never printed.

## Result

- Five Batch 3 rows were stale inventory joins. Duplicate filenames in
  different upload months caused the original join to select media 6481, 8211,
  6729, and 11774.
- The actual featured attachments are 6014, 6126, 6985, 7637, and 8871. All
  five have empty library alt and remain unapplied.
- The path-aware authenticated dry run returns 78 targets: 73
  `already-applied`, five `would-write`, and zero identity failures.
- Two earlier writes landed on unrelated duplicates 6729 and 11774. A scan of
  all 1,019 published post/page edit records found no published use of either
  wrong attachment. Their private pre-write snapshots are mode 0600, preserve
  empty alts, and both restore previews return `would-restore`.
- Page 6815 contains one literal `post_content` image block for media 6835 with
  `alt=""`; the attachment library alt is already descriptive.
- `/home/` is a published, self-canonical orphan page, but its current 13
  rendered images have zero alt violations.
- All 18 current missing-alt-attribute findings are editorial `post_content`,
  not the retired Meta pixel and not theme output.

## Baseline

`make doctor` passed with a credentials warning limited to the process env;
the repo-local environment source remained usable for authenticated GETs.
`make status-readonly` reported a clean, synced `main`, zero open PRs, no extra
worktrees, WordPress 7.0.4, and Aurora live/repo parity at 1.6.9. The declared
snapshot has routine counter drift: zero open PRs observed versus one declared,
43 open issues versus 40, and 66 draft posts versus 65.

## Corrected featured-image identities

Each public page still renders the targeted file with `alt=""`. Authenticated
edit context contains no matching in-body image and identifies the target as
the post's featured attachment.

| Post | Rendered file | Actual media | Current alt | Historical false join | Owning surface |
|---:|---|---:|---|---:|---|
| 6108 | `2024/06/Copy-of-Copy-of-AI-Immortality-w-Guy-Kawasaki-2.png` | 6126 | empty | 6481, whose file is under `2024/07/` | media-library `alt_text` |
| 6937 | `2024/09/MASTER-Blog-header-1.png` | 6985 | empty | 8211, whose file is under `2025/02/` | media-library `alt_text` |
| 7631 | `2024/12/MASTER-Blog-header-1.png` | 7637 | empty | 8211, whose file is under `2025/02/` | media-library `alt_text` |
| 5833 | `2024/06/Copy-of-AI-Immortality-w-Guy-Kawasaki-1.png` | 6014 | empty | 6729, whose file is under `2024/08/` | media-library `alt_text` |
| 8856 | `2025/04/image-19.png` | 8871 | empty | 11774, whose file is under `2026/05/` | media-library `alt_text` |

Media 6481 and 8211 were correctly protected from a write, but for the wrong
reason: they are unrelated attachments with duplicate basenames. Their
meaningful existing alts remain untouched. The inventory now binds all five
rows to their exact upload paths and actual featured IDs.

Media 6729 and 11774 were written before the path-aware guard existed. Their
current alts are the reviewed strings intended for posts 5833 and 8856, but
their upload paths do not match those posts. The intended attachments are 6014
and 8871. The wrong attachments had empty alt before the writes; the exact
private snapshots are:

- `.generated/alt-text-backfill/20260825T033423Z-media-apply/media-6729-before.json`
- `.generated/alt-text-backfill/20260825T033618Z-media-apply/media-11774-before.json`

The restore helper now accepts these historical snapshots only when the
sibling apply report proves one exact `written-verified` value and the live
ID, upload path, and current alt still match. Both authenticated restore dry
runs passed. No restore was applied in this session.

## Page 6815

- URL: `https://kriskrug.co/2024/09/01/august-vancouver-ai-community-meetup-recap-hackers-hustlers-heretics/`
- Post ID / slug: `6815` / `august-vancouver-ai-community-meetup-recap-hackers-hustlers-heretics`
- Exact block: `wp:image` ID 6835, file
  `crowd-shot-vancovuer-ai-1024x683.jpeg`
- Current rendered and raw alt: empty.
- Current attachment 6835 library alt: `Vancouver AI meetup crowd standing
  shoulder to shoulder under magenta light, watching something off frame`.
- Proposed block alt: the same reviewed string above.
- Owning surface: literal `post_content`; a media-library write cannot replace
  the baked empty attribute.

Smallest safe apply path: add a post-aware, single-target content selector to
the existing batch helper with offline tests; dry-run post 6815; verify ID,
slug, media ID, filename, and exactly one empty-alt match; save a private
mode-0600 full edit-context snapshot; change only that tag; read back
`content.raw` and cache-bypassed public HTML. Roll back by restoring the saved
full `content.raw` only if the post has not drifted.

## `/home/`

- WordPress page 2315 remains published and returned cache-bypassed HTTP 200.
- It self-canonicalizes to `https://kriskrug.co/home/` and did not expose a
  robots or Googlebot noindex directive.
- It was last modified `2026-06-17T08:07:38` and is titled `Recent Posts &
  Updates:`.
- Current image audit: 13 images, zero missing attributes, zero empty alts,
  zero filename-style alts.
- The cache-bypassed canonical homepage contained zero exact `/home/` links.
- Authenticated raw-content scan: zero exact inbound `/home/` links across all
  1,019 published posts and pages.

Therefore `/home/` is no longer an issue #4 alt blocker. Its retirement is a
separate information-architecture decision. Existing repo evidence recommends
redirecting the orphan rather than spending design effort on it; KK still owns
the redirect, unpublish, or maintain choice.

## The 18 missing-alt attributes

A cache-bypassed crawl reproduced all 18 identities exactly across six posts.
Authenticated raw edit context proves every one is owned by `post_content`.

| Post | Count | Surface |
|---:|---:|---|
| 41, `/2004/06/29/omg/` | 1 | legacy raw HTML, external Blogspot image |
| 54, `/2004/07/23/spark-online-version-20-brainstorming/` | 1 | legacy raw HTML, local `/images/` path |
| 61, `/2004/08/19/blogging-grows-up/` | 1 | legacy raw HTML, local `/images/` path |
| 2287, `/2017/01/20/sharon-anderson-morris/` | 13 | WordPress image blocks, media 2289-2296, 2298, and 2300-2303 |
| 5371, `/2024/04/19/not-all-white-guys-unpacking-the-wealth-tax-debate-in-canada/` | 1 | raw HTML hotlink to Midjourney CDN |
| 7631, `/2024/12/02/autolume-post-photographic-cybernetic-portraiture/` | 1 | raw HTML hotlink to Googleusercontent |

Surface totals: 13 WordPress image blocks and five legacy/raw-HTML images.
None is the Meta pixel. The five legacy images include three external hotlinks
and two old local `/images/` paths; the two modern hotlinks should be ingested
into the media library before their content tags are rewritten. All 18 still
need visual review before exact alt strings can be approved.

## Repository verification

- TDD regression: the old basename-only verifier accepted a duplicate from the
  wrong upload month; the new exact upload-path guard rejects it.
- Historical rollback regression: a corrected inventory can restore a removed
  wrong target only when its sibling apply report proves the exact
  `written-verified` value and live state has not drifted.
- Focused tests: 25 passed plus two subtests.
- `make test`: 548 repository tests, 12 SEO inventory tests, and 68 SEO
  backfill/link-safety tests passed; plugin/theme smoke checks passed.
- `make validate`: 44 PHP syntax checks and WordPress coding standards passed.
- `make docs-truth-check`, `git diff --check`, sensitive-pattern scan, and CSV
  invariants passed.
- Final authenticated media dry run: 78 targets, 73 `already-applied`, five
  `would-write`, zero refused identities.
- Restore previews for 6729 and 11774: both `would-restore`; no `--apply` used.

## Smallest-safe proposal

1. After explicit KK approval, restore media 6729 and 11774 individually from
   the exact snapshots above. Preview each again first; require current alt to
   equal the historical apply report; write the prior empty value; perform
   authenticated readback.
2. Dry-run media 6014, 6126, 6985, 7637, and 8871 individually. If ID, upload
   path, empty current alt, and proposed alt are exact, apply one at a time with
   private snapshots and authenticated/public readback.
3. Implement and test the post-aware one-row page-6815 content path in its own
   PR. Do not combine that live write with authority-hub work.
4. Keep `/home/` out of issue #4; handle any redirect as a separate approved
   information-architecture change.
5. Visually review the 18 missing-attribute images before drafting or applying
   alts. Ingest the two modern external hotlinks first.
6. Keep #4 open for archive-scope, screen-reader, and WCAG decisions.
