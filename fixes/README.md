# `fixes/` index

This directory holds two very different kinds of thing mixed together (run
`git ls-files fixes | wc -l` for the current file count; it is not kept here
because it drifts):

- **Snippet and tag sources** (`.php` and `.js`). Some are the source of truth for PHP that
  is running in production via the Code Snippets plugin; others are inactive,
  superseded, or drafts. Editing any of them is prod-adjacent work until its
  current slot/provider state is proved.
- **Supporting files** (everything else). These include three served-root files,
  this index, and archival handoff/reference artifacts. Nothing in the archival
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

## Table A. Snippet and tag sources (`.php`, `.js`)

Every tracked `fixes/*.php` and `fixes/*.js` file has a row below. Rows for the
files that went live in September and October (Snippets 24, 25 and 26 and the
#1090 GTM tag) were brought current on 2026-11-12 (#1227) from the deploy
receipts, with logged-out spot checks the same day.

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
| `schema-snippets-deployed.php` | **Canonical** Person / WebSite / BlogPosting / Breadcrumb / Service JSON-LD and Speaking `VideoObject` records | **Live, including Person consolidation, Speaking videos and the #1238 `JSON_HEX_TAG` / `JSON_HEX_AMP` flags** | 5 | saved 2026-11-12 | Person and Speaking schema went live in the KK-directed 2026-10-25 save: [release receipt](../docs/current-state/reports/schema-1089-release-2026-10-25.md). Since 2026-11-12 live snippet 5 also runs `JSON_HEX_TAG` and `JSON_HEX_AMP` in `kk_schema_emit()`. That KK-approved save changed only the flags line, with exact authenticated readback, logged-out JSON-LD checks and zero-error Schema Markup Validator results: [#1238 release receipt](../docs/current-state/reports/snippet-5-hextag-release-2026-11-12.md). Executable bytes from `kk_schema_constants()` onward match live exactly. The live header is still the #1082 header (commit `3807e6b`) that the 2026-10-25 save stored, so the repo header is documentation only. Historical approval packet: `issue-1089-schema-save-preflight-2026-09-29.md`. Live `data-jetpack-boost="ignore"` is Boost-injected. |
| `schema-snippets.php` | Reference / future mu-plugin draft of the same schema | **Not live** | none | 2026-08-15 | Gated on `kk_schema_is_ready()`, still full of `VERIFY-ME`, so it would emit nothing. Live `worksFor` / `sameAs` contradict it. Open issue #741 retains the authenticated-body proof and deletion/pointer decision |
| `asset-diet-snippet.php` | Drops unused Jetpack / Popup Maker / jQuery Migrate CSS+JS | **Live** | 10 | not re-checked here | `docs/current-state/archive/WORK-PLAN-2026-07-01.md`, `docs/current-state/AURORA-STYLESHEET-DECISION-2026-08-02.md`. Not modified by the separate #706 closeout. |
| `issue-706-script-diet-snippet.php` | Delays Site Kit gtag until first interaction or three-second idle; paired with the disabled WPCode Meta Pixel | **Live** | 22 | public render 2026-08-28 | [`issue-706-script-diet.md`](issue-706-script-diet.md) and [`../docs/current-state/reports/issue-706-script-diet-apply-20260817.md`](../docs/current-state/reports/issue-706-script-diet-apply-20260817.md); #706 closed after KK accepted the PSI trace caveat |
| `og-restore-snippet.php` | Retired Open Graph + Twitter Card bridge | **Inactive; theme is current provider** | 12 | capture: 2026-07-24; render: 2026-08-15 | Authenticated capture records ID 12 with `active=false`. Current markup contains the theme-only `meta name="description"`, theme `og:site_name`, and curated post description; activating this snippet would make the theme stand down and regress those fields. See `docs/current-state/reports/og-restore-snippet-diagnosis-20260815.md` |
| `gsc-404-query-param-canonicalize.php` | Canonicalizes legacy `?share=` tracking params out of GSC | **Live** | 8 | not re-checked here | Deploy receipt `docs/current-state/reports/gsc-404-live-deploy-20260618-050833Z.md` |
| `robots-txt-ai-policy.php` | robots.txt policy via the WP filter | **Not the live provider** | none | 2026-08-15 | Live `/robots.txt` is the physical file (its own header says `Source: ... fixes/robots.txt`), which wins over the filter exactly as this file's header warns. See Table B |
| `issue-331-archive-sitemap-policy.php` | v1 archive policy (author archives and taxonomies out of the core sitemap, archives noindex) | **Not live; superseded by `issue-331-archive-sitemap-policy-v2.php`** | none | 2026-11-12 | Never deployed. v2 replaced it before activation; do not activate both. Keep as the 2026-07-12 receipt artifact (`docs/current-state/reports/issue-331-archive-policy-20260712.md`). Its header comment is corrected in a separate comment-only PR (#1227) |
| `issue-331-archive-sitemap-policy-v2.php` | **Canonical** #331 v2 archive policy: drops the users, category and tag sitemap providers, `noindex,follow` on author, tag, category and date archives | **Live** | 26 ("KK 331 v2: archive sitemap + indexability policy", front-end) | deployed 2026-09-03; sitemap readback 2026-11-12 | [Deploy receipt](../docs/current-state/reports/DEPLOY-767-331-2026-09-03.md) (byte-diffed against this file before activation). Logged-out `/wp-sitemap.xml` on 2026-11-12 lists two children, posts-post and posts-page. Reconciliation: [`sitemap-1130-reconciliation-2026-10-25.md`](../docs/current-state/reports/sitemap-1130-reconciliation-2026-10-25.md). Rollback: deactivate snippet 26, purge cache. #767 sitemap half is handled here, so `issue-767-hide-user-sitemap.php` was not deployed |
| `issue-767-hide-rest-users.php` | Restricts unauthenticated GET/HEAD `/wp/v2/users` | **Live (v2)** | 24 ("KK 767: restrict unauthenticated REST users", global) | v1 live 2026-09-03; v2 live 2026-11-12; logged-out 401 re-checked 2026-11-12 | [Deploy receipt](../docs/current-state/reports/DEPLOY-767-331-2026-09-03.md) for v1. v2 (case-insensitive route match plus a controller-level backstop) was applied live on 2026-11-12 by the #767 session. **Its updated source lands with PR #1288**; until that merges this file is the v1 source and still carries the old prep-only header, so do not read that header as status. Snippet 24 is covered by #1288, not by #1227 |
| `issue-767-disable-author-probes.php` | 404s `/?author=N` query probes; leaves pretty author archives to #331 | **Live** | 25 ("KK 767: disable author enumeration probes", front-end) | deployed 2026-09-03; `/?author=1` 404 re-checked 2026-11-12 | [Deploy receipt](../docs/current-state/reports/DEPLOY-767-331-2026-09-03.md): `/?author=1` and `/?author=18` went from 301 to 404; `/author/kk/` stays 200 as #331 requires. The file header still says prep only (stale); fixing it is comment-only and needs KK's go-ahead |
| `issue-767-hide-user-sitemap.php` | Removes the users sitemap provider only; preserves every other provider | **Not live; not deployed** | none | 2026-11-12 | The September deploy skipped it because #331 v2 already drops the users provider and running both paths is forbidden ([receipt](../docs/current-state/reports/DEPLOY-767-331-2026-09-03.md)). Narrow alternative only; do not enable alongside snippet 26 |
| `issue-1002-xmlrpc-constrain.php` | Fallback `xmlrpc_enabled` disable for #1002 | **Not live; prep only** | none | 2026-09-08 | Host/WAF deny is the recommended control. This snippet does not change GET/HEAD 405. Do not enable if Jetpack core is reactivated |
| `issue-995-events-search-snippet.php` | Page 2250 `/events/` approved title + description via `get_post_metadata` | **Not live; prep only** | none | 2026-09-20 | Closeout in `docs/current-state/reports/issue-995-events-search-intent-20260920.md`. Last live-HTML readback: `issue-995-events-search-intent-20260908.md`. Do not activate without KK approval, a page-2250 snapshot, and rollback. Do not pair with snippet 12 |
| `issue-997-homepage-paged-canonical.php` | 301 static-front-page `/page/{n}/` (n ≥ 2) to `/`; force homepage canonical if a 200 still renders | **Not live; prep only** | none | 2026-09-08 | Diagnosis in `docs/current-state/reports/issue-997-gsc-url-errors-20260908.md`. Same-document alias only. Do not pair with a theme copy of the same filter. Do not redirect `/3/` or other 404s to `/` |
| `issue-1025-crawl-hygiene.php` | Track A #1025: repo-tracked `/home/` 301 + sitemap drop, stop minting `share`/`nb`/`amp`, 301 tag/author feeds and author `/page/{n}/` | **Not live; prep only** | none | 2026-09-18 | Soft-ship only. Live `/home/` 301 is already Redirection; snippet 8 already 301s share variants. Do not activate without SEO LGTM. Do not pair with a second Redirection `/home/` rule. See `issue-1025-apply.md`. Policy JSON: `issue-1025-crawl-policy.json`. |
| `issue-1131-exclude-home-sitemap.php` | Track A #1131: drop published page slug `home` (ID 2315) from the core page sitemap | **Not live; prep only** | none | 2026-10-17 | Narrower than #1025. Does not add a `/home/` redirect or touch feeds. Do not activate without KK / #1114. See `issue-1131-apply.md`. |
| `kk-news-sitemap-snippet.php` | Google News style sitemap at `/news-sitemap.xml` (#425) | **Active in the 2026-07-24 capture; public route not verified working** | 13 | capture: 2026-07-24; render: 2026-08-15 | Authenticated capture records ID 13 with `active=true`, while `/news-sitemap.xml` returned 301 rather than XML. The body was not read live in this pass, so do not assume this repo copy matches the current slot or redeploy it without authenticated readback and KK approval |
| `issue-158-shopify-embed.php` | Shopify Buy Button wiring for a Shop page | **Not live** (draft) | none | 2026-08-15 | `/shop/` returns 404; no `kk-shop` or `BuyButton` in live markup. Placeholders unfilled |
| `issue-39-schema-markup.php` | Original Person / Organization / Article schema | **Not live**, superseded by snippet 5 | none | 2026-08-15 | Live emits exactly one `Person` block and it has snippet 5's shape. `docs/current-state/archive/AGENT-SWARM-OPERATING-PLAN-2026-05-18.md` records #39 as superseded |
| `issue-43-twitter-cards.php` | Twitter/X card tags | **Not live** | none | 2026-08-15 | Live Twitter tags come from Aurora; authenticated capture shows the overlapping OG bridge (snippet 12) inactive |
| `issue-8-aria-labels.php` | ARIA labels + focus rings for icon controls | **Not live** (draft) | none | 2026-08-15 | No `kk-issue-8-icon-accessibility` style id in live markup. Corroborated by the 13-route style-id enumeration in `docs/current-state/AURORA-STYLESHEET-DECISION-2026-08-02.md` (zero unknown ids) |
| `issue-9-search-accessibility.php` | Accessible search form markup | **Not live** (draft) | none | 2026-08-15 | No `kk-site-search-field-` in live markup |
| `issue-1090-krug-signup-tag.js` | GTM Custom HTML tag that records a completed KRÜG newsletter signup on the Beehiiv `signedUp` event (consent-gated) | **Live as a GTM tag, not a Code Snippet** | GTM container `GTM-MGD93937`, published version 2 ("KRÜG completed signup — #1090") | deployed 2026-10-25 | [Release receipt](../docs/current-state/reports/krug-conversion-1090-2026-10-25.md); import file `issue-1090-krug-signup-gtm.json`, handoff `issue-1090-conversion-handoff-2026-09-30.md`. Runs on `vancouver.beehiiv.com`, not on kriskrug.co. #1090 stays open until organic delivery is observed. Rollback: pause the tag and publish a new version, or restore GTM version 1 (empty container) |
| `issue-1090-success-event.js` | Contract helper that would fire a GA4 event on a verified first-party success signal | **Not live** (its header says so) | none | 2026-11-12 | Candidate from the [#1090 preflight](../docs/current-state/reports/issue-1090-conversion-preflight-2026-09-29.md). The deployed conversion path is the GTM tag above, not this file. Do not enqueue it on kriskrug.co |

**Reading the "Live?" column.** "Live" means current production behaviour matches
this file. "Active in the capture" means only that the committed authenticated
2026-07-24 inventory recorded the Code Snippet slot as enabled. Neither phrase
means the bodies are byte-identical in the original inventory pass. Snippet 5's
October 25 and November 12 releases are an exception: each authenticated body
was read back and verified against the approved payload, as recorded in the
linked receipts.
The live JSON-LD wrapper
`<script data-jetpack-boost="ignore" type="application/ld+json">` is
**Boost-injected** (issue #758): Jetpack Boost's Defer JS pipeline stamps
that attribute onto `application/ld+json` (also `application/json` and
`importmap`) so it does not move those blocks. `kk_schema_emit()` in
`schema-snippets-deployed.php` correctly omits the attribute. Other live
scripts (Site Kit gtag, Meta Pixel inline, `speculationrules`, Boost's
own `boost-cache` bundle) are exempt because they are not in that type
set. Pasting the repo file over snippet 5 will not strip the rendered
attribute. Do not add it by hand.

## Table B. Served root files

Physical files served from the Pagely document root. A physical file **beats** any
WordPress filter at the same path, which is why `robots-txt-ai-policy.php` is inert.

| File | Serves as | Live? | Last verified | Note |
|---|---|---|---|---|
| `robots.txt` | `https://kriskrug.co/robots.txt` | **Live, one revision stale** | 2026-08-15 | Live body is identical to this file except the header date: live says `Last reviewed: 2026-06-07`, repo says `2026-07-01`. Directives themselves match |
| `llms.txt` | `https://kriskrug.co/llms.txt` | linked from live robots.txt | not checked | Template lives at `llms-txt-template.md` |
| `robots-txt-update.txt` | nothing | archival | n/a | Superseded draft of the robots policy |

## Applied handoff records (archival)

Files not covered by Table A, Table B, or this README are receipts and
reference artifacts, not runtime code. Do not treat them as sources of truth for
what is live; they describe what *was* applied or proposed at the time.

- `issue-<n>-*.md` and matching `issue-<n>-*.json` (roughly 37 files, mostly the
  July 2026 SEO backfill wave: #249, #284, #316, #328, #335, #336, #340, #342,
  #345, #353, #355). The `.json` is the machine payload, the `.md` is the human
  handoff. Current Snippet 5 save packet: `issue-1089-schema-save-preflight-2026-09-29.md`
  plus `issue-1089-schema-save-preflight-2026-09-29.json` (#1104 / #1089).
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
   would upgrade slot/body claims to direct proof. Needs `WP_USER` +
   `WP_APP_PASSWORD`. The `data-jetpack-boost` wrapper is settled without that
   read (#758): Boost injects it at output. The missing authenticated body
   still keeps issue #741 open; merging the index does not satisfy its
   authenticated-body acceptance criterion.
2. **Snippet 12 is inactive and should not be reactivated.** The committed capture
   supplies its ID and inactive state; current rendered output proves Aurora is the
   provider. Optional deletion/rename of the inactive live slot remains KK-gated.
3. **Snippet 13 was active in the 2026-07-24 capture, but its route did not render
   XML on 2026-08-15.** Read the live body and current active state before changing
   or redeploying it; the capture cannot prove today's slot contents.
4. **Live `/robots.txt` is one revision behind the repo copy** (see Table B).
5. **`schema-snippets.php` deletion/pointer decision** remains open in #741 and is
   not taken here.
