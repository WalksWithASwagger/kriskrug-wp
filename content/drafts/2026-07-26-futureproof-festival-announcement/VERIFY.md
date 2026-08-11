# VERIFY — Futureproof Festival announcement (#500)

**Package:** `content/drafts/2026-07-26-futureproof-festival-announcement/`
**Slug:** `futureproof-festival-announcement`
**Target:** WordPress draft only. No public publish.
**Refreshed:** 2026-08-11

## Current result

The repository package is refreshed, the guarded create-only WordPress run succeeded, and the separately authorized final-copy sync is complete.

| Field | Readback |
|---|---|
| WordPress post ID | `12732` |
| Status | `draft` |
| Slug | `futureproof-festival-announcement` |
| Featured media | `12725` |
| Private preview | `https://kriskrug.co/?p=12732` |
| Edit URL | `https://kriskrug.co/wp-admin/post.php?post=12732&action=edit` |

No public publish occurred. Issue #500 completed without updating an existing post; after it closed, a separately authorized sync updated only the private draft's `content` and `excerpt` fields.

## 2026-08-11 release refresh

### Copy and voice

- Visible title: **The Bat Signal: Why I'm Building Futureproof Festival in Vancouver**
- SEO title: **Building Futureproof Festival in Vancouver | Kris Krüg** (54 characters)
- `post.md` and `post.html` contain zero em dashes.
- `voicecheck.py` returned 0 flags across both files.
- Manual Host/Anti-Hero facet review passed; see `voice-audit/`.

### Current public facts

Verified from the official public festival pages on 2026-08-11:

- October 28–30, 2026
- H.R. MacMillan Space Centre, Vancouver
- Earlyworm CA$650 through August 15; standard CA$950; student CA$250; supporter CA$1,650
- Active BC + AI members receive 25% off
- Call for Talks is open through August 15
- Public speaker directory contains 13 profiles; the article links the live directory instead of freezing a roster in body copy
- BC + AI proof points retained from the approved source package: 300 members, 3,000+ attendees, 94+ documented events since 2023

The article sends volatile prices and deadlines to the official festival pages. Recheck those pages again if publication occurs after August 15.

### Links and media

- All 24 unique `http(s)` URLs in `post.md` and `post.html` returned HTTP 200 on 2026-08-11.
- Seven selected local image files resolved and passed the publisher quality gate.
- Lead image: Vancouver AI Meetup #31 stage photograph, Michael Caswell photography and Kris Krüg editing.
- Supporting audience photograph: Michael Caswell.
- Kris approved the copy and visual sequence in the issue flow before the create-only run.

### Publisher verification

```text
dry_run: true
quality gate: pass
images resolved: 7
slug before create: available
create: id 12732
authenticated readback: status=draft, slug=futureproof-festival-announcement, featured_media=12725
final-copy sync: content + excerpt only
post-sync readback: status=draft, title unchanged, featured_media=12725
```

The connector test suite passed: **148 tests**.

## WordPress media receipt

| File | Media ID |
|---|---:|
| `vanai-meetup31-stage-kris-futureproof-slide.webp` | 12725 |
| `vanai-meetup31-audience-wide-shot.webp` | 12726 |
| `futureproof-honest-conversation-poster.png` | 12727 |
| `manifesto-01-future-cultural-question.webp` | 12728 |
| `manifesto-06-who-shapes-us.webp` | 12729 |
| `manifesto-14-places-to-think.webp` | 12730 |
| `futureproof-salmon-starfield-share-20260527.jpg` | 12731 |

Local operational evidence remains gitignored beside this package: `publish.log`, the pre-write REST snapshot, the rollback manifest, and the narrow restore helper.

## Final-copy sync receipt

Kris separately authorized the post-issue private-draft sync on 2026-08-11. The dry-run proved the payload contained only `content` and `excerpt`, with exactly:

- two “Twenty-eight years on the internet” → “Three decades on the internet” replacements;
- one conference-bio phrase refinement;
- the aligned excerpt.

Authenticated post-write readback confirmed:

- `status=draft` and slug unchanged;
- visible title unchanged;
- featured media unchanged at `12725`;
- old phrases absent and new phrases present at the expected counts;
- body SHA-256 `97d0c9042b5763f0917330b78845798f79327107c08c4c97799809ec39d1a4f7`.

Rollback snapshot: `wp-snapshots/rest-post-12732-before-final-copy-sync-20260811T232451Z.json.tmp` (gitignored local evidence).

The repository and private WordPress draft are now copy-aligned. Review the private preview and authorize publication separately; publishing remains outside issue #500 and this sync.
