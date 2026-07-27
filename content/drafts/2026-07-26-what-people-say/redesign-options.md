# Redesign options (homepage section)

Draft concepts only. Markup/theme ship is a later pass after KK picks.

Shared constraints for every option:

- No "fresh proof" placeholder copy.
- No invented cites.
- No Beehiiv / email CTA inside this section (that is #416 / newsletter).
- Avoid the phrase **"Named people"** (already used in the live newsletter dek).
- Prefer Aurora tokens already on the homepage (ink, signal, void). Do not invent a purple glow system.
- Faces only when KK clears them. Default: name + role/context text.
- Mobile: stack. Tablet: 2-up. Desktop: 3-up or featured+rail.

---

## Option A  -  Three receipts (classic grid)

Rebuild the old three-card quote grid with **real** cleared quotes only.

- Kicker + sharp H2 + one-line dek
- Three `.aurora-quote-card` blocks
- Footer link: `More on /testimonials/` (archive) or `Book a keynote` → `/speaking/` / `/contact/`
- Optional soft rotate via CSS only (crossfade every N seconds) if reduced-motion is respected

**Pros:** Fast to implement with existing CSS classes. Familiar.  
**Cons:** Flat. Does not show the network/cluster idea KK asked for.  
**Best if:** KK wants proof live this week and network stays a separate spike.

---

## Option B  -  Clustered themes (recommended)

One section, three theme rails: **Stages / Rooms / Practice**.

- Each rail: theme label + one quote + attribution
- Optional thin connector line between rails (CSS, not a full graph)
- Secondary link under the grid: `See how the rooms connect` opens the network spike later, or routes to About/network once approved

**Pros:** Matches issue language ("clusters"). Separates talks vs convening vs programs.  
**Cons:** Needs at least two cleared named quotes or it looks thin.  
**Best if:** Homepage should feel like proof of the network, not a generic testimonial strip.

---

## Option C  -  Featured quote + rail

- One large pullquote (A1 or A2) with attribution
- Vertical rail of 2-3 shorter lines (audience or second named quote)
- Small "Network" teaser SVG (static, non-interactive) linking to a future `/network/` or modal only after go

**Pros:** Hierarchy. Featured line can carry booking intent.  
**Cons:** Temptation to overbuild the teaser into a second hero. Keep the SVG tiny.

---

## Option D  -  Network-first (spike embeds later)

Homepage section is mostly the interactive cluster diagram; quotes appear as node detail panels on click/focus.

**Pros:** Unique. Matches KK teardown ambition.  
**Cons:** Heavy for first viewport of proof. A11y, performance, and data-truth risk. **Not recommended for v1 live.** Use the standalone spike first.

---

## Motion budget (if Option A-C)

Keep to 2-3 intentional moves:

1. Section reveal (existing `data-reveal` pattern)
2. Soft quote emphasis on hover/focus (border or underline; no bounce)
3. Optional slow crossfade between two quotes **only** if `prefers-reduced-motion: no-preference`

No autoplay carousels with opaque controls. No emoji. No floating badges on faces.

---

## Agent recommendation

Ship concept **B** with copy Option 2. Fill with cleared A1 + A2 (+ one audience line if needed). Keep Option D in the spike HTML only until KK says go.
