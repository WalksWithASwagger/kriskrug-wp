# Voice Audit Blog Sweep — Swarm Issue Board

**Status:** Filed on WalksWithASwagger/kriskrug-wp (#603–#616)  
**Source audit:** [`content/drafts/voice-audit-blog-sweep-2026-08-01/00-summary.md`](../../content/drafts/voice-audit-blog-sweep-2026-08-01/00-summary.md) (commit `c93c5b5`)
**Skill loop:** snapshot-first `wp-live-edit` on kriskrug.co (Track A only)  
**Out of scope forever for this swarm:** Track B theme edits, Aurora CSS, homepage, unrelated drafts

## Wave diagram

```
Wave 1 (parallel — exclusive WP post IDs, zero content overlap):
  VOICE-1 canada memo trim (12030) ────────┐
  VOICE-2 chat-do prep+en-dash+umlaut (12032)┤
  VOICE-3 Ethọ́s encoding+title (12357/12363) ┼──► Wave 2 projects
  VOICE-4 god-skills tables (12263) ────────┤
  VOICE-5 ai-lands em dashes (12653) ───────┤
  VOICE-6 media umlaut+Kharé (11879) ───────┤
  VOICE-7 i-am-nomad close line (12612) ────┘

Wave 2 (parallel after Wave 1; bigger / decision-gated):
  VOICE-8 zero-to-one first-person rewrite (12034)  [needs-human-review before --apply]
  VOICE-9 artists-learn reveal de-template (12473)
  VOICE-10 Futureproof naming decision + align     [needs-decision]
  VOICE-11 membership price/count reconciliation   [needs-decision]

Wave 3 (parallel anytime — different repo):
  VOICE-12 kk-voice anti-glossary checker-gap regexes
```

## Exclusive ownership (no overlap)

| Issue | Owns (write) | Must not touch |
|-------|--------------|----------------|
| VOICE-1 | live post **12030** only | any other post |
| VOICE-2 | live post **12032** only | any other post |
| VOICE-3 | live posts **12357** + **12363** only | prose rewrites beyond Ethọ́s/title |
| VOICE-4 | live post **12263** only | reveal-density thinning (optional later) |
| VOICE-5 | live post **12653** only | other July posts |
| VOICE-6 | live post **11879** only | |
| VOICE-7 | live post **12612** only | |
| VOICE-8 | live post **12034** (+ draft under `content/drafts/…`) | cert post body except shared number decision via VOICE-11 |
| VOICE-9 | live post **12473** only | |
| VOICE-10 | naming decision + glossary note + listed posts' festival spelling | unrelated voice edits |
| VOICE-11 | reconcile numbers on **12034** and **12257** after KK picks truth | full rewrites |
| VOICE-12 | `~/Code/kk-voice/anti-glossary.md` (+ tests if present) | kriskrug-wp live posts |

## Shared hard rules (every live issue)

1. **Track A only.** No theme / FSE / `theme/kk-aurora/` edits.
2. **Snapshot before mutate.** REST `context=edit` → `backup/20260801-voice-sweep/<slug>/` before/after + rollback JSON.
3. **Dry-run first.** Comment the exact cut/diff on the issue. `--apply` only when acceptance anchors match.
4. **One post ID per agent** (VOICE-3 may do its two Ethọ́s posts serially in one issue).
5. **Re-verify:** cache-bypass `curl` of the live URL + `voicecheck.py` on the changed plain text.
6. **Do not** "improve" surrounding prose, SEO, or images unless the issue explicitly lists it.
7. Ground truth and verified rewrites live in `content/drafts/voice-audit-blog-sweep-2026-08-01/readings/` and `snapshots/`.

## Issue titles to file

1. `[EPIC] Voice sweep fixes — 15-post Dark Crystal audit (2026-08-01)`
2. `[swarm][voice-w1] Trim leaked strategy memo from Canada AI Machine post (12030)`
3. `[swarm][voice-w1] Trim prep notes + fix en-dashes/umlaut on What Would Chat Do (12032)`
4. `[swarm][voice-w1] Fix Ethọ́s mojibake + canonical title (12357, 12363)`
5. `[swarm][voice-w1] Rebuild broken markdown tables on God Skills post (12263)`
6. `[swarm][voice-w1] Strip 26 em dashes from AI Lands post (12653)`
7. `[swarm][voice-w1] Fix Kris Krüg umlaut + Kharé spelling on media appearances (11879)`
8. `[swarm][voice-w1] Fix I Am Nomad closing-line premise inversion (12612)`
9. `[swarm][voice-w2] Rewrite Zero to One into first person (12034)`
10. `[swarm][voice-w2] De-template reveal cadence on Artists Learn (12473)`
11. `[swarm][voice-w2] Decide Futureproof festival spelling and align posts`
12. `[swarm][voice-w2] Reconcile BC + AI membership price/count across two posts`
13. `[swarm][voice-w3] Add voice-sweep checker-gap regexes to kk-voice anti-glossary`

## Filed issue numbers

| Key | Issue |
|-----|-------|
| EPIC | [#603](https://github.com/WalksWithASwagger/kriskrug-wp/issues/603) |
| VOICE-1 canada memo | [#604](https://github.com/WalksWithASwagger/kriskrug-wp/issues/604) |
| VOICE-2 chat-do prep/en-dash | [#605](https://github.com/WalksWithASwagger/kriskrug-wp/issues/605) |
| VOICE-3 Ethọ́s encoding | [#606](https://github.com/WalksWithASwagger/kriskrug-wp/issues/606) |
| VOICE-4 god-skills tables | [#608](https://github.com/WalksWithASwagger/kriskrug-wp/issues/608) |
| VOICE-5 ai-lands em dashes | [#609](https://github.com/WalksWithASwagger/kriskrug-wp/issues/609) |
| VOICE-6 media umlaut/Kharé | [#610](https://github.com/WalksWithASwagger/kriskrug-wp/issues/610) |
| VOICE-7 i-am-nomad close | [#611](https://github.com/WalksWithASwagger/kriskrug-wp/issues/611) |
| VOICE-8 zero-to-one rewrite | [#612](https://github.com/WalksWithASwagger/kriskrug-wp/issues/612) |
| VOICE-9 artists-learn reveal | [#613](https://github.com/WalksWithASwagger/kriskrug-wp/issues/613) |
| VOICE-10 Futureproof naming | [#614](https://github.com/WalksWithASwagger/kriskrug-wp/issues/614) |
| VOICE-11 membership numbers | [#615](https://github.com/WalksWithASwagger/kriskrug-wp/issues/615) |
| VOICE-12 anti-glossary gaps | [#616](https://github.com/WalksWithASwagger/kriskrug-wp/issues/616) |

Note: GitHub issue #607 was not part of this batch (number skipped by the API).
