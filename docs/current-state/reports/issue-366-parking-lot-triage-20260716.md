# #366 Parking lot triage — after Monday primary queue

**Captured:** `2026-07-16T00:43:21Z`  
**Rule:** do not start until M1–M5 (#361–#365) are done **or** KK explicitly defers them. Pick **one**. Separate PR. No mixing with #339 / Aurora deploy evidence.

## Recommended pick order (if KK asks “what next?”)

| Rank | Issue | Why | Lane |
|---:|---|---|---|
| 1 | #331 | High SEO leverage; sitemap/indexability; keep out of #339 | Track A ops / snippets — needs human policy |
| 2 | #353 | Remaining body-H1 routes; one target at a time | Track A content |
| 3 | #290 | About/bio module plans exist; body write still gated | Track A content |
| 4 | #274 | GSC submit/monitor — human Search Console only | Human |
| 5 | #125 / #86 / #127 | Perf + mobile + a11y QA after Jetpack era | Track B QA |
| 6 | #318 | Repo bloat — KK-approved cleanup only | Ops |

## Explicitly not starting now

Primary Monday queue still has live gates on #362–#365. This triage only records preference; no parking-lot implementation PR in this orchestra commit.
