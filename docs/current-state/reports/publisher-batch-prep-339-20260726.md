# #339 Measured July Kris publisher batch — PREP ONLY

**Captured:** `2026-07-26T20:40:00Z`  
**Issue:** [#339](https://github.com/WalksWithASwagger/kriskrug-wp/issues/339) — `[SEO] Run the measured July Kris publisher batch`  
**Companion orchestration:** [#363](https://github.com/WalksWithASwagger/kriskrug-wp/issues/363)  
**Prior prep:** [`issue-363-publisher-orchestration-prep-20260716.md`](issue-363-publisher-orchestration-prep-20260716.md)  
**This session:** inventory + dry-run command sheet + guard refresh. **No live WordPress write. No publisher `--execute`. No theme upload. No cache purge. No GSC submit.**

**Optional checklist:** [`content/drafts/339-july-publisher-batch-checklist-2026-07-26.md`](../../../content/drafts/339-july-publisher-batch-checklist-2026-07-26.md)

---

## Verdict

Repo handoffs for the measured July batch are still green. Live Aurora is already **1.4.8** (the original 1.3.39 / 1.3.40 deploy checkbox is obsolete). Two source `modified` guards have drifted and must be refreshed before any write. Post **8802** already emits a *different* search title and meta description than the #339 checklist — that is an overwrite decision, not an additive backfill. Secrets are **absent** in this Cloud session, so authenticated dry-runs are blocked until `WP_USER` / `WP_APP_PASSWORD` are attached. **Do not run the live batch without KK ticks + dry-run proof.**

---

## Stop conditions (current)

| # | Gate | Status 2026-07-26 |
|---|---|---|
| 1 | KK exact-approval checklist on #339 | **Unchecked** (issue body still lists obsolete Aurora **1.3.39** zip) |
| 2 | Live Aurora SEO owner (standard description + Jetpack search titles) | **Live 1.4.8** / repo **1.4.8** — deploy prerequisite from July-13/16 is **superseded**, not pending |
| 3 | Fresh ID / slug / status / `modified` guards | **2 stale:** page `1208` About; post `12327` Storyhive |
| 4 | Authenticated REST preflight | **Blocked** — `WP_USER` / `WP_APP_PASSWORD` length `0`; July-14 comment already recorded `401` on `context=edit` |
| 5 | Dry-run proof reviewed by KK | **Not started** (cannot dry-run meta/body paths without creds) |
| 6 | Snapshot under `backup/<UTC>-july-publisher/` | **Not started** |

Until 1–5 clear, agents stop before any write.

---

## What the batch contains

One dependency-ordered production lane. Keep **#331** (archive indexability) and remaining **#353** body-H1 routes out.

### A. Theme / SEO owner (prerequisite — already on live)

| Item | Original #339 ask | 2026-07-26 readback |
|---|---|---|
| Aurora | Deploy 1.3.39 (issue) → later 1.3.40 (work plan / #363) | Live `style.css` **Version: 1.4.8** (byte-aligned with repo) |
| Standard meta description | One owner; 116-URL regression | Sample routes emit `<meta name="description">` (home, blog, about, LOTR, AI second brain) |
| Homepage OG title | Repair | Present: `Kris Krug \| AI Keynote Speaker & Creative Technologist` |
| Blog canonical | Repair | Present: `https://kriskrug.co/blog/` |
| Schema / news | Out of #339 scope; #425 rules apply | `make seo-publisher-smoke` **PASS** (sitemap, feed, news-sitemap, BlogPosting samples) |

**KK action on issue body:** replace the first checklist item. Do **not** approve uploading 1.3.39 or 1.3.40. Acknowledge live **1.4.8** as the SEO-owner baseline (or name a newer deploy if one is planned). Content checkboxes below stay as written.

### B. SEO fields (posts 35 + 8802)

| Issue | Post | Slug | Approved `jetpack_seo_html_title` | Approved `advanced_seo_description` | Live public title now | Live public description now |
|---|---:|---|---|---|---|---|
| #335 | 35 | `the-lord-of-the-rings-drinking-game` | `The Lord of the Rings Drinking Game: 4 Original Rules` | `Four original Lord of the Rings drinking game rules for Frodo, Sam, Legolas, and cliff falls, plus a trilogy marathon option. Play responsibly.` | `The Lord of the Rings Drinking Game \| Kris Krüg` (default + site name) | Excerpt-derived opener (not approved copy) |
| #336 | 8802 | `how-to-build-an-ai-second-brain-that-actually-works-for-you` | `Build an AI Second Brain That Actually Works for You` | `Build an AI second brain that works with your thought patterns, captures creative chaos, and turns scattered notes and voice memos into finished work.` | `Build an AI Second Brain That Actually Works` (**already custom; missing “for You”**) | Different excerpt-style copy already present |

**Implication:** post 35 is still a first-write of the approved fields. Post 8802 needs KK to **explicitly approve overwriting** the live title/description — additive `make seo-backfill` will skip non-empty keys. Use `--from-file` overwrite mode only after that tick.

### C. Body / href patches (content-only REST)

| Issue | Change | Source ID | Source slug | Target | Handoff | Live patch state |
|---|---|---:|---|---|---|---|
| #249 | One new About sentence + YCDD internal link | page **1208** | `about` | post 11936 / `you-cant-drink-data` | `fixes/issue-249-*` | Opening paragraph **still matches**; **no** YCDD link yet. **`modified` drifted** (see guards) |
| #328 | Wrap two existing phrases | posts **2950**, **2665** | community-weaving…, embracing-the-future… | post 3814 | `fixes/issue-328-*` | Needles present once each; **not linked** |
| #335 | Related-footer pair 35 ↔ 58 | posts **35**, **58** | LOTR, `mcsweeneys-lists` | each other | `fixes/issue-335-*` | Still needs authenticated `content.raw` to derive footer-only patch |
| #336 | Wrap two existing phrases | posts **9774**, **12327** | journalists AI, storyhive… | post 8802 | `fixes/issue-336-*` | Bare phrases present; **not linked**. **`12327` `modified` drifted** |
| #342 | Href-only on one anchor | post **11171** | `both-hands-full` | `https://www.bothhandsfull.com` | `fixes/issue-342-*` | Notion keynote href **still on the exact sentence**; a separate `Both Hands Full` → bothhandsfull.com link exists elsewhere — do not conflate |

### Explicitly not in this batch

- #331 taxonomy / archive noindex / sitemap scope  
- #353 remaining multi-H1 body migrations  
- #340 / #341 `bc-ai.net` → `bc-ai.ca` replacements (30 ready; needs **separate** exact approval)  
- #316 schema snippet identity, #345 `blogname`, GSC indexing quota, DNS/GA4  

---

## Public identity refresh (2026-07-26)

Anonymous REST only (`_fields=id,slug,status,modified,link,title`). Stop on any further drift at action time.

| Role | Type | ID | Slug | Status | `modified` (live) | Handoff guard | Drift |
|---|---|---:|---|---|---|---|---|
| #249 target | post | 11936 | `you-cant-drink-data` | publish | `2026-06-28T18:40:25` | same | OK |
| #249 source | page | 1208 | `about` | publish | `2026-07-24T17:22:59` | was `2026-07-01T11:33:51` | **STALE** — refresh guard; re-confirm paragraph exactness in `content.raw` |
| #328 target | post | 3814 | `the-power-of-most-benevolent-outcomes-…` | publish | `2026-06-28T20:37:13` | same | OK |
| #328 src P1 | post | 2950 | `community-weaving-…` | publish | `2026-06-28T20:38:58` | same | OK |
| #328 src P2 | post | 2665 | `embracing-the-future-…` | publish | `2026-06-28T20:39:43` | same | OK |
| #335 target + footer | post | 35 | `the-lord-of-the-rings-drinking-game` | publish | `2026-06-14T22:30:33` | same | OK |
| #335 pair | post | 58 | `mcsweeneys-lists` | publish | `2026-06-14T22:29:25` | same | OK |
| #336 target | post | 8802 | `how-to-build-an-ai-second-brain-…` | publish | `2026-06-28T20:27:34` | same | OK (meta content differs from checklist) |
| #336 src P1 | post | 9774 | `what-journalists-need-to-know-about-ai-right-now` | publish | `2026-06-14T20:05:53` | same | OK |
| #336 src P2 | post | 12327 | `storyhive-haus-of-owl-jordan-dack` | publish | `2026-07-18T11:20:49` | was `2026-06-17T19:47:06` | **STALE** — refresh guard; re-confirm needle in raw |
| #342 source | post | 11171 | `both-hands-full` | publish | `2026-06-28T20:26:51` | same | OK |

WP publicly reports **7.0.2**. Schema smoke: **PASS**.

---

## Schema / publisher surface prerequisites

Per [`SEO-PUBLISHER-SCHEMA-2026-07-19.md`](../SEO-PUBLISHER-SCHEMA-2026-07-19.md) and [`SEO-INDEXING-RUNBOOK.md`](../SEO-INDEXING-RUNBOOK.md):

- Default post schema remains **`BlogPosting`** (Code Snippet 5). This batch does **not** change schema type.
- News sitemap at `/news-sitemap.xml` is live (Snippet 13); empty urlset is valid when no 48h NewsArticle posts.
- Preflight: `make seo-publisher-smoke` (read-only; no secrets). Passed this session.
- Do not mix taxonomy sitemap / archive-index work (#331) into this publisher session.

---

## Slug-safety reminders (INCIDENT-2026-05-15)

From [`INCIDENT-2026-05-15-overwritten-post.md`](../INCIDENT-2026-05-15-overwritten-post.md) — mandatory for every write in this batch:

1. **Slug + ID together.** Resolve by `?slug=` or known ID, then confirm **both** match the handoff before PATCH.
2. **Never trust `meta_key` / `meta_value` REST filters** for identity — WP ignores unregistered keys and can return “most recent post.”
3. **CREATE default; UPDATE opt-in.** Notion connector: no `--update` without `--diff` first. Body patches here are deliberate UPDATEs — still require identity guards.
4. **Title / identity sanity.** Abort if live title/slug/`modified` diverge from the locked handoff (after intentional guard refresh).
5. **Minimal payload.** Body writes: top-level key **`content` only**. Meta writes: allowlisted Jetpack keys only (`jetpack_seo_html_title`, `advanced_seo_description`, optionally social). Never send title, slug, status, date, taxonomies, featured media, or unrelated meta in the same request.
6. **Snapshot before write.** Authenticated edit-context response + public HTML + SHA-256 under `backup/<UTC>-july-publisher/` (and per-issue subdirs as handoffs specify). Retain as rollback.
7. **One write → readback → next.** Authenticated raw + anonymous HTML. Roll back immediately on guard/route failure.
8. **Pagely revisions are not a safety net.** Do not assume WP stored a revision.

---

## Exact dry-run / preflight commands

Credential-free first (this session can run these):

```bash
make status-readonly
make seo-publisher-smoke
make verify
# family handoff unit tests (already green 2026-07-26: 33 OK)
python3 -m unittest \
  scripts.tests.test_issue_249_seo_handoff \
  scripts.tests.test_issue_328_seo_handoff \
  scripts.tests.test_issue_335_lotr_seo_handoff \
  scripts.tests.test_issue_336_ai_second_brain_seo_handoff \
  scripts.tests.test_issue_342_both_hands_full_link_handoff -v
```

After secrets are present (redacted presence check only — print lengths, never values):

```bash
# presence only
python3 -c 'import os; print("WP_USER", len(os.environ.get("WP_USER",""))); print("WP_APP_PASSWORD", len(os.environ.get("WP_APP_PASSWORD","")))'

# read-only inventory (must not 401)
FORMAT=json make seo-audit

# SEO field dry-run for LOTR + AI second brain (NO --execute)
# Prefer explicit from-file overwrite plan KK reviews; additive path skips 8802 if meta non-empty.
scripts/notion-to-wp/.venv/bin/python scripts/seo-backfill/backfill_meta.py \
  --ids 35,8802 --kind post --fields seo_title,meta_desc

# After KK approves exact overwrite JSON (example path; create only when KK asks):
# scripts/notion-to-wp/.venv/bin/python scripts/seo-backfill/backfill_meta.py \
#   --from-file content/drafts/339-july-publisher-batch-checklist-2026-07-26/seo-meta-overwrite.json \
#   --kind post
# Review planned vs old values. Live only with EXECUTE=1 / --execute after ticks + snapshot.
```

Body patches are **not** Notion connector publishes. Dry-run pattern per handoff:

1. `GET` edit-context by ID with `_fields=id,slug,status,modified,title,content` (and `meta` for SEO targets).  
2. Assert slug / status / refreshed `modified` / needle counts.  
3. Diff proposed `content` (or meta) against snapshot — human review.  
4. Only then `POST` minimal payload.  
5. Do **not** use `kk_notion_to_wp.py --update` for these surgical patches.

Optional Notion-style dry-run reminder (unrelated to this batch’s body surgery, but same safety culture):

```bash
# Never the live path for #339 patches — shown only as connector safety reference
# python kk_notion_to_wp.py --dry-run …   then   --diff …   before any --update
```

---

## Publisher sequence (when unlocked)

Mirror #339 + work-plan Phase 2; do not reorder:

1. Quote KK’s approved checklist wording (including Aurora **1.4.8** baseline + any 8802 overwrite tick) in the session log.  
2. Refresh every target/source ID, slug, status, `modified`, raw body, SEO fields, canonical — stop on stale.  
3. Snapshot under `backup/<UTC>-july-publisher/` with SHA-256.  
4. Confirm live Aurora **1.4.8** still owns standard description / search titles; spot-check regression sample (116 URLs if the existing script/list is used).  
5. Apply SEO fields for **35** then **8802** (overwrite JSON only if KK approved).  
6. Apply body patches in order: **#249 → #328 → #335 footers → #336 → #342**. One write + readback each.  
7. Authenticated + anonymous readback; schedule measurement windows (#249 ≥7d; others ≥14d / 28d as specified).  
8. Update source issues with live timestamp. **Do not** burn GSC indexing quota in-session.

---

## Repo readiness

| Packet | Files | Unit tests 2026-07-26 |
|---|---|---|
| #249 | `fixes/issue-249-you-cant-drink-data-seo-handoff-2026-07-12.{md,json}` | OK |
| #328 | `fixes/issue-328-most-benevolent-seo-handoff-2026-07-12.{md,json}` | OK |
| #335 | `fixes/issue-335-lotr-drinking-game-seo-handoff-2026-07-13.{md,json}` | OK |
| #336 | `fixes/issue-336-ai-second-brain-seo-handoff-2026-07-13.{md,json}` | OK |
| #342 | `fixes/issue-342-both-hands-full-link-handoff-2026-07-13.{md,json}` | OK |

---

## KK checklist refresh (paste into #339)

Replace the obsolete Aurora deploy line; keep content lines; add overwrite + guard lines:

- [ ] Acknowledge live Aurora **1.4.8** as the SEO-owner baseline for this batch (do **not** upload 1.3.39 / 1.3.40 zips).  
- [ ] Approve AI second-brain search title: `Build an AI Second Brain That Actually Works for You` — **including overwrite** of live `Build an AI Second Brain That Actually Works`.  
- [ ] Approve AI second-brain description (exact #339 wording) — **including overwrite** of the live excerpt-style description.  
- [ ] Approve LOTR search title + description (exact #339 wording).  
- [ ] Approve About-page sentence from #249 (exact wording).  
- [ ] Approve four copy-preserving link insertions in #328 and #336.  
- [ ] Approve href-only replacement on post 11171 (Notion → `https://www.bothhandsfull.com`), preserving anchor `both hands full`.  
- [ ] Approve LOTR / McSweeney’s related-footer pair (#335).  
- [ ] Acknowledge refreshed `modified` guards for page **1208** (`2026-07-24T17:22:59`) and post **12327** (`2026-07-18T11:20:49`) after raw needle reconfirm.  
- [ ] Approve dry-run evidence + snapshot path before any `--execute` / REST write.

---

## Measurement windows (after live + public readback)

| Issue | Wait | Baselines (locked in handoffs) |
|---|---|---|
| #249 | ≥7 full days (+ 28d compare) | Page 294/6/2.04%/7.96; query cluster 0 clicks @ 8.4–8.7 |
| #328 | ≥14 days (+ 28d where specified) | Query `most benevolent` 20 impr / pos 8.4 / 0% CTR |
| #335 | ≥14 / 28 days | Page 47/0/0%/10.43; query 27/0/0%/9.96 |
| #336 | ≥14 days | Page 1053/10/0.95%/11.27; query 46/2/@17.52 |
| #342 | ≥14 days post-recrawl | Article 56/3/5.36%/8.27; property/homepage low volume |

Do not claim causation before recrawl.

---

## Session evidence

- Branch intent: `cursor/339-publisher-batch-prep-f196` (docs only).  
- Secrets: absent (`WP_USER` / `WP_APP_PASSWORD` / `NOTION_TOKEN` length 0).  
- Live Aurora: **1.4.8**. WP: **7.0.2**.  
- `make seo-publisher-smoke`: PASS.  
- Handoff unit tests: 33 OK.  
- Live writes this session: **none**.
