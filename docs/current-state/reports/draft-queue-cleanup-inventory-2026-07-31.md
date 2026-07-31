# Draft-queue cleanup inventory — 2026-07-31

**Issue:** [#569](https://github.com/WalksWithASwagger/kriskrug-wp/issues/569)
**Branch:** `ops/569-draft-queue-inventory`
**Scope:** Report-only classification of `content/drafts/` entries. **Nothing deleted or moved.**
**Command:** `LOCAL_ONLY=1 make draft-queue-audit FORMAT=json` (2026-07-31)

## Summary counts

| Classification | Count | Meaning |
|---|---:|---|
| **Real packet** | 68 | Has `post.md` (and usually companion packet files). Includes one thin published remnant (`sponsor-deck`, 16 words). |
| **Publish-log-only** | 2 | Directory contains only `publish.log`. |
| **Empty shell** | 1 | No post body; only a tiny deploy note. |
| **Non-packet work product** | 21 | Audit flags `empty local artifact` (no `post.md`), but disk holds page-ops / research files. **Keep.** |
| **Publish residue** | 1 | Post-publish ops leftover with snapshots/media (not log-only). |
| **Total directories** | **93** | Plus 21 top-level files under `content/drafts/` (queue docs / SEO JSON / README) — not classified as dirs. |

**Audit cross-check:** markdown audit reports **23** `empty local artifact` rows. That flag means `words == 0` and no recognized packet files in the auditor’s file list — **not** “directory is empty on disk.” Of those 23:

| Audit `empty local artifact` → this inventory | Count |
|---|---:|
| Publish-log-only | 2 |
| Empty shell | 1 |
| Publish residue | 1 |
| Non-packet work product (keep) | 19 |

(The other 2 non-packet dirs — `accessibility-statement-2026-05`, `2026-07-26-land-acknowledgment` — show only `publish-gate.md` in the auditor file list but still hold README/work files on disk.)

## Proposed archive/delete list (KK approval required)

Prefer `mv` to an archive dir over `rm`. Untracked dirs have **no git safety net**.

| Path | Class | Live check | Recommendation |
|---|---|---|---|
| `content/drafts/2026-07-28-no-one-knows-what-to-call-us/` | publish-log-only (untracked) | `publish.log` says WP id `12638` `status=publish`. `curl -sI https://kriskrug.co/no-one-knows-what-to-call-us/` → **301** → `/2026/07/28/no-one-knows-what-to-call-us-yet/` (**200**). Public slug has `-yet`; do not invent other slugs. | **Archive OK** after KK ack — local body already gone; live post exists. |
| `content/drafts/2026-07-30-the-unmakable-becomes-makable/` | publish-log-only (untracked) | Log shows WP id `12645` still **`status=draft`**, slug evolved to `ai-animation-social-contract`. `curl -sI` for `/the-unmakable-becomes-makable/`, `/ai-animation-social-contract/`, and `?p=12645` → **404** (not public). | **Do not treat as published.** Archive local shell only if KK confirms the WP draft (or a successor packet) still holds the body. |
| `content/drafts/2026-07-24-seo-425-deploy/` | empty shell (1 tracked `NOTES.md`) | Notes only; points at a `/private/tmp/…` snippet snapshot. No post packet. | **Archive OK** — deploy receipt only. |
| `content/drafts/2026-07-24-sponsor-deck/` | real packet (thin) + publish.log | Log: `slug=sponsor-deck` `status=publish`. `curl -sI https://kriskrug.co/sponsor-deck/` → **200**. | **Optional archive** — live page present; local packet is stub (16 words). |
| `content/drafts/2026-07-24-contact-421/` | publish residue | Log: published contact portrait rebuild `page=2418`. `?p=2418` → **301** `/contact/` (**200**). Contains screenshots + REST snapshot (~6.8 MB). | **Optional archive** after KK confirms no rollback need from this dir. |

**Not proposed for delete:** all 21 non-packet work products (July 26 page-ops dirs, pillars, swarm-ready-pages, wp-draft-\*, accessibility-statement handoffs). Audit-empty ≠ empty.

## Keep / real packets

### Real packets (68) — retain in queue or handle via normal publish flow

Dated post/page packets with substantive `post.md` (word counts from local audit):

| Dir | Words | Notes |
|---|---:|---|
| `2026-05-06-comox-valley-ai-is-becoming-its-own-thing` | 3014 | |
| `2026-05-07-web-summit-vancouver-2026` | 2149 | |
| `2026-05-13-sovereign-ai-for-whom` | 4109 | |
| `2026-05-14-calling-us-all-in` | 2002 | |
| `2026-05-16-why-we-built-the-responsible-ai-professional-certification` | 1278 | |
| `2026-05-19-ai-keynote-chaos-creativity-channelnext` | 486 | |
| `2026-05-19-ai-media-appearances-podcast-guesting` | 759 | |
| `2026-05-19-both-hands-full-ai-creatives-lasalle-college` | 749 | |
| `2026-05-19-both-hands-full-vancouver-ai-march-2026` | 554 | |
| `2026-05-19-dear-ai-bass-coast-brain-stage` | 424 | |
| `2026-05-19-horizons-ai-models-future-machine-learning` | 488 | |
| `2026-05-19-inside-vancouvers-ai-boom-whistler-institute` | 644 | |
| `2026-05-21-i-wont-fake-the-people-who-showed-up` | 1462 | has `SUPERSEDED.md` |
| `2026-05-21-speak-it-into-existence-ai-voice-first-workflows` | 1611 | has `SUPERSEDED.md` |
| `2026-05-21-the-75-percent-rule-ai-art-adjacent-work` | 1793 | has `SUPERSEDED.md` |
| `2026-05-23-data-center-protest-signs` | 1422 | |
| `2026-05-23-you-cant-drink-data` | 2789 | large photo tree |
| `2026-05-24-agent-orchestrators-creative-insurgents-the-new-stack` | 2005 | |
| `2026-05-24-ai-wont-fix-your-broken-permit-process` | 1966 | |
| `2026-05-24-born-for-this-co-creative-age` | 219 | |
| `2026-05-24-canada-doesnt-need-a-bigger-ai-machine-it-needs-a-better-one` | 4051 | |
| `2026-05-24-canada-media-fund-prototyping-spektorai` | 626 | |
| `2026-05-24-community-washed-capitalism-when-volunteering-becomes-unpaid-labor-at-scale` | 597 | |
| `2026-05-24-finding-harmony-in-the-age-of-ai-a-digital-alchemists-guide-to-the-future` | 1112 | |
| `2026-05-24-funding-for-journalism-startups-and-media-companies-in-2023` | 556 | |
| `2026-05-24-future-proof-chaos-building-the-creative-tech-utopia` | 388 | |
| `2026-05-24-gender-balance-email-post-vancouver-ai` | 4061 | |
| `2026-05-24-guide-to-hacking-language-and-dismantling-colonialism` | 1263 | |
| `2026-05-24-how-a-late-night-brain-dump-became-a-multimedia-thought-leadership-machine` | 1125 | |
| `2026-05-24-how-to-build-an-ungovernable-life-and-why-youd-want-to` | 1047 | |
| `2026-05-24-how-we-did-it-behind-the-scenes-of-the-sfu-siat-microcredential-project` | 1104 | |
| `2026-05-24-human-element-shane-loki-talk` | 875 | |
| `2026-05-24-keynote-music-elevation-series-haus-of-owl` | 5215 | |
| `2026-05-24-kris-krugs-laws-of-digital-nomadism` | 1366 | |
| `2026-05-24-nik-badminton-a-sassy-critique-setting-the-ai-record-straight` | 2305 | |
| `2026-05-24-nobel-chemistry-foldit` | 764 | |
| `2026-05-24-outline-for-droid-army-post` | 662 | |
| `2026-05-24-rewiring-education-hacking-the-system-for-an-ai-powered-future` | 391 | |
| `2026-05-24-smudging-the-lines-humanity-embodiment-and-ai-in-the-creative-process` | 760 | |
| `2026-05-24-the-inside-out-evolution-how-ai-turned-this-old-dogs-brain-inside-out-and-why-youre-next` | 427 | |
| `2026-05-24-the-synthetic-renaissance-beyond-prompts-parameters` | 398 | |
| `2026-05-24-transmuting-words-into-gold-in-the-age-of-ai` | 1463 | |
| `2026-05-24-what-would-chat-do-and-why-thats-the-wrong-question` | 1414 | |
| `2026-05-24-why-100-young-canadians-are-writing-canadas-ai-future-and-why-bc-needs-to-show-up` | 929 | |
| `2026-05-24-zero-to-one-from-meetup-to-movement-bc-ais-grassroots-journey` | 3610 | |
| `2026-05-25-cotton-underwear-paradox` | 1997 | |
| `2026-06-04-ai-keynote-slides-visual-workflow` | 3539 | frontmatter `status: publish` |
| `2026-06-04-canada-ai-for-all-strategy-skeptical-guide` | 3429 | |
| `2026-06-04-the-great-canadian-proximity-game` | 972 | |
| `2026-06-07-god-skills-agentic-loop-workflows` | 2165 | |
| `2026-06-11-vancouver-ai-community-page` | 593 | |
| `2026-06-12-vancouver-world-cup-2026-becker-kk-robots` | 249 | |
| `2026-06-16-storyhive-haus-of-owl-jordan-dack` | 1757 | frontmatter `status: publish` |
| `2026-06-18-creative-ai-human-lab-network` | 973 | |
| `2026-06-23-ethos-lab-block-party` | 1097 | |
| `2026-06-23-vancouver-made-world-cup` | 879 | |
| `2026-06-28-context-creators` | 2309 | |
| `2026-06-28-keep-the-machine-strange` | 2625 | |
| `2026-07-05-artists-learn-machines-extract` | 1344 | has `publish.log` (WP draft staged; not log-only) |
| `2026-07-07-the-cheer-is-a-cap-table` | 1803 | frontmatter `status: publish` |
| `2026-07-18-developing-an-ai-mindset-successor` | 754 | |
| `2026-07-22-twenty-one-years-same-writer` | 1942 | |
| `2026-07-24-accessibility-statement` | 278 | |
| `2026-07-24-sponsor-deck` | 16 | thin; see optional archive above |
| `2026-07-25-accessibility-statement` | 2990 | |
| `2026-07-26-futureproof-festival-announcement` | 1255 | only July-26 dir that is a real post packet |
| `2026-07-31-ai-lands-inside-every-profession` | 905 | |
| `ai-glossary-2026-05` | 1783 | |

### Non-packet work products (21) — keep; not empty shells

These are page redesign / SEO / polish workspaces. Removing them would destroy local ops material.

- `2026-07-26-about-bio-payload`
- `2026-07-26-about-page`
- `2026-07-26-accessibility-statement`
- `2026-07-26-alt-text`
- `2026-07-26-client-logo-soup`
- `2026-07-26-creative-labs`
- `2026-07-26-join-bc-section`
- `2026-07-26-land-acknowledgment`
- `2026-07-26-newsletter-section`
- `2026-07-26-seo-authority-hubs`
- `2026-07-26-services-page`
- `2026-07-26-speaking-page`
- `2026-07-26-speaking-stages`
- `2026-07-26-undesigned-pages`
- `2026-07-26-what-people-say`
- `accessibility-statement-2026-05`
- `accessibility-statement-2026-07`
- `pillars`
- `swarm-ready-pages`
- `wp-draft-10594-post-10594`
- `wp-draft-11178-post-11178`

### Publish residue (1) — keep until KK approves optional archive

- `2026-07-24-contact-421` — see proposed list.

## Method

1. Checked out `main` (clean), pulled `--ff-only`, branched `ops/569-draft-queue-inventory`.
2. Ran `LOCAL_ONLY=1 make draft-queue-audit FORMAT=json` and captured the full local draft list (93 dirs).
3. For every directory under `content/drafts/`:
   - **Real packet** if `post.md` exists with body text (auditor word count > 0, or thin stub with packet companions).
   - **Publish-log-only** if the only file is `publish.log`.
   - **Empty shell** if no post body and only a tiny non-packet note (≤1 small file, no redesign workspace).
   - **Non-packet work product** if auditor reports empty / no `post.md` but disk has README/audit/html/json work files.
   - **Publish residue** if `publish.log` plus snapshots/media and no local post body.
4. For publish-log-only dirs, read `publish.log` for WP id / slug / status; probed live with `curl -sI` only for slugs **explicitly present in the log** (or the unambiguous `?p=` id). Did not guess alternate public slugs beyond following a single 301 from a log-derived URL.
5. No directories deleted or moved. This PR commits **only** this report.

## Definition of done (this phase)

- [x] Classification report covering all `content/drafts/` directories
- [x] Publish-log-only dirs checked against live (without aggressive slug guessing)
- [x] Proposed archive/delete list requires KK approval of exact paths
- [ ] Execution (archive/delete) — **out of scope** until KK approves
