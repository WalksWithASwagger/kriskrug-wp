# #402 SEO authority hubs: child issue drafts

**Parent:** [#402](https://github.com/WalksWithASwagger/kriskrug-wp/issues/402) (keep open; this packet does not close it)
**Research (merged):** [PR #670](https://github.com/WalksWithASwagger/kriskrug-wp/pull/670) → `content/drafts/2026-08-02-seo-authority-hubs/`
**Split proposal:** [`docs/current-state/reports/BACKLOG-GROOMING-DOSSIER-2026-08-15.md`](../../docs/current-state/reports/BACKLOG-GROOMING-DOSSIER-2026-08-15.md) section 3 (PR #769)

**Do not `gh issue create` from these files until KK says so.**

## Child count

**9 children.** The ten search terms in #402 collapse into 7 hub surfaces, plus one taxonomy prep pass and one writing task.

| File | Child | Covers | `link-matrix.csv` data rows |
|---|---|---|---|
| [`01-taxonomy-repair.md`](01-taxonomy-repair.md) | 1 | 5 miscategorized posts + dead `kriskrug.com/contact` on 2819 | 30 (repair) |
| [`02-wire-photography-hub.md`](02-wire-photography-hub.md) | 2 | Wire `/photography/` (page 12013) for terms 4, 7, 10 | 11-14 |
| [`03-rewrite-negotiation-checklist.md`](03-rewrite-negotiation-checklist.md) | 3 | Rewrite post 1210; then wire the checklist | 34-37 |
| [`04-ai-ethics-you-cant-drink-data.md`](04-ai-ethics-you-cant-drink-data.md) | 4 | `/ai-ethics/` hub: You Can't Drink Data | 7-10 |
| [`05-ai-for-creatives-cyber-love-garden.md`](05-ai-for-creatives-cyber-love-garden.md) | 5 | `/ai-for-creatives/` hub: Cyber Love Garden | 26-29 |
| [`06-ai-conversations-matt-mckenna.md`](06-ai-conversations-matt-mckenna.md) | 6 | `/ai-conversations/` hub: Matt McKenna | 15-17 |
| [`07-events-meetup-routing.md`](07-events-meetup-routing.md) | 7 | Meetup recaps → `/events/` | 18-25 |
| [`08-most-benevolent-outcomes.md`](08-most-benevolent-outcomes.md) | 8 | Most Benevolent Outcomes cluster (terms 1 and 2) | 1-6 |
| [`09-brand-navigation-krug-ai.md`](09-brand-navigation-krug-ai.md) | 9 | Brand navigation for `krug ai` | 31-33 |

Coverage: `1 + 4 + 4 + 4 + 4 + 3 + 8 + 6 + 3 = 37`. Every row in `link-matrix.csv` is assigned to exactly one child. No overlap. No orphans.

`hardcore photoshoot` (term 7) gets **no hub**. Its only deliverable is the category fix in child 1. Do not touch that post's title.

## Suggested labels (all children)

Apply on filing. Do **not** apply `agent:ready` or `swarm-ready` at create time; KK adds those after the live-write gate is explicit.

| Child | Labels |
|---|---|
| All nine | `content`, `seo`, `needs-human-review` |
| 1, 2, 3 | also `priority:high` |
| 4, 5, 6, 7, 8, 9 | also `priority:medium` |
| 3 only | also `enhancement` (it is the only writing task) |

Parent #402 already has `enhancement`, `help wanted`. Leave those on the parent. Do not copy `help wanted` onto the children.

## File first: taxonomy prep (child 1)

**File [`01-taxonomy-repair.md`](01-taxonomy-repair.md) first.** Five posts carry a `kk-collection-footer` derived from category. Recategorizing rewrites (or, if the footer is baked into `post_content`, requires this child to rewrite) the link surface every later child edits. Today a 2006 valet photoshoot is presented as Vancouver AI ecosystem content.

`hub-plan.md` listed category fixes as priority 4. The auto-footer coupling wins: child 1 is prep, not cleanup.

After 01 exists as a GitHub issue, file 02-09 in the same sitting and point `blocked by` at 01's new number.

### Then

1. File 02 (photography hub). Highest-leverage structural fix in the plan.
2. File 03 and set it blocked by 02. Same pages/posts (12013, 1222, 1056) in a chain; 03 adds the checklist sentence after 1210 is rewritten.
3. File 04, 05, 06, 07, 08. After 01 lands live, these are parallel **except** 05 must not PATCH post 2819 until 01's contact-link repair is on that post.
4. File 09 last among the hub children. It shares post 12030 with 04 and post 11700 with 08. Set 09 blocked by 04 **and** 08 so two agents cannot PATCH the same `post_content`.

### Shared-source serialization (do not run these pairs in parallel)

| Source | First writer | Second writer |
|---|---|---|
| Post 2819 | 01 (href repair) | 05 (Cyber Love Garden spoke) |
| Page 12013, posts 1222 and 1056 | 02 | 03 |
| Post 12030 | 04 | 09 |
| Post 11700 | 08 | 09 |

## Row ledger (`link-matrix.csv` data rows 1-37)

Data row 1 is the first row after the header (file line 2).

| Rows | Child | Source → target (short) |
|---|---|---|
| 1-6 | 08 | worldview, 11936, 11358, 11700 → 3814; 3814 → worldview; 3814 → `/ai-ethics/` |
| 7-10 | 04 | `/ai-ethics/`, 12030, 6144, 11882 → 11936 |
| 11-14 | 02 | `/photography/` → photo archive; `/photography/` → 1056; 1222 → 1056; 1056 → `/photography/` |
| 15-17 | 06 | `/ai-conversations/`, 2833, 2423 → 3183 |
| 18-25 | 07 | seven meetup posts + `/vancouver-ai/` → `/events/` |
| 26-29 | 05 | `/ai-for-creatives/`, 2819, 2661, 3567 → 2650 |
| 30 | 01 | 2819 → `/contact/` (repairs dead `.com` href) |
| 31-33 | 09 | 12653 → `/speaking/`; 12030 → `/about/`; 11700 → `/glossary/` |
| 34-37 | 03 | `/photography/`, 1222, 1056 → 1210; 1210 → `/photography/` |

## Shared safety (every child inherits this)

- Track A. Snapshot before any live PATCH. Slug and ID confirmation per [`INCIDENT-2026-05-15-overwritten-post.md`](../../docs/current-state/INCIDENT-2026-05-15-overwritten-post.md).
- Dry-run first. KK approval before `--execute`. Content-only payloads unless the child explicitly owns a rewrite (child 3 owns post 1210 body).
- Do not duplicate `kk-collection-footer`. Insert **before** that footer when the plan says "final paragraph".
- No em dashes. Preserve KK voice. No keyword stuffing.
- Do not run `scripts/seo-backfill/inject_links.py` in bulk. These inserts are surgical (exact anchor, exact block). The bulk injector's first-occurrence + footer path would fight the matrix.
- Do not close #402. Schema guidance and `AGENTS.md` SEO guardrails stay on the parent.
- Search Console was not available to PR #670. Ranking URL and intent claims are on-site inference. Re-check live by ID/slug before writing; skip a row if the link is already present.

## Paste-ready epic block (KK only, after the nine issues exist)

Do not post this until the children are filed and the new numbers can be filled in.

```markdown
## Split into per-hub children, 2026-08-16

Research merged via PR #670: `content/drafts/2026-08-02-seo-authority-hubs/` (`hub-plan.md`; `link-matrix.csv`, 37 apply-ready rows). Drafts live in `issues-to-create/seo-hubs-402/`. This parent stays open until the children ship.

The 10 search terms collapse into 7 hub surfaces plus one taxonomy prep pass and one writing task.

| Child | Covers | Link rows |
|---|---|---|
| Taxonomy repair, 5 posts + 1 dead link | prep for everything | 1 repair |
| Wire `/photography/` (12013) | `modelmayhem.com`, `hardcore photoshoot`, `negotiation equipment` | 4 |
| Rewrite post 1210 into the real checklist | `negotiation equipment for photographers` | 4 |
| `/ai-ethics/` hub: You Can't Drink Data | `you cant drink data` | 4 |
| `/ai-for-creatives/` hub: Cyber Love Garden | `cyber love garden` | 4 |
| `/ai-conversations/` hub: Matt McKenna | `matt mckenna miami` | 3 |
| `/events/` routing from the meetup archive | `vancouver ai community meetup` | 8 |
| Most Benevolent Outcomes cluster | `most benevolent outcome`, `... prayer` | 6 |
| Brand navigation | `krug ai` | 3 |

All 37 rows assigned, no overlap. File and land the taxonomy child first. After it lands, hub children are parallel except the shared-source pairs listed in `issues-to-create/seo-hubs-402/README.md`.

`hardcore photoshoot` deliberately gets no hub.
```
