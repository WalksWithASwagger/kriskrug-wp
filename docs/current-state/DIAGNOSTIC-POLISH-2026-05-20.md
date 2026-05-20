# Diagnostic and Polish Pass - 2026-05-20

**Purpose:** Implement the repo-truth, technical-debt, SOTA, and polish plan from the 2026-05-20 diagnostic session without touching live WordPress.
**Snapshot time:** 2026-05-20 17:30 UTC.
**Track:** Ops / docs / plugin hardening on `main`. No Track B theme files and no production WordPress content were changed.

## Verified state

- `main` is synced with `origin/main` (`0 0` divergence).
- Open PRs: `0`.
- Open issues: `63`.
- Open `track-b` + `aurora-v2` issues: `13`, with `#86` still the final real-staging QA gate.
- `origin/aurora/v2` is `18` ahead and `69` behind `origin/main`.
- Live site is still Catch Responsive. Aurora remains isolated Track B work.
- Live `/llms.txt` returns `404`.
- Live `/robots.txt` returns `200`, but still uses the current default sitemap/admin rules rather than an explicit AI-crawler stance.
- Live homepage still has two `<h1>` elements and multiple empty image alts.
- Live `/work/` resolves to `/recent-projects-include/` and still emits a blank WordPress.com OG image.
- Public HTML on homepage, About, Work, and Speaking includes JSON-LD scripts, so schema appears to be deployed via the Code Snippets path. Verify in wp-admin before editing or redeploying schema.

## State of affairs and trajectory

The codebase is cohesive in narrative direction: kriskrug.co is becoming the hub for Kris's creative AI, community-building, speaking, and field-work identity. Recent work has strengthened the About, Work, Speaking, homepage, source-pack, and owned-sites spine.

The risk is not lack of direction. The risk is operational drift:

- Repo docs, live WordPress, queued fixes, GitHub workflows, agent-state files, and Aurora branches were not all telling the same story.
- The repo previously described one custom WP module, but it now also includes the `kk-sidebar-promos` plugin.
- The repo described the old agent workflow as dormant, but `agent-pr-generator.yml` was still triggered by issue labels and could commit placeholder state.
- The fix queue still treated schema as fully queued even though public pages now appear to include the deployed schema snippet.

## Technical debt addressed in this pass

- Parked the placeholder Agent PR Generator so `auto-implement` labels no longer trigger misleading comments, state commits, pushes, or simulated automation.
- Updated agent-facing docs to say the old swarm is historical, while PR validation remains active and the generator workflow is now a manual read-only diagnostic stub.
- Reconciled live-state notes for schema, `/llms.txt`, robots, homepage H1/alt text, and Work OG/slug drift.
- Hardened `kk-sidebar-promos` rendering so featured images prefer the attachment alt text and fall back to decorative empty alt rather than repeating the visible promo title.
- Added a local smoke test for `kk-sidebar-promos` covering empty render behavior, image alt behavior, featured-promo expiry behavior, and Luma iCal parsing.

## SOTA direction

The site should keep moving toward native platform polish, editorial proof, measurable performance, and accessible motion:

- Prefer native progressive animation patterns where they fit: `https://developer.chrome.com/docs/web-platform/view-transitions/cross-document`, `https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API`, and `https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_scroll-driven_animations`.
- Treat Core Web Vitals as design constraints, especially INP, LCP, and CLS: `https://web.dev/articles/inp`, `https://web.dev/articles/lcp`, `https://web.dev/articles/cls`.
- Keep Aurora WordPress-native: block theme architecture and `theme.json` first, Interactivity API only for small stateful UI.
- Use WCAG 2.2 as the floor for focus visibility, target size, contrast, predictable navigation, and reduced-motion handling.
- Let real proof do the aesthetic work: talks, videos, field notes, event communities, project outcomes, and warm editorial linking should carry more weight than decorative effects.

## Interface polish and QoL backlog

Do these only after the backup gate is proven:

- Replace hard-coded sidebar image blocks with `kk-sidebar-promos` after a plugin deploy check and rollback path.
- Fix the homepage duplicate/empty H1 and the highest-visibility empty image alts.
- Add `/llms.txt` and choose the robots AI-crawler stance.
- Fix Work page public identity: slug/canonical/OG image should say "Work", not only `recent-projects-include`.
- Add event-card states: upcoming, recently passed, recording available, sold out when relevant.
- Add a small "currently gathering next" or "in the field now" module that reflects Kris's live community-building work.
- Add proof metadata to Work cards: year, role, community, artifact, outcome.
- Keep Aurora motion meaningful: page transition, section reveal, reading progress, and proof-card affordance. Remove decorative JS unless it survives reduced-motion and INP testing.

## Today's implemented checklist

- [x] Refresh repo truth around issue counts, Aurora divergence, schema status, and plugin status.
- [x] Stop the placeholder Agent PR Generator from auto-triggering on issue labels.
- [x] Document that live WordPress writes remain blocked behind backup/restore proof.
- [x] Audit `fixes/` against current live state at the queue level.
- [x] Add focused `kk-sidebar-promos` smoke coverage.
- [x] Fix sidebar promo image alt behavior.
- [ ] Complete real-staging Aurora QA for issue `#86`. Blocked until the staging surface with production-like media is available in this session.
- [ ] Prune Aurora theme motion code. Deferred because Track B theme files live off `main` and should be handled in the Aurora worktree/branch.
