# Issue #249 — `you can't drink data` striking-distance after #233

**Captured:** `2026-07-26T20:35:08Z`  
**Mode:** public HTML + public REST only. No WordPress writes. No Search Console API. No GA4.  
**Branch intent:** `docs(#249)` measurement + recommendation handoff.  
**Refs:** #249, #233; `fixes/issue-233-homepage-metadata-internal-links-2026-06-18.md`; `fixes/issue-198-search-console-striking-distance-links-2026-06-18.md`; `fixes/issue-249-you-cant-drink-data-seo-handoff-2026-07-12.md` (PR #330, merged); `content/drafts/2026-05-23-you-cant-drink-data/internal-links.md`.

## Verdict

#233’s **public deploy surface is still live** (homepage title + protest-arc companions published). The reserved **homepage/About exact-match backlink is still not live**. Ranking before/after for `you can't drink data` **cannot be closed from this VM** — there is no GSC API — so KK must pull Search Console for split windows. Recommendation: **apply the single About (1208) contextual backlink** already staged in the July 12 handoff, after refreshing identity/`modified` guards (About drifted on 2026-07-24).

## Timeline (deploy facts)

| When | What |
|---|---|
| 2026-05-23 | YCDD post **11936** published (`/2026/05/23/you-cant-drink-data/`) |
| 2026-06-17 | SEO Growth Digest / issue #198 flagged striking-distance cluster `you cant drink data` (digest body lives outside this repo; not present in-VM) |
| 2026-06-23 | Homepage `<title>` shortened via Jetpack `advanced_seo_title_formats.front_page` (#233 metadata half) |
| 2026-06-24 | Companions **11882** + **11929** published; protest-arc cross-links claimed complete; #233 closed; #249 opened for measurement |
| 2026-06-12 → 2026-07-09 | Issue #249 comment records a 28-day GSC baseline (page + query cluster) — **straddles** the 06-23/06-24 deploys |
| 2026-07-12/13 | Repo handoff + PR #330: choose **About 1208**, exact sentence, publisher gate; **no live write** |
| 2026-07-26 (this probe) | Public re-measure of title/meta + internal links; About backlink still absent |

## Public probe — homepage metadata (#233 half)

Logged-out `GET https://kriskrug.co/` → **200**, canonical self.

| Field | Live 2026-07-26 | Expected from #233 |
|---|---|---|
| `<title>` | `Kris Krug \| AI Keynote Speaker & Creative Technologist` (54 chars) | Same (Ü may render as `u` in title entity decode) |
| `meta name=description` | 153 chars — community-first tools / BC+AI / Both Hands Full copy | Matches #233 approved Jetpack description |
| `og:title` | Matches short title | Present |
| `canonical` | `https://kriskrug.co/` | OK |
| `robots` | `max-image-preview:large` (indexable) | OK |
| Links to YCDD / companions | **0** | Reserved backlink never claimed for homepage body |

Homepage metadata half of #233 remains **verified live**. Note: a 2026-07-16 meta-gap re-probe once saw missing `name=description` on `/`; today’s probe finds description **present** on `/`, `/about/`, and the three protest posts.

## Public probe — protest arc (internal links)

| ID | Slug / URL | Status | `modified` (public REST) | HTTP |
|---:|---|---|---|---:|
| 11936 | `you-cant-drink-data` → `/2026/05/23/you-cant-drink-data/` | publish | `2026-06-28T18:40:25` | 200 |
| 11882 | `we-trained-ai-on-stolen-work` → `/2026/05/19/we-trained-ai-on-stolen-work/` | publish | `2026-06-24T10:20:09` | 200 |
| 11929 | `data-center-protest-signs` → `/2026/05/23/data-center-protest-signs/` | publish | `2026-06-28T18:51:34` | 200 |

Old 11882 slug `/2026/05/19/both-hands-full-vancouver-ai-march-2026/` → **301** → new slug (WordPress redirect).

### Live cross-link graph (content anchors)

| From → To | Live today? | Observed anchor(s) |
|---|---|---|
| 11882 → 11936 | **yes** (2) | `environmental cost`; `You Can't Drink Data: notes from my first AI protest` |
| 11882 → 11929 | **yes** | `Both Hands Full at the Data Center: protest signs` |
| 11929 → 11936 | **yes** | `You Can't Drink Data: notes from my first AI protest` |
| 11929 → 11882 | **yes** | `We Trained AI On Stolen Work…` |
| 11936 → 11882 | **no** | none in public HTML |
| 11936 → 11929 | **no** | none in public HTML |
| Homepage → 11936 | **no** | — |
| About → 11936 | **no** | — |
| `/ai-ethics/` pillar → 11936 | **no** | — |
| `/category/ai-ethics-philosophy/` | **listing only** | YCDD appears in archive listing (not a contextual exact-match backlink) |

YCDD public SEO title/description (for completeness):

- title: `You Can't Drink Data | Notes From My First AI Protest` (53)
- description: 151 chars (West Coast third-way / anti-data-centre protest)
- canonical self; robots indexable

**Public finding vs #233 close comment:** the closeout claimed bidirectional `11936 ⇄ 11882 ⇄ 11929`. Companions still point at YCDD, but **YCDD no longer exposes outbound companion hrefs** in logged-out HTML (post `modified` is 2026-06-28, after the 06-24 companion publish). That weakens the intended striking-distance cluster relative to the closeout claim. Treat restoring 11936 → companions as a **separate body-only review item**, not as a substitute for the reserved exact-match About/homepage link.

## About surface (reserved backlink)

| Field | Live 2026-07-26 |
|---|---|
| Page ID | `1208` |
| Slug / URL | `about` → `https://kriskrug.co/about/` |
| Status | publish |
| `modified` | `2026-07-24T17:22:59` (**drifted** vs July 12 handoff guard `2026-07-01T11:33:51`) |
| Canonical | self |
| Exact phrase `you can't drink data` | **0** |
| Href `you-cant-drink-data` | **0** |
| Opening “two decades documenting…” paragraph | **still present** |
| Handoff add-on sentence (“physical costs of AI infrastructure…”) | **absent** |
| `content-architecture-2026:about` marker | present |

Repo payload `content/source-packs/content-architecture-2026/wp-payloads/about.html` still matches the pre-backlink paragraph (zero YCDD href). Homepage page `3930` (`empowering-events-organizations-for-the-ai-age`, `modified` `2026-06-29T16:49:49`) also has zero YCDD links and weaker surrounding copy for the preferred exact-match anchor.

## What this agent CAN measure (no GSC)

1. Public indexability signals: HTTP 200, self-canonical, robots not `noindex`.
2. Rendered homepage + article SEO title/description/og:title lengths and copy.
3. Presence/absence and anchor text of internal links among arc posts, About, homepage, hubs.
4. Public REST identity guards: `id`, `slug`, `status`, `link`, `modified`.
5. Redirect health for the retired 11882 slug.
6. Repo/issue chronology: #233 deploy dates, #249 baseline comment, PR #330 About proposal.
7. Confirmation that the **reserved exact-match backlink was never applied** on About or homepage.

## What KK must pull from Search Console (no API here)

SEO Growth Digest source referenced by #198/#233 (`…/seo-growth-weekly/digests/2026-06-17-seo-growth-digest.md`) is **not in this repo or VM**. Without GSC (or a pasted digest), positions/CTR cannot be refreshed.

### Pull checklist (paste into next digest)

**A. Split windows (do not reuse the mixed 06-12→07-09 window alone)**

| Window | Dates (property timezone) | Purpose |
|---|---|---|
| Pre-#233 | ~2026-05-26 → 2026-06-22 | Pre homepage-title + pre companion-cluster baseline |
| Post-#233 | 2026-06-25 → 2026-07-22 (or through today) | Post deploy movement |
| Optional 28-day rolling | last 28 full days ending yesterday | Continuity with issue comment |

**B. Filters / rows**

1. **Page** = `https://kriskrug.co/2026/05/23/you-cant-drink-data/` — impressions, clicks, CTR, average position for each window.
2. **Queries** containing normalized variants of `you cant drink data` / `you can't drink data` (and close misspellings GSC groups) — same four metrics; note 0-click rows.
3. **Page** = `https://kriskrug.co/` — impressions / CTR / avg position (homepage title change side-effect check only).
4. Optional: compare query → landing page mapping (confirm YCDD URL is the dominant landing page for the cluster).

**C. Compare against issue #249 recorded baseline (2026-06-12 → 2026-07-09)**

| Surface | Impressions | Clicks | CTR | Avg position |
|---|---:|---:|---:|---:|
| Landing page 11936 | 294 | 6 | 2.04% | 7.96 |
| Query cluster variants | present | 0 | n/a | 8.4–8.7 |

That baseline already sat mostly in striking distance (roughly positions 8–9) with **impressions but no query clicks**. It is **not** a clean pre/post because it overlaps the deploy dates — hence the split windows above.

**D. Success / next-action thresholds (from July 12 handoff; still valid)**

- Positive directional signal after an approved About edit: ≥1 query-cluster click **and** average position **below 8.4**, measured only after ≥7 full days post-edit.
- If impressions are zero or the seven-day gate fails → record **not yet measurable**, do not claim causation.
- Do not close #249 on public HTML alone.

## Homepage / About backlink decision

**Decision: About page 1208 — apply the single reserved contextual backlink. Do not put the exact-match anchor on the homepage in this pass.**

Reasons (public + prior handoff):

1. Spec + issue acceptance criteria reserved **one** contextual homepage/**About** link with preferred anchor `you can't drink data` (`internal-links.md`).
2. July 12 / PR #330 already chose About: opening copy already joins activism, AI, and human capacity; homepage has a legacy internal slug and no natural exact-match seam.
3. Live 2026-07-26: About still has **zero** YCDD hrefs and still contains the exact paragraph the handoff extends — so the sentence proposal remains the right edit surface.
4. Exact-match homepage footer/hero link would be weaker contextually and competes with speaker-positioning SERP goals of the shortened homepage title.
5. Hub pages (`/ai-ethics/`, Both Hands Full) also lack the link; prefer finishing the **already-reviewed** About sentence before opening a second surface.

### Exact proposal (unchanged copy; refresh guards)

Replace the About opening paragraph with the July 12 review-ready HTML (one added sentence, one exact-match anchor, same-tab internal link):

```html
<p>I have spent two decades documenting technology, art, activism, conferences, communities, and the back rooms where culture actually changes. These days, most of that work points at one question: how do we use AI to increase human capacity instead of flattening human judgment? That question includes the physical costs of AI infrastructure, which I confronted on the streets of Vancouver and wrote about in <a href="https://kriskrug.co/2026/05/23/you-cant-drink-data/">you can't drink data</a>.</p>
```

**Publisher must stop and re-snapshot** if page `1208` `id`/`slug`/`status` differ, if `modified` ≠ freshly fetched value (live was `2026-07-24T17:22:59` at probe time — **do not use the stale 2026-07-01 guard**), if the opening paragraph is no longer unique, or if a YCDD href already exists. Content-only REST (`content` key only). Full gate remains in `fixes/issue-249-you-cant-drink-data-seo-handoff-2026-07-12.md`.

## Next striking-distance targets (from prior digests; not remeasured)

| Query cluster | Disposition (unchanged) |
|---|---|
| `you cant drink data` | Primary — About backlink + GSC split-window read |
| `david zabowski nerdwallet mobile engineering` | No confirmed kriskrug.co target; do not invent links |
| `lord of the rings drinking game` | Legacy/low-strategy; parked (#335 handoff exists separately) |

No new public striking-distance query can be asserted without GSC. After KK pastes the split-window export, the next digest should name any new position-8–15 queries with a clear on-site target.

## Acceptance criteria status (#249)

| Criterion | Status |
|---|---|
| Next SEO digest records pre- vs post-deploy query position (+ homepage impressions/CTR) | **Blocked on KK GSC pull** — windows and baseline documented here |
| Decide homepage/About backlink | **Decide: About 1208**, exact anchor `you can't drink data`; still needs human publisher session |
| Note next striking-distance target | No new target without GSC; prior non-YCDD clusters unchanged |

## Agent-safe closeout

- This report is measurement + recommendation only.
- No live WP, Jetpack, Search Console, or analytics writes.
- Keep #249 open through: (1) KK GSC paste / digest rows, (2) About body-only apply + public readback, (3) ≥7-day remeasure.
- Optional follow-up ticket (not this commit): restore 11936 → 11882 / 11929 outbound contextual links if KK confirms they were lost after 2026-06-28 edits.
