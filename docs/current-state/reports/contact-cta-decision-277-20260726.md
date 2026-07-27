# Contact CTA decision memo — #277

**Captured:** `2026-07-26` (public probe; America/Vancouver day)  
**Issue:** [WalksWithASwagger/kriskrug-wp#277](https://github.com/WalksWithASwagger/kriskrug-wp/issues/277)  
**Lane:** Track A / platform decision (docs only — **no live WP writes**)  
**Related:** epic [#222](https://github.com/WalksWithASwagger/kriskrug-wp/issues/222); closed form-routing [#128](https://github.com/WalksWithASwagger/kriskrug-wp/issues/128) / [#174](https://github.com/WalksWithASwagger/kriskrug-wp/issues/174); content-architecture PR [#273](https://github.com/WalksWithASwagger/kriskrug-wp/pull/273) (issue body “Related: #273”)

## Verdict (provisional)

**Keep the lightweight email CTA** until KK completes the evidence checklist below and marks a different option.

Public `/contact/` is a coherent conversion page: intent copy + mailto primary action + Beehiiv newsletter secondary. There is **no** live contact form. Historical Jetpack Forms created notification/visibility debt (#128 / #174). Adding a plugin form or CRM intake without a measured friction signal would reintroduce that blast radius for no proven gain.

This memo does **not** close #277. Closure needs KK’s checklist + an explicit option pick.

## Public probe — `/contact/` (2026-07-26)

| Check | Result |
|---|---|
| URL | `https://kriskrug.co/contact/` |
| HTTP | `200` |
| WP page | id `2418`, slug `contact`, status `publish` |
| REST `modified` | `2026-07-24T17:05:35` |
| Cache | Pagely HIT + Jetpack Boost cache HIT on HTML fetch |
| Content marker | `<!-- content-architecture-2026:contact -->` present |
| `<form>` / `<input>` / `<textarea>` | **0 / 0 / 0** |
| Jetpack / CF7 / WPForms / Gravity markers | **none** in public HTML |
| Primary CTAs | mailto only (see below) |
| Newsletter CTA | external Beehiiv (`https://kriskrug.beehiiv.com/`) |

### Current CTA behavior

Page promise (hero): *“The fastest path is email.”* Visitors are coached to send context (who / when / where / what would make the work useful), then offered:

| Control | Label | Target | Role |
|---|---|---|---|
| Primary button | Email Kris | `mailto:feelmoreplants@gmail.com?subject=Inquiry%20from%20kriskrug.co` | Open mail client with prefilled subject |
| Secondary button | Get the newsletter | Beehiiv | List growth (not inquiry) |
| Mid-page plaintext | `feelmoreplants@gmail.com` | `mailto:feelmoreplants@gmail.com` (no subject) | Copy/paste fallback |
| Lower primary | Send the note | same mailto + subject as Email Kris | Repeat convert |
| Lower secondary | Subscribe free | Beehiiv | Repeat newsletter |

Intent scaffolding (not forms): four cards — talk/workshop, strategy/training, media/podcasts (links EPK), community collaborations.

**Implication:** conversion depends on the visitor having a working mail client or copying the address. Mobile OS mail handlers usually work; locked-down corporate browsers and webmail-only users may bounce. That friction is real in the abstract but **unmeasured** here — hence the checklist.

### Intentional history (why email is the status quo)

- `CONTENT-ARCHITECTURE-RESET-2026-07-01.md`: Contact preflight found **no Jetpack form block** in raw content; migration **preserved the email contact path** instead of inventing a form.
- Post-Jetpack cleanup (`post-jetpack-cleanup-20260701T194455Z.md`): Contact replacement recorded **PASS**; Jetpack core inactive; site still runs other plugins including **Zero BS CRM** (active in that snapshot) — but `/contact/` does **not** surface a CRM form.

## Decision options

### A — Keep email CTA only *(recommended default)*

**Do:** Leave `/contact/` as-is. Close #277 after checklist confirms no material complaints / volume failure.  
**Pros:** Zero plugin surface; matches page copy; avoids replaying Jetpack Forms notification debt; newsletter already has a separate Beehiiv path.  
**Cons:** No structured fields, no spam filter at form layer, no CRM auto-logging, mailto friction for some browsers.  
**When to pick:** Checklist shows inquiries arrive, KK replies from Gmail without missing leads, no visitor complaints about “no form.”

### B — Add a simple form later *(only if friction is visible)*

**Do:** File/implement a **separate** issue (stub drafted at `issues-to-create/contact-form-implementation-stub-from-277.md`). Do **not** bolt a form onto #277.  
**Pros:** Structured briefs; works without a mail client; can add honeypot/Akismet/CAPTCHA; optional CRM handoff.  
**Cons:** Plugin/security/spam/deliverability work; CASL/consent if any list capture; admin notification routing must be proven (the old failure mode).  
**When to pick:** Checklist shows missed leads, repeated “how do I contact you?” confusion, or mailto opens failing for target buyers.

### C — Route contact to CRM / newsletter tooling only

**Do:** Point inquiry CTA at Zero BS CRM (or similar) and/or keep newsletter on Beehiiv — **only** if KK already works that pipeline daily.  
**Pros:** Centralized contacts; tagging; less inbox sprawl *if* CRM is actually used.  
**Cons:** CRM was not the public contact path after architecture reset; marketing drafts treat CRM/ESP setup as gated; risk of coupling inquiry + newsletter without clear consent; more moving parts than mailto.  
**When to pick:** Clear workflow need (e.g. KK already triages every lead in CRM, wants tags/pipeline, and accepts form+spam ops). Newsletter-only is **not** a substitute for keynote/media inquiry.

## Evidence checklist (KK)

Complete privately (Gmail / Search Console / analytics). **Do not paste submitter PII into GitHub.**

### Complaints / broken-flow

- [ ] Any visitor / producer / booker messages in the last ~90 days saying they could not contact via `/contact/`?
- [ ] Any social DMs or replies that imply “site has no contact form” as a blocker?
- [ ] Any support/agent notes since Jetpack Forms removal about lost inquiries?

### Email volume / quality

- [ ] Rough weekly count of inbound mail with subject `Inquiry from kriskrug.co` (or equivalent contact intent) — too low / acceptable / overwhelming?
- [ ] Are briefs usually usable (audience, date, venue, budget) given the on-page “what to include” prompts?
- [ ] Any sense that serious buyers bounce before emailing (gut + optional analytics: `/contact/` → exit without outbound click if measurable)?

### Workflow need

- [ ] Is Gmail (current mailto destination) still the monitored reply path KK actually uses?
- [ ] Is Zero BS CRM (or another CRM) part of daily lead triage today? If no → Option C is out.
- [ ] Is the problem “capture/structure” (favors B) or “I already get enough good email” (favors A)?

### Decision stamp

- [ ] **Pick:** A / B / C  
- [ ] If **A:** comment on #277 and close.  
- [ ] If **B:** file the stub in `issues-to-create/contact-form-implementation-stub-from-277.md` (after KK edits), then close #277 as decided.  
- [ ] If **C:** open a CRM-routing issue with owner, consent, and spam requirements; do not reuse a generic form stub blindly.

## Recommendation summary

| Signal from checklist | Choice |
|---|---|
| No complaints + acceptable email volume | **A — keep email CTA** |
| Mailto friction or missed structured leads | **B — simple form later** (new issue) |
| CRM already owns triage and KK wants intake there | **C — CRM route** (new issue) |

**Agent recommendation today:** **A**, contingent on KK checklist. Stub for **B** is staged in-repo so filing is one approval away — not filed via `gh` from this session.

## Out of scope / not done

- No live WordPress content, plugin, or snippet changes.
- No form plugin install, CRM form publish, or Beehiiv embed change.
- No `gh issue create` for the implementation stub (write-gated / leave markdown only).
- Issue #277 left open for KK decision stamp.
