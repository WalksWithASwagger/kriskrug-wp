# Voice-sweep epic #603 remainder: 2026-08-16

**Issue:** [#603](https://github.com/WalksWithASwagger/kriskrug-wp/issues/603) `[EPIC] Voice sweep fixes: 15-post Dark Crystal audit (2026-08-01)`
**Lane:** Track A, verify-first. **Read-only against the live site.** No REST PATCH, no issue close, no theme deploy.
**Fetched:** 2026-08-16 19:40–19:50 PDT / 2026-08-17 02:40–02:50Z, logged out. Public REST `content.rendered` plus cache-busted HTML (`?cb=`).
**Repo:** `origin/main` at report commit. Live WordPress is independent of theme SHA. This report is the only write.
**Parallel same-evening 15-post table:** draft [PR #822](https://github.com/WalksWithASwagger/kriskrug-wp/pull/822). This file is the close-gate remainder packet (children + #612 + #764), not a second full-audit table.

Em dashes are written `{EMDASH}` in this file so a repo grep for U+2014 does not hit the report. This file contains zero U+2014 characters.

---

## Headline

**12 of 12 child issues exist. 11 are closed and still hold live. 1 child is still open: #612.** The live Zero to One post (12034) is still third person. Merged PR #803 prepared the first-person payload and did not apply it. `modified` is still `2026-08-01T18:44:59`.

**Related residue, not a child of #603:** [#764](https://github.com/WalksWithASwagger/kriskrug-wp/issues/764) is still OPEN. Post 12327 still has **21** body em dashes and live `Eth??s`. Post 12032 still links `?p=11876` (HTTP 404). Payload merged in PR #768; no WordPress write.

Closing #603 now would hide the only remaining in-scope live miss (#612). Do not close #764 to close the epic; it was never in the original 15-post set.

---

## Child inventory (filed from the epic body)

`#607` in this number range is an unrelated merged PR (`docs: ready testimonials showpiece v2 swarm`), not a #603 child. Children are **#604–#606 and #608–#616**.

| Issue | Wave | Live target | GitHub | Live 2026-08-16 | One-line verification |
|---|---|---|---|---|---|
| [#604](https://github.com/WalksWithASwagger/kriskrug-wp/issues/604) VOICE-1 | 1 | 12030 Canada AI Machine | CLOSED 2026-08-01 | **PASS** | Cache-bypass page: `Cohen White Paper` / `KK Worldview` / `Voice Profile` = 0. Essay close `"faster leak"` still present. `modified` 2026-08-01T11:57:26. |
| [#605](https://github.com/WalksWithASwagger/kriskrug-wp/issues/605) VOICE-2 | 1 | 12032 What Would Chat Do | CLOSED 2026-08-01 | **PASS** (own AC) | `KEY VIRAL` = 0, `? Use:` = 0, bio `Kris Krüg`, body U+2013 = 0, body U+2014 = 0. Dead `?p=11876` is **#764**, not this AC. `modified` 2026-08-01T12:00:50. |
| [#606](https://github.com/WalksWithASwagger/kriskrug-wp/issues/606) VOICE-3 | 1 | 12357 + 12363 Ethọ́s | CLOSED 2026-08-02 | **PASS** | `Eth??s` = 0 on both bodies. 12357 title `The Ethọ́s Lab Block Party Album`. 12363 cross-link decodes to Ethọ́s. SEO-layer ASCII `Ethos` remains (known Jetpack constraint; #606 scoped post title + body). |
| [#608](https://github.com/WalksWithASwagger/kriskrug-wp/issues/608) VOICE-4 | 1 | 12263 God Skills | CLOSED 2026-08-01 | **PASS** | 2 × `<table>`, pipe-separator gibberish = 0. `modified` 2026-08-01T11:55:47. |
| [#609](https://github.com/WalksWithASwagger/kriskrug-wp/issues/609) VOICE-5 | 1 | 12653 AI Lands | CLOSED 2026-08-01 | **PASS** | `content.rendered` U+2014 / `&mdash;` / `&#8212;` = **0**. Matches 2026-08-15 #734 readback. `modified` 2026-08-01T11:57:17. |
| [#610](https://github.com/WalksWithASwagger/kriskrug-wp/issues/610) VOICE-6 | 1 | 11879 media appearances | CLOSED 2026-08-01 | **PASS** | `Kris Krüg` present; ASCII `Khare` = 0; `Kharé` present. `modified` 2026-08-01T11:55:41. |
| [#611](https://github.com/WalksWithASwagger/kriskrug-wp/issues/611) VOICE-7 | 1 | 12612 I Am Nomad | CLOSED 2026-08-01 | **PASS** | Close is `She left with more time than she arrived with.` Old inversion absent. `modified` 2026-08-01T11:53:56. |
| [#612](https://github.com/WalksWithASwagger/kriskrug-wp/issues/612) VOICE-8 | 2 | 12034 Zero to One | **OPEN** | **FAIL** | Still third person. See section below. Payload in merged [PR #803](https://github.com/WalksWithASwagger/kriskrug-wp/pull/803). **Not applied.** |
| [#613](https://github.com/WalksWithASwagger/kriskrug-wp/issues/613) VOICE-9 | 2 | 12473 Artists Learn | CLOSED 2026-08-02 | **PASS** | Live: `The question is bigger than "did this one output copy that one work?"` Old `That is not just` specimen gone. `modified` 2026-08-01T18:30:02. |
| [#614](https://github.com/WalksWithASwagger/kriskrug-wp/issues/614) VOICE-10 | 2 | spelling align | CLOSED 2026-08-02 | **PASS** | 12638: `Future Proof` = 0, `Futureproof` present. 12653: `Futureproof Festival` present; one remaining `Future Proof` is the cited 2024 post title (documented keep). |
| [#615](https://github.com/WalksWithASwagger/kriskrug-wp/issues/615) VOICE-11 | 2 | 12034 + 12257 figures | CLOSED 2026-08-02 | **PASS vs close comment; leftover on 12034** | 12257: `$340/year`, `300 paying members`, `99+` gone. 12034 still mixes historical `130 paid members` (2×) and `cost just $240 annually` next to Individual `$340/year` and closer `300 paid members`. Close comment kept 130 as dated history; leftover `$240` current-price sentence is owned by the #612 payload recast. Do not reopen #615. |
| [#616](https://github.com/WalksWithASwagger/kriskrug-wp/issues/616) VOICE-12 | 3 | kk-voice anti-glossary | CLOSED 2026-08-02 | **PASS (tooling)** | Local `kk-voice` commit `fef2d10`. `anti-glossary.md` still has the decontracted-reveal, intervening-word, `Kris Krug\b`, and Ethọ́s-mojibake patterns. No kriskrug-wp live claim. |

**Open children of #603: 1 (#612).** Closed children: 11.

---

## #612 live: still third person (do not apply)

Public REST `GET /wp-json/wp/v2/posts/12034?_fields=id,slug,modified,title,content`

| Signal | Live 2026-08-16 |
|---|---|
| `id` / slug | 12034 / `zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey` |
| `modified` | **2026-08-01T18:44:59** (unchanged since the #615 number edits; PR #803 predicted this until apply) |
| Opening | `BC + AI transformed from an 80-person studio gathering…` (no `I`) |
| Narration | `when Kris Krüg opened the doors of MØTLEYKRÜG Media headquarters` |
| Checker hits | `As Krüg stated:` (1), `serves as CTO of Indigenomics Institute` (1) |
| First-person openers | `I opened the doors` = **false** on the cache-busted page |
| Figures | `130 paid members` × 2; `cost just $240 annually`; Individual `$340/year`; closer `300 paid members` |

Repo payload (merged, not live): `content/drafts/2026-08-01-zero-to-one-voice-rewrite/` from [PR #803](https://github.com/WalksWithASwagger/kriskrug-wp/pull/803) (supersedes draft-only [PR #667](https://github.com/WalksWithASwagger/kriskrug-wp/pull/667)). `rg -n "Krüg stated|As Krüg|serves as CTO"` on `proposed-content-raw.html` is the apply gate. Apply runbook: `APPLY-RUNBOOK.md`. Identity gate: ID 12034 + that slug. **KK comment-approval on #612 is still required. This lane did not PATCH.**

---

## Related residue: #764 (not a #603 child)

Found later during #745 triage. Out of the original 15-post sweep, so a gap rather than a regression of Wave 1.

| Defect | Live 2026-08-16 | Prepared? |
|---|---|---|
| Post **12327** body em dashes | REST `content.rendered` U+2014 = **21**. Page-wide 28 = 21 in `entry-content` + 7 theme chrome before it. `modified` **2026-07-18T11:20:49**. | [PR #768](https://github.com/WalksWithASwagger/kriskrug-wp/pull/768) merged; apply/restore hardened in #774 / #781. **Not PATCHed.** |
| Post **12327** `Eth??s` | 1× in body (`Haus of Owl, Eth??s Lab, 221A`). Same latin1/NCR class #606 fixed on 12357/12363. | Noted on #764 2026-08-15; still live. |
| Post **12032** Related link | `<a href="https://kriskrug.co/?p=11876">The 75% Rule</a>`. `GET https://kriskrug.co/?p=11876` → **HTTP 404**. | In the #768 payload. **Not PATCHed.** |

#605's own AC (prep notes / umlaut / dashes) still PASSes. The 404 link is extra.

---

## Epic acceptance criteria vs evidence

| #603 AC | Status |
|---|---|
| All Wave 1 children closed or waived by KK | **Met** (7/7 closed; all 7 live PASS) |
| P0 leaks gone from live Canada + What Would Chat Do | **Met** (#604, #605) |
| AI Lands live text has 0 em dashes under body readback | **Met** (#609; `voicecheck.py` on a fresh strip was **not run** this session) |
| Epic comment lists rollback paths for every live apply | **Not met.** Epic has one comment (child-issue index only). Rollback paths live on the child-issue close comments + `backup/20260801-voice-sweep/`. |
| Wave 2/3 done or parked with reason | **Not met.** #613–#616 done. **#612 still open, not parked.** |

Prior QA: [`voice-sweep-live-readback-20260815.md`](voice-sweep-live-readback-20260815.md) (#734, closed). This remainder agrees with that FAIL on 12034 and adds #610/#611/#613/#614/#616 plus #764.

---

## What would actually close the epic

Do **not** close #603, #612, or #764 from this report.

1. **KK comment-approves** the #612 draft (`before-after.md` + opening of `rewritten-body.md`).
2. **Snapshot-first apply** of the PR #803 payload to post 12034 only (`APPLY-RUNBOOK.md`: `context=edit` snapshot, ID+slug gate, dry-run, content POST, cache-bypass readback). Rollback is the snapshot `content.raw`.
3. **Live proof:** opening is first person; `Krüg stated` / `As Krüg` / `serves as CTO` = 0 in `content.rendered`; leftover `$240` / `130 paid members` recast per the payload (300 / $340 current figures, no invented “300 in 2.5 months”).
4. **Then** close #612, add the missing rollback-index comment on #603 (or waive that AC), and close #603.

**Optional, not required to close #603:** KK-authorized apply of #764 (12327 dashes + Ethọ́s + 12032 permalink). Keep #764 open until that write. Sitewide title-format em dash / umlaut-less `Kris Krug` is [#756](https://github.com/WalksWithASwagger/kriskrug-wp/issues/756) (chrome, not this epic).

---

## Commands run

```bash
gh issue view 603 --json number,title,state,body
# plus 604 605 606 608 609 610 611 612 613 614 615 616 764

curl -sS "https://kriskrug.co/wp-json/wp/v2/posts/<ID>?_fields=id,slug,link,status,modified,title,content,excerpt"
# IDs: 12030 12032 12357 12363 12263 12653 11879 12612 12034 12473 12638 12257 12327

curl -sL "<permalink>?cb=$RANDOM$RANDOM"   # cache-bypass greps for 604, 605, 606, 608, 612, 764
curl -sS -o /dev/null -w "%{http_code}" "https://kriskrug.co/?p=11876"  # 404
```

Dash counts used `python3` `.count(chr(0x2014))` on REST bodies and saved HTML. No `{EMDASH}` was written into the repo except as the token above.

## Commands not run

| Check | Reason |
|---|---|
| `voicecheck.py` on stripped live bodies | Body-string greps were enough for the claimed AC; sibling `kk-voice` was only sampled for #616 regex presence |
| Authenticated `context=edit` | Not needed to prove public remainder; would be required immediately before any future PATCH |
| WordPress PATCH / cache purge | Forbidden this lane |
| `gh issue close` | Forbidden this lane |

## Writes

None to WordPress. None to GitHub issues. This markdown file only.

**Fetched:** 2026-08-16 19:40–19:50 PDT. **Method:** logged-out `curl` + public REST. **Production writes:** none.
