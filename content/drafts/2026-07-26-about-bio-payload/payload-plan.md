# Payload plan - About/bio archive consolidate (#290)

**Mode:** DRAFT / PLAN ONLY. Do not PATCH live WP from this package without KK approval, human-reviewed final HTML, authenticated snapshot, and a rollback path.  
**Target:** page ID `1208`, slug `about`, URL https://kriskrug.co/about/  
**Update type:** body-only (`content.raw`). Do not send `title`, `slug`, or SEO plugin fields unless KK explicitly approves a separate title change.  
**Related:** #269, #270, #22; sibling layout/copy package PR #504 (`content/drafts/2026-07-26-about-page/`)

## Public title freeze

Live public title (authenticated REST public readback 2026-07-26):

| Field | Value | Action |
|---|---|---|
| WP `title.rendered` | `About Kris Krüg` | **Preserve** |
| Visible H1 | `About Kris Krüg` | **Preserve** |
| Document `<title>` | `About Kris Krüg \| AI Speaker, Creative Technologist & Community Builder` | Out of scope unless KK opens SEO title work |
| `og:title` / `twitter:title` | `About Kris Krüg` | Out of scope for this body pass |

**Rule:** this plan never changes the public page title. If KK wants a new title later, that is a separate, explicitly approved edit with its own snapshot note.

## What live About already does (2026-07-26)

Body is a single `<!-- wp:html -->` pack (`content-architecture-2026:about`):

1. Lead (kicker `About` + display H2 + two paragraphs)
2. Rooms (four media cards)
3. Trail / receipts (four proof cards; still says `Public trail` twice on live until #418 applies)
4. CTA (`Start with the work` → `/contact/`)

Site chrome (footer) already carries a short land line pointing at Musqueam, Squamish, and Tsleil-Waututh, plus a Reconciliation link. About body does **not** currently hold a dedicated land-acknowledgment section.

## Goals (acceptance from #290)

1. Review pilot-school story (#269) and archive-mining findings (#270).
2. Produce a body-only payload **plan** that preserves the public title unless KK approves a change.
3. Say where #22 land acknowledgment should live, if natural.
4. Separate must-have bio additions from optional archive/story modules.
5. Include snapshot / write / rollback for the eventual live update.
6. Keep final payload human-reviewed before any WordPress write.

## Scope boundaries

| In scope for eventual #290 write | Out of scope |
|---|---|
| Additive About body modules (pilot beat, credential lines, optional story cards) | Changing WP title / H1 / slug |
| Placement notes that respect the post-architecture pack structure | Restoring pre-2026-07 "Five rooms" / Beastie Boys / gallery About |
| Checklist for body-only REST update | Live WP write in this PR |
| Optional draft snippets for KK to approve | Wholesale replace with `fixes/UPDATED-ABOUT-PAGE-COMPLETE.md` |
| Coordination with #418 layout base | Competing full `payload-body.html` that duplicates PR #504 CSS |
| Flag short-bio pilot mention as a **separate** decision | Editing `theme/kk-aurora/templates/single.html` in this Track A commit |
| Flag homepage hero / persona-guide mentions as optional later | Homepage pattern or docs voice-guide edits here |

## Recommended page composition (after #418 base)

Keep the four-section pack. Insert archive texture as **small additive modules**, not a second About page:

```text
[Lead]          keep; optional one-sentence personal beat in body para 2
[Rooms]         keep (current work)
[Receipts]      keep (#418 Option A preferred); enrich card 1 credentials if KK wants
[Origin beat]   NEW optional section: Photography + flying (pilot school)
[Land & values] NEW short About-body ack ONLY if KK wants page-local visibility beyond footer
[CTA]           keep
```

Default recommendation: ship **must-have credential enrichments + one short pilot origin beat**, skip optional archive series modules on the page itself (those become posts).

## Sequencing with PR #504 / #418

1. **#418 first (preferred):** apply layout unify + kill double `public trail` from `content/drafts/2026-07-26-about-page/`.
2. **Then #290:** graft approved modules from `draft-snippets.md` into the post-#418 body (or into a merged apply-ready HTML KK signs once).
3. **Do not** open two concurrent live About writes. One snapshot, one approved body, one write.
4. If KK wants a single combined apply: take #418 `payload-body.html` as base, insert #290 snippets, re-run greps (`public trail`, pack marker), then one PATCH.

## Must-have vs optional (summary)

Full table in `modules.md`.

- **Must-have (About body):** short pilot-school origin beat tied to photography; high-confidence credential lines already half-present (TEDxOilSpill) plus Bryght / Northern Voice / Vancouver AI → BC+AI if KK confirms wording; link back to 2013 pilot post where it fits.
- **Optional (About body or later posts):** aerial/drone bridge, Galiano/Feelmore, PopTech/COP15 expansion, BitTorrent authorship (gated), full "From the Archives" series posts, short-bio "...and licensed private pilot", homepage hero tagline.

## Land acknowledgment (#22)

See `land-acknowledgment.md`. Default: **footer remains primary sitewide home**; About body gets a short "Land & values" paragraph only if KK wants the About narrative to state Indigenous sovereignty as foundational (it already does in older long-form drafts and Indigenomics work). Always link to `/reconciliation-indigenous-land-acknowledgement/`. Match live nation naming (Musqueam, Squamish, Tsleil-Waututh under Coast Salish), not the looser #22 issue phrasing alone.

## Author bio / theme note (not this body write)

`theme/kk-aurora/templates/single.html` short bio:

> Kris Krug is an AI keynote speaker, creative technologist, photographer, and community builder working across BC + AI, Vancouver AI, and Futureproof Festival, and a living network of AI-era projects.

#269 optional append: `...and licensed private pilot`. That is Track B / theme if edited in template, or a separate content decision. **Do not mix into the About body PATCH.**

## Human review gate

Before any live write:

- [ ] KK picks modules from `modules.md`
- [ ] KK approves or rewrites snippet text in `draft-snippets.md`
- [ ] Confirm BitTorrent line stays **off** until authorship credit is verified
- [ ] Confirm #418 copy option (A recommended) is either already live or merged into the same payload
- [ ] Title field remains `About Kris Krüg` (unchanged)
- [ ] Checklist in `checklist.md` completed through pre-edit snapshot
