# Issue #122 — undesigned pages, 2026-08-16 recheck

**Date:** 2026-08-16
**Scope:** re-verify the 24 pages named in the [2026-08-02 inventory](../UNDESIGNED-PAGES-INVENTORY-2026-08-02.md) (PR [#654](https://github.com/WalksWithASwagger/kriskrug-wp/pull/654), the doc that pinned the issue's "~25" estimate at 24), plus a full-site check for any *new* undesigned pages published since.
**Method:** read-only, logged-out HTTP only. No WP auth, no page/theme edit, no live write of any kind.
**Parent issue:** [#122](https://github.com/WalksWithASwagger/kriskrug-wp/issues/122)

---

## Headline result

**All 24 pages from the 2026-08-02 inventory still reproduce as bare-title-plus-legacy-body today.** Zero have been redesigned, retired, redirected, or noindexed in the intervening two weeks.

| Check | Result |
|---|---|
| Pages re-fetched (logged out) | 24 / 24 |
| Still HTTP 200 at the original URL | 24 / 24 |
| Still classify as bare (zero non-wrapper `aurora-*` tokens, no inline `<style>`) | 24 / 24 |
| Redirected to a different URL | 0 / 24 |
| Carrying `noindex` in `<meta name="robots">` | 0 / 24 |
| New pages published site-wide since 2026-08-02 | 0 (`X-WP-Total: 46` then and now; identical 46 page IDs) |
| New undesigned pages found | 0 |

Because the live published-page set is **byte-for-byte the same 46 WP IDs** as two weeks ago, there is no new content-route surface to inventory — the boundary from the last pass still holds exactly. No new pages qualify for addition to this list.

## Method detail

1. Pulled the 24 target rows (ID, slug, URL) straight from [`pages-inventory-2026-08-02.csv`](../pages-inventory-2026-08-02.csv).
2. `GET` each URL logged out (no cookies, no auth header, custom read-only user agent), recorded final HTTP status and any redirect target.
3. Classified each response using the **same discriminator** as the 2026-08-02 doc: count of `aurora-*` class tokens inside `entry-content`, excluding the two wrappers the template always injects (`aurora-page-content`, `aurora-prose`). Zero non-wrapper tokens + no inline `<style>` = still bare. Any non-wrapper token = redesigned with Aurora primitives. Inline `<style>` with zero tokens = bespoke-but-not-Aurora (none of the 24 hit this case, consistent with 2026-08-02).
4. Checked `<meta name="robots">` on all 24 for `noindex`.
5. Re-pulled `GET /wp-json/wp/v2/pages?per_page=100&status=publish` (public, unauthenticated) and diffed the 46 returned IDs against the 46 IDs in the 2026-08-02 CSV — zero adds, zero removals.
6. Re-fetched `/` logged out and re-parsed `<header>` / `<footer class="wp-block-template-part">` for nav membership, to confirm which of the 24 sit in global chrome. Unchanged from 2026-08-02: none in the header's 7-link primary nav; four in the footer (two in a footer nav tile, two in the site-wide `aurora-footer-bottom` copyright bar that renders on all 46 pages).
7. Read live `style.css` — theme is Aurora **1.6.5** in production today. (The repo's tracked line is ahead per `AGENTS.md`; this does not change the page-content classification, since `page.html`'s wrapper classes are stable across the versions checked.)

## Full table — all 24 original pages

`still-bare?` = matches the 2026-08-02 bare-title-plus-body signal today. `disposition` = this pass's recommendation.

| URL | WP ID | HTTP status | Redirected? | Still bare? | Words | Nav | Disposition |
|---|---:|---:|---|---|---:|---|---|
| [/reconciliation-indigenous-land-acknowledgement/](https://kriskrug.co/reconciliation-indigenous-land-acknowledgement/) | 3899 | 200 | no | yes | 135 | footer (copyright bar, all 46 pages) | **must-fix** |
| [/the-kk-worldview/](https://kriskrug.co/the-kk-worldview/) | 3948 | 200 | no | yes | 259 | footer (copyright bar, all 46 pages) | **must-fix** |
| [/motleykrug-podcast/](https://kriskrug.co/motleykrug-podcast/) | 2828 | 200 | no | yes | 903 | footer (Site tile) | **must-fix** |
| [/privacy-policy/](https://kriskrug.co/privacy-policy/) | 2985 | 200 | no | yes | 434 | footer (Utility tile) | **must-fix** |
| [/glossary/](https://kriskrug.co/glossary/) | 11887 | 200 | no | yes | 1209 | no | **must-fix** (best SEO asset in the set) |
| [/ai-upgrade-for-creative-professionals/](https://kriskrug.co/ai-upgrade-for-creative-professionals/) | 6770 | 200 | no | yes | 948 | no | **must-fix** (highest inbound-linked offer, 5 posts) |
| [/cinematic-podcasts-hollywood-grade-storytelling-meets-generative-ai/](https://kriskrug.co/cinematic-podcasts-hollywood-grade-storytelling-meets-generative-ai/) | 7764 | 200 | no | yes | 738 | no | later |
| [/generative-ai-workshop-for-artists-creatives/](https://kriskrug.co/generative-ai-workshop-for-artists-creatives/) | 2603 | 200 | no | yes | 341 | no | later |
| [/art-island-perspectives-from-a-creative-community/](https://kriskrug.co/art-island-perspectives-from-a-creative-community/) | 2543 | 200 | no | yes | 815 | no | later |
| [/sponsor-cyberpunk-chronicles-newsletter/](https://kriskrug.co/sponsor-cyberpunk-chronicles-newsletter/) | 3969 | 200 | no | yes | 1506 | no | later |
| [/product-review-policy-instructions/](https://kriskrug.co/product-review-policy-instructions/) | 3974 | 200 | no | yes | 862 | no | later |
| [/ai-upgrade-for-modern-media-leaders/](https://kriskrug.co/ai-upgrade-for-modern-media-leaders/) | 7610 | 200 | no | yes | 1401 | no | later |
| [/japanese-introduction-page-kaykaysan/](https://kriskrug.co/japanese-introduction-page-kaykaysan/) | 3595 | 200 | no | yes | 209 | no | later (multilingual cluster) |
| [/chinese-introduction-kang-jia/](https://kriskrug.co/chinese-introduction-kang-jia/) | 3598 | 200 | no | yes | 209 | no | later (multilingual cluster) |
| [/russian-introduction-kristofor-kruglov/](https://kriskrug.co/russian-introduction-kristofor-kruglov/) | 3600 | 200 | no | yes | 223 | no | later (multilingual cluster) |
| [/farsi-introduction-khalil-khalifa/](https://kriskrug.co/farsi-introduction-khalil-khalifa/) | 3601 | 200 | no | yes | 209 | no | later (multilingual cluster) |
| [/hindi-introduction-krishna-vishwanathapriyadhanvanshi/](https://kriskrug.co/hindi-introduction-krishna-vishwanathapriyadhanvanshi/) | 3606 | 200 | no | yes | 209 | no | later (multilingual cluster) |
| [/karibu-kwenye-kabila-la-kidijitali-.../swahili-welcome-page/](https://kriskrug.co/karibu-kwenye-kabila-la-kidijitali-la-dunia-la-kris-krug-kuunganisha-dunia-kupitia-lugha-na-teknolojia-swahili-welcome-page/) | 3623 | 200 | no | yes | 391 | no | later (multilingual cluster, surviving Swahili page) |
| [/urdu-language-introduction-kris-krug/](https://kriskrug.co/urdu-language-introduction-kris-krug/) | 3696 | 200 | no | yes | 354 | no | later (multilingual cluster) |
| [/home/](https://kriskrug.co/home/) | 2315 | 200 | no | yes | 449–465* | no | **close-as-wont-fix** (retire: orphan dupe of `/`, redirect target) |
| [/news/](https://kriskrug.co/news/) | 2389 | 200 | no | yes | 37–38* | no | **close-as-wont-fix** (retire: all 3 links already on `/publications/`) |
| [/subscribe/](https://kriskrug.co/subscribe/) | 2808 | 200 | no | yes | 0 | no | **close-as-wont-fix** (retire: header already links beehiiv) |
| [/swahili-introduction-kintu-krowfeather-.../](https://kriskrug.co/swahili-introduction-kintu-krowfeather-karibu-kwenye-kabila-la-kidijitali-la-dunia-la-kris-krug-kuunganisha-dunia-kupitia-lugha-na-teknolojia/) | 3603 | 200 | no | yes | 518 | no | **close-as-wont-fix** (retire: duplicate of 3623, redirect into it) |
| [/ai-upgrade-community-coaching-w-kris-krug-peter-bittner/](https://kriskrug.co/ai-upgrade-community-coaching-w-kris-krug-peter-bittner/) | 6755 | 200 | no | yes | 185 | no | **close-as-wont-fix** (retire pending confirmation offer is dead — open KK question from 2026-08-02, unanswered) |

\* Minor word-count deltas vs. the 2026-08-02 doc (e.g. 449 vs 465, 37 vs 38) come from this pass's simpler HTML-stripping regex, not content edits — both passes agree these pages are effectively unchanged and still bare.

**Disposition tally: 6 must-fix, 13 later, 5 close-as-wont-fix (24 total).**

None of the 24 is actually `noindex`ed or currently redirected — the site has made **zero** progress on this issue since 2026-08-02, including on the free wins (Wave 1 retire candidates were never actioned; KK go/no-go from the original inventory is still outstanding). "Close-as-wont-fix" below means *recommend retire/redirect instead of design spend*, not *already resolved*.

## New pages found on content routes

**None.** `GET /wp-json/wp/v2/pages?per_page=100&status=publish` returns the identical 46 page IDs as the 2026-08-02 baseline — no page has been added, removed, or unpublished. Per the scope note in the task, this check was limited to pages (not posts), matching the issue's own scope.

## Ranking rationale

- **Must-fix (public nav / high traffic):** the four pages in global chrome (`/reconciliation-indigenous-land-acknowledgement/`, `/the-kk-worldview/`, `/motleykrug-podcast/`, `/privacy-policy/`) render on every single page view of the site — the footer bottom bar alone is in 46/46 pages. Plus `/glossary/` (the single best SEO asset in the set per the 2026-08-02 word-count/structure read) and `/ai-upgrade-for-creative-professionals/` (highest inbound-link count of any page in the 24, a real revenue offer). Traffic/inbound-link counts are carried over from the 2026-08-02 doc's link-graph pass (970 posts crawled) and were not re-crawled here — re-running that full crawl for a recheck would be scope creep past what this task asked for; the underlying page set hasn't changed, so those counts are not expected to have shifted meaningfully.
- **Later:** real content with some inbound signal or commercial intent, but no nav exposure and not the top revenue/SEO pages. Includes the six remaining offer/editorial pages and the seven-page multilingual cluster (one shared template fixes all seven at once, per the 2026-08-02 plan).
- **Close-as-wont-fix:** the four original Wave-1 retire candidates (zero inbound links, zero unique value, each redundant with something already live) plus the coaching offer page flagged as possibly dead. Recommend redirect/retire, not redesign — cheapest possible win, and it was already recommended two weeks ago with no action taken.

## What did not change since 2026-08-02

- Nav membership (0 in header, 4 in footer) — re-verified against live rendered HTML today.
- Theme template resolution — all 24 still render through `theme/kk-aurora/templates/page.html`.
- Robots/indexing posture — none noindexed, all still in the live page set (sitemap not re-checked directly this pass, but REST `status=publish` confirms all 24 remain published).
- The four Wave-1 retire decisions and the "is 6755 still a live offer" question from the 2026-08-02 doc are **still open** — no KK decision has landed in the tracked repo or issue thread since.

## Provenance

- `GET https://kriskrug.co/wp-json/wp/v2/pages?per_page=100&status=publish&page=1&_fields=id,slug,link,title,modified,date` — 46 results, `X-WP-Total: 46`, `X-WP-TotalPages: 1`, diffed against `pages-inventory-2026-08-02.csv`
- Logged-out `GET` on all 24 original URLs, custom read-only user agent, no cookies/auth
- `GET https://kriskrug.co/` re-parsed for header/footer nav hrefs
- `GET https://kriskrug.co/wp-content/themes/kk-aurora/style.css` — live theme reads `Version: 1.6.5`
- No WordPress admin session, no REST auth, no file write against the live site

Zero writes of any kind were made against kriskrug.co.
