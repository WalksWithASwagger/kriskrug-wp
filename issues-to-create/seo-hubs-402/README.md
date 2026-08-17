# #402 SEO authority hubs: child issue drafts

**Parent:** [#402](https://github.com/WalksWithASwagger/kriskrug-wp/issues/402) (keep open; this packet does not close it)
**Research (merged):** [PR #670](https://github.com/WalksWithASwagger/kriskrug-wp/pull/670) → `content/drafts/2026-08-02-seo-authority-hubs/`
**Split proposal:** [`docs/current-state/reports/BACKLOG-GROOMING-DOSSIER-2026-08-15.md`](../../docs/current-state/reports/BACKLOG-GROOMING-DOSSIER-2026-08-15.md) section 3 (PR #769)

**Filed 2026-08-16** as GitHub issues #826–#834. Do not file duplicates. #402 stays open. Receipt: [`docs/current-state/reports/seo-hub-split-402-20260816.md`](../../docs/current-state/reports/seo-hub-split-402-20260816.md).

## Child count

**9 children.** The ten search terms in #402 collapse into 7 hub surfaces, plus one taxonomy prep pass and one writing task.

| File | Child | GitHub | Covers | `link-matrix.csv` data rows |
|---|---|---|---|---|
| [`01-taxonomy-repair.md`](01-taxonomy-repair.md) | 1 | [#826](https://github.com/WalksWithASwagger/kriskrug-wp/issues/826) | 5 miscategorized posts + dead `kriskrug.com/contact` on 2819 | 30 (repair) |
| [`02-wire-photography-hub.md`](02-wire-photography-hub.md) | 2 | [#827](https://github.com/WalksWithASwagger/kriskrug-wp/issues/827) | Wire `/photography/` (page 12013) for terms 4, 7, 10 | 11-14 |
| [`03-rewrite-negotiation-checklist.md`](03-rewrite-negotiation-checklist.md) | 3 | [#828](https://github.com/WalksWithASwagger/kriskrug-wp/issues/828) | Rewrite post 1210; then wire the checklist | 34-37 |
| [`04-ai-ethics-you-cant-drink-data.md`](04-ai-ethics-you-cant-drink-data.md) | 4 | [#829](https://github.com/WalksWithASwagger/kriskrug-wp/issues/829) | `/ai-ethics/` hub: You Can't Drink Data | 7-10 |
| [`05-ai-for-creatives-cyber-love-garden.md`](05-ai-for-creatives-cyber-love-garden.md) | 5 | [#830](https://github.com/WalksWithASwagger/kriskrug-wp/issues/830) | `/ai-for-creatives/` hub: Cyber Love Garden | 26-29 |
| [`06-ai-conversations-matt-mckenna.md`](06-ai-conversations-matt-mckenna.md) | 6 | [#831](https://github.com/WalksWithASwagger/kriskrug-wp/issues/831) | `/ai-conversations/` hub: Matt McKenna | 15-17 |
| [`07-events-meetup-routing.md`](07-events-meetup-routing.md) | 7 | [#832](https://github.com/WalksWithASwagger/kriskrug-wp/issues/832) | Meetup recaps → `/events/` | 18-25 |
| [`08-most-benevolent-outcomes.md`](08-most-benevolent-outcomes.md) | 8 | [#833](https://github.com/WalksWithASwagger/kriskrug-wp/issues/833) | Most Benevolent Outcomes cluster (terms 1 and 2) | 1-6 |
| [`09-brand-navigation-krug-ai.md`](09-brand-navigation-krug-ai.md) | 9 | [#834](https://github.com/WalksWithASwagger/kriskrug-wp/issues/834) | Brand navigation for `krug ai` | 31-33 |

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

## Land first: taxonomy prep (#826)

**Land [#826](https://github.com/WalksWithASwagger/kriskrug-wp/issues/826) first.** Five posts carry a `kk-collection-footer` derived from category. Recategorizing rewrites (or, if the footer is baked into `post_content`, requires this child to rewrite) the link surface every later child edits. Today a 2006 valet photoshoot is presented as Vancouver AI ecosystem content.

`hub-plan.md` listed category fixes as priority 4. The auto-footer coupling wins: child 1 is prep, not cleanup.

Children #827–#834 are already filed. Apply order:

1. Land #827 (photography hub) after #826. Highest-leverage structural fix.
2. Land #828 after #827. Same pages/posts (12013, 1222, 1056); #828 adds the checklist sentence after 1210 is rewritten.
3. After #826 is live, #829, #830, #831, #832, #833 are parallel **except** #830 must not PATCH post 2819 until #826's contact-link repair is on that post.
4. Land #834 last among the hub children. It shares post 12030 with #829 and post 11700 with #833.

### Shared-source serialization (do not run these pairs in parallel)

| Source | First writer | Second writer |
|---|---|---|
| Post 2819 | #826 (href repair) | #830 (Cyber Love Garden spoke) |
| Page 12013, posts 1222 and 1056 | #827 | #828 |
| Post 12030 | #829 | #834 |
| Post 11700 | #833 | #834 |

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

## Paste-ready epic block (KK only)

Children are filed. Do not post until KK reviews. Canonical copy also lives in [`docs/current-state/reports/seo-hub-split-402-20260816.md`](../../docs/current-state/reports/seo-hub-split-402-20260816.md).

```markdown
## Split into per-hub children, 2026-08-16

Research merged via PR #670: `content/drafts/2026-08-02-seo-authority-hubs/` (`hub-plan.md`; `link-matrix.csv`, 37 apply-ready rows). Live reconfirm 2026-08-16: none of the planned hub wirings have shipped. This parent stays open until the children ship. Schema guidance and AGENTS.md SEO guardrails stay here.

The 10 search terms collapse into 7 hub surfaces plus one taxonomy prep pass and one writing task.

| Child | Issue | Covers | Link rows |
|---|---|---|---|
| Taxonomy repair, 5 posts + 1 dead link | #826 | prep for everything | 1 repair |
| Wire `/photography/` (12013) | #827 | `modelmayhem.com`, `hardcore photoshoot`, `negotiation equipment` | 4 |
| Rewrite post 1210 into the real checklist | #828 | `negotiation equipment for photographers` | 4 |
| `/ai-ethics/` hub: You Can't Drink Data | #829 | `you cant drink data` | 4 |
| `/ai-for-creatives/` hub: Cyber Love Garden | #830 | `cyber love garden` | 4 |
| `/ai-conversations/` hub: Matt McKenna | #831 | `matt mckenna miami` | 3 |
| `/events/` routing from the meetup archive | #832 | `vancouver ai community meetup` | 8 |
| Most Benevolent Outcomes cluster | #833 | `most benevolent outcome`, `... prayer` | 6 |
| Brand navigation | #834 | `krug ai` | 3 |

All 37 rows assigned, no overlap. Land #826 first. After it lands, hub children are parallel except: #827→#828 (photography pages); #826→#830 on post 2819; #829→#834 on post 12030; #833→#834 on post 11700.

`hardcore photoshoot` deliberately gets no hub.
```
