# #994 proposal refresh — retain the pending #339 Second Brain packet

**Status:** PREP ONLY. Confirmation of the existing package. No live WordPress write.
**Issue:** [#994](https://github.com/WalksWithASwagger/kriskrug-wp/issues/994)
**Diagnosis:** [`docs/current-state/reports/issue-994-second-brain-diagnosis-20260920.md`](../../../docs/current-state/reports/issue-994-second-brain-diagnosis-20260920.md)
**Existing apply owner:** [`content/drafts/339-july-publisher-batch-2026-08-16/apply-336-ai-second-brain.md`](../339-july-publisher-batch-2026-08-16/apply-336-ai-second-brain.md)
**Last live-HTML readback:** 2026-09-08 (PR #1000). This file does not re-fetch.

This is the issue-specific proposal #994 asked for if a field-level decision is needed. The decision is **retain**. Named title, description, body, and link fields stay exactly as #336 / #339 already approved. This file must not be used as a second overwrite packet.

Do not edit the #339 folder from a #994 session. Do not PATCH 8802 / 9774 / 12327 from this file.

---

## Verdict

**Retain.** Zero named-field revisions.

| Choice | This refresh |
|---|---|
| Retain pending #339 package | **Selected** |
| Revise named fields | Not selected — no query-level GSC rows to justify new copy |
| No edit | Not selected — last-live title still drops "for You"; both source needles still unlinked as of 2026-09-08 |

The Sep 6 page drop (1,146 → 602 impressions, 14 → 3 clicks; sitewide clicks 172 → 168) happened while the packet was still unapplied. The packet is not the cause. Absence of a later apply receipt is why the same payload is still the recommendation.

---

## Exact before / after vs the existing package

Last-live values are the 2026-09-08 public HTML / public REST snapshot. Approved values are copied from `seo-meta-overwrite.json` and `apply-336-ai-second-brain.md`. **#994 after = #339 after.**

### A. SEO fields (post 8802 only)

Do not change the public post title, excerpt, slug, date, taxonomies, or body from this lane.

| Field | Last live (2026-09-08) | #339 approved | This refresh |
|---|---|---|---|
| `jetpack_seo_html_title` / `<title>` | `Build an AI Second Brain That Actually Works` (44) | `Build an AI Second Brain That Actually Works for You` (52) | **same as #339** |
| `advanced_seo_description` / standard description | `Most digital systems are designed for neurotypical productivity zombies. What if you built one optimized for your actual thought patterns instead?` (146) | `Build an AI second brain that works with your thought patterns, captures creative chaos, and turns scattered notes and voice memos into finished work.` (150) | **same as #339** |
| og/twitter description | follows the zombies excerpt | will follow the approved description | **same as #339** |
| H1 / post title | `How to Build an AI Second Brain That Actually Works for You` | leave | leave |
| URL / slug | `/2025/04/01/how-to-build-an-ai-second-brain-that-actually-works-for-you/` | leave | leave |

Why these strings stay:

- The title restores the article's own promise already in the H1 ("for You") without rewriting the post title.
- The description names thought patterns, creative chaos, notes, voice memos, and finished work — claims the body already makes.
- Both stay inside normal SERP truncation. No em dashes. No new factual claims.
- A new title or description without query rows would be a competing packet, which #994 forbids.

Overwrite mode is required. Both keys were already non-empty on 2026-08-16 and 2026-09-08. Additive `make seo-backfill` will skip 8802.

### B. Inbound wraps (9774 and 12327 only)

Target href: `https://kriskrug.co/2025/04/01/how-to-build-an-ai-second-brain-that-actually-works-for-you/`

| Source | Last live (2026-09-08) | #339 FIND → REPLACE | This refresh |
|---|---|---|---|
| 9774 `what-journalists-need-to-know-about-ai-right-now` | needle `AI as a second brain` ×1; target hrefs 0 | wrap those exact words | **same as #339** |
| 12327 `storyhive-haus-of-owl-jordan-dack` | needle `knowledge bases and named assistants` ×1; target hrefs 0 | wrap those exact words | **same as #339** |

Replacement HTML, unchanged:

```html
<a href="https://kriskrug.co/2025/04/01/how-to-build-an-ai-second-brain-that-actually-works-for-you/">AI as a second brain</a>
```

```html
<a href="https://kriskrug.co/2025/04/01/how-to-build-an-ai-second-brain-that-actually-works-for-you/">knowledge bases and named assistants</a>
```

Wrap existing words only. Do not edit the em dash after the 9774 phrase. FIND must match exactly once. Abort on 0 or >1.

No third source. #1030 later drafted extra inbounds from 12744 / 12263 and a 11878 retitle. Those stay on #1030.

---

## Publisher preconditions (for #339, not this PR)

1. Snapshot 8802 (meta + content), 9774, and 12327 before any write.
2. Confirm ID + slug + `publish` + then-current `modified` on each. Stop on drift.
3. **Refresh 12327 first.** Last live `modified` was `2026-09-07T13:07:06`. The packet guard is still `2026-08-16T21:03:50` with raw SHA-256 `045c697906260becae376d39fcf0987911ac9c94e5d3b25def8a4f1b4a69981d`. Recut the hash pair immediately before dry-run. The replacement HTML does not change.
4. Meta-only overwrite on 8802 from `seo-meta-overwrite.json`. Read back both keys.
5. Content-only wraps on 9774 then 12327. Top-level `content` only.
6. Public readback: approved title/description on 8802; each source has exactly one href to 8802; 8802 still 200 and self-canonical.
7. Rollback: restore prior meta from the overwrite `old` map, then re-POST each snapshotted `content.raw`.

KK ticks and dry-run proof still live on #339. This file does not add ticks.

---

## What this file is not

- Not a live apply runbook to execute from #994.
- Not a silent edit of `apply-336-ai-second-brain.md`, `manifest.json`, or the #336 fixtures.
- Not a title/description rewrite.
- Not an indexing request, cache purge, or Validate Fix.
- Not a promise that rank or CTR will recover.

---

## Measurement

Use the protocol in the 2026-09-20 diagnosis §7. Clock starts only after an approved public readback of the #339 fields. Success is a defensible before/after, not a promised rank increase.
