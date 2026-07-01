# Aurora Opal Live Audit - 2026-07-01

- Generated: `2026-07-01T23:01:23.294Z`
- Mode: live production pages after Aurora `1.3.28` deploy.
- Threshold failure count: `0`
- Follow-up: live single-post HTML renders `.aurora-article` without the new `.aurora-reader-pane` class, so the opal sheen/pane selector did not bind on production. Typography, contrast, overflow, and screenshot checks passed; the single template should be reset/ported or the theme should add an `.aurora-article` fallback in a follow-up Track B pass.

## Live CSS Readback

```text
7:Version: 1.3.28
501:  --aurora-opal-void: #090c11;
509:  --aurora-black: var(--aurora-opal-void);
522:  --aurora-readable-measure: 720px;
535:  background-color: var(--aurora-opal-void);
539:    linear-gradient(180deg, #10131a 0%, var(--aurora-opal-void) 44%, var(--aurora-opal-plum) 100%),
540:    var(--aurora-opal-void);
2272:  max-width: var(--aurora-readable-measure);
2299:  max-width: var(--aurora-readable-measure);
```

## Live Template Selector

- Article HTTP status: `200`
- `.aurora-reader-pane` present: `false`
- Rendered article class: `wp-block-group aurora-article has-global-padding is-layout-constrained wp-container-core-group-is-layout-ed92f1a2 wp-block-group-is-layout-constrained`
- Interpretation: production appears to be serving a customized/stale single-post block template shape for the article wrapper. No unapproved Site Editor reset was performed during this deploy.

| Page | Viewport | Overflow X | H1 px | Body min px | Prose min px | Article contrast | Pure white text | Pure black panels | Result |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Article | `1440x1100` | 0 | 69.6 | 18.88 | 18.88 | 10.53 | 0 | 0 | PASS |
| Article | `768x900` | 0 | 48.8 | 18.0288 | 18.0288 | 10.53 | 0 | 0 | PASS |
| Article | `390x844` | 0 | 37.6 | 17 | 17 | 10.53 | 0 | 0 | PASS |
| Article | `360x740` | 0 | 36.48 | 17 | 17 | 10.53 | 0 | 0 | PASS |
| Blog | `1440x1100` | 0 | 68 |  |  | 10.53 | 0 | 0 | PASS |
| Blog | `768x900` | 0 | 48 |  |  | 10.53 | 0 | 0 | PASS |
| Blog | `390x844` | 0 | 37.12 |  |  | 10.53 | 0 | 0 | PASS |
| Blog | `360x740` | 0 | 35.84 |  |  | 10.53 | 0 | 0 | PASS |
| About | `1440x1100` | 0 | 63.36 | 18 | 18 | 10.53 | 0 | 0 | PASS |
| About | `768x900` | 0 | 48 | 18 | 18 | 10.53 | 0 | 0 | PASS |
| About | `390x844` | 0 | 35.1 | 17.424 | 17.424 | 10.53 | 0 | 0 | PASS |
| About | `360x740` | 0 | 34 | 17.36 | 17.36 | 10.53 | 0 | 0 | PASS |
| Vancouver AI | `1440x1100` | 0 | 63.36 | 18 | 18 | 10.53 | 0 | 0 | PASS |
| Vancouver AI | `768x900` | 0 | 48 | 18 | 18 | 10.53 | 0 | 0 | PASS |
| Vancouver AI | `390x844` | 0 | 35.1 | 17.424 | 17.424 | 10.53 | 0 | 0 | PASS |
| Vancouver AI | `360x740` | 0 | 34 | 17.36 | 17.36 | 10.53 | 0 | 0 | PASS |
| Services | `1440x1100` | 0 | 63.36 | 18 | 18 | 10.53 | 0 | 0 | PASS |
| Services | `768x900` | 0 | 48 | 18 | 18 | 10.53 | 0 | 0 | PASS |
| Services | `390x844` | 0 | 35.1 | 17.424 | 17.424 | 10.53 | 0 | 0 | PASS |
| Services | `360x740` | 0 | 34 | 17.36 | 17.36 | 10.53 | 0 | 0 | PASS |
| Contact | `1440x1100` | 0 | 63.36 | 18 | 18 | 10.53 | 0 | 0 | PASS |
| Contact | `768x900` | 0 | 48 | 18 | 18 | 10.53 | 0 | 0 | PASS |
| Contact | `390x844` | 0 | 32 |  |  | 10.53 | 0 | 0 | PASS |
| Contact | `360x740` | 0 | 34 | 17.36 | 17.36 | 10.53 | 0 | 0 | PASS |

## Reduced Motion

- Article pane sheen opacity under `prefers-reduced-motion: reduce`: `not applicable`
- Reason: `.aurora-reader-pane` is absent from live article HTML, so the sheen interaction does not bind in production.

## Screenshots

- `docs/current-state/reports/screenshots/aurora-opal-live-20260701/aurora-opal-live-about-desktop.png`
- `docs/current-state/reports/screenshots/aurora-opal-live-20260701/aurora-opal-live-article-desktop.png`
- `docs/current-state/reports/screenshots/aurora-opal-live-20260701/aurora-opal-live-article-mobile390.png`
- `docs/current-state/reports/screenshots/aurora-opal-live-20260701/aurora-opal-live-blog-desktop.png`
- `docs/current-state/reports/screenshots/aurora-opal-live-20260701/aurora-opal-live-contact-mobile390.png`
- `docs/current-state/reports/screenshots/aurora-opal-live-20260701/aurora-opal-live-services-mobile390.png`
- `docs/current-state/reports/screenshots/aurora-opal-live-20260701/aurora-opal-live-vancouver-ai-desktop.png`

Note: `aurora-opal-live-contact-mobile390.png` was regenerated after the first capture hit a transient `503`; the final screenshot was gated on HTTP `200`.

## Failures

- None
