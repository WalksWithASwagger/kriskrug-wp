# Current State Snapshot - 2026-07-09

**Snapshot time:** 2026-07-09 (from 2026-07-08 Cursor Cloud audit + live `gh` / public WP probes).  
**Branch context:** `main` plus open draft PR stack #308–#313.  
**Mode:** Track A docs/code hygiene; no live WordPress write authorized by this snapshot.

This file is the **declared** input for `make current-state-drift-check` / `make morning-truth` / `make status-readonly`. It replaces `CURRENT-STATE-2026-06-23.md` and the stale count block in `WORK-PLAN-2026-05-23.md` for drift purposes. Keep those older files as historical.

## Verified State

- Open PRs: `6`.
- Open issues: `29`.
- Open `priority:high` issues: `14`.
- Open `track-b` issues: `4`.
- Open `aurora-v2` issues: `2`.
- Open `swarm-ready` issues: `6`.
- Open `swarm-parked` issues: `1`.
- Open `needs-human-review` issues: `9`.
- Open `agent-safe` issues: `8`.
- Production still publicly reports WordPress `6.9.4`.
- Live theme: `kk-aurora` **1.3.36** (public `style.css` Version header).
- WordPress draft queue: `0` scheduled posts, `64` draft posts, `4` draft pages.
  - Counts above are the last **authenticated** read (morning-truth 2026-07-03). Unauthenticated startup reads still report `0/0/0` until `.env` exists and/or PR #309 lands — that zero is a **false zero**, not an empty queue (#303).
- Local draft packages (local-only audit 2026-07-08): ~65 packages — 5 strong / 25 needs media-tax / 30 thin / 5 empty-admin.
- WP public smoke: 0 failures; OG/Twitter warnings on `/`, `/speaking/`, `/work/`.
- `/accessibility/` still 404; statement packet drafted in PR #311.
- `/projects/` → 301 `/work/`.
- GSAP/ScrollTrigger CDN: absent. Homepage reveal safety net: absent.
- `make verify`: green on current tooling (Notion publisher tests + root script tests + PHPCS + docs-truth).

## Open PR stack (review order)

1. #308 Work visual-card ship (#302)
2. #309 WP auth client consolidation (#306 / #303)
3. #310 Cursor Cloud AGENTS notes
4. #311 a11y / hub-link / About planning packets
5. #312 `publish_common` refactor (#254)
6. #313 audit workplan

## Active plan

[`AUDIT-WORKPLAN-2026-07-09.md`](AUDIT-WORKPLAN-2026-07-09.md) — Phase 0 secrets (KK tonight), Phase 1 merge stack, then one Track A content packet.

## Explicitly not authorized

No production WordPress create/update/publish/schedule from this snapshot. Docs/code hygiene only until KK returns with WP/Notion auth and a packet pick (3A/3B/3C/3D).
