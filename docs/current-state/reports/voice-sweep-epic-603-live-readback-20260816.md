# Live readback: #603 voice-sweep epic (15-post Dark Crystal audit)

**Issue:** [#603](https://github.com/WalksWithASwagger/kriskrug-wp/issues/603)
**Lane:** Track A, verify-first. **Read-only against the live site.** No REST PATCH, no publish, no wp-admin change, no deploy, no theme edit.
**Fetched:** 2026-08-16 19:40 PDT / 2026-08-17 02:40 UTC, logged out. Public REST `content.rendered` for every named post, plus cache-bypassed HTML (`?cb=$RANDOM$RANDOM`) for all 15 audit posts and related post 12327.
**Does not duplicate:** PR [#755](https://github.com/WalksWithASwagger/kriskrug-wp/pull/755) (merged; 7-post #734 readback on 2026-08-15) or PR [#768](https://github.com/WalksWithASwagger/kriskrug-wp/pull/768) (merged; 12327 dash payload prepared, not applied).

Quoted em dashes in this file are written `{EMDASH}` so the report itself contains zero U+2014.

## Verdict up front

Wave 1 is live-clean. The only FAIL on a post named in #603 / its children is **12034 Zero to One**, still third-person, still mixing `$240` / `130 paid members` with `$340` / `300`. That FAIL is already owned by open [#612](https://github.com/WalksWithASwagger/kriskrug-wp/issues/612) and the merged (not live-applied) payload in PR [#803](https://github.com/WalksWithASwagger/kriskrug-wp/pull/803).

**There is no uncovered live residue on the 15-post set.** The later 12327 dash / 12032 dead-link defects ride open [#764](https://github.com/WalksWithASwagger/kriskrug-wp/issues/764) + merged PR #768; they are outside the epic's child list.

**#603 cannot close yet.** It can close after the #612/#803 apply lands (or KK explicitly parks/waives the rewrite). Do not wait on #764 to close the epic.

Covering-PR status as of this fetch (the prompt called them "open"; they are not):

| Named cover | Actual state | What it owns |
|---|---|---|
| PR #803 | **MERGED** 2026-08-17, live apply **not done** (`12034.modified` still `2026-08-01T18:44:59`) | First-person rewrite + `$340` / `300` figures |
| PR #768 / issue #764 | PR **MERGED** 2026-08-16; issue **OPEN**; live apply **not done** (`12327.modified` still `2026-07-18T11:20:49`) | 21 body `{EMDASH}` on 12327 + `?p=11876` 404 on 12032 |
| Issue #734 / PR #755 | Both **closed/merged** | Prior 7-post readback; 12653 body dashes already PASS |

## Child-issue roll

| Child | State | Live vs original defect |
|---|---|---|
| #604 VOICE-1 12030 | CLOSED | **PASS** |
| #605 VOICE-2 12032 | CLOSED | **PASS** (prep/umlaut/en-dash). Related 404 is #764, not this issue. |
| #606 VOICE-3 12357+12363 | CLOSED | **PASS** |
| #608 VOICE-4 12263 | CLOSED | **PASS** |
| #609 VOICE-5 12653 | CLOSED | **PASS** (body 0 `{EMDASH}`; page chrome is #756) |
| #610 VOICE-6 11879 | CLOSED | **PASS** |
| #611 VOICE-7 12612 | CLOSED | **PASS** |
| #612 VOICE-8 12034 | **OPEN** | **FAIL** - covered by merged #803, not applied |
| #613 VOICE-9 12473 | CLOSED | **PASS** |
| #614 VOICE-10 12638+12653 | CLOSED | **PASS** (rejected two-word festival spelling gone from named posts) |
| #615 VOICE-11 12034+12257 | CLOSED | **PASS** on 12257. Leftover `$240 annually` / dated `130` on 12034 rides #612. |
| #616 VOICE-12 kk-voice | CLOSED | Not a live post. **Skipped** here (sibling repo). |

#607 was never part of this batch.

## Full table - every post named in #603 or a child

| Post ID | URL | Original defect | Child | Live | Evidence (2026-08-16) |
|---|---|---|---|---|---|
| 12030 | https://kriskrug.co/2026/06/26/canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one/ | P0 internal strategy memo after the essay | #604 | **PASS** | REST+HTML: `Cohen White Paper` 0, `KK Worldview` 0, `Voice Profile` 0, `16cc6f799a338` 0, `PDF-FinalReport-AISymposium` 0. Essay still closes on `faster leak`. `modified=2026-08-01T11:57:26`, 1,796 words. |
| 12032 | https://kriskrug.co/2026/06/28/what-would-chat-do-and-why-thats-the-wrong-question/ | P0 prep notes; P1 umlaut; P2 en-dashes as em dashes | #605 | **PASS** | `KEY VIRAL` 0, `? Use:` 0, body U+2013 0, bio `Kris Krüg` present, `Kris Krug\b` 0 in REST body. 1,045 words. **Related (not this defect):** live HTML still has `<a href="https://kriskrug.co/?p=11876">The 75% Rule</a>`; `?p=11876` HTTP 404. Covered by #764/#768. |
| 12357 | https://kriskrug.co/2026/06/23/ethos-lab-block-party/ | P0 `Eth??s` mojibake; P1 title → Ethọ́s Lab | #606 | **PASS** | REST title `The Ethọ́s Lab Block Party Album`. `Eth??s` 0. Body 5 × Ethọ́s / 6 × `&#7885;` NCR. Same SEO-ASCII caveat as #755 (`<title>` still `Ethos Lab`); out of #606 AC. |
| 12363 | https://kriskrug.co/2026/06/23/vancouver-made-world-cup/ | P0 `Eth??s` in cross-link | #606 | **PASS** | `Eth??s` 0. 1 × Ethọ́s in REST body (NCR `&#7885;`). Entry `{EMDASH}` 0. |
| 12263 | https://kriskrug.co/2026/06/20/god-skills-agentic-loop-workflows/ | P0 markdown tables rendering as gibberish | #608 | **PASS** | 2 × `wp-block-table` / `<table>`, 8 `<th>`, 22 `<tr>`. `\| --- \|` 0. Body `{EMDASH}` 0. |
| 12653 | https://kriskrug.co/2026/07/31/ai-lands-inside-every-profession/ | P1 26 prose em dashes; P3 Futureproof spelling | #609 #614 | **PASS** | REST `content.rendered` U+2014/`&mdash;`/`&#8212;` = 0. HTML `entry-content` `{EMDASH}` = 0. Page still has 3 chrome dashes (1 in `<title>` fallback, 2 in header comment) - #756, not body. Festival copy is `Futureproof Festival`. The one `Future Proof:` hit is the 2024 article title citation, left alone by #614. En dashes in `October 28-30` remain (allowed). |
| 11879 | https://kriskrug.co/2026/07/02/ai-media-appearances-podcast-guesting/ | P1 umlaut-less link text + Kharé/Khare mix | #610 | **PASS** | REST body: `Kris Krug\b` 0, `Kris Krüg` ×4, `Kharé` ×2, `Khare` 0. Theme author-card / footer still say `Kris Krug` (Track B; #735/#756). `Future Proof Creatives` is a show name, not the festival. |
| 12612 | https://kriskrug.co/2026/07/18/i-am-nomad-ai-film/ | P3 closing line inverted the film's time-gain | #611 | **PASS** | Live close: `She left with more time than she arrived with. Turns out so did we.` Old close 0. |
| 12034 | https://kriskrug.co/2026/06/30/zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey/ | P2 third-person rewrite; membership `$240`/130 vs `$340`/300 | #612 #615 | **FAIL** | Still `As Krüg stated`. `130 paid members` ×2 (dated Nov 2025 / 2.5-month sentences). `The new membership cost just $240 annually` still live. Individual tier `$340/year` and closer `300 paid members` also live - internal contradiction. `seamless` / `cutting-edge` / `pivotal` still in body. `modified=2026-08-01T18:44:59` (no apply since #615's surgical numbers). **Covered by merged #803; do not re-prepare.** |
| 12473 | https://kriskrug.co/2026/07/06/artists-learn-machines-extract/ | P2 decontracted "not just" reveal (L38-40) | #613 | **PASS** | Old specimen `That is not just` 0. Live: `The question is bigger than "did this one output copy that one work?"` Remaining `not just` is the comparative liability line #613 left on purpose. |
| 12638 | https://kriskrug.co/2026/07/28/no-one-knows-what-to-call-us-yet/ | P3 Future Proof vs Futureproof | #614 | **PASS** | Article `Future Proof` 0. Live: `building toward Futureproof, our festival…`. Full canonical `Futureproof Festival of AI` was not substituted (would double "festival"); #614 closed on the one-word swap. Body `{EMDASH}` 0. |
| 12257 | https://kriskrug.co/2026/06/18/why-we-built-the-responsible-ai-professional-certification/ | P2 membership conflict with 12034 | #615 | **PASS** | `300 paying members` present. `99+ paying` 0. `$340/year` present. `$240` 0. |
| 12035 | https://kriskrug.co/2026/06/24/ai-wont-fix-your-broken-permit-process/ | Clean bill (no child) | - | **PASS** | REST+HTML: body `{EMDASH}` 0. No P0/P1 needles. Original audit: no material flags. |
| 12190 | https://kriskrug.co/2026/06/22/the-great-canadian-proximity-game/ | Clean bill; satire keep | - | **PASS** | Body `{EMDASH}` 0. Uses `Futureproof Festival` (already one-word). |
| 12479 | https://kriskrug.co/2026/07/10/the-cheer-is-a-cap-table/ | Clean bill; `buckle-up` keep | - | **PASS** | Body `{EMDASH}` 0. Page chrome dashes only. |

### Related, not an #603 child (named here so it is not mistaken for epic residue)

| Post ID | URL | Defect | Tracker | Live | Covered? |
|---|---|---|---|---|---|
| 12327 | https://kriskrug.co/2026/06/17/storyhive-haus-of-owl-jordan-dack/ | 21 prose `{EMDASH}` (found after the sweep; never in the 15) | #764 / PR #768 | **FAIL** | **Yes - payload merged, not PATCHed.** REST `content.rendered` U+2014 = **21**, `&mdash;` = 0. `modified=2026-07-18T11:20:49`. Also live `Eth??s Lab` (×1 in body); #768 runbook explicitly left that out of the dash payload. Treat Eth??s as a follow-on on #764, not a new epic child. |

## What is *not* remaining residue

- Re-doing the #755 seven-post PASS list. Reconfirmed; none of those six PASSes regressed.
- Re-preparing 12327 dash rewrites. #768 already did.
- Re-preparing the 12034 first-person body. #803 already did.
- Theme `<title>` `{EMDASH}` + umlaut-less `Kris Krug` fallback (#756, PR #789) and theme author-bio card umlaut (#735). Track B. Epic out of scope.
- #616 checker-gap regexes in `kk-voice`. Closed; not re-run from this repo.

## Epic acceptance criteria vs this fetch

| #603 AC | Status |
|---|---|
| All Wave 1 children closed or KK-waived | **Met** (all seven closed; live PASS) |
| P0 leaks gone from Canada + What Would Chat Do (cache-bypass) | **Met** |
| AI Lands live text 0 em dashes | **Met** (body; chrome is #756) |
| Epic comment lists rollback paths for every live apply | **Not met as a comment on #603 itself.** Paths exist on the child issues (`backup/20260801-voice-sweep/…`). Process checkbox only. |
| Wave 2/3 done or parked with reason | **Not met.** #612 still open and live-FAIL. #613-#616 closed. |

## Commands run

```bash
# public REST body (authoritative for post content)
curl -sS "https://kriskrug.co/wp-json/wp/v2/posts/<ID>?_fields=id,slug,link,title,modified,content,excerpt"

# cache-bypassed logged-out pages
curl -sS -o live-<ID>.html "<url>?cb=$RANDOM$RANDOM"

# 404 confirmation for the related #764 link
curl -sS -o /dev/null -w "%{http_code}" "https://kriskrug.co/?p=11876"
# -> 404
```

Dash counts used `str.count("\u2014")` on REST `content.rendered` and on HTML `entry-content`, never a literal em dash in this repo.

## Writes to production

None.
