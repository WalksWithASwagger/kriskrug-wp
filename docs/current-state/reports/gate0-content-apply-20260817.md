# Gate 0 content apply receipt — 2026-08-17

**Status:** live. Posts 12327, 12032, 12732, and 12034 updated. Logged-out cache-busted HTML matches REST.
**Track:** Track A. Snapshot-first. Content field only.
**KK go:** "good job. proceed" after Aurora 1.6.8, against WORK-PLAN-2026-08-17 Gate 0 items 2–4.

#706 WPCode Lite and #731 Boost regen were not this pass. `Eth??s Lab` on 12327 was left as-is (own NCR pass).

## #764 — posts 12327 + 12032

Script: `python3 scripts/apply_issue_764_fix.py --apply` under Varlock.

| ID | Slug | What changed | REST after |
|---|---|---|---|
| 12327 | `storyhive-haus-of-owl-jordan-dack` | 21 U+2014 in `content.rendered` → 0 | `modified_gmt` 2026-08-17T05:03:50 |
| 12032 | `what-would-chat-do-and-why-thats-the-wrong-question` | `?p=11876` → `/2026/06/17/storyhive-haus-of-owl-jordan-dack/` | `modified_gmt` 2026-08-17T05:03:47 |

Public HTML (`?cb=`): both 200 MISS, 12327 entry-content em dash 0, 12032 `?p=11876` 0.

Snapshots: `backup/issue-764-em-dash-404/rest-post-{12032,12327}-before-20260817T050342Z.json`.

Rollback:

```bash
make varlock-run CMD='python3 scripts/apply_issue_764_fix.py --restore backup/issue-764-em-dash-404/rest-post-12327-before-20260817T050342Z.json --apply'
make varlock-run CMD='python3 scripts/apply_issue_764_fix.py --restore backup/issue-764-em-dash-404/rest-post-12032-before-20260817T050342Z.json --apply'
```

## #729 — post 12732

Exact find/replace from `content/drafts/2026-07-26-futureproof-festival-announcement/fix-729/PAYLOAD.md`. Each FIND matched once in `content.raw`. Identity: id 12732, slug `futureproof-festival-announcement`.

Public HTML: `August 15, 2026` 0, `August 31, 2026` 1, "submissions for this round have closed" present, body em dash 0. `modified_gmt` 2026-08-17T05:05:22.

Snapshot: `backup/20260817T050520Z-12732-futureproof-729/rest-post-12732-before.json`.

## #612 — post 12034

Payload: `content/drafts/2026-08-01-zero-to-one-voice-rewrite/proposed-content-raw.html` (PR #803). Live `content.raw` still matched the 2026-08-01 snapshot hash `01541a3de9df42e0…` before write. Identity: id 12034, slug `zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey`, title starts `Zero to One`. Payload had 0 chars above U+00FF.

Public HTML: `I opened my studio doors` 1, `Kris Krüg opened the doors` 0, `As Krüg stated` 0, `130 paid members` 0, `$240` 0, `$340/year` present, `300 members` present, body em dash 0. `modified_gmt` 2026-08-17T05:05:29.

Snapshot: `backup/20260817T050528Z-12034-zero-to-one-612/rest-post-12034-before.json`.
