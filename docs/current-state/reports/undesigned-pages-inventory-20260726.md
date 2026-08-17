# Issue #122 — Undesigned generic content pages inventory

**Captured:** `2026-07-26` (public sitemap + logged-out HTML readback only; **no WP auth writes**).
**Branch:** `cursor/122-undesigned-pages-f196`
**Parent:** [#122](https://github.com/WalksWithASwagger/kriskrug-wp/issues/122)
**Companion priority list:** [`content/drafts/2026-07-26-undesigned-pages/PRIORITY.md`](../../../content/drafts/2026-07-26-undesigned-pages/PRIORITY.md)

## Verdict

The original “~25 undesigned pages” claim is still directionally right for the **long tail**, but the surface has changed:

1. **Floor lift already shipped** — PR [#166](https://github.com/WalksWithASwagger/kriskrug-wp/pull/166) added `aurora-prose` to `templates/page.html`, so ordinary pages are no longer typographically bare.
2. **Fifteen high-value pages already got Aurora content primitives** (2026-07-01 Trust + Offers + Topic Hubs; see [`CONTENT-ARCHITECTURE-RESET-2026-07-01.md`](../archive/CONTENT-ARCHITECTURE-RESET-2026-07-01.md)).
3. **What remains for #122** is the prioritized split: a few **bespoke content redesigns** (nav / commercial / proof) vs **generic `page` template polish** for the true long tail — **without** a theme stylesheet rebuild ([#474](https://github.com/WalksWithASwagger/kriskrug-wp/issues/474)+).
4. **Services** (`/generative-ai-services/`) stays on [#420](https://github.com/WalksWithASwagger/kriskrug-wp/issues/420), not this ticket’s execution queue.

## Method

| Source | Use |
|---|---|
| `https://kriskrug.co/wp-sitemap-posts-page-1.xml` | Canonical published page URL set (**46** locs) |
| Public HTML `GET` (logged out) | Template chrome + content markers |
| Repo docs / issues | Prior waves, open page tickets |

**Undesigned signal (this pass):** theme `aurora-page-*` chrome + WP title H1, **without** Aurora content primitives (`aurora-proof-*`, `aurora-display-heading`, `aurora-page-lead`, `kk-services*`, `kk-publications*`, `kk-sponsor*`, `kk-r9-pack`). Legacy class families (`user-infos`, dated offer prose, empty body) also count.

**Not used:** authenticated WP REST PATCH, Site Editor writes, theme CSS edits.

## Approach recommendation

| Lane | When | How |
|---|---|---|
| **A — Improve generic `page` template** | Long-tail / utility / multilingual / policy | Keep one `templates/page.html`. After [#474](https://github.com/WalksWithASwagger/kriskrug-wp/issues/474)+ lands, add modest floor features (optional featured image band, title suppress when body opens with `aurora-display-heading`, shared CTA strip). **Do not** ship a parallel CSS rebuild for pages now. |
| **B — Bespoke treatment** | High commercial / nav / proof pages | Prefer **body-only Aurora primitives** (Jul 1 pattern) over new hardcoded `page-*.html` templates. Hardcoded templates that omit `wp:post-content` caused the 2026-05-25 masking incident — do not repeat. Dedicated FSE templates only when layout truly cannot live in post content, and only with a rollback path. |
| **C — Out of #122 execution** | Services rethink | [#420](https://github.com/WalksWithASwagger/kriskrug-wp/issues/420) owns copy + scroll + stylesheet coordination. |
| **D — Triage / archive** | Empty, duplicate, or expired offer pages | Content ops decision (redirect / noindex / merge) before design spend. |

**Decision rule:** If the page is in primary nav, sells an offer, or is a booking/proof surface → **B**. If it is a language intro, policy, glossary, thin archive, or dated course landing → **A** (or **D**). Topic hubs already on Aurora primitives → **maintain via A**, not new bespoke templates.

## Inventory by bucket

### 0) Out of scope for “generic page undesigned”

| Path | Why |
|---|---|
| `/` | `front-page` template |
| `/blog/` | Posts-page / writing archive (`home` / index lane) |
| `/generative-ai-services/` | Has Aurora services body; redesign tracked as **#420** |

### 1) Already Aurora-primitivized (Jul 1) — still on generic `page.html`

These are **not** “bare title + legacy blob” anymore, but they still share the single `page` chrome (theme H1 + content kickers). Open page tickets refine layout/copy; do not re-migrate from scratch.

| Path | ID | Notes / related |
|---|---:|---|
| `/about/` | 1208 | **#418** (backgrounds / double public trail); bio enrichment #269/#270 |
| `/contact/` | 2418 | **#421** closed (portrait + newsletter language); keep as reference |
| `/work/` | 2672 | Proof grid in content; no dedicated open PAGE issue as of this pass |
| `/speaking/` | 1887 | **#419** multimedia rebuild |
| `/responsible-ai-professional/` | 11914 | Offer / education |
| `/podcast-guesting-page-epk/` | 3609 | Media booking |
| `/vancouver-ai/` | 12315 | Topic hub |
| `/ai-for-creatives/` | 12316 | Topic hub |
| `/ai-events/` | 12317 | Topic hub |
| `/ai-ethics/` | 12318 | Topic hub |
| `/ai-tools/` | 12321 | Topic hub |
| `/ai-for-journalists/` | 12320 | Topic hub |
| `/ai-conversations/` | 12319 | Topic hub |
| `/indigenous-ai/` | 12322 | Topic hub |

### 2) Content-designed but still generic-chrome (post–Jul 1)

| Path | ID | Markers | Recommendation |
|---|---:|---|---|
| `/publications/` | 1895 | `kk-publications*` | **Bespoke polish** (proof/archive wave) — content-side |
| `/sponsor-deck/` | 12625 | `kk-sponsor*` | Maintain; already rebuilt 2026-07-24 (#459) |
| `/photography/` | 12013 | `kk-page` + gallery | **Bespoke** light (gallery rhythm) |
| `/events/` | 2250 | partial `aurora-proof-*` | **Bespoke** light / split upcoming vs archive |

### 3) True long-tail undesigned (bare / legacy) — ~25 surfaces

These match the spirit of #122: generic `page` title + legacy or thin content, little or no Aurora primitive structure.

#### 3a) Proof / authority / archive (prefer bespoke content packets)

| Path | ID | Readback notes |
|---|---:|---|
| `/testimonials/` | 2409 | Legacy `user-infos` quote stack; feeds homepage **#415** |
| `/motleykrug-podcast/` | 2828 | Long legacy body + media |
| `/the-kk-worldview/` | 3948 | Short authority essay, no Aurora sections |
| `/reconciliation-indigenous-land-acknowledgement/` | 3899 | Short; related **#22** land acknowledgment |
| `/news/` | 2389 | ~39 words; thin press-clip stub |

#### 3b) Marketing / offer landings (template polish **or** triage)

| Path | ID | Readback notes |
|---|---:|---|
| `/ai-upgrade-for-creative-professionals/` | 6770 | Long course landing; dated “Starts January 14, 2025” |
| `/ai-upgrade-for-modern-media-leaders/` | 7610 | Same family; long legacy blocks |
| `/ai-upgrade-community-coaching-w-kris-krug-peter-bittner/` | 6755 | Short coaching landing |
| `/generative-ai-workshop-for-artists-creatives/` | 2603 | Workshop landing, plain prose |
| `/art-island-perspectives-from-a-creative-community/` | 2543 | Legacy project page |
| `/cinematic-podcasts-agencia-grade-storytelling-meets-generative-ai/` | 7764 | Offer/project page (200) |
| `/sponsor-cyberpunk-chronicles-newsletter/` | 3969 | Long sponsor pitch; `/sponsor` redirects here |

#### 3c) Multilingual intro pages (template polish; one shared pattern)

| Path | ID |
|---|---:|
| `/japanese-introduction-page-kaykaysan/` | 3595 |
| `/chinese-introduction-kang-jia/` | 3598 |
| `/russian-introduction-kristofor-kruglov/` | 3600 |
| `/farsi-introduction-khalil-khalifa/` | 3601 |
| `/swahili-introduction-kintu-krowfeather-…/` | 3603 |
| `/hindi-introduction-krishna-vishwanathapriyadhanvanshi/` | 3606 |
| `/urdu-language-introduction-kris-krug/` | 3696 |
| `/karibu-kwenye-kabila-…-swahili-welcome-page/` | 3623 |

Eight language intros + a second Swahili welcome URL. Same structure (title + paragraphs). **One shared content pattern** beats eight bespoke templates.

#### 3d) Policy / utility (template polish only)

| Path | ID | Notes |
|---|---:|---|
| `/privacy-policy/` | 2985 | Prose policy |
| `/product-review-policy-instructions/` | 3974 | Long policy |
| `/glossary/` | 11887 | Long definition list; no Aurora structure |

#### 3e) Triage candidates (design spend blocked on ops decision)

| Path | ID | Why |
|---|---:|---|
| `/subscribe/` | 2808 | Main body effectively **empty** in public readback |
| `/home/` | 2315 | “Recent Posts & Updates” page; overlaps `/blog/` |
| Duplicate Swahili welcome vs intro | 3623 / 3603 | Consolidate or 301 |

## Counts

| Bucket | Count |
|---|---:|
| Published pages (sitemap) | **46** |
| Out of generic-page scope (home, blog, Services/#420) | 3 |
| Already primitivized (Jul 1) | 14 (+ Services counted above) |
| Content-designed post–Jul 1 (pubs / sponsor / photo / events) | 4 |
| True long-tail undesigned (3a–3d) | **~25** |
| Triage-first (3e, excluding double-count) | 2–3 |

The ~25 long-tail figure in the issue title still holds for bucket 3.

## Prior art / do-not-regress

| Event | Lesson |
|---|---|
| PR [#135](https://github.com/WalksWithASwagger/kriskrug-wp/pull/135) (2026-05-26) | Retired hardcoded Work/Speaking/Services/Publications templates so DB content renders again |
| PR [#166](https://github.com/WalksWithASwagger/kriskrug-wp/pull/166) | Floor lift via `aurora-prose` on `page.html` |
| Content architecture 2026-07-01 | Body-only Aurora primitives beat page-specific CSS class sprawl |
| Stylesheet rebuild [#423](https://github.com/WalksWithASwagger/kriskrug-wp/issues/423) / [#474](https://github.com/WalksWithASwagger/kriskrug-wp/issues/474)+ | **No page-theme CSS campaign in this ticket**; defer structural `page.html` CSS to post-scaffold |

## Acceptance mapping (#122)

| AC | Status after this doc |
|---|---|
| Define approach: improved generic `page` and/or custom for high-value | **Done** (Approach section) |
| Services redesigned (tracked separately) | **Owned by #420** (not closed here) |
| Consistent spacing / hero across content pages | **Partial** — prose floor live; shared hero still deferred to post-#474 template polish + content packets |
| Prioritized list: bespoke vs template polish | **Done** — see `PRIORITY.md` |

## Next execution order (suggested)

1. KK confirm **PRIORITY.md** tiers (especially triage of `/subscribe/`, `/home/`, AI Upgrade dates).
2. Content packets for **P1 bespoke** (Testimonials, Publications, Photography, Events, Worldview) using Jul 1 primitives — Track A commits, no theme rebuild.
3. One shared multilingual intro payload (Track A) applied across the eight intros.
4. After #474 scaffold is safe: small `page.html` floor PR (title suppress + optional media band) closing the “consistent hero” AC without per-page templates.

## Reproduce

```bash
curl -sL https://kriskrug.co/wp-sitemap-posts-page-1.xml | grep -oE 'https://kriskrug.co/[^<]+'
# then logged-out GET each path; classify by presence of aurora-proof / kk-services / kk-publications / kk-sponsor / kk-r9-pack
```
