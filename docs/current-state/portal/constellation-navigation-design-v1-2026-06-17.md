# Constellation Navigation Design V1 - 2026-06-17

**Status:** V1 design/spec artifact. No theme implementation, WordPress writes, deploy, analytics instrumentation, external integration, or private source handling is implemented by this document.

**Issue:** GitHub #63 - `[PORTAL] Beautiful Constellation Navigation Design`

**Lane:** Track B-ready design/spec, docs-only.

## Goal

Give issue #63 a practical implementation target: a beautiful but usable project-network navigation surface that shows how Kris's major bodies of work connect, without replacing the site's primary navigation or creating a heavy custom app.

The constellation should help visitors understand the ecosystem quickly, then move toward the right next step: hire, invite, read, attend, explore a project, or contact Kris.

## Assumptions

1. `kriskrug.co` remains the home base for Kris's identity, services, writing, speaking, and project proof.
2. The constellation is a guided discovery module, not the site's only navigation system.
3. Aurora remains the likely implementation lane because this requires theme-level interaction, responsive layout, motion rules, and accessibility checks.
4. Production URLs stay stable unless KK separately approves a redirect or IA change.
5. The six project nodes named in issue #63 are the starting set, but labels and targets need final content approval before implementation.

## Target Users And Use Cases

Primary users:

- Event organizers evaluating Kris for a keynote, workshop, moderation, or advisory role.
- AI, culture, and community leaders trying to understand how BC + AI, Vancouver AI, Indigenomics, The Upgrade AI, photography, and thought leadership relate.
- Readers who arrive through a post and need a quick map of Kris's broader work.
- Collaborators, sponsors, and partners looking for the right project doorway.
- Returning followers who know one project but not the full network.

Primary use cases:

| Use case | Desired outcome |
|---|---|
| "Who is Kris and what is he building?" | Understand the ecosystem in under 20 seconds. |
| "Which project is relevant to me?" | Select one node and get a concise description plus a clear link. |
| "Can I hire or invite him?" | Move from project context to Speaking, Services, or Contact. |
| "Where does BC + AI fit?" | See it as a major community and industry node without making it the only story. |
| "I cannot use animation or pointer hover." | Use the same content through keyboard, screen reader, reduced-motion, and mobile list paths. |

## Information Architecture

The constellation should sit below the first brand/offer signal, not above it. It works best as a homepage or Work-page section after the visitor already sees "Kris Krug" and the primary role promise.

Recommended placement options:

| Surface | Recommendation | Reason |
|---|---|---|
| Homepage | Optional V1 placement after hero/proof chips | Strongest orientation moment, but must not delay first contentful paint. |
| Work page | Preferred first implementation target | Visitors expect project relationships here, and it keeps the experiment away from the global header. |
| About page | Secondary compact version | Useful as "Current Work" context, but avoid making About too visually busy. |
| Header/global nav | Do not implement in V1 | Too much risk for core navigation, mobile usability, and accessibility. |
| Footer | Text fallback only | Good for durable links, not the animated concept. |

Recommended node set for V1:

| Node | Role in the network | Likely target |
|---|---|---|
| BC + AI | Community and industry association work in British Columbia | External `bc-ai.ca` or internal BC + AI role page if approved |
| Indigenomics | AI, technology, and Indigenous economic future work | Work/project detail or external property if approved |
| The Upgrade AI | AI literacy, training, and media/product work | Internal Services/Work section or external property if approved |
| Vancouver AI | Local events, community learning, and practical AI adoption | Events, Vancouver AI pillar, or BC + AI context page |
| Photography | Documentary, event, portrait, and visual culture proof | Photography page/archive teaser |
| Thought Leadership | Writing, talks, podcasts, and public ideas | Blog/Writing, Speaking, and selected pillar posts |

Secondary links should remain outside the constellation: Newsletter, Contact, Services, Speaking, Events, Blog/Writing, Podcast, Publications, Testimonials, policies.

## Constellation Metaphor Boundaries

Use the metaphor as a spatial aid, not as a literal interface that obscures content.

The constellation may include:

- Six stable nodes, each with a label, short description, and target link.
- Thin connection lines showing relationship types.
- A subtle idle drift, pulse, or draw-in effect.
- Focus/hover detail panels.
- Optional "path" highlighting from one node to related nodes.

The constellation should not include:

- Starfields, particle storms, or decorative backgrounds that compete with text.
- Hidden unlabeled points that look clickable but do nothing.
- Motion that is required to understand the relationships.
- Physics simulation as the default layout.
- Canvas-only text or links.
- More than six primary nodes in V1.
- A global navigation replacement.

Relationship line types:

| Relationship | Example | Visual treatment |
|---|---|---|
| Community | BC + AI to Vancouver AI | Solid line, strongest weight. |
| Practice | Photography to Thought Leadership | Fine line, medium weight. |
| Platform | The Upgrade AI to Thought Leadership | Dashed or low-opacity line. |
| Partnership/proof | Indigenomics to BC + AI or Thought Leadership | Solid line, medium weight. |

Line labels are optional and should be hidden by default. If added, they appear only in the detail panel or as accessible text, not as tiny floating labels.

## Interaction Model

Default desktop state:

- Six nodes arranged in a stable radial or asymmetric cluster.
- Each node shows a plain-language label.
- One node may be featured by default if the module is placed on a page with strong context, but no node should be visually "selected" in a way that hides the others.
- Connection lines are visible but restrained.

Pointer behavior:

- Hovering a node highlights it, strengthens related lines, dims unrelated lines slightly, and opens a detail panel.
- Clicking a node opens the same detail panel first if the panel is not already open.
- A second click on the primary CTA inside the panel navigates to the target.
- Node labels and CTA text must be real HTML, not image text.

Keyboard behavior:

- The constellation is introduced by a semantic heading and short text.
- Tab order follows the visible node order, then the active detail panel CTA.
- Each node is a real `button` or link with a clear accessible name.
- Arrow-key navigation may be added only if it is fully documented and does not replace normal Tab behavior.
- `Enter` or `Space` opens the node detail.
- `Escape` closes the detail panel and returns focus to the active node.
- Focus indicators are visible against all background states.

Touch/mobile behavior:

- Do not depend on hover.
- Default mobile presentation is a vertical or two-column "project map" list with small connection hints.
- Tapping a node expands an inline detail panel with description and CTA.
- The animated constellation can appear as a static visual header above the list if it does not add load or confusion.
- Hit targets are at least 44 by 44 CSS pixels.
- The mobile list must preserve the same six nodes, descriptions, and targets as desktop.

Reduced-motion behavior:

- No idle animation.
- No line drawing animation.
- State changes use instant or very short opacity changes.
- The static layout still communicates the project relationships.

## Navigation States

| State | Requirements |
|---|---|
| Loading | Show the semantic heading and text/list content immediately. Enhancement can follow after CSS/JS loads. |
| Ready | All nodes are visible, labeled, and reachable. No required content is hidden behind animation. |
| Hover | Active node, related lines, and detail summary become clearer within 150 ms. |
| Focus | Same clarity as hover, plus a visible focus ring. |
| Selected/open | Detail panel shows title, one-sentence description, relationship hints, and one primary CTA. |
| Visited | Optional subtle visited style on node CTA; do not make visited nodes look disabled. |
| Error/no JS | Render as a normal HTML list of project cards with links. |
| Reduced motion | Render as static or near-static module. |
| High contrast/forced colors | Preserve labels, links, and focus order; do not rely on line color alone. |

## Visual Constraints

- Use the Aurora direction: editorial black, photographic depth, restrained glass, cyan/teal as an interaction signal, and real project proof where available.
- Avoid a one-note blue/purple gradient system. Constellation lines can be cool-toned, but project nodes should have distinct non-color cues such as icon shape, label, metadata, or line pattern.
- Do not place cards inside cards. The detail panel may be a single framed surface; the constellation itself should feel like a section, not a nested dashboard.
- Do not use decorative orbit blobs or particle clouds.
- Keep labels readable at normal text sizes. No tiny labels on curved paths.
- Connection lines should never run through body copy or CTA buttons.
- Use real photos or project thumbnails near the module if available; do not let the constellation become abstract clip art.
- Keep animation subtle enough that the module still feels like navigation, not a splash screen.

## Accessibility Criteria

V1 must meet WCAG 2.1 AA for the module before any production rollout:

- Semantic heading precedes the module.
- All nodes have accessible names matching visible labels.
- Each node detail has programmatic relationship to its trigger, such as `aria-expanded` and `aria-controls` where appropriate.
- Color contrast passes 4.5:1 for normal text and 3:1 for large text and focus indicators.
- Focus order matches reading/visual order.
- Keyboard-only users can open details, follow links, and close panels without trapping focus.
- Screen reader users receive the same project names, descriptions, relationship hints, and CTAs.
- Motion respects `prefers-reduced-motion`.
- The module remains usable at 320 px width, 200% browser zoom, and with forced colors/high contrast.
- No essential information is conveyed by color, line position, or animation alone.

Manual QA checklist:

- [ ] Keyboard smoke: Tab, Shift+Tab, Enter, Space, Escape.
- [ ] Screen reader smoke: VoiceOver on macOS or iOS, at minimum.
- [ ] Reduced motion smoke.
- [ ] Mobile touch smoke at 320 px and 390 px.
- [ ] Desktop smoke at 1280 px and 1440 px.
- [ ] Contrast check for all node, line, panel, and focus states.

## Performance Constraints

- Default HTML fallback must be useful before JavaScript runs.
- No WebGL, Three.js, or physics engine in V1 unless KK explicitly approves a heavier prototype.
- Prefer CSS/SVG/HTML for nodes and lines.
- If SVG is used, text and links should remain in HTML or be mirrored with accessible HTML controls.
- JavaScript enhancement budget target: under 10 KB gzipped for this module.
- Animation uses transform and opacity only.
- No autoplay media inside the module.
- Do not block page rendering on analytics, external APIs, or remote project data.
- Lazy-load any supporting images below the first viewport.

## Rollout Phases

| Phase | Scope | Exit criteria |
|---|---|---|
| Phase 0 - Spec approval | Review this document against issue #63 and current IA docs | KK approves node labels, targets, and first placement surface. |
| Phase 1 - Static content map | Build a no-JS HTML section/list in a Track B branch or block pattern | Six nodes, descriptions, targets, and fallback layout reviewed. |
| Phase 2 - Visual prototype | Add SVG/CSS constellation layout as progressive enhancement | Desktop and mobile screenshots show readable, stable layout. |
| Phase 3 - Interaction/a11y pass | Add focus/hover/open states and reduced-motion behavior | Manual keyboard, screen reader, mobile, contrast, and no-JS checks pass. |
| Phase 4 - Staging measurement | Test on real Aurora staging pages | Lighthouse/performance and manual QA evidence captured. |
| Phase 5 - Production decision | Decide whether to ship on Work page, homepage, or hold | No deploy unless Track B release gate and KK approval are satisfied. |

## Metrics

The module should be judged by navigation clarity, not novelty alone.

Launch-readiness metrics:

- Time to understand the six-project network during review: under 20 seconds for a first-time reviewer.
- Keyboard completion: reviewer can open each node and follow a CTA without pointer input.
- Mobile completion: reviewer can identify all six nodes and expand details without horizontal scrolling.
- Performance: no meaningful regression to Core Web Vitals on the placement page.
- Accessibility: WCAG 2.1 AA checklist passes before production.

Post-launch metrics if analytics are approved:

- Node CTA click-through by project.
- Work/Speaking/Contact assisted paths after constellation interaction.
- Scroll depth through the module.
- Mobile interaction rate versus desktop interaction rate.
- Rage-click or quick-back signals if available.
- Qualitative feedback from at least three target users.

Do not add analytics for V1 without a separate instrumentation/privacy decision.

## Acceptance Criteria For Issue #63

This design/spec artifact satisfies the repo-safe design phase of issue #63 when:

- [x] Target users and use cases are defined.
- [x] Information architecture and placement recommendations are defined.
- [x] The constellation metaphor has boundaries and relationship rules.
- [x] Navigation states are documented.
- [x] Keyboard, touch/mobile, no-JS, and reduced-motion behavior are specified.
- [x] Visual constraints are tied to the Aurora design direction.
- [x] Accessibility criteria and manual QA checks are defined.
- [x] Performance constraints are defined.
- [x] Rollout phases and metrics are defined.
- [x] Implementation stop rules are defined.

The issue should not be closed by this artifact alone unless KK decides the requested deliverable was design/spec only. A later Track B implementation PR should reference this file and use `Refs #63`, not `Closes #63`, until the interactive module is built and verified.

## Implementation Stop Rules

Stop and ask KK before implementation if any of these are true:

- A proposed change touches `theme/kk-aurora/`, production WordPress, redirects, live menus, snippets, plugins, analytics, or external services outside an approved Track B branch.
- Node labels, targets, or project inclusion are uncertain.
- The design requires private data, private member lists, unpublished source material, or non-public project details.
- The implementation would replace primary navigation.
- The prototype requires WebGL, a physics engine, heavy animation libraries, or persistent client-side state.
- Mobile behavior depends on hover or tiny spatial targets.
- Accessibility fallback would be materially different from the visual experience.
- Performance evidence shows the module harms the placement page.

## Open Decisions

1. First placement surface: Work page, homepage, or About page compact version?
2. Final labels: "BC + AI" versus "BC+AI", "Vancouver AI" versus "Vancouver AI Community", and "Thought Leadership" versus "Writing + Talks"?
3. Final targets for each node: internal pages first, external properties first, or mixed?
4. Should Indigenomics and The Upgrade AI be represented as external projects, Kris role pages, or Work-page anchors?
5. Should Photography be a full node in V1 or a supporting proof layer?
6. Should lines communicate relationship types visually, or stay decorative and let detail copy explain the relationships?
7. Is the module allowed on the homepage before Aurora's broader header/nav QA is complete?
8. What is the minimum evidence package required before a production deploy: screenshots only, Lighthouse plus screenshots, or full browser/a11y notes?

## Recommended Next Step

If KK approves this spec, create a Track B issue or branch for Phase 1 only: a static HTML/CSS project map on the Work page with the exact six nodes, descriptions, and links. Do not start with animation. Make the content and fallback right first, then layer the constellation treatment on top.
