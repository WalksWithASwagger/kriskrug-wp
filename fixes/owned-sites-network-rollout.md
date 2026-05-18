# Owned Sites Network Rollout Pack

**Track:** A - Content + SEO
**Status:** Applied to production on 2026-05-18 via WordPress REST
**Production safety:** This changed public page/widget/menu content. WordPress revisions were created for the edited pages.

## Production Changes Applied

| Surface | Live change | ID / rollback handle |
|---|---|---|
| About page | Added `Current Work` section | page `1208`, slug `about` |
| Work/Projects page | Added visual `Project Network` teaser grid | page `2672`, slug `recent-projects-include` |
| Speaking page | Added `Keynote Portals` section | page `1887`, slug `speaking` |
| Primary menu | Renamed `Projects` to `Work`, added `Speaking`, reordered menu | menu `242`; new Speaking item `11851`; Work item `3958` |
| Footer Area 1 | Added `Elsewhere in KK's AI Network` widget | widget `block-102` |

Cache note: the new footer widget appeared first on cache-busted URLs. Re-saving the homepage and edited pages refreshed the ordinary public HTML.

## Recommendation On The Issue Question

Skip a GitHub issue for this pass. The scope is small and already captured in `docs/current-state/OWNED-SITES-LINKING-RECOMMENDATION-2026-05-18.md`.

Use this file as the rollout artifact. Create a GitHub issue only if the rollout gets split, blocked, or needs a second pass for image uploads/schema.

## Success Criteria

- Top navigation stays focused: no external sites added as primary nav peers.
- `Projects` nav label becomes `Work`, with target unchanged for now.
- `Speaking` is added to primary nav.
- About page gets a short `Current Work` section.
- Work/Projects page gets a visual `Project Network` section.
- Speaking page gets a `Keynote Portals` section.
- Sidebar or footer gets a compact `Elsewhere in KK's AI Network` widget.
- External links resolve after publish:
  - `https://bc-ai.ca/`
  - `https://www.punkrockai.com/`
  - `https://www.bothhandsfull.com/`
  - `http://developinganaimindset.com/`

## Preflight

Run these read-only checks before editing:

```bash
curl -ILs https://bc-ai.ca/ | rg -i '^(HTTP|location:|content-type:)'
curl -ILs https://www.punkrockai.com/ | rg -i '^(HTTP|location:|content-type:)'
curl -ILs https://www.bothhandsfull.com/ | rg -i '^(HTTP|location:|content-type:)'
curl -ILs http://developinganaimindset.com/ | rg -i '^(HTTP|location:)'
curl -ILs https://kriskrug.co/about/ | rg -i '^(HTTP|location:)'
curl -ILs https://kriskrug.co/recent-projects-include/ | rg -i '^(HTTP|location:)'
curl -ILs https://kriskrug.co/speaking/ | rg -i '^(HTTP|location:)'
```

Backup note: `backup/2026-05-16/manifest.md` confirms a local UpdraftPlus backup with database/plugins/themes/mu-plugins/others. If there has been meaningful production editing since then, take a fresh DB backup before updating these pages.

## Graphic Sources

Use these as teaser images if WordPress accepts external image URLs. Prefer uploading them to the kriskrug.co media library later so the site does not depend on remote image hotlinks.

| Site | Teaser image | Alt text |
|---|---|---|
| BC + AI | `https://bc-ai.ca/wp-content/uploads/2026/05/bcai-living-ecosystem.webp` | The BC + AI living ecosystem, a glowing seedling surrounded by connected principles |
| Punk Rock AI | `https://www.punkrockai.com/public/photos/michelle-diamond/195.webp` | Kris Krug presenting Punk Rock AI at CreativeMornings Vancouver |
| Both Hands Full | `https://www.bothhandsfull.com/opengraph-image?46af5f0ff830fe03` | Both Hands Full keynote portal graphic |
| Developing an AI Mindset | `https://i0.wp.com/kriskrug.co/wp-content/uploads/2024/04/AI-Immortality-w-Guy-Kawasaki.png?fit=1200%2C604&ssl=1` | Kris Krug AI keynote at Innovate West |

## 1. About Page Copy

Edit `/about/`. Add this after the opening mission/identity section and before the long proof blocks.

```html
<h2>Current Work</h2>

<p>I work through a small network of living projects: community infrastructure, keynote portals, workshops, and field notes for the AI age.</p>

<ul>
  <li><a href="https://bc-ai.ca/">BC + AI Ecosystem</a> is the community and industry association I help lead in British Columbia, focused on responsible, inclusive, place-rooted AI.</li>
  <li><a href="https://www.punkrockai.com/">Punk Rock AI</a> is a CreativeMornings Vancouver keynote portal about making culture with the tools, without surrendering taste or critique.</li>
  <li><a href="https://www.bothhandsfull.com/">Both Hands Full</a> is the World AI Film Festival edition of the same thesis for filmmakers: hold critique in one hand, curiosity in the other, and keep walking.</li>
  <li><a href="http://developinganaimindset.com/">Developing an AI Mindset</a> is an earlier keynote/workshop resource for teams starting their AI journey.</li>
</ul>
```

## 2. Work Page Visual Section

Edit `/recent-projects-include/`. Add this near the top, after the first intro paragraph. If the page is later renamed to `/work/`, keep this section intact.

```html
<section class="kk-network">
  <h2>Project Network</h2>
  <p>These are the live projects, communities, and talk portals where my AI work becomes something people can use.</p>

  <div class="kk-network-grid">
    <article class="kk-network-card">
      <a href="https://bc-ai.ca/">
        <img src="https://bc-ai.ca/wp-content/uploads/2026/05/bcai-living-ecosystem.webp" alt="The BC + AI living ecosystem, a glowing seedling surrounded by connected principles" />
      </a>
      <div class="kk-network-card-body">
        <h3><a href="https://bc-ai.ca/">BC + AI Ecosystem</a></h3>
        <p>The community and industry association for a responsible and inclusive AI future in British Columbia. Events, membership, partners, resources, and a growing province-wide network.</p>
      </div>
    </article>

    <article class="kk-network-card">
      <a href="https://www.punkrockai.com/">
        <img src="https://www.punkrockai.com/public/photos/michelle-diamond/195.webp" alt="Kris Krug presenting Punk Rock AI at CreativeMornings Vancouver" />
      </a>
      <div class="kk-network-card-body">
        <h3><a href="https://www.punkrockai.com/">Punk Rock AI</a></h3>
        <p>A CreativeMornings Vancouver keynote rebuilt as a standalone portal: talk, recap, tools, exercises, release-day prompts, and a maker-first argument for human agency in the AI age.</p>
      </div>
    </article>

    <article class="kk-network-card">
      <a href="https://www.bothhandsfull.com/">
        <img src="https://www.bothhandsfull.com/opengraph-image?46af5f0ff830fe03" alt="Both Hands Full keynote portal graphic" />
      </a>
      <div class="kk-network-card-body">
        <h3><a href="https://www.bothhandsfull.com/">Both Hands Full</a></h3>
        <p>The World AI Film Festival edition for filmmakers working through the age of synthetic everything: keynote, slides, exercises, library, stories, and film club.</p>
      </div>
    </article>

    <article class="kk-network-card">
      <a href="http://developinganaimindset.com/">
        <img src="https://i0.wp.com/kriskrug.co/wp-content/uploads/2024/04/AI-Immortality-w-Guy-Kawasaki.png?fit=1200%2C604&amp;ssl=1" alt="Kris Krug AI keynote at Innovate West" />
      </a>
      <div class="kk-network-card-body">
        <h3><a href="http://developinganaimindset.com/">Developing an AI Mindset</a></h3>
        <p>A foundational AI keynote/workshop resource for organizations and teams that need shared language, practical exercises, and a first step into AI adoption.</p>
      </div>
    </article>
  </div>
</section>
```

Use this CSS in the same Custom HTML block if the editor strips class styling from blocks. If it works better as Additional CSS, paste it there instead.

```css
.kk-network {
  margin: 2rem 0;
}

.kk-network-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
  margin: 1.25rem 0 0;
}

.kk-network-card {
  border: 1px solid #d8d8d8;
  border-radius: 6px;
  overflow: hidden;
  background: #fff;
}

.kk-network-card img {
  display: block;
  width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: cover;
}

.kk-network-card-body {
  padding: 1rem;
}

.kk-network-card h3 {
  margin: 0 0 0.5rem;
  font-size: 1.1rem;
}

.kk-network-card p {
  margin: 0;
}
```

## 3. Speaking Page Section

Edit `/speaking/`. Add this below the speaker intro and before any old talks/archive material.

```html
<h2>Keynote Portals</h2>

<p>Some talks become more than a stage slot. I rebuild them as working portals with scripts, exercises, resources, and tools people can use after the room empties.</p>

<ul>
  <li><a href="https://www.punkrockai.com/">Punk Rock AI</a> - CreativeMornings Vancouver, May 2026.</li>
  <li><a href="https://www.bothhandsfull.com/">Both Hands Full</a> - World AI Film Festival, Sao Paulo edition.</li>
  <li><a href="http://developinganaimindset.com/">Developing an AI Mindset</a> - AI adoption keynote/workshop resource.</li>
</ul>
```

## 4. Sidebar Or Footer Widget

Use Appearance -> Widgets if available in Catch Responsive.

Widget title:

```text
Elsewhere in KK's AI Network
```

Widget body:

```html
<p>Community, talks, tools, and field notes from Kris's AI work beyond this site.</p>
<ul>
  <li><a href="https://bc-ai.ca/">BC + AI Ecosystem</a></li>
  <li><a href="https://www.punkrockai.com/">Punk Rock AI</a></li>
  <li><a href="https://www.bothhandsfull.com/">Both Hands Full</a></li>
  <li><a href="http://developinganaimindset.com/">Developing an AI Mindset</a></li>
</ul>
```

## 5. Navigation Updates

WordPress admin -> Appearance -> Menus:

1. Rename `Projects` to `Work`.
2. Keep its URL pointing to `/recent-projects-include/` for now.
3. Add `Speaking` and point it to `/speaking/`.
4. Do not add the external domains to primary nav.
5. Keep `NEWSLETTER` out of the IA discussion for this pass. If it is easy to move into a CTA/widget, do that later as part of the broader nav cleanup.

## Post-Publish Verification

```bash
curl -Ls https://kriskrug.co/about/ | rg -n 'Current Work|BC \\+ AI Ecosystem|Punk Rock AI|Both Hands Full|Developing an AI Mindset'
curl -Ls https://kriskrug.co/recent-projects-include/ | rg -n 'Project Network|kk-network|bcai-living-ecosystem|michelle-diamond|opengraph-image|AI-Immortality'
curl -Ls https://kriskrug.co/speaking/ | rg -n 'Keynote Portals|Punk Rock AI|Both Hands Full|Developing an AI Mindset'
curl -Ls https://kriskrug.co/ | rg -n 'Elsewhere in KK|bc-ai.ca|punkrockai.com|bothhandsfull.com|developinganaimindset.com'
curl -ILs http://developinganaimindset.com/ | rg -i '^(HTTP|location:)'
```

Expected:

- About, Work, and Speaking pages show the new section text.
- The homepage or footer/sidebar source includes the widget if the widget is sitewide.
- `developinganaimindset.com` returns a 307 redirect to Notion, then 200.

Verified on 2026-05-18:

- `https://kriskrug.co/about/` renders `Current Work` and all four owned-site links.
- `https://kriskrug.co/recent-projects-include/` renders the `Project Network` teaser grid and all four image sources.
- `https://kriskrug.co/speaking/` renders `Keynote Portals` and the three keynote-resource links.
- `https://kriskrug.co/` renders primary nav as `About`, `Work`, `Services`, `Speaking`, `Events`, `Blog`, `Podcast`, `Contact`, `NEWSLETTER`.
- `https://kriskrug.co/` renders footer widget `block-102` with `Elsewhere in KK's AI Network`.
- `http://developinganaimindset.com/` returns `307` to the Notion page, then `200`.
- Teaser image checks returned `200` for BC + AI, Punk Rock AI, Both Hands Full, and AI Mindset images.

## Rollback

Use WordPress revisions for the three page edits. For the menu/widget changes, manually remove the new widget, remove `Speaking`, and rename `Work` back to `Projects` if needed.

Do not bulk database-restore for this unless wp-admin becomes unusable. These are small reversible content changes.
