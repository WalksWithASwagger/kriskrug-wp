# Contact CTA decision brief — #277 (2026-08-16 recheck)

**Captured:** 2026-08-16 evening PT (`2026-08-17T02:37Z` UTC)  
**Issue:** [WalksWithASwagger/kriskrug-wp#277](https://github.com/WalksWithASwagger/kriskrug-wp/issues/277)  
**Lane:** Track A / platform decision (docs only — **no live WP writes, no form implementation**)  
**Mode:** public / logged-out HTML + REST. No wp-admin, no plugin mutate, no cache purge.  
**Predecessor:** [`contact-cta-decision-277-20260726.md`](contact-cta-decision-277-20260726.md) (merged as PR [#519](https://github.com/WalksWithASwagger/kriskrug-wp/pull/519)). This file is a live recheck, not a replacement of that memo's KK checklist.  
**Related:** #424 QA (no form controls on main-nav routes); closed form-routing #128 / #174; closed contact-page refresh #421; Jetpack-delete gate #276.

## Headline for KK

**Keep the lightweight email CTA. Do not add a contact form.**

Live `/contact/` is still mailto + Beehiiv. There is still **no** contact form, Calendly embed, Typeform, or CRM intake. The page body has not changed since `2026-07-24`. Three weeks of later audits (#424, a11y 2026-08-02, security headers 2026-08-15) independently re-confirm zero `<form>` tags. Adding a plugin form would recreate the Jetpack Forms notification/spam/accessibility blast radius without a measured conversion failure.

This brief does **not** close #277. Closure still needs KK's Gmail-volume stamp. The recommendation is Option A so KK can close after a 30-second inbox check, not after more research.

---

## Verification

| Check | Why | Command / method | Result |
|---|---|---|---|
| Live theme Version | Do not treat repo `style.css` as production | Public `GET /wp-content/themes/kk-aurora/style.css` | **PASS** — `Version: 1.6.5` |
| `/contact/` HTTP | Page is up | Unauthenticated GET | **PASS** — `200`, Boost `hit`, gateway `HIT` |
| REST identity | Slug/id match the architecture payload | `GET /wp-json/wp/v2/pages?slug=contact` | **PASS** — id `2418`, slug `contact`, `publish`, title `Contact Kris Krüg` |
| REST freshness | Did the body move since the July memo? | same | **PASS (unchanged)** — `modified` still `2026-07-24T17:05:35` |
| Form markup | Confirm #424 QA | Parse 8 main-nav routes for `<form>`, `<input>`, `<textarea>`, `<select>`, `<button>` | **PASS** — **0 / 0 / 0 / 0 / 0** on every route |
| Form-plugin markers | Jetpack Forms / CF7 / WPForms / Gravity / Fluent / CRM | Case-insensitive HTML scan | **PASS** — none |
| Calendly / Typeform / Tally / HubSpot | Alternate booking/intake | HTML scan | **PASS** — none |
| Beehiiv embed vs link | Newsletter path | HTML scan | **PASS** — outbound link only; **0** `embeds.beehiiv` iframes on sampled routes |
| Visitor-complaint issues | “Broken contact / no form” reports in this repo | `gh issue list --search "contact form"` | **PASS (none found)** — open items are #277 itself, #276, #424, #744. No new complaint issue since Jetpack Forms came off. |
| Form implementation | Explicit non-goal | — | **NOT RUN** — do not implement a form |
| Gmail inquiry volume | Acceptance criterion 2 on #277 | Needs KK inbox | **BLOCKED** — agent cannot see `feelmoreplants@gmail.com` |
| Authenticated plugin list | Confirm Zero BS CRM / Akismet still installed | wp-admin / REST plugins | **SKIPPED** — unauthenticated; not required for the public-CTA decision |

**Checks not run:** `make status-readonly` (not needed for this CTA inventory); pixel gate; wp-admin Jetpack Forms inbox; analytics `/contact/` → mailto click rates.

---

## What exists today

### Live stack at capture

| Signal | Value |
|---|---|
| WordPress generator | `7.0.4` |
| Site Kit | `1.185.0` |
| Aurora (public `style.css`) | **1.6.5** (repo `main` may already carry 1.6.6 — ignore repo Version for live claims) |
| Contact page | id `2418`, `<!-- content-architecture-2026:contact -->` still present |
| Last content edit | 2026-07-24 (same timestamp as the 2026-07-26 memo) |

### `/contact/` conversion controls

Hero copy still coaches the visitor: *“The fastest path is email.”* Ask for who / when / where / what would make the work useful. Four intent cards (talk/workshop, strategy/training, media/podcasts, community) are copy, not forms.

| Control | Label | Target | Role |
|---|---|---|---|
| Primary button | Email Kris | `mailto:feelmoreplants@gmail.com?subject=Inquiry%20from%20kriskrug.co` | Inquiry |
| Secondary button | Get the newsletter | `https://kriskrug.beehiiv.com/` | List growth, **not** inquiry |
| Mid-page plaintext | `feelmoreplants@gmail.com` | `mailto:feelmoreplants@gmail.com` (no subject) | Copy/paste fallback |
| Lower primary | Send the note | same mailto + subject as Email Kris | Repeat convert |
| Lower secondary | Subscribe free | Beehiiv | Repeat newsletter |

**Confirmed vs #424 QA:** no contact form. Only mailto + Beehiiv. Every “button” is an `<a>` (`.kk-contact-button` / `.aurora-button`). Zero native `<button>` / `<input>` / `<textarea>`.

### Homepage + footer contact CTAs

Sampled routes: `/`, `/about/`, `/speaking/`, `/services/` (canonical `/generative-ai-services/`), `/work/`, `/blog/`, `/photography/`, `/contact/`.

**Header (every sampled route)**

- Nav: `Contact` → `/contact/`
- Utility: `Newsletter` → Beehiiv
- Primary CTA: `Work with me` → `/services/` (not a form)

**Homepage body**

- `Get the weekly email` → Beehiiv
- No mailto on the homepage itself

**Footer (homepage `<footer>`, same pattern on inner pages)**

- `Work with me` → `/services/`
- `Get in touch` → `/contact/`
- `Subscribe free` → Beehiiv
- Utility `Contact` → `/contact/`
- No mailto in the footer

**In-page funnels into `/contact/` (not extra destinations)**

| Route | Label |
|---|---|
| `/about/` | Contact Kris (×2) |
| `/speaking/` | Start a booking conversation |
| `/services/` | Start a conversation |
| `/work/` | Talk about a project |

### Conversion-path count (distinct destinations)

There are **two** public conversion destinations. Everything else is a link into those two.

| # | Path | Present? | Where | Converts to |
|---:|---|---|---|---|
| 1 | **mailto** (Gmail) | **Yes — 3 anchors, 1 address** | `/contact/` only | Keynote / media / strategy / community inquiry |
| 2 | **Beehiiv** (hosted list) | **Yes — header + footer + contact secondary** | Sitewide | Newsletter. Not a brief. |
| 3 | On-site `/contact/` links | **Yes — nav, footer Get in touch, page-level CTAs** | All sampled routes | Funnel into path 1 |
| 4 | Form plugin (Jetpack / CF7 / WPForms / Gravity / Fluent) | **No** | — | — |
| 5 | Native `<form>` / search form on main-nav routes | **No** | — | — |
| 6 | Calendly / other scheduler | **No** | — | — |
| 7 | Typeform / Tally / HubSpot / Mailchimp embed | **No** | — | — |
| 8 | Beehiiv **iframe** embed | **No** on sampled routes | — | Link-out only |
| 9 | `tel:` | **No** on current `/contact/` | Historical raw export had a phone line; live page does not | — |
| 10 | Zero BS CRM public form | **No** in public HTML | CRM may still be installed; it is not the contact path | — |

**Net:** inquiry = Gmail via mailto. List = Beehiiv. Booking/media/project CTAs around the site all dump into `/contact/`, then mailto.

### Independent later audits (same finding)

| Source | Date | Quote / finding |
|---|---|---|
| #424 inventory [`INTERACTION-STATES-GAP-INVENTORY.md`](../INTERACTION-STATES-GAP-INVENTORY.md) | 2026-07-25 | Zero `<form>` / `<input>` / `<textarea>` / `<select>` / `<button>` on eight main-nav routes. Contact page: mailto + two link-buttons. Newsletter is an outbound Beehiiv link, not an embed. |
| [`A11Y-WCAG-AUDIT-2026-08-02.md`](../A11Y-WCAG-AUDIT-2026-08-02.md) | 2026-08-02 | WCAG 3.3.x form criteria **not applicable**. `/contact/` is mailto; newsletter is off-site Beehiiv. |
| [`security-headers-audit-2026-08-15.md`](security-headers-audit-2026-08-15.md) | 2026-08-15/16 | `/contact/` has no form (three `mailto:` links, zero `<form>` tags), so the classic clickjack-the-form target is absent. |
| This probe | 2026-08-16 | Same three mailtos, same Beehiiv URLs, still zero forms. Page `modified` unchanged since 2026-07-24. |

---

## What a “real form” would cost

Do **not** implement from this issue. If KK later picks Option B, file the existing stub [`issues-to-create/contact-form-implementation-stub-from-277.md`](../../../issues-to-create/contact-form-implementation-stub-from-277.md) as a **new** issue. Cost, honestly:

### Plugin / stack

- Re-enabling **Jetpack Forms** is the wrong answer. #128 / #174 exist because submissions piled up in an unmonitored wp-admin inbox. Jetpack core is slated for delete (#276).
- A small dedicated plugin (Fluent, a tiny CF7, native `wp_mail` + honeypot) is still a new Pagely-resident PHP POST surface, update cadence, and rollback plan.
- A hosted embed (Typeform, Tally, Beehiiv form) moves spam off WordPress but adds a third-party script, privacy copy, and a split between “inquiry” and “subscribe” that the current page already handles by **not** mixing them.
- Zero BS CRM intake only pays if KK already triages every lead there. Public HTML does not show a CRM form today. That is Option C, not a stealth add-on.

### Spam and deliverability

- Mailto has **no on-site spam surface**. The inbox still gets unsolicited mail; Gmail’s filters already run. A form creates a new unauthenticated POST, so you owe honeypot and/or CAPTCHA, Akismet or equivalent, rate limiting, and a **proven** notification path.
- The last form stack failed on that last item: notifications existed, nobody watched them. A replacement that is not tested end-to-end (test submit arrives, not in spam, KK actually sees it) is worse than mailto.
- Hosted forms still need a monitored destination and a subject prefix for filters.

### Accessibility

- Today WCAG 3.3.1–3.3.4 are **N/A** because there are no form controls (#424, 2026-08-02 a11y audit).
- A real form immediately requires visible labels, error identification, error suggestion, focus management, and a non-color-only invalid state. #424 also noted the theme’s `.aurora-form-*` classes are dead CSS with **no live consumer**. Shipping a form forces that primitives work (or an inaccessible plugin default).
- mailto is a native `<a>`. Keyboard and screen-reader support is already the browser’s. The remaining friction is “no mail client,” not “unlabeled field.”

### Security / privacy / ops

- Security-headers audit: `/contact/` is not a clickjack-the-form target **because there is no form**. Adding one raises the value of `frame-ancestors` / `X-Frame-Options` (#709) before go-live.
- CASL: do not auto-subscribe inquirers. Beehiiv stays a separate opt-in. The current split already does this correctly.
- Retention: WP form entries are personal data. The repo is public. #128’s rule still holds — no submitter PII in GitHub.
- Theme/cache: Pagely + Jetpack Boost. Form pages often need cache bypass on POST. Mailto needs none.

**Rough effort if Option B is ever chosen:** a dedicated issue, plugin/hosting pick, spam + notification proof, a11y pass, privacy-policy line, cache exception, rollback to the 2026-07-24 mailto payload. That is days of gated work, not a snippet.

---

## Decision options (unchanged)

| Option | Do | When |
|---|---|---|
| **A — Keep email CTA** *(recommended)* | Leave `/contact/` as-is. Close #277 after KK confirms Gmail volume is acceptable. | No complaints + inquiries already arrive in Gmail. |
| **B — Simple form later** | File the stub as a **new** issue. Do not bolt a form onto #277. | Documented missed leads or mailto failure for target buyers. |
| **C — CRM / newsletter-only intake** | Separate CRM-routing issue. Newsletter-only is **not** a substitute for keynote/media inquiry. | KK already lives in that pipeline daily. |

---

## Recommendation

**Option A. Keep-as-is.**

Reasons, in order:

1. The lightweight CTA is complete, not a stub: intent copy, two mailto buttons, a plaintext address, Beehiiv as a **separate** list path.
2. Sitewide booking/project CTAs already point at `/contact/`. The funnel is coherent.
3. #424 and later a11y/security audits treated “no form” as a **simplification**, not a gap to fill.
4. The last form created operational debt (#128 / #174). Cost of a replacement is real; benefit is hypothetical until KK says volume or friction is bad.
5. Live content has been stable for 23 days. No GitHub issue describes a visitor who could not contact KK.

**What KK still owes (private, no PII in GitHub):**

- [ ] Any “I couldn’t contact you / there’s no form” messages in the last ~90 days?
- [ ] Rough weekly count of mail with subject `Inquiry from kriskrug.co` — too low / fine / too much?
- [ ] Is `feelmoreplants@gmail.com` still the inbox KK actually answers?

If those three are “no / fine / yes,” **comment on #277 and close it.** If any is a real miss, pick B and file the stub. Do not leave #277 open as an unbounded “maybe add a form someday” ticket.

---

## Out of scope / not done

- No live WordPress content, plugin, snippet, or theme change.
- No form plugin install, CRM form publish, Calendly embed, or Beehiiv iframe.
- No `gh issue create` from the Option B stub.
- #277 left open for KK’s stamp.
- #276 (delete inactive Jetpack) can proceed without waiting on a form; mailto does not depend on Jetpack Forms.
