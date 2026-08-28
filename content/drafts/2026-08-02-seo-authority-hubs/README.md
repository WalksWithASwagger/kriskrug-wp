# Authority hubs for the surprising KrisKrug.co search terms

Issue: [#402](https://github.com/WalksWithASwagger/kriskrug-wp/issues/402)
Date of research: 2026-08-02
Lane: Track A. The research files are plans; bounded `fix-*` packs have separate states below.

## What this is

Issue #402 lists ten search terms that already pull impressions on kriskrug.co. This folder
maps each term to the live URL that ranks or should rank, then gives an apply-ready internal
linking plan: hub, spokes, exact anchor text, and where in the body each link goes.

Three files:

| File | What it holds |
|---|---|
| `README.md` | Method, what was verified, what could not be verified |
| `hub-plan.md` | One section per term: hub, spokes, anchors, insertion points, plus the fixes that are not links |
| `link-matrix.csv` | Machine-readable: source_url, target_url, anchor_text, section_hint, http_status |

## Execution status as of 2026-08-28

| Pack | Issue | State |
|---|---:|---|
| `fix-826/` | #826 | Applied and verified 2026-08-18; see `docs/current-state/reports/issue-826-applied-20260818.md` |
| `fix-827/` | #827 | Applied and verified 2026-08-18; see `docs/current-state/reports/issue-827-applied-20260818.md` |
| `fix-828/` | #828 | Drafted and dry-run verified; Kris voice review and a fresh live approval remain |
| `fix-829/` to `fix-832/` | #829-#832 | Prepared only; each needs its own live approval |
| No pack yet | #833-#834 | Issue scope only; #834 remains blocked on #829 and #833 |

## Method

Everything here came from read-only calls against the public site. No auth, no writes, no
connector runs, no REST PATCH.

1. Ran each of the ten terms (plus spelling variants) through
   `https://kriskrug.co/wp-json/wp/v2/search?search=<term>` to find candidate pages.
2. Pulled the full rendered body of every candidate via
   `https://kriskrug.co/wp-json/wp/v2/posts/<id>` and `/pages/<id>` so insertion points reference
   real paragraphs, not guesses.
3. Extracted every existing internal link from each candidate so the plan does not propose
   links that are already there.
4. Pulled the category and tag taxonomy with post counts to find which archive pages could
   carry hub weight.
5. Checked `<title>`, `<meta name="description">`, and `<link rel="canonical">` on the five
   most important ranking URLs.
6. Ran `curl -s -o /dev/null -w '%{http_code}' -L` against every URL cited in `hub-plan.md`
   and `link-matrix.csv`. All 41 unique internal URLs returned 200 on 2026-08-02. A wider set
   of 72 candidate URLs was checked during research; these 41 are what survived into the plan.
7. Checked the outbound links on the ranking posts too, which is how the two dead links below
   surfaced.

## Verified on 2026-08-02

- Every internal URL in `hub-plan.md` and `link-matrix.csv` returns HTTP 200.
- The eight topic hub pages already exist and are published: `/photography/` (12013),
  `/vancouver-ai/` (12315), `/ai-for-creatives/` (12316), `/ai-events/` (12317),
  `/ai-ethics/` (12318), `/ai-conversations/` (12319), `/ai-tools/` (12321),
  `/ai-for-journalists/` (12320), `/indigenous-ai/` (12322). This plan does not propose new
  hub pages. It wires the ones that shipped.
- `/photography/` (page 12013) contains **zero** internal links. It is a curated gallery with
  a Flickr exit and no route to the 158 posts in
  `https://kriskrug.co/category/photography-visual-storytelling/`. That is the single biggest
  structural gap behind three of the ten terms.
- `/ai-ethics/` does not link to `you-cant-drink-data`, which is the post that ranks for the
  term. `/ai-for-creatives/` does not link to the Cyber Love Garden post.
  `/ai-conversations/` does not link to the Matt McKenna post.
- The Vancouver AI meetup recaps already link to `/vancouver-ai/`. Six of them checked, six
  had it. None of them link to `/events/`, which is where the next meetup registration lives.
- Five posts sit in the wrong category. Details in `hub-plan.md` under "Category fixes".
- Two dead outbound links on ranking posts:
  - `http://modelmayhem.com/posts.php?thread_id=138265` returns 404. It is the only
    substantive link on post 1210, the post that ranks for the negotiation term. The Wayback
    Machine returns no snapshot for it (`archived_snapshots: {}`), so the original checklist
    is gone.
  - `http://www.kriskrug.com/contact` on post 2819 returns 000, connection failure. Wrong
    domain, `.com` instead of `.co`.

## What could not be verified

**Search Console query data was not available to this session.** No property access, no API
credentials, no exported CSV in the repo. Everything about ranking position, impression
volume, click-through rate, and which URL Google actually serves for a given query is
therefore **inference from the site's own content**, not measurement.

Concretely, these claims rest on inference:

- "Post X is the page that ranks for term Y." Verified only that post X is the best on-site
  match for the term and that no other page competes for it. Not verified against Search
  Console's page-level query report.
- Every statement about search intent behind a term, including the two calls in `hub-plan.md`
  that a term is an intent mismatch not worth chasing.
- Every prioritization. The ordering in `hub-plan.md` is by structural gap size and effort,
  not by measured impression volume.

Anyone with Search Console access should re-check these before applying. The three specific
questions worth answering first:

1. For `most benevolent outcome`, is the ranking URL post 3814, or is Google serving a
   category or tag archive instead?
2. For `negotiation equipment for photographers`, what is the actual landing page? Post 1210
   is 84 words with a dead link, so if it ranks, the impression source is the title and meta
   description alone.
3. For `hardcore photoshoot` and `modelmayhem.com`, what is the click-through rate? Both are
   flagged here as likely low-value intent. Measured CTR settles it.

Issue #402 also asks for schema guidance (Person, Article, FAQPage, BreadcrumbList) and for
agent docs encoding SEO guardrails. Both touch files outside this lane's ownership
(`AGENTS.md`, `inc/`, theme templates), so they are noted in the PR body rather than edited.

## How to apply

Do not apply the research files directly. Use the matching `fix-*` pack and its runbook.
Issues #826 and #827 are historical applied receipts; #828 through #832 are not live. Every
future write happens post by post through the normal Track A path, dry-run then slug-match then write, per
[`scripts/notion-to-wp/README.md`](../../../scripts/notion-to-wp/README.md).

Two ordering constraints:

1. Do the category fixes before the link inserts. Three of the proposed links are inside the
   auto-generated `kk-collection-footer` block, and that block renders from the post's
   category. Fixing the category rewrites the footer for free.
2. The `/photography/` page inserts are page-content edits on page 12013. That page carries a
   large inline `<style>` block, same pattern as `/about/`. Edit the content, do not
   regenerate it.

## Counting against the acceptance criteria in #402

- Each of the ten terms has a page action: yes, `hub-plan.md` has one section per term.
- At least five internal links from old search-winning posts to current strategic pages:
  `link-matrix.csv` has 37 rows, 19 of which originate on a post published before 2025.
- No keyword stuffing: anchors are written as sentence fragments in KK voice. None of them
  repeat the target term verbatim except where the term is a proper noun, which is the case
  for `Cyber Love Garden`, `Matt McKenna`, and `You Can't Drink Data`.
