# Aurora 1.3.40 pre-deploy public baseline

**Captured:** `2026-07-16T00:35:18Z`
**Live theme:** `1.3.37`

No credentials used. Baseline for comparing after an approved 1.3.40 upload.

| Path | Status | title (truncated) | canonical | og:title | og:url | desc× | og:title× |
|---|---:|---|---|---|---|---:|---:|
| `/` | 200 | Kris Krug / AI Keynote Speaker & Creative Technologist | `https://kriskrug.co/` | `—` | `https://kriskrug.co/` | 0 | 0 |
| `/blog/` | 200 | Blog — Kris Krug / AI Keynote Speaker & Creative Techno | `None` | `Writing — Kris Krug` | `https://kriskrug.co/` | 0 | 1 |
| `/blog/page/2/` | 200 | Blog — Page 2 — Kris Krug / AI Keynote Speaker & Creati | `None` | `Writing — Kris Krug` | `https://kriskrug.co/` | 0 | 1 |
| `/about/` | 200 | About Kris Krüg — Kris Krug / AI Keynote Speaker & Crea | `https://kriskrug.co/about/` | `About Kris Krüg` | `https://kriskrug.co/about/` | 0 | 1 |
| `/speaking/` | 200 | AI Keynote Speaker Kris Krüg — Kris Krug / AI Keynote S | `https://kriskrug.co/speaking/` | `AI Keynote Speaker Kris Krüg` | `https://kriskrug.co/speaking/` | 0 | 1 |
| `/work/` | 200 | Work — Kris Krug / AI Keynote Speaker & Creative Techno | `https://kriskrug.co/work/` | `Work` | `https://kriskrug.co/work/` | 0 | 1 |
| `/2026/01/24/both-hands-full/` | 200 | Both Hands Full — Kris Krug / AI Keynote Speaker & Crea | `https://kriskrug.co/2026/01/24/both-hands-full/` | `Both Hands Full` | `https://kriskrug.co/2026/01/24/both-hands-full/` | 0 | 1 |

## Gaps the 1.3.40 deploy is meant to address

- Home `og:title`: `MISSING` (#346).
- `/blog/` canonical=`None` og:url=`https://kriskrug.co/` (#347).
- `/blog/page/2/` canonical=`None` og:url=`https://kriskrug.co/` (#347).
- Standard `meta name=description` count on `/`: 0 (#36 / #333).
- `og:site_name` on `/`: `Kris Krüg | Generative AI Tools & Techniques` (legacy Generative AI Tools identity still present; #345/#316 separate).

JSON twin: `aurora-140-predeploy-public-baseline-20260716.json`

