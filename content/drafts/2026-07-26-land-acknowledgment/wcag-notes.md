# WCAG notes - land acknowledgment (#22)

Working reference: WCAG 2.1 AA. This is guidance for the draft, not a conformance claim for the live site.

## What already helps

- Footer sits in `<footer role="contentinfo">` with labeled tiles (`aria-label` on brand / newsletter / nav sections).
- Acknowledgment is plain text in a paragraph (not an image of text).
- Reconciliation route is a real HTML page with an `h1`.
- Decorative woven SVG strip uses `aria-hidden="true"`.

## Risks to watch when changing copy or placement

### 1. Contrast (1.4.3 Contrast Minimum)

- Footer brand tile uses Aurora cream/ink system. Any new acknowledgment sentence must keep AA contrast against the footer background.
- Do not style the acknowledgment in muted gray that fails AA on cream or dark bands.
- If About Option C lands inside #418's paper (`#efe6d2`) / panel (`#e6dcc2`) system, use the same ink tokens as the rest of that pack. No new low-contrast accent color for "solemn" tone.

### 2. Link purpose (2.4.4 Link Purpose in Context)

- Prefer link text like `Musqueam`, `Squamish`, `Tsleil-Waututh`, or `Full acknowledgment`.
- Avoid bare URLs or `Learn more` / `click here` without surrounding context.
- If footer already has a `Reconciliation` link, do not add a second adjacent link with identical purpose and different wording without a reason.

### 3. Unicode Nation names (1.3.1 / readable text)

- Autonyms are respectful and belong on the Reconciliation page.
- Small footer type + complex Unicode can fail font coverage or look like mojibake in some extracts/clients.
- Recommendation: English Nation names in footer; autonyms on the dedicated page where type is larger and intentional.
- If Option B Unicode footer is chosen, smoke-test with system fonts on iOS Safari, Android Chrome, and a desktop screen reader. Confirm characters announce usefully or provide English in parentheses (already common pattern).

### 4. Mobile / reflow (1.4.10 Reflow, 1.4.4 Resize Text)

- Keep footer acknowledgment to one short paragraph. Long essays break the bento tile on 320 to 375px widths.
- Do not force nowrap on Nation names.
- About module should use the same single-column collapse as #418 grids (`max-width: 720px` pattern), not a fixed multi-column land block.

### 5. Keyboard and focus (2.1.1, 2.4.7)

- Nation links and the Reconciliation link must show visible focus styles consistent with Aurora buttons/links.
- Do not wrap the whole footer brand tile in one giant link.

### 6. Semantics / headings

- Footer: keep acknowledgment as `<p>`, not an `h2` competing with "Still paying attention…"
- About Option C: use one `h2` (or `h3` if nested under an existing section scheme) named clearly, e.g. `Land and commitments`. One job per section.

### 7. Language of parts (3.1.2)

- If autonyms are included, wrapping them in `lang` (or leaving them as proper names with English gloss in parentheses) is ideal when practical. Do not invent incorrect `lang` codes. English gloss in parentheses is an acceptable fallback used widely in Vancouver acknowledgments.

## Suggested smoke checks after any live apply

1. Keyboard-only tab through footer brand links + Reconciliation link.
2. Zoom to 200% on a 1280px viewport; acknowledgment still readable, no horizontal clip.
3. Contrast check on footer paragraph and any new About module text.
4. Screen reader skim: Nation names announced; Reconciliation link purpose clear.
5. Mobile screenshot at 375px of footer brand tile.

## Non-claims

- Do not mark the acknowledgment block with `aria-label="land acknowledgment"` unless UX research says visitors need that landmark; over-labeling can add noise.
- Do not claim the site is WCAG AA compliant because this sentence was added.
