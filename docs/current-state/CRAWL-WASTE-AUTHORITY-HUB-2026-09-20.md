# Crawl waste and authority-hub policy — #1025

**Issue:** [#1025](https://github.com/WalksWithASwagger/kriskrug-wp/issues/1025)
**Status:** In-repo policy. This file plus [`fixes/issue-1025-crawl-policy.json`](../../fixes/issue-1025-crawl-policy.json) are the robots / sitemap / noindex recommendations. **No live WordPress change.**
**Lane:** Track A (content + SEO ops)
**Does not authorize:** Code Snippets activate, robots.txt edit, Search Console submit, Request Indexing, or page/post PATCH.

Machine-readable twin: [`fixes/issue-1025-crawl-policy.json`](../../fixes/issue-1025-crawl-policy.json).
Prep snippet already on `main` via PR #1029: [`fixes/issue-1025-crawl-hygiene.php`](../../fixes/issue-1025-crawl-hygiene.php) and [`fixes/issue-1025-apply.md`](../../fixes/issue-1025-apply.md).

This pack closes the in-repo half of #1025. Live activate, GSC validation, and paste of the authority module stay KK-gated.

---

## 1. What this issue is for

Make kriskrug.co a cleaner personal authority hub that passes relevant traffic to BC + AI and Futureproof, without spending crawl budget on aliases, share copies, archive feeds, or thin taxonomy surfaces.

Preserve:

- `https://kriskrug.co/feed/`
- `https://kriskrug.co/sitemap.xml` → `/wp-sitemap.xml`
- the physical `robots.txt` at [`fixes/robots.txt`](../../fixes/robots.txt)
- recent post indexability
- #331 archive `noindex, follow` (do not broaden)

---

## 2. Dated GSC before-state (not re-exported)

This session is **in-repo only**. There is no Search Console export here. The numbers below are copied from the #1025 issue body (grounding dated 2026-09-15; coverage last updated Sep 3). Do not treat them as current counts.

| Bucket | Dated claim |
|---|---:|
| Indexed | 1,371 |
| Not indexed | 2,680 |
| Crawled - currently not indexed | 892 |
| Server errors | 10 |
| 404s | 125 |
| Duplicates without user-selected canonical | 33 |

Named classes in that issue, not a fresh URL list: tag feeds, author pagination, `?share=` copies, malformed legacy URLs, thin old posts, and `/home/` as an indexable alias.

Later public readback (2026-09-18, in the apply note) already showed `/home/` 301ing via Redirection and share/amp/nb 301ing via snippet 8. That is dated evidence, not a new probe from this file.

Related triage that already lives in-repo (do not reopen from here):

- [#996](https://github.com/WalksWithASwagger/kriskrug-wp/issues/996) unindexed-primary batch — [`reports/issue-996-unindexed-primary-triage-20260908.md`](reports/issue-996-unindexed-primary-triage-20260908.md)
- [#997](https://github.com/WalksWithASwagger/kriskrug-wp/issues/997) 404 / canonical / 5xx classes — [`reports/issue-997-gsc-url-errors-20260908.md`](reports/issue-997-gsc-url-errors-20260908.md)
- [#331](https://github.com/WalksWithASwagger/kriskrug-wp/issues/331) archive sitemap + robots — [`SEO-ARCHIVE-INDEXABILITY-2026-08-02.md`](SEO-ARCHIVE-INDEXABILITY-2026-08-02.md)

---

## 3. Robots recommendations

**Do not edit** [`fixes/robots.txt`](../../fixes/robots.txt). Live `/robots.txt` is the physical file. The WordPress `robots_txt` filter in [`fixes/robots-txt-ai-policy.php`](../../fixes/robots-txt-ai-policy.php) does not win while that file exists.

Keep exactly these directives:

```txt
Sitemap: https://kriskrug.co/sitemap.xml

User-agent: *
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php
Disallow: /?s=
Disallow: /search/
```

The named AI-crawler group already in that file stays. AI/search discovery is the 2026-06-07 stance.

Do **not** add:

| Tempting rule | Why not |
|---|---|
| `Disallow: /tag/` / `/category/` / `/author/` | #331 already marks those archives `noindex, follow`. A robots block hides followable links and is a policy broaden. |
| `Disallow: /feed/` or `/*/feed/` | The site RSS must stay crawlable. Tag/author feeds are a 301 job, not a robots job. |
| Extra `Sitemap:` lines for news / image / video | Those URLs 404 after Jetpack-off. See [`fixes/robots-txt-update.txt`](../../fixes/robots-txt-update.txt). |

If a later session wants feed suppression in robots.txt, that is a new issue. #1025's accepted path is 301 + stop advertising `rel="alternate"` for tag/author feeds.

---

## 4. Sitemap recommendations

Submit only `https://kriskrug.co/sitemap.xml`.

| Child | Recommendation | Owner when activated |
|---|---|---|
| `wp-sitemap-posts-post-1.xml` | Keep. Do not drop published posts. | core |
| `wp-sitemap-posts-page-1.xml` | Keep pages; drop slug `home` (page 2315) | #1025 snippet |
| Users / category / tag children | Stay out | #331 v2 (snippet 26) |
| Date archives | Stay out (core never listed them) | n/a |

Do not submit `news-sitemap.xml`, `image-sitemap-index-1.xml`, or `video-sitemap-1.xml`.

`/sitemap.xml` → `/wp-sitemap.xml` is an intentional WordPress 301. Do not "fix" it.

---

## 5. Noindex recommendations

Keep the #331 v2 set. Do not add new classes from this issue.

| Surface | Robots | Notes |
|---|---|---|
| Author, tag, category, date, leftover taxonomy archives (including their `/page/N/`) | `noindex, follow` | Already snippet 26 |
| Author `/page/{n}/` for n ≥ 2 | After #1025 activate: 301 to page 1 | Page 1 stays 200 + existing noindex |
| Singular posts and pages | indexable | No bulk noindex of thin legacy |
| `/home/` page | 301 to `/`; drop from page sitemap | Do not unpublish page 2315 from this pack |
| `https://kriskrug.co/feed/` | not a robots-meta surface | Preserve |

Thin legacy posts: keep/improve, merge+301, or noindex **one URL at a time**. Forbidden: bulk delete, bulk Request Indexing. See [`content/drafts/issue-1025-authority-hub/thin-legacy-triage.md`](../../content/drafts/issue-1025-authority-hub/thin-legacy-triage.md).

---

## 6. Crawl-waste patterns found in this repo

Nothing below was deleted. Historical captures stay. Active sources do not mint these URLs.

| Pattern | Where it still appears | Disposition |
|---|---|---|
| Exact `/home/` and `/home` | Apply note; page 2315 still published; alt-text draft cites `/home/` as a public empty-alt URL | Live 301 via Redirection (2026-09-18). Repo fallback + sitemap drop in the #1025 snippet. Theme has no `/home/` hrefs. |
| Nested `/home/{slug}/` attachment leftovers | `backup/20260518-113350/page-snapshots/page-2672-work.html` (`data-permalink="https://kriskrug.co/home/generative-ai-1/#main"` and siblings) | Document only. The snippet is exact-path. Do not 301 `/home/generative-ai-1/`. |
| `?share=` / `nb=` / `amp=` | `docs/current-state/raw/pages/*.html` Jetpack share buttons; snippet 8 source | Historical HTML. Inbound 301 already live (`KK GSC404`). Snippet 8 stays the owner. |
| Tag and author feeds | Apply note (2026-09-18): `/tag/sxsw-sxswi/feed/` and `/author/kk/feed/` still 200 RSS with `rel="alternate"` | Prep 301 + suppress extra feed links. Preserve `/feed/`. Leave category and comments feeds. |
| Author pagination | Apply note: `/author/kk/page/2/` 200, already `noindex, follow`; page 1 still links through `/page/41/` | Prep 301 n ≥ 2 to the first author page. |
| Homepage `/page/{n}/` canonical collision | #997 report + `fixes/issue-997-homepage-paged-canonical.php` | Owned by #997. Do not fold into this snippet. |
| Jetpack-only sitemap URLs in old raw XML | `docs/current-state/raw/sitemap-yoast.xml`, `news-sitemap.xml`, `image-sitemap.xml`, `video-sitemap.xml` | Historical captures. Do not advertise. |

Active `theme/kk-aurora/` has no `/home/` or `?share=` minting. Do not treat backup or `raw/` HTML as a live generator.

---

## 7. Authority hub (paste-ready, not live)

kriskrug.co stays the personal record. BC + AI and Futureproof are the public rooms.

Paste pack: [`content/drafts/issue-1025-authority-hub/`](../../content/drafts/issue-1025-authority-hub/).

| Surface | What to add when KK pastes |
|---|---|
| `/about/`, `/work/`, `/speaking/` | Stable **Organizations and projects** module with descriptive deep links, not homepage-only labels |
| New relevant personal articles | 1–3 contextual deep links to a matching BC + AI program/report or Futureproof page |

Do not duplicate the ALL IN article matrix. That paste set is [#1030](https://github.com/WalksWithASwagger/kriskrug-wp/issues/1030) / [`content/drafts/issue-1030-cross-link-matrix/`](../../content/drafts/issue-1030-cross-link-matrix/).

`twitter:site` is [#1024](https://github.com/WalksWithASwagger/kriskrug-wp/issues/1024). Do not edit it from this pack.

---

## 8. Live follow-on (not this PR)

1. SEO LGTM, then activate [`fixes/issue-1025-crawl-hygiene.php`](../../fixes/issue-1025-crawl-hygiene.php) per the apply note.
2. Paste the organizations module on About / Work / Speaking after a page snapshot.
3. KK submits only `https://kriskrug.co/sitemap.xml` and starts GSC validation. Agents do not Request Indexing.
4. Keep #994 / #995 / #274 on their own clocks.

Rollback for the snippet is deactivate + cache purge. It must not edit content, Redirection, snippet 8, #331, `robots.txt`, or Search Console rows.
