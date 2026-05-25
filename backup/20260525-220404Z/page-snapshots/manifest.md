# Events page snapshot - Aurora 1.3.4 polish

- Public URL: https://kriskrug.co/events/
- REST target: id `2250`, slug `events`, status `publish`, title `Events`
- Modified before update: `2026-05-24T17:08:30` GMT
- Public HTML sha256: `adbe3cae25ffb35c5a65d2dc774adc6c96f2295240648e012fce8e58a6c85888`
- REST JSON sha256: `5f82b3b6f7efe1cc513603757b2fe12eb4da1f28d656e8cd85c41848b5667785`
- Raw content H1 count before update: `1`
- Update applied: changed the Events content hero from `h1` to `h2`; generic page title remains the single public H1.
- Modified after update: `2026-05-25T22:05:07` GMT
- REST update readback sha256: `e5cceb7be605ddc694b7c62990e74f7bd405dcea8ee64ee79ed02add46b73bfe`
- Public regular after-update sha256: `e7eba481377f752ea5b29f9d1fc23f27de4e220ac7d1bc6f27b5aec165607654`
- Public cache-busted after-update sha256: `e7eba481377f752ea5b29f9d1fc23f27de4e220ac7d1bc6f27b5aec165607654`
- Public after-update H1 check: exactly one H1, `Events`; `#aurora-events-title` is an H2.

## Services redirect query-string fix

- Redirection rule ID `4` was snapshotted before update in `redirection.redirects-before-services-query-fix.json`.
- Rule target verified before update: `/services/` -> `/generative-ai-services/`.
- Update applied: changed `match_data.source.flag_query` from `exact` to `pass`.
- Readback saved in `redirection.services-update-readback.json`.
- Public after-update check: `/services/?aurora_qa=redirect-fix` returns `301` to `/generative-ai-services/?aurora_qa=redirect-fix`, then `200`.
