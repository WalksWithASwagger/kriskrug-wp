# Current State Snapshot - 2026-10-25

**Snapshot:** Sunday, October 25, 2026, refreshed after the approved November
meetup and ALL IN page update at 2026-10-26 05:15 UTC. This is the declared drift baseline, not a
promise that counters remain unchanged. Run `make status-readonly` for current
observations. Supersedes [September 21](CURRENT-STATE-2026-09-21.md).

## Verified state

- Open PRs: `0` at the 05:10 UTC startup check, before this release-receipt PR.
- Open issues: `28` at the same startup check.
- Production still publicly reports WordPress `7.0.7`.
- WordPress draft queue: `0` scheduled posts, `68` draft posts, `4` draft pages.
- Public Aurora `style.css`: `1.6.12`. Fetched `origin/main`: `1.6.13`.
  The approved image-only repair does not deploy all of 1.6.13 or change the
  version header. Compare exact release hunks and live owners as well as versions.
- Canonical main before this release: `a13ec6fc754ce14ffb4bcba241f61ad25f9fdb45`.
  Use the release PR and a fresh GitHub readback for its eventual merge SHA.
- The original working checkout remains on `codex/local-checkpoint-2026-10-02`,
  with its local documentation commit and untracked content packages preserved.
  A match between that older checkout's header and production is not main parity.
- `/projects/` redirects to `/work/`. Homepage, Events, Work, Speaking, Services
  and Contact returned 200 during the October 25 public checks.

## Completed and remaining work

1. **Events #1134:** merged after required CI. Page 2250 was applied with explicit
   approval, verified identity, source hash, private snapshot and exact stored
   readback. Normal and uncached public requests show Futureproof, Prompt Victoria,
   AMPA and the approved November 25 meetup in Next up. September's spotlight is
   gone; Get tickets uses the direct festival ticket URL. The [November/ALL IN
   release](reports/events-november-allin-release-2026-10-25.md) preserves all 74
   prior identities and 43 images, and adds two entries: 76 IDs, 72 past rooms,
   33 meetup editions, 39 frames, four upcoming cards and 13 documentation links.
2. **Homepage image #1114 / #1118:** the existing image-only approval was used.
   Trusted SFTP and the database homepage override were verified. Only the packaged
   artwork, source/dimension hunks and Work share-image fallback were applied.
   Kris accepted the repaired artwork and the baseline was re-frozen explicitly.
   Homepage and Work share-image changes are verified on normal public URLs.
3. **Schema #1089:** saved through Varlock with explicit approval. The
   [release receipt](reports/schema-1089-release-2026-10-25.md) verifies the
   Person and Speaking VideoObjects, authenticated readback, normal warm-cache
   delivery and zero validator errors/warnings. No additional KK save is pending.
4. **Sitemap #1130 / #331:** public index has 986 post and 46 page entries, no
   taxonomy/author children. Three existing archive samples emit noindex,follow.
   The September 3 deployment receipt already records the chosen archive policy.
   Reconcile the old checklist with that receipt; no new archive changes were made.
5. **Homepage/footer copy and links:** separately approved and applied October 25.
   Homepage names Vancouver, October 28–30, 2026; footer YouTube and the Services/
   Futureproof destinations are corrected. Full visual comparison: 33 PASS.
   At 19:45 UTC all six normal and uncached routes deliver the approved links.
   The earlier stale shared caches expired naturally; no manual purge is claimed.
6. **Work, Subscribe and Publications:** [Work card readability and KRÜG
   subscription routing](reports/work-subscribe-release-2026-10-25.md) and
   [Publications overflow](reports/publications-layout-release-2026-10-25.md)
   are repaired and live. Do not repeat the earlier artwork task.
7. **Conversions and maintenance:** completed-signup measurement is installed;
   #1090's six-hour monitor awaits the first genuine signup plus GA4 delivery.
   The weekly Events proposal monitor is active and recognizes the November/ALL
   IN release. #1102's instant event-intake integration remains unimplemented.
8. **Remaining owner inputs:** practice publication and genuine participant
   evidence, editorial choices, approved favicon/imagery, unconfirmed event
   roles, and the existing policy/Contact/interaction decisions. See the
   [follow-through receipt](reports/kriskrug-futureproof-followthrough-2026-10-25.md).

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
