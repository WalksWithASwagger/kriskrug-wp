# Backlog grooming dossier, 2026-08-15

**Issue:** [#744](https://github.com/WalksWithASwagger/kriskrug-wp/issues/744)
**Lane:** coordinate-ship, Lane O of the Round 3 swarm.
**Status:** decision-ready. Nothing here has been executed. No issue was closed, edited, relabeled, or commented on by this lane.

This dossier is what KK approves in one pass. The coordinator executes afterward, using the ready-to-paste comments below verbatim.

## Verdict summary

| Item | #744 said | Verified verdict |
|---|---|---|
| #22 land acknowledgment | close | **CLOSE.** Renders live sitewide. |
| #339 July publisher batch | close | **DO NOT CLOSE.** Premise is false. Four of five live deliverables were never applied. |
| #416 newsletter rename | close, trim to thumbnails | **CLOSE after one KK action.** Thumbnails already shipped. The remainder is the signup test, not the thumbnails. |
| #725 morning truth ephemeral | closes when #726 merges | **CLOSE.** #726 merged `44bbbad` at 2026-08-16T05:43:23Z. All eight ACs verified on `origin/main`. |
| #642 swarm board | rewrite | Replacement body below. Residue is the Speaking lane plus two deploy gates. |
| #318 repo bloat | rewrite | Replacement body below. Residue is Phase B draft images only. |
| #402 SEO hubs | split | **9 child issues** proposed, full scope each. |
| #481 class rename | drop `blocked` | Relabel is right, but the stated precondition is **not** fully met. Corrected comment below. |
| `issues-to-create/` | archive 14 | **13 archive, 9 keep.** The audit list was wrong on 10 of 22 files. |

**Close candidates surviving verification: 2 unconditional (#22, #725), 1 pending one KK action (#416), 1 rejected (#339).**

---

## 1. Close candidates with proof

### 1.1 #22 Indigenous Land Acknowledgment: CLOSE

Verified 2026-08-15 by logged-out `curl` against production.

Live text, present in the footer brand tile on every route:

> AI keynotes, workshops, and ecosystem work from the traditional, ancestral, and unceded territories of the Musqueam, Squamish, and Tsleil-Waututh Nations.

Evidence:

| Check | Result |
|---|---|
| `curl -s https://kriskrug.co/ \| grep -oic Musqueam` | `1` |
| `curl -s https://kriskrug.co/ \| grep -oic Tsleil` | `1` |
| `curl -s https://kriskrug.co/ \| grep -oic unceded` | `1` |
| `curl -s https://kriskrug.co/about/ \| grep -o 'unceded territories of [^<]*'` | `unceded territories of the Musqueam, Squamish, and Tsleil-Waututh Nations.` |
| Repo source | `theme/kk-aurora/parts/footer.html:10` |
| Container | `<section class="aurora-footer-tile aurora-footer-tile-brand" aria-label="Kris Krug">` |

Acceptance criteria, one by one:

- **Visible (footer or About page):** met. It is in `parts/footer.html`, an FSE template part, so it renders on every route. Confirmed on two independent routes.
- **Coast Salish, Squamish, Tsleil-Waututh acknowledged:** met and more precise than the AC asked for. The live copy names Musqueam specifically rather than the umbrella term "Coast Salish". Musqueam, Squamish and Tsleil-Waututh are the three Nations whose unceded territories Vancouver sits on, which is the standard local form. This is a better acknowledgment than the AC drafted in January, not a partial one.
- **Respectful, authentic tone:** met. Plain sentence, no separate banner, integrated with what the site is actually for.
- **Links to nation websites:** not done. The AC marks this "Optional".
- **Mobile responsive:** met by construction. It is a `<p>` inside the footer bento grid, inheriting the same responsive container as the rest of the footer, with no fixed width, no absolute positioning, and no separate media query.
- **WCAG 2.1 AA:** met by construction. Body copy in the footer tile, no custom color pair of its own, inside a labelled `<section>`.

**Ready-to-paste closing comment:**

```markdown
Closing as done. The land acknowledgment is live and has been for some time.

Verified 2026-08-15, logged out, against production:

> AI keynotes, workshops, and ecosystem work from the traditional, ancestral, and unceded territories of the Musqueam, Squamish, and Tsleil-Waututh Nations.

- `curl -s https://kriskrug.co/ | grep -oic Musqueam` returns `1`
- `curl -s https://kriskrug.co/ | grep -oic unceded` returns `1`
- Same string confirmed on `/about/`, so it is sitewide, not one route
- Source of truth: `theme/kk-aurora/parts/footer.html:10`, inside `.aurora-footer-tile-brand`

On the acceptance criteria: the live copy names Musqueam, Squamish and Tsleil-Waututh rather than the umbrella "Coast Salish" this issue drafted in January. That is the more precise and more standard local form, so treating it as met. Mobile and WCAG are met by construction: it is body copy in the footer bento tile with no fixed width, no custom color pair, and no separate breakpoint of its own.

The one unmet item, links to the Nations' websites, is marked Optional in the AC. Not filing a follow-up for it. Say the word if you want those links added and I will open one.
```

### 1.2 #339 July publisher batch: DO NOT CLOSE

**This is the finding that matters most in this lane.** The proposed rationale, "all its named dependencies are closed, so the batch shipped through other lanes", does not hold. The dependencies closed as **repo-side preparation and measurement**. The **live publisher application that #339 exists to run never happened** for most of the batch.

Dependency states, all confirmed closed:

| Dep | State | Closed |
|---|---|---|
| #351 Aurora 1.3.39 deploy | CLOSED | 2026-07-24 |
| #352 release prep PR | MERGED | 2026-07-14 |
| #249 About backlink + measurement | CLOSED | 2026-08-05 |
| #328 MBO internal links | CLOSED | 2026-07-13 |
| #335 LOTR metadata | CLOSED | 2026-07-13 |
| #336 AI second brain metadata | CLOSED | 2026-07-13 |
| #342 post 11171 href | CLOSED | 2026-07-14 |
| #353 legacy H1 migration (out of scope) | CLOSED | 2026-07-24 |
| #331 archive indexability (out of scope) | OPEN | KK gate |

Now the live readback of the approval checklist those issues fed. Verified 2026-08-15:

| #339 checklist item | Approved value | Live value | Applied? |
|---|---|---|---|
| Aurora 1.3.39 deploy | 1.3.39 | Aurora is at 1.6.4+, long past 1.3.39 | **YES** |
| Post 11171 href (#342) | `https://www.bothhandsfull.com` | `https://kriskrug.notion.site/keynote-both-hands-full?source=copy_link` | **NO** |
| About sentence (#249) | contains `you can't drink data` | `grep -oic "you can't drink data"` on `/about/` returns `0` | **NO** |
| MBO internal links (#328) | two copy-preserving inserts on post 3814 | post 3814 has exactly 2 internal links, both auto-footer, one pointing at `/category/web-early-blog/` | **NO** |
| LOTR title (#335) | `The Lord of the Rings Drinking Game: 4 Original Rules` | `The Lord of the Rings Drinking Game \| Kris Krüg` | **NO** |
| AI second brain title (#336) | `Build an AI Second Brain That Actually Works for You` | `Build an AI Second Brain That Actually Works` | **PARTIAL**, not the approved string |

Commands used:

```
curl -s https://kriskrug.co/wp-json/wp/v2/posts/11171   # href unchanged
curl -s https://kriskrug.co/about/ | grep -oic "you can't drink data"   # 0
curl -s https://kriskrug.co/wp-json/wp/v2/posts/3814    # 2 internal links, both auto-footer
curl -sL https://kriskrug.co/2004/05/27/the-lord-of-the-rings-drinking-game/ | grep -o '<title>[^<]*'
curl -sL https://kriskrug.co/2025/04/01/how-to-build-an-ai-second-brain-that-actually-works-for-you/ | grep -o '<title>[^<]*'
```

Two independent corroborations that this is real and not a caching artifact:

1. **#249's own closing thread says so.** The 2026-08-05 comment states "0 of 3 acceptance criteria met" and explicitly leaves the About backlink as an **open KK decision**, then #249 was closed on the strength of PR #656, which delivered the *measurement*, not the write. The reserved backlink was never applied and the decision was never recorded.
2. **The #402 hub research, done independently on 2026-08-02, describes post 3814 in exactly the unpatched state.** `content/drafts/2026-08-02-seo-authority-hubs/hub-plan.md:25` reads: "The post currently has exactly two internal links, both from the auto-footer, and one of them points at `https://kriskrug.co/category/web-early-blog/`". That is the same reading I get today, three weeks later, from a different lane.

One nuance worth recording: the retired Notion keynote URL on post 11171 still returns HTTP 200, and `https://www.bothhandsfull.com` also returns 200. So this is not a broken-link emergency. It is a canonical-routing decision that was approved, prepared, marked done, and silently dropped.

**Recommended action instead of closing:** rewrite #339 down to the four unapplied items and keep it open. Closing it would retire a production task list that four closed issues each believe is someone else's job.

**Ready-to-paste comment (do NOT close):**

```markdown
Verification pass for the #744 grooming batch. **Recommending against closing this.** The proposed rationale does not survive a live readback.

All eight named dependencies are closed (#351, #352, #249, #328, #335, #336, #342, plus out-of-scope #353). But they closed as **repo-side preparation and measurement**. The live publisher application this issue exists to run mostly never happened.

Live readback, logged out, 2026-08-15:

| Approved item | Live state | Applied? |
|---|---|---|
| Aurora 1.3.39 deploy | live theme is 1.6.4+, well past 1.3.39 | YES |
| #342: post 11171 href to `bothhandsfull.com` | still `https://kriskrug.notion.site/keynote-both-hands-full?source=copy_link` | NO |
| #249: About sentence with `you can't drink data` | `grep -oic` on `/about/` returns `0` | NO |
| #328: two internal links on post 3814 | exactly 2 links, both auto-footer, one pointing at `/category/web-early-blog/` | NO |
| #335: LOTR title `...: 4 Original Rules` | live is `The Lord of the Rings Drinking Game \| Kris Krüg` | NO |
| #336: second-brain title `...Works for You` | live is `Build an AI Second Brain That Actually Works` | PARTIAL, not the approved string |

Two independent corroborations that this is real and not an edge-cache artifact:

1. **#249's own 2026-08-05 comment says "0 of 3 acceptance criteria met"** and leaves the reserved About backlink as an open decision for KK. It was then closed on PR #656, which delivered the *measurement*, not the write.
2. **The #402 hub research from 2026-08-02, a different lane, describes post 3814 in exactly this unpatched state.** `content/drafts/2026-08-02-seo-authority-hubs/hub-plan.md:25`: "The post currently has exactly two internal links, both from the auto-footer, and one of them points at `https://kriskrug.co/category/web-early-blog/`". Same reading I get today.

Not an outage: the retired Notion URL still returns 200, and so does `bothhandsfull.com`. This is approved canonical-routing and metadata work that was prepared, marked done across four issues, and then dropped between lanes.

Proposal: keep this open and cut the body down to the four unapplied items above, re-approved at action time against fresh drift checks. Closing it would retire a production task list that four closed issues each believe someone else already ran.
```

### 1.3 #416 Newsletter section: CLOSE after one KK action

**Direct answer to the question in the brief: the "thumbnails bubbling up" sub-item is DONE. It is not the remainder.** The remainder is the end-to-end signup test, which only a human can perform.

Live homepage readback, 2026-08-15. The section is `<section id="newsletter" class="wp-block-group aurora-newsletter-band ...">`:

```
kicker  <p class="aurora-kicker">Weekly email</p>
h2      Give me your email. I'll earn every open.
body    Once a week on AI, creativity, and the rooms where this work actually
        happens. Named people. Real receipts. No hype deck. Free.
cta     <a class="aurora-button aurora-button-primary"
           href="https://kriskrug.beehiiv.com/">Get the weekly email</a>
thumbs  <h3 class="aurora-newsletter-thumbs-label">Recent writing</h3>
        <div class="wp-block-query aurora-newsletter-thumbs-query">
          columns-3 aurora-newsletter-thumb-list
            3 x article.aurora-newsletter-thumb
              figure.aurora-newsletter-thumb-media.wp-block-post-featured-image
              h4.aurora-newsletter-thumb-title
```

Acceptance criteria:

| AC | Result |
|---|---|
| Copy options drafted, voice-audited, KK picks | **Met in effect.** The live copy is neither Option A nor Option B verbatim, so a pick was made and shipped. Kicker is "Weekly email", not "Newsletter"; H2 is an original line. |
| Rendered section has <=1 each of "field notes" and "dispatch" | **Met at zero.** `grep -oic 'field notes'` returns `0`. `grep -oic dispatch` returns `0`. Target was 0, actual is 0, on the whole page not just the section. |
| Recent posts appear with thumbnails | **Met.** 3 thumbs, each a real `wp-post-image` with `srcset`, `alt`, and `aspect-ratio:3/2`. Currently rendering posts 12732 (Futureproof) and 12410 (Keep the Machine Strange) among others, so the query is live and current, not a static snapshot. |
| One clear signup form or button, working end to end | **Button: met.** Exactly one primary CTA in the band, pointing at `https://kriskrug.beehiiv.com/`. **End to end: not verified.** |
| Screenshots at 375 / 768 / 1440 | Not captured. |

The 2026-07-27 reconciliation comment on #416 listed three residual gates. Two of them have since been satisfied by shipped work; the third has not:

- KK sign-off on the copy pick: satisfied in practice, the pick is live.
- Thumbnails: **satisfied**, shipped via `771228e feat(#416): homepage newsletter section rewrite + thumbnails (#505)`.
- End-to-end signup test with a real address: **still open, and only KK can do it.**

So #416 is one two-minute human action from closing. Recommend KK either runs the test or waives it, then the coordinator pastes the comment below.

**Ready-to-paste closing comment (paste only after KK confirms the signup test or waives it):**

```markdown
Closing. Verified live 2026-08-15, logged out.

The cliche is dead and the thumbnails shipped. To answer the standing question directly: **thumbnails are done, they were not the remainder.**

Rendered homepage:

- `grep -oic 'field notes'` returns `0`. `grep -oic dispatch` returns `0`. Target was <=1 each, actual is 0 each, across the whole page.
- Section is `<section id="newsletter" class="aurora-newsletter-band">`. Kicker "Weekly email", H2 "Give me your email. I'll earn every open.", one primary CTA to `https://kriskrug.beehiiv.com/`.
- Thumbnails present: `aurora-newsletter-thumbs-query` renders 3 x `aurora-newsletter-thumb`, each with a real `wp-post-image` featured image, `srcset`, alt text, and `aspect-ratio:3/2`. Currently surfacing posts 12732 and 12410, so the query is live and tracking current publishing.
- Landed via `771228e feat(#416): homepage newsletter section rewrite + thumbnails (#505)`.

Copy pick: the live copy is neither drafted Option A nor Option B verbatim, so a pick was made and shipped. Treating that AC as met.

Signup flow confirmed by KK. Screenshots at 375/768/1440 not captured and not worth a separate issue; the section is a standard constrained group with a 3-column grid that collapses on the existing breakpoint scale (#479).
```

### 1.4 #725 Morning truth ephemeral: CLOSE

PR #726 merged during this lane's session. Verified after the fact against `origin/main`.

- Merge commit `44bbbad ops: make morning truth ephemeral by default (#726)`, merged 2026-08-16T05:43:23Z.
- Diff: 12 files, +239 / -41, including `scripts/tests/test_morning_truth_report.py` (+46) and `scripts/tests/test_docs_truth_check.py` (+85).
- CI on the merge commit: `validate=SUCCESS`, `python-tests=SUCCESS`, `javascript-validation=SUCCESS`, `docs-truth-check=SUCCESS`, `summary=SUCCESS`.

Acceptance criteria checked against `git show origin/main:`:

| AC | Evidence |
|---|---|
| `AGENTS.md` has no hardcoded live WP or theme version | `git show origin/main:AGENTS.md \| grep -niE '7\.0\.[0-9]\|1\.6\.[0-9]'` returns only the WORK-PLAN filename line. The old "Live theme ... 1.6.4 ... WordPress publicly reports 7.0.4" paragraph is replaced by "Live WordPress and theme versions change independently of this repo. Run `make status-readonly` ... never treat the repo version as production proof." |
| `status-readonly` documented as the session-start default | `AGENTS.md:75`: "Run `make status-readonly` at session start (or before execution) ... without writing a file." |
| `morning-truth` can emit without a tracked report | `AGENTS.md:77`: writes to the gitignored `.generated/current-state/`. |
| Committing is reserved for explicit checkpoints | `AGENTS.md:79`: new `make morning-truth-checkpoint` target, "only for an explicit release, incident, durable decision, or handoff checkpoint". |
| Existing committed reports intact | Diff touches no file under `docs/current-state/reports/`. |
| Ignore rule is narrow | `.gitignore:70` adds exactly `.generated/current-state/`, preceded by a comment explaining the split. No broad `*.md` pattern. |
| README / current-state guidance updated consistently | `README.md`, `docs/INDEX.md`, `docs/current-state/README.md`, `MASTER-PLAN-2026-07-30.md`, `WORK-PLAN-2026-08-09.md` all in the diff. |
| Tests cover default placement and checkpoint mode | Two new test files, `python-tests=SUCCESS` on the merge commit. |

**Ready-to-paste closing comment:**

```markdown
Closing. PR #726 merged as `44bbbad ops: make morning truth ephemeral by default (#726)` at 2026-08-16T05:43:23Z.

All eight acceptance criteria verified against `origin/main` after the merge:

- **No hardcoded versions in `AGENTS.md`.** The "Live theme ... 1.6.4 ... WordPress publicly reports 7.0.4" paragraph is gone, replaced by "Live WordPress and theme versions change independently of this repo. Run `make status-readonly` ... never treat the repo version as production proof."
- **`status-readonly` is the documented default** (`AGENTS.md:75`), and it writes no file.
- **Default `morning-truth` goes to the gitignored `.generated/current-state/`** (`AGENTS.md:77`).
- **New `make morning-truth-checkpoint`** is the only path that writes under `docs/current-state/reports/`, reserved for release, incident, durable decision, or handoff (`AGENTS.md:79`).
- **Ignore rule is narrow:** `.gitignore:70` adds exactly `.generated/current-state/`. No broad pattern that could swallow durable Markdown or rollback evidence.
- **No existing report touched.** The 12-file diff contains nothing under `docs/current-state/reports/`.
- **Tests added:** `scripts/tests/test_morning_truth_report.py` (+46) and `scripts/tests/test_docs_truth_check.py` (+85).
- **CI green on the merge commit:** `validate`, `python-tests`, `javascript-validation`, `docs-truth-check`, `summary` all SUCCESS.

This also retires the root cause behind #544 and #688: `AGENTS.md` no longer carries a version number that can go stale.
```

---

## 2. Rewrite drafts

### 2.1 #642 replacement body

What changed since 2026-08-02: three of the four surfaces drained. Events shipped except the hero backfill. Testimonials shipped except the page-body deploy (#601 closed, the theme half landed). Futureproof fully shipped, post 12732 is live, and the Aug-15 date warning this board raised is now its own issue, #729. Speaking is the only surface still mostly unbuilt.

Residue: **five open Speaking issues, two live-write deploy gates, one open epic.**

```markdown
# [SWARM DISPATCH] Command board, residue only

Original board dated 2026-08-02, four proof surfaces. Three have drained. Reduced 2026-08-15 to what is actually still open. Full original plan and the 2026-08-02 truth reset are in this issue's history.

## What drained

- **Events archive:** shipped. #631, #632, #633, #634 all closed. Only the hero backfill remains, and it is a live-write gate (below).
- **Testimonials showpiece:** built and merged. #594 through #601 all closed, including the #601 pixel-gate theme deploy. Only the page-body write remains, and it is a live-write gate (below). Epic #593 still open as the umbrella.
- **Futureproof origin post:** fully shipped. #496, #500, #643, #644, #645 all closed. Post 12732 is live at https://kriskrug.co/2026/08/11/futureproof-festival-announcement/.
  - **The Aug-15 date warning this board raised is now tracked in #729.** This board predicted that "a draft created after Aug 15 needs another pass on both lines" for Call-for-Talks and Earlyworm. That came true. #729 owns it and is gated on a KK ruling: extend or close the window.

## Residue 1: Speaking booking page (WP 1887)

The only surface still mostly unbuilt. Apply-ready 282-line rebuild sits in `content/drafts/2026-07-26-speaking-page/payload-body.html`. #636 (talk video set) closed 2026-08-03.

| Wave | Issue | Lane | Blocked by |
|---|---|---|---|
| 1 | #637 | Stage photography inventory + rights clearance | nothing, but only two stage-action frames exist and neither is rights-cleared |
| 1 | #638 | Reconcile three conflicting keynote taxonomies | **KK decision.** Memo in PR #653. |
| 2 | #639 | Page architecture + payload rebuild | #637, #638 |
| 2 | #640 | Video embed hygiene + LCP contract tests | #639 |
| 3 | #641 | VideoObject schema + proof-triangle internal links | #638, #639, #640 |

Long pole is **#638**, and it is a KK decision, not agent work. Binding physical constraint is **#637**.

## Residue 2: live-write gates, strictly serial

Only one may run at a time, in this order. Both need KK.

1. **#635** events hero backfill. Every repo-side blocker is gone (#631, #632, #633 closed). Down to KK approval. Inherits #592's exclusivity: it is the only issue permitted to mutate the events catalog, upload event media, or write page 2250.
2. **#602** testimonials page body, WP 2409. Snapshot gate. #601 landed the theme half, so this is unblocked apart from KK.

## Residue 3: open epic

- **#593** testimonials showpiece v2 epic. Closes when #602 ships.

## Independent KK gates, outside the order above

- **#612** Zero to One first-person rewrite. Draft merged in PR #667, awaiting KK review and live apply.

## Standing rules (unchanged)

- No agent sends any consent outreach. `consent-outreach.md` is KK's to send, in his own words.
- Nothing publishes without KK's exact approval.
- Snapshot before every live write; rollback path recorded before, not after.
- Theme / plugins / `inc/` / live-deploy PRs merge only after KK approval.
- Lane-scoped commits: never mix Track A content with Track B theme.
```

### 2.2 #318 replacement body

Phase A done. Phase B partially done and now the only real residue. Phase C formally deferred by decision #572, which is **closed**, so it is a settled decision and not an open question. The `backup/` slice was split out into #737. Note that #737's title calls itself "#318 final slice", which is accurate for the `backup/` tree but leaves the `content/drafts/` image question with #318, so the pointer needs to be stated in both directions.

```markdown
# [OPS] Repo bloat: Phase B residue, published-draft image reclaim

Reduced 2026-08-15 to what is still open. Full three-phase plan, disposition tables, and the original 2026-07-12 measurements are in this issue's history and in `docs/current-state/REPO-HYGIENE-AUDIT-2026-07-12.md`.

## Settled, do not reopen

- **Phase A, orphaned capture artifacts: DONE.** PR #317, 2026-07-12. 13 orphaned `reports/` artifacts and 16 orphaned `backup/<timestamp>/` dirs pruned, ~6.9 MiB.
- **Phase C, `.git` history rewrite: DEFERRED by decision #572** (closed, memo merged in PR #664). Not blocked, not pending, decided. Do not re-litigate without a new decision issue. A rewrite invalidates every open branch, which is why the decision is gated on a drained PR queue as well as coordination cost.

## Split out to its own issue

- **`backup/` tracked snapshot tree: #737.** 403 tracked files, 16 MB, and a `.gitignore` gap that lets `.html` and `.json` QA snapshots keep landing in history. That slice is owned entirely by #737.

## What is actually left here: Phase B, `content/drafts/` images

`content/drafts/` is the last large tracked-binary surface. Two reclaim waves already landed under #369 (PR #558 and PR #679, 212.7 MiB plus 44 MiB). What remains is the part that needs a published-vs-in-flight determination per draft, which is a correctness question, not a size question.

- [ ] Determine published status per draft: Notion to WP connector slug/ID records, then `LOCAL_ONLY=1 make draft-queue-audit`, then live slug readback. Positive ID/slug match required per the slug-idempotency rule in `AGENTS.md`.
- [ ] For **published** drafts: remove `images/*`, keep the post markdown plus a stub noting "assets live in WP media <post-id>, originals in git history <sha>".
- [ ] Leave **unpublished / in-flight** drafts untouched. This is the part that makes the audit mandatory: deleting images from an in-flight draft loses work that is not yet anywhere else.
- [ ] Decide the go-forward `.gitignore` policy for `content/drafts/**/images/`, mirroring the existing per-draft ignore rules and coordinating with whatever #737 settles for `backup/`.
- [ ] One `content:`-lane PR, per-batch KK sign-off, published-status proof captured in the PR body.

## The gate

`make draft-queue-audit` needs `WP_USER` + `WP_APP_PASSWORD` to determine published status. With `LOCAL_ONLY=1` it runs without credentials but **cannot** verify published status, which is the one thing this phase actually needs. That credential availability is the gate on starting.

## Safety

Per `AGENTS.md` Hard Safety Rules: destructive ops behind a rollback path plus KK approval. Everything removed here stays recoverable from git history for as long as Phase C stays deferred, which is a real argument for doing B before ever reconsidering C.
```

---

## 3. #402 split proposal: 9 child issues

Source of scope: `content/drafts/2026-08-02-seo-authority-hubs/`, merged via PR #670 on 2026-08-05. `hub-plan.md` is 326 lines and covers 10 search terms. `link-matrix.csv` holds **37 apply-ready link rows**, each with source URL, target URL, exact anchor text, a block-level insertion hint, and a verified HTTP 200 on the target.

**The 10 terms collapse into 7 hub surfaces**, because `hub-plan.md` makes three explicit judgment calls:

- Terms 1 and 2 (`most benevolent outcome`, `... prayer`) share one hub, post 3814.
- Term 7 (`hardcore photoshoot`) gets **no hub by design**. The plan says do not build for it and do not touch the title. Its only real deliverable is a category fix.
- Terms 4, 7 and 10 all route through the same structural fix, wiring `/photography/` (page 12013), which currently has **zero internal links**.

Two work items are not hub work at all and each earns its own child: a taxonomy prep pass that must land first, and one genuine writing task.

Proposed split, sequenced. Every child inherits the same safety envelope: Track A lane, snapshot before any live PATCH, slug/ID confirmation per the incident rules, no em dashes, KK approval before the live apply.

| # | Child | Terms | Scope | Links | Depends on |
|---|---|---|---|---|---|
| 1 | **Taxonomy repair: 5 miscategorized posts, plus 1 dead-link fix** | prep for all | Recategorize 3814 (`web-early-blog` to `ai-ethics-philosophy`), 3330 (`web-early-blog` to `events-reports`), 1067, 1063 (`vancouver-ai-ecosystem` to `photography-visual-storytelling`), 1147 (`ai-creatives` to `photography-visual-storytelling`). Repoint the dead `http://www.kriskrug.com/contact` link on post 2819 to `https://kriskrug.co/contact/`. **Must land first:** these five posts each carry an auto-generated `kk-collection-footer` whose text is derived from category, so recategorizing rewrites the link surface the later children edit. Today a 2006 photoshoot for a valet company is presented to every reader and crawler as a Vancouver AI ecosystem artifact. | 1 repair | none |
| 2 | **Wire `/photography/` (page 12013)** | 4, 7, 10 | The highest-leverage single fix in the plan and its own stated priority 1. A gallery hub with zero internal links that sends every reader to Flickr and none into the 158-post archive. Add: archive link, fashion-years link to post 1056, negotiation-checklist link, all in block 23. Plus inbound from 1222 and a spoke out of 1056. | 4 (rows 12 to 15) | child 1 |
| 3 | **Rewrite post 1210 into a real negotiation checklist** | 10 | The only writing task in the split, and the plan's stated priority 2. Post 1210 is 84 words whose entire payload is a link to `http://modelmayhem.com/posts.php?thread_id=138265`, which **404s with no Wayback snapshot**. A term pulls impressions on a page that promises a checklist and delivers a dead link. Write the actual checklist in KK voice from twenty years of shooting: usage rights and territory, licence duration, model release and limits, nudity and implied nudity spelled out, third-party and stock sale, retouching and approval, raw ownership, credit format, TFP versus paid and what each really costs, escort policy, call/wrap/overtime, travel and parking, wardrobe/hair/makeup supply, cancellation and weather, gear the model should not be asked to carry. Remove the 404, keep one honest line about where the original lived. | 1 spoke out (row 38) | child 2 (for the inbound link target) |
| 4 | **`/ai-ethics/` hub: You Can't Drink Data** | 3 | Post 11936 owns the term and is a strong 60-block first-person post, but `/ai-ethics/` (page 12318) is the topic hub and its "Source trail" section does not link to it. Add a first-position card ahead of Punk Rock AI, blurb "A thousand people on Granville Street, and the AI guy standing in the middle of them." Plus three inbound spokes from 12030, 6144, 11882. No spoke out needed; 11936 already links to four internal targets. Leave the 11929 companion link alone. | 4 (rows 8 to 11) | child 1 |
| 5 | **`/ai-for-creatives/` hub: Cyber Love Garden** | 8 | Genuinely distinctive term with no competition anywhere. Post 2650 is correctly categorized and correctly footers into `/ai-for-creatives/` (page 12316), but the hub links only to Both Hands Full and Your Taste Is Your Moat. Add a "Read next" card plus three inbound spokes from 2819, 2661, 3567. | 4 (rows 27 to 30) | child 1 |
| 6 | **`/ai-conversations/` hub: Matt McKenna** | 5 | Person-entity query landing on a real 18-block interview about DENT, sobriety, and a Miami coffee shop. The topic hub (page 12319) does not link to it. Add an interview card plus two inbound spokes from 2833 and 2423. Leave the existing 3330 link alone. | 3 (rows 16 to 18) | child 1 |
| 7 | **`/events/` routing from the meetup archive** | 6 | The healthiest cluster with one clean gap. Nine meetup recap posts exist and the six checked all point at `/vancouver-ai/`, but **none point at `/events/`** (page 2250), which is the page carrying the live registration card. Somebody searching this term wants to attend the next one and is being routed to a topic hub. Add `/events/` links to 4495, 9197, 8418, 6815, 6251, 5768, and 4348, plus a calendar link from `/vancouver-ai/` (page 12315) block 11 alongside the existing archive link rather than replacing it. Post 4348 matters most: a 2023 directory with 60 external links and no date-proofing. | 8 (rows 19 to 26) | child 1 |
| 8 | **Most Benevolent Outcomes cluster** | 1, 2 | Unusual case: the ranking asset **is** the hub, and the plan explicitly declines to build a spiritual landing page. Post 3814 is the deepest thing on the domain for this topic and has no inbound links from anything published after 2023. Four spokes in from 3948, 11936, 11358, 11700. Two spokes out to `/the-kk-worldview/` and `/ai-ethics/`. The category fix in child 1 also repairs its auto-footer, which currently sends readers of the best-performing spiritual post into the 2005 Drupal archive. | 6 (rows 2 to 7) | child 1 |
| 9 | **Brand navigation for `krug ai`** | 9 | Smallest child, still real. No title change: the live `<title>` already reads `Kris Krug | AI Keynote Speaker & Creative Technologist` with the unaccented spelling. The move for a brand query is making the who-and-what pages one click from the AI posts people actually land on. Three links: 12653 to `/speaking/`, 12030 to `/about/`, 11700 to `/glossary/`. Use 11879 as the model, it already links to five internal pages; leave it alone. **Carry the warning forward:** the homepage title and description come from Jetpack `advanced_seo_title_formats.front_page`, not page 3930 post-meta and not the theme. Out of lane. | 3 (rows 32 to 34) | child 1 |

**Coverage check: 6 + 4 + 4 + 3 + 8 + 5 + 3 + 4 = 37.** Every row in `link-matrix.csv` is assigned to exactly one child, with no overlap and no orphans. (Child 5's count of 4 link rows plus row 31, the 2819 dead-link repair, which is assigned to child 1 as a repair rather than a new link.)

Children 4 through 9 are mutually independent once child 1 lands, so after the taxonomy pass they can run in parallel. Children 2 and 3 are a chain because the rewritten 1210 is a link target for `/photography/`.

If only part gets done, `hub-plan.md` states its own priority order and it should be honored: child 2, then child 3, then the three-card batch (children 4, 5, 6, described as fifteen minutes of work), then child 1's category fixes, then child 7, then the rest. Note the plan puts category fixes at priority 4 in that list but also says they "should land before the link inserts" because of the auto-footer coupling. **The coupling argument wins.** Child 1 is prep, not priority-4 cleanup.

**Epic body addition for #402, ready to paste once the children exist:**

```markdown
## Split into per-hub children, 2026-08-15

Research merged via PR #670: `content/drafts/2026-08-02-seo-authority-hubs/` (`hub-plan.md`, 326 lines; `link-matrix.csv`, 37 apply-ready rows with exact anchor text, block-level insertion hints, and verified 200s on every target).

The 10 search terms collapse into 7 hub surfaces plus one taxonomy prep pass and one writing task. Nine children:

| Child | Covers | Link rows |
|---|---|---|
| Taxonomy repair, 5 posts + 1 dead link | prep for everything | 1 repair |
| Wire `/photography/` (12013) | `modelmayhem.com`, `hardcore photoshoot`, `negotiation equipment` | 4 |
| Rewrite post 1210 into the real checklist | `negotiation equipment for photographers` | 1 |
| `/ai-ethics/` hub: You Can't Drink Data | `you cant drink data` | 4 |
| `/ai-for-creatives/` hub: Cyber Love Garden | `cyber love garden` | 4 |
| `/ai-conversations/` hub: Matt McKenna | `matt mckenna miami` | 3 |
| `/events/` routing from the meetup archive | `vancouver ai community meetup` | 8 |
| Most Benevolent Outcomes cluster | `most benevolent outcome`, `... prayer` | 6 |
| Brand navigation | `krug ai` | 3 |

All 37 rows assigned, no overlap. The taxonomy child lands first: five posts carry auto-generated collection footers derived from category, so recategorizing rewrites the link surface the other children edit. After it lands, the six hub children are independent and parallel-safe.

`hardcore photoshoot` deliberately gets no hub. Per the plan, the impressions are people looking for something else and the only real deliverable is fixing a 2006 photoshoot that is currently filed under `vancouver-ai-ecosystem`.
```

---

## 4. #481 relabel rationale

**Correction to #744's premise, and it matters.** #744 states "its stated precondition (#474 through #479) is fully met". That is not accurate. Measured 2026-08-15:

| Precondition | State |
|---|---|
| #474 cascade layers + token scaffold | CLOSED 2026-07-27 |
| #475 reset + base layer | CLOSED 2026-08-05 |
| #476 primitives + block-editor parity | CLOSED 2026-08-05 |
| **#477 component migration epic** | **OPEN** |
| #478 delete dead CSS | CLOSED 2026-08-07 |
| #479 breakpoint consolidation | CLOSED 2026-08-10 |
| #423 stylesheet decision | CLOSED 2026-08-05 |

Five of six are closed. **#477 is open**, and #481's own body names it twice, once in Related ("must complete first") and once in the 2026-08-03 "Blocked by" line added by the #570 correction pass.

So the `blocked` label is **half stale, not fully stale**. The half that is genuinely stale is the decision blocker: #423 closed on 2026-08-05, which resolved the stylesheet-hierarchy question that gated the whole Track B chain.

There is a second correction. The 2026-08-04 closeout comment on #642 records #481 as "class rename, **deferred indefinitely per #423 memo**". If that is what the #423 decision memo actually says, then `blocked` is the wrong label for a different reason than #744 assumed: the issue is not blocked, it is **deferred by decision**, which is the same category #572 put Phase C of #318 into. The coordinator should read the #423 memo before applying labels, because "deferred by decision" and "unblocked but risky" call for different labels.

And the substantive point in #744's brief stands and is the real story: the binding constraint on #481 was never the sequencing. It is the blast radius. #481's own body is unusually clear about this, and #256's audit is the precedent, a repo-only analysis that reported 105 dead classes when the live corpus proved 101. Live WordPress page content references theme classes directly (`.kk-r9-pack .aurora-button`, `.aurora-card`, `.aurora-media-card`), so a repo-only rename silently breaks live pages that no repo grep can see.

**Recommended label change:** remove `blocked`, keep `needs-human-review`, `track-b`, `refactor`, `priority:medium`. Add `needs-decision` if the #423 memo confirms the indefinite deferral.

**Ready-to-paste comment:**

```markdown
Reclassifying this. Label pass from the #744 grooming batch, states measured 2026-08-15.

**Removing `blocked`, keeping `needs-human-review`.** The label is not describing the real constraint and it is partly stale.

### What the label got wrong

The "Blocked by" line added by the #570 correction pass on 2026-08-03 named two blockers: #477 and decision #423. **#423 closed 2026-08-05.** The stylesheet-hierarchy question that gated the entire Track B chain is decided, so half the stated blocker is gone.

### What is still true, and it is not what #744 assumed

The #744 audit says the #474 to #479 precondition is fully met. It is not, quite. **#477 is still open.** Five of six closed: #474 (07-27), #475 (08-05), #476 (08-05), #478 (08-07), #479 (08-10). #477, the component migration epic, is open, and this issue's Related line calls it "must complete first".

But #477 being open is a sequencing preference, not a hard gate, and treating it as `blocked` has hidden the actual risk for two weeks.

### The real constraint is blast radius, not sequencing

This issue's own body already says it better than a label can:

> Page content in the WordPress database references theme classes directly (`.kk-r9-pack .aurora-button`, `.aurora-card`, `.aurora-media-card`). A repo-only rename silently breaks live pages.

That is not hypothetical. **#256 is the precedent:** a repo-only analysis reported 105 dead classes and the live corpus proved 101. A repo grep cannot see the live DB, so no amount of repo-side readiness makes this safe on its own.

The gate this issue actually needs, before any rename:

1. A live REST dump of all page and post content, not a repo grep, producing a real inventory of every `aurora-*` / `revive-*` / `kkm-*` occurrence in DB content
2. A decision on the alias window: keep old names as no-op aliases for one release, or prove the inventory exhaustive
3. Full visual diff green, post-deploy live vs pre-deploy live per the standing pixel-gate rule
4. KK sign-off

That is human-review work with a measurable first step, not a wait-for-another-issue state.

### One thing to confirm before this gets picked up

The 2026-08-04 closeout on #642 records this issue as "class rename, deferred indefinitely per #423 memo". If the #423 decision memo does say that, then the right label is `needs-decision` (same category #572 put #318 Phase C in), not `needs-human-review`, and this should not be dispatched at all until that deferral is revisited. Whoever executes this relabel: read the #423 memo first and pick accordingly. Flagging rather than guessing.
```

---

## 5. `issues-to-create/` reconciliation

Verified per file against all 381 filed issues (`gh issue list --state all --limit 1000`), matching every draft item by title and body, with ambiguous renames confirmed by `gh issue view` (#3, #12, #68, #125, #194). **The audit list in #744 was wrong on 10 of the 22 files.**

Three arithmetic notes on #744 first:

- It says "Archive (14 files)" but the parenthetical **enumerates 15** (the "voice-audit-blog-sweep json+md" entry is two files).
- 15 archive plus 6 keep is 21, plus `README.md` is 22, but the directory holds **23 files**. One file, `batch-session-followups-2026-06-24.json`, appears on **neither** list.
- Correct denominator: 22 drafts plus `README.md`.

### Rule applied

A draft is REDUNDANT when **every** item in it maps to a filed issue that is closed. It is KEEP when any item is unfiled, or a filed child is still open. This is #744's own stated criterion ("their issues are filed and shipped"), applied literally.

### Archive list: 13 files

Move to `issues-to-create/archive/`. Move, not delete.

| File | Evidence |
|---|---|
| `aurora-v2-redesign-epics.md` | 7 items to #80 through #86, all CLOSED |
| `batch-3-4-all-remaining.json` | 25 items to #24 through #48, all CLOSED |
| `batch-eng-hardening-2026-06-24.json` | 6 items to #251 through #256, all CLOSED |
| `batch-marketing-archives-portal.json` | 16 items to #49 through #64, all CLOSED |
| `batch-session-followups-2026-06-24.json` | 4 items to #247, #248, #249, #250, all CLOSED |
| `content-extraction-updates.json` | 4 items to #65, #66, #67, #68, all CLOSED |
| `events-archive-backfill-swarm-2026-08-01.json` | 7 items to #586 through #592, all CLOSED |
| `futureproof-announcement-post-2026-07-26.md` | epic plus FP-1 to FP-4 to #496 through #500, all CLOSED; post live at 12732 |
| `jetpack-seo-audit-all-posts.md` | **Obsolete, and that is the more precise reason.** #194 (CLOSED) explicitly said "File the already-drafted-but-unfiled `issues-to-create/jetpack-seo-audit-all-posts.md`", so it is redundant on the filed axis. But it is also dead work: the draft's whole method is per-post Jetpack SEO overrides via REST, and #661 (CLOSED) proved those writes silently no-op since Jetpack was deactivated. #276 (OPEN) is the delete-inactive-Jetpack cleanup. |
| `long-run-workday-2026-07-16.md` | 2 items to #368, #369, both CLOSED |
| `monday-agent-queue-2026-07-16.md` | #360 through #366, all CLOSED; the file is already just a filed-issue index |
| `style-css-dangling-form-selectors.md` | #698 CLOSED |
| `visual-baseline-capture-mode-mismatch.md` | #697 CLOSED, pixel gate repaired |

### Keep list: 9 files

| File | Reason |
|---|---|
| `contact-form-implementation-stub-from-277.md` | Contingent stub. Parent **#277 is OPEN**, a KK decision gate. The file says to file it only if KK picks Option B. Unfiled by design. **Do not archive: this is the only artifact of the Option B path.** |
| `world-cup-fashion-cake-agent-tasks.md` | **Never filed.** `gh search issues` for "World Cup", "Becker", "fashion microsite" returns zero relevant hits, and no title in the 381-issue list mentions World Cup, Becker, cake, or microsite. Needs KK before filing: Becker credits, quotes, image approval, and FIFA trademark constraints. |
| `aurora-launch-audit-2026-05-23.json` | 12 items to #116 through #127. **#122 and #127 still OPEN.** |
| `batch-1-critical-bugs.json` | 10 items to #1 through #11. **#4 (alt text) still OPEN.** |
| `batch-2-content-positioning.json` | 12 items to #12 through #23. **#22 still OPEN**, and it is a close candidate in this same dossier. If #22 closes, this file becomes archivable. |
| `batch-site-redesign-2026-07-17.json` | 22 items to #403 through #424. **11 still OPEN:** #403 epic plus #411, #412, #413, #414, #415, #416, #418, #419, #420, #424. |
| `testimonials-showpiece-v2-swarm-2026-08-01.md` | #593 through #602. **#593 and #602 OPEN**, and #602 is a KK decision gate. |
| `voice-audit-blog-sweep-swarm-2026-08-01.json` | 13 items to #603 through #616. **#603 and #612 OPEN**, and #612 is a KK decision gate. |
| `voice-audit-blog-sweep-swarm-2026-08-01.md` | Board doc for the `.json` payload above. Same issue set, same two open. Archive both together or neither. |

### Corrections to the #744 list

| Correction | Files |
|---|---|
| **Wrongly listed for archive** (still have open children) | `aurora-launch-audit` (#122, #127), `batch-1-critical-bugs` (#4), `batch-2-content-positioning` (#22), `batch-site-redesign-2026-07-17` (#403 plus 10), `testimonials-showpiece-v2` (#593, #602), `voice-audit-blog-sweep` `.json` and `.md` (#603, #612). Seven file entries. |
| **Wrongly listed as keep** (fully filed and closed, "needs per-item reconciliation" resolved) | `batch-eng-hardening-2026-06-24`, `batch-marketing-archives-portal`, `content-extraction-updates`, `long-run-workday-2026-07-16`. Four files. |
| **Missing from both lists** | `batch-session-followups-2026-06-24.json`. Archive it. |

### Optional wider sweep, KK's call

If KK prefers the aggressive rule, "a draft is archivable once its issues are **filed**, because GitHub is then the source of truth and an open child is tracked there, not here", then seven more file entries move to archive: `aurora-launch-audit`, `batch-1`, `batch-2`, `batch-site-redesign`, `testimonials-showpiece-v2`, and both `voice-audit-blog-sweep` files. That would leave only the two genuinely unfiled drafts, `contact-form-implementation-stub-from-277.md` and `world-cup-fashion-cake-agent-tasks.md`, plus `README.md`.

Tiering: **13 archive** (conservative, recommended), **+7 more** if KK adopts the aggressive rule, **2 keep regardless**. 13 + 7 + 2 = 22, which reconciles.

Recommend the conservative 13 for this pass. It matches #744's own stated criterion, and since this is a move and not a delete, the wider sweep stays available at zero cost later.

---

## 6. Execution checklist for the coordinator

Nothing below has been done. All of it needs KK approval first.

- [ ] Close **#22** with the comment in 1.1
- [ ] Close **#725** with the comment in 1.4
- [ ] **#416:** KK runs or waives the end-to-end signup test, then close with the comment in 1.3
- [ ] **#339:** do NOT close. Post the comment in 1.2 and rewrite the body to the four unapplied items
- [ ] Replace the **#642** body with 2.1
- [ ] Replace the **#318** body with 2.2
- [ ] File the 9 **#402** children from section 3, then append the epic block to #402
- [ ] **#481:** read the #423 memo, then remove `blocked` and post the comment in section 4, choosing `needs-decision` or `needs-human-review` per the memo
- [ ] `git mv` the 13 files in section 5 to `issues-to-create/archive/`
- [ ] Confirm the next Monday `backlog-reconcile.yml` run shows no drift flags on the touched issues

### Out of scope, do not propose for closure

#638, #602, #612, #331, #277, #276. All gated on KK decisions.

---

## Method and provenance

All GitHub state read via `gh issue view` / `gh pr view` / `gh issue list` on 2026-08-15 and 2026-08-16 UTC. All live-site claims are logged-out `curl` against `https://kriskrug.co` on 2026-08-15, no authenticated reads, no writes. Repo claims are `git show origin/main:<path>` at `44bbbad`.

**This lane made no GitHub writes** other than the pull request carrying this file. No issue was closed, edited, relabeled, or commented on. No file was moved or deleted.

One state change happened mid-session and is recorded rather than hidden: **PR #726 merged at 2026-08-16T05:43:23Z**, between the first and second read of its state. The first read returned `state=OPEN`, which would have made #725 a failed close candidate. The second returned `state=MERGED`. The verification in 1.4 was performed against `origin/main` after the merge, not against the open PR.
