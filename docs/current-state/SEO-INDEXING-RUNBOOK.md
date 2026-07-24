# SEO Indexing & Distribution Runbook

Owner issue: #426. A durable, slow-burn checklist for turning KrisKrug.co posts
(new and legacy) into indexable, internally-linked, query-targeted assets. Run
it in small batches over time, not as a one-shot sweep.

**This is process infrastructure, not a content-rewrite mandate.** No public
publishing, social posting, outreach, account, or plugin change happens from
this runbook without explicit KK approval (see the gate table).

## Batch size

**5 to 10 posts per wave.** Pick a batch by one theme (a hub topic, a legacy
category, or a set of surprising Search Console winners from #402). Never open
more than one batch at a time.

## Per-post checklist

Work each post through these. Everything in the "Agent-safe" column can be done
and verified without KK; everything in "KK-gated" waits for his approval.

| Step | Agent-safe (do + collect evidence) | KK-gated (draft only) |
|---|---|---|
| Title / meta | Draft an improved `<title>` + meta description in KK voice (no em dashes, no AI tropes). Cross-check gaps with `make seo-audit` (read-only inventory). | Publishing the change live |
| Answer-first intro | Draft a 1–2 sentence answer-first opening for the target query | Publishing the rewrite |
| Internal links | List 3–5 relevant internal links (other posts + a hub) with anchor text | Editing live post body |
| Hub links | Identify the authority hub the post belongs to (AI community, ethics, photography, personal voice) | Building/renaming a hub page |
| Schema | Run `make seo-publisher-smoke` and confirm Article-family + required fields per [SEO-PUBLISHER-SCHEMA-2026-07-19.md](SEO-PUBLISHER-SCHEMA-2026-07-19.md) (#425) | Changing the schema type live |
| Feed / sitemap | Confirm the post appears in `/feed/` and `wp-sitemap-posts-post-1.xml` | n/a |
| New content path | For Notion-sourced posts: run publisher dry-run (`python kk_notion_to_wp.py --dry-run …` per [scripts/notion-to-wp/README.md](../../scripts/notion-to-wp/README.md)); review `content/drafts/<slug>/` package | Live publish or `--update` |
| Search Console | Draft the exact URL(s) to submit for indexing | Submitting in Search Console (KK account) |
| Cache readback | Verify public HTML with cache-busted curl (`?cachebust=<ts>`) after any live change | Pagely PressCACHE purge after REST/theme edits |
| External citation | Draft a backlink/citation ask (who, why, one line) | Sending any outreach |

## Verification commands / evidence

Collect this evidence per batch and paste it into the batch issue:

```bash
make seo-publisher-smoke                          # sitemap/feed/schema health (#425)
make seo-audit                                    # read-only Jetpack meta inventory
curl -s "https://kriskrug.co/feed/" | grep -c "<item>"
curl -s "https://kriskrug.co/<post-url>?cachebust=$(date +%s)" | grep -oE '"@type":"[^"]+"'
```

Never claim a live change happened; agents only draft and verify public
read-only state. Live edits go through the wp-live-edit snapshot-first flow with
KK approval. After KK publishes or patches via REST, Pagely cache does not
auto-purge — KK must purge before logged-out verification counts.

## Batch issue-body template

Copy this into a new issue when starting a wave (or add to
`issues-to-create/`):

```markdown
## SEO indexing batch: <theme> (wave N)

Runbook: docs/current-state/SEO-INDEXING-RUNBOOK.md
Batch (5–10 posts):
- [ ] <post url 1>
- [ ] <post url 2>
...

For each post, produce (agent-safe, draft only):
- Draft title + meta (KK voice, no em dashes)
- Answer-first intro draft
- 3–5 internal links + hub link
- Schema/feed/sitemap evidence (`make seo-publisher-smoke` output)
- Search Console URLs to submit (KK submits)
- One external citation ask (KK sends)

KK-gated before anything ships: publish edits, hub changes, Search Console
submission, Pagely purge, outreach.
```

## Related SEO work

- #425 — publisher/news sitemap + article-schema rule (`make seo-publisher-smoke`).
- #402 — surprising Search Console winners → authority hubs (source of batch themes).
- #274 / #331 / #347 — taxonomy sitemap, canonical, and metadata handoffs (do not overlap; this runbook does not touch taxonomy).
- #383 — queued SEO human-gate decisions.
- Existing context: [SEO-PUBLISHER-SCHEMA-2026-07-19.md](SEO-PUBLISHER-SCHEMA-2026-07-19.md), [SEO_AUDIT.md](SEO_AUDIT.md), [SEO-OVERHAUL-2026-06-14.md](SEO-OVERHAUL-2026-06-14.md).
