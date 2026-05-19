# Aurora v2 - Next Session Playbook

**Branch:** `aurora/v2`
**Current base:** `88da99a` - merged PR `#93` after the first Aurora review PR `#87`
**Status:** Aurora v2 is active in Local only for review/smoke work. Track A content, connector, backup, and SEO work stay on `main`.

**2026-05-18 update:** A first visual redesign implementation now exists on `codex/aurora-redesign-2026-05-18`. Start with `AURORA-REDESIGN-SMOKE-2026-05-18.md` for the current preview state, screenshot artifacts, Local backup paths, and remaining review items. Use `AURORA-TOMORROW-ROADMAP-2026-05-19.md` to guide the next review and implementation session.

**2026-05-19 P0 update:** PR `#87` merged the first reviewable redesign into `aurora/v2`, then PR `#93` merged the first swarm-wave header and visual-system work. The follow-up branch `codex/aurora-p0-staging-rescue-2026-05-19` addresses issue `#80` by tightening the remaining mobile header/nav behavior, refreshing screenshots, and rerunning Local smoke. Start with `AURORA-P0-STAGING-RESCUE-2026-05-19.md` before opening new Aurora work.

---

## Where to pick up

```bash
cd /Users/kk/Code/kriskrug-wp
git fetch --prune origin
git worktree add ../kriskrug-wp-aurora-next origin/aurora/v2 -b codex/aurora-next-YYYY-MM-DD
git log --oneline -3
```

Expected recent history includes PR `#93` and PR `#87` merged into `aurora/v2`.

Theme lives at `theme/kk-aurora/`. Installable zip lives at `theme/kk-aurora.zip`. Browser preview lives at `demo/index.html`.

## Background reading (in this order)

1. `docs/current-state/TWO-TRACK-MODEL.md` — why Aurora is Track B, separate from content/SEO work.
2. `docs/current-state/AURORA-MIGRATION-PLAN.md` — the full migration plan (this is the canonical "what we're trying to do").
3. `theme/kk-aurora/IMPLEMENTATION-PLAN.md` — design spec the theme was built against.
4. `THEME-PROPOSALS.md` — design proposals it came out of.
5. `.claude/context/kris-krug-verified-facts.md` — facts KB so copy on the new theme doesn't hallucinate.

## What KK should pre-confirm before next session

Pick ONE staging path and have it ready:

**Path A — Cloudways dev box (24.144.80.107)**
- [ ] SSH creds in 1Password or shared somewhere the next agent can be given them
- [ ] Confirm there's a dev/staging WP install (or that it's OK to spin one up)
- [ ] DB credentials for that install
- [ ] Confirm the dev box isn't being used for anything else right now

**Path B — Local by Flywheel (recommended for speed)**
- [ ] Local by Flywheel installed on this Mac
- [ ] A blank WP site spun up (any name — "aurora-test" works)
- [ ] Admin login captured

Either path is fine. Local is faster to iterate and has zero blast radius. Cloudways is closer to production but slower and riskier.

## First smoke test for a fresh branch

1. Confirm Local WP is running and `kk-aurora` is active.
2. If using `http://localhost:10003`, temporarily switch local `home` and `siteurl` to that host for same-origin asset QA, then restore them to `http://kriskrug-local.local` before closeout.
3. Visit each URL and screenshot. Save screenshots to `docs/current-state/aurora-smoke-2026-MM-DD/`:
   - `/` (home)
   - `/about/`
   - `/speaking/`
   - `/recent-projects-include/`
   - `/2026/05/15/your-taste-is-your-moat/`
   - `/2026/05/16/make-culture-not-content/`
   - `/2026/05/14/calling-us-all-in/`
   - `/2026/05/07/web-summit-vancouver-2026/`
4. Check focus-visible state, reduced-motion state, and horizontal overflow at desktop, tablet, mobile, and narrow phone widths.
5. Check the console for JS errors. `aurora-animations.js` and `micro-interactions.js` should load clean.

## What NOT to do next session

- Don't point production DNS at the new theme
- Don't run the Notion→WP connector against the staging install (that's Track A and assumes the prod theme)
- Don't rebase or merge `aurora/v2` into `main` until smoke + iteration are done
- Don't do Track A content edits from an Aurora branch.

## When to merge back

After smoke test passes, after KK has reviewed the live theme on staging, after any iteration commits are squashed/cleaned. Then PR `aurora/v2` -> `main` or follow the swap-over strategy in `AURORA-MIGRATION-PLAN.md`.
