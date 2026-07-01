# Content Architecture Reset - Trust + Offers Wave - 2026-07-01

**Status:** live on production
**Track:** Track A page content
**Branch:** `codex/content-architecture-trust-offers`
**Dependency:** Aurora `1.3.27` readability reset merged via PR #272
**Issue:** #122 local evidence update; no external issue comment or close action performed

## Summary

The first Trust + Offers wave is live. Seven high-value pages now use Aurora-owned content primitives instead of page-specific `kk-*`, `kkp-*`, `kkx-*`, and `kk-services-*` class systems.

Updated pages:

| Page | ID | URL | Role |
|---|---:|---|---|
| Services | 2666 | `/generative-ai-services/` | Offer |
| Contact | 2418 | `/contact/` | Utility / conversion |
| Work | 2672 | `/work/` | Portfolio / proof |
| About | 1208 | `/about/` | Trust |
| Speaking | 1887 | `/speaking/` | Offer / authority |
| Responsible AI Professional | 11914 | `/responsible-ai-professional/` | Offer / education |
| Podcast EPK | 3609 | `/podcast-guesting-page-epk/` | Media / booking |

Source pack:

- `content/source-packs/content-architecture-2026/`
- Payload map: `content/source-packs/content-architecture-2026/wp-payloads/page-map.json`
- Deploy helper: `scripts/content_architecture_deploy.py`
- Payload tests: `scripts/tests/test_content_architecture_payloads.py`

## What Changed

- Replaced first-wave page bodies with body-only Aurora payloads.
- Removed legacy page-specific class families from updated page raw content.
- Preserved public URLs and WordPress page titles.
- Did not send `title` fields in REST updates.
- Kept the separate performance lane untouched.
- Contact preflight found no Jetpack form block in current raw content, so the migration preserved the existing email contact path instead of creating a new form.

Allowed content primitives used:

- `aurora-page-lead`
- `aurora-section-kicker`
- `aurora-display-heading`
- `aurora-card-grid`
- `aurora-card`
- `aurora-media-card`
- `aurora-proof-section`
- `aurora-proof-grid`
- `aurora-proof-module`
- `aurora-button`

## Live Write Evidence

Deploy command:

```bash
python3 scripts/content_architecture_deploy.py --execute
```

Snapshots and deploy report:

- `backup/20260701T193335Z-content-architecture/deploy-report.json`
- `backup/20260701T193335Z-content-architecture/page-snapshots/`
- `backup/20260701T193335Z-content-architecture/page-snapshots/sha256sums.txt`

The deploy helper verified ID, slug, status, payload markers, REST readback, and public HTML after each write.

Post-write readback:

| Page | REST markers | Public markers | Retired classes | HTTP |
|---|---:|---:|---:|---:|
| Services | pass | pass | 0 | 200 |
| Contact | pass | pass | 0 | 200 |
| Work | pass | pass | 0 | 200 |
| About | pass | pass | 0 | 200 |
| Speaking | pass | pass | 0 | 200 |
| Responsible AI Professional | pass | pass | 0 | 200 |
| Podcast EPK | pass | pass | 0 | 200 |

Rollback command pattern:

```bash
python3 scripts/content_architecture_deploy.py \
  --restore \
  --snapshot-dir backup/20260701T193335Z-content-architecture/page-snapshots \
  --page services
```

Repeat `--page` for any page key from `page-map.json`.

## Verification

Commands:

```bash
python3 scripts/content_architecture_deploy.py
python3 -m unittest scripts.tests.test_content_architecture_payloads
python3 -m unittest discover scripts/tests
git diff --check
make status-readonly
```

Viewport/readability audit:

- `docs/current-state/reports/content-architecture-readability-audit-20260701.md`
- `docs/current-state/reports/content-architecture-readability-audit-20260701.json`
- Screenshot folder: `docs/current-state/reports/screenshots/content-architecture-20260701/`
- Pages audited: Services, Contact, Work, About, Speaking, Responsible AI Professional, Podcast EPK
- Viewports audited: `1440x1100`, `768x900`, `390x844`, `360x740`
- Failure count: `0`

Acceptance results:

- No horizontal overflow.
- Standard page H1 size met threshold on desktop, tablet, and mobile.
- Body/prose/card text met size threshold.
- Mobile touch targets passed.
- No body H1s.
- No retired class prefixes in updated raw page content.

## Remaining Work

- Do not close #122 yet; the first wave is done, but topic hubs, archives, policy pages, and legacy multilingual pages remain.
- Next content architecture wave should target topic hubs: `/vancouver-ai/`, `/ai-for-creatives/`, `/ai-events/`, `/ai-ethics/`, `/ai-tools/`, `/ai-for-journalists/`, `/ai-conversations/`, and `/indigenous-ai/`.
- About still has separate content opportunities from #269 and #270; treat those as copy/source enrichment, not layout migration.
- Accessibility work #4, #46, and #48 remains separate.
- Performance work #125 and #86 remains owned by the separate performance lane.
