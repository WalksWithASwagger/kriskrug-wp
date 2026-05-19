# Speaking Horizons Verification - 2026-05-18

Follow-up deploy for the Speaking page after KK asked to proceed with named podcast/produced-interview proof. This adds `Horizons by Compass Datacenters` to the live Speaking page and source pack.

## Source Evidence

- Public source page: `https://horizons.compassdatacenters.com/series/exploring-ai-models-the-future-of-machine-learning/`
- Source page identifies the series as `Exploring AI Models: The Future of Machine Learning`.
- Source page identifies Kris Krüg as the guest/source for the AI chapters.
- YouTube clip metadata was captured for:
  - `metadata/horizons-EBGdM6T9Fr8.json`
  - `metadata/horizons-tfXkDhlqnrE.json`
  - `metadata/horizons-pfecN8_1boA.json`

## Rollback Evidence

Fresh page-level snapshot captured before the live write:

- `backup/20260518-215912/page-snapshots/page-1887-speaking.json`
- `backup/20260518-215912/page-snapshots/page-1887-speaking.html`
- `backup/20260518-215912/page-snapshots/sha256sums.txt`

Checksum verification:

```bash
cd backup/20260518-215912/page-snapshots
shasum -a 256 -c sha256sums.txt
```

## Live Readback

Authenticated WordPress REST readback for page `1887` confirmed:

| Field | Result |
|---|---|
| Slug | `speaking` |
| Status | `publish` |
| Content | Matches `wp-payloads/speaking.html` |
| Comments/pings | `closed/closed` |
| Horizons marker | Present |
| Horizons YouTube embed | Present |
| Horizons external link | Present |

## Public Checks

`https://kriskrug.co/speaking/` returned `200` and contained:

- `Horizons by Compass Datacenters`
- `Horizons: Exploring AI Models`
- `EBGdM6T9Fr8`
- `Watch the Horizons series`
- `Podcast guesting EPK`

The YouTube embed `https://www.youtube.com/embed/EBGdM6T9Fr8` returned `200`.

Note: the Horizons source page is publicly indexed and browser-readable, but command-line `curl` received a Cloudflare `403` during verification. The source page was verified through web/browser access and the live page uses a normal human-facing anchor.

## Screenshot Evidence

Browser screenshot evidence lives under:

- `verification/screenshots-horizons-20260518-215912/contact-sheet-top.png`
- `verification/screenshots-horizons-20260518-215912/contact-sheet-full.png`
- `verification/screenshots-horizons-20260518-215912/results.json`

The screenshot pass reported desktop and mobile `200` responses, one visible H1, Horizons markers present, no `Leave a Reply`, and `unloaded: 0`.
