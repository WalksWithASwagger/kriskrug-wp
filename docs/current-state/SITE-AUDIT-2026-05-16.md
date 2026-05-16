# Site audit — 2026-05-16 (reader-facing pass)

**Scope:** what a visitor encounters when they land on kriskrug.co, not the SEO machinery underneath. This is the punch-list Track A (content/SEO) can chew through on the current Catch Responsive theme without waiting for Aurora.

**Method:** `curl` of homepage + main nav targets + spot-checks of H1/H2 hierarchy, hero copy, popup behavior, and link targets. Mobile was not tested live — flagged as a follow-up.

---

## Severity legend

- **🔴 P0** — visible to every visitor on first paint. Fix this week.
- **🟡 P1** — confuses topical signal or breaks a journey. Fix this month.
- **🟢 P2** — polish / accumulated cruft. Fix during Aurora migration or whenever.

---

## 1. Homepage — `https://kriskrug.co/`

### 🔴 P0 — hero copy is the wrong positioning

The page title is modern: *"Kris Krüg | Generative AI Tools & Techniques, Empowering Events & Organizations for the AI Age."* But the first paragraph a visitor reads is:

> *"I believe in the power of connection. For me, it's not just about revealing moments through photographs or managing social media feeds…"*

This is KK's 2018-era event-photographer/community-manager positioning. The current KK is **Executive Director of BC + AI Ecosystem + founder of TheUpgrade.ai + creative AI educator**. A reader hits a positioning mismatch within 50 words.

**Action:** rewrite the hero copy block to match the current title + the byline KK now uses on every post (`Executive Director, BC + AI Ecosystem; teaches creative pros through TheUpgrade.ai`). Pull the voice from the "Both Hands Full" framing in [Make Culture, Not Content](https://kriskrug.co/2026/05/16/make-culture-not-content/).

### 🔴 P0 — the only H1 on the page is "Why Choose Me?"

Catch Responsive doesn't emit an H1 from the page title. The first H1 in the DOM is a body-level *"Why Choose Me?"* heading. Google reads that as the page's primary topic.

**Action:** add an H1 at the top of the homepage content with KK's actual positioning. Demote *"Why Choose Me?"* to H2.

### 🟡 P1 — Stewart Butterfield testimonial reads as dated

The Slack-attributed testimonial about KK at conferences pre-dates Butterfield's 2022 departure from Slack. The testimonial may still be accurate, but the attribution makes the site feel frozen in time.

**Action:** verify with KK whether to keep / re-caption (e.g., `Stewart Butterfield, then-CEO of Slack`) / rotate to a newer testimonial.

### 🟡 P1 — auto-opening Beehiiv popup at 1000ms

A Popup Maker rule auto-opens the Beehiiv newsletter popup 1 second after page load on every visit (`pum-3884`, cookie window 1 month). For a returning reader this is fine; for first-time visitors it interrupts the hero before they've finished reading. Conversion-killer in 2026 web design.

**Action:** change trigger from `auto_open` (1000ms) to `scroll_open` at 50% scroll OR `time_open` at 30s. Keep the cookie suppression.

### 🟢 P2 — sidebar widgets feel 2018

Pinned posts and tag cloud sidebar dominate the right rail. The hierarchy isn't terrible, but the design itself looks dated against the new in-post enrichment work.

**Action:** defer to Aurora. Aurora's FSE templates handle this naturally with a cleaner layout.

---

## 2. About — `https://kriskrug.co/about/`

### 🔴 P0 — page has 4 H1s

```
<h1 class="entry-title">Techartist, quasi-sage, cyberpunk anti-hero from the future.
<h1 class="wp-block-heading">Publications
<h1 class="wp-block-heading">Portraits:
<h1 class="wp-block-heading">Clients
```

The entry-title H1 is correct. The other three should be H2. This is exactly the kind of sitewide hierarchy violation that confuses Google's topical extraction and the TRAFFIC-DIAGNOSTIC doc called out.

**Action:** wp-admin edit /about/, demote `Publications`, `Portraits:`, `Clients` from H1 to H2. ~5 min REST PATCH.

### 🟢 P2 — copy is good but long

About is dense with text. Not broken — just a candidate for a punk-zine reformat when Aurora ships.

---

## 3. Blog — `https://kriskrug.co/blog/`

### 🟡 P1 — no H1 on the page

The blog index page returns zero `<h1>` elements. Catch Responsive renders the archive list directly without a page heading. Search engines treat the page as "topic-less list."

**Action:** add an H1 (e.g., *"Field Notes from the AI Frontier"* or whatever frames KK's writing). Two paths:
- a) Set a Page-style hero block above the archive list (requires Catch Responsive customization or a Code Snippets PHP filter)
- b) Defer to Aurora, which handles archive H1s natively

Recommend deferring to Aurora — adding a hero to Catch Responsive's blog index is fragile.

---

## 4. Services — `https://kriskrug.co/generative-ai-services/`

URL is correct (the nav links here, not `/services/`). Returns 200. Not inspected this pass — flagged for next session as part of the punch-list:

- Verify H1 hierarchy
- Verify pricing/offer freshness
- Verify CTA still goes where KK wants

### 🟡 P1 — `/services/` itself is 404

If anyone types `/services/` directly (or it's referenced anywhere in old emails / cards / external links), they hit a 404. The nav link works because it points at the longer slug, but `/services/` should at least redirect.

**Action:** add a 301 redirect `/services/` → `/generative-ai-services/` via Redirection plugin (or .htaccess). 30-second fix.

---

## 5. Other nav targets

| Page | Status | Notes |
|---|---|---|
| `/about/` | 200 | 4× H1s (P0 above) |
| `/blog/` | 200 | no H1 (P1 above) |
| `/motleykrug-podcast/` | 200 | not deep-inspected |
| `/generative-ai-services/` | 200 | not deep-inspected |
| `/recent-projects-include/` | 200 | weird slug; functional but ugly URL |
| `/events/` | 200 | not deep-inspected |
| `/contact/` | 200 | entry-title H1 looks right |
| Newsletter (Beehiiv) | external | OK |

### 🟡 P1 — `/work/` redirects to an 11-year-old single post

```
HTTP/2 301
location: https://kriskrug.co/2011/11/19/workin-with-the-united-nations-on-a-digital-crowdsourcing-campaign-to-stop-the-spread-of-hiv/
```

Someone landing on `/work/` (a natural URL to try) gets bounced to a 2011 UN HIV crowdsourcing post. Dead-end UX for anyone looking for KK's current work.

**Action:** change the redirect to point at `/recent-projects-include/` (or wherever current work lives). Even better: rename `/recent-projects-include/` → `/work/` and add a 301 back the other direction.

### 🟢 P2 — `/recent-projects-include/` slug

That URL pattern is awkward (looks like a sentence fragment, breaks SERP titles). Renaming it `/work/` with a 301 chain solves both this and the `/work/`-redirect issue above.

---

## 6. Sitewide

### 🟡 P1 — heavy theme stack

Catch Responsive + jQuery + jQuery Migrate + multiple Jetpack JS bundles + Popup Maker + Site Kit + Genericons. Inline critical CSS is ~50KB. Already flagged in [`TRAFFIC-DIAGNOSTIC-2026-05-15.md`](TRAFFIC-DIAGNOSTIC-2026-05-15.md). Aurora is the structural fix.

**Action (interim):** the Popup Maker auto-open kills LCP and INP both. Changing it to scroll-trigger should claw back a meaningful chunk of Core Web Vitals without touching the theme.

### 🟢 P2 — image alt-text site-wide

Most pre-2026 images have empty alt. Already in the FIX_QUEUE (P1.4). Vision-LLM batch is the right tool when KK greenlights.

### 🟢 P2 — mobile rendering not tested this pass

The viewport meta is set correctly and the theme has mobile-menu CSS, but actual narrow-viewport testing requires Chrome MCP with a resized window. Add to next session.

---

## Punch list (Track A pulls from this)

Ordered by leverage:

1. **🔴 Rewrite homepage hero copy** (P0) — biggest first-impression fix
2. **🔴 Add H1 to homepage; demote "Why Choose Me?" to H2** (P0) — search signal repair
3. **🔴 Demote 3 H1s on About to H2** (P0) — same search signal repair, REST PATCH
4. **🟡 Change Popup Maker trigger** from auto-1s to scroll-50% or time-30s (P1) — UX + Core Web Vitals
5. **🟡 Fix `/work/` redirect** to point at current projects (P1) — broken visitor journey
6. **🟡 301 `/services/` → `/generative-ai-services/`** (P1) — direct-URL coverage
7. **🟡 Verify Stewart Butterfield testimonial** attribution / rotate to newer (P1) — credibility
8. **🟢 Mobile pass via Chrome MCP** — narrow viewport (375px iPhone, 768px tablet) — find layout breaks
9. **🟢 Deep-inspect /services/, /events/, /podcast/, /projects/** — apply same H1 + freshness check
10. **🟢 Image alt-text batch** (existing FIX_QUEUE P1.4)
11. **🟢 Add H1 to blog index** — recommend deferring to Aurora

Items 1–6 are mechanical and unblock next session's Track A work without any theme dependency.

---

## What this audit deliberately does NOT cover

- **The redesign itself** — Track B owns that
- **Pricing / business model freshness** — that's KK's call, not an auditor's
- **Notion / KB hygiene** — separate workstream
- **Email / Beehiiv funnel beyond the popup trigger** — Track A scope is the site, not the marketing stack

When Aurora ships (Track B), most of the P2 polish items resolve automatically. P0 and P1 items should ship on the current theme first — they affect SEO and UX in the wait window before redesign.

---

## Track A in-progress (2026-05-16)

### Completed via REST PATCH this session

1. **Homepage hero rewrite** (page ID 3930, not 247 as initially suspected) — replaced the "I believe in the power of connection / quilt of creative awesomeness" opening with current positioning: "Generative engines now spill out adequate everything..." plus a second paragraph naming KK as ED of BC + AI Ecosystem and founder of TheUpgrade.ai. Inline `<a>` links added directly (no auto-link pass needed). Verified live at https://kriskrug.co/.
2. **Homepage H1 added** — inserted `<h1>Kris Krüg, Generative AI for Creative Professionals</h1>` at top of content. Confirmed live via curl. Note: the theme still emits an empty `<h1 class="entry-title">` above the content — that is a theme issue for Track B / Aurora and cannot be removed via REST.
3. **Homepage "Why Choose Me?" demoted** from H1 to H2 (in same PATCH as #1/#2).
4. **About page H1 demotions** (page ID 1208) — `Publications`, `Portraits:`, `Clients` all demoted to H2. Verified live at https://kriskrug.co/about/. Only remaining H1 is the theme-emitted `entry-title`.

Backups of pre-PATCH raw content saved to `/tmp/old-homepage-hero.html` and `/tmp/old-about.html` (session-local; re-fetch via `?context=edit` if a future session needs them).

### Skipped — require wp-admin / plugin access

5. **Popup Maker trigger change (P0)** — requires the wp-admin Popup Maker settings UI. Steps for KK:
   - wp-admin → Popup Maker → Popups → edit the "subscribe" popup
   - Triggers tab → change from "Auto Open" to "Click Open" (or add a 30s+ delay with a 7-day cookie so it fires once per visitor)
   - Save and test in an incognito window

6. **`/work/` redirect fix (P1)** — requires the Redirection plugin OR a Code Snippet using `template_redirect`. Steps for KK:
   - Install/activate "Redirection" plugin if not present (Tools → Redirection)
   - Add a 301: source `/work/` → target `/portfolio/` (or whichever current-projects page KK wants; confirm target first)
   - Test by hitting https://kriskrug.co/work/ in incognito; should land on the target with a 301

7. **`/services/` → `/generative-ai-services/` 301 (P1)** — same Redirection-plugin pattern as #6. Source `/services/`, target `/generative-ai-services/`, type 301.

Items 5–7 are roughly 10-15 minutes of wp-admin clicking once Redirection is installed. A future Claude Code session with Chrome MCP wp-admin auth could also execute them.
