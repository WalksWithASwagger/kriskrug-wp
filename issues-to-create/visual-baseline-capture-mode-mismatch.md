# [QA] visual-baseline captures render 4000px linearized instead of config viewport — pixel gate unusable

**Filed:** [#697](https://github.com/WalksWithASwagger/kriskrug-wp/issues/697) (2026-08-10)

**Labels:** bug, priority:high, tests, track-b

## Problem

The pixel gate (`make visual-baseline` / `visual-diff`) produced a 33/33 FAIL on the 2026-08-10 Aurora 1.6.0 deploy that turned out to be a capture-pipeline artifact, not a regression.

Evidence (all under `docs/current-state/reports/visual-baseline/`):

- `20260803T033115Z/png/home-desktop.png` — **4000×36762**, page renders linearized (critical CSS only, no layout)
- `20260810T043948Z/png/home-desktop.png` (pre-deploy baseline) — **4000×36322**, same linearized mode
- `20260810T054311Z/png/home-desktop.png` (post-deploy candidate) — **2880×14338**, fully styled, matches config

`capture-config.json` is byte-identical between the two 2026-08-10 runs (desktop = 1440×900 @2x → 2880 wide). The candidate honored it; both baseline runs did not. Whatever fell back to 4000px width also failed to apply the main stylesheet (Boost bundle), so baselines capture an unstyled page. Diffing an unstyled baseline against a styled candidate produced 14–89% pixel deltas across every route/viewport.

Note the Aug 3 run has the same defect, so this predates the 1.6.0 deploy and any baseline made in that mode is invalid.

## Impact

The official gate (post-deploy live vs pre-deploy live) cannot produce a trustworthy verdict until capture mode is deterministic. The 1.6.0 deploy was verified manually instead (see `diff-20260810T054311Z.json` + deploy closeout notes).

## Acceptance criteria

- Root-cause why capture runs sometimes ignore the configured viewport and render without the main CSS (suspects: resource blocklist hitting the Boost bundle, viewport override failing, deferred-CSS timing).
- Capture driver asserts output PNG width == viewport width × scale and fails loudly on mismatch.
- Capture driver asserts the main stylesheet (or Boost bundle) loaded before screenshotting.
- Re-capture a known-good baseline after the fix.
