# Thin legacy posts — triage, do not sweep

#1025 allows three outcomes per URL. It forbids bulk delete and bulk Request Indexing.

| Outcome | When | What to file |
|---|---|---|
| Keep / improve | Still a real essay, talk, or record. Thin title or missing inbound only. | One-post draft in `content/drafts/` plus the indexing runbook |
| Merge + 301 | Duplicate or superseded by a clearer later URL | Named source slug, named target slug, then a Redirection rule after KK approval |
| noindex | No successor and no reason to keep it in the index | Singular robots on that post only. Not a category-wide flip. |

Do not start from the 892-row "Crawled - currently not indexed" example list. That mix is tag feeds, share copies, author pagination, and thin old posts. The crawl-hygiene snippet plus #331 already cover the machine classes.

The one named primary from the 2026-09-06 GSC note is already triaged in [`docs/current-state/reports/issue-996-unindexed-primary-triage-20260908.md`](../../../docs/current-state/reports/issue-996-unindexed-primary-triage-20260908.md):

`https://kriskrug.co/2024/01/31/exploring-the-intersection-of-photography-and-generative-ai/`

That URL stays a keep/improve candidate. It is not a delete target.
