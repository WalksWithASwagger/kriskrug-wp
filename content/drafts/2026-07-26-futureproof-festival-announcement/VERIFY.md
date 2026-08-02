# VERIFY — Futureproof Festival announcement (#500 / FP-4)

**Package:** `content/drafts/2026-07-26-futureproof-festival-announcement/`  
**Slug:** `futureproof-festival-announcement`  
**Target status:** WordPress `draft` only. Never `--publish`. Never `--update` / PATCH.  
**Verified:** 2026-07-26 (cloud swarm agent, credential-free path); body rewritten 2026-08-02 for #645 (see note below); this file's own checklists below are **not yet re-run against the #645 body** and remain #500's job to re-verify before any draft create.

## #645 rewrite note (2026-08-02) — re-verify before #500 acts

`post.md` and `post.html` were substantially rewritten under #645 (new title "The Bat Signal," new lead image, conference-lineage receipts section, no hard-coded speaker list). The completeness table, em-dash count, speaker-embargo check, fact table, and link count below describe the **July 26 / early-August small-fix body**, not this new one. Before #500 runs any dry-run or draft-create command, re-run this file's checks against the current `post.md`/`post.html`. As a head start, the #645 rewrite pass already confirmed:

- Em dashes: 0 in both `post.md` and `post.html` (re-checked 2026-08-02, same method as below).
- Links: 17 unique URLs in the new body (down from 34; the hard-coded speaker/org list and FATALE links were removed, see `internal-links.md`), all HTTP 200 on 2026-08-02.
- Speaker embargo: no individual speaker names appear in body copy at all now; the roster is linked, not listed, so the FP-2 embargo table in `speakers.md` is no longer a publish-blocking dependency for this piece (see `speakers.md`'s #645 addendum).
- Facts: dates, venue, Earlyworm CA$650/August 15, Call for Talks August 15, and 300/3,000+/94+ receipts are all current in the new body as of 2026-08-02 (sourced live from futureproof.website and KK's 2026-08-01 membership ruling).
- New dependency for #500: the two Meetup #31 photos used as lead + supporting images are staged locally but are **unresolved hotlinks with no written cross-site reuse release** (see `asset-manifest.md`). #500 should not treat them as upload-ready without Kris's explicit sign-off, same as every other image in this package.

### Dry-run executed 2026-08-02 (offline, no credentials, no WP writes)

```
scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/create_local_wp_draft.py \
  content/drafts/2026-07-26-futureproof-festival-announcement/post.md
```

**First run FAILED**, and the failure was real, not environmental:

```
ERROR: while parsing a block mapping
expected <block end>, but found '<scalar>'
```

Two alt values contained `Meetup #31`. In YAML a whitespace-preceded `#` opens a comment, so the alt scalar truncated mid-sentence and the folded continuation line broke the block mapping. `post.md` would not load at all, meaning #500 could not have dry-run or created anything. Fixed by single-quoting both values (commit `91ab3f1`); the `#31` text and line folding are preserved.

**Re-run PASSES.** Result:

| Field | Value |
|---|---|
| `dry_run` | `true` |
| `title` | The Bat Signal |
| `slug` | `futureproof-festival-announcement` |
| categories | Vancouver AI Ecosystem |
| tags | Futureproof, BC + AI, Vancouver AI, Festival, Space Centre, Build What Lasts |
| images resolved | 7 (all local files exist; wordmark correctly absent) |
| `slug_check` | `skipped_offline` |

**What this does and does not prove.** It proves the quality gate passes, the frontmatter parses, the payload shape is valid, and every referenced image resolves to a real local file. It does **not** prove the slug is free: the dry-run path is deliberately offline (`dry_run_wp_config()`, no authenticated probe), so `slug_check` is `skipped_offline`. The create-only slug collision check (`assert_slug_available`) runs only on the `--execute` path. #500 still owns that check, and must still abort on collision rather than PATCH.

## Verdict

Package is **complete and verification-ready**.  
**WP draft was NOT created** in this session: `WP_USER` / `WP_APP_PASSWORD` are unset, and `create_local_wp_draft.py` hard-exits without credentials even in dry-run (per AGENTS.md / connector README).

Hand to KK (or a secrets-attached session) for dry-run → `--execute` create-only, **after** re-running this file's checklists against the #645 body.

---

## Package completeness (#500 acceptance)

| Artifact | Status |
|---|---|
| `post.md` frontmatter (title, slug, status=draft, categories, tags, excerpt, seo, images[]) | PASS |
| `post.html` Gutenberg `<!-- wp:* -->` body (40 block markers) | PASS |
| `seo-meta.md` | PASS |
| `alt-text.md` | PASS |
| `internal-links.md` | PASS |
| `speakers.md` (FP-2 cleared 8) | PASS |
| `asset-manifest.md` + `images/` (6 binaries, hero designated) | PASS |
| `VOICE-NOTES.md` | PASS (from #499) |

Sources assembled on branch `cursor/500-futureproof-wp-draft-prep-f196`:

- Story / SEO / HTML: `origin/cursor/499-futureproof-story-f196`
- Images + asset-manifest: `origin/cursor/497-futureproof-assets-f196`
- Speakers: `origin/cursor/498-futureproof-speakers-f196`

---

## Issue #500 step checklist

### 1. Voice / em dashes

- [x] Em dash count: `grep -c '—' post.md post.html` → **0 / 0**
- [x] Light slop banlist scan (delve / tapestry / realm / seamless / game-changer / utilize / harness / "it's not just"): **none**
- [ ] Full `voice-slop-audit` skill: **not present in this repo** (no SKILL.md / script found). Mechanical checks above + `VOICE-NOTES.md` stand in; KK should still do a human voice pass before public publish.

### 2. Speaker embargo re-check

- [x] Body names match FP-2 cleared list in `speakers.md`: Amber Case, Ana Serrano, Lynda Brown-Ganzert, Zaro, Mayumi Rollings, Anthonia Ogundele, Kaoru Yoshihira, Peter Bittner
- [x] Display name **Zaro** (not Gabriel) in announce copy
- [x] No HOLD names announced
- [x] Each `/speakers/<slug>/` URL returned HTTP 200 on re-curl (see link table)

### 3. Fact check

| Fact | In package? |
|---|---|
| Dates Oct 28-30, 2026 | YES (`October 28-30, 2026`) |
| Venue H.R. MacMillan Space Centre | YES (link: `hrmacmillanspacecentre.com`) |
| Earlyworm CA$650 | YES |
| Earlyworm priority ends August 15 | YES |
| Receipts 300 / 3,000+ / 94+ | YES |
| Call for Talks closes August 15 | YES (package) |

**Note (updated 2026-08-02):** two facts were corrected after the 2026-07-26 check.

1. **Call for Talks is August 15, not July 31.** KK extended it. The July 31 date was a *priority* window; the deadline is now a hard close. Canonical source is `~/Code/futureproof-festival/lib/pricing.ts:345` (`CALL_FOR_TALKS_CLOSE_DEADLINE = 2026-08-15T23:59:00-07:00`), confirmed by public readback of `futureproof.website/call-for-talks/` rendering "August 15, 2026". This resolves the old `Sept 31` ambiguity in the issue text; there is no September 31 and no September cutoff.
2. **Membership is 300, not 250+.** Per KK's 2026-08-01 ruling: 300 paid members at $340/year. The 250+ figure predates it.

Both Earlyworm and the Call for Talks now close on **August 15, 2026**. If this draft is created after that date, both lines need another pass.

### 4. Links live

All **34** unique `http(s)` URLs in `post.md` + `post.html` returned **HTTP 200** via `curl -I -L` (2026-07-26). Includes festival, speakers, orgs, internal kriskrug.co posts, and remote image asset URLs used in `post.html`.

### 5–6. Dry-run + create draft

- [x] Documented exact commands below
- [ ] Dry-run executed — **BLOCKED ON CREDS**
- [ ] `--execute` create-only — **NOT RUN** (no draft)
- [ ] `status==draft` readback / WP id / preview URL in `publish.log` — **N/A until secrets session**

---

## Exact publisher commands (from `scripts/notion-to-wp/README.md`)

Working directory: repo root. Prefer Varlock when secrets are resolved.

### Dry-run (validate quality gate + slug create-only; no WP writes)

```bash
# Preferred when Varlock resolves WP_USER + WP_APP_PASSWORD:
make varlock-run CMD="scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/create_local_wp_draft.py content/drafts/2026-07-26-futureproof-festival-announcement/post.md"

# Or with process env already injected:
scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/create_local_wp_draft.py content/drafts/2026-07-26-futureproof-festival-announcement/post.md
```

Expect: quality gate clean; slug `futureproof-festival-announcement` available (create-only). If slug already exists → **abort**, do not PATCH.

### Create WordPress draft only (`status=draft`)

```bash
make varlock-run CMD="scripts/notion-to-wp/.venv/bin/python scripts/notion-to-wp/create_local_wp_draft.py content/drafts/2026-07-26-futureproof-festival-announcement/post.md --execute"
```

After success:

1. Confirm `publish.log` records WP post id + edit/preview URL.
2. Authenticated readback: `status == draft`, slug match, featured media set from uploaded hero.
3. **Do not** pass `--publish`. Public publish / `--update` needs explicit KK sign-off + `--diff` review (out of scope for #500).

### Safety gates (2026-05-15)

- Create-only. Slug collision → abort.
- Never PATCH without verified slug-match target and KK-approved update path.
- Draft only; no live publish from this issue.

---

## This session: credential block

```
WP_USER present: False
WP_APP_PASSWORD present: False
NOTION_TOKEN present: False
scripts/notion-to-wp/.venv: absent in cloud pod
scripts/notion-to-wp/.env: absent
```

Per AGENTS.md: connector / `create_local_wp_draft.py` **hard-exits requiring creds even in dry-run**. Credential-free prep (this package + VERIFY) is the correct ship for this environment.

**WP draft created: no.**

---

## Hand-off for secrets-attached follow-up

1. Ensure `scripts/notion-to-wp/.venv` exists (`pip install -r scripts/notion-to-wp/requirements.txt`).
2. Inject `WP_USER` + `WP_APP_PASSWORD` (Cursor Cloud secrets or `make varlock-run`).
3. Run dry-run command above; paste redacted success lines into `publish.log`.
4. Run `--execute`; assert draft readback; leave post private for KK review.
5. Close #500 acceptance boxes only after draft id + preview URL exist.
