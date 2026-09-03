# Decision Sheet, 2026-09-03

One page for the rulings that unblock everything else. 32 issues are open and
**30 of them carry a human gate**: 25 `needs-human-review`, 8 `blocked`, 5
`needs-decision`. The bottleneck is decisions, not agent throughput.

Each item below states the ask, the evidence behind it, a recommendation, and
what it would touch if you say yes. **Nothing here has been applied.** Every
live lane is staged to the line before its write and stops there.

---

## 1. #767 security, apply the username-enumeration fix

**Priority: high. This is the one I would do first.**

**Ask:** approve applying the three prepared snippets.

**Evidence, re-verified 2026-09-03 with `scripts/check_user_enumeration.sh`:
4 of 4 checks still FAIL**, which is the documented pre-apply state.

- `GET /wp-json/wp/v2/users` returns 200 and lists two accounts:
  `kk` and the host-provisioned `wpadmin5102`.
- `wp-sitemap-users-1.xml` publishes both `/author/<username>/` archives and is
  linked from `/wp-sitemap.xml`.
- `/?author=1` and `/?author=18` both 301 to username-bearing URLs.
- No HSTS header on the homepage.

The snippets already exist and are unusually careful: `issue-767-hide-rest-users.php`
blocks unauthenticated reads at `rest_pre_dispatch` rather than unregistering
the route, specifically so the block editor's author picker and Site Kit keep
working. `issue-767-disable-author-probes.php` closes `?author=N` while leaving
pretty `/author/<slug>/` archives reachable, because #331 already decided those
stay. There is nothing left to write.

**Recommendation:** approve. Apply the REST and author-probe snippets first,
then re-run the check script. The sitemap half is also covered by activating
#331's v2 snippet, so pick one path and not both.

**Blast radius:** live Code Snippets. Rollback is deactivation. The named risk
is the block editor and Site Kit, and the post-apply checks for both are
written into the snippet header.

---

## 2. #735 brand canon

**Ask:** rule on two things. Organization styling, `BC + AI` or `BC+AI`. And
one canonical descriptor set from the five competing candidates.

**Evidence:** the copy deck records the conflict and refuses to settle it. The
display-name half is already settled: `Kris Krüg` with a diacritic-free ASCII
alternate in schema only.

**Why it matters more than it looks:** this gates the press-kit copy deck, the
25/75/150-word bios, and section 4 of the EPK payload. The payload I shipped
uses only wording already public on the live EPK precisely because this is open.

**Recommendation:** rule on both in one line each. The spaced `BC + AI` already
matches the homepage, About, and the live EPK, so ratifying current usage is the
cheapest correct answer.

**Blast radius:** none directly. It unblocks copy, it does not change a page.

---

## 3. #745 draft queue disposition

**Ask:** approve the dispositions in
[`DRAFT-QUEUE-TRIAGE-2026-09-03.md`](DRAFT-QUEUE-TRIAGE-2026-09-03.md).

**Evidence:** 57 packages triaged. **21 are already published**, which the issue
did not account for, and the batch is 27 packages rather than 28. Recommended:
21 shipped, 6 rewrite, 11 shelve, 19 cull, where cull means move to
`content/drafts/archive/`, not delete.

**Recommendation:** approve by rule rather than row, then let me execute. There
is also one genuine open question in the sheet: whether the 21 shipped packages
should move to a `content/drafts/published/` directory or just get a status
marker in place.

**Blast radius:** local files only. No WordPress write. Moves are reversible.

---

## 4. #830, #831, #832, #833 authority-hub links

**Ask:** approve each apply separately, as the work plan requires.

**Evidence: all four dry-runs ran clean on 2026-09-03, no writes.**

| Issue | Targets | Link rows | What it adds |
|---|---:|---:|---|
| #830 Cyber Love Garden | 4 | 4 | Links into `/ai-for-creatives/` |
| #831 Matt McKenna | 3 | 3 | Links into `/ai-conversations/` |
| #832 meetup recaps | 8 | 8 | Routes recap posts to `/events/` |
| #833 Most Benevolent Outcomes | 5 | 6 | Inbound and outbound worldview links |

**Recommendation:** approve #832 first. It is the largest, it routes to a page
whose art direction is already settled, and it is pure internal linking.

**Blast radius:** live post and page content. Each script snapshots and supports
`--restore`. #834 stays parked: it depends on #833 and has no apply script yet.

---

## 5. #882 press kit publish

**Ask:** approve publishing the rebuilt EPK payload to page 3609.

**Evidence:** dry-run on 2026-09-03 returned `target ok: podcast_epk id=3609
slug=podcast-guesting-page-epk`, one page planned, no writes. The payload landed
in #946 with 24 contract tests. Downloads render only the four assets you
cleared, each with its photographer credit.

**One thing to know before approving:** the repo payload had drifted *behind*
live. The STORYHIVE interview section existed on the live page but not in the
repo, so deploying the old payload would have deleted it. The rebuild restores
it. That drift is why the release checklist now opens with a version-parity step.

**Recommendation:** approve after a visual check on the dry-run diff. Follow
[`press-kit/RELEASE-CHECKLIST.md`](../../content/source-packs/content-architecture-2026/press-kit/RELEASE-CHECKLIST.md).

**Blast radius:** page 3609 body only. Title and slug unchanged. Snapshot and
`--restore` rollback.

---

## 6. #602 testimonials publish

**Ask:** approve the page-2409 body deploy.

**Evidence:** dry-run clean on 2026-09-03, `target ok: testimonials id=2409`,
one page planned, no writes. Its blocker #601 closed on 2026-08-10, so this
waits only on you.

**Recommendation:** approve alongside #882; same deployer, same rollback shape.

**Blast radius:** page 2409 body only.

---

## 7. Smaller calls

| Issue | Ask | Recommendation |
|---|---|---|
| #771 | Publish or park "I Made a Gorgeous Ghost" | Your editorial call; I have no evidence to add. |
| #737 | Untrack 129 backup HTML snapshots + 2 PNGs | Approve. `.gitignore` already excludes `backup/**/*.html`, so the tracked ones are legacy. Archive first, then untrack. |
| #742 | Keep or retire six one-off publisher scripts | Retire, but only after confirming none is referenced by a Makefile target. |
| #424 / #477 | Theme component order | #477's own body says its blockers are stale and recommends doing #424 first. Ratify that and both can move. |

---

## What I would do with a yes

In order of value per unit of your attention: **#767**, because it is a live
security exposure and the fix is written and waiting. Then **#735**, because two
one-line rulings unblock the press kit, the copy deck, and the brand canon.
Then **#832**, the largest staged content lane. Everything else can follow.
