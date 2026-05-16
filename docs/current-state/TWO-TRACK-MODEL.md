# Two-track operating model

**Decided 2026-05-16 with KK.** Captures how the kriskrug.co work splits so each stream can move at its own pace without blocking the other.

---

## The problem this solves

Content/SEO improvements (publish a post, fix an H1, add a link, run a categorization sweep) move in days. A theme migration moves in weeks-to-months because it touches Site Editor templates, plugin compatibility, all post types, mobile, and a cutover window. Bundling them into one workstream means either:

- the content work waits for the redesign (bad — SEO degrades while you wait), or
- the redesign gets rushed (bad — that's how the 2026-05-15 incident happened)

So we split them.

---

## Track A — Content + SEO

| | |
|---|---|
| **Branch** | `main` |
| **Cadence** | Weekly (publishing) + ad-hoc enrichment |
| **Owner** | Publisher-mode Claude sessions |
| **Touches** | Posts, pages, media, taxonomies, Jetpack settings, Code Snippets (PHP/CSS), schema JSON-LD, Redirection rules, alt text |
| **Never touches** | Theme files (`theme/kk-aurora/` or Catch Responsive), FSE templates, theme.json |
| **Lives in** | `content/drafts/`, `fixes/`, `scripts/notion-to-wp/`, `docs/current-state/` |

### What Track A does

- Notion → kriskrug.co publishing via [`scripts/notion-to-wp/kk_notion_to_wp.py`](../../scripts/notion-to-wp/kk_notion_to_wp.py) — 1–2 posts/week
- Post-publish enrichment passes (slides, photos, embeds, pull-quotes, auto-links via [`text_polish.py`](../../scripts/notion-to-wp/text_polish.py))
- Categorization sweeps + link-graph building
- Schema maintenance via [`fixes/schema-snippets-deployed.php`](../../fixes/schema-snippets-deployed.php) (Code Snippet id 5)
- GSC + Lighthouse monitoring, sitemap health
- Site-wide content cleanup driven by [`SITE-AUDIT-2026-05-16.md`](SITE-AUDIT-2026-05-16.md) (homepage hero rewrite, About H1 demotion, popup trigger change, /work/ redirect, etc.)
- Image alt-text batches (existing FIX_QUEUE P1.4)

### Track A's success measures

- Posts published per month (target: 4–8)
- GSC impressions trending up 2–4 weeks after categorization + recency improvements
- Punch-list items from SITE-AUDIT closed
- No incidents that require restoring from backup

---

## Track B — Aurora v2 redesign

| | |
|---|---|
| **Branch** | `aurora/v2` (new — rebased onto current `main`) |
| **Cadence** | Paced sprints, not weekly |
| **Owner** | Architect-mode Claude sessions (separate context) |
| **Touches** | `theme/kk-aurora/` (theme.json, templates, patterns, assets), FSE Site Editor on staging, theme settings on production at cutover |
| **Never touches** | Post content, post media, taxonomies, schema snippets, the connector |
| **Lives in** | `theme/`, `demo/`, [`docs/current-state/AURORA-MIGRATION-PLAN.md`](AURORA-MIGRATION-PLAN.md) |

### What Track B does

- **Rebase first** — the old branch (`origin/claude/setup-wordpress-rebuild-KVLxh`, last touched 2026-01-18) deletes Track A's work. Track B's first step is creating `aurora/v2` from current `main` and cherry-picking `theme/` + `demo/` from the old branch.
- **Stand up staging** — install on Cloudways dev (`24.144.80.107`) or Local by Flywheel
- **Iterate** via WP Site Editor on staging; push tweaks back to the branch
- **Smoke-test** all post types (long-form, image-heavy, embed-heavy — Make Culture and Your Taste are the stress tests)
- **Cutover** during a low-traffic window (Sunday morning Pacific) with rollback ready (Catch Responsive stays installed-but-inactive)
- **Monitor 24h** post-cutover

### Track B's success measures

- Aurora renders all post types correctly on staging before cutover
- Core Web Vitals improve post-cutover (LCP, INP, CLS)
- No content lost in migration
- KK signs off on staging before production push

---

## What both tracks share (read, neither owns alone)

- `backup/` — both tracks read manifests; Track B owns making a fresh backup before cutover
- `docs/current-state/` — both tracks contribute, both tracks read; doc names should make ownership obvious (`AURORA-*` = Track B, `SEO-*` / `CONTENT-*` / `TRAFFIC-*` = Track A)
- `scripts/notion-to-wp/text_polish.py` `LINK_MAP` — Track A authors entries as new pillar posts publish; Track B inherits the same map (theme-agnostic)
- `fixes/schema-snippets-deployed.php` — Track A maintains; Track B confirms it still renders post-theme-swap
- The 2026-05-15 incident postmortem — both tracks live with the same safety rules (slug-based idempotency, backup before destructive ops, no PATCH without verified target)

---

## How to know which track you're in

Open the session, ask:

- **Am I editing a post / page / media / category / popup setting / schema / redirect?** → Track A
- **Am I editing theme files / FSE templates / theme.json / patterns?** → Track B

If you're doing both in the same session, you've probably scope-crept; finish one, commit, then start the other in a fresh session.

---

## What this doesn't (yet) solve

- **Sequencing big calls between tracks.** Example: if Track A's reader audit suggests a homepage hero rewrite, should that rewrite happen on the current theme (Track A) or wait for Aurora (Track B)? Default: ship on current theme if the fix is ≤ a few hours; defer to Aurora if it's a layout-level decision. KK has final call on close ones.
- **Coordination cadence.** No standing weekly sync between tracks because there's currently one human (KK) reviewing both. Revisit if/when that changes.
- **Branch hygiene** for Track B. Once `aurora/v2` exists, keeping it in sync with `main` (via rebase, not merge) is the architect-session's responsibility. Stale-branch risk is real — the 4-month gap on the current Aurora branch is exactly what this section is trying to prevent recurring.

---

## Living doc

Edit this file whenever the split needs refinement. Don't let it drift while the actual practice evolves elsewhere.
