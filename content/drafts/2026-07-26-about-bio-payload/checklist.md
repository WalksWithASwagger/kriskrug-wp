# Snapshot / write / rollback checklist (#290)

**Hard rule:** planning package only until KK signs modules + final HTML. No live WP write from the #290 draft folder alone.

## Pre-flight

- [ ] Confirm lane: Track A body-only About update (page `1208` / slug `about`)
- [ ] Confirm public title stays `About Kris Krüg` (do not send `title` in REST update)
- [ ] Confirm sibling #418 / PR #504 status:
  - [ ] Already applied live, **or**
  - [ ] Merged into the same approved apply HTML as base
- [ ] KK completed pickers in `modules.md` and approved text in `draft-snippets.md`
- [ ] BitTorrent line absent unless authorship credit confirmed
- [ ] Attribution cautions respected (Eriksson Bryght post; Traub Burning Man book)
- [ ] Secrets present for write session: `WP_USER` + `WP_APP_PASSWORD` (length check only; never print)
- [ ] Dry-run path rehearsed; no connector publish without `--dry-run` first if using scripts

## Snapshot (before any write)

- [ ] Authenticated GET `GET /wp-json/wp/v2/pages/1208?context=edit`
- [ ] Save full JSON: `backup/<UTC-timestamp>-about-290/page-1208-before.json`
- [ ] Save `content.raw` alone: `backup/<UTC-timestamp>-about-290/page-1208-before.content.raw.html`
- [ ] Save public rendered HTML: `curl -sL https://kriskrug.co/about/ > backup/<UTC-timestamp>-about-290/about.public-before.html`
- [ ] Record meta: page ID, slug, title, modified GMT, content hash, payload byte length
- [ ] Grep baselines on before HTML:
  - [ ] `public trail` count (expect 0 if #418 Option A already live)
  - [ ] Pack marker `content-architecture-2026:about` present
  - [ ] Rooms / CTA / `/contact/` still present

## Build final payload

- [ ] Start from post-#418 body (live or PR #504 `payload-body.html`)
- [ ] Insert only KK-approved modules from `draft-snippets.md`
- [ ] Keep wrapper `kk-page kk-r9-pack` and pack marker comment
- [ ] Do not change H1/title fields
- [ ] Re-grep payload:
  - [ ] No em dashes in new copy
  - [ ] `public trail` count matches agreed #418 option
  - [ ] Pilot URL present if M1/M2 approved
  - [ ] Land link present if O6 approved
- [ ] Human (KK) reads final HTML once more

## Write (only after sign-off)

- [ ] Body-only REST update: send `content` raw; **omit** `title`, `slug`, `status` changes
- [ ] Prefer idempotent script with slug check `about` → ID `1208` before PATCH
- [ ] Purge Pagely cache for `/about/`
- [ ] Authenticated readback GET; save `page-1208-after.json`
- [ ] Public logged-out fetch; save `about.public-after.html`

## Verify

- [ ] Title still `About Kris Krüg`
- [ ] Approved modules visible; deferred modules absent
- [ ] #418 acceptance still holds (backgrounds/columns/trail copy)
- [ ] Screenshots at 375 / 768 / 1440
- [ ] `/contact/` CTA works
- [ ] If O6: reconciliation link works; footer ack still present
- [ ] No accidental wipe of rooms media cards

## Rollback

If anything is wrong:

1. PATCH `content.raw` from `page-1208-before.content.raw.html` (or full before JSON content field).
2. Purge Pagely `/about/` again.
3. Confirm public HTML matches before hash / spot greps.
4. Stop; do not "fix forward" without a new KK approval.

## Explicit non-actions for this checklist

- Do not edit `theme/kk-aurora/templates/single.html` in the same commit/write as About body.
- Do not publish archive-series posts as part of the About PATCH.
- Do not update footer land copy from this About payload unless KK opens that lane separately.
