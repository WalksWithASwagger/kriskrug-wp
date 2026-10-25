# Current State Snapshot - 2026-10-25

**Snapshot:** Sunday, October 25, 2026, after Events PR #1134 merged and its
approved page update was verified. This is the declared drift baseline, not a
promise that counters remain unchanged. Run `make status-readonly` for current
observations. Supersedes [September 21](CURRENT-STATE-2026-09-21.md).

## Verified state

- Open PRs: `0` after #1134 merged, before this handoff PR.
- Open issues: `41`.
- Production still publicly reports WordPress `7.0.7`.
- WordPress draft queue: `0` scheduled posts, `68` draft posts, `4` draft pages.
- Public Aurora `style.css`: `1.6.12`. Fetched `origin/main`: `1.6.13`.
  The approved image-only repair does not deploy all of 1.6.13 or change the
  version header. Compare exact release hunks and live owners as well as versions.
- Canonical main after #1134: `16fc6742948e1889573894820e232568bf55cc97`.
- The original working checkout remains on `codex/local-checkpoint-2026-10-02`,
  with its local documentation commit and untracked content packages preserved.
  A match between that older checkout's header and production is not main parity.
- `/projects/` redirects to `/work/`. Homepage, Events, Work, Speaking, Services
  and Contact returned 200 during the October 25 public checks.

## Completed and remaining work

1. **Events #1134:** merged after required CI. Page 2250 was applied with explicit
   approval, verified identity, source hash, private snapshot and exact stored
   readback. Normal and uncached public requests show Futureproof, Prompt Victoria
   and AMPA in Next up. September's spotlight is gone; Get tickets uses the direct
   festival ticket URL. All 74 live event identities and evergreen content remain.
2. **Homepage image #1114 / #1118:** the existing image-only approval was used.
   Trusted SFTP and the database homepage override were verified. Only the packaged
   artwork, source/dimension hunks and Work share-image fallback were applied.
   Kris accepted the repaired artwork and the baseline was re-frozen explicitly.
   Homepage and Work share-image changes are verified on normal public URLs.
3. **Schema #1089:** the approved 14,765-byte candidate is unchanged. A fresh
   private source snapshot confirms active global Snippet 5, KK Schema, as the sole
   schema emitter. The prepared Person/VideoObject changes are still not live.
   KK's save remains the next action; do not reopen the September approval or add
   the separate YouTube identity choice.
4. **Sitemap #1130 / #331:** public index has 986 post and 46 page entries, no
   taxonomy/author children. Three existing archive samples emit noindex,follow.
   The September 3 deployment receipt already records the chosen archive policy.
   Reconcile the old checklist with that receipt; no new archive changes were made.
5. **Homepage/footer copy and links:** separately approved and applied October 25.
   Homepage names Vancouver, October 28–30, 2026; footer YouTube and the Services/
   Futureproof destinations are corrected. Full visual comparison: 33 PASS.
   Uncached delivery is verified; consult the receipt for shared-cache state.
6. **Reserve:** ALL IN navigation is prepared in draft PR #1141 for editorial
   review, without publication. Work body artwork still uses its previous
   reference; the approved image change covered its social-image fallback.

## Operating references

- [September 9 live-lane procedures](WORK-PLAN-2026-09-09.md), retained for their
  identity, snapshot and approval requirements, not as today's issue queue.
- [Two-track model](TWO-TRACK-MODEL.md): separate content, theme and ops changes.
- [Runtime reference](AGENT-RUNTIME-REFERENCE.md) and `.env.schema`: Varlock and
  existing trusted access; no plaintext secret reads.
- [October 25 release receipt](reports/site-readiness-20261025.md).

`check-live-parity` now names the Git ref it compares and defaults to the locally
fetched `origin/main`. It performs no fetch. Use `--ref HEAD` for an explicit
checkout comparison. Startup reports compare `origin/main...HEAD`, no longer
query the retired `origin/aurora/v2`, and inspect the current `/work/` route.
WordPress's expected version is 7.0.7; unrelated smoke failures remain visible.

Auto-Triage Issues and Marquee Weekly Scan remain disabled. This handoff does not
enable them, publish drafts, modify analytics, or authorize another live release.
