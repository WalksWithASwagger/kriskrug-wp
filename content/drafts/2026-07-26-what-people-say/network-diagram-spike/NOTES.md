# Network diagram spike  -  notes

## Intent

Standalone, shareable preview for KK reaction. Not a live embed. Not a framework. No CDN. Open `index.html` in any modern browser.

## What you will see

- SVG graph with five **illustrative** clusters around a Kris hub:
  - Stages (keynotes / festivals)
  - Rooms (Vancouver AI / BC + AI convening)
  - Practice (programs / education)
  - Media (photo / film / press)
  - Futureproof (festival node)
- Click or keyboard-activate a node to highlight its cluster and show a short blurb.
- Reduced-motion: skips the soft drift animation.

## What is fake on purpose

Node names are **placeholders for layout**, not a claimed org chart. Do not screenshot this as "the real network" in external decks until KK replaces labels with cleared people/orgs.

Quotes in the detail panel are drawn from the Tier A bank text for demo only. Same permission gate as the homepage section.

## Explicit non-goals (this spike)

- No D3, no Canvas, no WebGL, no force-layout library
- No live WordPress shortcode
- No personal emails, phone numbers, or private CRM edges
- No auto-fetch of LinkedIn / Notion

## Go / no-go for KK

| Decision | Meaning |
|---|---|
| **Go (homepage teaser)** | Tiny static SVG or linked preview later; full interactivity stays off-home or behind a dedicated route |
| **Go (dedicated page)** | Build a real data file (JSON of nodes/edges) under Track A content, then a light page |
| **No-go** | Keep quotes section only; archive this HTML as reference |

## How to preview

```bash
# from repo root, any static server, or just:
xdg-open content/drafts/2026-07-26-what-people-say/network-diagram-spike/index.html
# or open the file path directly in Chrome / Firefox / Safari
```

Eval from issue: prototype renders with **no external CDN dependencies**. This file meets that bar (inline CSS + JS only).
