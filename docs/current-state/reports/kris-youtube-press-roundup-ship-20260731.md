# Kris YouTube Press Roundup Ship Receipt

**Local date:** 2026-07-31

**Target:** WordPress post `11879`, `ai-media-appearances-podcast-guesting`

**Live URL:** https://kriskrug.co/2026/07/02/ai-media-appearances-podcast-guesting/

**Result:** Published and publicly verified

## Change

Added one Gutenberg-native `Recent Video Interviews and Talks` subsection inside the existing `Produced Video Interviews` section. The insertion links and credits:

1. Kris Krüg's Power Struggle edition: `n_aGBFGnPzo`, with Stewart Muir and the source appearance.
2. Kris Krüg's LLLSummit edition: `Vbk2B7aqw8E`, with the source event talk.
3. Kris Krüg's Human Biography edition: `TOk2YwViBKs`, with Sharad Kharé, the source appearance, and the owned companion article.

No existing body copy, title, slug, publication status, taxonomy, metadata, featured media, or Publications-page content was intentionally changed.

## Editorial evidence

- Research: `content/drafts/kris-youtube-interviews-press-roundup-research.md`
- Approved copy: `content/drafts/2026-07-31-kris-youtube-interviews-press-roundup.md`
- Voice audit: `content/drafts/voice-audit/00-summary.md`
- Dark Crystal mechanical scan: zero findings
- Final word count: 159 words including the heading and linked titles

## Dry run and write receipt

- Authenticated target verification: post `11879`, expected slug/title, status `publish`
- Before SHA-256: `0986b8ede7f58410b01d5c2327e84ec44c3f3abe2ce2de92b1828e193cce5488`
- After SHA-256: `4576bc1cc795a8c2354df047958aa4bb612938f40aa4509bf1d61578af09b78e`
- WordPress `modified_gmt`: `2026-08-01T00:33:51`
- WordPress local modified time: `2026-07-31T16:33:51`
- Update script: `scripts/update_media_appearances_roundup.py`

The default script path is dry-run only. `--apply` is required for a write. A second default run returned `[NOOP]`, confirming the updater is idempotent against the shipped state.

## Snapshot and rollback

- Authenticated before snapshot: `backup/20260731-kris-youtube-press-roundup/post-11879-before-youtube-roundup-20260801T003350Z.json`
- Raw body snapshot: `backup/20260731-kris-youtube-press-roundup/post-11879-before-youtube-roundup-20260801T003350Z.html`
- Rollback manifest: `backup/20260731-kris-youtube-press-roundup/rollback-manifest.json`

Rollback dry-run:

```bash
varlock run --inject vars -- python3 scripts/update_media_appearances_roundup.py \
  --restore backup/20260731-kris-youtube-press-roundup/post-11879-before-youtube-roundup-20260801T003350Z.json
```

Add `--apply` only when an authorized rollback is required. The rollback dry-run was executed and showed only removal of the newly added subsection.

## Verification

Passed:

- `make env-check`
- Python AST parse of `scripts/update_media_appearances_roundup.py`
- `voicecheck.py --json content/drafts/2026-07-31-kris-youtube-interviews-press-roundup.md`
- Authenticated dry-run diff: one bounded insertion before `Long-Form Podcast Conversations`
- Authenticated post-write readback: content hash matched the proposed body
- Cache-bypassed public readback: heading and all three Kris video IDs present once
- Canonical public readback: heading and all three Kris video IDs present once
- Public REST readback: correct ID, slug, status, modified time, heading, and three video IDs
- `python3 scripts/wp7-public-smoke.py --path 'https://kriskrug.co/2026/07/02/ai-media-appearances-podcast-guesting/'`
- All three Kris uploads, all three source appearances, and the owned Human Biography companion returned HTTP `200`
- Idempotency run returned `[NOOP]`
- Rollback dry-run produced the expected bounded removal diff

The canonical URL was already fresh after the REST write, so no manual Pagely PressCACHE purge was required.

## Intentional consequence and remaining scope

The three Kris uploads remain Unlisted on YouTube, but the public roundup now makes them discoverable through KrisKrug.co. This was the explicitly approved consequence of the ship action.

The site now has one canonical grouping surface. A separate literal `/press/` page or duplicated Publications-page entries would be an information-architecture decision, not a blocker for this delivery. The larger revolutionary `both hands full` article remains held for a separate editorial pass.
