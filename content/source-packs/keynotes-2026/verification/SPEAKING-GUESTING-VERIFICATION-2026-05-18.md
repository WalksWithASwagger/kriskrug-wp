# Speaking Guesting Verification - 2026-05-18

Follow-up deploy for the Speaking page after the second-pass polish. This adds podcast guesting, video appearances, host/emcee/moderator positioning, and the Vancouver AI March 2026 public video proof point.

## Rollback Evidence

Fresh page-level snapshots were captured before the live writes:

- `backup/20260518-214007/page-snapshots/page-1887-speaking.json`
- `backup/20260518-214007/page-snapshots/page-1887-speaking.html`
- `backup/20260518-214007/page-snapshots/sha256sums.txt`
- `backup/20260518-214334/page-snapshots/page-1887-speaking.json`
- `backup/20260518-214334/page-snapshots/page-1887-speaking.html`
- `backup/20260518-214334/page-snapshots/sha256sums.txt`

Checksum verification passed from the snapshot directories:

```bash
cd backup/20260518-214007/page-snapshots
shasum -a 256 -c sha256sums.txt
cd backup/20260518-214334/page-snapshots
shasum -a 256 -c sha256sums.txt
```

## Live Readback

Authenticated WordPress REST readback for page `1887` confirmed:

| Field | Result |
|---|---|
| Slug | `speaking` |
| Title | `AI Keynote Speaker Kris Krüg` |
| Modified | `2026-05-18T20:43:53` |
| Content | Matches `wp-payloads/speaking.html` |
| Comments/pings | `closed/closed` |
| Jetpack SEO title | Matches `page-meta.json` |
| Jetpack SEO description | Matches `page-meta.json` |

## Public URL Check

`https://kriskrug.co/speaking/` returned `200` and contained these markers:

- `Podcasts, interviews, hosting, and emcee work`
- `Podcast guesting EPK`
- `Host / emcee / moderator`
- `big-production interview shows`
- `Book Kris for a keynote, workshop, podcast, or hosted event`
- `We Trained AI on Stolen Work`

## Screenshot Evidence

Browser screenshot evidence lives under:

- `verification/screenshots-appearances-20260518-214007/contact-sheet-top.png`
- `verification/screenshots-appearances-20260518-214007/contact-sheet-full.png`
- `verification/screenshots-appearances-20260518-214007/results.json`

The screenshot pass reported desktop and mobile `200` responses, one visible H1, appearance/video markers present, no `Leave a Reply`, and `unloaded: 0`.

## Source Pack Additions

The deploy is backed by:

- `video-research/metadata/vancouver-ai-march-2026-appearance.json`
- `video-research/thumbnails/vancouver-ai-march-2026-appearance.jpg`
- `video-research/transcripts/vancouver-ai-march-2026-appearance.en.txt`
- `video-research/transcripts/vancouver-ai-march-2026-appearance.en.vtt`
