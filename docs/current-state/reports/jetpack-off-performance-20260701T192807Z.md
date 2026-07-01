# Jetpack-Off Performance Report 20260701T192807Z

- Snapshot/rollback dir: `/Users/kk/Code/kriskrug-wp/backup/20260701T192429Z-jetpack-off`
- PressCACHE purge: `Cache Purge: Success`
- Jetpack core: inactive; Boost/Protect/CRM/Site Kit/Akismet/Redirection/Code Snippets/WPCode remained active.

## Cold TTFB p50 before -> after

- `/`: 3.712s -> 0.635s
- `/about/`: 3.659s -> 0.533s
- `/blog/`: 0.588s -> 0.855s
- `/work/`: 3.838s -> 0.519s
- `/contact/`: 3.778s -> 0.495s

## Warm TTFB p50 before -> after

- `/`: 0.496s -> 0.363s
- `/about/`: 0.42s -> 0.504s
- `/blog/`: 0.295s -> 0.42s
- `/work/`: 0.286s -> 0.418s
- `/contact/`: 0.35s -> 0.426s

## QA

- `/`: status 200, redirects 0, TTFB 0.419s, gateway=HIT, boost=hit, effective=https://kriskrug.co/
- `/about/`: status 200, redirects 0, TTFB 0.419s, gateway=HIT, boost=hit, effective=https://kriskrug.co/about/
- `/blog/`: status 200, redirects 0, TTFB 0.415s, gateway=HIT, boost=hit, effective=https://kriskrug.co/blog/
- `/work/`: status 200, redirects 0, TTFB 0.395s, gateway=HIT, boost=hit, effective=https://kriskrug.co/work/
- `/contact/`: status 200, redirects 0, TTFB 0.418s, gateway=HIT, boost=hit, effective=https://kriskrug.co/contact/
- `/robots.txt`: status 200, redirects 0, TTFB 0.471s, gateway=BYPASS, boost=None, effective=https://kriskrug.co/robots.txt
- `/llms.txt`: status 200, redirects 0, TTFB 0.507s, gateway=MISS, boost=None, effective=https://kriskrug.co/llms.txt
- `/?share=twitter`: status 200, redirects 1, TTFB 0.686s, gateway=HIT, boost=hit, effective=https://kriskrug.co/
- `/?nb=1`: status 200, redirects 1, TTFB 0.712s, gateway=HIT, boost=hit, effective=https://kriskrug.co/
- `/?amp=1`: status 200, redirects 1, TTFB 0.761s, gateway=HIT, boost=hit, effective=https://kriskrug.co/
- `/projects/`: status 200, redirects 1, TTFB 0.592s, gateway=HIT, boost=hit, effective=https://kriskrug.co/work/
- `/recent-projects-include/`: status 200, redirects 1, TTFB 0.704s, gateway=HIT, boost=hit, effective=https://kriskrug.co/work/

## Contact replacement

- `/contact/` has mailto CTA: `True`
- `/contact/` Jetpack form marker present: `False`
- Public `/contact/` mailto visible: `True`
