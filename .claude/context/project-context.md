# Kris Krug Project Context

> kriskrug.co is Kris Krug's personal website, not the BC + AI organization website.

## Identity

Kris Krug is a Vancouver-based photographer, AI community builder, and keynote speaker. This site presents his photography, writing, speaking, experiments, and community work in his own name.

Kris also convenes the BC + AI ecosystem, but that project lives at `bc-ai.ca` and in separate repositories. Do not describe Kris as an organization or turn kriskrug.co into a BC + AI community portal.

## Repository purpose

This repository is the operations and content hub adjacent to the Pagely-hosted WordPress site. It contains:

- guarded content and SEO publishing tools
- draft and source content before publication
- the canonical Aurora theme line
- custom WordPress modules and helper plugins
- audits, rollback evidence, and current operating runbooks

The repository is not a file-for-file production mirror. Verify live state with `make status-readonly` and public readback before making production claims.

## Audience

- people considering Kris for speaking, photography, consulting, or collaboration
- readers exploring his writing, projects, archives, and AI work
- event and community participants looking for Kris's current work
- search engines and assistive technologies that need clear, structured content

## Editorial priorities

1. Preserve Kris's first-person identity and personality.
2. Keep claims grounded in source material; do not invent credentials, quotations, dates, or outcomes.
3. Make the next reader action clear without turning every page into generic marketing copy.
4. Maintain accessible headings, links, media alternatives, contrast, focus states, and keyboard behavior.
5. Protect performance, privacy, security, and search integrity.

For voice calibration across Kris's different roles, use `docs/kris-krug-roles-module.md` as a reference, not as permission to fabricate a persona or unsupported claim.

## Engineering priorities

- Follow `AGENTS.md` and the current-state front door before dated or historical plans.
- Keep Track A content/SEO and Track B theme work separate by commit.
- Prefer small WordPress-native changes over new frameworks.
- Run dry-runs and exact slug/ID checks before WordPress mutations.
- Capture a rollback path and perform authenticated plus public readback after an approved live write.
- Do not equate merging repository code with deploying it to production.

## Decision check

Before changing the site, ask:

- Is this about Kris's personal site or a different organization?
- Is the claim supported by a current source?
- Is the change in the correct Track A or Track B lane?
- Does it improve clarity, accessibility, performance, security, or reader value?
- What evidence and rollback path will prove the change is safe?

Start with `AGENTS.md`, `docs/current-state/README.md`, and a fresh `make status-readonly` run.
