# Placement recommendation (#22)

## Decision frame

#22 allows footer **or** About. Live site already uses footer. About body currently has no land module. Dedicated Reconciliation page holds the long form + Nation links.

## Recommendation

| Placement | Action | Timing |
|---|---|---|
| Footer brand tile | Keep always-on. Prefer Option A wording from `copy-options.md`. | Track B theme edit after KK picks copy (`parts/footer.html`) |
| Footer bottom | Keep `Reconciliation` link (already live). Do not duplicate a second ack paragraph in the bottom bar. | None unless label tweak |
| About body | Optional Option C / #290 O6 **after** #418 ships. Do not add to #418 `payload-body.html`. Skip on first #290 write by default. | Later Track A page body write |
| Reconciliation page | Keep as canonical long form + Nation links. Optional micro-polish only with separate KK approval. | Out of scope for this packet unless KK asks |

## Why footer first

1. Acceptance allows footer alone; it is already sitewide and mobile-rendered in Aurora.
2. #290 explicitly deferred land acknowledgment out of the first About body slice.
3. #418 is a layout/background/"public trail" packet. Injecting land copy there mixes concerns and risks merge conflict with that draft PR.
4. A buried one-liner inside a services sentence is easier to miss than a dedicated acknowledgment sentence. Improving the footer copy addresses visibility without a second surface.

## Coordination with #290

Source pack (historical): `content/source-packs/content-architecture-2026/about-bio-payload-plan-2026-07-08.md` deferred About-body rewrite.

Sibling draft (active): `content/drafts/2026-07-26-about-bio-payload/land-acknowledgment.md` reaches the same verdict: footer is primary sitewide home; About-body O6 is optional values reinforcement, not a second system. O6 placement: **after Receipts / origin beat, before CTA**. Default first #290 write: **skip O6**.

This #22 packet owns footer tone options + WCAG/nation-link notes. It does not replace #290's About payload plan. If both packages propose About copy, prefer one KK-approved module (O6 or Option C), not both.

## Coordination with #418

`content/drafts/2026-07-26-about-page/` (branch `cursor/418-about-page-draft-f196`) owns About CSS/grid and "public trail" copy. Land acknowledgment is **not** in that payload. Leave it out.

If KK later wants Option C / O6 on About:

1. Let #418 apply (or explicitly supersede) first.
2. Snapshot page 1208 again.
3. Append one land section after Receipts / before CTA, matching #418 paper/panel tokens.
4. Do not reopen "public trail" copy in the same commit.
5. Do not ship competing O6 + Option C blocks.

## Implementation lanes (when KK approves)

- **Footer wording change:** Track B. Edit `theme/kk-aurora/parts/footer.html`, bump theme Version per Aurora practice, deploy with KK go-ahead.
- **About Option C:** Track A. Body-only REST update to page 1208 after snapshot; no title change.
- **Nation links in footer paragraph:** Optional. Prefer linking the existing Reconciliation route rather than three external Nation URLs in small footer type (see `nation-links.md` and `wcag-notes.md`).

## Anti-conflict checklist

- [ ] No edits to `content/drafts/2026-07-26-about-page/` from this issue
- [ ] No competing rewrite of `content/drafts/2026-07-26-about-bio-payload/` O6 from this issue (reference it; do not fork)
- [ ] No About body land module in the same PR as #418 unify
- [ ] No live WP write from this draft package
- [ ] Theme footer change lands in a Track B commit if/when approved
