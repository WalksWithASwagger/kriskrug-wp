# #339 Measured July publisher batch: 2026-08-16 live refresh

**Captured:** `2026-08-17T02:20:44Z`
**Issue:** [#339](https://github.com/WalksWithASwagger/kriskrug-wp/issues/339)
**Payloads:** [`content/drafts/339-july-publisher-batch-2026-08-16/`](../../../content/drafts/339-july-publisher-batch-2026-08-16/)
**Supersedes:** [`publisher-batch-prep-339-20260726.md`](publisher-batch-prep-339-20260726.md)
**Mode:** read-only. Public REST + public HTML. No WordPress write. No theme upload. No cache purge.

Lane O of the 2026-08-15 audit ([`BACKLOG-GROOMING-DOSSIER-2026-08-15.md`](BACKLOG-GROOMING-DOSSIER-2026-08-15.md)) was right not to close this. Four of five live content deliverables were never applied. This pass re-fetched every named target and prepared apply-ready payloads for what is still open.

## DONE vs STILL OPEN

| Item | Verdict | Live evidence |
|---|---|---|
| Aurora 1.3.39 zip | **DEAD / obsolete** | Public `style.css` Version **1.6.5**. Repo `theme/kk-aurora/style.css` Version **1.6.6**. Uploading 1.3.39 would downgrade production. |
| #249 About YCDD sentence | **STILL OPEN** | `GET /about/` 200. Count of `you can't drink data` = **0**. Count of `you-cant-drink-data` hrefs = **0**. Page 1208 slug `about`, modified `2026-08-01T09:59:39`. The reserved paragraph is still present once. |
| #328 Most Benevolent wraps | **STILL OPEN** | Post 3814 still has two kriskrug.co body links, both footer (category + AI companions). Post 2950 has `Most Benevolent Outcomes` once, unlinked. Post 2665 has `cultivating the most benevolent outcomes` once, unlinked. Modified guards unchanged since 2026-06-28. |
| #335 LOTR title/desc + footer | **STILL OPEN** | Public title `The Lord of the Rings Drinking Game \| Kris Krüg`. Description is the excerpt opener, not the approved rules copy. Footer on 35 and 58 still points at `/2023/12/28/building-ai-companions-w-john-anthony-hartman-of-ihaverobots/`. |
| #336 AI second brain | **STILL OPEN** | Public title `Build an AI Second Brain That Actually Works` (not the approved `...Works for You`). Description is still the zombies excerpt. Posts 9774 and 12327 still have the unlinked needles. |
| #342 post 11171 href | **STILL OPEN** | `content.rendered` still contains `https://kriskrug.notion.site/keynote-both-hands-full?source=copy_link` once, anchor `both hands full`. Zero `bothhandsfull.com` hrefs in the body. Modified `2026-08-10T18:24:39`. |

Closed issues #249, #328, #335, #336, and #342 closed as repo-side prep or measurement. They are not live-apply receipts.

## Strike the 1.3.39 deploy step

The issue body still asks KK to approve `kk-aurora-seo-metadata-1.3.39-20260713.zip` (SHA-256 `d4a812abe51a1d879be4a290a7381b6d9222a08a4fd1cc2145b1adf67019e86d`) with a 1.3.37 rollback zip. **That checkbox is dead.**

- Live Aurora: **1.6.5** (`https://kriskrug.co/wp-content/themes/kk-aurora/style.css`)
- Repo Aurora: **1.6.6**
- Standard description and per-post search titles are theme-owned (`inc/seo-title.php`, `inc/seo-meta-rest.php` from #661/#677)
- Sampled 1.6.5 routes (home, About, LOTR, AI second brain) each emit one `<meta name="description">`

OG and description work from the 1.3.39 era needs a **separate check against current 1.6.5 theme output**, not a zip rollback. Title-format leftovers belong with issues like #756, not this publisher batch.

Paste-ready replacement for the first #339 checkbox (human edit of the issue):

- [x] ~~Approve deploying Aurora 1.3.39 from `kk-aurora-seo-metadata-1.3.39-20260713.zip`~~ **Struck 2026-08-16.** Live is 1.6.5. Do not upload that zip. OG/description questions go to a current-theme check, not 1.3.39.

## Identity refresh (public REST)

| Role | Type | ID | Slug | Status | `modified` | Drift vs July 13/26 handoff |
|---|---|---:|---|---|---|---|
| #249 source | page | 1208 | `about` | publish | `2026-08-01T09:59:39` | **STALE vs both prior guards** |
| #249 target | post | 11936 | `you-cant-drink-data` | publish | `2026-08-10T18:24:37` | drifted (link target only; no write) |
| #328 target | post | 3814 | `the-power-of-most-benevolent-outcomes-...` | publish | `2026-06-28T20:37:13` | OK |
| #328 src 1 | post | 2950 | `community-weaving-...` | publish | `2026-06-28T20:38:58` | OK |
| #328 src 2 | post | 2665 | `embracing-the-future-...` | publish | `2026-06-28T20:39:43` | OK |
| #335 SEO + footer | post | 35 | `the-lord-of-the-rings-drinking-game` | publish | `2026-06-14T22:30:33` | OK |
| #335 pair | post | 58 | `mcsweeneys-lists` | publish | `2026-06-14T22:29:25` | OK |
| #336 SEO | post | 8802 | `how-to-build-an-ai-second-brain-...` | publish | `2026-06-28T20:27:34` | OK (meta content still wrong) |
| #336 src 1 | post | 9774 | `what-journalists-need-to-know-about-ai-right-now` | publish | `2026-06-14T20:05:53` | OK |
| #336 src 2 | post | 12327 | `storyhive-haus-of-owl-jordan-dack` | publish | `2026-07-18T11:20:49` | same as 2026-07-26 refresh |
| #342 source | post | 11171 | `both-hands-full` | publish | `2026-08-10T18:24:39` | **STALE vs July 13 guard** |

WordPress generator: `7.0.4`. Compact capture: `content/drafts/339-july-publisher-batch-2026-08-16/live-evidence-compact.json`.

## SEO field note (posts 35 and 8802)

Public REST now returns `jetpack_seo_html_title` and `advanced_seo_description` on posts. Both targets already have non-empty values, so `make seo-backfill` additive mode will skip them. Use `seo-meta-overwrite.json` with `--from-file` after an explicit overwrite tick.

## What this session did not do

- No PATCH, POST, or DELETE to WordPress
- No theme SFTP / zip upload
- No cache purge
- No GitHub issue-body mutation (KK still owns the checklist edit)
- No Search Console or GA4 calls

## Next handoff

A publisher session with `WP_USER` + `WP_APP_PASSWORD`, KK ticks on the refreshed checklist, snapshots under `backup/<UTC>-july-publisher/`, and the apply order in the payload README. Rollback is the snapshotted `content.raw` / prior meta. Pagely revisions are not a safety net ([INCIDENT-2026-05-15](../INCIDENT-2026-05-15-overwritten-post.md)).
