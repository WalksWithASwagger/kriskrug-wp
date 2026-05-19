# Aurora v2 — Next Session Playbook

**Branch:** `aurora/v2` (commit `daf5f31` — feat: aurora/v2)
**Status:** Theme + demo cherry-picked from the stale rebuild branch onto current `main`. Track A (connector, audits, fixes, backup) verified intact. Nothing installed or deployed yet.

**2026-05-18 update:** A first visual redesign implementation now exists on `codex/aurora-redesign-2026-05-18`. Start with `AURORA-REDESIGN-SMOKE-2026-05-18.md` for the current preview state, screenshot artifacts, Local backup paths, and remaining review items. Use `AURORA-TOMORROW-ROADMAP-2026-05-19.md` to guide the next review and implementation session.

---

## Where to pick up

```bash
cd /Users/kk/code/kriskrug-wp
git checkout aurora/v2
git log --oneline -3
```

You should see:
- `daf5f31 feat: aurora/v2 — bring kk-aurora theme + demo onto current main`
- `<sha>   docs: aurora v2 next-session playbook` (this doc)
- `8f3fa3b docs: two-track operating model + reader-facing site audit`

Theme lives at `theme/kk-aurora/` (21 files). Installable zip at `theme/kk-aurora.zip` (48K). Browser preview at `demo/index.html`.

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

## First 30-minute smoke test (next session)

1. **Install the theme.** Upload `theme/kk-aurora.zip` via Appearance → Themes → Add New → Upload Theme. Activate.
2. **Seed minimal content.** Import or hand-create:
   - A homepage (set as static front page)
   - An About page
   - Two posts pasted from production:
     - `/2026/05/15/your-taste-is-your-moat/`
     - `/2026/05/16/make-culture-not-content/`
3. **Visit each URL and screenshot.** Save screenshots to `docs/current-state/aurora-smoke-2026-MM-DD/`:
   - `/` (home)
   - `/about/`
   - `/2026/05/15/your-taste-is-your-moat/`
   - `/2026/05/16/make-culture-not-content/`
4. **Open `demo/index.html` in a browser side-by-side.** Compare. The live theme should match the demo's vibe — gradients, typography, animations. Flag any drift.
5. **Check the console for JS errors.** `aurora-animations.js` and `micro-interactions.js` should load clean.

## What NOT to do next session

- Don't point production DNS at the new theme
- Don't run the Notion→WP connector against the staging install (that's Track A and assumes the prod theme)
- Don't rebase or merge `aurora/v2` into `main` until smoke + iteration are done
- Don't push `aurora/v2` to `origin` yet — leave that for KK (`git push -u origin aurora/v2`)

## When to merge back

After smoke test passes, after KK has reviewed the live theme on staging, after any iteration commits are squashed/cleaned. Then PR `aurora/v2` → `main` (or whatever swap-over strategy AURORA-MIGRATION-PLAN.md prescribes for going live).
