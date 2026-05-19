# Aurora Tomorrow Roadmap - 2026-05-19

Track: B - Aurora v2 theme  
Starting branch: `codex/aurora-redesign-2026-05-18`  
Preview target: `http://kriskrug-local.local`

## Goal

Turn the first visual redesign slice into a reviewable Aurora v2 direction with real KK media, tighter mobile polish, and a short implementation backlog for the next build pass.

## Morning Review

1. Open the Local preview and screenshots:
   - `http://kriskrug-local.local`
   - `docs/current-state/aurora-smoke-2026-05-18/aurora-home-desktop.png`
   - `docs/current-state/aurora-smoke-2026-05-18/aurora-home-mobile.png`
2. Review the smoke report:
   - `docs/current-state/AURORA-REDESIGN-SMOKE-2026-05-18.md`
3. Score the direction against three questions:
   - Does it feel unmistakably like Kris, not a generic AI speaker site?
   - Does the homepage make personal brand authority obvious in the first viewport?
   - Does the mobile presentation feel intentional enough for human review?

## Feedback Targets

Ask reviewers to focus on:

- Hero message: clarity, taste, and whether the headline earns the first screen.
- Photo treatment: whether the image feels premium, personal, and credible.
- Navigation: whether the paths match how people actually hire, read, or research Kris.
- Project hierarchy: whether BC + AI, The Upgrade AI, Indigenous AI, Punk Rock AI, photography, and speaking feel properly weighted.
- Mobile polish: header density, hero crop, CTA visibility, and whether anything feels cramped.

## Implementation Lanes

### Lane 1 - Media Source Of Truth

- Choose the final photo/video asset set for Aurora.
- Replace temporary external hero imagery with repo-managed or WordPress-managed assets.
- Decide whether the homepage gets one hero video, a project video reel, or both.
- Confirm alt text and captions for every major asset.

### Lane 2 - Motion And Interaction

- Keep motion purposeful: reveal, guide, and reward attention.
- Add one high-value scroll interaction after content is stable.
- Test reduced-motion behavior before adding more animation.
- Avoid decorative motion that competes with the writing or photography.

### Lane 3 - Mobile Polish

- Re-check 390-500px widths after media changes.
- Decide whether the mobile nav stays expanded or becomes a compact menu.
- Tighten the hero crop for phone screens.
- Confirm no text wraps awkwardly in project cards, CTA buttons, or footer links.

### Lane 4 - Content Mapping

- Map homepage cards to real URLs and canonical project pages.
- Decide which posts anchor the writing band.
- Identify any missing pages needed before staging review.
- Keep Track A content edits separate from Track B theme work.

### Lane 5 - Issue And PR Prep

- Convert review outcomes into small GitHub issues or a single Aurora punch-list issue.
- Push only the Track B branch until staging review is complete.
- Use `Refs`, not `Closes`, for partial implementation PRs.
- Keep production theme changes off `main` until Aurora has passed staging review.

## Suggested Day Plan

| Timebox | Outcome |
|---|---|
| 30 min | KK solo review of Local preview and screenshots |
| 45 min | External eyeballs: brand, story, mobile, and hire-me clarity |
| 60 min | Decide final media package and homepage hierarchy |
| 90 min | Implement the next polish slice |
| 30 min | Smoke test, screenshots, update this roadmap or open issues |

## Done For Tomorrow

- Review feedback is captured in issues, a punch-list, or an updated roadmap.
- Final media direction is chosen or explicitly blocked.
- Next code slice is scoped tightly enough for one branch/commit.
- Local preview still returns 200 for home, key pages, and sample posts.
