# #364 Hub-link wraps — agent-ready / write-gated

**Captured:** `2026-07-16T00:43:21Z`  
**Primary packets:** #284 / #278  
**Public recheck:** `issue-284-public-recheck-20260716.md` — **0/11 href drift**, **0/11 modified drift**

## Packet

- Markdown: `fixes/issue-284-topic-hub-links-handoff-2026-07-12.md`
- JSON: `fixes/issue-284-topic-hub-links-handoff-2026-07-12.json`
- Unit tests: `scripts/tests/test_issue_284_topic_hub_links_handoff.py` (green)

## Review-ready wraps only (await KK `patch_id` list)

Ordered source writes (ordinary batch — AI Ethics / AI Tools wrappers):

| Order | Source ID | Slug | `patch_id`s | `modified` guard |
|---:|---:|---|---|---|
| 1 | 12035 | `ai-wont-fix-your-broken-permit-process` | `12035-ai-tools` | `2026-07-01T16:24:28` |
| 2 | 12257 | `why-we-built-the-responsible-ai-professional-certification` | `12257-ai-ethics` | `2026-06-28T20:25:58` |
| 3 | 2781 | `audio-deep-fakes-ai-chatbots-and-new-web-development-tools` | `2781-ai-tools` | `2026-06-28T20:39:27` |
| 4 | 12030 | `canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one` | `12030-ai-ethics`, `12030-ai-tools` | `2026-06-28T14:14:24` |

KK must approve **these** patch IDs (or a strict subset) before any REST `content` write.

## Indigenous AI queue — do not touch without per-row approval

| Source ID | Slug | Status / proposed patch |
|---:|---|---|
| 7450 | indigenomics-now-2024-… | `human-review-required-existing-link-no-op` |
| 12030 | canada-doesnt-need-… | `12030-indigenous-ai` proposed-not-live |
| 12035 | ai-wont-fix-… | `12035-indigenous-ai` proposed-not-live |
| 12257 | why-we-built-… | `12257-indigenous-ai` proposed-not-live |
| 11905 | sovereign-ai-for-whom | `11905-indigenous-ai` proposed-not-live |

## Post-approval dry-run plan (no execute without secrets + ticks)

1. Re-run public href/`modified` recheck; abort on any drift.
2. Snapshot each approved source under `backup/<timestamp>-hub-links/<id>/` (`content.raw`, edit-context JSON, SHA-256).
3. Body-only REST patch one source at a time in packet order.
4. Public smoke: each source URL contains the expected hub href exactly once (per expected-after counts).
5. Leave Indigenous rows untouched unless separately approved.

## Blockers now

- No KK approval list attached to #364 / #284.
- No Cloud WP credentials for write or authenticated dry-run paths that hard-exit without `.env`.
