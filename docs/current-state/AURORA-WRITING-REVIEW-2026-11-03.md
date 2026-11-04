# Writing redesign: original final-review record

KK approved the merge and deployment. Aurora 1.7.1 is live with the changes from #1172 and the style-order correction from #1173. Pagely caches were purged, Boost regenerated Critical CSS, and the public blog and long post passed desktop and mobile checks. The rest of this document records the earlier review. [Release receipt](AURORA-WRITING-RELEASE-2026-11-03.md)

Aurora 1.7.0 implements the approved November 3 design proof. Latest thinking comes first: a chronological list with a thumbnail, title, short description and date, followed by native pagination. The article template uses a quiet reading column and optional contents navigation.

Draft PR: https://github.com/WalksWithASwagger/kriskrug-wp/pull/1172

## Review locally

- Review controls: http://127.0.0.1:8794/journal-review.html
- Writing: http://127.0.0.1:8794/blog/
- Long article: http://127.0.0.1:8794/2026/11/02/you-cant-rent-a-social-licence/
- Older-content fixture: http://127.0.0.1:8794/2005/01/01/older-post-fixture/
- Ordinary-page control: http://127.0.0.1:8794/page-control/
- Scripts-disabled article: http://127.0.0.1:8794/journal-nojs.html

The disposable WordPress 7.0.8 / PHP 8.2 fixture runs the actual theme. It imports eight published post snapshots and asserts that their stored content is unchanged. Featured photos are local copies of the public photos used in the proof; inline media and embeds retain their authored URLs. The fixture uses five posts per page to exercise pagination; production's setting remains 19. Its ninth post is explicitly labelled synthetic and has no image or manual excerpt. No production posts, settings, templates or caches were changed.

The preview process must remain running. Reproduce from this worktree after `npm ci`:

```sh
node scripts/tests/journal-preview.mjs \
  .generated/blog-review/wordpress-readback.json \
  /Users/kk/Code/kriskrug-wp/design-proofs/writing-2026-11-03/assets
```

The authenticated GET-only source snapshots and screenshots remain local in `.generated/blog-review/` and are ignored. They are not shipped in the theme. The fixture imports a provided snapshot and never authenticates to or writes to the live site. Auto-updates and cron are disabled only inside this disposable fixture.

## Implementation

- One `journal-entry` block pattern supplies thumbnails, linked titles, excerpts and dates for Writing, search, archives and related posts. `journal-query` shares the archive query/pagination/empty state. Missing images leave a text-only entry; missing excerpts use WordPress's generated summary.
- One conditional `journal.css` owns the reading surface. It replaces the old archive grids, dark/cream card overrides, image washes, panel treatments and reveal classes. Ordinary pages retain their existing prose stylesheet and chrome.
- Desktop thumbnails are 188px wide; phone thumbnails are 94px (82px on the narrowest layout). Descriptions remain visible. The normal article measure is 680px, with 20px/1.72 type on desktop and 18px/1.7 on phones.
- Compact blog-specific header/footer preserve the signature and static rainbow. Search submits to WordPress and category/RSS links remain native. Menu and contents disclosures are keyboard operable. The contents list opens on desktop and collapses on smaller screens.
- Paragraph reveals, reader-pane sheen, image fades, micro-interactions and page transitions are removed from journal routes. Article text is server-rendered and readable without scripts. The remaining JS adds reading time and contents links without hiding prose.
- Published body order and embeds are preserved. Unlike the one-off proof, the theme does not extract or move a particular post's introductory paragraph/caption. The featured image is bounded above the authored body. Instagram's injected 326px minimum is overridden only inside article prose to fit narrow phones.
- Related posts still exclude the current article. The manual-excerpt-only restriction now applies to the article's dek, allowing generated descriptions in its related-post rows.
- The saved single template's `ignoredHookedBlocks: ["jetpack/subscriptions"]` setting is preserved, avoiding a newly injected subscription block in production.

## Verification

- `make verify PYTHON=.venv/bin/python`: passed (184 publisher, 877 operational, 12 SEO inventory, 68 pytest checks; JavaScript/PHP syntax, behavior harnesses, plugin/theme smoke, docs truth and focused WordPress coding standards).
- CSS inventory ratchet: reduced the front-end budget from 7,489 to 7,142 lines and from 173 to 162 `!important` declarations.
- Nine changed template/pattern/part files passed `make voice-check` with zero violations.
- The repository's isolated Ruff rule set (`E4,E7,E9,F`) passed for changed Python tests. The broader machine-default Ruff configuration reports pre-existing style rules; it is not this repository's gate.
- Browser review: 1440px desktop, 390px phone, plus 320px and 767px breakpoints. No horizontal overflow after the Instagram correction; no hidden article paragraphs. Three complete index entries fit at 1440×900; two at 390×844.
- Verified native search and empty results, category results, older/newer pagination, missing image/manual-excerpt fallback, keyboard menu open/Escape, contents anchor/focus, current-post exclusion, and the scripts-disabled article (68 paragraphs, none hidden).
- Ordinary-page control keeps its old template and micro-interactions and does not load `journal.css`.
- New text/controls have contrast checks against both paper surfaces. This is focused verification, not a full accessibility certification.

Brave was used first; it became unavailable during native control. Remaining responsive checks and screenshots used the in-app browser. Screenshots are local review evidence, not a production pixel-gate pass. The local fixture does not reproduce Jetpack Boost, Pagely caches, every production plugin, every historical post, or Site Editor behavior.

## Production preflight and rollback

Read-only November 3 observations: live WordPress 7.0.8, public Aurora 1.6.12. Main already contains the undeployed 1.6.13 URL corrections; this candidate includes those inherited changes. `make status-readonly` still reports the old declared WordPress 7.0.5 version gate as drift; that startup failure is separate from the implementation test suite.

The saved single-post template **overrides the file on disk**:

- REST ID: `kk-aurora//single`
- WordPress ID: `12415`
- Source: `custom`, origin: `theme`
- Captured raw content SHA256: `b9b4f73f7fc2026b16433a0b91dbc13b13ad63ed741eb490b62760446b85c0a6`
- Local rollback copy: `.generated/blog-review/single-template-before.html`

Home/index and shared header/footer came from theme files on this readback. The front-page template is also saved in the database; it is unrelated and must be preserved. The public blog HTML contained no `wp-custom-css` style tag. Theme global-style readback is captured locally; no global styles were changed.

After KK approves the final design, merge and deploy remain separate actions requiring approval under `AGENTS.md` and the Aurora release checklist:

1. Recheck live version, template IDs/content hashes, branch/CI and concurrent changes. Stop if the single template drifted; compare and preserve any new edits. Capture the current theme and exact single template before changing them. Do not overwrite the primary checkout or other active worktrees.
2. Use KK's approved wp-admin ZIP or Pagely SFTP channel. Deploy the reviewed theme and synchronize **only** `kk-aurora//single` with the reviewed `templates/single.html`. Verify the slug/ID before the write and GET the saved content afterward. Do not reset all templates or global styles.
3. Regenerate Jetpack Boost critical CSS and purge Boost/Pagely page and CDN caches. Confirm the public stylesheet is 1.7.0 and actually contains the new journal rules. Check that no stale combined bundle applies old blog selectors.
4. Run the live visual baseline/comparison gate and public asset parity readback, including homepage/control pages as regression checks. Review the intentional blog differences; do not claim a zero-diff pass. Test real search, page two, taxonomy archives, the long article, an older article, embeds, mobile and keyboard navigation.
5. If rollback is needed, restore the captured theme **and** the exact saved single template, then rebuild/purge the same caches and verify public rendering. A theme-only rollback would leave the new database template pointing at missing patterns/parts.

No merge, production upload, template write, or cache purge is authorized by this review packet.

## Prepared packages

Local packages were built from committed theme source and verified by the packaging helper. They have not been uploaded:

- Candidate 1.7.0: `.generated/blog-review/packages/kk-aurora-writing-review-1.7.0-20261103.zip`
- Candidate SHA256: `28c68213f4a56bc4516cea0adf81ba0f34790a861f413840667e1b6ae2441480`
- Reference rollback 1.6.12 from `edeac1e`: `.generated/blog-review/packages/kk-aurora-rollback-1.6.12-20261103.zip`
- Reference rollback SHA256: `3775530ba595019bcee7d3be7749be9d1855c24abae28942dbad8f06240f9de0`

The reference rollback package does not replace the fresh production theme/template snapshot required at deployment. The paired database-template rollback described above is essential.
