# [FORMS] Implement simple contact form on `/contact/` (from #277)

**STATUS:** Contingent stub — file **only if** KK picks Option B on [#277](https://github.com/WalksWithASwagger/kriskrug-wp/issues/277) after the evidence checklist in `docs/current-state/reports/contact-cta-decision-277-20260726.md`. Do not mass-file; do not deploy without KK approval + rollback path.

**Suggested labels:** `platform`, `content`, `needs-human-review`, `priority:medium`  
**Parent decision:** #277 · epic context: #222

## Goal

Replace (or supplement) the lightweight mailto CTA on `/contact/` with a **simple, spam-resistant contact form** that delivers to a monitored inbox — without recreating the Jetpack Forms notification backlog (#128 / #174).

## Why this exists

Public probe (2026-07-26): `/contact/` has **zero** forms; primary actions are mailto to the public inquiry address with subject `Inquiry from kriskrug.co`. Newsletter stays on Beehiiv. Option A (keep email) is the default unless KK documents real friction.

## Non-goals

- Do not re-enable Jetpack core solely for Forms.
- Do not couple inquiry submit → newsletter subscribe without explicit CASL consent.
- Do not put submitter PII in GitHub issues, commits, or CI logs.
- Do not ship CRM automation until Option C is separately approved.

## Proposed approach (pick one in implementation)

1. **Native / lightweight plugin** (e.g. small WP form plugin already acceptable on Pagely) with honeypot + Akismet (Akismet is already in the historical plugin set).
2. **Hosted embed** (Beehiiv/Typeform/etc.) only if inquiry and list growth are intentionally split and consent copy is clear.
3. **CRM form (Zero BS CRM)** only if KK confirms daily CRM triage — prefer a dedicated CRM issue if that is the real path.

Document the chosen stack in the issue before any live install.

## Requirements

### Product

- [ ] Preserve page intent: ask for who / when / where / usefulness (mirror current “what to include” cards).
- [ ] Keep a visible mailto fallback for mail-client users.
- [ ] Thank-you state that does not imply automated SLA.

### Security / spam

- [ ] Honeypot and/or CAPTCHA; Akismet or equivalent where available.
- [ ] Rate limiting or plugin-equivalent abuse controls.
- [ ] No open redirect; no storing full message bodies in public logs.

### Deliverability / ops

- [ ] Notification `to:` is a **monitored** address KK actually reads (confirm in wp-admin; do not commit the address if it differs from the public mailto).
- [ ] Subject prefix stable for Gmail filters (e.g. `[kriskrug.co contact]`).
- [ ] End-to-end test: marked test submission arrives **and** is not spam; document privately.
- [ ] Rollback: deactivate form / revert `/contact/` body to mailto-only CTA with cache purge plan.

### Privacy

- [ ] Privacy policy link near submit.
- [ ] Retention owner for form entries if stored in WP.
- [ ] No bulk export into newsletter without opt-in.

## Acceptance criteria

- [ ] KK approved stack + rollback owner.
- [ ] Dry-run / staging or inactive snippet proof before production activate (per incident safety rules).
- [ ] Live `/contact/` submits successfully; notification path verified once.
- [ ] Public HTML no longer relies on mailto as the **only** inquiry path (mailto may remain as fallback).
- [ ] #277 closed as “decided → implement here” with link to this filed issue.

## Rollback

Revert Contact page (id `2418`) to the email-CTA architecture payload (or last known good revision), deactivate/remove the form plugin or block, purge Pagely/Boost cache, confirm mailto CTAs restore on public readback.

## References

- Decision memo: `docs/current-state/reports/contact-cta-decision-277-20260726.md`
- Historical: `docs/current-state/CONTACT-FORM-DELIVERABILITY-FIX-2026-06-14.md`, #128, #174
- Architecture note: Contact email path preserved in `docs/current-state/archive/CONTENT-ARCHITECTURE-RESET-2026-07-01.md`
