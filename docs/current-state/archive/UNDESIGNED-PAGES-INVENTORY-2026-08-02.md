# Undesigned pages inventory (issue #122)

**Date:** 2026-08-02
**Scope:** every published WordPress page on kriskrug.co, classified by design state, with a prioritized redesign plan.
**Method:** read-only. Live REST reads plus live rendered-HTML reads. No page was edited.
**Companion data:** [`pages-inventory-2026-08-02.csv`](pages-inventory-2026-08-02.csv) (46 rows, one per published page, machine-readable).
**Revised:** 2026-08-02, second pass. An adversarial verify pass filed six charges against the first version: four wrong numbers, one overstated dependency, one naming problem. Five stood and are fixed, one is partly rebutted. See [Correction log](#correction-log) at the bottom.

---

## Headline numbers

| Metric | Value | How it was measured |
|---|---:|---|
| Published pages | **46** | `X-WP-Total: 46` on `GET https://kriskrug.co/wp-json/wp/v2/pages?per_page=100&status=publish&page=1`, `X-WP-TotalPages: 1` |
| Undesigned (LEGACY + STUB) | **24** | classifier below, run over the rendered `entry-content` of all 46 |
| Already designed | **21** | 16 DESIGNED + 5 DESIGNED-INLINE |
| Template-driven utility | **1** | `/blog/` (posts archive) |
| Pages carrying design CSS inside DB content | **9** (45,590 bytes of CSS, tags excluded) | `<style>` block contents in `content.rendered`, see the byte-method note below |

**The issue's "~25" estimate is correct.** The real number is **24**: 22 LEGACY plus 2 STUB. I would not adjust the issue text, only pin the number.

**Template resolution, actually measured.** 44 of the 46 pages render through the generic `theme/kk-aurora/templates/page.html`. Two do not:

| ID | Route | Template that renders it | Evidence |
|---:|---|---|---|
| 3930 | `/` (front page) | `front-page.html` | `<main id="aurora-main" class="wp-block-group aurora-home-2026 aurora-home-revive aurora-keynote-first …">` |
| 2316 | `/blog/` | `home.html` | `<main id="aurora-main" class="wp-block-group aurora-writing-archive …">`, and `<body class="blog wp-embed-responsive …">` with no `page-template-default` at all |
| the other 44 | everything else | `page.html` | `<main id="aurora-main" class="wp-block-group aurora-page-2026 kk-page …">` |

Method: `curl -sL` on all 46 public URLs, then match the `class` attribute of `<main id="aurora-main">` against the `<main>` class each template file declares. The `<main>` class is the discriminator; the `<body>` class is not. `page-template-default` in `<body class>` only means the page has no custom page-template assigned in post meta, so page 3930 carries it while still being rendered by `front-page.html` under the WP template hierarchy. The first version of this doc claimed all 46 went through `page.html` and cited the body class as proof. That was wrong twice over: wrong for 2316, which does not carry the class, and wrong as a method for 3930, which does carry it but does not use `page.html`.

There are zero *bespoke per-page* templates in the theme, which is the point that matters for #122: `theme/kk-aurora/templates/` holds `404.html`, `archive-marquee_board.html`, `front-page.html`, `home.html`, `index.html`, `page.html`, `single-marquee_board.html`, `single.html`, and nothing page-specific. PR #135 retired the hardcoded per-page ones (see the 2026-05-26 comment on #122). All 24 undesigned pages are inside the 44 on `page.html`.

---

## How each page was classified

I pulled `content.rendered` from the REST API for all 46 pages, then fetched each public URL with `curl -sL` and isolated the `entry-content` container from the live HTML. Four signals decided the bucket:

1. **Aurora pattern markup in the page's own content.** Count of `aurora-*` class tokens inside `entry-content`, excluding the two wrapper classes the template always adds (`aurora-page-content`, `aurora-prose`). A page with `aurora-proof-section`, `aurora-card`, `aurora-media-card`, `aurora-section-kicker`, `aurora-display-heading` is deliberately built. A page with exactly the two wrappers and nothing else is not.
2. **Inline `<style>` in the DB content.** A bespoke design that lives in a `<style>` block rather than the theme.
3. **Core-block-only prose.** Content whose entire class inventory is `wp-block-paragraph`, `wp-block-heading`, `wp-block-list`, `wp-block-separator`, `wp-block-image`. That is the legacy wall.
4. **Word count of the rendered text**, with `<style>` and `<script>` stripped.

Buckets:

| State | Definition | n |
|---|---|---:|
| **DESIGNED** | Aurora pattern markup in the content, or a bespoke block template drives the route | 16 |
| **DESIGNED-INLINE** | No Aurora patterns, but a deliberate bespoke layout whose CSS is a `<style>` block in the DB content | 5 |
| **LEGACY** | Bare `aurora-page-title` plus core-block prose, zero design intent in the content | 22 |
| **STUB** | Under ~50 words of real content | 2 |
| **UTILITY** | No page content at all, route is a template-driven archive | 1 |

Worked example of the discriminator. `/vancouver-ai/` (page 12315) returns **22** `aurora-*` tokens across **8** distinct classes in its own content, wrappers excluded (`aurora-proof-section`, `aurora-section-kicker`, `aurora-display-heading`, `aurora-page-lead`, `aurora-proof-grid`, `aurora-card`, `aurora-media-card`, `aurora-button`), so it is DESIGNED. Counted wrapper-inclusive the same page is 24 tokens across 10 classes; the first version of this doc printed the wrapper-inclusive numbers next to a wrapper-excluded definition, which is the error. `/the-kk-worldview/` (page 3948) returns **0** tokens of its own (2 wrapper-inclusive) and 4 `wp-block-heading` plus 4 `wp-block-list` plus 3 `wp-block-paragraph`, so it is LEGACY.

---

## The 24 undesigned pages

Sorted by wave (rationale further down). `in_p` = distinct published posts linking here. `in_pg` = distinct pages linking here. Word counts are rendered prose, `<style>` stripped.

**Nav is defined as:** the page appears as an `href` inside `nav.aurora-primary-nav` in `theme/kk-aurora/parts/header.html`, or anywhere inside `theme/kk-aurora/parts/footer.html`, **including the `aurora-footer-bottom` copyright bar**. Both parts are global chrome and render on all 46 pages (checked: `aurora-footer-bottom` is present in the rendered HTML of every one of the 46). The header brand logo links to `/` and is not counted as nav.

### Wave 1: retire, do not redesign (4 pages)

Nothing links to any of these, and none of them carry content that does not already exist somewhere better. These are the cheapest win in the whole issue: four 301s and the undesigned surface drops from 24 to 20 with zero design work.

| ID | URL | Title | Words | Modified | in_p | in_pg | Nav | Why retire |
|---:|---|---|---:|---|---:|---:|---|---|
| 2315 | [/home/](https://kriskrug.co/home/) | Recent Posts & Updates: | 465 | 2026-06-17 | 0 | 0 | no | Orphan duplicate front page. The real front page is page **3930**, which renders through `front-page.html` (body class `home`, `aurora-hero-2026` present). `/home/` is a leftover carrying one `wp-block-latest-posts` block. It is in the sitemap and competes with `/`. |
| 2389 | [/news/](https://kriskrug.co/news/) | News | 37 | 2026-06-17 | 0 | 0 | no | Three outbound press links (Georgia Straight x2, Vancouver Is Awesome). I checked all three against page 1895 `/publications/` content: **all three already appear there**. 100% redundant. |
| 2808 | [/subscribe/](https://kriskrug.co/subscribe/) | Stay Connected With Kris Krüg Email Newsletter | 0 | 2023-08-20 | 0 | 0 | no | Zero words. One beehiiv iframe (`embeds.beehiiv.com/552dc13c-76df-4a0b-9663-b7e668042177`). The header already ships a Newsletter link straight to `https://kriskrug.beehiiv.com/`. Untouched since 2023-08-20. |
| 3603 | [/swahili-introduction-kintu-krowfeather-.../](https://kriskrug.co/swahili-introduction-kintu-krowfeather-karibu-kwenye-kabila-la-kidijitali-la-dunia-la-kris-krug-kuunganisha-dunia-kupitia-lugha-na-teknolojia/) | Swahili Introduction | 518 | 2023-10-21 | 0 | 0 | no | **Duplicate of page 3623.** Both embed the same YouTube video `Umwh-EG5YVk`. 3603 has zero inbound links and has not been touched since 2023-10-21; 3623 is the one the source post links to. Keep 3623, redirect 3603 into it. |

KK decision needed on all four. These are live routes in the sitemap, so this is a redirect decision, not an agent decision.

### Wave 2: offer and sales pages (6 pages)

One shared template does all six: hero with the offer name, who it is for, what you get, proof, price or "ask", one CTA. Today every one of them is an `<hr>`-separated wall.

| ID | URL | Title | Words | Modified | in_p | in_pg | Nav | Notes |
|---:|---|---|---:|---|---:|---:|---|---|
| 6770 | [/ai-upgrade-for-creative-professionals/](https://kriskrug.co/ai-upgrade-for-creative-professionals/) | AI Upgrade for Creative Professionals | 948 | 2026-06-29 | 5 | 0 | no | **Highest inbound of any legacy page (5 posts).** 12 images, 16 `<hr>`. Real revenue page. |
| 7610 | [/ai-upgrade-for-modern-media-leaders/](https://kriskrug.co/ai-upgrade-for-modern-media-leaders/) | AI Upgrade for Modern Media Leaders | 1401 | 2026-06-29 | 0 | 0 | no | Longest offer page. 7 images, 12 `<hr>`. Zero inbound: it is being sent by hand, not found. |
| 3969 | [/sponsor-cyberpunk-chronicles-newsletter/](https://kriskrug.co/sponsor-cyberpunk-chronicles-newsletter/) | Cyberpunk Chronicles Newsletter Sponsor Guide | 1506 | 2026-06-17 | 0 | 0 | no | Biggest word count in the legacy set. Commercial. Should reuse the `kk-sponsor-*` treatment already built for `/sponsor-deck/` (page 12625) instead of inventing a new one. |
| 7764 | [/cinematic-podcasts-.../](https://kriskrug.co/cinematic-podcasts-hollywood-grade-storytelling-meets-generative-ai/) | Cinematic Podcasts | 738 | 2026-06-17 | 3 | 0 | no | 3 video embeds, 28 list items. |
| 2603 | [/generative-ai-workshop-for-artists-creatives/](https://kriskrug.co/generative-ai-workshop-for-artists-creatives/) | Generative AI & Creative Potential Workshops | 341 | 2026-06-17 | 2 | 0 | no | Short. One video embed. Closest to the `/services/` offer shape. |
| 6755 | [/ai-upgrade-community-coaching-w-kris-krug-peter-bittner/](https://kriskrug.co/ai-upgrade-community-coaching-w-kris-krug-peter-bittner/) | AI Upgrade Community Coaching w/ Kris Krug & Peter Bittner | 185 | 2026-06-17 | 0 | 0 | no | Thinnest of the six. Ask KK whether this offer still exists before spending design time. Possible Wave 1 retire. |

### Wave 3: policy, statement, reference, editorial (7 pages)

Two sub-templates, both cheap: a "document" layout (heading rhythm, readable measure, last-updated stamp) and a "media story" layout.

| ID | URL | Title | Words | Modified | in_p | in_pg | Nav | Sub-template |
|---:|---|---|---:|---|---:|---:|---|---|
| 11887 | [/glossary/](https://kriskrug.co/glossary/) | AI Glossary | 1209 | 2026-06-26 | 0 | 1 (12321) | no | **Reference / definition list.** 26 `<h3>` terms, 57 paragraphs, 2 callout quotes. The single best SEO asset in the legacy set and it renders as an undifferentiated scroll. Needs an anchored A-Z index and term cards. Do this one first in the wave. |
| 2828 | [/motleykrug-podcast/](https://kriskrug.co/motleykrug-podcast/) | Kris Krüg's MØTLEYKRÜG Podcast | 903 | 2026-06-17 | 3 | 0 | **footer (Site tile)** | Media-card grid. 10 images, 25 links, 10 `wp-block-media-text` blocks. One of the four undesigned pages in global chrome. |
| 2543 | [/art-island-perspectives-from-a-creative-community/](https://kriskrug.co/art-island-perspectives-from-a-creative-community/) | Art Island: Perspectives from a Creative Community | 815 | 2026-06-17 | 1 | 0 | no | Editorial media-text. 7 figures, 3 captions. |
| 3974 | [/product-review-policy-instructions/](https://kriskrug.co/product-review-policy-instructions/) | Product Review Policy & Instructions | 862 | 2026-06-17 | 0 | 0 | no | Document layout. 11 `<h3>`, 28 list items. Orphan but it is a policy page people get pointed at from email. |
| 2985 | [/privacy-policy/](https://kriskrug.co/privacy-policy/) | KK Pledge to Privacy | 434 | 2026-06-17 | 0 | 0 | **footer (Utility tile)** | Document layout. 7 `<h2>`, 7 `<hr>`. Second of the four in global chrome. |
| 3948 | [/the-kk-worldview/](https://kriskrug.co/the-kk-worldview/) | The KK Worldview | 259 | 2026-06-17 | 0 | 0 | **footer (bottom bar)** | Statement. 4 `<h2>` + 16 list items, no images. Linked as "Worldview" from the site-wide copyright bar on all 46 pages, so it is one of only two named links in the site's final line. Would benefit more from an editorial pass than a design pass, and the chrome placement raises the stakes on that. |
| 3899 | [/reconciliation-indigenous-land-acknowledgement/](https://kriskrug.co/reconciliation-indigenous-land-acknowledgement/) | Reconciliation & Indigenous Land Acknowledgement | 135 | 2026-06-17 | 0 | 1 (12322) | **footer (bottom bar)** | Statement with 3 photos. Shortest real page in the set, and linked as "Reconciliation" from the site-wide copyright bar on all 46 pages. Also linked from the `/indigenous-ai/` hub, which is already Aurora-designed, so the contrast is visible to anyone who follows that link. **Do this one first in Wave 3 alongside `/glossary/`:** a land acknowledgement that the whole site points at should not be the least finished page on the domain. |

### Wave 4: the multilingual intro cluster (7 pages)

These are one thing, not seven. Every page in the cluster is: an English or in-language intro paragraph, a YouTube embed of an AI-dubbed intro video, and body copy. They all descend from one 2023 post, [Breaking the Language Barrier](https://kriskrug.co/2023/10/21/breaking-the-language-barrier-my-deepfake-experiment-shocks-and-sparks-debate/) (post 3627), which is the sole inbound link for all of them. Build one "language intro" template with a video hero and a language switcher and ship all seven in a single pass.

| ID | URL | Language | YouTube ID | Words | Modified | in_p |
|---:|---|---|---|---:|---|---:|
| 3595 | [/japanese-introduction-page-kaykaysan/](https://kriskrug.co/japanese-introduction-page-kaykaysan/) | Japanese | `jZDzsvqJMEw` | 209 | 2026-06-17 | 1 |
| 3598 | [/chinese-introduction-kang-jia/](https://kriskrug.co/chinese-introduction-kang-jia/) | Chinese | `4v-fpXJQpzI` | 209 | 2026-06-17 | 1 |
| 3600 | [/russian-introduction-kristofor-kruglov/](https://kriskrug.co/russian-introduction-kristofor-kruglov/) | Russian | `4tMG4BYq9kc` | 223 | 2026-06-14 | 1 |
| 3601 | [/farsi-introduction-khalil-khalifa/](https://kriskrug.co/farsi-introduction-khalil-khalifa/) | Farsi | `k-vgtE8cBcM` | 209 | 2026-06-17 | 1 |
| 3606 | [/hindi-introduction-krishna-vishwanathapriyadhanvanshi/](https://kriskrug.co/hindi-introduction-krishna-vishwanathapriyadhanvanshi/) | Hindi | `cJzLbiXaeJw` | 209 | 2026-06-17 | 1 |
| 3696 | [/urdu-language-introduction-kris-krug/](https://kriskrug.co/urdu-language-introduction-kris-krug/) | Urdu | `FGgTopzrkiQ` | 354 | 2026-06-14 | 1 |
| 3623 | [/karibu-kwenye-kabila-la-kidijitali-.../](https://kriskrug.co/karibu-kwenye-kabila-la-kidijitali-la-dunia-la-kris-krug-kuunganisha-dunia-kupitia-lugha-na-teknolojia-swahili-welcome-page/) | Swahili | `Umwh-EG5YVk` | 391 | 2026-06-17 | 1 |

Note the cluster has no in-language navigation between the pages. Someone who lands on the Hindi page from YouTube has no route to anything except the browser back button. That is a bigger conversion problem than the styling.

---

## Prioritization: how the ranking was built

The ranking signal from the issue is (linked from nav or a high-value page) x (carries real content worth saving) x (externally linked or likely to be landed on).

**Linked-from signal.** Measured, not guessed. I downloaded `content.rendered` for all 970 published posts (`X-WP-Total: 970`) and all 46 pages, extracted every `href`, resolved kriskrug.co-relative and absolute URLs to a page slug, and counted distinct sources. Full counts are in `pages-inventory-2026-08-02.csv`.

**Nav membership, re-derived from the rendered navigation markup.** Corrected on the second pass. The first version said 22 of 24 and named only two footer pages; it missed the `aurora-footer-bottom` copyright bar. The real count is **20 of the 24 undesigned pages are in no global nav at all. Four are in the global footer:**

| ID | Route | Where in the footer |
|---:|---|---|
| 2828 | `/motleykrug-podcast/` | "Site" tile, labelled *Podcast* |
| 2985 | `/privacy-policy/` | "Utility" tile, labelled *Privacy* |
| 3899 | `/reconciliation-indigenous-land-acknowledgement/` | `aurora-footer-bottom` copyright bar, labelled *Reconciliation* |
| 3948 | `/the-kk-worldview/` | `aurora-footer-bottom` copyright bar, labelled *Worldview* |

None of the 24 is in the header nav. The header's `nav.aurora-primary-nav` is exactly seven links: `/about/`, `/work/`, `/speaking/`, `/services/`, `/photography/`, `/blog/`, `/contact/`.

How re-derived: `curl -sL https://kriskrug.co/` then extract every `href` inside `<header>…</header>` and inside the outer `<footer class="wp-block-template-part">`, giving 9 header hrefs and 26 footer hrefs. Cross-checked against the tracked source, `theme/kk-aurora/parts/header.html` and `theme/kk-aurora/parts/footer.html`, where the last two lines of the footer are literally:

```html
<div class="aurora-footer-bottom">
  <p>Copyright 2026 Kris Krug. All rights reserved.</p>
  <p><a href="/reconciliation-indigenous-land-acknowledgement/">Reconciliation</a> / <a href="/the-kk-worldview/">Worldview</a></p>
</div>
```

**Content-worth-saving signal.** Rendered word count plus asset count (images, embeds), both in `pages-inventory-2026-08-02.csv`. The four Wave 1 pages score at or near zero on this.

**External-landing signal (UNVERIFIED).** I have no analytics access from a read-only session. All 46 pages are in `wp-sitemap-posts-page-1.xml` and **none of them carry a `noindex` robots meta**, so every one of them is a live SEO surface. That is the strongest evidence available without Search Console. Three pages have plausible external distribution independent of the site: the seven multilingual pages (linked from YouTube video descriptions, UNVERIFIED), `/podcast-guesting-page-epk/` (already DESIGNED, sent to bookers), and the offer pages (sent by hand in email). **Someone with Search Console or Jetpack Stats access should re-sort Waves 2-4 by actual landing volume before the design work starts.** The wave grouping by shared template holds regardless.

**What this produces.** The retire set is separated out first because it is free. Then offer pages, because they are the only pages in the set with a revenue path. Then the reference and policy set, because `/glossary/` is the best SEO asset in the group and the **four** footer-linked pages are the only ones a visitor can stumble into from global chrome. Then the multilingual cluster, which is the largest single-template win but the least commercially urgent.

The corrected nav count changes the ranking inside Wave 3, not the wave assignment. All four footer-linked pages were already in Wave 3, but `/reconciliation-indigenous-land-acknowledgement/` and `/the-kk-worldview/` were ranked as orphans on the strength of their zero inbound content links. They are not orphans: they are the only two named links in the site-wide copyright bar, which means they carry more chrome exposure than any other page in the 24. Both move to the front of Wave 3 next to `/glossary/`.

---

## Cross-reference: the inline-`<style>` pattern and issue #480

The known repo gotcha, restated from live readback rather than memory:

- `/recent-projects-include/` now **301s to `/work/`**, not the other way round. Verified: `curl -o /dev/null -w '%{http_code} %{redirect_url}'` on `https://kriskrug.co/recent-projects-include/` returns `301 -> https://kriskrug.co/work/`. Page **2672** now owns the slug `work` directly and returns 200. Any doc or memory note that still says "/work/ redirects to /recent-projects-include/" is stale and should be corrected. (`/services/` does still 301 to `/generative-ai-services/`, page 2666.)
- Page 2672's design CSS is a `<style>` block inside its DB content, confirmed: 959 bytes, 14 `!important`, one `::first-letter` rule.

**I found nine pages on this pattern, not six.** Issue #480 tracks six routes at "29 KB". Live readback on 2026-08-02 says nine routes at **45,590 bytes**.

**Byte method, stated precisely.** The figures below are the CSS *inside* each `<style>` element, tags excluded: `re.findall(r'<style[^>]*>(.*?)</style>', content_rendered, re.S)` summed per page, against `GET /wp-json/wp/v2/pages?per_page=100&status=publish&_fields=id,slug,content`. Every one of the nine blocks opens with a bare `<style>` (no attributes), so tag-inclusive counting adds exactly 15 B per page (`<style>` 7 + `</style>` 8) and the tag-inclusive total is **45,725 B**. Each page has exactly one block. The first version of this doc said "counting `<style>...</style>` bytes", which describes the tag-inclusive count while printing the tag-exclusive numbers. The numbers were right, the sentence was not.

| ID | Route | Bytes | `!important` | `::first-letter` | CSS namespace | In #480? |
|---:|---|---:|---:|---:|---|---|
| 1895 | `/publications/` | 15,386 | 0 | 0 | `kk-press-*` | **NO, uncounted** |
| 12625 | `/sponsor-deck/` | 7,752 | 22 | 2 | `kk-sponsor-*` | **NO, uncounted** |
| 2418 | `/contact/` | 5,422 | 17 | 2 | `kk-contact-*` | yes |
| 12013 | `/photography/` | 5,024 | 12 | 1 | `kkx-*` | yes |
| 2666 | `/generative-ai-services/` | 4,418 | 13 | 1 | `kk-services-*` | yes (as `/services/`) |
| 1208 | `/about/` | **3,488** | 25 | 1 | `aurora-*` overrides | yes, but #480 records 959 B |
| 2250 | `/events/` | 2,182 | 0 | 0 | `aurora-event-*` | **NO, uncounted** |
| 1887 | `/speaking/` | 959 | 14 | 1 | `kk-r9-pack` | yes |
| 2672 | `/work/` | 959 | 14 | 1 | `kk-r9-pack` | yes |
| | **Total** | **45,590** | **117** | **9** | | |

(Tags included that total is 45,725 B. #480's own headline number is "29 KB", but the per-route table inside #480 sums to 17,741 B at the byte values it records, so #480 is internally inconsistent as well as short by three routes.)

Two things #480 needs to absorb:

1. **Three uncounted routes.** `/publications/` alone is 15,386 bytes, larger than every route #480 currently lists put together. It is `!important`-free, which makes it the least dangerous but the largest. `/sponsor-deck/` (7,752 B, 22 `!important`) is the second-largest and the most aggressive.
2. **`/about/` grew from 959 B to 3,488 B** since #480 was written, almost certainly when the full-bleed portrait hero landed in Aurora 1.5.7 / PR #618 (2026-08-01). #480's byte table is stale.

Only two of these namespaces have any presence in the tracked theme: `theme/kk-aurora/assets/css/revive-port.css` contains 4 hits for `kk-contact-2026` and 4 for `kk-sponsor`. `kk-press`, `kk-services-2026`, `kkx-hero`, and `kk-r9-pack` appear nowhere in `theme/kk-aurora/`. So for six of the nine routes, **the inline block is the only source of truth for that page's design.** Deleting it without a theme-side replacement un-designs the page.

**What this actually means for #122. Corrected on the second pass: #480 is not a hard blocker for the 24.**

The first version of this doc said "#122 cannot ship cleanly ahead of it" and used that to explain away the unmet "consistent spacing/hero treatment" criterion. That claim does not survive its own data. **All 24 undesigned pages have `inline_css_bytes = 0`.** Cross-check: the nine pages carrying a `<style>` block are 1895, 12625, 2418, 12013, 2666, 1208, 2250, 2672, 1887, and every single one of them is classified DESIGNED or DESIGNED-INLINE. The intersection of "the 24" and "the 9" is empty. A `page.html` spacing or hero change aimed at the 24 would be overridden on exactly zero of them.

The real relationship, stated accurately:

- **Sequencing note, not a block.** #480 matters because after the 24 are fixed, the nine inline-CSS routes would be the remaining odd ones out. If `page.html` gains a new spacing or heading rhythm, those nine keep their old one until #480 retires the inline blocks. That is a site-wide consistency argument about the *other* nine routes, not a dependency of the 24.
- **The one genuine coupling.** If the #122 work changes the `aurora-page-content` / `aurora-prose` selectors themselves rather than only adding new ones, then #480's payload rewrite and the template change have to be coordinated, because six of the nine namespaces (`kk-press`, `kk-services-2026`, `kkx-*`, `kk-r9-pack`) exist nowhere in the theme and their pages would un-design if the inline block were removed without a theme-side replacement. That is a coordination cost on the nine, not a gate on the 24.
- **Practical order.** Doing #480 first is still the tidier sequence and I would recommend it. It is not the reason the third acceptance criterion is unmet. That criterion is unmet because this pass was scoped read-only, inventory-and-plan, and no template work was attempted. See the acceptance-criteria section for the honest version.

---

## Proposed approach and wave sequence

Answering the first acceptance criterion directly: **improve the generic `page.html` template, and add exactly three sub-templates, not one bespoke template per page.** 24 pages is far too many for bespoke treatment, and the evidence says they collapse into three shapes plus a retire pile.

**Wave 0 (recommended first, not a blocker, Track A + Track B, issue #480 not #122).** Retire the nine inline `<style>` blocks into theme CSS. Update #480's route list from six to nine and its byte total from 29 KB to 45,590 B. This is about the nine inline-CSS routes staying consistent with the other 37 after `page.html` changes; it does **not** gate Waves 1 to 4, because none of the 24 target pages carries inline CSS. Rewriting existing `aurora-page-content` / `aurora-prose` rules (as opposed to adding new ones) is the one case where the two issues have to be coordinated.

**Wave 1 (Track A, 4 pages, no design work).** Retire `/home/`, `/news/`, `/subscribe/`, and the duplicate Swahili page 3603. Four 301s. Drops the undesigned count from 24 to 20. **Needs KK's go/no-go on each redirect target.**

**Wave 2 (6 pages).** One "offer" sub-template covering `/ai-upgrade-for-creative-professionals/`, `/ai-upgrade-for-modern-media-leaders/`, `/sponsor-cyberpunk-chronicles-newsletter/`, `/cinematic-podcasts-.../`, `/generative-ai-workshop-for-artists-creatives/`, `/ai-upgrade-community-coaching-.../`. The `kk-sponsor-*` treatment on `/sponsor-deck/` and the `kk-services-*` treatment on `/generative-ai-services/` are both already-built precedents. Do not invent a third. Ask KK first whether 6755 is a live offer.

**Wave 3 (7 pages).** Two sub-templates. "Document" for `/privacy-policy/`, `/product-review-policy-instructions/`, `/the-kk-worldview/`, `/reconciliation-indigenous-land-acknowledgement/`. "Media story / grid" for `/motleykrug-podcast/` and `/art-island-.../`. `/glossary/` needs its own anchored definition layout and should be split out and shipped first, on its own, because it is the highest-value SEO page in the set. Order inside the wave, after the nav correction: `/glossary/` and `/reconciliation-indigenous-land-acknowledgement/` first, then `/the-kk-worldview/` and `/privacy-policy/`, then `/motleykrug-podcast/`, then the two with no chrome exposure.

**Wave 4 (7 pages).** One "language intro" sub-template with a video hero and a cross-language switcher, applied to all seven surviving multilingual pages in one pass. Add the switcher regardless of the design work: right now there is no route between them.

Total: 24 pages, four waves, three new sub-templates.

---

## What needs KK

1. **Four retire decisions (Wave 1).** `/home/` → `/`, `/news/` → `/publications/`, `/subscribe/` → beehiiv or the footer signup, Swahili 3603 → 3623. These are live indexed routes; an agent should not 301 them unilaterally.
2. **Is `/ai-upgrade-community-coaching-w-kris-krug-peter-bittner/` (6755) still a live offer?** 185 words, zero inbound, untouched since 2026-06-17. If it is dead it moves to Wave 1 and Wave 2 becomes five pages.
3. **Search Console or Jetpack Stats readback** to re-sort Waves 2-4 by real landing volume. Everything about external traffic in this document is UNVERIFIED.
4. **Confirm the Wave 0 ordering**, that is, whether #480 lands before any generic-template change under #122. Recommended but optional: none of the 24 carries inline CSS, so Waves 1 to 4 can proceed without it.
5. **`/the-kk-worldview/` (3948) may need an editorial rewrite, not a redesign.** 259 words, no images, zero inbound content links, but it is one of the two links in the site-wide copyright bar. Design will not fix the copy.
6. **Both copyright-bar pages are the least finished pages on the site.** `/reconciliation-indigenous-land-acknowledgement/` (135 words) and `/the-kk-worldview/` (259 words) are linked from every one of the 46 pages and are the two thinnest statements in the whole set. Worth a decision on whether that placement is intentional.

---

## Acceptance criteria for #122, honest status

**2 of 4 closed by this pass. 1 was already true before it and is now verified. 1 is open.**

- [x] **Define an approach: improved generic `page` template and/or custom templates for high-value pages.** Closed by this pass. Improve `page.html`, add exactly three sub-templates (offer, document/media-story, language-intro), retire four pages. Evidence: the "Proposed approach and wave sequence" section above. Caveat: this is a proposal, not a ratified decision. KK still has to confirm the wave ordering and the four retire targets.
- [x] **Services page redesigned (tracked separately).** True, but not because of this pass. It was already live. Verified here on 2026-08-02: `curl -sL https://kriskrug.co/generative-ai-services/` renders 26 `kk-services-*` class tokens across 12 distinct classes (`kk-services-hero`, `kk-services-display`, `kk-services-proof-grid`, `kk-services-ribbon-grid`, `kk-services-cta`, and 7 more). It is inline CSS, not the native template referenced in the 2026-05-26 comment, because PR #135 retired the hardcoded templates. That is why it is in the #480 table above.
- [ ] **Consistent spacing/hero treatment across content pages.** **Open. Nothing was built.** The honest reason is scope, not an external block: this pass was read-only inventory and planning, and no theme file was touched. The first version of this doc said "blocked on #480", which was wrong. All 24 target pages have zero inline CSS (verified: the nine pages with a `<style>` block are 1895, 12625, 2418, 12013, 2666, 1208, 2250, 2672, 1887, none of which is in the 24), so a `page.html` change would land on all 24 without being overridden. #480 is a consistency argument about the nine *other* routes.
- [x] **Prioritized list of which pages get bespoke treatment vs. template polish.** Closed by this pass. This document plus `pages-inventory-2026-08-02.csv`, 46 rows, with `wave` and `proposed_action` columns.

---

## Provenance

Everything above came from these read-only calls on 2026-08-02:

- `GET https://kriskrug.co/wp-json/wp/v2/pages?per_page=100&status=publish&page=1&_fields=id,slug,link,title,modified,date,parent,menu_order,template,content,excerpt` (46 results, `X-WP-Total: 46`, `X-WP-TotalPages: 1`)
- `GET https://kriskrug.co/wp-json/wp/v2/posts?per_page=100&page=1..10&_fields=id,link,title,content` (970 results, `X-WP-Total: 970`) for the internal link graph
- `curl -sL` on all 46 public page URLs for rendered-HTML classification
- `GET https://kriskrug.co/` for the header and footer nav inventory
- `GET https://kriskrug.co/wp-sitemap-posts-page-1.xml` (all 46 pages present)
- Redirect checks on `/services/`, `/recent-projects-include/`, `/work/`, `/home/`, `/news/`, `/subscribe/`
- Repo reads: `theme/kk-aurora/templates/page.html`, `theme/kk-aurora/assets/css/revive-port.css`, `theme/kk-aurora/style.css` (Version 1.5.8)
- `gh issue view 122`, `gh issue view 480`

Second pass, 2026-08-02, added:

- `curl -sL https://kriskrug.co/` re-parsed for nav: 9 hrefs inside `<header>`, 26 inside the outer `<footer class="wp-block-template-part">`, including the two `aurora-footer-bottom` links the first pass missed
- Repo reads: `theme/kk-aurora/parts/header.html`, `theme/kk-aurora/parts/footer.html`, and the full listing of `theme/kk-aurora/templates/`
- `curl -sL` re-run on all 46 public page URLs, matching `<main id="aurora-main" class="…">` against each template's declared `<main>` class: 44 `aurora-page-2026 kk-page`, 1 `aurora-home-2026 …` (3930), 1 `aurora-writing-archive` (2316). `aurora-footer-bottom` present in all 46
- `GET /wp-json/wp/v2/pages?…&_fields=id,slug,link,title,modified,content` re-run for the inline-CSS byte recount: 9 pages with a `<style>` block, 45,590 B tag-exclusive, 45,725 B tag-inclusive, 117 `!important`
- Namespace greps re-run: `kk-contact-2026` 4 hits and `kk-sponsor` 4 hits in `theme/kk-aurora/`; `kk-press`, `kk-services-2026`, `kkx-hero`, `kk-r9-pack` 0 hits each
- Redirect re-check: `/recent-projects-include/` 301 to `https://kriskrug.co/work/`, `/work/` 200, `/services/` 301 to `https://kriskrug.co/generative-ai-services/`

Zero writes of any kind were made against kriskrug.co, in either pass.

---

## Correction log

Second pass, 2026-08-02, after an adversarial verify of the first version. Six charges, five corrected, one partly rebutted.

| # | Charge | Disposition |
|---:|---|---|
| 1 | "22 of the 24 undesigned pages are reachable from no global nav at all. Only `/motleykrug-podcast/` and `/privacy-policy/` sit in the footer." | **Corrected. The charge was right.** Four are in the global footer, not two. The first pass parsed the footer's `nav` tiles and missed the `aurora-footer-bottom` copyright bar, which links `/reconciliation-indigenous-land-acknowledgement/` (3899) and `/the-kk-worldview/` (3948) on every page. Real number is **20 of 24**. Fixed in the headline nav paragraph, the Wave 3 table, the `nav` column of the CSV for 3899 and 3948, the ranking rationale, the PR body, and a correction comment on issue #122. |
| 2 | "Every one of the 46 pages renders through `page.html`, verified: all 46 carry `page-template-default`." | **Corrected. The charge was right.** 2316 `/blog/` has body class `blog wp-embed-responsive wp-theme-kk-aurora aurora-theme` with no `page-template-default`, and 3930 carries the class but renders through `front-page.html`. Real distribution: 44 on `page.html`, 1 on `front-page.html`, 1 on `home.html`, measured off the `<main>` class. Not outcome-changing: all 24 target pages are inside the 44. |
| 3 | "Blocked on #480" is overstated and was the excuse for the unmet acceptance criterion. | **Corrected. The charge was right.** All 24 target pages have `inline_css_bytes = 0`; the nine inline-CSS pages are all DESIGNED or DESIGNED-INLINE. Reframed as a sequencing recommendation about the other nine routes. The unmet criterion is now attributed to scope, which is the true reason. |
| 4 | Byte-count wording does not match the number. | **Corrected on wording, partly rebutted on the number.** The wording was wrong and is fixed: the figures are tag-exclusive. The verifier's tag-inclusive total of 45,727 B does not reproduce. All nine blocks open with a bare `<style>` (no attributes), so the delta is exactly 15 B per page on all nine, and the tag-inclusive total is **45,725 B**. Both totals are now printed. |
| 5 | `/vancouver-ai/` is 22 tokens / 8 classes wrapper-excluded, not 24 / 10; `/news/` is 37 words, not 38. | **Corrected. The charge was right on both.** The 24/10 figures were wrapper-inclusive printed against a wrapper-excluded definition. `/news/` is 37 words; the 38th token was the trailing `&nbsp;` paragraph. Fixed in the doc and in the CSV. |
| 6 | `pages.csv` is undated in a directory where data files are dated; the doc is not registered in `docs/current-state/README.md`. | **Half corrected, half deliberately deferred.** Renamed to `pages-inventory-2026-08-02.csv` and all four references updated. README registration is **not** done on purpose: PR #652 is concurrently rewriting `docs/current-state/README.md` and editing it here would collide with another agent's lane. The index entry should be added by whoever lands #652, or in a follow-up once it merges. |
