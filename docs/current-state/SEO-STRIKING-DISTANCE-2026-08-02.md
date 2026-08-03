# Issue #249: `you can't drink data` striking-distance re-measure

**Captured:** 2026-08-03T01:28:01Z (UTC), session dated 2026-08-02
**Mode:** read-only. Public HTML with cache bypass, public REST, and authenticated REST GET. Zero writes.
**Supersedes for freshness:** `docs/current-state/reports/issue-249-ycdd-striking-distance-20260726.md` (2026-07-26). That report is still correct on most points; this one adds three things it did not have.
**Refs:** #249, #233, #357; `fixes/issue-249-you-cant-drink-data-seo-handoff-2026-07-12.md`; PR #330 (merged).

---

## Read this first: I do not have Search Console

I have no Google Search Console access from this machine. No API credential, no OAuth, no exported digest file in the repo. The SEO Growth Digest that #233 and #198 cite (`.../seo-growth-weekly/digests/2026-06-17-seo-growth-digest.md`) is not in this repo and not on this VM.

That means **I cannot report a ranking position for `you can't drink data`, before or after the #233 deploy.** Any number in this document that looks like a rank came from a KK comment on issue #249, and I am quoting it as a quote, not measuring it. The only new numbers here are on-page facts I fetched myself.

Everything else on the issue's acceptance list, I measured.

---

## The three things that changed since the 2026-07-26 report

1. **Jetpack is deactivated.** The plugin that #233 used to set the homepage title is off. The SEO surface is now owned by the Aurora theme. Details below.
2. **`make seo-audit` is returning a false negative on all 1016 published items.** It reports every post and page as missing an SEO title and meta description. That is a tool break, not a content gap, and it is caused by point 1.
3. **The inbound link picture is much better than anyone recorded.** Nine published posts link to the target with ten hrefs, eight of them on a near exact-match anchor. Prior docs only ever counted the two protest companions. This changes the recommendation.

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

This is the most decision-relevant thing I found and it is not recorded anywhere in the repo.

Authenticated `GET /wp-json/wp/v2/plugins` returns 12 plugins. Jetpack is present but **inactive**:

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
| `?p=11936` | Resolves 200 to the pretty permalink |
| `http://` and `www.` variants | Both resolve 200 to the canonical `https://kriskrug.co/` host |
| Old slug `/2026/05/19/both-hands-full-vancouver-ai-march-2026/` | Redirects to `/2026/05/19/we-trained-ai-on-stolen-work/`, 200 |
| Generators in head | `WordPress 7.0.2` and `Site Kit by Google 1.184.0`. No competing SEO plugin |

Only nit worth an issue: point `Sitemap:` in `robots.txt` straight at `/wp-sitemap.xml` instead of through the 301. Near zero ranking effect, five minute fix, owned by the active "KK SEO root files" snippet.

---

## 6. Internal link equity into the target

This is where the prior read was incomplete. I searched the whole published corpus, not just the arc, using `GET /wp-json/wp/v2/posts?search=you-cant-drink-data&per_page=100`, which does a `LIKE` against post content. `x-wp-total: 9`. Pages: `x-wp-total: 0`.

**Nine posts, ten hrefs:**

| Post | Slug | Anchor text |
|---:|---|---|
| 12653 | `ai-lands-inside-every-profession` | `You Can't Drink Data` |
| 12184 | `canada-ai-for-all-strategy-skeptical-guide` | `You Can't Drink Data` |
| 12183 | `ai-keynote-slides-visual-workflow` | `You Can't Drink Data` |
| 11929 | `data-center-protest-signs` | `You Can't Drink Data: notes from my first AI protest` |
| 11882 | `we-trained-ai-on-stolen-work` | `environmental cost` **and** `You Can't Drink Data: notes from my first AI protest` |
| 11700 | `punk-rock-ai` | `You Can't Drink Data` |
| 11620 | `applied-ethical-ai-responsible-ai-professional-certification-rap` | `You Can't Drink Data` |
| 11358 | `spa-at-the-end-of-time` | `You Can't Drink Data` |
| 11252 | `name-the-bias` | `You Can't Drink Data` |

Every anchor uses a curly apostrophe. Eight of the ten are the bare exact phrase. Spot-checked live: post 12653's public HTML renders `href="https://kriskrug.co/2026/05/23/you-cant-drink-data/">You Can&#8217;t Drink Data`, cache-bypassed, HTTP 200.

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

Blunt framing first. The target has nine inbound internal links with eight near exact-match anchors, a clean canonical, a correct title, a correct description, sitemap inclusion, no noindex, 2621 words, and 44 original photographs. There is no on-page or crawl defect left to fix. If it is still sitting around position 8, the constraint is almost certainly off-page or SERP-intent, not anything in this table.

That reframes the one action #249 was holding open.

### Rank 1: pull Search Console. Effort: 10 minutes. Gain: unblocks everything.

Nothing below can be prioritised honestly without it. Exact pull spec in the next section. Do this first.

### Rank 2: add the two missing outbound links from 11936 to its companions. Effort: one body-only edit. Gain: small but real.

This is the only genuine link-graph defect I can see. Reciprocal links inside a tight topical cluster are the cheap version of a hub. It also makes the #233 closeout comment true, which it currently is not. One post, `content` field only, both companion URLs already known good.

I did **not** make this edit. It is a live WordPress write and out of scope for this task.

### Rank 3: fix `make seo-audit`. Effort: small. Gain: restores a broken instrument.

Right now a routine audit tells you 1016 pages are missing SEO metadata. Somebody will eventually believe it and launch a pointless backfill. Either register the two meta keys for REST in the theme, or move the audit off REST.

### Rank 4: point robots.txt `Sitemap:` at `/wp-sitemap.xml` directly. Effort: 5 minutes. Gain: near zero.

Housekeeping. Bundle it with the next snippet edit.

### Rank 5 and demoted: the reserved About page 1208 backlink.

**I recommend not doing this yet, which reverses the 2026-07-12 handoff and the 2026-07-26 report.**

Both of those chose About 1208 on the reasoning that the target had almost no internal link equity and the reserved link was the available lever. That reasoning was built on an incomplete count. The real count is nine linking posts and eight near exact-match anchors. Adding a tenth link with a ninth copy of the same anchor is not a striking-distance lever, it is noise. Exact-match anchor repetition also has diminishing and eventually negative returns.

The proposed sentence is also weak copy. "That question includes the physical costs of AI infrastructure, which I confronted on the streets of Vancouver and wrote about in you can't drink data" reads like it was written to hold a link, because it was. About page copy is high-value real estate and this sentence does not earn its place there.

If GSC comes back and shows the query genuinely stuck at 8 to 9 with impressions and zero clicks over a clean post-deploy window, the fix is far more likely to be **title and description rewritten for click-through**, not another internal link. At position 8 with impressions and no clicks, you have a snippet problem, not an authority problem.

Keep the About sentence parked. Do not delete the handoff, it is a fine fallback. Just stop treating it as the next action.

### What I cannot tell you without Search Console

- Whether the position moved at all after 2026-06-23 and 2026-06-24.
- Whether impressions are growing, flat, or decaying.
- Whether `/2026/05/23/you-cant-drink-data/` is even the page Google ranks for the query, or whether a companion or the category archive is cannibalising it.
- Whether the homepage title change helped or hurt homepage CTR.
- What the next striking-distance target should be. I have no query data, so I will not invent one. #249's third acceptance criterion stays open.

---

## 8. Exact Search Console pull for KK

Property: `https://kriskrug.co` (or the domain property, whichever is verified). Report: **Performance on Search results**.

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

**How to read it.**

- Position improved and clicks appeared: #233 worked. Record it, close the measurement half.
- Position flat around 8 to 9, impressions healthy, clicks near zero: snippet problem. Rewrite the title and description for CTR. Do not add more internal links.
- Impressions collapsed: check Pull C first for cannibalisation, then the URL Inspection tool on the target.
- Under 10 impressions in any window: record `not yet measurable` and wait. Do not claim causation either way.

The comparison values already on record in the #249 comment, for the mixed 2026-06-12 to 2026-07-09 window: page 294 impressions / 6 clicks / 2.04% CTR / position 7.96, and the query cluster at positions 8.4 to 8.7 with impressions and zero clicks. Those are KK's numbers quoted from the issue, not measured by me.

---

## 9. Acceptance criteria, marked honestly

| #249 criterion | Status |
|---|---|
| Next SEO digest records the query position pre vs post deploy, plus homepage impressions and CTR | **NOT MET.** No GSC access here. Pull spec written above, needs KK |
| Decide whether to add the reserved contextual homepage/About backlink, anchor `you can't drink data` | **MET, and the answer is no, not yet.** Reverses the 2026-07-12 and 2026-07-26 recommendation, on the grounds that the target already has 9 inbound links with 8 near exact-match anchors. Reasoning in section 7 |
| Note any next striking-distance target surfaced | **NOT MET.** Needs query data. I will not name a target I cannot see |

**Keep #249 open.** The measurement half is genuinely blocked on KK pulling Search Console. The backlink half now has a defensible answer and can be recorded.

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
