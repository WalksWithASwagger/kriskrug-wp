# Monthly measurement readout: November 2026 (baseline)

Filled from [`templates/monthly-measurement-readout.md`](../templates/monthly-measurement-readout.md). This is the baseline readout, taken mid-month so the December 1 readout has something to compare against. Owner issue: #1279. Read-only: nothing was written to WordPress, Beehiiv or Search Console.

## Readout record

| Field | Value |
|---|---|
| Readout month (YYYY-MM) | 2026-11 (baseline, partial month) |
| Filled on (YYYY-MM-DD) | 2026-11-12 |
| Window covered | Posts and KRÜG: 2026-11-01 to 2026-11-12. Search Console: its last 28 days, 2026-10-14 to 2026-11-10. |
| Filled by | Agent session, read-only |
| Kris approved public numbers for this readout? (yes/no, which rows) | Yes, in chat on 2026-11-12: Search Console totals and top queries, the KRÜG subscriber count, and lab performance scores |

## Rows

| Row | Result | Source | Not measured because |
|---|---|---|---|
| Inquiries by Contact subject (counts only, from Kris) | not measured | Kris's own count | Kris counts these himself; his first monthly count is due December 1 (#1277) |
| KRÜG sends this month (dates) | None. KRÜG has never sent an issue; the first monthly letter is due by December 17 (#1278) | Beehiiv KRÜG publication, read-only | |
| KRÜG subscriber change (direction only unless Kris approves numbers) | 20 active subscribers. +2 since the signup measurement went live on 2026-10-25 (both on 2026-10-29); flat from November 1 to 12 | Beehiiv subscriber growth, read-only | |
| Search Console clicks, last 28 days | 199 (CTR 2.5%, average position 8.7) | Search Console performance report, domain property, signed-in browser | |
| Search Console impressions, last 28 days | 7.97K | Same | |
| Search Console top 10 queries, last 28 days | See the table below | Same | |
| Field Core Web Vitals for `/` (CrUX or PageSpeed field data) | not measured | PageSpeed Insights, mobile | Google reports no real-user (CrUX) data for the site yet. Lab scores for `/` on 2026-11-12: 87 mobile, 98 desktop |
| Field Core Web Vitals for `/speaking/` | not measured | PageSpeed Insights | No real-user data for the origin, so none per page; the anonymous PageSpeed API quota was also exhausted that day |
| Field Core Web Vitals for one recent post (URL in Source) | not measured | PageSpeed Insights, `/2026/11/09/who-gets-a-say-canada-ai-future-canada-now/` | Same reason |
| Published post count this month | 4 (November 1 to 12). October had 4 | Public REST, `X-WP-Total` | |
| Scheduled post count | 0 | Authenticated read-only queue count (`wp_queue_counts()`) | |

### Top 10 Search Console queries (2026-10-14 to 2026-11-10)

| Query | Clicks | Impressions |
|---|---:|---:|
| kris krug | 28 | 110 |
| kris krüg | 9 | 36 |
| kris krug vancouver | 6 | 16 |
| data center protest signs | 1 | 45 |
| augie ai | 1 | 40 |
| most benevolent outcome | 1 | 22 |
| claude paint | 1 | 19 |
| you cant drink data | 1 | 18 |
| most benevolent outcome prayer | 1 | 15 |
| asa mathat | 1 | 15 |

326 queries in total for the window.

## Notes

- Anything Kris decided to keep private: nothing for this readout.
- Rows that changed source or method since last month: none (first readout). Search Console lags about two days, so its window ends 2026-11-10.
- Two baseline observations for the roadmap: branded searches ("kris krug" and "kris krüg") bring most clicks; nothing is scheduled to publish, so the "never zero scheduled" target in theme 3 is not met yet.
- The next readout is due December 1, 2026; a one-time scheduled task (`kriskrug-monthly-readout-december`) prepares it locally for Kris's review.
