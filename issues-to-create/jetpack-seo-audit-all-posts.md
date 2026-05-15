# Audit Jetpack SEO meta on all blog posts (title, description, social share)

**Labels:** `seo`, `content`, `audit`, `priority/high`
**Estimated effort:** 6–10 hours (depends on how many posts get touched)
**Related:** [`docs/current-state/SEO_AUDIT.md`](../docs/current-state/SEO_AUDIT.md), `docs/current-state/CONTENT_AUDIT.md`, FIX_QUEUE P1.1

## Why

Jetpack's SEO Tools module gives **per-post overrides** for:

- **SEO title** (`jetpack_seo_html_title`) — what appears in `<title>` and Google SERPs
- **Meta description** (`advanced_seo_description`) — the snippet in SERPs and AI Overviews
- **Social share message** (`jetpack_publicize_message`) — the text auto-tweeted/posted when Jetpack Publicize fires

Most existing posts on kriskrug.co don't have these set. They fall back to:
- SEO title = post title + site tagline (often >60 chars, gets truncated in SERPs)
- Meta description = first paragraph or AI-generated excerpt (often third-person, off-brand)
- Social share = post title alone (no hook, no voice)

This audit catches the gap and brings every post up to a baseline.

## Scope

**In scope (this issue):**
- All 941 published `post` posts on kriskrug.co
- The 34 published `page`s (separate sub-list — pages don't need social-share but do need SEO title + description)
- Audit only — fixing is a follow-up batch per cohort

**Out of scope (for now):**
- Attachment SEO
- `jetpack-testimonial` CPT
- `transcript` CPT (recently added by [`inc/digital-composting.php`](../inc/digital-composting.php))

## Approach

### 1. Inventory current state

Run a script that pulls `meta.jetpack_seo_html_title`, `meta.advanced_seo_description`, `meta.jetpack_publicize_message`, and `excerpt` for every post (paginate REST API) and dumps to CSV.

Script lives at `scripts/seo-audit/inventory.py` (to be written; mirror the structure of `scripts/notion-to-wp/`).

Columns:
- post_id, slug, link, published_date, modified_date, category, traffic_band (if GA4 available), word_count
- has_seo_title (bool), seo_title_length, seo_title_truncates (>60 chars)
- has_meta_desc (bool), meta_desc_length, meta_desc_first_person (regex: starts with "I" or "My"?)
- has_social_message (bool), social_length
- excerpt_present, excerpt_first_person (same heuristic)

### 2. Cohort by priority

Group posts into bands so we don't try to fix all 941 at once:

| Cohort | Definition | Target |
|---|---|---|
| **A: Top 20 by traffic** | GA4 top-20 in last 12 months | Fully hand-curated SEO title + description + share message |
| **B: Recent 2024+** | ~140 posts since 2024-01-01 | Curated where worth it, auto-derived (from article body, KK voice) elsewhere |
| **C: Evergreen anchors** | The 10 from [CONTENT_AUDIT.md §2.5](../docs/current-state/CONTENT_AUDIT.md) | Hand-curated |
| **D: Long tail** | Everything else (~770 posts) | Auto-derive only; flag any that 404 or have empty body |

### 3. Fix mechanism

Two paths:
- **Manual via wp-admin** for cohort A + C (~30 posts) — KK opens each in editor, sets the Jetpack SEO box.
- **Programmatic via REST** for cohorts B + D — adapt the excerpt-derivation logic from [`scripts/notion-to-wp/kk_notion_to_wp.py`](../scripts/notion-to-wp/kk_notion_to_wp.py) (the `derive_excerpt`, `derive_seo_title`, `derive_social_message` functions). Idempotent — only updates posts where the field is currently empty.

The REST PATCH pattern is proven (see `scripts/notion-to-wp/`): authenticate with the existing Application Password, send `meta: { jetpack_seo_html_title, advanced_seo_description, jetpack_publicize_message }` on `POST /wp-json/wp/v2/posts/{id}`. WP 6.9 + Jetpack 15.8 accept these keys without `register_post_meta()` because Jetpack registers them itself.

### 4. Pull KK voice from article body, not AI summaries

**Don't reuse the auto-generated AI summary** as the meta description — it's third-person ("The author attended..."), generic, and off-brand. Instead:

- For long-form posts: pull the first substantive callout / pullquote / opening paragraph
- Strip leading "The short version:" / "TL;DR:" / "Summary:" markers
- Take first 1–3 sentences up to ~250 chars

The Notion connector now does this by default — same logic applies to the audit script.

## Acceptance criteria

- [ ] Inventory CSV exists at `content/seo-audit-YYYY-MM-DD.csv` covering all 941 posts + 34 pages
- [ ] Cohort A posts (top 20) all have hand-curated SEO title, meta description, and social share message in KK voice
- [ ] Cohort C evergreen anchors have the same
- [ ] Cohort B + D have auto-derived values via the audit script; script logs every change to `content/seo-audit-YYYY-MM-DD.log`
- [ ] Final CSV re-pulled and diff'd against the original: every post in cohorts A–C has `has_seo_title=true`, `has_meta_desc=true`, `has_social_message=true`
- [ ] Random sample of 10 posts spot-checked via the live site: SEO title appears in `<title>`, meta description appears in `<meta name="description">`, social share message appears in the post's "Sharing" panel in wp-admin
- [ ] [`docs/current-state/CHANGELOG.md`](../docs/current-state/) (new file) records what was changed and when, with the post ID ranges by cohort

## Prerequisites

- [ ] WP Application Password is in place (already done — used by `scripts/notion-to-wp/`)
- [ ] GA4 access for cohort A traffic data (optional but strongly recommended; otherwise cohort A becomes "the 10 evergreen anchors only")
- [ ] One verified backup exists in `backup/` (per [`docs/current-state/BACKUP_PLAN.md`](../docs/current-state/BACKUP_PLAN.md)) — REST PATCHes are reversible per-post but a backup gives the nuclear option

## Risk + rollback

- Each REST PATCH only touches the three meta keys named above. No body content is touched.
- Worst case for the auto-derived cohort: the description sounds slightly generic on some long-tail posts. Easily re-runnable to overwrite.
- Each batch logs every change; reverting is `for id in failed_ids: PATCH /posts/{id} meta={…empty…}`.

## Notes

- See [`docs/current-state/SEO_AUDIT.md` §2.2](../docs/current-state/SEO_AUDIT.md) for the upstream finding that prompted this work.
- This issue depends on **none** of the FIX_QUEUE P0 items, so it can run in parallel with the schema + llms.txt + robots.txt work.
- After this lands, P1.5 ("rewrite long titles to fit 60-char SERP window") becomes trivial — most of it is already captured by the SEO title overrides.

---

**Filing:** Once ready, file with `gh issue create -F issues-to-create/jetpack-seo-audit-all-posts.md -t "Audit Jetpack SEO meta on all blog posts"`.
