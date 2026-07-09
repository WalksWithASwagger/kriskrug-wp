# Audit Workplan — 2026-07-09

**Status:** active execution plan after the 2026-07-08 Cursor Cloud audit.  
**Supersedes for sequencing:** `POST-SHIP-AUDIT-WORKPLAN-2026-06-04.md` (keep as historical).  
**Does not authorize** any live WordPress write. Dry-run, slug/ID checks, snapshots, and KK approval still apply.

## Audit snapshot (2026-07-08)

| Signal | Observed | Notes |
|---|---|---|
| Live theme | `kk-aurora` **1.3.36** | Matches AGENTS.md / HANDOFF addendum |
| WordPress | **6.9.4** | Public smoke 0 failures, 3 OG/Twitter warnings |
| Open issues | **29** | Declared 48 in CURRENT-STATE / work plan → drift |
| Open PRs | **5** | Declared 0 → drift |
| Draft queue (unauthenticated) | `0/0/0` | **False zero** — missing `.env`; #303/#309 |
| Local draft packages | ~65 | 5 strong / 25 media-tax / 30 thin / 5 empty-admin |
| `/accessibility/` | **404** | Statement drafted, not published |
| GSAP / reveal safety net | absent | Good |
| `make verify` | green | 53 Notion + 71 root + PHPCS + docs-truth |

Sources: `make status-readonly`, `LOCAL_ONLY=1 make draft-queue-audit`, `make verify`, `scripts/wp7-public-smoke.py`, live `style.css` Version header, `gh issue/pr list`.

## North star

Restore **trustworthy queue truth**, clear the **reviewable PR stack**, then run **one Track A content packet** and **one Track B QA packet** without mixing lanes.

## Lane map

| Lane | Goal | Primary issues / PRs |
|---|---|---|
| A0 — Merge stack | Land already-done agent work | #308→#309→#310→#311→#312 |
| A1 — Truth hygiene | Fix false zeros + stale declared counts | #303, #306; docs refresh |
| A2 — Content publish prep | One body-only packet after KK review | #278/#284/#305; #290/#307; #48/#288/#304 |
| A3 — Cadence | Refill scheduled queue after truth restored | EPIC #219 context; draft audit |
| B1 — Theme/QA | Perf, mobile, undesigned pages | #125, #127, #86, #122, #256 |
| Ops — Access | Secrets + Notion so agents can finish audits | `.env`, Notion MCP |

---

## Phase 0 — Unblock access (human)

Do this once; everything authenticated depends on it.

1. Add `scripts/notion-to-wp/.env` (or cloud secrets) with `WP_USER` / `WP_APP_PASSWORD` (and `WP_AUTH_MODE=login` if using the #309 path).
2. Authenticate Notion MCP in Cursor desktop **or** add `NOTION_TOKEN` so agents can find drafts (e.g. Tristan Harris / AI documentary panel) that are not in this repo.
3. Re-run:
   ```bash
   make status-readonly
   scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/draft_queue_audit.py --format markdown
   ```
4. Done when authenticated draft counts are non-zero (expect ~64 draft posts / ~4 draft pages unless live state truly changed) and Notion search works.

---

## Phase 1 — Merge the existing PR stack (KK review)

Merge in this order; do not close issues until the PR that satisfies them is merged.

| Order | PR | Issue(s) | Why first |
|---|---|---|---|
| 1 | [#308](https://github.com/WalksWithASwagger/kriskrug-wp/pull/308) Work visual-card ship | #302 | Base for stacked #309; packages already-live Work deploy |
| 2 | [#309](https://github.com/WalksWithASwagger/kriskrug-wp/pull/309) WP auth client consolidation | #306, #303 | Restores truthful draft-queue / morning-truth reads |
| 3 | [#310](https://github.com/WalksWithASwagger/kriskrug-wp/pull/310) Cursor Cloud AGENTS notes | setup | Durable cloud env caveats |
| 4 | [#311](https://github.com/WalksWithASwagger/kriskrug-wp/pull/311) a11y + hub-link + About plans | #304/#305/#307 (+ feeds #288/#48/#278/#284/#290) | Planning packets ready for human gates |
| 5 | [#312](https://github.com/WalksWithASwagger/kriskrug-wp/pull/312) `publish_common` refactor | #254 | Code quality; no live write |

**Stop rules:** no force-push to `main`; no auto-merge (`allow_auto_merge=false`); green checks ≠ permission to merge.

**Done when:** open PR count is back near 0 for this stack; #302/#254 closable; #303/#306 closable or explicitly parked with remaining write-client follow-up noted.

---

## Phase 2 — Docs / truth hygiene (agent-safe after Phase 1)

Track A docs-only; one commit concern.

1. Commit a fresh `make morning-truth` report (or keep the latest `status-readonly` evidence if file writes are restricted).
2. Update front-door pointers:
   - `docs/current-state/README.md` → newest morning-truth + this workplan
   - `AGENTS.md` “latest morning-truth” link (still cites `20260624` in one place)
3. Refresh declared counts in a **new** dated snapshot (do not silently rewrite historical `CURRENT-STATE-2026-06-23.md` numbers without a banner). Prefer `CURRENT-STATE-2026-07-09.md` + drift-check inputs.
4. Mark `WORK-PLAN-2026-05-23.md` / June post-ship plan as historical for *sequencing* (already partially bannered).

**Done when:** `make status-readonly` drift on open PRs/issues matches reality; agents stop rediscovering stale “48 issues / 0 PRs”.

---

## Phase 3 — Track A content packets (KK-gated writes)

Run **one packet per session**. Body-only REST. Snapshot under `backup/<timestamp>-…/` first.

### Packet 3A — Topic-hub internal links

- Plan: `content/source-packs/content-architecture-2026/internal-link-batch-plan-2026-07-07.md` (#305 / PR #311)
- Issues: #278, #284
- Do: 14 autonomous-safe body-only links from the plan table
- Do **not**: auto-add `/indigenous-ai/` links (human-review queue in the plan)
- Verify: cache-busted public smoke that each source URL contains the hub href

### Packet 3B — Accessibility statement draft → WP draft

- Plan: `content/drafts/accessibility-statement-2026-07/` (#304 / #288 / #48)
- Human gates before any write: reporting channel, WCAG edition wording, response-time language, reuse of old draft `11886` if it still exists
- Do: create/update WordPress **draft** only; no footer link; no publish
- Publish + footer link remain #48 after preview QA

### Packet 3C — About “From the archive” module

- Plans: `about-bio-source-map-2026-07-07.md` + `about-bio-payload-plan-2026-07-08.md` (#307 / #290 / #269 / #270)
- Do: body-only insert after Public trail; preserve title; no land-acknowledgment rewrite (#22 separate)
- Block: “licensed private pilot” or new credentials without KK wording

### Packet 3D — Cadence refill

- After authenticated draft audit is truthful, pick **one** strong local/WP draft through review → preview → schedule
- Strong local candidates from audit: `keep-the-machine-strange`, remaining unpublished strong packs; cross-check live slug before creating duplicates
- Keep #95 (media appearances) as human editorial gate, not a publish shortcut

---

## Phase 4 — Track B / platform (separate sessions)

Do not mix with Phase 3 content writes.

| Priority | Issue | Action |
|---|---|---|
| 1 | #125 | Boost critical CSS / post-Jetpack perf cleanup |
| 2 | #127 | Dedicated mobile/responsive QA (blocked label — confirm blocker) |
| 3 | #86 | Post-Jetpack perf/a11y/tracking QA umbrella |
| 4 | #122 | Undesigned generic pages (~25) — needs design owner |
| 5 | #256 | CSS dead-code / schema snippet / snippets overlap |
| 6 | #4 / #46 | Alt-text debt + full WCAG audit (long-running) |

Also close OG/Twitter smoke warnings on `/`, `/speaking/`, `/work/` if still present after #308 Work packaging.

---

## Phase 5 — Code follow-ups (agent-safe, no live write)

1. Finish #306 remaining write-capable auth clients if #309 only covered read-only paths.
2. Extend #254 pattern to `publish_context_creators.py` and `publish_keep_the_machine_strange.py` (out of #254 scope).
3. Replace hardcoded `/Users/kk/...` paths with repo-relative / env-driven paths in connector + one-off publish scripts (cloud + other machines break today).
4. Optional: Notion search pass for missing drafts (Tristan Harris / AI documentary panel) once token/MCP works — file a draft package or issue if found.

---

## Explicitly parked / human-only

- #274 / #279 — Search Console submit + query review
- #276 — Delete inactive Jetpack after rollback window
- #277 — Contact CTA product decision
- #249 — SEO striking-distance measurement (blocked)
- #222 — Platform trust epic (umbrella)
- #22 — Land acknowledgment placement decision
- Any `--execute` / `--publish` / `--update` against production without KK

---

## Default next sequence (copy this)

1. **KK:** Phase 0 secrets + Notion auth.  
2. **KK:** Review/merge PR stack Phase 1 in order.  
3. **Agent:** Phase 2 docs hygiene PR.  
4. **KK picks one:** 3A hub links **or** 3B a11y draft **or** 3C About module.  
5. **Agent (Track B session):** #125 or #127 only after content packet closes.

## Restart commands

```bash
git fetch --prune
git status --short --branch
gh pr list --state open --limit 20
gh issue list --state open --limit 50
make status-readonly
LOCAL_ONLY=1 make draft-queue-audit
make verify
```

After `.env` exists:

```bash
scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/draft_queue_audit.py --format markdown
make morning-truth
```
