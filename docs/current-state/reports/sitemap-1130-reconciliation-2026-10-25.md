# Sitemap reconciliation for #1130 / #331 — October 25, 2026

**Recommendation: narrow the parent to evidence/closure follow-through.** Its
blanket taxonomy-bloat implementation was already deployed September 3 as
Snippet 26, using `fixes/issue-331-archive-sitemap-policy-v2.php`. Do not implement
the July checklist again or create a new indexability decision from stale wording.

Read-only checks refreshed at 5:22 p.m. PDT (`2026-10-26T00:22:50Z`): `/sitemap.xml` returns 301 to `/wp-sitemap.xml`;
the index is 200, `application/xml`. Its two children return 200 with 986 post
entries and 46 page entries. These are 1,032 sitemap entries, not Google-indexed
pages. Each child's entries are distinct within that file.

| Original acceptance item | October 25 disposition |
|---|---|
| Review query-to-page evidence before policy changes | No new policy change proposed. Historical review/approval belongs to the September deployment receipt; current GSC traffic evidence was not accessed. |
| Preserve post/page membership | Both providers remain present; counts reflect later publishing. This bounded read is not a July-to-today per-URL deletion audit. |
| Exclude/noindex author archives | Sitemap exclusion confirmed; sampled `/author/kk/` is 200, noindex,follow. |
| Exclude/noindex tag archives | Sitemap exclusion confirmed; sampled `/tag/sxsw-sxswi/` is 200, noindex,follow. |
| Retained category landing-page metadata and sitemap membership | September's approved v2 policy retains no indexable category exceptions. This conditional item does not require adding categories back. |
| Exclude/noindex thin categories | Sampled `/category/ai-ethics-philosophy/` is 200, noindex,follow; category provider absent. |
| Permanent sitemap handoff | Confirmed 301 to canonical core index. |
| Before/after receipt and retained inventory | Existing September 3 and September 21 receipts document the transition. Today's result updates public delivery, not Google indexing or every URL's history. |

Exactly three archive URLs were inspected, all from the maintained
`scripts/sitemap_followthrough.py` sample list. Each has one title and one H1,
no canonical and `max-image-preview:large, noindex, follow`. Under the deployed
policy they remain browseable archives, not search landing pages.

Evidence: [public readback](sitemap-1130-readback-2026-10-25.json); repository
`docs/current-state/reports/DEPLOY-767-331-2026-09-03.md` and
`docs/current-state/reports/issue-274-sitemap-followthrough-20260921.md`.
The script `sitemap-readback.py` records exact read-only GET targets.

Remaining owner work: accept the reconciled checklist and decide whether fresh
aggregate GSC coverage/traffic evidence is needed before closing #331. No claim
about current Google indexing is possible from XML alone. No settings, robots,
redirects, archive content, public issue comments or issue state changed.

## Exact request scope

GET `https://kriskrug.co/sitemap.xml` without following its redirect; GET
`https://kriskrug.co/wp-sitemap.xml`; follow its two discovered child URLs; GET
the three archive URLs listed in the JSON receipt. All requests were read-only.
Source helpers: `scripts/sitemap_followthrough.py` (`fetch`, `parse_locs`).
Source policy: `fixes/issue-331-archive-sitemap-policy-v2.php`, deployed in
[the September 3 receipt](DEPLOY-767-331-2026-09-03.md). The
[September 21 follow-through](issue-274-sitemap-followthrough-20260921.md)
already demonstrated the same two-provider policy.

This completes the bounded #1130 reconciliation. #331 remains open for its
owner's evidence/closure decision; no stop labels or indexability settings
were changed. No current aggregate GSC evidence was retrieved. The July
requirement for a full retained-URL crawl and GSC follow-up is not claimed
complete from this seven-URL public check. The original post/page-membership
acceptance cannot be proved by counts alone.
