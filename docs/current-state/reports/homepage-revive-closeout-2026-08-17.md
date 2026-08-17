# Homepage revive closeout: 2026-08-17

**Status:** source on `main`. **Not live.** No theme SFTP. No WordPress writes.

## What shipped to `main`

| PR | Commit | What |
|---|---|---|
| #846 | `f35db91` | #745 SHELVED/REWRITE/STATUS markers + proposed A5 list. Did not cull. |
| #845 | `7347cd1` | #690 editor swatch name `Cream Elevated (same as Panel)`. Hex unchanged. |
| #844 | `17ae392` | Aurora **1.6.8** homepage stack (#411–#416). CSS ratchet 6920→7489 lines, 169→173 `!important`. |

Closed leftover remotes after the unique work was on `main` or in those PRs. Origin heads are now **`main` only**.

#745 was auto-closed by the #846 merge and **reopened**. Cull of the 14 unpublished packages still needs KK.

## Verify

- Homepage unit tests, voice-gate, css-ratchet, and docs-truth-check were green locally 2026-08-17.
- Live public `style.css` is **1.6.7** (2026-08-17 04:23 UTC). Repo is **1.6.8**.
- Homepage HTML still has the TED/SXSW name strip. No `aurora-creative-labs` / `aurora-logo-soup` / `aurora-stages-band`. 1.6.8 is not live.
- Title pipe + Krüg chrome from 1.6.7 is live (`AI Lands Inside Every Profession | Kris Krüg`; homepage `Kris Krüg | …`).
- Pixel gate is still owed before any 1.6.8 deploy. Gate 0 in the day runbook is now "deploy 1.6.8" on top of live 1.6.7.

## Left alone

- Untracked `docs/current-state/reports/visual-baseline/{diff,manifest}-20260817T035118Z.json` (issue #473 capture from another session).
- Other-session `/tmp/kriskrug-wp-*` dirs and `/Users/kk/Code/.worktrees/*`.
- 14-draft cull, 26-file #740 archive, live apply (#764/#729/#612/#706).
