# Live readback: 2026-08-01 voice-sweep fixes

**Issue:** [#734](https://github.com/WalksWithASwagger/kriskrug-wp/issues/734) (Lane C, Round 1 of the 2026-08-15 swarm)
**Lane:** Track A, verify-first. **Read-only against the live site.** No REST PATCH, no publish, no wp-admin change, no deploy.
**Fetched:** 2026-08-15 22:06 PDT / 2026-08-16 05:06Z, logged out, cache-bypassed (`?cb=$RANDOM$RANDOM`), plus the public REST `content.rendered` for each post.

## Verdict up front

**All 3 residual em dashes on post 12653 are theme chrome. Zero are in the post body.** #609 finished the job. Nothing was written to the live site from this lane, and no correction payload was prepared, because the conditional that would have required one (dashes in the body) is false.

Six of seven checks PASS. The one FAIL is post 12034, which is the already-known, already-owned #612 rewrite.

## Results

| Post | What was claimed fixed | Issue | Result | Evidence (fetched 2026-08-15) |
|---|---|---|---|---|
| **12653** AI Lands | 26 prose em dashes stripped | [#609](https://github.com/WalksWithASwagger/kriskrug-wp/issues/609) | **PASS** | `content.rendered` U+2014 = **0**, `&mdash;` = 0, `&#8212;` = 0. 3 dashes on the page, all outside the body (breakdown below). |
| **12030** Canada AI Machine | internal strategy memo removed | [#604](https://github.com/WalksWithASwagger/kriskrug-wp/issues/604) | **PASS** | `Cohen White Paper` 0, `KK Worldview` 0, `Voice Profile` 0, `16cc6f799a338` 0, `PDF-FinalReport-AISymposium` 0, on both the page and the body. Essay intact at 1,796 words, still closes on `"Or it's not progress, it's just a faster leak."` |
| **12032** What Would Chat Do | panel-prep notes cut, umlaut restored | [#605](https://github.com/WalksWithASwagger/kriskrug-wp/issues/605) | **PASS** | `KEY VIRAL` 0, `? Use:` 0 on page and body. Bio reads `Kris Krüg is a National Geographic photographer turned AI educator`. En dashes (U+2013) in body = 0. 1,045 words. |
| **12357** Ethọ́s Lab Block Party | mojibake + canonical title | [#606](https://github.com/WalksWithASwagger/kriskrug-wp/issues/606) | **PASS** (body + H1) | `Eth??s` = 0. Body carries 6 × `Eth&#7885;&#769;s`, which decode to **Ethọ́s** (5 in prose, 1 in alt text). H1 and REST `title.rendered` = `The Eth&#7885;&#769;s Lab Block Party Album`. Caveat below. |
| **12363** Vancouver Made World Cup | Ethọ́s cross-link | [#606](https://github.com/WalksWithASwagger/kriskrug-wp/issues/606) | **PASS** | `Eth??s` = 0. Cross-link reads `<a href="https://ethosblockparty.com/the-day">The Eth&#7885;&#769;s Lab Block Party album</a>`. |
| **12263** God Skills | broken markdown tables rebuilt | [#608](https://github.com/WalksWithASwagger/kriskrug-wp/issues/608) | **PASS** | 2 × `<figure class="wp-block-table"><table class="has-fixed-layout">`, 8 `<th>`, 22 `<tr>`. Raw `\|` characters in body = **0**. Pipe-separator gibberish (`\| --- \|`) = 0 on page and body. |
| **12034** Zero to One | membership figures | [#612](https://github.com/WalksWithASwagger/kriskrug-wp/issues/612) (open) | **FAIL** | Stale figures still live. Detail below. Not fixed here by design. |

## The 12653 dash question, answered

Three U+2014 characters exist in the 111,909-byte rendered page. Byte offsets and sources:

| # | Offset | Where | Source |
|---|---|---|---|
| 1 | 562 | `<title>AI Lands Inside Every Profession {EMDASH} Kris Krug \| AI Keynote Speaker &#038; Creative Technologist</title>` | Site-wide SEO title format, not post content |
| 2 | 68,586 | `<!-- Critical-geometry guard (#701). … the header rendered with OLD layout rules {EMDASH} nav flex-wrapped to ~98px …` | `theme/kk-aurora/parts/header.html` line 7 |
| 3 | 68,648 | `… the marquee SVGs at ~53px {EMDASH} until the deferred bundle landed …` | same HTML comment |

The post body container (`entry-content`) starts at byte offset **76,775**. Every dash is upstream of it.

**Dashes 2 and 3 are a code comment in the theme header.** They never render as visible text. They ship on every page of the site: confirmed identical `guard_comment_dashes=2` on all seven pages fetched for this report.

**Dash 1 is a site-wide title-format template, not a per-post string.** Posts that carry a custom SEO title render `Post Title | Kris Krüg` (12030, 12032, 12034, 12363, 12732, 12410). Posts with no custom SEO title fall back to `%post_title% {EMDASH} Kris Krug | AI Keynote Speaker & Creative Technologist`, which contributes exactly one em dash. Confirmed on 12653, and independently on **12656, 12638, 12612**. `og:title` and `twitter:title` on 12653 are clean (`AI Lands Inside Every Profession`).

So: **body 0, chrome 3.** No body edit is warranted, none was prepared, and no live write was attempted.

### Corollary worth KK's attention

That same fallback title string also spells the brand **`Kris Krug` without the umlaut**, and it is what Google sees for every post lacking a custom SEO title. One setting change fixes both the em dash and the umlaut across the whole tail. Proposed follow-up is at the bottom of this report. The theme's author-bio card has the same umlaut miss in `theme/kk-aurora/templates/single.html` line 55 (`Kris Krug is an AI keynote speaker, creative technologist, photographer…`). Both are chrome, both are out of scope for #734, neither is a regression.

## 12034: the one FAIL

Live body still carries the pre-ruling figures alongside the newer tier copy, and contradicts itself inside one post:

| Live string | Where | KK's August ruling |
|---|---|---|
| `the association had enrolled 130 paid members` | mid-post, growth section | 300 members |
| `Reaching 130 paid members within 2.5 months validated the membership model` | later, governance section | 300 members |
| `The new membership cost just $240 annually but offered expanded benefits` | Vancouver Core AI conversion paragraph | $340/year |
| `Individual : $340/year (1 seat for freelancers and independent practitioners)` | tier list | correct already |
| `From 80 people in a studio to 300 paid members of a nonprofit` | closing paragraph | correct already |

The post says **130 paid members** in two places and **300 paid members** in a third. That internal contradiction is live right now.

**Not fixed here.** #612 is the vehicle and it is open, staged, and gated on KK review. Applying figure edits from this lane would collide with that lane's payload and would exceed #734's stated boundary ("No fixes applied beyond em-dash/artifact residue without KK approval").

**What the fix takes:** #612's draft rewrite adopts the ruling ($340/year, 300 members), KK approves the draft in an issue comment, then a snapshot-first `wp-live-edit` apply against 12034 with a cache-bypass readback. Three string sites above are the minimum touch if KK ever wants a figures-only hotfix decoupled from the voice rewrite; that would be a separate, smaller approval.

## 12357 caveat: body is clean, SEO layer is not

The post body and H1 are canonical. The SEO/social layer is still ASCII:

- `<title>The Ethos Lab Block Party Album | Kris Krug</title>`
- `<meta name="description">`, `og:description`, `twitter:description` all read `at the Ethos Lab block party`
- The taxonomy term renders `Ethos Lab` at `/tag/ethos-lab/`

This is **plausibly deliberate**, not a miss. Two documented constraints point that way: REST writes to `jetpack_seo_html_title` / `advanced_seo_description` return 500 on combining-diacritic values like Ethọ́s, and Jetpack SEO meta is currently unregistered from REST so writes silently no-op. #606's acceptance criteria scoped the title fix to the post title, which passed. Flagging, not failing.

## Nothing regressed

Every previously-closed sweep item that was checked is still holding at the values its issue demanded. No new defect appeared in any of the six posts.

One drift note, not a defect: the repo payload at `content/drafts/2026-08-02-emdash-remediation/remediated-body.md` is **ahead of live on two reveal-density sentences**. The live post has all 26 dashes gone and one of the three reveal variations applied (`That is a design choice, not a romance about grit.`). The other two are still in their original form live:

- live: `The failure mode is not departure. The failure mode is a province with no serious pathway home.`
  payload: `What kills a region is having no serious pathway home.`
- live: `The point is not to cheerlead AI but to build enough shared practice…`
  payload: `I am not asking you to cheer for AI. I am asking you to help build…`

#609 owned dashes; reveal density was the secondary ask. Both live sentences are dash-free, so the issue's acceptance criteria are met either way. Whether to land the remaining two variations is a KK call, not a QA finding.

## Commands run

```bash
# rendered pages, logged out, cache-bypassed
curl -sS -o live-<ID>.html "<url>?cb=$RANDOM$RANDOM"

# authoritative post body, no auth needed
curl -sS "https://kriskrug.co/wp-json/wp/v2/posts/<ID>?_fields=id,slug,modified,content,title"

# dash counting without reintroducing the character into this repo
python3 -c "import pathlib;print(pathlib.Path('live-12653.html').read_text(encoding='utf-8').count(chr(0x2014)))"
```

Quoted evidence in this report writes the em dash as the literal token `{EMDASH}`, matching the convention in `content/drafts/2026-08-02-emdash-remediation/dash-ledger.md`, so that grepping the repo for the character does not hit this file. This file contains zero U+2014 characters.

## Proposed follow-up (not filed by this lane)

**Title:** `seo: strip the em dash and restore the umlaut in the fallback post title format`

The site-wide SEO title format `%post_title% {EMDASH} Kris Krug | AI Keynote Speaker & Creative Technologist` puts an em dash and an umlaut-less brand into the `<title>` of every post that has no per-post SEO title (confirmed on 12612, 12638, 12653, 12656). Posts with a custom SEO title use `Post Title | Kris Krüg` and are unaffected. Fix is one Jetpack `advanced_seo_title_formats.posts` change, not a content edit. Two known landmines: Jetpack SEO meta is currently unregistered from REST so writes may silently no-op, and combining-diacritic values 500 on write. A plain `ü` (U+00FC) is precomposed and latin1-safe, so it should be fine, but verify with a public readback rather than trusting the write's response. Refs #734.

---

**Fetched:** 2026-08-15 22:06 PDT. **Method:** logged-out `curl` + public REST. **Writes to production:** none.
