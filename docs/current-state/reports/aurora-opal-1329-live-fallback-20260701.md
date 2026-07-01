# Aurora Opal 1.3.29 Live Fallback Audit - 2026-07-01

- Generated: `2026-07-01T23:51:15.300Z`
- Mode: live production article after Aurora 1.3.29 reader-pane fallback deploy
- Failure count: `0`

## CSS Readback

```text
7:Version: 1.3.29
501:  --aurora-opal-void: #090c11;
509:  --aurora-black: var(--aurora-opal-void);
522:  --aurora-readable-measure: 720px;
535:  background-color: var(--aurora-opal-void);
539:    linear-gradient(180deg, #10131a 0%, var(--aurora-opal-void) 44%, var(--aurora-opal-plum) 100%),
540:    var(--aurora-opal-void);
2272:  max-width: var(--aurora-readable-measure);
2299:  max-width: var(--aurora-readable-measure);
3194:.aurora-single-2026 > .aurora-article {
3215:.aurora-single-2026 > .aurora-article::before,
3216:.aurora-single-2026 > .aurora-article::after {
3226:.aurora-single-2026 > .aurora-article > * {
3232:.aurora-single-2026 > .aurora-article::before {
3242:.aurora-single-2026 > .aurora-article::after {
4105:  .aurora-single-2026 > .aurora-article {
4180:  .aurora-single-2026 > .aurora-article {
4185:  .aurora-single-2026 > .aurora-article::after {
```

## Article Wrapper

- Live selector checked: `.aurora-single-2026 > .aurora-article`
- Live article still lacks `.aurora-reader-pane`: `true`
- Fallback surface applied: `true`

| Viewport | HTTP | Overflow X | H1 px | Prose min px | Pane bg | Radius | Sheen opacity | Screenshot |
|---|---:|---:|---:|---:|---|---|---|---|
| desktop | 200 | 0 | 69.6 | 18.88 | rgba(24, 24, 32, 0.88) | 8px | 0.13 -> 0.24 | docs/current-state/reports/screenshots/aurora-opal-1329-live-20260701/aurora-opal-1329-article-desktop.png |
| mobile390 | 200 | 0 | 37.6 | 17 | rgba(24, 24, 32, 0.88) | 8px | 0.13 -> 0.24 | docs/current-state/reports/screenshots/aurora-opal-1329-live-20260701/aurora-opal-1329-article-mobile390.png |

## Reduced Motion

- Emulated reduced motion: `true`
- Sheen opacity: `0`
- Pseudo-element opacity: `0`

## Failures

- None
