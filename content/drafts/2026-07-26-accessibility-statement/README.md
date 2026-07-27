# Accessibility statement draft packet (2026-07-26)

Track A / agent-safe. Draft only. **No WordPress writes. No publish. No footer/theme edits in this packet.**

| | |
|---|---|
| Primary issue | [#288](https://github.com/WalksWithASwagger/kriskrug-wp/issues/288) draft statement for human review |
| Publish umbrella | [#48](https://github.com/WalksWithASwagger/kriskrug-wp/issues/48) create/publish `/accessibility/` + footer link |
| Full audit | [#46](https://github.com/WalksWithASwagger/kriskrug-wp/issues/46) WCAG 2.1 AA audit (separate track) |
| Public file | `statement.md` (strip reviewer block before any WP paste) |
| Target URL | `https://kriskrug.co/accessibility/` (still **404** as of 2026-07-26 probe) |

## How this relates to #48 / #46 / earlier drafts

- **#288** is the draft-only child: write honest copy, leave contact/SLA/escalation as KK placeholders, stop before publish.
- **#48** is the parent publish umbrella: live page at `/accessibility/`, current status, known issues, reporting, accommodation path, roadmap, footer link, page-level a11y. This packet feeds #48; it does **not** satisfy #48.
- **#46** is the full audit. This statement explicitly says no independent audit has been done. Do not treat this draft as audit closeout.
- **Supersedes** (keep as history; do not publish them):
  - `content/drafts/2026-07-25-accessibility-statement/post.md` (skip-link/contrast claims pinned to live 1.4.3; outdated after 1.4.4-1.4.8)
  - `content/drafts/2026-07-24-accessibility-statement/post.md` (overclaims skip link / WCAG 2.2 / "we" voice)
  - `content/drafts/accessibility-statement-2026-07/` (evidence pinned to Aurora 1.3.37 / 2026-07-16 pa11y)
  - `content/drafts/accessibility-statement-2026-05/` (historical)

**Do not close #288, #48, or #46 from this commit.** #288 stays open until KK reviews. #48 stays open until the page is live and linked. #46 stays open until a real audit lands.

## Live evidence baked into this draft (2026-07-26)

Read-only HTTP only:

- `/accessibility/` → **404**
- Live Aurora → **1.4.8** (public `style.css` Version; matches repo)
- Homepage → theme `<a class="skip-link" href="#aurora-main">Skip to content</a>` present; `#aurora-main` present
- Footer → no Accessibility link yet (add only after 200)
- `/contact/` → **200** (proposed reporting channel)

Theme history useful for posture wording (not claimed as full AA):

- 1.4.4+ restored theme skip link to `#aurora-main` and suppressed competing core skip link
- 1.4.4-1.4.6 contrast / cream-system / writing-card a11y work (#464 lineage, #485, related)

## KK gates before any WordPress action

Copy from `statement.md` reviewer block. Short list:

1. Confirm public accessibility contact (contact page +/or email; no invented alias).
2. Confirm or delete reply-time language.
3. Confirm or omit formal escalation route.
4. Confirm WCAG 2.1 AA vs 2.2 AA naming.
5. Keep "partially conformant" unless an independent audit changes that.
6. Set "Last reviewed" to the real publish date.
7. Confirm whether the published page must hit AAA (#48) or AA + plain structure.

## Publish steps (gated on KK; do not run from this agent session)

1. KK reviews `statement.md` and answers the placeholders.
2. Confirm no live page, redirect, or menu item already owns `/accessibility/`. Recheck draft page `11886` if authenticated access is available (reuse or delete; do not duplicate).
3. Create or update a WordPress **draft** page only (slug `accessibility`). Paste **publishable copy only** (below `---- PUBLISHABLE COPY ----`).
4. SEO title suggestion: `Accessibility | Kris Krug`. Meta: short paraphrase of the excerpt in front matter intent (status, known problems, how to report, what is next).
5. Build the page as a plain reference: one H1, H2 sections from the draft, paragraphs and lists only, no embeds/required images, descriptive link text.
6. Keyboard, zoom, and mobile smoke on the draft page itself.
7. Publish only after KK approval. Verify `https://kriskrug.co/accessibility/` returns **200**.
8. **Separate Track B session:** add footer `Accessibility` link next to Privacy/Contact in `theme/kk-aurora/parts/footer.html`. Never add the footer link while the URL is still 404.
9. Update #288 / #48 comments with the live URL and remaining gaps. Leave #46 open for the audit.

## Agent boundaries

- Allowed: this draft packet, commit, push on the issue branch.
- Forbidden here: WP create/update/publish, redirects, menus, theme/footer edits, Code Snippets, closing related issues.
