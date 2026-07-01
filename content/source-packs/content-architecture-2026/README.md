# Content Architecture 2026 Source Pack

Systematic Trust + Offers migration for KrisKrug.co after the Aurora readability reset.

## Status

- Track: Track A page content
- Branch: `codex/content-architecture-trust-offers`
- Live theme dependency: Aurora `1.3.27`
- First wave: Services, Contact, Work, About, Speaking, Responsible AI Professional, Podcast EPK
- Second wave: Vancouver AI, AI for Creatives, AI Events, AI Ethics, AI Tools, AI for Journalists, AI Conversations, Indigenous AI
- Live write posture: snapshot-gated, body-only REST updates

## Purpose

This pack turns high-value legacy content pages into a small reusable Aurora content system. It keeps the site visual and expressive while removing page-specific CSS namespaces and restoring a predictable hierarchy.

## Files

- `page-inventory.md` - published page inventory and migration priority.
- `module-spec.md` - allowed content modules and authoring rules.
- `topic-hubs.md` - Wave 2 topic hub intent, order, and content rules.
- `wp-payloads/*.html` - body-only replacement payloads for first-wave pages.
- `wp-payloads/topic-hubs/*.html` - body-only replacement payloads for topic hub pages.
- `wp-payloads/page-map.json` - page IDs, slugs, URLs, and required readback markers.
- `wp-payloads/topic-hubs/page-map.json` - Wave 2 page IDs, slugs, URLs, and required readback markers.
- `deploy-checklist.md` - snapshot, REST write, readback, screenshot, and rollback gate.
- `deploy-checklist-topic-hubs.md` - Wave 2 snapshot, REST write, readback, screenshot, and rollback gate.

## First-Wave Targets

| Page | ID | URL | Role |
|---|---:|---|---|
| Services | 2666 | `/generative-ai-services/` | Offer |
| Contact | 2418 | `/contact/` | Utility / conversion |
| Work | 2672 | `/work/` | Portfolio / proof |
| About | 1208 | `/about/` | Trust |
| Speaking | 1887 | `/speaking/` | Offer / authority |
| Responsible AI Professional | 11914 | `/responsible-ai-professional/` | Offer / education |
| Podcast EPK | 3609 | `/podcast-guesting-page-epk/` | Media / booking |

## Second-Wave Targets

| Page | ID | URL | Role |
|---|---:|---|---|
| Vancouver AI | 12315 | `/vancouver-ai/` | Local ecosystem hub |
| AI for Creatives | 12316 | `/ai-for-creatives/` | Creative practice hub |
| AI Events | 12317 | `/ai-events/` | Event discovery hub |
| AI Ethics | 12318 | `/ai-ethics/` | Responsible AI hub |
| AI Tools | 12321 | `/ai-tools/` | Practical tools / glossary hub |
| AI for Journalists | 12320 | `/ai-for-journalists/` | Media and newsroom hub |
| AI Conversations | 12319 | `/ai-conversations/` | Thought leadership / podcast hub |
| Indigenous AI | 12322 | `/indigenous-ai/` | Careful Indigenous AI / sovereignty hub |

## Safety Notes

- Do not include a `title` field in REST updates.
- Snapshot each page immediately before writing.
- Verify ID, slug, status, title, raw content, excerpt, meta, and modified date before every write.
- Preserve unrelated performance artifacts in the worktree.
- Do not close issue #122 until the first-wave pages pass live verification and the remaining generic-page queue is documented.
