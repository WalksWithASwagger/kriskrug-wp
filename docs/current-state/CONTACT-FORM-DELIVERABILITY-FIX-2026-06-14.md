# Contact-form deliverability fix plan — 2026-06-14 (#128 / #174)

Read-only audit run today (`make jetpack-feedback-audit`):
- Feedback totals: **545 inbox, 110 spam, 0 trash** (110 spam is the symptom — real inquiries are likely being silently filtered).
- One form page: **contact (page 2418)**, routing keys present: `to`, `subject`, `customThankyou`, `customThankyouMessage` (values redacted — PII-safe).
- Jetpack forms config: central form management ON, integrations/webhooks/MailPoet enabled, feedback store healthy.

This is a PII-safe plan. No names, emails, or message bodies were read or exported. Every live change below is a **KK gate**.

## Live end-to-end test — 2026-06-14 (agent-run, authorized by KK)

### CORRECTED CONCLUSION: the form works. Earlier "broken" call was wrong.
- **The form delivers real leads.** Notification `to:` on page 2418 is correct (`feelmoreplants@gmail.com`); subject is `[Vancouver photographer Kris Krüg] Contact Kris Krüg`. Gmail shows real submissions arriving from `wordpress@kriskrug.co` and being actioned: Tyler Funk (Jun 9), Tayyaba Mansoor (Jun 8), Steve Cahill (Jun 6), Jimmy/TruNorth (Mar 22) — Alex (alex@bc-ai.ca) has been replying. Delivery is healthy.
- **My single test was inconclusive, not proof of breakage.** The test submission was captured (WP Feedback **545 → 546**, entry id 12308; thank-you rendered) but produced no visible notification in the session window. Most likely cause: I used KK's own address (`feelmoreplants@gmail.com`) as the *submitter* email — a self-addressed message Gmail can suppress/merge — and/or normal send-queue delay. It landed in the feedback **inbox**, not Akismet spam (spam count stayed 110).
- **Retraction:** my earlier note that "545 stored submissions may be unread inquiries KK never got pinged about" was incorrect. Those are stored copies of mails KK *has* been receiving and replying to.

### If KK wants certainty (optional, low priority)
Re-run one test with a NON-KK submitter email (a throwaway), then check Gmail after a few minutes. Only pursue the SPF/DKIM/SMTP hardening below if a clean external test actually fails.

## Root-cause hypotheses (most → least likely)
1. **Notification email lands in spam** — Jetpack sends form notifications from a `wordpress@kriskrug.co` / server address that fails SPF/DKIM alignment for Gmail, so notifications (not just one test) get spam-filed. This matches "test submission landed in spam."
2. **`to` recipient is a stale/unmonitored alias** — notifications arrive but to an address nobody watches.
3. **Submissions captured in WP Feedback but notifications not firing** — 545 stored means capture works; the gap is the *email* leg.

## Fix sequence (KK-gated where noted)
1. **Recipient — CONFIRMED CORRECT** ✓ — `to:` on page 2418 is `feelmoreplants@gmail.com` and real leads arrive there. No change needed. (Steps 2–5 below are only relevant if a clean external re-test fails.)
2. **Allowlist + filter in Gmail** *(KK)* — create a filter for the Jetpack sender (`From: *@kriskrug.co` / the wordpress server address) → "Never send to Spam", apply a label. Rescue the 110 spam items into the inbox.
3. **Fix sender authentication** *(KK / Pagely)* — confirm SPF includes the sending host and DKIM is signing for `kriskrug.co`; consider routing Jetpack mail through an authenticated SMTP (Pagely's relay or a transactional provider) so Gmail trusts it. This is the durable fix for hypothesis #1.
4. **End-to-end delivery test** *(agent runs after KK applies 1–3)* — submit a marked test via the live `/contact/` form, then confirm it (a) stores in WP Feedback and (b) arrives in the monitored inbox **not** spam. Re-run `make jetpack-feedback-audit` to confirm counts move.
5. **Document + close** — record the routing destination (redacted), the auth fix, and the passing test in this file; cross-post proof to #128 / #174 and close.

## What the agent can do without a gate
- Re-run the read-only audit anytime (`make jetpack-feedback-audit`).
- Draft the Gmail filter spec and the SPF/DKIM check steps for KK.
- Run the post-fix delivery test once KK confirms the recipient.

## What needs KK
- Confirming/choosing the monitored recipient address (truly KK's call — I won't guess an inbox).
- Any Gmail-side or DNS/SMTP change (account + Pagely access).
