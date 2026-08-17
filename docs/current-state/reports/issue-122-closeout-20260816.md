# Issue #122 closeout — 2026-08-16

**Lane Y (verify / closeout).** Docs only. No WordPress write, no theme edit, no issue close.
**Probe UTC:** `2026-08-17T02:40:10Z`
**Live theme readback:** Aurora **1.6.5** (`style.css` `Version:`). Repo `main` is ahead; this pass measured production.
**Parent:** [#122](https://github.com/WalksWithASwagger/kriskrug-wp/issues/122)
**Prior evidence:** [2026-08-02 inventory](../UNDESIGNED-PAGES-INVENTORY-2026-08-02.md) (PR [#654](https://github.com/WalksWithASwagger/kriskrug-wp/pull/654)); [2026-08-16 recheck](undesigned-pages-recheck-20260816.md) (PR [#809](https://github.com/WalksWithASwagger/kriskrug-wp/pull/809)).

## Verdict

**Not closeable.** Inventory and disposition work is done. The live defect is not. All 24 undesigned pages from the inventory still render as bare title + legacy body. Original acceptance still has unchecked boxes for consistent spacing/hero treatment and for actually applying the generic-vs-bespoke plan.

Do not paste a closing comment. Keep #122 open until a follow-up actually changes live pages (redesign, retire/redirect, or a KK wont-fix on the whole long tail).

## What is done

| Deliverable | State |
|---|---|
| Approach defined (improve `page.html` + three sub-templates, four waves) | Done — inventory PR #654 |
| Prioritized list (bespoke vs template polish vs retire) | Done — 6 must-fix / 13 later / 5 close-as-wont-fix in PR #809 |
| Services page redesigned (`/generative-ai-services/`) | Still holds — live 200, **not** bare (inline `<style>` in `entry-content`; zero non-wrapper `aurora-*` tokens) |
| 2026-08-16 recheck of all 24 | Merged as PR #809 — 24/24 still HTTP 200, still bare, none redirected, none noindexed; published page set still 46 IDs |
| This closeout spot-check | 5/5 sampled pages still match the recheck PASS (still-bare) |

Issue comments already recorded Services as redesigned and the hardcoded-template retirement (PR #135). That AC item is the only live-design win on this issue.

## Independent spot-check (logged-out)

Same discriminator as PR #809: non-wrapper `aurora-*` class tokens inside `entry-content` (excluding `aurora-page-content` / `aurora-prose` that `page.html` always injects) plus inline `<style>`. Zero non-wrapper tokens and no inline style = still bare.

| URL | Recheck claimed | This pass | Match? |
|---|---|---|---|
| [/privacy-policy/](https://kriskrug.co/privacy-policy/) (must-fix, footer Utility) | 200, still bare, no redirect, not noindex | 200, tokens=`aurora-page-content aurora-prose` only, no `<style>`, robots=`max-image-preview:large` | **PASS** |
| [/glossary/](https://kriskrug.co/glossary/) (must-fix, SEO) | same | same | **PASS** |
| [/the-kk-worldview/](https://kriskrug.co/the-kk-worldview/) (must-fix, copyright bar) | same | same | **PASS** |
| [/japanese-introduction-page-kaykaysan/](https://kriskrug.co/japanese-introduction-page-kaykaysan/) (later, multilingual) | same | same | **PASS** |
| [/subscribe/](https://kriskrug.co/subscribe/) (retire candidate) | same | same; beehiiv iframe still present | **PASS** |

**PASS:** 5/5 sampled pages still match the recheck.
**PASS:** `GET /wp-json/wp/v2/pages?per_page=1&status=publish` → `X-WP-Total: 46` (unchanged).
**PASS:** `/generative-ai-services/` still not bare (inline style present).
**NOT-RUN:** remaining 19 of 24 pages (sample only; no reason to expect a different result given the identical 46-ID page set).
**NOT-RUN:** inbound-link recrawl of 970 posts (out of scope; counts carried from 2026-08-02).

Commands: logged-out Python `urllib` GETs, custom UA `kriskrug-wp-issue-122-closeout/1.0`, no cookies, no auth. Zero writes against kriskrug.co.

## Residue — #122 is not closeable

Original acceptance criteria:

- [x] Define an approach
- [x] Services page redesigned
- [ ] Consistent spacing/hero treatment across content pages — **not implemented**
- [x] Prioritized list of bespoke vs template polish

The third box is the live work. PR #809's "close-as-wont-fix" row means *recommend retire instead of redesign*, not *already resolved*. None of those five are redirected or noindexed.

### Remaining pages that still need a decision (do not file from this lane)

Residue is **24 pages**, not a crisp ≤3-page slice. Do not open follow-ups from this closeout. Candidates if KK splits the epic later:

**Follow-up A — must-fix (6), public chrome / highest signal**

- `/reconciliation-indigenous-land-acknowledgement/` (3899) — footer copyright bar
- `/the-kk-worldview/` (3948) — footer copyright bar
- `/motleykrug-podcast/` (2828) — footer Site tile
- `/privacy-policy/` (2985) — footer Utility tile
- `/glossary/` (11887) — best SEO asset in the set
- `/ai-upgrade-for-creative-professionals/` (6770) — highest inbound-linked offer

**Follow-up B — later (13), template polish**

- `/cinematic-podcasts-hollywood-grade-storytelling-meets-generative-ai/` (7764)
- `/generative-ai-workshop-for-artists-creatives/` (2603)
- `/art-island-perspectives-from-a-creative-community/` (2543)
- `/sponsor-cyberpunk-chronicles-newsletter/` (3969)
- `/product-review-policy-instructions/` (3974)
- `/ai-upgrade-for-modern-media-leaders/` (7610)
- multilingual cluster (7): `/japanese-introduction-page-kaykaysan/` (3595), `/chinese-introduction-kang-jia/` (3598), `/russian-introduction-kristofor-kruglov/` (3600), `/farsi-introduction-khalil-khalifa/` (3601), `/hindi-introduction-krishna-vishwanathapriyadhanvanshi/` (3606), surviving Swahili `/karibu-kwenye-kabila-la-kidijitali-.../swahili-welcome-page/` (3623), `/urdu-language-introduction-kris-krug/` (3696)

**Follow-up C — retire/redirect (5), KK go/no-go still open since 2026-08-02**

- `/home/` (2315) — orphan duplicate of `/`
- `/news/` (2389) — press links already on `/publications/`
- `/subscribe/` (2808) — header already links beehiiv
- `/swahili-introduction-kintu-krowfeather-.../` (3603) — duplicate of 3623
- `/ai-upgrade-community-coaching-w-kris-krug-peter-bittner/` (6755) — possibly dead offer; KK question unanswered

## Ready-to-paste comment — do not use to close

#122 is **not** closeable. If KK wants a comment on the issue (keep-open, not a close):

```
Lane Y closeout 2026-08-16 (spot-check of PR #809, not a close).

Not closeable. The 2026-08-16 recheck still holds: 5/5 sampled pages
(/privacy-policy/, /glossary/, /the-kk-worldview/,
/japanese-introduction-page-kaykaysan/, /subscribe/) are HTTP 200,
still bare (only page.html wrappers aurora-page-content + aurora-prose,
no inline <style>, not noindexed). Live theme 1.6.5. Published page
set still 46 IDs. /generative-ai-services/ remains the one designed
win (inline CSS, not bare).

Done: approach, prioritized list, Services page, inventory (#654),
recheck (#809). Not done: consistent spacing/hero treatment on the
24, and the Wave-1 retire/redirect go/no-go.

Keep open. Do not split into follow-ups until KK picks a slice
(must-fix 6 / later 13 / retire 5). Report:
docs/current-state/reports/issue-122-closeout-20260816.md
```

## Next step

KK: pick one slice. Cheapest is Follow-up C (four redirects plus a yes/no on page 6755). Highest visible leverage is Follow-up A (the four footer pages every visitor sees). This lane does not implement either.
