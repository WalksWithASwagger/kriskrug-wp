# Publish gate - land acknowledgment (#22)

**Mode:** draft package for KK. No live WordPress write and no theme deploy from this packet.

## Already true on production (do not "add from zero")

- Footer brand tile includes Musqueam / Squamish / Tsleil-Waututh unceded territories line.
- Footer bottom links to `/reconciliation-indigenous-land-acknowledgement/`.
- Dedicated Reconciliation page includes Coast Salish framing, three Nations, and Nation website links.

## Human gates before any change

- [ ] KK picks a copy option in `copy-options.md` (or "keep baseline / close as visible").
- [ ] KK confirms Musqueam remains named (recommended for Vancouver).
- [ ] KK confirms placement: footer only / About later / both.
- [ ] KK confirms Nation-link strategy in `nation-links.md`.
- [ ] If footer wording changes: Track B PR for `theme/kk-aurora/parts/footer.html` + theme version bump + deploy approval.
- [ ] If About Option C: wait until #418 is applied or explicitly deferred; fresh snapshot of page 1208; body-only update; no title change.
- [ ] Dry-run / screenshot review at 375 / 768 / 1440.
- [ ] WCAG smoke from `wcag-notes.md`.
- [ ] Pagely purge for touched routes after live apply.
- [ ] Rollback path: restore prior footer part or About `content.raw` snapshot.

## Do not

- Patch live WP from this folder.
- Edit #418 About payload files in the same change set.
- Claim Nation consultation or endorsement.
- Ship Unicode footer autonyms without a font/AT smoke.
- Use em dashes in approved copy.

## Suggested issue close conditions

Close #22 when KK either:

1. Accepts live baseline as meeting "visible" (footer + Reconciliation page), or
2. Approves and ships footer Option A/B (and optionally schedules About Option C after #418).
