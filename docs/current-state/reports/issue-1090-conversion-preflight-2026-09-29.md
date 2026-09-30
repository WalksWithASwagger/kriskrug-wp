# #1090 conversion preflight — inventory and synthetic packet

**Track:** A — Content + SEO (measurement prep only)
**Issues:** [Refs #1103](https://github.com/WalksWithASwagger/kriskrug-wp/issues/1103), [Refs #1090](https://github.com/WalksWithASwagger/kriskrug-wp/issues/1090)
**Status:** repo-side preparation. **Keep #1090 open.** This child does not select the conversion, does not mark a GA4 key event, and does not write WordPress.
**Inspected:** 2026-09-30, logged-out GET only. No production form was submitted, including with a fake address.
**SEO brief:** Sulu SHIP note on #1103 (comment 5911307211). A conversion counts only on a verified success signal, never on a click. Inventory both candidates in full, including `/speaking/` and article footer entry points.

The dated GA4 counts on #1090 are **dated provenance only**. This packet does not refresh them and does not invent new property totals.

---

## 0. Method and boundary

Read-only logged-out inspection of public HTML plus the Aurora templates that own the recurring chrome. Network GETs only. No POST, no Beehiiv subscribe, no mailto send, no GA4 admin, no WordPress save.

Routes fetched on 2026-09-30:

| Route | Final URL | HTTP | Same-origin form | Beehiiv iframe |
|---|---|---|---|---|
| `/` | `https://kriskrug.co/` | 200 | no | no |
| `/speaking/` | `https://kriskrug.co/speaking/` | 200 | no | no |
| `/contact/` | `https://kriskrug.co/contact/` | 200 | no | no |
| `/subscribe/` | `https://kriskrug.co/subscribe/` | 200 | no | **yes** |
| `/newsletter/` | 301 → `/2023/09/18/newsletter-002-rebirth-and-revolution/` | 200 | no | no |
| `/blog/` | `https://kriskrug.co/blog/` | 200 | no | no |
| `/work/`, `/about/` | same-host 200 | 200 | no | no |
| `/podcast-guesting-page-epk/` | 200 | 200 | no | no |
| `/generative-ai-services/` | 200 | 200 | no | no |
| Article | `https://kriskrug.co/2026/05/07/web-summit-vancouver-2026/` | 200 | no | no |
| Article | `https://kriskrug.co/2026/09/29/world-tourism-day-capilano-glowing-jellyfish-problem/` | 200 | no | no |

A GET/network inspection **cannot prove** successful-submit tracking. Success behavior is unverified unless a local fixture, authorized staging environment, or provider-admin readback supplies it. That limit is why the candidate helper is tested only against synthetic data.

Popup Maker / `popmake` chrome from 2026-05 backups was **absent** on every 2026-09-30 route above. Do not inventory that historical popup as a current entry.

---

## 1. Newsletter signup inventory

Provider: Beehiiv publication hosted at `https://kriskrug.beehiiv.com/`. Form ownership is Beehiiv, not WordPress. kriskrug.co does not render a same-origin email field except inside the `/subscribe/` iframe.

### 1.1 Entry points

| URL / surface | UI entry | What the visitor actually gets | Success mechanism observable from kriskrug.co | Existing observable GA4 (read-only) |
|---|---|---|---|---|
| Site header (all inspected routes) | Utility link **Newsletter** | Same-tab outbound to `https://kriskrug.beehiiv.com/` | None. This is a click. | Site Kit `G-X7JE8B32L7` is present (`kk-gtag-delayed`). Enhanced-measurement outbound `click` is the dated #1090 observation; **not re-measured here**. |
| Site footer tile (all inspected routes, including `/speaking/` and both articles) | **Subscribe free** | Same-tab outbound to `https://kriskrug.beehiiv.com/` | None. Click. | Same as header. |
| Homepage `#newsletter` band | **Get the weekly email** | Same-tab outbound to Beehiiv | None. Click. | Same. |
| `/blog/` writing band | **Get the weekly email** | Same-tab outbound to Beehiiv | None. Click. | Same. |
| `/contact/` page body | **Get the newsletter** and a second **Subscribe free** (`target=_blank` `rel=noopener noreferrer`) | New-tab outbound to Beehiiv | None. Click. | Same. |
| `/subscribe/` | Cross-origin iframe `https://embeds.beehiiv.com/552dc13c-76df-4a0b-9663-b7e668042177` (`data-test-id="beehiiv-embed"`) plus the shared header/footer links | Signup UI lives on `embeds.beehiiv.com` | **Inaccessible** from the parent page. Beehiiv's default post-submit state is an in-iframe success message. | Page-level `page_view` / delayed gtag only. Parent cannot see iframe success. |
| `/newsletter/` | Not a form | 301 to a 2023 newsletter *post* | Not a signup path. Historical Beehiiv click-wraps and one `magic.beehiiv.com` Subscribe link sit in old post HTML; they are content, not current chrome. | n/a |
| Theme pattern `component-utility-system.php` | **Join the newsletter** | Repo-only pattern pointing at Beehiiv | Not observed on the inspected live routes | n/a |

Neither candidate is the default. `newsletter_submit` is the newsletter candidate name only.

### 1.2 `/subscribe/` iframe limitation

The live `/subscribe/` embed is a **cross-origin iframe** on `embeds.beehiiv.com`. A GET of the embed shell on 2026-09-30 returned a Beehiiv SPA (`/assets/index-*.js`) with Beehiiv's own GTM container `GTM-WJXL7FH`. The parent page has no same-origin access to that document.

**Do not implement postMessage listeners.** No documented parent-page subscribe-success API was observed in the embed shell, and Sulu's brief forbids guessing one.

Beehiiv's current public subscribe-form help (updated 2026-07-27) names the provider-supported success routes:

1. **Show a success message** inside the form (default, up to 80 characters). That message stays in the iframe. kriskrug.co cannot count it.
2. **Redirect to an external website** after signup. If KK points that redirect at a first-party thank-you URL on kriskrug.co, the parent can treat landing on that URL as `thank_you_state`.
3. **Email submitted** automations and the Subscribers report, including UTMs on the embed URL. Those are Beehiiv-admin surfaces, not page-side events.
4. An **Attribution tracking script** that forwards UTMs into Beehiiv. That is acquisition attribution, not a verified subscribe conversion.

Until one of those provider routes is configured and readable, end-to-end subscribe verification is **unavailable**. A local synthetic stub does **not** prove the Beehiiv integration.

The 2026-09-28 #1090 comment that recommended creating a GA4 `newsletter_click` key event from outbound `click` + `link_domain=kriskrug.beehiiv.com` is **rejected** by this packet. That counts a click. It is not a conversion.

---

## 2. Speaking inquiry inventory

There is no speaking inquiry form. [#277](https://github.com/WalksWithASwagger/kriskrug-wp/issues/277) is still open and keeps email-only contact as the current default. Jetpack / Gravity form markup was absent on every inspected route.

### 2.1 Entry points

| URL / surface | UI entry | Destination | Success mechanism | Existing observable GA4 |
|---|---|---|---|---|
| `/speaking/` | **Start a booking conversation** (twice in the page body) | `/contact/` | Navigation only. Not a submit. | None verified for inquiry success. |
| `/speaking/` | **Contact Kris about your event**; **Ask about this talk** (three talk cards in the live payload / body copy) | `/contact/` | Navigation only. | None. |
| `/speaking/` | Shared header **Contact** and footer **Get in touch** | `/contact/` | Navigation only. | None. |
| `/speaking/` article-adjacent chrome | Header **Newsletter** and footer **Subscribe free** | Beehiiv | Newsletter click, not an inquiry. | Outbound click only (dated). |
| Article footer (sampled 2026-05-07 and 2026-09-29 posts) | Author panel **Book Kris** | `/speaking/` | Organic-landing inquiry *entry*, not a success. | None. |
| Article footer | Site footer **Subscribe free** + header **Newsletter** | Beehiiv | Newsletter click. | Outbound click only (dated). |
| `/contact/` | **Email Kris** and **Send the note** | `mailto:feelmoreplants@gmail.com?subject=Inquiry%20from%20kriskrug.co` | Mail-client handoff. Opening mailto is a click, not a confirmed send. | Dated #1090 probe: mailto added no collect hit. Not re-run. |
| `/contact/` | Visible address | `mailto:feelmoreplants@gmail.com` | Same mailto limit. | Same. |
| EPK `/podcast-guesting-page-epk/` | **Start a media inquiry** | `/contact/` | Navigation only. Adjacent inquiry entry, not a speaking-form success. | None. |
| Services `/generative-ai-services/` | **Start a conversation** | `/contact/` | Navigation only. Adjacent. | None. |

Do not label any of these `newsletter_submit`.

A verified speaking conversion does not exist on the live site today. The first honest success signal would be a same-origin form confirmation after #277, or another provider-owned receipt that this page can see. Until then, `speaking_inquiry_submit` is a named candidate only.

---

## 3. Evidence versus unknowns

| Claim | Status | What would upgrade it |
|---|---|---|
| Entry URLs, labels, hrefs, and the `/subscribe/` iframe src | **Verified** by 2026-09-30 logged-out HTML | Re-GET if chrome changes |
| No same-origin signup or inquiry `<form>` on inspected routes | **Verified** | Re-GET |
| Successful Beehiiv subscribe tracking on kriskrug.co | **Inaccessible** | Beehiiv-admin readback, or a first-party thank-you redirect that this repo can fixture |
| Successful mailto inquiry | **Unverified / not observable** | A form success state (#277) or an authorized mailbox receipt protocol. Public GET cannot see sent mail. |
| Site Kit outbound `click` on Beehiiv links | **Dated provenance** from the 2026-09-28 #1090 comment | Optional later probe; still would not be a conversion |
| Which Beehiiv publication `kriskrug.beehiiv.com` currently is | **Unknown in this session** | Provider-admin. #1090's earlier note pointing at kk-kb#3559 was not re-checked. |
| Whether the `/subscribe/` form already has an external thank-you redirect | **Unknown** | Beehiiv Subscribe forms → Settings. Do not submit the live form to find out. |
| GA4 key-event configuration | **Out of scope** | WalksWithASwagger/kk-kb#3627, KK only |

---

## 4. Event decision table

Neither row is selected. KK chooses under #1090.

| Candidate conversion | Event name | Verified success signal | Deduplication | Remaining KK / provider prerequisite |
|---|---|---|---|---|
| Newsletter signup | `newsletter_submit` | Beehiiv **confirmed subscribe** that this site can see: first-party thank-you URL after Beehiiv's documented external redirect, or a Beehiiv-admin / automation receipt copied into a later authorized staging check. In-iframe success text is **not** usable. Click, outbound, and `newsletter_click` are **not** signals. | One event per distinct `submissionId` (thank-you landing token or Beehiiv subscription id). Repeat callbacks for the same id are no-ops. A later distinct successful subscribe may fire once. | KK picks this candidate. Beehiiv-admin: confirm publication, configure redirect or accept that counting stays in Beehiiv until that exists. Do not mark a GA4 key event until the signal is real. |
| Speaking inquiry | `speaking_inquiry_submit` | Same-origin form **confirmed submit** or thank-you state after server acceptance. mailto open is **not** a signal. `/contact/` and `/speaking/` clicks are **not** signals. | One event per distinct inquiry id. Same rule as above. | KK picks this candidate **and** #277 (or a successor) actually ships a form with a success state. No snippet can invent that state today. |

Recommendation for the later #1090 decision, not a selection: newsletter remains the weekly-plan default **if and only if** KK accepts a provider-side or thank-you-redirect success signal. If KK wants an on-page WordPress event this week without Beehiiv admin work, neither candidate is ready.

---

## 5. Candidate files (clearly not live)

A reliable page-side integration surface does **not** exist for the current Beehiiv iframe or for mailto. The candidate is therefore a success-only helper plus a 316-style handoff, not a Beehiiv listener.

| File | Role |
|---|---|
| `fixes/issue-1090-success-event.js` | Candidate helper. Fires `gtag('event', …)` only for `newsletter_submit` or `speaking_inquiry_submit` when `signal` is `confirmed_submit` or `thank_you_state` and `submissionId` is unique and opaque. Event params are allowlisted to `submission_id` + `signal` only. No click listener. No postMessage. **NOT LIVE.** |
| `fixes/issue-1090-conversion-handoff-2026-09-30.md` | Deploy / snapshot / rollback / KK decisions. Pattern follows `fixes/issue-316-schema-identity-handoff-2026-07-13.md`. |
| `scripts/tests/issue_1090_success_event_harness.cjs` | Synthetic fixture. Intercepts gtag in-process. Zero external submissions. |
| `scripts/tests/test_issue_1090_conversion_preflight.py` | Packet / theme / helper contract. |

The helper is unused until KK picks a conversion **and** a verified success signal exists. Reuse Site Kit's existing gtag; do not add a second analytics loader.

### 5.1 Local proof (executed)

```bash
node scripts/tests/issue_1090_success_event_harness.cjs
```

Contract:

- none on load
- none on click, outbound, mailto, validation failure, or submit error
- one on confirmed success
- no duplicate for a repeated success callback or a second include of the helper
- a later distinct successful submission fires once
- inquiry uses `speaking_inquiry_submit`, never `newsletter_submit`
- extra keys (`email`, `name`, arbitrary form values) are dropped from gtag params
- an email or a name used as `submissionId` is rejected

This proves the helper. It does **not** prove Beehiiv or mailbox integration.

### 5.2 Provider integration protocol (not executed)

Stay in Beehiiv admin or an authorized staging copy. Do not submit the production `/subscribe/` form.

1. Open Subscribers → Subscribe forms for the publication behind `kriskrug.beehiiv.com` and the embed id `552dc13c-76df-4a0b-9663-b7e668042177`.
2. Read Settings: success message versus **Redirect to an external website**. Record the current value privately.
3. If KK wants a first-party signal, set the redirect to a dedicated thank-you URL that is not a useful content page, then fixture that URL locally with the helper and a one-time `submissionId`.
4. Confirm the thank-you page fires exactly one `en=newsletter_submit` collect hit in a host-blocked browser, and that `/subscribe/` load and Beehiiv-link clicks fire none.
5. If KK prefers to keep success inside Beehiiv, stop. Count subscribers in Beehiiv. Do not invent a parent-page event.

### 5.3 Event-param allowlist (Sulu guard)

gtag event params **never** include an email, a name, or any form field value. The helper builds the params object from an allowlist. Any other key on the call — including `email`, `name`, `first_name`, `last_name`, `company`, `message`, `phone`, or a nested `params` bag — is dropped.

Allowed params only:

| Key | Allowed values |
|---|---|
| `submission_id` | Opaque token (`[A-Za-z0-9_-]+`). Thank-you landing token or provider subscription id. Not an email, not a name, not a form field. |
| `signal` | `confirmed_submit` or `thank_you_state` |

A `submissionId` that contains `@` or whitespace (email or name) is rejected and does not fire. The helper never copies the caller object into gtag.

---

## 6. Handoff snapshot

**Proposed deployment owner:** KK, after the conversion choice. Agent may paste the already-reviewed helper only onto an approved first-party thank-you page or form-success path.

**Snapshot / readback / rollback:** see `fixes/issue-1090-conversion-handoff-2026-09-30.md`. Short version: snapshot the current Code Snippet or page HTML privately before any save; activate nothing until the success URL exists; rollback is deactivate / restore the snapshot; purge only the affected cache.

**Privacy:** tests use synthetic ids (`sub-1`, `page-a`, `tok-9`). No personal email, no production subscriber data, no secrets. Event params are allowlisted to `submission_id` and `signal`; email, name, and form field values are dropped.

**KK decisions still required (do not take them here):**

1. Conversion choice: newsletter or speaking inquiry.
2. Production approval for any later snippet or thank-you page.
3. GA4 key-event setup in WalksWithASwagger/kk-kb#3627.

---

## 7. Completion checklist for #1103

- [x] Inventory newsletter and speaking paths by URL, UI entry, provider, ownership, success mechanism, and existing observable GA4 notes
- [x] Include `/speaking/` and article-footer entries
- [x] Separate verified HTML from unknowns; GET cannot prove successful-submit tracking
- [x] Event decision table with `newsletter_submit` vs `speaking_inquiry_submit`
- [x] Cross-origin iframe documented; no postMessage workaround
- [x] Candidate helper tested locally with synthetic data; provider path marked not executed
- [x] Event-param allowlist: only opaque `submission_id` and `signal`; email / name / form values dropped or rejected
- [x] Handoff with files, owner, snapshot/rollback, privacy-safe evidence, and KK decisions
- [x] Keep #1090 open; no key-event or production completion claim
