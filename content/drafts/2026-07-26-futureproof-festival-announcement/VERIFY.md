# VERIFY — Futureproof Festival announcement (#500 / FP-4)

**Package:** `content/drafts/2026-07-26-futureproof-festival-announcement/`  
**Slug:** `futureproof-festival-announcement`  
**Target status:** WordPress `draft` only. Never `--publish`. Never `--update` / PATCH.  
**Verified:** 2026-07-26 (cloud swarm agent, credential-free path)

## Verdict

Package is **complete and verification-ready**.  
**WP draft was NOT created** in this session: `WP_USER` / `WP_APP_PASSWORD` are unset, and `create_local_wp_draft.py` hard-exits without credentials even in dry-run (per AGENTS.md / connector README).

Hand to KK (or a secrets-attached session) for dry-run → `--execute` create-only.

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
