# Repo reclaim list — #369 / #318 (2026-07-26)

**Status:** ranked, verified proposal for KK path-by-path approval. **No deletes in this commit.**  
**Branch:** `cursor/369-reclaim-list-f196`  
**Parent:** [#369](https://github.com/WalksWithASwagger/kriskrug-wp/issues/369) · [#318](https://github.com/WalksWithASwagger/kriskrug-wp/issues/318)

## Measurement snapshot (working tree, 2026-07-26)

| Path | `du -sh` | Notes |
|---|---:|---|
| `content/drafts/` | **238 MB** | Dominated by tracked PNGs/JPGs for already-published posts |
| `docs/current-state/reports/` | **28 MB** | ~22.6 MB under `screenshots/`; rest is markdown + small captures |
| `backup/` | **20 MB** | Tracked HTML/JSON/PNG snapshots only — `*.zip` / `*.gz` already gitignored |

**Sources refreshed:** `REPO-HYGIENE-AUDIT-2026-07-12.md`, `reports/repo-hygiene-prune-triage-20260716.md`, `reports/issue-318-phase-b-reclaim-inventory-20260716.json`, public WP slug probe (2026-07-26), `CURRENT-STATE-2026-07-16.md` + README + `backup/*/DEPLOY-HANDOFF.md` cross-check.

**Totals (tracked reclaim candidates):**

| Bucket | Approx reclaimable | Risk mix |
|---|---:|---|
| Published-post draft images | **188.6 MB** | safe (after WP media spot-check) |
| `you-cant-drink-data` photo archive | **20.7 MB** | review (source photography set) |
| Unpublished / not-found draft images | **23.3 MB** | review |
| Report screenshots + root PNGs | **24.1 MB** | safe |
| Obsolete / unreferenced `backup/` dirs | **9.5 MB** | review (historical QA docs may cite) |
| **Grand total proposed** | **~266 MB** | working-tree only; no history rewrite |

Out of scope (separate KK thread): `git filter-repo` / force-push to shrink `.git`.

---

## Rules for the eventual delete PR

1. KK must approve the exact paths below (or a subset) before any delete/move PR.
2. Keep all `*.md` under `content/drafts/` and all `morning-truth-*.md` / narrative reports.
3. Do not touch paths in **§ Exclusions preserved**.
4. Prefer `git rm` of approved binaries; extend `.gitignore` / Git LFS for future spill. No history rewrite in that PR.
5. `backup/**/*.zip` is already ignored — there are **no tracked zips** to reclaim; disk zips (if any on a laptop clone) stay local-only.

---

## Ranked reclaim list

Columns: **path** · **size** · **reason** · **risk** · **recommended action**.

### A. Draft images — published posts (safe after WP media spot-check)

Public REST confirmed `status=publish` (inventory 2026-07-16 + re-probe 2026-07-26). Canonical media lives on WP/CDN; repo copies are publish working files. **Keep markdown; remove image binaries only.**

| Path | Size | Reason | Risk | Recommended action |
|---|---:|---|---|---|
| `content/drafts/2026-05-23-data-center-protest-signs/images/` | 40.2 MB | draft PNG/JPG; live post `11929` | safe | delete (after WP media check) |
| `content/drafts/2026-05-16-why-we-built-the-responsible-ai-professional-certification/images/` | 33.3 MB | draft PNG; live post `12257` | safe | delete |
| `content/drafts/2026-05-07-web-summit-vancouver-2026/images/` | 28.1 MB | draft PNG; live post `11826` | safe | delete |
| `content/drafts/2026-05-13-sovereign-ai-for-whom/images/` | 22.8 MB | draft PNG/JPG; live post `11905` | safe | delete |
| `content/drafts/2026-06-07-god-skills-agentic-loop-workflows/images/` | 21.6 MB | draft PNG; live post `12263` | safe | delete |
| `content/drafts/2026-06-04-ai-keynote-slides-visual-workflow/images/` | 7.8 MB | draft PNG; live post `12183` | safe | delete |
| `content/drafts/2026-06-23-vancouver-made-world-cup/images/` | 7.2 MB | draft JPG/PNG; live post `12363` | safe | delete |
| `content/drafts/2026-06-04-the-great-canadian-proximity-game/images/` | 3.9 MB | draft PNG; live post `12190` | safe | delete |
| `content/drafts/2026-06-16-storyhive-haus-of-owl-jordan-dack/images/` | 3.8 MB | draft PNG; live post `12327` | safe | delete |
| `content/drafts/2026-05-24-what-would-chat-do-and-why-thats-the-wrong-question/images/` | 3.8 MB | draft PNG; live post `12032` | safe | delete |
| `content/drafts/2026-06-23-ethos-lab-block-party/images/` | 3.2 MB | draft JPG; live post `12357` | safe | delete |
| `content/drafts/2026-05-24-canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one/images/` | 3.1 MB | draft PNG; live post `12030` | safe | delete |
| `content/drafts/2026-05-24-ai-wont-fix-your-broken-permit-process/images/` | 3.0 MB | draft PNG; live post `12035` | safe | delete |
| `content/drafts/2026-07-07-the-cheer-is-a-cap-table/images/` | 2.9 MB | draft PNG; live post `12479` | safe | delete |
| `content/drafts/2026-05-14-calling-us-all-in/images/` | 2.4 MB | draft JPEG; live post `11765` | safe | delete |
| `content/drafts/2026-07-05-artists-learn-machines-extract/images/` | 1.3 MB | draft PNG; live post `12473` | safe | delete |
| **Subtotal A** | **~188.6 MB** | | | |

Optional future policy (not this PR): track new draft images via Git LFS or keep them gitignored like `you-cant-drink-data/photos-raw/`.

### B. Draft photo archive — published but source-like (review)

| Path | Size | Reason | Risk | Recommended action |
|---|---:|---|---|---|
| `content/drafts/2026-05-23-you-cant-drink-data/photos/` | 20.7 MB | draft JPG archive (`photos/best/` + `photos/inbody/`); live post `11936` | review | move to gitignore **or** Git LFS — do not blunt-delete without KK call on outtakes vs WP media |
| **Subtotal B** | **~20.7 MB** | | | |

### C. Draft images — not found on public WP (review)

| Path | Size | Reason | Risk | Recommended action |
|---|---:|---|---|---|
| `content/drafts/2026-05-24-human-element-shane-loki-talk/images/` | 18.3 MB | draft PNG; no public post/page slug match | review | keep until KK confirms draft/private/elsewhere, then delete or LFS |
| `content/drafts/2026-05-24-how-we-did-it-behind-the-scenes-of-the-sfu-siat-microcredential-project/images/` | 2.7 MB | draft PNG; not public | review | keep / LFS until publish fate known |
| `content/drafts/2026-05-25-cotton-underwear-paradox/images/` | 2.2 MB | draft PNG; not public | review | keep / LFS until publish fate known |
| **Subtotal C** | **~23.3 MB** | | | |

### D. Report screenshots & capture spill (safe)

Markdown summaries stay. These binaries are one-off visual/ops evidence; `.gitignore` already blocks new `reports/screenshots/` growth.

| Path | Size | Reason | Risk | Recommended action |
|---|---:|---|---|---|
| `docs/current-state/reports/screenshots/aurora-opal-20260701/` | 6.0 MB | report screenshot | safe | delete |
| `docs/current-state/reports/screenshots/aurora-opal-live-20260701/` | 6.0 MB | report screenshot | safe | delete |
| `docs/current-state/reports/screenshots/aurora-readability-*-20260701.png` (4 files at screenshots root) | 5.3 MB | report screenshot | safe | delete |
| `docs/current-state/reports/screenshots/aurora-opal-1329-live-20260701/` | 1.9 MB | report screenshot | safe | delete |
| `docs/current-state/reports/screenshots/topic-hubs-20260701/` | 1.8 MB | report screenshot | safe | delete |
| `docs/current-state/reports/screenshots/content-architecture-20260701/` | 1.6 MB | report screenshot | safe | delete |
| `docs/current-state/reports/front-page-feature-pillars-final-polish-desktop-20260703-165421Z.png` | 1.1 MB | report screenshot | safe | delete |
| `docs/current-state/reports/front-page-feature-pillars-final-polish-mobile-20260703-165421Z.png` | 0.3 MB | report screenshot | safe | delete |
| `docs/current-state/reports/screenshots/` (remaining tracked PNGs if any after dirs above) | ~0 MB residual in tree total **22.6 MB** | report screenshot | safe | delete whole tracked `screenshots/` tree |
| **Subtotal D (screenshots + root PNGs)** | **~24.1 MB** | | | |

Small root JSON/HTML/CSV captures (~0.7 MB under `reports/`) are optional follow-on: many are cited by sibling `.md` reports — treat as **review**, not in the first delete wave.

### E. Obsolete / unreferenced `backup/` dirs (review)

Not cited by `CURRENT-STATE-2026-07-16.md`, README deploy lines, or `backup/*/DEPLOY-HANDOFF.md`. Some appear in older Aurora QA docs — KK should confirm those historical links may go stale.

| Path | Size | Reason | Risk | Recommended action |
|---|---:|---|---|---|
| `backup/20260525-qa-visual-134/` | 4.5 MB | obsolete backup QA PNGs (cited by `AURORA-LIVE-QA-2026-05-25.md`) | review | delete after KK OK that May-25 QA evidence can live in git history only |
| `backup/20260525-qa-visual/` | 4.3 MB | obsolete backup QA PNGs | review | delete (same gate) |
| `backup/20260624-181106Z-issue233-companions/` | 0.3 MB | obsolete backup JSON | review | delete |
| `backup/20260519-105949/` | 0.1 MB | obsolete backup page snapshot | review | delete |
| `backup/20260623-163028Z/` | 0.1 MB | obsolete backup HTML | review | delete |
| `backup/20260518-123159/` | 0.1 MB | obsolete backup (not in #76 README set) | review | delete |
| `backup/20260518-214007/` | 0.1 MB | obsolete backup | review | delete |
| `backup/20260518-214334/` | 0.1 MB | obsolete backup | review | delete |
| `backup/20260705T201901Z-artists-learn-machines-extract/` | ~0 MB | obsolete backup crumbs | review | delete |
| **Subtotal E** | **~9.5 MB** | | | |

Note: future `backup/**/*.png` is already gitignored; deleting the tracked QA PNGs stops reintroducing them on checkout only after the delete PR.

---

## Top 20 paths by size (quick scan)

| # | Path | Size | Bucket |
|---:|---|---:|---|
| 1 | `content/drafts/2026-05-23-data-center-protest-signs/images/` | 40.2 MB | A safe |
| 2 | `content/drafts/2026-05-16-why-we-built-the-responsible-ai-professional-certification/images/` | 33.3 MB | A safe |
| 3 | `content/drafts/2026-05-07-web-summit-vancouver-2026/images/` | 28.1 MB | A safe |
| 4 | `content/drafts/2026-05-13-sovereign-ai-for-whom/images/` | 22.8 MB | A safe |
| 5 | `content/drafts/2026-06-07-god-skills-agentic-loop-workflows/images/` | 21.6 MB | A safe |
| 6 | `content/drafts/2026-05-23-you-cant-drink-data/photos/` | 20.7 MB | B review |
| 7 | `content/drafts/2026-05-24-human-element-shane-loki-talk/images/` | 18.3 MB | C review |
| 8 | `content/drafts/2026-06-04-ai-keynote-slides-visual-workflow/images/` | 7.8 MB | A safe |
| 9 | `content/drafts/2026-06-23-vancouver-made-world-cup/images/` | 7.2 MB | A safe |
| 10 | `docs/current-state/reports/screenshots/aurora-opal-20260701/` | 6.0 MB | D safe |
| 11 | `docs/current-state/reports/screenshots/aurora-opal-live-20260701/` | 6.0 MB | D safe |
| 12 | `docs/current-state/reports/screenshots/` readability root PNGs | 5.3 MB | D safe |
| 13 | `backup/20260525-qa-visual-134/` | 4.5 MB | E review |
| 14 | `backup/20260525-qa-visual/` | 4.3 MB | E review |
| 15 | `content/drafts/2026-06-04-the-great-canadian-proximity-game/images/` | 3.9 MB | A safe |
| 16 | `content/drafts/2026-06-16-storyhive-haus-of-owl-jordan-dack/images/` | 3.8 MB | A safe |
| 17 | `content/drafts/2026-05-24-what-would-chat-do-and-why-thats-the-wrong-question/images/` | 3.8 MB | A safe |
| 18 | `content/drafts/2026-06-23-ethos-lab-block-party/images/` | 3.2 MB | A safe |
| 19 | `content/drafts/2026-05-24-canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one/images/` | 3.1 MB | A safe |
| 20 | `content/drafts/2026-05-24-ai-wont-fix-your-broken-permit-process/images/` | 3.0 MB | A safe |

Largest single files (for delete-PR cherry-picking):

| Path | Size |
|---|---:|
| `content/drafts/2026-05-13-sovereign-ai-for-whom/images/01-sovereign-ai-for-whom.png` | 7.8 MB |
| `content/drafts/2026-05-13-sovereign-ai-for-whom/images/03-sovereign-ai-for-whom.png` | 5.3 MB |
| `content/drafts/2026-05-13-sovereign-ai-for-whom/images/04-sovereign-ai-for-whom.jpg` | 4.2 MB |
| `content/drafts/2026-06-07-god-skills-agentic-loop-workflows/images/99-optional-from-intent-to-ship-review-required.png` | 3.9 MB |
| `content/drafts/2026-05-23-data-center-protest-signs/images/03-my-position-yes-also-help.png` | 3.7 MB |

---

## Exclusions preserved (do **not** delete)

Referenced by `CURRENT-STATE-2026-07-16.md`, `docs/current-state/README.md`, recent deploy handoffs, or active content-architecture / GSC rollback notes.

| Path | Size (tracked) | Why keep |
|---|---:|---|
| `backup/aurora-deploy-20260724/` | 2.0 MB | Active Revive/Aurora deploy handoff + e2e/R9 evidence (`DEPLOY-HANDOFF.md`, README 2026-07-24 readback) |
| `backup/aurora-deploy-20260716/` | ~0 MB (+ ignored zips) | CURRENT-STATE / WORK-PLAN **1.3.40** package + checksums |
| `backup/aurora-deploy-20260713/` | ~0 MB | Handoff retained so “do not upload 1.3.39” remains auditable |
| `backup/aurora-deploy-20260614/` | ~0 MB | Historical deploy handoff still indexed in release checklist |
| `backup/20260518-111546/` | 1.3 MB | Issue #76 rollback — README |
| `backup/20260518-113350/` | 1.3 MB | Issue #76 rollback — README |
| `backup/20260518-215912/` | 0.1 MB | Issue #76 / Speaking rollback — README |
| `backup/20260518-223014/` | 0.5 MB | IA-polish rollback — README / RESUME-HERE |
| `backup/20260518-224340/` | 0.2 MB | About rollback — README / RESUME-HERE |
| `backup/20260701T193335Z-content-architecture/` | 1.2 MB | Content-architecture deploy snapshots |
| `backup/20260701T202734Z-content-architecture/` | 0.9 MB | Content-architecture deploy snapshots |
| `backup/20260706T190831Z-content-architecture/` | 0.1 MB | Work visual-card snapshots |
| `backup/20260706T191550Z-content-architecture/` | 0.1 MB | Work visual-card final deploy |
| `backup/20260618-050328Z/` | ~0 MB | GSC-404 before snapshots |
| `backup/20260618-050833Z/` | 0.1 MB | GSC-404 after snapshots |
| `backup/20260618-051950Z/` | ~0 MB | a11y CTA hotfix snapshots |
| `backup/20260604-work-page-68/` | 0.1 MB | Work page metadata proof |
| `backup/20260525-201025Z/` | 0.8 MB | May-25 content recovery snapshots (still cross-linked) |
| `backup/20260525-220404Z/` | 0.3 MB | Events page after snapshots |
| `backup/2026-05-16/` | ~0 MB | Manifest / checksums for backup-check |
| `backup/page-snapshots/` | 0.1 MB | Indexed page snapshot crumbs |
| All `docs/current-state/reports/*.md` (esp. `morning-truth-*.md`) | n/a | Startup source of truth — never prune for reclaim |
| `content/drafts/**/*.md` | n/a | Draft source text stays |

**Excluded tracked backup subtotal ≈ 9.2 MB** (plus any laptop-local ignored zips under aurora-deploy dirs).

---

## Suggested KK approval shapes

1. **Approve Tier A + D only** (~212 MB) — largest safe win; leave B/C/E for a second pass.
2. **Approve A + B + D** (~233 MB) — includes `you-cant-drink-data` photo move/delete call.
3. **Approve all A–E** (~266 MB) — full working-tree reclaim; accept stale links in May-25 QA docs.

Reply on #369 with the chosen shape (or an edited path allow-list). Then open a focused delete-only PR — no history rewrite.

## Acceptance checklist (#369)

- [x] Ranked reclaim list committed (`docs/current-state/reports/repo-reclaim-list-20260726.md`)
- [ ] KK approves exact paths
- [ ] PR removes only approved paths
- [ ] Morning-truth still works; no active deploy rollback broken
