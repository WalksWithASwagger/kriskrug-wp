# Topic Hubs Wave - 2026-07-01

Wave 2 turns the eight AI topic pages into readable navigation hubs. The goal is not to make long essays; each page should quickly orient a reader, expose the strongest related material, and route high-intent visitors toward Services, Speaking, Work, EPK, or Contact.

## Targets

| Page | ID | Slug | Role |
|---|---:|---|---|
| Vancouver AI | 12315 | `vancouver-ai` | Local ecosystem hub |
| AI for Creatives | 12316 | `ai-for-creatives` | Creative practice hub |
| AI Events | 12317 | `ai-events` | Event discovery hub |
| AI Ethics | 12318 | `ai-ethics` | Responsible AI hub |
| AI Conversations | 12319 | `ai-conversations` | Thought leadership / podcast hub |
| AI for Journalists | 12320 | `ai-for-journalists` | Media and newsroom hub |
| AI Tools | 12321 | `ai-tools` | Practical tools / glossary hub |
| Indigenous AI | 12322 | `indigenous-ai` | Careful Indigenous AI / sovereignty hub |

## Authoring Rules

- Body-only payloads. Do not send `title` in REST updates.
- Preserve public URLs and WordPress titles.
- Use one body `aurora-display-heading` per page, and no body `<h1>`.
- Use only Aurora-owned content primitives from `module-spec.md`.
- Retire old `kkp-*` hub classes in updated raw content.
- Reuse current public site or owned-project assets. Do not upload new media in this wave.
- Keep Indigenous AI careful and evidence-led. Avoid speaking on behalf of Indigenous communities or claiming ownership of Indigenous-led work.

## Batch Order

1. Vancouver AI
2. AI for Creatives
3. AI Events
4. AI Ethics
5. AI Tools
6. AI for Journalists
7. AI Conversations
8. Indigenous AI
