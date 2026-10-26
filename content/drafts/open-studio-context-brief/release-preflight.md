# First-practice release preflight

Preparation for #1105; release owner #983 and transformation #977. **No study has run and no production operation is authorized by this packet.** It reuses [the existing evaluation protocol](evaluation.md), [teaching copy](copy.md) and [blank worksheet](worksheet.md). The first practice contains no runtime AI.

## Frozen candidate and evidence

| Input | Exact version |
|---|---|
| Browser-tested repository | `92a0e8b1475fe737550ddff1a85301a1f08a06ef` |
| Plugin source tree | `a167516a0125c255606db06681403835c37a162d` |
| Proof PR #993 | MERGED, `48e63604d5724c62446ed23e56a567cef17e8930`; #982 CLOSED |
| Teaching PR #991 | MERGED, `7e43d0d4c9395631bd87ad70ee46948b93146679` |
| Entry PR #979 | MERGED, `26d2ec91759d248e140f69fc874bb0e835763064` |
| Method | `0.1-draft`, unchanged |
| Teaching `copy.md` SHA-256 | `2392e31023cbab2f2f41271ab54b5b36958756c6371120819cc6aed78ae6f855` |
| Blank worksheet SHA-256 | `a5e0581dd218ce08924d0ef05fcd066e634e3330e7f45f4ce0b29548dbb4e8f0` |
| Plugin `copy.json` SHA-256 | `8bed22aafd0c2ad5c2f524032f41cf5c6e808b873821d96663ea5a0b59700d61` |
| Evaluation protocol SHA-256 | `e1923b6a64a863c4e911e11f2941f8a705f38a5af20d5a2b1ebccb768b552e3e` |
| Production ZIP SHA-256 | `478f8a4baaabcce6938ae17bf89bc0adab16ae2877f5aa319eb32689d34ee57a` |

Fresh GitHub readback confirmed those merge/issue states. The plugin README records accepted teaching input; PR #991 has no human review or exact-copy approval comment available in the current readback. Preserve that historical statement without promoting merge state into fresh copy/publication approval. The new parent-page wording and contextual CTA below are proposals. #983 retains its explicit copy and live-permission gates.

## Live identity and route readback

Read-only Varlock check: **2026-10-26 04:41 UTC**, October 25 Pacific.

- Source post **12744**, slug `what-i-showed-founders-about-ai-workflows`, status `publish`, modified GMT `2026-09-18T13:00:22`, featured media **12742**. [Canonical source](https://kriskrug.co/2026/09/03/what-i-showed-founders-about-ai-workflows/) returns 200.
- Source raw SHA-256: `529eb87020ba78606e47eea8bd9789eee004097588dc3594d472d966bee46bd1`.
- All-status authenticated exact-slug page lookups find **no** `practice` parent and **no** `context-brief` page. Both `/practice/` and `/practice/context-brief/` return 404 publicly. Recheck immediately before any future creation.
- `OPTIONS /wp-json/wp/v2/pages` advertises GET and POST; the authenticated account has edit/publish-page capabilities. The actual creation route is **POST `/wp-json/wp/v2/pages`**, not the post-only draft CLI. No create was attempted, so write success is unproven.
- Authenticated plugin inventory contains no `kk-practice` entry. The plugin is not installed in this readback. Fixture success does not prove live deployment.
- Existing Events links reach the North House article. The Services page returns 200 but has no North House recap link, and source post 12744 lacks #979's `north-house-next-step` paragraph. Those two merged #979 inserts are not observed live; do not apply them silently with this release.

The desired nested URL needs a **parent page**, an additional reviewed content operation. The child template deliberately uses an unresolved parent token; it is not a ready-to-send payload. Do not use a slash in `slug`, invent a parent ID or silently substitute `/context-brief/`. Resolve the parent plan and exact copy before live permission.

## Page payload and source patch

The private packet is `/Users/kk/Code/kriskrug-wp/.generated/current-state/practice-release-1105-2026-10-25/`. It contains exact JSON templates, page HTML, source before/candidate/diff, readbacks, manifest, tested ZIP and synthetic browser evidence. Nothing there is a publisher command.

Proposed parent payload, for a new draft page only after approval:

```json
{
  "title": "Practice",
  "slug": "practice",
  "status": "draft",
  "parent": 0,
  "content": "<!-- wp:paragraph -->\n<p>Start with <a href=\"https://kriskrug.co/2026/09/03/what-i-showed-founders-about-ai-workflows/\">the North House workflow recap</a>. A short context-brief exercise is being prepared here.</p>\n<!-- /wp:paragraph -->"
}
```

Proposed child template follows. Bind `parent` to the positive integer returned by the verified parent creation/readback. The body includes the **actual saved output** of the existing block's `editor.save`, preserving all six questions as its deactivation fallback; never replace it with a self-closing dynamic block. Review the reused North House image/caption with the page. No new artwork is generated.

```json
{
  "title": "Prepare your AI work brief",
  "slug": "context-brief",
  "status": "draft",
  "parent": "REPLACE_WITH_VERIFIED_PRACTICE_PARENT_ID",
  "content": "<!-- wp:image {\"id\":12742,\"sizeSlug\":\"full\"} -->\n<figure class=\"wp-block-image size-full\"><img src=\"https://kriskrug.co/wp-content/uploads/2026/09/kris-krug-north-house-show-and-tell-2026.jpg\" alt=\"Kris Krüg speaking to founders at North House in Vancouver, with the Futureproof Festival speaker page on the screen behind him\" class=\"wp-image-12742\"/><figcaption>The North House workshop. The photo-walk example below is fictional.</figcaption></figure>\n<!-- /wp:image -->\n\n<!-- wp:kk/context-brief --><section class=\"kk-practice-worksheet\"><h2>Prepare your AI work brief</h2><p>Use the worksheet below. Write your answers in a document or print a copy.</p><section><h3>What are you trying to accomplish?</h3><p>Name the thing you want to make or the decision you need to prepare. Keep it small enough to review in one sitting.</p><p>Not provided. Resolve before relying on this brief.</p></section><section><h3>Who is this for?</h3><p>Name the reader or user. What do they already know, and what should they be able to do with the result?</p><p>Not provided. Resolve before relying on this brief.</p></section><section><h3>What sources or context are available?</h3><p>List the documents, examples or facts the work needs. Say what you have permission to use, what is missing and where an answer still needs checking. Listing a source does not give this exercise or another tool access to it.</p><p>Not provided. Resolve before relying on this brief.</p></section><section><h3>What would a useful result satisfy?</h3><p>Write a few conditions someone could check. Include the format, the essential information and how you will know it is ready. “Make it better” leaves a lot to guess.</p><p>Not provided. Resolve before relying on this brief.</p></section><section><h3>What must remain private or outside the task?</h3><p>Name what must not be shared, assumed or done. Include any actions that need separate permission. If you have not checked a source's sharing permission, keep its contents out.</p><p>Not provided. Resolve before relying on this brief.</p></section><section><h3>What decision or check must remain with a person?</h3><p>Name the person or role who will review the result, what they must check and what they must approve before anyone acts on it.</p><p>Not provided. Resolve before relying on this brief.</p></section><p>Context brief · Method version 0.1-draft · Inspired by the North House recap.</p></section><!-- /wp:kk/context-brief -->"
}
```

Proposed source CTA, inserted once immediately after the existing paragraph beginning “If you want a concrete thing to try” under “One challenge to take home”:

```html
<!-- wp:paragraph -->
<p>Start with one small task. <a href="https://kriskrug.co/practice/context-brief/">Prepare your work brief</a> with six questions, then keep a copy to use with your team or chosen AI tool.</p>
<!-- /wp:paragraph -->
```

The candidate source raw SHA-256 is `ba4295d6ec0cf07f74ba6693998e9ec287e367b896612be83081347d50a1cf08`. It adds one paragraph and preserves every original byte, image, existing link and block in order. The source write, if approved later, sends **content only**; title, status, slug, dates, author, taxonomy, featured media and SEO metadata remain untouched. Never reuse the stale September #979 source hash or replace this article with an old draft.

## Indexing and fallback expectations

The draft pages remain unpublished during review. Once separately approved for publication, the child must return 200 at `/practice/context-brief/`, use a single self-canonical URL without query/fragment, have the reviewed title and ordinary indexable page behavior, and appear in the intended page sitemap. The useful parent should link to the child only after the child passes live checks. Verify actual SEO/header/cache behavior rather than assuming repository settings control production. No robots or redirect change is included in these payloads.

With JavaScript off, all six questions and help remain readable and printable; the page directs the visitor to write answers in a document. With the plugin deactivated, saved worksheet content remains useful at the same URL. The input and output stay memory-only until explicit copy/download/print; no answers attach to Contact. Production cache/nonce/CSP coherence and the absence of third-party script execution require a separate live readback before opening the page to visitors.

## Study readiness

Use the existing A/B crossover protocol and appended blank forms in [evaluation.md](evaluation.md), not a second study. Five consented adults; P1–P4 keep their existing counterbalance and P5 is assigned A/X then B/Y before observations. Condition A is the article plus blank worksheet; B adds the guided exercise. Both tasks remain synthetic during the timed comparison. No model scores the work.

The unchanged primary target is **4/5 usable guided briefs in ten minutes without help** under the existing all-six-dimensions rubric. The separate **3/5 real use within seven days** target requires optional follow-up and a real own-task brief. Exporting a synthetic task is not real use. No reply is unknown. Record assistance, unfinished work and failures without changing thresholds or pooling replacement cohorts.

A human owner records consent and approved private storage/deletion dates before recruitment. No names, contact details or participant answers belong in this repository, public issues or screenshots. Store any identity/contact key separately from coded observations; collect no recordings by default. Keep only aggregate outcomes public. The appended sheets are blank, not fabricated observations.

## Conditional rollout and rollback

All live steps below remain pending approval covering the exact artifact and content operations.

1. Refresh all statuses, slugs and hashes. Snapshot source post 12744, any existing parent/child pages and current plugin state privately (mode 0600). Check for conflicting concurrent edits and existing consumers. If the expected identities/bodies differ, stop and prepare a fresh diff.
2. Verify the reviewed ZIP hash and production-only contents. Install/activate the plugin **before** dependent content. Verify its live privacy/cache behavior in an approved review surface. If this cannot be established safely, do not publish the exercise or its entry link.
3. Resolve/create the approved parent and child drafts through `/pages`. A successful create returns a real ID: read it back and verify slug, type, parent and exact body. If a create times out, do not replay it; search all statuses and reconcile the possible created page first.
4. After copy and live approval, publish the useful parent and then the child, with exact identity/hash guards. Verify canonical/indexing, mobile/keyboard/exports, normal console, analytics/network/storage boundaries, no-JS and saved fallback behavior. Production WordPress and caching differ from the disposable fixture; record their actual versions and headers.
5. Add the source CTA **last**, only after the destination works. Immediately re-fetch post 12744, verify the expected original hash, send its content-only candidate once, then confirm authenticated exact-body readback and normal/cache-bypassed public navigation. Keep #979's separate inserts out of this patch.
6. Roll back the entry CTA first, but only if its current body matches this release's candidate. Restore the child to its approved static worksheet while preserving its public URL. Keep the parent useful. Restore/deactivate the plugin only after checking no remaining page depends on it. Never delete a public page or overwrite a later edit to simplify rollback.

## Verification and ready/pending matrix

At the exact tested commit above, `make practice-test`, `make practice-browser-test` and `make practice-package` pass. The disposable real WordPress fixture is **7.0.4 / PHP 8.2**, using Node **24.22.1**, npm **11.19.1** and local Chromium. It tests 320/390/768/1280px, keyboard-only completion, exact export bytes and copy failure, print, no-JS, actual plugin deactivation, real editor save/reopen, normal console, network/storage/cookie canaries and a separate expected CSP-denial probe. Measured normal-text contrast is **14.88:1** and compressed frontend JS/CSS is **2,984 bytes**. No real participant data or production conversion is used.

The locked development dependency audit reports the new [body-parser denial-of-service advisory](https://github.com/advisories/GHSA-27r3-jxmh-p828) through WordPress Playground/Express. `npm audit` offers no automatic fix for this tree. The fixture is disposable and rebound to loopback, and the production ZIP excludes npm dependencies. This is a separate development-tool dependency follow-up; the audit is not reported clean. Package/lock files are unchanged by this preparation.

| Gate | State |
|---|---|
| Proof code, teaching sources, ZIP and hashes | Ready and frozen above; recheck before release |
| Exact page/CTA proposals and private snapshots | Prepared; parent ID intentionally unresolved |
| Fixture mobile/keyboard/exports/privacy/fallback | Passed; no live-site or real-user claim |
| Voice/doc/diff checks on preparation | Record final results in the linked release-preparation receipt |
| Exact public copy, parent plan and image/caption review | Pending KK's release decision |
| Plugin installation and page/post writes | Pending explicit live permission; none executed |
| Five participants, consent, storage owner/deletion date | Pending human arrangements; no contact made |
| 4/5 ten-minute result and 3/5 seven-day use | Unmeasured; no study performed |
| #979 Services and recap entry inserts | Merged but not observed live; separate scope |
| #983 closure | Blocked on its real release and human evidence; keep open |
