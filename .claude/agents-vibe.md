# Kris Krug Agent Vibe Guide

> Work on kriskrug.co as a personal, personality-forward website with production-grade operational care.

## Keep the identity straight

Kris Krug is a person: a photographer, AI community builder, and keynote speaker. kriskrug.co is his personal site. BC + AI is related to Kris's work but is a separate organization with its own site and repositories.

Write in Kris's voice only when the source material supports it. Keep the energy specific, candid, and human; avoid generic corporate language, invented biography, or community-organization framing.

## How to work here

### Evidence before confidence

- Read `AGENTS.md` and the current-state front door.
- Run `make doctor` and `make status-readonly` before current-state claims.
- Treat repository versions, cached captures, and old handoffs as evidence—not proof of production.
- Say what is fact, inference, or still unknown.

### Small, reversible changes

- Keep one concern and one Track A/Track B lane per commit.
- Match existing code and content patterns.
- Prefer a direct WordPress-native solution over a new abstraction.
- Preserve unrelated work in the tree.
- Do not deploy merely because a PR merged.

### Live WordPress discipline

For every approved mutation:

1. Run the documented dry-run.
2. Verify the exact object ID, slug, type, and status.
3. Capture a private snapshot or other proportionate rollback path.
4. Apply only the approved object or bounded batch.
5. Perform authenticated and public readback.
6. Record a concise receipt without secrets or private content.

### Accessibility, performance, and security

- Use semantic HTML and preserve keyboard and screen-reader behavior.
- Treat useful alternative text, visible focus, readable contrast, and heading order as product requirements.
- Avoid unnecessary JavaScript and oversized assets.
- Validate and sanitize data at user and external-system boundaries; escape output in the proper WordPress context.
- Never expose secrets, private drafts, credentials, or rollback snapshots in commits or issue comments.

## Communication style

- Lead with the outcome and concrete evidence.
- Be direct, warm, and specific.
- Explain non-obvious tradeoffs without narrating routine mechanics.
- Do not call kriskrug.co `kk.ca`.
- Do not describe the site as BC + AI community infrastructure.
- Use Canadian spelling when writing new prose unless quoted source material requires otherwise.

## Code style

- Follow WordPress APIs and the repository's WPCS configuration.
- Prefix public PHP symbols with the existing project prefix.
- Use names that explain behavior; comments should explain only non-obvious constraints or reasons.
- Add or update tests for behavior changes and run the narrowest meaningful check before the full gate.

## Finish line

Work is ready only when the requested behavior, documentation, verification, git state, and external readback required by the task agree. If any proof is missing, report the gap instead of declaring success.
