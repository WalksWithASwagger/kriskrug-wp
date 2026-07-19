# Issue #406 — What should the marquee board actually do?

Research-only spike. 2026-07-19. No live-site, theme, or WordPress changes made.
Part of epic #403 (site redesign, Wave 1). Sibling issue #405 already moves the
board to the bottom of the homepage.

---

## Recommendation (decision-ready)

**Keep the LED board as a visual. Kill the automation behind it. Turn it into a
single, hand-picked "now showing" line that points at one real thing (a current
talk, a live essay, a thing KK is building) with a link.**

Concretely:

1. Keep `parts/marquee-current.html` and `assets/js/marquee.js`. The LED board is
   genuinely on-brand and interactive, which is exactly what #403 asks for. Move it
   to the bottom per #405.
2. Retire the weekly loop: disable `.github/workflows/marquee-weekly.yml`, and stop
   treating `scan.py` output as a content pipeline. It mines draft essays for
   abstract quote fragments, which is the opposite of "surface the good stuff."
3. Do not activate the gated Tier 3 WordPress plugin / `/marquee/` archive. The
   compounding-SEO-archive ambition was never turned on and adds maintenance drag
   for a payoff the site does not need.
4. Give the board one job: a rotating or hand-set current-focus line that links
   somewhere useful. KK edits it when there is something to say, not on a cron.

Why: the feature today is an elaborate self-improving content engine wrapped around
a single decorative McLuhan quote that has not changed since the day it shipped, and
that quote links to nothing. That is novelty over cohesion and it buries value
instead of surfacing it, both of which #403 names as the enemy. The Coupland-lineage
LED board is a real asset. The auto-quote machine around it is not.

If KK does not want to babysit even a hand-set line, the honest fallback is **kill it
entirely** (Option A). Do not keep the current auto-loop running as-is.

---

## Options

### Option A — Kill it entirely
Remove the board from the homepage, retire the workflow, plugin, and scripts.

- Pros: zero maintenance, one fewer thing that looks half-baked, simplest possible
  homepage. Nothing of value is currently live to lose.
- Cons: throws away a distinctive, on-brand visual and the Coupland lineage KK clearly
  cares about. The interactivity #403 wants disappears with it.
- Effort: low. Delete the pattern include, the workflow, and the plugin/scripts.
- Data source / refresh: none.

### Option B — Keep the visual, kill the automation (RECOMMENDED)
The LED board stays. It shows one hand-picked current line that links to a real
destination. KK sets it when there is news, not weekly.

- Pros: keeps the best part (the visual + lineage), drops the parts that never worked
  (auto-quotes, gated archive, weekly PR noise). Becomes a genuine "what KK is on
  right now" signal that points at real work, which matches "surface the good stuff."
  Low ongoing cost because there is no cadence obligation.
- Cons: needs KK to set the line by hand occasionally. Loses the (theoretical)
  passive-SEO archive, which was never live anyway.
- Effort: low to medium. Strip the workflow, simplify `marquee.json` to a single
  editable board record plus a link field, keep `build.py` -> partial. Add a link
  target (the board currently links nowhere).
- Data source / refresh: KK, by hand, via `marquee.json` -> `build.py`. No cron.

### Option C — Rebuild as a live feed (latest writing or next talk)
Auto-pull the newest published post or the next scheduled talk and render its title
on the board, linked.

- Pros: always current with no manual step, and it points at real published work
  instead of draft fragments. Doubles as a "latest" teaser.
- Cons: rebuilds most of the pipeline for a feed that other homepage sections
  (Writing page #409, Speaking #414/#419) may already cover better. Risk of
  duplicating what those sections do. Title-on-a-board can read awkwardly versus a
  crafted line.
- Effort: medium. Swap `scan.py` for a WP REST pull of the latest post/talk, keep
  `build.py` and the partial. Wire the link.
- Data source / refresh: WordPress REST (latest `post`) or a talks source, refreshed
  on a schedule or on publish.

---

## Evidence (what the board is today)

Verified against the actual code, not from memory. Key paths:

- **Homepage placement.** `theme/kk-aurora/templates/front-page.html:6` includes
  `wp:pattern {"slug":"kk-aurora/marquee-hero"}` near the top of the page. #405
  moves it to the bottom.
- **Render wrapper.** `theme/kk-aurora/patterns/marquee-hero.php` is a thin wrapper
  that `file_get_contents()` the generated partial.
- **Live board markup.** `theme/kk-aurora/parts/marquee-current.html` is generated,
  pre-rendered, self-styled (scoped Aurora tokens), and shows **"THE MODEL / IS THE /
  MESSAGE"**. It links to nothing. `data-skin="led"` (dot-matrix); 3 other skins
  (`splitflap`, `letterpress`, `teletype`) exist but are unused.
- **Data source of truth.** `content/marquee/marquee.json` holds `meta`, `boards[]`
  (live + archived), and curated `candidates[]`. The single live board is the McLuhan
  seed, `date: 2026-06-26`. It has not rotated since it shipped.
- **The loop.** `scripts/marquee/` = `scan.py` (mines `content/drafts/*/post.md` for
  short declarative lines and scores them) -> curate by hand into `candidates[]` ->
  `promote.py` (pick becomes live, old board archived) -> `build.py` (renders partial
  + `/marquee/` archive). `content/marquee/README.md` documents the full design.
- **Weekly automation.** `.github/workflows/marquee-weekly.yml` runs Mondays 15:00 UTC,
  scans drafts, and opens a **draft PR** with 2-8 candidates for KK to pick. Output of
  the last scan lives in `content/marquee/proposals.json` (8 candidates, all abstract
  fragments pulled from draft essays, e.g. "THE LEARNED / PARAMETERS / INSIDE A MODEL",
  "WE'RE A / NONPROFIT", "LLMS ARE TRAINED / ON WHAT EXISTS").
- **Gated WordPress serving (never activated).** `plugins/kk-marquee-board/` ships a
  `marquee_board` CPT, meta, Article schema, CSS/JS, a smoke test, and
  `DEPLOYMENT.md`. `make marquee-package` packages it for wp-admin upload.
  `scripts/marquee/sync.py` + `wp_sync.py` push boards to WP over REST. Theme templates
  `single-marquee_board.html` and `archive-marquee_board.html` exist. Per
  `content/marquee/README.md` and `docs/current-state/MARQUEE-CLOSEOUT-2026-06-26.md`,
  Tier 3 go-live is **gated on KK** and has not happened: `/marquee/` is not serving in
  production.
- **Build history.** 6 marquee commits between 2026-06-26 and 2026-06-28 (v1 -> Tier 3),
  then nothing. PRs #257, #259, #260, #263 merged in that window. No promoted board
  since the seed.

### Fact vs inference

- **Fact:** the board shows one static McLuhan quote, links nowhere, has not rotated
  since 2026-06-26; the weekly Action exists; the WP plugin and `/marquee/` archive are
  built but not live; `scan.py` sources abstract lines from draft essays.
- **Inference / judgment:** that the auto-quote loop adds little value, that the visual
  is worth keeping, and that Option B best fits #403. This is a recommendation, not a
  measured result. No analytics on marquee engagement were available in-repo, so the
  "unclear value" read is qualitative, grounded in #403's stated principles.

### KK teardown quote (issue #406)

> It looks like a concept that was half-baked and not rolled out. You can pull out the
> roadmap there and do some research and come up with ways to make it more awesome.

The half-baked read is accurate: the ambitious half (WP-native archive, weekly rotation)
was built but never switched on, leaving a decorative quote at the top of the homepage.

---

## Approval gates / next routing

- This doc is draft-only. No workflow, theme, plugin, or live-site change was made.
- If KK picks Option B, next step is a scoped implementation issue: strip the workflow,
  add a link field to the board record, set the first hand-picked line, coordinate with
  #405 (placement). Keep content edits and theme edits in separate PRs per the README's
  lane note.
- Note for #406 acceptance criteria: that issue asks for the doc at
  `docs/proposals/marquee-board-2026-07.md`. This spike was routed to
  `docs/current-state/reports/`. If the issue path is required, copy or move before
  closing #406.
