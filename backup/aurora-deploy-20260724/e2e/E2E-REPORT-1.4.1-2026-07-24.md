# Aurora 1.4.1 — e2e spot check (2026-07-24)

## Verdict

**Pass.** R1–R4 live on Pagely.

## Deploy

- Zip: `kk-aurora-revive-a11y-1.4.1-1.4.1-20260725.zip`
- SHA256: `725a88ab8f1e2f141169d1b16bfc56ee47e06423da9d745a4b52f067620fbd84`
- Media **#12633**; one-shot snippet **#16** (inactive); option `kk_aurora_sync_141`
- Public hashes MATCH for `style.css`, `revive-port.css`, `parts/header.html`
- REST theme version **1.4.1**; Boost hash `06822ae7e0` includes `--revive-accent-text` + `focus-visible`

## Checks

| Check | Result |
|---|---|
| Skip links | **1** (`#wp-skip-link`); theme skip removed |
| Accent text `#b53c18` on cream | **4.67:1** AA pass |
| Bright fill `#d94a1f` on cream | 3.42:1 (fills/CTA only — intentional) |
| Focus-visible rules in revive-port + Boost | present |
| Nav density | `flex-wrap: nowrap` + horizontal scroll |

Raw: `readback-141.json`
