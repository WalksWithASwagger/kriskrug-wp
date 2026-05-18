# Swarm Status - 2026-05-18

**Purpose:** Current command-desk status after the first bounded issue/content/Aurora swarm.

**Safety stance:** No production WordPress writes were made by this swarm. Draft publishing stopped at local `--dry-run` packs. GitHub issue hygiene was allowed. Connector changes stayed local and are covered by tests.

---

## Executive Status

The backlog is now less foggy:

- GitHub issue hygiene started: completed/duplicate/dormant issues were closed or relabeled.
- The next publishing batch exists locally as three dry-run packs, and authenticated WordPress now shows 32 older admin draft posts plus 3 draft pages.
- The connector has focused post-incident tests and a small readback verification step.
- Track A quick fixes are packaged with snippets, dry-run commands, verification, and rollback.
- Nav/IA decisions are packaged for KK review.
- Aurora remains the gating lane for redesign cutover. Local renders with Aurora active, but the desktop header/nav is broken, so no production activation should happen yet.

## Lane Results

| Lane | Result | Artifact / evidence | Next action |
|---|---|---|---|
| Lane 0 - Queue hygiene | Completed first pass | GitHub issues `#1`, `#2`, `#6`, `#37`, `#39`, and `#69` closed or reframed; `#23` left open with `needs-human-review` | Continue a second hygiene pass over stale `auto-implement` labels before broad issue swarms |
| Lane 1 - Track A quick fixes | Pack created | [`TRACK-A-QUICK-FIX-PACK-2026-05-18.md`](TRACK-A-QUICK-FIX-PACK-2026-05-18.md) | Publisher session applies fixes after backup: title separator, Twitter/X replacement, mobile popup, broken-link scan |
| Lane 2 - Draft publishing relaunch | Three local dry-run packs created; authenticated WP draft inventory checked | [`DRAFT-PUBLISHING-DISCOVERY-2026-05-18.md`](DRAFT-PUBLISHING-DISCOVERY-2026-05-18.md), [`NEXT-PUBLISHING-PLAN-2026-05-18.md`](NEXT-PUBLISHING-PLAN-2026-05-18.md), and `content/drafts/2026-05-*` | Editorial cleanup, category mapping, alt-text cleanup, private admin-draft triage, then create WP drafts only |
| Lane 3 - Connector hardening | Tests and readback guard added | `scripts/notion-to-wp/tests/`, `kk_notion_to_wp.py`, `README.md` | Keep behavior small; consider `--diff` later after next successful batch |
| Lane 4 - Aurora staging | Local staging alive, but not cutover-ready | [`AURORA-STAGING-REPORT-2026-05-18.md`](AURORA-STAGING-REPORT-2026-05-18.md) | Fix desktop header/nav on `aurora/v2`, rerun six-page smoke, then decide iterate vs pivot |
| Lane 5 - Nav/IA structure | Decision pack created | [`NAV-IA-DECISION-PACK-2026-05-18.md`](NAV-IA-DECISION-PACK-2026-05-18.md) | KK decision on Work vs Projects, Speaking in nav, Newsletter as CTA, Events/Web Summit split |

## Next Batch Of Posts

Authenticated WordPress currently has 32 draft posts and 3 draft pages. That admin draft queue is old, all-Misc, empty-slug, and mostly not ready. The full title inventory is intentionally local-only because this repo is public.

These Notion/local packs are ready as local review packs, not ready for one-click publish yet:

| Priority | Draft pack | Status | Must fix before WP draft |
|---:|---|---|---|
| 1 | `content/drafts/2026-05-13-sovereign-ai-for-whom/` | Strongest candidate; 121 blocks, 6 images | Category mapping for `Feature`; hand-edit one HTML-contaminated alt string |
| 2 | `content/drafts/2026-05-16-why-we-built-the-responsible-ai-professional-certification/` | 83 blocks, 13 images | Compare against live RAP post `11620`; replace byline excerpt/meta; review slide-derived alt text |
| 3 | `content/drafts/2026-05-06-comox-valley-ai-is-becoming-its-own-thing/` | 110 blocks, no images | Replace `Draft status...` excerpt/meta; decide whether it needs a featured image |

Authenticated exact-slug checks found no WP post or draft for those three candidate slugs. They should still become WordPress drafts first, not direct publishes.

Publisher guardrails:

- Re-run `--dry-run` immediately before any live connector run.
- Do not use `--publish` unless KK explicitly approves immediate publication.
- Prefer create-only WP drafts first; review in wp-admin before publishing.
- Do not use `--update` without fresh slug, WP ID, and title-similarity verification.

## Production Fix Queue

Do these in one serialized publisher session after a fresh backup:

1. Add the `KK title separator fix` Code Snippet from the Track A quick-fix pack.
2. Run WP-CLI dry-run search-replaces for `feelmoreplants` to `x.com/kriskrug`, then apply only if counts are sane.
3. Disable the Beehiiv popup on mobile/tablet; keep desktop delay at 30 seconds.
4. Run Broken Link Checker as a one-shot scan, export CSV, then disable it.
5. Update `RESUME-HERE.md` only after the production session actually completes.

## Security Note

`RESUME-HERE.md` previously pasted a WordPress application password in tracked documentation. It has been redacted from current tracked files. On 2026-05-18 at 11:14 PT, the exposed `kk-notion-to-wp` application password and the older `MCP AI` application password were revoked, and a fresh connector credential was stored only in the gitignored local `.env`. Git history still contains the old leaked value unless a coordinated history rewrite is approved.

## Recommended Next Swarm

Use four bounded workers, not one giant free-for-all:

| Worker | Scope | Output |
|---|---|---|
| Publisher prep | Three draft packs plus private WP admin draft triage | Clean excerpts/meta/alt/category decisions, no WP writes |
| Track A publisher | Production quick fixes only | Backup proof, applied fixes, curl verification, rollback notes |
| Aurora staging | `aurora/v2` only | Rendered staging report with screenshots and cutover verdict |
| Issue hygiene 2 | GitHub issues only | Close/relabel stale `auto-implement` issues; open scoped issues for real current work |
