## Visual regression — PASS

Baseline `BASE1` → candidate `BASE2` against `https://kriskrug.co`, generated 2026-07-25T21:05:13+00:00.

**33 pass · 0 warn · 0 fail · 0 error** across 33 route/viewport pairs.

Tolerance: pass ≤ 0.1% differing pixels · warn ≤ 1.0% · fail > 1.0% or > 2.0% full-page height delta · per-pixel threshold 0.2.

| Route | Viewport | Diff % | Height Δ% | Method | Verdict |
|---|---|---:|---:|---|---|
| `/` | mobile | 0 | 0 | sha256-identical | **PASS** |
| `/` | tablet | 0 | 0 | sha256-identical | **PASS** |
| `/` | desktop | 0 | 0 | sha256-identical | **PASS** |
| `/about/` | mobile | 0 | 0 | sha256-identical | **PASS** |
| `/about/` | tablet | 0 | 0 | sha256-identical | **PASS** |
| `/about/` | desktop | 0 | 0 | sha256-identical | **PASS** |
| `/generative-ai-services/` | mobile | 0 | 0 | sha256-identical | **PASS** |
| `/generative-ai-services/` | tablet | 0 | 0 | sha256-identical | **PASS** |
| `/generative-ai-services/` | desktop | 0 | 0 | sha256-identical | **PASS** |
| `/speaking/` | mobile | 0 | 0 | sha256-identical | **PASS** |
| `/speaking/` | tablet | 0 | 0 | sha256-identical | **PASS** |
| `/speaking/` | desktop | 0 | 0 | sha256-identical | **PASS** |
| `/work/` | mobile | 0 | 0 | sha256-identical | **PASS** |
| `/work/` | tablet | 0 | 0 | sha256-identical | **PASS** |
| `/work/` | desktop | 0 | 0 | sha256-identical | **PASS** |
| `/photography/` | mobile | 0 | 0 | sha256-identical | **PASS** |
| `/photography/` | tablet | 0 | 0 | pixel | **PASS** |
| `/photography/` | desktop | 0 | 0 | pixel | **PASS** |
| `/blog/` | mobile | 0 | 0 | sha256-identical | **PASS** |
| `/blog/` | tablet | 0 | 0 | sha256-identical | **PASS** |
| `/blog/` | desktop | 0 | 0 | sha256-identical | **PASS** |
| `/contact/` | mobile | 0 | 0 | sha256-identical | **PASS** |
| `/contact/` | tablet | 0 | 0 | sha256-identical | **PASS** |
| `/contact/` | desktop | 0 | 0 | sha256-identical | **PASS** |
| `/2026/07/18/i-am-nomad-ai-film/` | mobile | 0 | 0 | sha256-identical | **PASS** |
| `/2026/07/18/i-am-nomad-ai-film/` | tablet | 0 | 0 | sha256-identical | **PASS** |
| `/2026/07/18/i-am-nomad-ai-film/` | desktop | 0 | 0 | sha256-identical | **PASS** |
| `/definitely-not-a-page-404-probe/` | mobile | 0 | 0 | sha256-identical | **PASS** |
| `/definitely-not-a-page-404-probe/` | tablet | 0 | 0 | sha256-identical | **PASS** |
| `/definitely-not-a-page-404-probe/` | desktop | 0 | 0 | sha256-identical | **PASS** |
| `/category/vancouver-ai-ecosystem/` | mobile | 0 | 0 | sha256-identical | **PASS** |
| `/category/vancouver-ai-ecosystem/` | tablet | 0 | 0 | sha256-identical | **PASS** |
| `/category/vancouver-ai-ecosystem/` | desktop | 0 | 0 | sha256-identical | **PASS** |

### Environment readback

- Live theme version: **1.4.3** (repo `theme/kk-aurora/style.css`: **1.4.5**)
- Live-vs-repo CSS md5 identity: **DRIFT**
  - `style.css` ≠ live `28a523c46532` / repo `0ab1fadf9e64`
  - `assets/css/animations.css` = live `7645e93ae4fd` / repo `7645e93ae4fd`
  - `assets/css/bleeding-edge.css` = live `88d0fc9c77d8` / repo `88d0fc9c77d8`
  - `assets/css/editor.css` = live `4b0cb7208888` / repo `4b0cb7208888`
  - `assets/css/revive-port.css` ≠ live `737818af2441` / repo `f1ffb49f638f`
  - `assets/css/typography-refined.css` = live `69e3035368a8` / repo `69e3035368a8`
- Jetpack Boost CSS bundle: baseline `78b2cf14fa` → candidate `78b2cf14fa` (unchanged)
  - If a deploy happened between these two runs, an unchanged Boost hash means it did not reach the edge (risk R-2) — not that it had no visual effect. Purge Boost + PressCACHE and re-run before reading this as a green light.

_Screenshots cannot see focus, hover or keyboard behaviour (#424 remains a separate gate), and there is no staging environment — this compares post-deploy live against pre-deploy live (§4.7)._
