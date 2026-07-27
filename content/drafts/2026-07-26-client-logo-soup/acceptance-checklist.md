# Acceptance checklist (#413)

Draft package status as of 2026-07-26. Theme/live apply stays blocked until gates below clear.

## Issue acceptance criteria

| Criterion | Status | Notes |
|-----------|--------|-------|
| Source inventory of Peter-era logo/testimonial assets documented | **Done (draft)** | `inventory.md`; mirrored intent of 2026-07-19 issue comment; refreshed with media API + Upgrade site wrap |
| Logo band ships with ≥8 client logos, monochrome at rest | **Blocked** | No client logo files in repo/media; markup sketch ready in `proposed-html.html` |
| Hover/focus interaction works with mouse and keyboard | **Spec ready** | `treatment.md` + `proposed-css.css` + enhancer sketch; not live |
| KK approves the client list before go-live | **Needs KK** | `client-list-for-kk.md` |

## Evals / verification (when building)

- [ ] Each logo media URL returns HTTP 200
- [ ] Aspect ratios correct (`object-fit: contain`; no crop of wordmarks)
- [ ] `alt` text = client name only
- [ ] Monochrome treatment consistent at rest (no stray full-color mark)
- [ ] Screenshots at 375, 768, 1440; wrap is graceful
- [ ] No layout shift when hover/focus activates (shared readout, fixed cell size)
- [ ] Keyboard: Tab reaches each logo control; focus-visible ring visible; readout updates
- [ ] `prefers-reduced-motion` path checked
- [ ] Voice: no em dashes in section copy; no "Fortune 500" claim

## Safety / collision

- [x] No live WP writes in this packet
- [x] No theme file edits on this branch (avoids stomping #505 newsletter PR)
- [x] Section id/classes distinct from `#newsletter` / `aurora-newsletter-band`
- [x] Does not replace `#stages` text proof strip
- [ ] Homepage snapshot before any future live insert
- [ ] Aurora package / version bump only on Track B apply commit
- [ ] Rollback: remove section HTML + CSS; purge cache

## KK / Peter unblock list

- [ ] Approve ≥8 names on `client-list-for-kk.md`
- [ ] Deliver logo files (or folder URL)
- [ ] Pick copy option in `copy.md` (A wired)
- [ ] Confirm hover mode: color / note / both (both recommended)
- [ ] Confirm placement: after `#stages` (recommended) vs after work-band

## Exit criteria for "draft packet complete"

This PR meets the draft-only swarm brief when:

1. Inventory, treatment, copy, acceptance checklist, and proposed markup/CSS are committed.
2. Client list approval sheet is ready for KK.
3. No live or theme collision with #505.
