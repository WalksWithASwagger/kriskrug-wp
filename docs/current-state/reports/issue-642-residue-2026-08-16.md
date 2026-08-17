# Issue #642 residue rewrite — 2026-08-16

**Mode:** docs / queue hygiene only. No live WordPress writes. **Do not `gh issue edit`.** Agents do not rewrite GitHub issue bodies without KK.  
**Source issue:** [#642](https://github.com/WalksWithASwagger/kriskrug-wp/issues/642) `[SWARM DISPATCH] Command board — 2026-08-02` — **OPEN**  
**Branch:** `docs/642-residue-20260816`  
**Compared against:** original #642 body (created 2026-08-02), issue comments through 2026-08-05, live GitHub state 2026-08-16 (PDT) / 2026-08-17T02:45Z, public readbacks the same hour.  
**Prior draft:** `docs/current-state/reports/BACKLOG-GROOMING-DOSSIER-2026-08-15.md` §2.1 — **stale.** Wave 1 speaking (#637, #638) closed after that dossier. This file replaces that draft as the paste-ready body.

This report does **not** close #642 or edit its body. KK pastes the replacement below in the GitHub UI if it looks right.

## Verdict

The 2026-08-02 board is **mostly shipped**. Three of four proof surfaces drained. Keep #642 open only as a thin pointer to genuine residue. Do not treat it as a dispatchable swarm.

Residue that is still real:

1. **Speaking live rebuild** — #419 umbrella, children #639 / #640 / #641. Taxonomy decided; page 1887 not applied.
2. **Two live-write deploy gates** — #635 events heroes, #602 testimonials body.
3. **One open epic** — #593, waits on #602.
4. **Two successor live applies** — #729 Futureproof date copy, #612 Zero to One rewrite. Repo payloads exist; production still stale.

Drop `swarm-ready` when the body is replaced. Remaining work is KK-gated live apply, not autonomous swarm.

---

## Original workstream cross-check

Checked 2026-08-16 against `gh issue view`, merged PRs, and logged-out public readbacks. Live Aurora `style.css` **1.6.5**. Repo `origin/main` is **1.6.7** (`59505f1`); that drift is not #642 residue.

### Surface 1 — Events archive

| Issue | Original role | State now | Evidence |
|---|---|---|---|
| #592 | Exclusive live apply for `/events/` backfill | **CLOSED** 2026-08-02 | Verified ship in #642 body: 66 events, no TruNorth, no `file://` |
| #631 | Render-contract tests | **CLOSED** 2026-08-03 | PR [#651](https://github.com/WalksWithASwagger/kriskrug-wp/pull/651) merged |
| #632 | Hero ledger 2024/2025 | **CLOSED** 2026-08-03 | PR [#647](https://github.com/WalksWithASwagger/kriskrug-wp/pull/647) merged |
| #633 | Hero ledger 2026 + meetup series | **CLOSED** 2026-08-03 | PR [#648](https://github.com/WalksWithASwagger/kriskrug-wp/pull/648) merged |
| #634 | Post-ship internal-link plan | **CLOSED** 2026-08-03 | PR [#649](https://github.com/WalksWithASwagger/kriskrug-wp/pull/649) merged |
| **#635** | Exclusive hero backfill live apply | **OPEN** | No apply PR. Live `/events/` still has **49** `aurora-event-compact-media--empty` and **70** `data-event-end` (2026-08-16). Labels still include `blocked`. |

**Residue:** #635 only. Every repo-side blocker named on the original board is closed. Inherits #592 exclusivity: only this issue may mutate the events catalog, upload event media, or write page 2250.

### Surface 2 — Testimonials showpiece

| Issue | Original role | State now | Evidence |
|---|---|---|---|
| #594–#600 | Inventory, LinkedIn, CSS, copy, curate, payload, consent packet | **CLOSED** 2026-08-02 | PRs [#627](https://github.com/WalksWithASwagger/kriskrug-wp/pull/627)–[#630](https://github.com/WalksWithASwagger/kriskrug-wp/pull/630) |
| #601 | Pixel-gate theme deploy (`aurora-tstm`) | **CLOSED** 2026-08-10 | Closed after the 2026-08-10 Aurora 1.6.0 deploy. Live 1.6.5 still carries the CSS. |
| **#602** | Snapshot-gate page body, WP 2409 | **OPEN** | Live page 2409 `modified` **2026-08-01T19:09:19**. `aurora-tstm` class count **0**. Draft runbook PR [#817](https://github.com/WalksWithASwagger/kriskrug-wp/pull/817). No live PATCH. |
| **#593** | Epic umbrella | **OPEN** | Closes when #602 ships. Body still says Wave 4 is open, which is still true for the page-body half. |

**Residue:** #602 live apply + epic #593. Theme half is done.

### Surface 3 — Futureproof origin post

| Issue | Original role | State now | Evidence |
|---|---|---|---|
| #496 | Epic | **CLOSED** 2026-08-12 | Post 12732 published |
| #500 | KK-authorized WP draft create | **CLOSED** 2026-08-11 | PRs [#535](https://github.com/WalksWithASwagger/kriskrug-wp/pull/535), [#718](https://github.com/WalksWithASwagger/kriskrug-wp/pull/718), [#719](https://github.com/WalksWithASwagger/kriskrug-wp/pull/719) |
| #643 / #644 / #645 | Lineage, Meetup #31 art, network follow-up | **CLOSED** 2026-08-02 | PR [#646](https://github.com/WalksWithASwagger/kriskrug-wp/pull/646) |
| **#729** | Successor: refresh expired Aug-15 Call-for-Talks + Earlyworm copy | **OPEN** | This is the date warning #642 raised. KK ruled 2026-08-16: close Call for Talks; Earlyworm through **Aug 31**. Payload PR [#790](https://github.com/WalksWithASwagger/kriskrug-wp/pull/790) **merged**. Live post 12732 still has **two** `August 15, 2026` strings and **zero** `August 31, 2026`. Apply still owed (no WP creds in the preparing session). |

**Residue:** #729 live apply only. Origin post shipped.

### Surface 4 — Speaking booking page (WP 1887)

| Issue | Original role | State now | Evidence |
|---|---|---|---|
| #636 | Verify talk video set | **CLOSED** 2026-08-03 | PR [#650](https://github.com/WalksWithASwagger/kriskrug-wp/pull/650) |
| #637 | Stage photography + rights | **CLOSED** 2026-08-17 | Inventory PR [#657](https://github.com/WalksWithASwagger/kriskrug-wp/pull/657); closed via PR [#799](https://github.com/WalksWithASwagger/kriskrug-wp/pull/799) `Fixes #637`. Rights constraint now lives on #419 (cleared Meetup 30 frame only). |
| #638 | Reconcile keynote taxonomies | **CLOSED** 2026-08-17 | Research PR [#653](https://github.com/WalksWithASwagger/kriskrug-wp/pull/653). KK six-talk ruling + payload PR [#798](https://github.com/WalksWithASwagger/kriskrug-wp/pull/798) auto-closed it. Ruling receipt: `docs/current-state/reports/keynote-taxonomy-638-ruling-2026-08-17.md`. **Live `/speaking/` does not yet match the ruling.** |
| **#639** | Page architecture + payload rebuild | **OPEN** | Repo payload rebuilt in PR #798 (`payload-body.html` has the six talks + two lazy YouTube iframes). Live page 1887 `modified` **2026-07-24**: four-talk Set C (Both Hands Full, Punk Rock AI, Developing an AI Mindset, **Responsible AI**). Zero iframes. Compost AI / Leadership / Power Taste Trust: **0**. |
| **#640** | Embed hygiene + LCP contract tests | **OPEN** | No dedicated PR. Payload now has `loading="lazy"` iframes; contract tests still missing. |
| **#641** | VideoObject schema + proof-triangle links | **OPEN** | No dedicated PR. Still Wave 3. |
| **#419** | Speaking multimedia umbrella | **OPEN** | Owns the live rebuild that sells keynotes. PR #798 is `Refs #419`, not a live apply. |

Original board: “Speaking deploy — mint when #641 lands.” **Still unminted.** Do not invent it here. Live apply stays on #419 after #640/#641 repo work, with KK snapshot gate.

**Residue:** #419 + #639 + #640 + #641. Wave 1 is done as repo/decision work. Live page is still the July 24 four-talk body.

### Independent KK gate named on the original board

| Issue | Original role | State now | Evidence |
|---|---|---|---|
| **#612** | Zero to One first-person rewrite, post 12034 | **OPEN** | Draft PR [#667](https://github.com/WalksWithASwagger/kriskrug-wp/pull/667) merged 2026-08-05. Apply-ready rewrite PR [#803](https://github.com/WalksWithASwagger/kriskrug-wp/pull/803) merged 2026-08-17 (`Refs #612`). Live post `modified` **2026-08-01**; still mixes `$240` / `$340` and `130` paid members. No PATCH. |

WORK-PLAN-2026-08-16: “#612 / #602 unanswered; stay parked.” Treat as parked live apply, not swarm.

### Not #642 residue

#418 About and #420 Services rode along in PR #798. They were never on this board. Do not pull them into the rewritten body.

---

## What the 2026-08-15 dossier got wrong

`BACKLOG-GROOMING-DOSSIER-2026-08-15.md` §2.1 said residue was “five open Speaking issues” including #637 and #638 as open KK gates. Both closed 2026-08-17. The replacement body below is the corrected set.

---

## Replacement GitHub body (paste into #642)

```markdown
# [SWARM DISPATCH] Command board — residue only

Original board: 2026-08-02, four proof surfaces (events, testimonials, Futureproof, speaking). Three drained. Reduced 2026-08-16 to what is still open. Full original plan is in this issue's history. This issue is a pointer board, not a swarm.

Do not start work from this issue. Open the successor and follow that issue's gates.

## What drained

- **Events archive:** shipped. #592, #631, #632, #633, #634 closed. Picture problem remains on #635.
- **Testimonials showpiece:** built and merged (#594–#601). Theme CSS is live. Page body is not. Epic #593 stays open until #602 ships.
- **Futureproof origin post:** shipped. #496, #500, #643, #644, #645 closed. Post 12732 is live. The Aug-15 date warning this board raised is **#729**.
- **Speaking Wave 1:** shipped as repo/decision work. #636 videos, #637 photography inventory, #638 six-talk ruling all closed. Live `/speaking/` is still the 2026-07-24 four-talk body.

## Residue 1 — Speaking live rebuild (WP 1887)

Canonical set is the **6-talk topic bank** (#638 closed on that ruling; receipt `docs/current-state/reports/keynote-taxonomy-638-ruling-2026-08-17.md`). Payload rebuilt in PR #798. **Not applied.**

| Issue | What is left |
|---|---|
| **#419** | Umbrella. Live multimedia rebuild that sells keynotes. |
| **#639** | Repo payload exists; live page 1887 still Set C (Responsible AI in the grid; no Compost / Leadership / Power Taste Trust; zero iframes). |
| **#640** | Embed hygiene + LCP contract tests. Markup is in the payload; tests are not. |
| **#641** | VideoObject schema + proof-triangle internal links. |

Live apply stays on #419 after #640/#641. No separate speaking-deploy issue was minted. Do not invent one from this board.

## Residue 2 — live-write gates, strictly serial

Only one may run at a time. Both need KK + snapshot + credentials.

1. **#635** events hero backfill. Repo blockers gone. Live `/events/` still shows empty hero slots. Exclusive: only this issue may mutate the events catalog, upload event media, or write page 2250.
2. **#602** testimonials page body, WP 2409. Snapshot gate. #601 closed. Live page still the 2026-08-01 v1 body. Draft runbook: PR #817. Epic **#593** closes when this ships.

## Residue 3 — successor live applies (payloads merged, production stale)

- **#729** Futureproof post 12732: close Call for Talks; Earlyworm through **August 31**. Payload PR #790 merged. Live still has two `August 15, 2026` strings.
- **#612** Zero to One first-person rewrite, post 12034. Payload PRs #667 and #803 merged. Live still third-person / mixed membership figures. Parked until KK reviews.

## Standing rules (unchanged)

- No agent sends consent outreach. `consent-outreach.md` is KK's to send.
- Nothing publishes without KK's exact approval.
- Snapshot before every live write; rollback path recorded before, not after.
- Theme / plugins / `inc/` / live-deploy PRs merge only after KK approval.
- Lane-scoped commits: never mix Track A content with Track B theme.
```

---

## Proposed comment (paste on #642 after the body replace)

```markdown
Rewrote this board down to residue. Agents did not `gh issue edit`; replacement is in `docs/current-state/reports/issue-642-residue-2026-08-16.md`.

Cross-check 2026-08-16 (live Aurora 1.6.5):

- Events: #631–#634 closed. **#635** still open (49 empty heroes live).
- Testimonials: #594–#601 closed. **#602** + epic **#593** still open (page 2409 unmodified since 2026-08-01).
- Futureproof: origin shipped. Date risk moved to **#729** (PR #790 merged, live still Aug 15).
- Speaking: Wave 1 closed (#636, #637, #638). Live 1887 still July 24 four-talk body. Successors **#419 / #639 / #640 / #641**.
- Independent: **#612** payload merged, live apply parked.

Please drop `swarm-ready` on this issue. Remaining work is KK-gated live apply, not a swarm.
```

---

## Agent boundaries

| Allowed | Forbidden |
|---|---|
| This report, commit, draft PR | `gh issue edit`, closing #642 or children |
| Cite live readbacks and merged PRs | Live WP PATCH, theme deploy, SFTP |
| Recommend the paste-ready body | Relabel via API |

## Refs

- Issue: #642
- Successors still open: #419, #639, #640, #641, #635, #602, #593, #729, #612
- Closed on this board's original set: #592, #631–#634, #594–#601, #496, #500, #643–#645, #636–#638
- PRs: #647–#651, #630, #657, #653, #798, #799, #790, #803, #817 (draft)
