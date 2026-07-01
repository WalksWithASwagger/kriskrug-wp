# Cold TTFB Isolation Report 20260701T190629Z

- Snapshot: `/Users/kk/Code/kriskrug-wp/backup/20260701T190629Z-cold-ttfb-isolation`
- Stop reason: `none`
- Likely culprit(s): `Jetpack`

## Baseline cold p50 TTFB

- `/`: 3.718s TTFB, 3.718s total, statuses [200, 200, 200]
- `/about/`: 4.176s TTFB, 4.176s total, statuses [200, 200, 200]
- `/blog/`: 0.579s TTFB, 0.594s total, statuses [200, 200, 200]
- `/work/`: 4.177s TTFB, 4.177s total, statuses [200, 200, 200]
- `/projects/`: 0.847s TTFB, 0.847s total, statuses [200, 200, 200]

## Isolation results

- **Popup Maker**: no threshold hit; heavy hits=[]; restored=active
  - `/`: 3.718s -> 3.93s (-0.212s, -5.7%)
  - `/about/`: 4.176s -> 3.885s (0.291s, 7.0%)
  - `/work/`: 4.177s -> 3.656s (0.521s, 12.5%)
  - `/blog/`: 0.579s -> 0.638s (-0.059s, -10.2%)
- **MCP Adapter**: no threshold hit; heavy hits=[]; restored=active
  - `/`: 3.718s -> 3.749s (-0.031s, -0.8%)
  - `/about/`: 4.176s -> 4.003s (0.173s, 4.1%)
  - `/work/`: 4.177s -> 3.65s (0.527s, 12.6%)
  - `/blog/`: 0.579s -> 0.625s (-0.046s, -7.9%)
- **Jetpack CRM**: no threshold hit; heavy hits=[]; restored=active
  - `/`: 3.718s -> 3.657s (0.061s, 1.6%)
  - `/about/`: 4.176s -> 3.992s (0.184s, 4.4%)
  - `/work/`: 4.177s -> 3.764s (0.413s, 9.9%)
  - `/blog/`: 0.579s -> 0.562s (0.017s, 2.9%)
- **Site Kit**: no threshold hit; heavy hits=[]; restored=active
  - `/`: 3.718s -> 4.353s (-0.635s, -17.1%)
  - `/about/`: 4.176s -> 3.648s (0.528s, 12.6%)
  - `/work/`: 4.177s -> 4.149s (0.028s, 0.7%)
  - `/blog/`: 0.579s -> 0.616s (-0.037s, -6.4%)
- **Jetpack Protect**: no threshold hit; heavy hits=[]; restored=active
  - `/`: 3.718s -> 3.927s (-0.209s, -5.6%)
  - `/about/`: 4.176s -> 3.668s (0.508s, 12.2%)
  - `/work/`: 4.177s -> 4.118s (0.059s, 1.4%)
  - `/blog/`: 0.579s -> 0.864s (-0.285s, -49.2%)
- **WPCode Lite**: no threshold hit; heavy hits=[]; restored=active
  - `/`: 3.718s -> 4.205s (-0.487s, -13.1%)
  - `/about/`: 4.176s -> 3.738s (0.438s, 10.5%)
  - `/work/`: 4.177s -> 3.802s (0.375s, 9.0%)
  - `/blog/`: 0.579s -> 0.795s (-0.216s, -37.3%)
- **Schema snippet 5**: no threshold hit; heavy hits=[]; restored=True
  - `/`: 3.718s -> 3.742s (-0.024s, -0.6%)
  - `/about/`: 4.176s -> 4.886s (-0.71s, -17.0%)
  - `/work/`: 4.177s -> 3.945s (0.232s, 5.6%)
  - `/blog/`: 0.579s -> 0.675s (-0.096s, -16.6%)
- **Jetpack Boost**: no threshold hit; heavy hits=[]; restored=active
  - `/`: 3.718s -> 3.748s (-0.03s, -0.8%)
  - `/about/`: 4.176s -> 4.708s (-0.532s, -12.7%)
  - `/work/`: 4.177s -> 3.776s (0.401s, 9.6%)
  - `/blog/`: 0.579s -> 0.6s (-0.021s, -3.6%)
- **Jetpack**: LIKELY CULPRIT; heavy hits=['/', '/about/', '/work/']; restored=active
  - `/`: 3.718s -> 1.11s (2.608s, 70.1%)
  - `/about/`: 4.176s -> 0.519s (3.657s, 87.6%)
  - `/work/`: 4.177s -> 0.843s (3.334s, 79.8%)
  - `/blog/`: 0.579s -> 0.63s (-0.051s, -8.8%)

## Final QA

- `/`: status 200, redirects 0, TTFB 0.467s, gateway=MISS, boost=hit
- `/about/`: status 200, redirects 0, TTFB 0.416s, gateway=HIT, boost=hit
- `/blog/`: status 200, redirects 0, TTFB 0.415s, gateway=HIT, boost=miss
- `/work/`: status 200, redirects 0, TTFB 0.771s, gateway=HIT, boost=miss
- `/projects/`: status 200, redirects 1, TTFB 0.59s, gateway=HIT, boost=miss
- `/recent-projects-include/`: status 200, redirects 1, TTFB 0.608s, gateway=HIT, boost=miss
- `/robots.txt`: status 200, redirects 0, TTFB 1.696s, gateway=BYPASS, boost=None
- `/llms.txt`: status 200, redirects 0, TTFB 2.298s, gateway=MISS, boost=None
- `/?share=twitter`: status 200, redirects 1, TTFB 1.031s, gateway=HIT, boost=hit
- `/?nb=1`: status 200, redirects 1, TTFB 1.22s, gateway=HIT, boost=hit
- `/?amp=1`: status 200, redirects 1, TTFB 2.516s, gateway=HIT, boost=hit
