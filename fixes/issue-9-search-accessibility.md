# Issue #9 - Search Field Accessibility

Prepared for GitHub issue #9: `[A11Y] Fix Search Field Accessibility`.

## Assumptions

- This is Track A work on `main`: deployable current-theme guidance only, no Aurora/theme-file edits.
- Live WordPress writes remain blocked until backup/restore proof exists.
- The current Catch Responsive search markup in the raw snapshots is representative of production.
- `fixes/issue-9-button-hover-states.css` is historical/misnamed for current issue #9 and should not be redeployed for this lane.

## Current Evidence

Raw snapshots show two search forms on each checked public page:

- Header widget search: `docs/current-state/raw/homepage.html:196`
- Primary-nav hidden search: `docs/current-state/raw/homepage.html:227`
- Repeated on About, Blog, Contact, and Events snapshots.

Observed markup:

```html
<form role="search" method="get" class="search-form" action="https://kriskrug.co/">
    <label>
        <span class="screen-reader-text">Search for:</span>
        <input type="search" class="search-field" placeholder="Search" value="" name="s" title="Search for:">
    </label>
    <input type="submit" class="search-submit" value="Search">
</form>
```

Accessibility gaps from the snapshot:

- Label text is present but hidden with `.screen-reader-text`; issue #9 requires visible associated label text.
- Search input has a `title`, but no descriptive `aria-label`.
- Search submit uses visible value text in HTML, but the theme hides `.widget_search .search-submit` and `.nav-primary .search-submit`.
- The form has `role="search"`, but no explicit accessible name.
- The primary-nav search toggle is an icon wrapper with a hidden anchor; keyboard focus needs a visible target, `aria-expanded`, and focus handoff to the search field.

Jetpack Instant Search is also present with `overlayTrigger: "submit"`, so preserving the normal GET search form and submit action is the safest path.

## Deployable Fix

Use `fixes/issue-9-search-accessibility.php` as a Code Snippets entry after the backup gate is clear.

Deployment notes:

1. Create a disabled Code Snippets entry named `KK Issue 9 Accessible Search`.
2. Paste the PHP from `fixes/issue-9-search-accessibility.php` without the opening `<?php` tag.
3. Activate only after a fresh backup/restore proof exists.
4. Clear page/cache layers.
5. Verify on homepage, About, Blog, Contact, and Events before closing issue #9.

What the snippet does:

- Replaces `get_search_form()` output with named `role="search"` forms: `Header site search` and `Navigation site search`.
- Adds visible `label for=...` text: `Search the site`.
- Adds `aria-label="Search the site"` to the search input.
- Uses a real `<button>` with `aria-label="Submit site search"` so the submit control is not hidden by existing `.search-submit` CSS.
- Adds 44px minimum target sizing and visible focus outlines.
- Adds `aria-controls`, `aria-expanded`, and keyboard/focus behavior to the Catch Responsive primary-nav search toggle.

## Verification Checklist

Run these read-only checks after deploy:

```bash
curl -L https://kriskrug.co/ | rg -n 'kk-search-form|aria-label="Header site search"|aria-label="Navigation site search"|for="kk-site-search-field|kk-search-submit|kk-issue-9-search-toggle'
curl -L 'https://kriskrug.co/?s=ai' -o /tmp/kk-search-results.html
rg -n '<title>|Search|kk-search-form' /tmp/kk-search-results.html
```

Manual keyboard checks:

- Tab from the browser address bar into the header.
- Confirm the visible search input label reads `Search the site`.
- Confirm the search field receives focus with a visible outline.
- Type a query, tab to the Search button, press Enter, and confirm search results open.
- Tab to the primary-nav search icon, press Enter, and confirm the nav search expands and focus moves into the field.
- Press Shift+Tab and Tab around the opened nav search; focus remains visible and follows DOM order.

Screen reader proof:

- VoiceOver/Safari or NVDA/Firefox should announce the forms as `Header site search` and `Navigation site search`.
- The input should announce `Search the site, edit text/search`.
- The button should announce `Submit site search, button`.
- The nav toggle should announce `Open site search, button` and then `Close site search, button` after activation.

WCAG mapping:

- 1.3.1 Info and Relationships: explicit label association.
- 2.1.1 Keyboard: field, button, and nav toggle keyboard operable.
- 2.4.3 Focus Order: focus moves predictably into the opened nav search.
- 2.4.7 Focus Visible: 3px focus outline on input, button, and toggle.
- 3.3.2 Labels or Instructions: visible search label.
- 4.1.2 Name, Role, Value: named search landmark, named input, named button, toggle expanded state.

## Closure Recommendation

Do not close issue #9 from this repo-only pack alone. Mark it ready for deployment, then close after the snippet is live and the keyboard plus screen-reader checks above are recorded against production.
