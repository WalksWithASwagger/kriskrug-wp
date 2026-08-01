# Kris Media Appearances Visual KB Refresh Ship Receipt

**Local date:** 2026-07-31

**Target:** WordPress post `11879`, `ai-media-appearances-podcast-guesting`

**Live URL:** https://kriskrug.co/2026/07/02/ai-media-appearances-podcast-guesting/

**Result:** Published and publicly verified

## Why this pass happened

The page had one hero image, no video embeds in the article body, and a stale note saying its sources were collected on May 19, 2026. The KB already held a much richer public record than the page showed.

The user asked for visible video proof and for missing work already present in the knowledge base to be surfaced.

## Live change

- Added two Gutenberg-native YouTube embeds in a responsive `Watch the Work` section:
  - Power Struggle, Kris-channel edition `n_aGBFGnPzo`
  - STORYHIVE On Location, `zVy9zCQXPu0`
- Kept the Kris-channel LLLSummit and Human Biography editions immediately below the embeds.
- Added five verified earlier-video records from 2008–2024:
  - Byte Club with Nessa Palmer
  - OHEY / AI-Volution with Rob Anthony
  - Citizen media and activism with Justin Ruckman
  - W2 Culture + Media House launch interview
  - The Lab with Leo Laporte on Drupal, Bryght, and Raincity Studios
- Added six selected press and quoted-commentary records:
  - Business in Vancouver on the B.C. AI ecosystem
  - The Tyee on public participation in AI adoption
  - Business in Vancouver on AI and legal work
  - Pique Newsmagazine on public agency
  - CBC News / The Early Edition on Meta and platform power
  - BC Studies co-authored community-of-practice paper
- Added a clear handoff to `Press and Publications` for the wider written record.
- Replaced the stale May 19 source note with an honest selected-proof-stack boundary.

No title, slug, publication status, taxonomy, featured media, or Publications-page content was intentionally changed.

## Source and voice evidence

- KB gap audit: `content/drafts/2026-07-31-media-appearances-kb-gap-audit.md`
- Exact visible copy: `content/drafts/2026-07-31-media-appearances-visual-kb-refresh.md`
- Voice audit: `content/drafts/voice-audit-media-appearances-visual-refresh/`
- Dark Crystal facet: The ED with The Host's warmth
- Mechanical result: zero findings, zero em dashes
- Word count: 496 words including headings and linked titles

The public summaries were checked against the canonical press-clipping records in `kk-kb`. The CBC entry is identified as an embedded Early Edition segment, and the BC Studies item is identified as co-authored scholarship rather than independent reporting.

## Write receipt

- Before SHA-256: `4576bc1cc795a8c2354df047958aa4bb612938f40aa4509bf1d61578af09b78e`
- After SHA-256: `834a5dc0c70ea54448626e9da31020756988c747db5926a1569a0e171548f91b`
- WordPress `modified_gmt`: `2026-08-01T00:55:32`
- Update script: `scripts/refresh_media_appearances_visual_archive.py`

The script defaults to dry-run. `--apply` is required for a write. Its post-write readback matched the proposed content hash, and a second default run returned `[NOOP]`.

## Snapshot and rollback

- Authenticated before snapshot: `backup/20260731-kris-youtube-press-roundup-v2/post-11879-before-visual-kb-refresh-20260801T005532Z.json`
- Raw body snapshot: `backup/20260731-kris-youtube-press-roundup-v2/post-11879-before-visual-kb-refresh-20260801T005532Z.html`
- Rollback manifest: `backup/20260731-kris-youtube-press-roundup-v2/rollback-manifest.json`

Authorized rollback command:

```bash
varlock run --inject vars -- python3 scripts/update_media_appearances_roundup.py \
  --restore backup/20260731-kris-youtube-press-roundup-v2/post-11879-before-visual-kb-refresh-20260801T005532Z.json \
  --apply
```

## Verification

Passed:

- `make env-check`
- Python AST parse of `scripts/refresh_media_appearances_visual_archive.py`
- Dark Crystal `voicecheck.py --json`
- authenticated target verification for post `11879`, expected slug/title, status `publish`
- authenticated dry-run with a bounded three-part diff
- authenticated post-write hash readback
- cache-bypassed public readback
- canonical public HTML contains both rendered YouTube iframe URLs
- canonical public HTML contains the new press section, earlier-video section, and selected-proof-stack footer
- `python3 scripts/wp7-public-smoke.py --path 'https://kriskrug.co/2026/07/02/ai-media-appearances-podcast-guesting/'`
- updater idempotency returned `[NOOP]`
- in-app mobile DOM check found both rendered iframes, all five archive links, the new headings, and the new footer
- in-app visual check confirmed playable Power Struggle and STORYHIVE cards, readable captions, and a clean handoff into Recent Video Interviews and Talks

The canonical URL was fresh after the REST write. No manual Pagely cache purge was required.

## Remaining scope

- The Media Appearances page is intentionally selective. The full KB inventory is not duplicated on the public page.
- The Publications page is linked from this page but does not yet have a reciprocal link back to Media Appearances.
- The larger revolutionary `both hands full` article remains a separate editorial project, as previously requested.
- The live WordPress change is complete. The repository receipt still requires review and merge through draft PR `#579`.
