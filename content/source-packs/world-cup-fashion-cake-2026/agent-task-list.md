# Agent Task List

This list is designed for handoff to other agents. It separates creative, implementation, and publishing work so each agent can take one lane without mutating live WordPress content by accident.

## Agent 1: Content Curator

- Read this source pack and the pasted chat/process capture.
- Produce a tightened microsite copy deck with five chapters:
  - The Mood Board
  - The Prompt Machine
  - Vancouver Match Fever
  - Lost Angels Meets Vancouver
  - Army of Robots
- Select only short, publishable chat fragments.
- Keep Tania Becker and Kris/KRUG named.
- Deliver `content.md` or a typed content module for the microsite implementer.

Acceptance:

- Copy is publishable and does not expose private chat clutter.
- World Cup facts are sourced.
- No official logo usage is requested.

## Agent 2: Image Intake And Selects

- Wait for final Midjourney selects from Kris.
- Rename optimized derivatives with stable filenames.
- Record each selected image in a manifest with prompt ID, caption, alt text, and provenance.
- Mark all mood boards and downloaded Tania reference images as process/reference unless explicitly approved.

Acceptance:

- 12 to 24 final images are ready for the microsite.
- Every public image has alt text and a caption.
- Reference-only images are not accidentally shipped as final art.

## Agent 3: Microsite Implementer

- Create a standalone Next.js app outside this repo.
- Implement the routes and content model described in `microsite-implementation-brief.md`.
- Use full-bleed editorial images, strong responsive typography, and stable image layouts.
- Include the motion test only as process media if it improves the page.
- Do not connect to WordPress.

Acceptance:

- Local build passes.
- Desktop and mobile screenshots show no broken layouts, blank canvases, or overlapping text.
- Site can be deployed independently.

## Agent 4: Blog Draft Writer

- Use `blog-post-brief.md` and the microsite copy deck to complete the local draft package:
  - `content/drafts/2026-06-12-vancouver-world-cup-2026-becker-kk-robots/post.md`
  - `post.html`
  - `seo-meta.md`
  - `alt-text.md`
  - `internal-links.md`
- Keep the post reflective and first-person.
- Add final microsite URL only after it exists.

Acceptance:

- The draft is review-ready, not publish-ready.
- Category, tags, excerpt, and meta description are intentional.
- No WordPress connector has been run.

## Agent 5: QA And Publish Gate

- Verify image rights/provenance.
- Verify Tania approval for name, credits, and any quoted lines.
- Run local static checks for the microsite.
- Run local WordPress draft package dry-run only after Kris approves the final post package.

Acceptance:

- Publish gate is documented.
- Any live WordPress action has explicit Kris approval.
- The final PR or publish note records what was checked and what remains human-review-only.

