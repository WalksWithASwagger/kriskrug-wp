# `fixes/` index

65 files live here and they are two very different kinds of thing mixed into one
directory:

- **Snippet PHP sources** (14 `.php`). Some are the source of truth for PHP that
  is running in production via the Code Snippets plugin; others are inactive,
  superseded, or drafts. Editing any of them is prod-adjacent work until its
  current slot/provider state is proved.
- **Supporting files** (51 non-PHP files). These include three served-root files,
  this index, and 47 archival handoff/reference artifacts. Nothing in the archival
  group runs in production.

Both look the same in a file listing. That is the trap this index exists to close
(issue #741).

---

## House rule

1. **Edit only the canonical file.** If two files look like the same snippet, the
   one marked canonical in Table A wins. The other one gets a pointer header, not
   an edit.
2. **Verify against live before you edit.** Read back the rendered output (or the
   snippet body if you have an app password) and confirm the file you are about to
   change actually matches what is running. Repo copies drift from live in *both*
   directions, same as the theme does.
3. **Verify against live after you deploy.** Then update the `LAST VERIFIED` line
   in the file header with the date and the method you used.
4. **A repo file is not proof of production.** Never assume. This applies to
   snippets exactly as `AGENTS.md` says it applies to `theme/kk-aurora/style.css`.
5. **No snippet deploys without KK approval and a stated rollback path.** Rollback
   for a Code Snippet is normally: deactivate it, then restore the prior body from
   a snapshot.

---

## Table A. Snippet PHP sources

Public behaviour verified 2026-08-15 (issue #741) by logged-out readback of
`https://kriskrug.co/` and `https://kriskrug.co/2026/08/10/keep-the-machine-strange/`,
plus `/robots.txt`, `/wp-sitemap.xml`, `/news-sitemap.xml` and `/shop/`. The Code
Snippets REST route (`code-snippets/v1/snippets`) returns **401** without a WP app
password and none was resolvable in that session, so **no snippet body was read
back live**. Snippet IDs and the 2026-07-24 active flags come from the committed,
authenticated capture at
`backup/aurora-deploy-20260724/snippets/code-snippets-before-creamfix-20260724T225655Z.json`.
That capture is durable evidence of the state on its timestamp, not proof that a
slot or body is unchanged today; current-provider claims also use rendered output.

| File | Purpose | Live? | Snippet ID | Last verified | Evidence |
|---|---|---|---|---|---|
| `schema-snippets-deployed.php` | **Canonical** Person / WebSite / BlogPosting / Breadcrumb / Service JSON-LD | **Live** | 5 | 2026-08-15 | Rendered JSON-LD matches values, block set and key order, incl. `Person.image` appended last and the #425 `BlogPosting` default. ID from `docs/current-state/TWO-TRACK-MODEL.md`, `docs/current-state/CSS-DEADCODE-OVERLAP-AUDIT.md` |
| `schema-snippets.php` | Reference / future mu-plugin draft of the same schema | **Not live** | none | 2026-08-15 | Gated on `kk_schema_is_ready()`, still full of `VERIFY-ME`, so it would emit nothing. Live `worksFor` / `sameAs` contradict it. Open issue #741 retains the authenticated-body proof and deletion/pointer decision |
| `asset-diet-snippet.php` | Drops unused Jetpack / Popup Maker / jQuery Migrate CSS+JS | **Live** | 10 | not re-checked here | `docs/current-state/archive/WORK-PLAN-2026-07-01.md`, `docs/current-state/AURORA-STYLESHEET-DECISION-2026-08-02.md`. **Issue #706 is active against this file. Do not edit it without coordinating.** |
| `issue-706-script-diet-snippet.php` | Prepared Site Kit gtag delay; pairs with a separately gated Meta Pixel removal | **Not live; prep only** | none | 2026-08-16 | `issue-706-script-diet.md` and merged PR #760 state that nothing was applied and #706 closes only after a KK-approved apply plus PSI verification |
| `og-restore-snippet.php` | Retired Open Graph + Twitter Card bridge | **Inactive; theme is current provider** | 12 | capture: 2026-07-24; render: 2026-08-15 | Authenticated capture records ID 12 with `active=false`. Current markup contains the theme-only `meta name="description"`, theme `og:site_name`, and curated post description; activating this snippet would make the theme stand down and regress those fields. See `docs/current-state/reports/og-restore-snippet-diagnosis-20260815.md` |
| `gsc-404-query-param-canonicalize.php` | Canonicalizes legacy `?share=` tracking params out of GSC | **Live** | 8 | not re-checked here | Deploy receipt `docs/current-state/reports/gsc-404-live-deploy-20260618-050833Z.md` |
| `robots-txt-ai-policy.php` | robots.txt policy via the WP filter | **Not the live provider** | none | 2026-08-15 | Live `/robots.txt` is the physical file (its own header says `Source: ... fixes/robots.txt`), which wins over the filter exactly as this file's header warns. See Table B |
| `issue-331-archive-sitemap-policy.php` | Excludes author archives from the core sitemap | **Not live** | none | 2026-08-15 | `/wp-sitemap.xml` still lists `wp-sitemap-users-1.xml` |
| `kk-news-sitemap-snippet.php` | Google News style sitemap at `/news-sitemap.xml` (#425) | **Active in the 2026-07-24 capture; public route not verified working** | 13 | capture: 2026-07-24; render: 2026-08-15 | Authenticated capture records ID 13 with `active=true`, while `/news-sitemap.xml` returned 301 rather than XML. The body was not read live in this pass, so do not assume this repo copy matches the current slot or redeploy it without authenticated readback and KK approval |
| `issue-158-shopify-embed.php` | Shopify Buy Button wiring for a Shop page | **Not live** (draft) | none | 2026-08-15 | `/shop/` returns 404; no `kk-shop` or `BuyButton` in live markup. Placeholders unfilled |
| `issue-39-schema-markup.php` | Original Person / Organization / Article schema | **Not live**, superseded by snippet 5 | none | 2026-08-15 | Live emits exactly one `Person` block and it has snippet 5's shape. `docs/current-state/archive/AGENT-SWARM-OPERATING-PLAN-2026-05-18.md` records #39 as superseded |
| `issue-43-twitter-cards.php` | Twitter/X card tags | **Not live** | none | 2026-08-15 | Live Twitter tags come from Aurora; authenticated capture shows the overlapping OG bridge (snippet 12) inactive |
| `issue-8-aria-labels.php` | ARIA labels + focus rings for icon controls | **Not live** (draft) | none | 2026-08-15 | No `kk-issue-8-icon-accessibility` style id in live markup. Corroborated by the 13-route style-id enumeration in `docs/current-state/AURORA-STYLESHEET-DECISION-2026-08-02.md` (zero unknown ids) |
| `issue-9-search-accessibility.php` | Accessible search form markup | **Not live** (draft) | none | 2026-08-15 | No `kk-site-search-field-` in live markup |

**Reading the "Live?" column.** "Live" means current production behaviour matches
this file. "Active in the capture" means only that the committed authenticated
2026-07-24 inventory recorded the Code Snippet slot as enabled. Neither phrase
means the bodies are byte-identical, because no snippet body was read back live in
this pass. One known open delta is recorded in the header of
`schema-snippets-deployed.php`: live wraps JSON-LD in
`<script data-jetpack-boost="ignore" ...>` and nothing in this repo emits that
attribute. Resolve that before the next schema deploy.

## Table B. Served root files

Physical files served from the Pagely document root. A physical file **beats** any
WordPress filter at the same path, which is why `robots-txt-ai-policy.php` is inert.

| File | Serves as | Live? | Last verified | Note |
|---|---|---|---|---|
| `robots.txt` | `https://kriskrug.co/robots.txt` | **Live, one revision stale** | 2026-08-15 | Live body is identical to this file except the header date: live says `Last reviewed: 2026-06-07`, repo says `2026-07-01`. Directives themselves match |
| `llms.txt` | `https://kriskrug.co/llms.txt` | linked from live robots.txt | not checked | Template lives at `llms-txt-template.md` |
| `robots-txt-update.txt` | nothing | archival | n/a | Superseded draft of the robots policy |

## Applied handoff records (archival)

The 47 files not covered by Table A, Table B, or this README are receipts and
reference artifacts, not runtime code. Do not treat them as sources of truth for
what is live; they describe what *was* applied or proposed at the time.

- `issue-<n>-*.md` and matching `issue-<n>-*.json` (roughly 37 files, mostly the
  July 2026 SEO backfill wave: #249, #284, #316, #328, #335, #336, #340, #342,
  #345, #353, #355). The `.json` is the machine payload, the `.md` is the human
  handoff.
- `*.css` (`aurora-cream-pack-chrome.css`, `issue-5-color-contrast.css`,
  `issue-9-button-hover-states.css`, `issue-10-cta-hover-states.css`). Historical
  CSS proposals. The two that reached production as snippets (9 and 11) are
  recorded **inactive**; see `docs/current-state/AURORA-STYLESHEET-DECISION-2026-08-02.md`
  before reactivating anything here.
- `gsc-404-redirection-import-2026-06.json`, a one-shot Redirection plugin import.
- Loose narrative docs: `README-FIXES-BATCH-1.md`, `UPDATED-ABOUT-PAGE-COMPLETE.md`,
  `owned-sites-network-rollout.md`, `llms-txt-template.md`.

## Open flags from the 2026-08-15 index pass

Recorded here so they are not lost. None are fixed in the #741 PR.

1. **No snippet body was ever read back.** Everything in Table A is inferred from
   rendered output. An authenticated `GET code-snippets/v1/snippets?context=edit`
   would upgrade all of it to direct proof, and would settle the
   `data-jetpack-boost` question. Needs `WP_USER` + `WP_APP_PASSWORD`.
   This missing direct proof keeps issue #741 open; merging the index does not
   satisfy its authenticated-body acceptance criterion.
2. **Snippet 12 is inactive and should not be reactivated.** The committed capture
   supplies its ID and inactive state; current rendered output proves Aurora is the
   provider. Optional deletion/rename of the inactive live slot remains KK-gated.
3. **Snippet 13 was active in the 2026-07-24 capture, but its route did not render
   XML on 2026-08-15.** Read the live body and current active state before changing
   or redeploying it; the capture cannot prove today's slot contents.
4. **Live `/robots.txt` is one revision behind the repo copy** (see Table B).
5. **`schema-snippets.php` deletion/pointer decision** remains open in #741 and is
   not taken here.
