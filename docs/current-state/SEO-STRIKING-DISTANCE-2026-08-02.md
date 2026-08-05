# Issue #249: `you can't drink data` striking-distance re-measure

**Captured:** 2026-08-03T01:28:01Z (UTC), session dated 2026-08-02
**Corrected:** 2026-08-03T02:40Z after an adversarial verify pass. See "Correction log" below.
**Mode:** read-only. Public HTML with cache bypass, public REST, and authenticated REST GET. Zero writes.
**Supersedes for freshness:** `docs/current-state/reports/issue-249-ycdd-striking-distance-20260726.md` (2026-07-26). That report is still correct on most points; this one adds three things it did not have.
**Refs:** #249, #233, #357; `fixes/issue-249-you-cant-drink-data-seo-handoff-2026-07-12.md`; PR #330 (merged 2026-07-13).

## Correction log (2026-08-03)

The first version of this file was wrong in three ways. All three are fixed in place. Recording them here so nobody quotes the old numbers out of the PR body or the issue thread.

| What was wrong | What it said | What is true |
|---|---|---|
| Anchor count, stated 5 times | "eight" bare exact-match anchors | **7** bare exact-phrase anchors out of **10** total. **9** of the 10 contain the phrase. Counting rule and full list in section 6 |
| Backlink decision | Marked acceptance criterion 2 **MET** and reversed the About 1208 link on this agent's own authority | KK already decided this on #249 on 2026-07-12 and it was acted on in merged PR #330. An agent does not overturn that. The section is now a flagged **recommendation to revisit**, and the criterion is back to **OPEN**. See section 7, Rank 5 |
| `?p=11936` behaviour | "Resolves 200 to the pretty permalink" | **301** to `https://kriskrug.co/2026/05/23/you-cant-drink-data/`, then 200. One hop. Correct behaviour, imprecisely recorded |

---

## Read this first: I do not have Search Console

I have no Google Search Console access from this machine. No API credential, no OAuth, no exported digest file in the repo. The SEO Growth Digest that #233 and #198 cite (`.../seo-growth-weekly/digests/2026-06-17-seo-growth-digest.md`) is not in this repo and not on this VM.

That means **I cannot report a ranking position for `you can't drink data`, before or after the #233 deploy.** Any number in this document that looks like a rank came from a KK comment on issue #249, and I am quoting it as a quote, not measuring it. The only new numbers here are on-page facts I fetched myself.

Two of #249's three acceptance criteria need that data and stay unmet because of it. The third is a KK decision that KK already made. **Honest score on this issue: 0 of 3 closed by this report.** What I did measure is the on-page and link-graph side, which is real work and is not the same as closing the issue. Full accounting in section 9.

---

## Lead finding: the #233 mechanism is gone, and one of our audit tools is now lying because of it

This is the most decision-relevant thing in the file and none of it was recorded anywhere in the repo before now.

**Jetpack is deactivated.** The plugin #233 used to set the homepage title is off. Authenticated `GET /wp-json/wp/v2/plugins` returns 12 plugins including `inactive | Jetpack | jetpack/jetpack`, re-verified 2026-08-03T02:38Z. `GET https://kriskrug.co/wp-json/jetpack/v4/settings` returns HTTP 404 `{"code":"rest_no_route"}`, and that is the exact endpoint #233 wrote `advanced_seo_title_formats.front_page` through. The mechanism #249 was created to measure no longer exists.

**The titles survive only because the theme is holding them up.** The homepage `<title>` renders because `theme/kk-aurora/functions.php:322` hardcodes the string `Kris Krug | AI Keynote Speaker & Creative Technologist`. Per-post SEO titles render because `theme/kk-aurora/inc/seo-title.php:30-50` reads `jetpack_seo_html_title` post meta directly with `get_post_meta`, which does not care whether the plugin that registered the key is running. Meta descriptions moved the same way, to `theme/kk-aurora/functions.php:610-624`. The SEO surface is theme-owned now, not plugin-owned. Full detail in section 2.

> ### TOOLING TRAP: `make seo-audit` is a false negative on all 1016 published items
>
> `make seo-audit` reports **1016 of 1016** published items missing an SEO title and missing a meta description. That number is garbage. It is a tool break caused by the Jetpack deactivation, not a content gap.
>
> Proof: post 11936's SEO title is visibly rendering on the live page right now, and it is counted in the 1016. Authenticated `GET /wp-json/wp/v2/posts/11936?context=edit&_fields=meta` returns `{"meta":{"footnotes":""}}`, re-verified 2026-08-03T02:38Z. With Jetpack off, `jetpack_seo_html_title` and `advanced_seo_description` are no longer registered for REST, so `scripts/seo-audit/inventory_lib.py:8-10` finds nothing and every record scores as empty. 1016 is just the published-item total: `x-wp-total: 970` posts plus `x-wp-total: 46` pages.
>
> **Do not launch a backfill off those counts.** Anyone who runs this target and believes it will burn a day rewriting metadata that already exists. Mechanism and fix options in section 3, and it is follow-up 2 at the bottom.

**Third change since the 2026-07-26 report: the inbound link picture is much better than anyone recorded.** Nine published posts link to the target with ten hrefs, seven of them on the bare exact-match anchor. Prior docs only ever counted the two protest companions. Counting rule and full list in section 6.

---

## 1. Did the #233 deploy actually land?

Yes for the homepage title and description, verified two ways. Pagely ARES edge caching is a known gotcha in this repo, so I fetched each URL twice: once with a unique `?cb=<epoch>` buster plus `Cache-Control: no-cache` and `Pragma: no-cache`, and once completely plain, which is what the edge serves a real visitor and Googlebot.

Both fetches returned identical head values. All five fetches were HTTP 200 from `server: Pagely-ARES/1.22.28`. No `x-cache`, `age`, or `x-pagely` header is exposed by the edge, so the plain-versus-busted comparison is the proof, not a header.

Plain, edge-cached fetch of `https://kriskrug.co/`:

```
<title>Kris Krug | AI Keynote Speaker &#038; Creative Technologist</title>
<link rel="canonical" href="https://kriskrug.co/"
```

Plain, edge-cached fetch of `https://kriskrug.co/2026/05/23/you-cant-drink-data/`:

```
<title>You Can't Drink Data | Notes From My First AI Protest</title>
<link rel="canonical" href="https://kriskrug.co/2026/05/23/you-cant-drink-data/"
```

**One correction to the #233 closeout comment.** It records the shipped title as `Kris Krüg | AI Keynote Speaker & Creative Technologist`. The live title is `Kris Krug`, no umlaut. That is not drift, it is what the current source string says, see the next section. The closeout comment is simply wrong on that character. Low impact for ranking, worth knowing before anyone "fixes" it back.

---

## 2. The #233 mechanism is gone. The theme is holding the title up.

Detail for the lead finding above. Not recorded anywhere else in the repo.

Authenticated `GET /wp-json/wp/v2/plugins` returns 12 plugins, re-verified 2026-08-03T02:38Z. Jetpack is present but **inactive**:

```
inactive | Jetpack | jetpack/jetpack
active   | Jetpack Boost | jetpack-boost/jetpack-boost
active   | Jetpack CRM  | zero-bs-crm/ZeroBSCRM
active   | Jetpack Protect | jetpack-protect/jetpack-protect
```

Consequences I verified:

- `GET https://kriskrug.co/wp-json/jetpack/v4/settings` returns `{"code":"rest_no_route", ... "status":404}`. The exact endpoint #233 wrote `advanced_seo_title_formats.front_page` through no longer exists.
- `GET /wp-json/wp/v2/posts/11936?context=edit&_fields=meta` returns `{"meta":{"footnotes":""}}`. The keys `jetpack_seo_html_title` and `advanced_seo_description` are no longer registered for REST, because Jetpack was what registered them.
- The values themselves are still in the database and still render, because the theme reads them directly with `get_post_meta`.

Where the SEO surface lives now, in repo source:

| Output | Source | Line |
|---|---|---|
| Homepage `<title>` | hardcoded string `Kris Krug \| AI Keynote Speaker & Creative Technologist` | `theme/kk-aurora/functions.php:322` |
| Singular `<title>` | `pre_get_document_title` filter reading `jetpack_seo_html_title` post meta (shipped for #357) | `theme/kk-aurora/inc/seo-title.php:30-50` |
| Homepage meta description | `advanced_seo_front_page_description` option, with a hardcoded fallback | `theme/kk-aurora/functions.php:610-612` |
| Singular meta description | `advanced_seo_description` post meta, falling back to excerpt then trimmed content | `theme/kk-aurora/functions.php:619-624` |

Proof the post meta is still the live source and not the excerpt fallback: post 11936's excerpt is 209 characters and begins `Kris Krug marches in Vancouver's first anti-AI, anti-data-centre protest...`, while the rendered `<meta name="description">` is 151 characters and begins `I marched in Vancouver's first anti-data-centre protest...`. Different strings, so the stored `advanced_seo_description` is winning.

**Two live notes this invalidates.** The memory note `homepage-seo-title-jetpack-front-page-format` ("the homepage title comes from Jetpack `advanced_seo_title_formats.front_page`, not page 3930 post-meta") is now stale: it comes from the theme. And the memory note about Jetpack SEO meta REST writes returning 500 on combining diacritics is moot, because you cannot write those keys over REST at all right now.

I could not determine **when** Jetpack was deactivated. UNVERIFIED. The 2026-06-23 #233 comment describes a live Jetpack generator, so it happened after that.

---

## 3. `make seo-audit` output, and why you should not act on it

The Makefile target calls `scripts/notion-to-wp/.venv/bin/python`. That venv does not exist inside a git worktree, so the target fails with `No such file or directory` until you point it at the main checkout's venv. It also needs `WP_USER` / `WP_APP_PASSWORD`, while Varlock resolves `WP_API_USERNAME` / `WP_API_PASSWORD`, so the names have to be bridged. Once both are handled it runs:

```
# Jetpack SEO Metadata Inventory
- Total: 1016 (970 posts, 46 pages)
- Missing SEO title: 1016
- Missing meta description: 1016
- Posts missing social message: 970
```

Zero out of 1016 records have an SEO title. That includes post 11936, whose SEO title is visibly rendering on the live page right now.

Cause: `scripts/seo-audit/inventory_lib.py:8-10` reads `jetpack_seo_html_title`, `advanced_seo_description`, and `jetpack_publicize_message` from the REST `meta` object, and `scripts/seo-audit/inventory.py:34` requests `_fields=id,slug,title,link,meta`. With Jetpack off, none of those keys are in `meta`, so every record scores as empty.

The one thing the run is still good for is inventory: 970 published posts, 46 published pages, and correct id/slug/link mapping for the three arc posts.

**Do not use this target's "missing" counts for anything until it is fixed.** Options, cheapest first: read the values via a WP-CLI or authenticated PHP path instead of REST, register the two meta keys for REST in the theme now that the theme owns them, or reactivate Jetpack. That is a separate ticket, not this one.

---

## 4. On-page truth for the arc

All three posts confirmed live, HTTP 200, cache-bypassed and plain.

| | 11936 target | 11882 companion | 11929 companion |
|---|---|---|---|
| URL | `/2026/05/23/you-cant-drink-data/` | `/2026/05/19/we-trained-ai-on-stolen-work/` | `/2026/05/23/data-center-protest-signs/` |
| Status | publish | publish | publish |
| `modified` | 2026-06-28T18:40:25 | 2026-06-24T10:20:09 | 2026-06-28T18:51:34 |
| `<title>` | `You Can't Drink Data \| Notes From My First AI Protest` (53) | `Both Hands Full At Vancouver AI \| Kris Krug` (43) | `Both Hands Full at the Data Center: Protest Signs for the Middle` (64) |
| meta description | 151 chars | 152 chars | 153 chars |
| H1 | `You Can't Drink Data` | `We Trained AI On Stolen Work. I Am More Creative Than Ever.` | `Both Hands Full at the Data Center: Protest Signs for People Who Refuse to Pick a Side` |
| og:title | `You Can't Drink Data` | full post title | full post title |
| canonical | self, exactly 1 tag | self, exactly 1 tag | self, exactly 1 tag |
| robots meta | `max-image-preview:large`, indexable | same | same |
| Body words | 2621 (3072 with captions) | 554 | 1217 (1370 with captions) |
| H2 count | 8 | not counted | not counted |
| Images | 44 | not counted | not counted |
| JSON-LD | 3 blocks: BlogPosting, BreadcrumbList, Person/Organization | 3 blocks, same shape | 3 blocks, same shape |

Notes on the target specifically:

- Title 53 chars and description 151 chars are both inside normal SERP truncation. No length problem to fix.
- `<title>`, H1, and og:title diverge on purpose: the title tag carries the `Notes From My First AI Protest` qualifier, the H1 and og:title are the bare phrase. That is fine and arguably correct, since the H1 is the exact query string.
- JSON-LD comes from the active "KK Schema" Code Snippet (confirmed active via authenticated `GET /wp-json/code-snippets/v1/snippets`). The `BlogPosting.description` uses the excerpt, not the SEO description, so the two disagree. Cosmetic, not a ranking issue.
- 44 images is a lot of protest-sign photography. UNVERIFIED whether that is hurting Core Web Vitals on this URL, I did not run a field-data or Lighthouse check and CWV is a real ranking input at position 8.

---

## 5. Indexation signals

Everything I can see says the target is cleanly indexable. There is no crawl or canonical problem to blame.

| Check | Result |
|---|---|
| In sitemap | Yes. `https://kriskrug.co/2026/05/23/you-cant-drink-data/` is in `wp-sitemap-posts-post-1.xml` (970 URLs total) |
| Companions in sitemap | Both present |
| Retired 11882 slug in sitemap | Absent, correct |
| Canonical agrees with sitemap URL | Yes, exact string match |
| Conflicting canonicals | None. Exactly one `rel="canonical"` tag per page across all five pages checked |
| `noindex` | Absent from all five pages |
| `robots.txt` | Allows the URL. Disallows only `/wp-admin/`, `/?s=`, `/search/`. AI crawlers explicitly allowed |
| Sitemap declared in robots.txt | `https://kriskrug.co/sitemap.xml`, which **301s** to `/wp-sitemap.xml`. Works, but a redirecting sitemap declaration is sloppy |
| `?p=11936` | **301** to `https://kriskrug.co/2026/05/23/you-cant-drink-data/`, then 200. One hop, correct WordPress canonical-redirect behaviour. Verified `curl -sS -o /dev/null -D - "https://kriskrug.co/?p=11936"` returns `HTTP/2 301` plus that `location:`, and `curl -sSL -w "%{http_code} %{num_redirects}"` returns `200 1` |
| `http://` and `www.` variants | Both resolve 200 to the canonical `https://kriskrug.co/` host |
| Old slug `/2026/05/19/both-hands-full-vancouver-ai-march-2026/` | Redirects to `/2026/05/19/we-trained-ai-on-stolen-work/`, 200 |
| Generators in head | `WordPress 7.0.2` and `Site Kit by Google 1.184.0`. No competing SEO plugin |

Only nit worth an issue: point `Sitemap:` in `robots.txt` straight at `/wp-sitemap.xml` instead of through the 301. Near zero ranking effect, five minute fix, owned by the active "KK SEO root files" snippet.

---

## 6. Internal link equity into the target

This is where the prior read was incomplete. I searched the whole published corpus, not just the arc, using `GET /wp-json/wp/v2/posts?search=you-cant-drink-data&per_page=100`, which does a `LIKE` against post content. `x-wp-total: 9`. Pages: `x-wp-total: 0`.

**Counting rule, stated so the number can be re-derived.** From `content.rendered` of each of those 9 posts, take every `<a href="...">` whose href contains the slug `you-cant-drink-data`. That is the anchor set. For each anchor, strip inner tags, HTML-unescape (`&#8217;` becomes a curly apostrophe), normalise curly apostrophes to straight, collapse whitespace, lowercase. Then:

- **bare exact phrase** means the normalised anchor text equals `you can't drink data` and nothing else.
- **contains the phrase** means `you can't drink data` appears as a substring, which also catches the longer `you can't drink data: notes from my first ai protest`.

Re-run of that rule on 2026-08-03T02:34Z:

```
posts returned          : 9
total anchors to target : 10
bare exact phrase       : 7
containing phrase       : 9
neither                 : 1
```

**Nine posts, ten hrefs, seven bare exact-phrase anchors:**

| Post | Slug | Anchor text | Bare exact | Contains phrase |
|---:|---|---|:--:|:--:|
| 12653 | `ai-lands-inside-every-profession` | `You Can't Drink Data` | yes | yes |
| 12184 | `canada-ai-for-all-strategy-skeptical-guide` | `You Can't Drink Data` | yes | yes |
| 12183 | `ai-keynote-slides-visual-workflow` | `You Can't Drink Data` | yes | yes |
| 11929 | `data-center-protest-signs` | `You Can't Drink Data: notes from my first AI protest` | no | yes |
| 11882 | `we-trained-ai-on-stolen-work` | `environmental cost` | no | **no** |
| 11882 | `we-trained-ai-on-stolen-work` | `You Can't Drink Data: notes from my first AI protest` | no | yes |
| 11700 | `punk-rock-ai` | `You Can't Drink Data` | yes | yes |
| 11620 | `applied-ethical-ai-responsible-ai-professional-certification-rap` | `You Can't Drink Data` | yes | yes |
| 11358 | `spa-at-the-end-of-time` | `You Can't Drink Data` | yes | yes |
| 11252 | `name-the-bias` | `You Can't Drink Data` | yes | yes |

Post 11882 carries two hrefs to the target, which is why 9 posts produce 10 anchors.

Every anchor that contains the phrase renders it with a curly apostrophe (`You Can&#8217;t Drink Data` in the raw HTML). The one anchor that does not contain the phrase, `environmental cost` in 11882, has no apostrophe at all. Spot-checked live: post 12653's public HTML renders `href="https://kriskrug.co/2026/05/23/you-cant-drink-data/">You Can&#8217;t Drink Data`, cache-bypassed, HTTP 200.

**An earlier version of this file said "eight" here and in four other places. That was wrong.** It is 7 bare and 9 containing, out of 10. If you are reading a quote of this report that says eight, the quote is stale.

**Surfaces that do NOT link to it:**

| Surface | Links to 11936 |
|---|---|
| Homepage `/` (page 3930) | 0 |
| About `/about/` (page 1208) | 0 |
| `/ai-ethics/` pillar page | 0 |
| Any published page at all | 0 |
| `/category/ai-ethics-philosophy/` | listing only, not a contextual link |

**Outbound from the target:** 4 internal, 12 external.

Internal outbound: `grassroots builders` to `/2025/02/16/bcs-ai-ecosystem-a-mycelial-network-of-creation/`, `more creative than I've ever been` to `/2026/05/04/punk-rock-ai/`, `both hands full` to `/2026/01/24/both-hands-full/`, `your judgment is the whole game` to `/2026/05/15/your-taste-is-your-moat/`.

**The #233 closeout claim is still wrong and has been wrong for five weeks.** It says the cluster is bidirectional, `11936 ⇄ 11882 ⇄ 11929`. Post 11936 contains **zero** hrefs to either companion. The 2026-07-26 report caught this; nothing has changed since. Both companions still point in, 11936 still points at neither.

Post 11936 is categorised `AI Ethics & Philosophy` (term 1678) with 7 tags.

---

## 7. Recommendation, ranked by effort against likely gain

Blunt framing first. The target has nine inbound internal linking posts carrying ten hrefs, seven of them on the bare exact-match anchor and nine of the ten containing the phrase, plus a clean canonical, a correct title, a correct description, sitemap inclusion, no noindex, 2621 words, and 44 original photographs. There is no on-page or crawl defect left to fix. If it is still sitting around position 8, the constraint is almost certainly off-page or SERP-intent, not anything in this table.

That is new evidence bearing on the one action #249 was holding open. It is evidence, not a decision. See Rank 5.

### Rank 1: pull Search Console. Effort: 10 minutes. Gain: unblocks everything.

Nothing below can be prioritised honestly without it. Exact pull spec in the next section. Do this first.

### Rank 2: add the two missing outbound links from 11936 to its companions. Effort: one body-only edit. Gain: small but real.

This is the only genuine link-graph defect I can see. Reciprocal links inside a tight topical cluster are the cheap version of a hub. It also makes the #233 closeout comment true, which it currently is not. One post, `content` field only, both companion URLs already known good.

I did **not** make this edit. It is a live WordPress write and out of scope for this task.

### Rank 3: fix `make seo-audit`. Effort: small. Gain: restores a broken instrument.

Right now a routine audit tells you 1016 pages are missing SEO metadata. Somebody will eventually believe it and launch a pointless backfill. Either register the two meta keys for REST in the theme, or move the audit off REST.

### Rank 4: point robots.txt `Sitemap:` at `/wp-sitemap.xml` directly. Effort: 5 minutes. Gain: near zero.

Housekeeping. Bundle it with the next snippet edit.

### Rank 5: the reserved About page 1208 backlink. RECOMMENDATION TO REVISIT, not a decision. KK's call, already made.

> **Flag.** This section previously read as a reversal and marked the acceptance criterion MET. That was out of line. KK already decided this, on the record, and the decision was acted on. What follows is new evidence arguing for a second look. It does not change the decision. Only KK does that.

**The decision that already exists.** On issue #249, dated 2026-07-12, KK wrote:

> The 28-day evidence gate is now clear for 2026-06-12 through 2026-07-09: Page: 294 impressions, 6 clicks, 2.04% CTR, average position 7.96. Exact `you cant drink data` query variants are clustering around positions 8.4-8.7 with impressions but no clicks. **Decision: use the single contextual homepage/About backlink reserved by the original spec, with anchor text `you can't drink data`.** This is a measured striking-distance action, not a new-content bet.

That was acted on in **PR #330, merged 2026-07-13** (`958984f`, "seo: add you can't drink data review handoff"), which selected About page 1208, wrote the exact sentence, and recorded the identity guards, snapshot, content-only REST boundary, rollback, and readback steps. The remaining gate on that PR is a human approving the sentence and applying the write. That gate is still open. Nothing about it is cancelled by this report.

**The new evidence, and why I think it is worth a second look before that write happens.**

The 2026-07-12 handoff and the 2026-07-26 report both selected About 1208 partly on the premise that the target had almost no internal link equity. Section 6 shows that premise was built on an incomplete count. The real picture is nine linking posts, ten hrefs, seven of them the bare exact phrase and nine of the ten containing it. The reserved About link would be the eleventh href and the eighth bare exact-phrase anchor. Exact-match anchor repetition has diminishing and, past some point, negative returns, so the marginal value of that eighth copy is lower than it looked in July.

Second, the proposed sentence reads as copy written to hold a link: "That question includes the physical costs of AI infrastructure, which I confronted on the streets of Vancouver and wrote about in you can't drink data." About page copy is high-value real estate. That is a judgement call about voice and page quality, and it is KK's, not mine.

Third, the diagnosis may point elsewhere. KK's own numbers show position 8.4 to 8.7 with impressions and zero clicks. If a clean post-deploy Search Console window confirms that shape, the constraint is snippet click-through, not internal authority, and the higher-value action would be rewriting the title and description for CTR rather than adding an eleventh internal link. That is a hypothesis I cannot test without the data in section 8.

**What I am actually asking for.** Not "do not do it". Rather: before the About 1208 write is applied, look at the corrected link count and the Pull A / Pull B numbers, then confirm or change the July decision. If the answer stays "ship the About link", the handoff in PR #330 is ready and nothing is lost. The acceptance criterion stays **open** either way, because deciding it is not mine to do.

### What I cannot tell you without Search Console

- Whether the position moved at all after 2026-06-23 and 2026-06-24.
- Whether impressions are growing, flat, or decaying.
- Whether `/2026/05/23/you-cant-drink-data/` is even the page Google ranks for the query, or whether a companion or the category archive is cannibalising it.
- Whether the homepage title change helped or hurt homepage CTR.
- What the next striking-distance target should be. I have no query data, so I will not invent one. #249's third acceptance criterion stays open.

---

## 8. Exact Search Console pull for KK

**The exact report: Google Search Console → left sidebar → Performance → Search results.** That is the one titled "Performance on Search results" at the top of the page. Not "Discover", not "Google News", not Site Kit's WordPress dashboard summary, which rounds and truncates. Property: `https://kriskrug.co`, or the domain property `kriskrug.co`, whichever is the verified one. Turn on all four metric toggles (Clicks, Impressions, Average CTR, Average position) before reading anything.

Site Kit by Google 1.184.0 is active on the site (seen in the head generators, section 5), so the GSC property is already connected. The pulls below are all in that one report, using the filter bar and the Queries / Pages tabs.

**Pull A. Landing page, split windows.** Filter Page = exact `https://kriskrug.co/2026/05/23/you-cant-drink-data/`. Record clicks, impressions, CTR, average position for each:

| Window | Dates | Why |
|---|---|---|
| Pre-deploy | 2026-05-26 to 2026-06-22 | Clean baseline, after publish, before #233 |
| Post-deploy | 2026-06-25 to 2026-07-22 | Clean 28 days after both #233 halves |
| Recent | 2026-07-06 to 2026-08-02 | Current state |

Do not reuse the 2026-06-12 to 2026-07-09 window from the #249 comment on its own. It straddles both deploy dates, so it cannot show a before or an after.

**Pull B. The query itself.** Queries tab, filter Query contains `drink data`. Grab every variant row (`you cant drink data`, `you can't drink data`, and whatever GSC groups with them) for the same three windows. Note zero-click rows explicitly, they are the signal.

**Pull C. Cannibalisation check.** With the Query filter from Pull B still applied, switch to the **Pages** tab. If any URL other than `/2026/05/23/you-cant-drink-data/` is picking up impressions for the query, that is the real problem and no internal link will fix it.

**Pull D. Homepage side effect.** Filter Page = exact `https://kriskrug.co/`, same three windows, clicks / impressions / CTR / position. This is the only read on whether the #233 title change helped.

**Pull E. The next striking-distance target (closes #249's third criterion).** Same report, Queries tab, no page filter, window 2026-07-06 to 2026-08-02, then export to sheet and sort. A striking-distance query is one with average position between roughly 5 and 20, impressions above zero, and clicks at or near zero. Take the top few by impressions. That list is the answer to "note any next striking-distance target surfaced". I cannot produce it without the export.

**How to read it.**

- Position improved and clicks appeared: #233 worked. Record it, close the measurement half.
- Position flat around 8 to 9, impressions healthy, clicks near zero: snippet problem. Rewrite the title and description for CTR. Do not add more internal links.
- Impressions collapsed: check Pull C first for cannibalisation, then the URL Inspection tool on the target.
- Under 10 impressions in any window: record `not yet measurable` and wait. Do not claim causation either way.

The comparison values already on record in the #249 comment, for the mixed 2026-06-12 to 2026-07-09 window: page 294 impressions / 6 clicks / 2.04% CTR / position 7.96, and the query cluster at positions 8.4 to 8.7 with impressions and zero clicks. Those are KK's numbers quoted from the issue, not measured by me.

---

## 9. Acceptance criteria, marked honestly

**Honest count: 0 of 3 met.** Nothing on this list is closed by this report. What the report adds is evidence, three previously unrecorded live-state findings, and an exact pull spec. That is useful and it is not the same as done.

| #249 criterion | Status |
|---|---|
| Next SEO digest records the query position pre vs post deploy, plus homepage impressions and CTR | **NOT MET, and unmet-able from this session.** No Google Search Console access exists here: no API credential, no OAuth, no service account, and the SEO Growth Digest that #233 and #198 cite is not in this repo or on this machine. This is not a "did not get to it", it is a hard blocker. The report KK needs is **Search Console → Performance → Search results**, pulled four ways per section 8. Pull A (Page filter, exact `https://kriskrug.co/2026/05/23/you-cant-drink-data/`, the three windows) is the one that closes this criterion |
| Decide whether to add the reserved contextual homepage/About backlink, anchor `you can't drink data` | **OPEN, and it is KK's to close.** KK already decided this on #249 on 2026-07-12 (use the About/homepage backlink, anchor `you can't drink data`), acted on in merged PR #330. An earlier version of this file marked it MET by reversing that decision on the agent's own authority. That was wrong and is retracted. Section 7 Rank 5 now carries the new link-count evidence as a flagged recommendation to revisit before the About 1208 write is applied. Confirming or changing the July decision is a KK action |
| Note any next striking-distance target surfaced | **NOT MET, same blocker.** Naming a next striking-distance target requires the Queries tab of the same Performance → Search results report, filtered to positions 5 to 20 with impressions above zero. I have no query data at all, so any target I named would be invented |

**Keep #249 open.** All three criteria are still live. Two are blocked on KK pulling Search Console, one is a KK decision that already exists and now has new evidence worth a second look before the write lands.

---

## 10. Scope and safety

Read-only session. No POST, PATCH, PUT, or DELETE against kriskrug.co. No theme deploy, no SFTP, no publish, no snippet edit, no Jetpack change, no analytics write, no outreach. Authenticated REST calls were all GET (`/wp/v2/plugins`, `/wp/v2/posts/11936?context=edit`, `/jetpack/v4/settings`, `/code-snippets/v1/snippets`) via Varlock-injected credentials. No `.env` file was read or printed.

No ranking improvement is claimed by this document.

### Follow-ups worth their own issues

1. Post 11936 has no outbound links to 11882 or 11929. The #233 closeout comment says it does. Body-only fix, one post.
2. `make seo-audit` reports 1016/1016 missing after Jetpack was deactivated. Tool fix.
3. Jetpack deactivation is not recorded anywhere in `docs/current-state/`. The theme now owns SEO titles and descriptions. AGENTS.md and the `homepage-seo-title-jetpack-front-page-format` memory note are both stale on this.
4. `robots.txt` declares a sitemap URL that 301s.
5. The live homepage title is `Kris Krug`, not `Kris Krüg` as #233's closeout claims. Decide whether the umlaut belongs there, then make the source and the record agree.
