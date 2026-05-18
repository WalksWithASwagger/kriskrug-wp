# Owned Sites Linking Recommendation - 2026-05-18

**Lane:** Track A content/SEO strategy
**Scope:** docs-only recommendation. No WordPress writes.
**Inputs read:** live `kriskrug.co` homepage/About/Projects/Services/Events pages, `NAV-IA-DECISION-PACK-2026-05-18.md`, `CONTENT_AUDIT.md`, external site homepages for Both Hands Full, Punk Rock AI, Developing an AI Mindset, and BC + AI.

**Rollout artifact:** `fixes/owned-sites-network-rollout.md`
**Production status:** Applied on 2026-05-18. See rollout artifact for page IDs, widget ID, verification, and rollback handles.

## Assumptions

1. `kriskrug.co` remains the home base and personal/professional entity hub.
2. The other sites are proof objects in KK's wider AI work, not peers that should all become top-level nav items.
3. The current Catch Responsive top nav is already near capacity.
4. Any WordPress production edits still need the repo's Track A safety gates: backup first, small copy changes, live verification after publish.

## Short Recommendation

Do not add every external property to the primary navigation.

Instead:

1. Add a concise **Current Work / Project Network** section high on the About page.
2. Rework the Projects page into a **Work** hub and feature these as cards.
3. Add a compact sitewide sidebar/footer widget called **Elsewhere in KK's AI Network**.
4. Use the Speaking page for the keynote portals and talks.
5. Keep top nav focused on visitor intent: `About`, `Work`, `Services`, `Speaking`, `Events`, `Blog`, `Podcast`, `Contact`.

## Why

The current top nav already has eight items plus newsletter. Adding external domains as nav peers would make the site feel more fragmented and would leak visitors before they understand KK's role.

The better pattern is: kriskrug.co explains the ecosystem, then sends people outward with context.

## Recommended Placement By Site

| Site | What it is | Primary placement | Secondary placement | Top nav? |
|---|---|---|---|---|
| `bc-ai.ca` | Active community and industry association for responsible, inclusive, place-rooted AI in British Columbia | About page role section + Work page featured card | Footer/sidebar network widget | No direct top-nav item |
| `punkrockai.com` | CreativeMornings Vancouver keynote portal and maker toolkit | Speaking page talk portal section | Work page "Talk portals" card + related blog posts | No |
| `bothhandsfull.com` | World AI Film Festival keynote portal for filmmakers | Speaking page talk portal section | Work page "Talk portals" card + related blog posts | No |
| `developinganaimindset.com` | Earlier foundational AI mindset keynote/workshop resource, currently redirecting to Notion | Speaking page archive/resource section | About page only if framed as "earlier foundation" | No |
| `kriskrug.co` | Home base for KK's identity, services, writing, events, and proof | Primary site | N/A | Already is the nav root |

## About Page Section

Place this after the opening mission/identity section and before the long publications/clients proof blocks. The About page currently has strong voice, but readers need a faster "what are you building now?" bridge.

Suggested heading:

```markdown
## Current Work
```

Suggested copy:

```markdown
I work through a small network of living projects: community infrastructure, keynote portals, workshops, and field notes for the AI age.

- [BC + AI Ecosystem](https://bc-ai.ca/) is the community and industry association I help lead in British Columbia, focused on responsible, inclusive, place-rooted AI.
- [Punk Rock AI](https://www.punkrockai.com/) is a CreativeMornings Vancouver keynote portal about making culture with the tools, without surrendering taste or critique.
- [Both Hands Full](https://www.bothhandsfull.com/) is the World AI Film Festival edition of the same thesis for filmmakers: hold critique in one hand, curiosity in the other, and keep walking.
- [Developing an AI Mindset](http://developinganaimindset.com/) is an earlier keynote/workshop resource for teams starting their AI journey.
```

Keep it short. The About page is already long, so this should orient readers rather than become another full portfolio page.

## Work Page Section

The existing Projects page should become the main hub for these links. This supports the existing IA recommendation to rename `Projects` to `Work`.

Suggested section:

```markdown
## Project Network

These are the live projects, communities, and talk portals where my AI work becomes something people can use.

### BC + AI Ecosystem

The community and industry association for a responsible and inclusive AI future in British Columbia. Events, membership, partners, resources, and a growing province-wide network.

[Visit BC + AI](https://bc-ai.ca/)

### Punk Rock AI

A CreativeMornings Vancouver keynote rebuilt as a standalone portal: talk, recap, tools, exercises, release-day prompts, and a maker-first argument for human agency in the AI age.

[Open Punk Rock AI](https://www.punkrockai.com/)

### Both Hands Full

The World AI Film Festival edition for filmmakers working through the age of synthetic everything: keynote, slides, exercises, library, stories, and film club.

[Open Both Hands Full](https://www.bothhandsfull.com/)

### Developing an AI Mindset

A foundational AI keynote/workshop resource for organizations and teams that need shared language, practical exercises, and a first step into AI adoption.

[Open Developing an AI Mindset](http://developinganaimindset.com/)
```

## Speaking Page Section

Use `Speaking` as the clean home for the keynote portals. This is stronger than putting the portals in the primary nav.

Suggested heading:

```markdown
## Keynote Portals
```

Suggested copy:

```markdown
Some talks become more than a stage slot. I rebuild them as working portals with scripts, exercises, resources, and tools people can use after the room empties.
```

Suggested list:

- `Punk Rock AI` - CreativeMornings Vancouver, May 2026.
- `Both Hands Full` - World AI Film Festival, Sao Paulo edition.
- `Developing an AI Mindset` - AI adoption keynote/workshop resource.

## Sidebar / Footer Widget

Use a compact widget, not a giant sitewide block.

Suggested title:

```text
Elsewhere in KK's AI Network
```

Suggested links:

1. BC + AI Ecosystem
2. Punk Rock AI
3. Both Hands Full
4. Developing an AI Mindset

Suggested description:

```text
Community, talks, tools, and field notes from Kris's AI work beyond this site.
```

## Primary Navigation

Do not add these external domains to primary nav.

Recommended current-theme nav remains:

1. About
2. Work
3. Services
4. Speaking
5. Events
6. Blog
7. Podcast
8. Contact

Newsletter should be a CTA or footer/sidebar link, not a peer IA item.

## Implementation Order

1. Update the Projects nav label to `Work`, keeping the existing target for now.
2. Add `Speaking` to top nav.
3. Add the About page `Current Work` section.
4. Add or refresh the Work page `Project Network` section.
5. Add the compact sidebar/footer widget.
6. Verify each external link resolves:
   - `https://bc-ai.ca/` -> 200
   - `https://www.punkrockai.com/` -> 200
   - `https://www.bothhandsfull.com/` -> 200
   - `http://developinganaimindset.com/` -> 307 to Notion, then 200

## Later Cleanup

- Consider republishing `Developing an AI Mindset` as a proper static/keynote page rather than leaving the canonical experience on Notion.
- Add reciprocal links from Punk Rock AI and Both Hands Full back to the most relevant `kriskrug.co` pages if they are missing.
- Decide whether future auto-links for `Punk Rock AI` and `Both Hands Full` should point to the external portals or stay pointed at internal `kriskrug.co` posts in `scripts/notion-to-wp/text_polish.py`.
- Create a `Talk Portals` or `Keynote Portals` collection only if KK expects more standalone talks.
- Add schema later: `Person` on About, `Organization`/`Role` context for BC + AI, `CreativeWork` or `Event` markup for keynote portals.

## Bottom Line

Use `kriskrug.co` as the narrative hub. The external sites should appear as a deliberate network of current work, not as loose links scattered through the nav.
