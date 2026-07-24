# Publisher / News Discovery + Article Schema Rules — 2026-07-19

Owner issue: #425. Read-only audit + the rule going forward.

**2026-07-24 live:** Code Snippet **5** `KK Schema` emits `BlogPosting` by
default (`NewsArticle` via `_kk_schema_type` or tag `news-article`). Snippet
**13** `KK News Sitemap` serves `/news-sitemap.xml` (48h NewsArticle window;
empty urlset is valid). Sources: `fixes/schema-snippets-deployed.php`,
`fixes/kk-news-sitemap-snippet.php`. Snapshot before deploy:
`/private/tmp/kriskrug-code-snippets-before-425-20260724T222705Z.json`.

## Audit (2026-07-19, public read-only)

| Surface | State |
|---|---|
| Sitemap | WordPress core `wp-sitemap.xml` only: posts, pages, category, tag, users. Healthy (200). |
| News sitemap | **Live** at `/news-sitemap.xml` (snippet 13). Empty when no tagged NewsArticle posts in 48h. |
| Feed | `/feed/` healthy (200, valid RSS). |
| Post schema | Default **`BlogPosting`** (snippet 5 / `kk_schema_post_type`) plus `Person`, `Organization`/`WebSite`, `BreadcrumbList`, `ImageObject`. |
| Required fields | Present on sampled posts: `headline`, `datePublished`, `dateModified`, `author` (@id `#person`), `publisher` (@id `#person`), `image`, `mainEntityOfPage`. |

Takeaway: the plumbing is solid (canonical author/publisher identity, dates,
image), but every post is a generic `Article`. There is no publisher/news
discovery surface for timely posts.

## Schema-type rule (going forward)

Encode this in the schema snippet when the change is deployed. Decide by post
character, not blindly by post type:

- **`BlogPosting`** — evergreen essays, field notes, opinion, how-to. This is
  the default for most KrisKrug.co writing. It is the honest type for durable
  personal writing and keeps the existing author/publisher identity graph.
- **`NewsArticle`** — timely, dated, event-or-announcement posts (festival
  recaps, launches, "this happened this week"). Only these are news-sitemap
  eligible. Do not blanket-apply `NewsArticle`; Google penalizes non-news posts
  in a news sitemap.
- **`Article`** — fallback only when a post fits neither cleanly.

Keep the existing required fields on every type (they already validate). Add a
`section` / `articleSection` from the primary category when the type is
`NewsArticle` or `BlogPosting`.

## News sitemap recommendation

WordPress core does not emit a Google-News sitemap. Options, in order of
preference:

1. **Custom snippet** (fits the existing Code Snippets pattern): emit
   `<url>` entries with `news:news` for `NewsArticle`-classified posts from the
   last 48 hours only, at `/news-sitemap.xml`. Lowest plugin footprint.
2. **Yoast News SEO** add-on: turnkey, but adds a paid plugin dependency.

Either is a **live change** and therefore KK-gated. Ship behind the same
snapshot-first flow as other live SEO snippets; do not auto-deploy.

## Regression check

`scripts/seo_publisher_smoke.py` (read-only) verifies sitemap + feed health and
that recent posts still carry an Article-family node with all required fields.
The missing news sitemap is reported as a NOTE, not a failure, so the check
stays green until the news sitemap is deliberately shipped (flip it to required
in the same PR).

```
python3 scripts/seo_publisher_smoke.py            # live
python3 scripts/seo_publisher_smoke.py --base URL --posts 5
make seo-publisher-smoke
```

## Boundary vs existing SEO issues

This issue owns publisher/news discovery + article schema *type*. It does not
touch taxonomy sitemap bloat, canonical rules, or per-post metadata handoffs
owned by the existing SEO issues (#274 / #331 / #347). The schema snippet edit,
when made, must not add taxonomy entries to any sitemap.
