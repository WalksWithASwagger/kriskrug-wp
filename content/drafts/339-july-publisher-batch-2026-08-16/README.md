# #339 July publisher batch, refreshed 2026-08-28

**Status:** PREP ONLY. Authenticated read-only guards refreshed; no live WordPress write.
**Issue:** [#339](https://github.com/WalksWithASwagger/kriskrug-wp/issues/339)
**Evidence report:** [`docs/current-state/reports/publisher-batch-refresh-339-20260816.md`](../../../docs/current-state/reports/publisher-batch-refresh-339-20260816.md)
**Supersedes:** [`content/drafts/339-july-publisher-batch-checklist-2026-07-26.md`](../339-july-publisher-batch-checklist-2026-07-26.md) and the 2026-07-26 prep report.

Authenticated readback: `2026-08-28T22:40:34Z`. Aurora live and repo `main` both `1.6.9`. WordPress `7.0.4`.

## DONE vs STILL OPEN

| Item | Verdict | Why |
|---|---|---|
| Aurora 1.3.39 zip deploy | **DEAD / obsolete** | Live is 1.6.9. Do not upload that zip. OG/description work from that era needs a separate check against current 1.6.9 theme output. |
| #249 About YCDD sentence | **STILL OPEN** | `/about/` has 0 matches for `you can't drink data`. Opening paragraph still present. |
| #328 Most Benevolent wraps | **STILL OPEN** | Needles present once each on 2950 and 2665. Zero hrefs to post 3814. |
| #335 LOTR title/desc + footer pair | **STILL OPEN** | Public title is still `The Lord of the Rings Drinking Game \| Kris Krüg`. Footer still points at the AI companions post. |
| #336 AI second brain title/desc + wraps | **STILL OPEN** | Live title is `Build an AI Second Brain That Actually Works` (missing "for You"). Needles on 9774 and 12327 are unlinked. |
| #342 post 11171 href | **STILL OPEN** | Exact sentence still points at `https://kriskrug.notion.site/keynote-both-hands-full?source=copy_link`. |

Closed GitHub issues #249, #328, #335, #336, #342 were repo-side prep or measurement. They are not proof the live writes happened.

## Theme zip: strike this

The retired #339 contract asked KK to approve deploying `kk-aurora-seo-metadata-1.3.39-20260713.zip`. **Keep that action struck.** Production and repo `main` both run Aurora **1.6.9**. Uploading 1.3.39 would be a downgrade.

Standard descriptions and per-post search titles are theme-owned (`inc/seo-title.php`, `inc/seo-meta-rest.php`). Sampled 1.6.9 routes already emit one `<meta name="description">`. Remaining OG/title-format questions belong with current theme output, not with that zip.

## Payloads in this folder

| File | What it is |
|---|---|
| `apply-249-about-ycdd.md` | One new About sentence + YCDD link on page 1208 |
| `apply-328-most-benevolent.md` | Two copy-preserving wraps on posts 2950 and 2665 |
| `apply-335-lotr-seo-and-footer.md` | SEO overwrite on post 35 plus footer pair 35 <-> 58 |
| `apply-336-ai-second-brain.md` | SEO overwrite on post 8802 plus wraps on 9774 and 12327 |
| `apply-342-both-hands-full.md` | Href-only on post 11171 |
| `seo-meta-overwrite.json` | `--from-file` overwrite plan for posts 35 and 8802 |
| `manifest.json` | Machine-readable verdicts and identity guards |
| `authenticated-guard-refresh-20260828.json` | Authenticated raw/desired hashes for the two previously drifted objects; no body content or credentials |
| `live-evidence-compact.json` | Historical 2026-08-17 public REST + HTML head capture (no full HTML) |

## Shared apply rules (INCIDENT-2026-05-15)

1. Snapshot first. Authenticated `context=edit` JSON plus public HTML plus SHA-256 under `backup/<UTC>-july-publisher/`.
2. Match **ID + slug + status + modified** before every PATCH. Stop on drift.
3. Body writes: top-level `content` only. Meta writes: allowlisted keys only (`jetpack_seo_html_title`, `advanced_seo_description`).
4. FIND must match exactly once in `content.raw`. Abort on 0 or >1.
5. One write, then authenticated + cache-busted public readback, then the next target.
6. Rollback is re-POST of snapshotted `content.raw` / prior meta. Do not rely on Pagely revisions.
7. Latin1 DB: keep new copy ASCII or latin1. Non-latin1 in FIND strings from live HTML stay as NCR (`&#8217;`). Do not introduce em dashes.
8. Do not run the Notion connector for these patches.

## Apply order (after KK ticks + secrets + dry-run)

1. SEO meta: post **35**, then **8802**, from `seo-meta-overwrite.json` (overwrite; both fields are already non-empty).
2. Body: **#249** page 1208 -> **#328** 2950 then 2665 -> **#335** footers 35 then 58 -> **#336** 9774 then 12327 -> **#342** 11171.

## KK ticks still required

- [ ] Strike the Aurora 1.3.39 zip line on #339. Do not upload it.
- [ ] Approve overwriting post 35 SEO title and description with the exact strings in `seo-meta-overwrite.json`.
- [ ] Approve overwriting post 8802 SEO title and description (live values already differ).
- [ ] Approve the #249 About sentence.
- [ ] Approve the four copy-preserving wraps (#328 and #336).
- [ ] Approve the #335 footer pair.
- [ ] Approve the #342 href-only replacement.
- [ ] Acknowledge refreshed `modified` guards: page 1208 `2026-08-16T21:29:03`, post 11171 `2026-08-10T18:24:39`, post 12327 `2026-08-16T21:03:50`.
- [ ] Dry-run evidence reviewed. Snapshot dir created.

Out of scope: #331, #353, #340 bc-ai.net, GSC indexing quota, DNS/GA4, any live write in this PR.
