# Aurora v3 — Local QA results + roadmap (2026-05-24)

Branch `aurora/v3-reconcile` (theme **kk-aurora 1.3.0**), QA'd on Local (localhost:10003)
via rendered-HTML inspection + DB checks. This is the reconciled line: the rescued 1.2.0
build + proof-trail/dek fix + #116 reveal hardening. Deploy zip staged at `~/Desktop/kk-aurora.zip`.

## What shipped in v3 (and QA verdict)

| Item | What changed | Local QA |
|---|---|---|
| **#117 `/blog/` archive** | 1.2.0's `home.html` is a real query-loop archive | ✅ 9 post cards, query blocks, no homepage-hero markers |
| **Proof-trail removed** | deleted the hardcoded "Proof trail: reported from…" line | ✅ 0 occurrences site-wide |
| **Author-controlled dek** | `core/post-excerpt` + `render_block` filter (`manual_excerpt_dek_only`) shows the dek **only** when a manual `post_excerpt` exists | ✅ shows on posts w/ excerpt; **blank** on posts without (verified vs DB) |
| **#116 homepage reveal** | hide is JS-injected (safe-fail) + new rAF pass reveals in-viewport on first frame | ✅ no static `opacity:0` served; v1.3.0 JS enqueued. Runtime visual confirm pending on prod |
| No regressions | Speaking 200, 404 works | ✅ |

**Deploy status:** zip built, awaiting KK's wp-admin upload (native file picker = KK's step;
SFTP still blocked). After upload + Pagely purge: verify prod logged-out, then remove the
Customizer force-visible band-aid (the homepage fix is now in-theme).

## Decisions captured

- **Do NOT blind-port `aurora/v2`'s fix-commits.** v2's launch-fix batch (`feb2003`) and
  `dd2f428` (retire hero pattern) overlap with — and in places conflict with — 1.2.0 (which
  keeps `hero-gradient.php` and already has `home.html`). QA passed on 1.2.0 without them.
  Treat any v2 port as a per-file, QA-driven decision, not a merge. (Original task #15 → folded here.)
- **Local DB is partial** (`/work/` absent locally; only ~9 posts) — pagination on `/blog/`
  couldn't be exercised locally. Re-verify pagination + the archive at scale on prod.

## Roadmap — next Aurora work (prioritized)

### P0 — finish this deploy
- [ ] KK uploads `~/Desktop/kk-aurora.zip` (Appearance → Themes → Add New → Upload → Replace).
- [ ] Pagely "Purge All Caches + CDN"; verify `/`, `/blog/`, a post (dek + no proof-trail) logged-out w/ cache-bust.
- [ ] Visual: homepage hero visible on 5 cold loads; then **remove Customizer band-aid CSS**.

### P1 — remaining launch polish (open issues, now unblocked once /blog + homepage are sound)
- [ ] **#118** duplicate H1 on generic `page.html`. · **#121** low-contrast body text (WCAG AA).
- [ ] **#119** host canonical proof images (Upgrade-AI 400 black card) · **#120** Both Hands Full card overlap.
- [ ] **Hardcoded "Field note" label** (`single.html` L24) — same generic-stamp smell as the
  proof-trail; replace with the post's real category or remove. (KK flagged proof-trail; this is its sibling.)

### P2 — verify/measure
- [ ] **#127** mobile/responsive QA on real device/breakpoints (nav→hamburger, hero crop, grids, gallery columns).
- [ ] **#125** Lighthouse (LCP/INP/CLS); consider self-hosting GSAP.
- [ ] **#117 at scale**: `/blog/` pagination + category archives once live with all posts.

### P3 — content-as-DB (per the 2026-05-24 architecture decision)
- The ~25 undesigned pages (#122) should be **page content via REST** reusing Aurora classes,
  NOT new theme templates — no theme deploys, KK-editable. Convert Services off its legacy
  template when editability is wanted.

## Branch / artifacts
- `aurora/v3-reconcile`: `3c31272` (rescue) · `577c7fb` (dek) · `52a4f80` (#116) · `9f0dfd0` (1.3.0)
- Backup of the original untracked 1.2.0: `docs/current-state/aurora-1.2.0-untracked-backup-20260524.tgz`
- Deploy zip: `~/Desktop/kk-aurora.zip` (kk-aurora 1.3.0)
