# Swarm batch: Futureproof Festival announcement post (kriskrug.co)

Staged 2026-07-26. Source plan: `~/.claude/plans/goal-hey-it-s-kris-hashed-firefly.md`.
Track A (content). One post, decomposed into an epic + 4 swarmable issues across 3 waves.
**Nothing here publishes.** Wave 3 stops at a verified WP *draft* + preview URL; public publish needs KK sign-off.

Filing order: epic first, then FP-1..FP-4 (so they can reference the epic number). All target
`WalksWithASwagger/kriskrug-wp`. Repo convention: create-only, slug-based idempotency, 2026-05-15 incident rules apply.

Dependency graph:
```
Wave 1 (parallel):   FP-1 assets ──┐        FP-2 speakers ──┐
                                    ├──────────────────────┤
Wave 2:                             └──►  FP-3 write post  ◄┘
Wave 3:                                        └──►  FP-4 verify + create draft
```

---

## EPIC — [EPIC] Futureproof Festival announcement post (Track A)

**Labels:** `content`, `priority:high`, `swarm-ready`

Kris is launching **Futureproof Festival** (Oct 28-30, 2026, H.R. MacMillan Space Centre, Vancouver — presented by BC + AI). This epic ships one showpiece story post on **kriskrug.co**, in KK's voice, that tells the whole origin arc (the **FATALE** dream — *Future of Art, Technology and Alternative Living Experiment* — growing up into Futureproof), puts out a "bat signal" to the people he's built with over 28 years to converge on Vancouver in October, links out to the Futureproof site / Luma / BC+AI / his companion posts, brings in festival design assets, and announces the public speaker lineup.

**Anchor facts (do not drift):** Oct 28-30, 2026 (ignore stale week-long "Oct 25-31" dates). Public line "The most honest AI conversation happening anywhere this year. No hype. No panic." Tagline "Build what lasts." Earlyworm pass CA$650 (priority ends Aug 15), Call for Talks priority Jul 31. BC+AI receipts: 250+ members / 3,000+ attendees / 94+ events. Site `https://futureproof.website/`, RSVP `https://luma.com/futureproof-festival`.

**Voice gate (hard):** no em dashes, no AI voice. See `~/.claude/.../memory/kk-no-em-dashes-no-ai-voice.md`, `kk-voice-cheatsheet.md`, `content-showpiece-standard.md`.

**Sub-issues:** FP-1 (assets) · FP-2 (speakers) · FP-3 (write) · FP-4 (verify + draft).

- [ ] All four sub-issues merged / completed
- [ ] Verified WP **draft** exists with preview + edit URL logged; KK reviewed
- [ ] Publish decision made by KK (out of scope for the swarm)

---

## FP-1 — [CONTENT] Futureproof post: stage design assets + alt text

**Labels:** `content`, `priority:medium`, `swarm-ready`, `swarm-wave-1`, `agent-safe`
**Depends on:** none (Wave 1) · **Blocks:** FP-3, FP-4

Curate the festival design assets the announcement post will feature and stage them into the draft package with real alt text. No writing, no WP calls.

### Scope
Create `content/drafts/2026-07-26-<slug>/images/` and copy in:
- **1 hero poster** (becomes `featured_media_id`) — prefer a web-optimized production asset, e.g. `~/Code/futureproof-festival/public/graphics/honest-conversation/futureproof-honest-conversation-poster.png` or an aurora poster.
- **1 wordmark** — `~/Code/futureproof-festival/public/brand/futureproof/futureproof-wordmark-*` (pick the variant that reads on kriskrug.co's background).
- **2-3 gallery posters** — from `~/Code/futureproof-festival/public/graphics/` or `public/media/gallery/` (aurora / surrealist / dreamscape).

Write `content/drafts/2026-07-26-<slug>/asset-manifest.md`: each file → source path, chosen role (hero / wordmark / gallery-N), and a specific, descriptive alt string (KK alt style, no "image of").

### Source of truth
Prefer human-approved production assets in `~/Code/futureproof-festival/public/`. Exploration library `~/Code/kk-kb/content/projects/02-bc-ai-ecosystem-nonprofit/events/2026/bc-ai-festival-week/branding/outputs/` (242 files, `gallery.html` index) is fallback only.

### Acceptance criteria
- [ ] `images/` contains 4-6 files, each with a real alt string in `asset-manifest.md`
- [ ] One file explicitly designated hero/featured
- [ ] Filenames are web-safe; no absolute `/Users/` paths written into any tracked file
- [ ] No binaries opened/edited; assets copied as-is

---

## FP-2 — [CONTENT] Futureproof post: verify + assemble public speaker lineup

**Labels:** `content`, `priority:high`, `swarm-ready`, `swarm-wave-1`, `needs-human-review`
**Depends on:** none (Wave 1) · **Blocks:** FP-3

⚠️ **Safety-critical: active speaker embargo.** Only speakers cleared for public may appear in the post. Read-only against the festival repo. **Never edit** `speaker-roster-allowlist.json`.

### Scope
For the 8 speakers publicly listed on futureproof.website — Amber Case, Ana Serrano, Lynda Brown-Ganzert, Gabriel "Zaro", Anthonia Ogundele, Mayumi Rollings, Peter Bittner, Kaoru Yoshihira — confirm each is public/authorized, then produce `content/drafts/2026-07-26-<slug>/speakers.md`: cleared name → affiliation → link (their `futureproof.website/speakers/<slug>` page or own site). Flag and **drop/hold** anyone not cleared.

### Source of truth (read-only)
- `~/Code/futureproof-festival/data/speaker-roster-allowlist.json` (authorization gate — read only)
- `~/Code/futureproof-festival/data/speaker-pipeline.json` (status: brainstorm/conversation/verbal-yes/confirmed)
- `~/Code/futureproof-festival/lib/speakers.ts` (`confirmed: true` are publishable)
- Cross-ref: `~/Code/futureproof-festival/docs/internal/ops/speakers/roster-pipeline-reconciliation-2026-07-18.md`

### Acceptance criteria
- [ ] Every name in `speakers.md` is verified public/authorized against the allowlist + pipeline (cite the status)
- [ ] Any non-cleared name is listed under a "HOLD — do not announce" section, not in the publish list
- [ ] Each cleared speaker has affiliation + a live link
- [ ] `speaker-roster-allowlist.json` untouched

---

## FP-3 — [CONTENT] Futureproof post: write the story in KK voice

**Labels:** `content`, `priority:high`, `swarm-wave-2`, `needs-human-review`
**Depends on:** FP-1 (assets), FP-2 (speakers) · **Blocks:** FP-4

Write the post: `post.md` (frontmatter + body) and `post.html` (Gutenberg body from `wp_blocks.py`), plus the SEO side files. This is the creative core — KK reviews voice before it moves to FP-4.

### Story arc (~900-1200 words, em-dash-free)
1. The baby is here. Futureproof. Oct 28-30, Vancouver, the Space Centre. (pull quote)
2. The dream: "I have long dreamt of an avant-garde festival of the future."
3. **FATALE origin:** it started as an idea I called FATALE — the Future of Art, Technology and Alternative Living Experiment — and kept evolving until this was it.
4. Meetup → festival truth: "I didn't start these meetups to start a meetup." BC+AI receipts. The Space Centre comes home.
5. What Futureproof is: honest AI conversation, no hype no panic; listening / making / experiencing; festival not conference; "critique in one hand, curiosity in the other"; "Build what lasts."
6. The speakers (from FP-2 `speakers.md`), each linked, "more to come."
7. The bat signal: 28 years on the internet, third trip around the sun, converge on Vancouver in October. (pull quote)
8. CTA: RSVP on Luma; Earlyworm pass (CA$650, ends Aug 15); Call for Talks (Jul 31); sponsor/exhibit. All linked.

### Build rules
- Frontmatter contract: mirror `content/drafts/2026-05-13-sovereign-ai-for-whom/post.md` (`title, slug, post_date: '2026-07-26', status: draft, post_type: post, author_wp_id: 1, categories, tags, featured: true, featured_media_id, excerpt, seo{meta_title, meta_description}, images[{file, alt}]`).
- `post.html` built from `scripts/notion-to-wp/wp_blocks.py` helpers: `hero_image` (FP-1 hero), `inline_image`@460 (wordmark), `gallery` (FP-1 posters), `pullquote`, `heading`, `inline` (links/bold), `separator`. Showpiece reference: `content/drafts/2026-05-23-you-cant-drink-data/`.
- Links: futureproof.website (+/speakers,/tickets,/call-for-talks), luma.com/futureproof-festival, bc-ai.ca(+/events), vancouver.ai, companion posts `kriskrug.co/2026/06/01/long-road-to-futureproof/` and `kriskrug.co/2024/10/10/future-proof-inside-vancouvers-thriving-ai-ecosystem/`; optional lineage `fatalefestival.com`.
- Also write `seo-meta.md`, `alt-text.md`, `internal-links.md`.

### Acceptance criteria
- [ ] `post.md` + `post.html` + 3 SEO side files present; frontmatter valid; `post.html` contains `<!-- wp:` blocks
- [ ] Zero em dashes (`grep -c '—'` → 0); no AI tropes
- [ ] Every person/org/project hyperlinked; ≥2 pull quotes; ≥1 gallery; images placed contextually
- [ ] FATALE acronym spelled out once; dates/prices/receipts match anchor facts
- [ ] Speakers exactly match FP-2 cleared list

---

## FP-4 — [CONTENT] Futureproof post: verify + create WP draft (no publish)

**Labels:** `content`, `priority:high`, `swarm-wave-3`, `needs-human-review`, `deployment`
**Depends on:** FP-3 · **Blocks:** none

Final gate. Run the full verification battery, then create the kriskrug.co **draft** via the local publisher. **Never `--publish`.**

### Steps
1. Voice: run `voice-slop-audit` skill on the draft; assert `grep -c '—' post.md post.html` → 0.
2. Speaker embargo re-check: names still match FP-2 cleared list.
3. Fact check: dates (Oct 28-30), venue, prices (CA$650 / Aug 15 / Jul 31), receipts (250+/3,000+/94+).
4. Links live: `curl -I` each external URL → 200/live.
5. Dry run: `scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/create_local_wp_draft.py content/drafts/2026-07-26-<slug>/post.md` — passes quality gate + slug is create-only available.
6. Create draft: re-run with `--execute` (auth via `make varlock-run CMD='...'` or `WP_USER`/`WP_APP_PASSWORD`). Publisher uploads images, sets featured, reads back and asserts `status==draft`. Log WP id + edit/preview URL to `publish.log`.

### Safety (2026-05-15 incident rules)
- Create-only; if slug already exists → **abort**, do not PATCH/overwrite.
- Draft only. Public publish / `--update` requires explicit KK sign-off + `--diff` review — out of scope here.

### Acceptance criteria
- [ ] voice-slop-audit clean; zero em dashes
- [ ] All external links return live
- [ ] Dry run passes; slug create-only available
- [ ] WP **draft** created; `status==draft` confirmed on readback; id + preview URL in `publish.log`
- [ ] No publish performed; handed to KK for review
