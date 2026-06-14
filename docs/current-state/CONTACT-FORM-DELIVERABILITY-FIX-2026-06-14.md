# Contact-form deliverability fix plan — 2026-06-14 (#128 / #174)

Read-only audit run today (`make jetpack-feedback-audit`):
- Feedback totals: **545 inbox, 110 spam, 0 trash** (110 spam is the symptom — real inquiries are likely being silently filtered).
- One form page: **contact (page 2418)**, routing keys present: `to`, `subject`, `customThankyou`, `customThankyouMessage` (values redacted — PII-safe).
- Jetpack forms config: central form management ON, integrations/webhooks/MailPoet enabled, feedback store healthy.

This is a PII-safe plan. No names, emails, or message bodies were read or exported. Every live change below is a **KK gate**.

## Live end-to-end test — 2026-06-14 (agent-run, authorized by KK)
Submitted a marked test through the live `/contact/` form:
- **Capture works:** WP Feedback count moved **545 → 546** (new entry id 12308); thank-you page rendered ("Thanks! Your message has been sent to KK").
- **Notification does NOT arrive:** Gmail search across **inbox and spam** (`in:anywhere`, last 90 min) found **no** notification from kriskrug.co. Gmail was actively receiving other mail throughout, so this is non-delivery, not a search miss.
- **Refined root cause:** this is worse than "lands in spam" — the notification email is **not being delivered to feelmoreplants@gmail.com at all**. Prime suspect is now **hypothesis #2 (the form `to` recipient is a stale/wrong address)** or **#1 (Jetpack mail send failing / blocked at the sender)**. The public thank-you lists `feelmoreplants@gmail.com`, but the actual notification `to:` (redacted) may differ.
- **So 545 captured submissions may represent real inquiries KK never got pinged about** — worth a backfill review of the WP Feedback inbox.

## Root-cause hypotheses (most → least likely)
1. **Notification email lands in spam** — Jetpack sends form notifications from a `wordpress@kriskrug.co` / server address that fails SPF/DKIM alignment for Gmail, so notifications (not just one test) get spam-filed. This matches "test submission landed in spam."
2. **`to` recipient is a stale/unmonitored alias** — notifications arrive but to an address nobody watches.
3. **Submissions captured in WP Feedback but notifications not firing** — 545 stored means capture works; the gap is the *email* leg.

## Fix sequence (KK-gated where noted)
1. **Confirm the recipient** *(KK — now the prime suspect)* — open the contact form block on page 2418 and check the notification `to:` address. The live test proved capture works but no email reaches `feelmoreplants@gmail.com`, so a wrong/stale `to:` is the most likely cause. Set it to a monitored inbox.
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
