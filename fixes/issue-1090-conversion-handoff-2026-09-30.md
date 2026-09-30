# Issue #1090: conversion-event handoff

**Track:** A — Content + SEO
**Status:** repo-side human-review handoff; **NOT LIVE**
**Child packet:** [`docs/current-state/reports/issue-1090-conversion-preflight-2026-09-29.md`](../docs/current-state/reports/issue-1090-conversion-preflight-2026-09-29.md)
**Helper:** `fixes/issue-1090-success-event.js`
**Issues:** Refs #1103, Refs #1090. Keep both open. This file does not authorize a WordPress save or a GA4 admin change.

Pattern follows `fixes/issue-316-schema-identity-handoff-2026-07-13.md`: decision, evidence, separate deployment gate, rollback. Production snippets are prod-rendering code.

---

## Decision (for KK, not taken here)

Pick **one** conversion later under #1090:

| Choice | Event name | Allowed only when |
|---|---|---|
| Newsletter signup | `newsletter_submit` | Beehiiv confirmed subscribe that kriskrug.co can see (first-party thank-you redirect) or KK explicitly accepts a Beehiiv-admin-only count |
| Speaking inquiry | `speaking_inquiry_submit` | A same-origin form success state exists. #277 is still email-only. mailto is not enough |

Do not label an inquiry `newsletter_submit`. Do not count a click. Do not implement postMessage against the `/subscribe/` iframe.

Until that choice and a verified success signal exist, leave this helper off the site.

---

## What this handoff deploys later

Nothing today.

If KK later approves a first-party thank-you URL (Beehiiv Settings → Redirect to an external website) or a #277 form success state, the reviewed helper may be loaded on **that success surface only**. Call:

```js
kkRecordVerifiedConversion({
  eventName: "newsletter_submit", // or speaking_inquiry_submit
  signal: "thank_you_state",      // or confirmed_submit
  submissionId: "unique-token",
});
```

Site Kit remains the gtag owner (`G-X7JE8B32L7`, delayed by snippet 22). This helper calls `gtag('event', …)` and adds no second loader.

---

## Separate deployment gate

Do not apply this from the worker lane. A future production session needs explicit KK approval for the exact save.

1. Confirm the conversion choice on #1090 and that a verified success signal exists. Stop if the only available signal is a click or an in-iframe Beehiiv message.
2. Snapshot the current success-page HTML or Code Snippet body privately (mode 0600, outside the repo). Use the existing authenticated snapshot method from the #316 / #706 runbooks. Do not commit credentials, subscriber emails, or mailbox contents.
3. Dry-run the helper on a local fixture with synthetic ids. Required command:

   ```bash
   node scripts/tests/issue_1090_success_event_harness.cjs
   ```

4. If installing as a Code Snippet, paste only the helper plus a one-line call on the success surface. Scope it to that URL. Leave snippet 22 (script diet) and Site Kit settings unchanged.
5. Logged-out readback of the success URL: exactly one collect hit with the chosen `en=` name, none on load of `/`, `/speaking/`, `/contact/`, or `/subscribe/`, none on a Beehiiv or mailto click.
6. **Do not mark a GA4 key event** in this session. That stays with KK in WalksWithASwagger/kk-kb#3627.

---

## Rollback

1. Deactivate the new snippet or restore the prior success-page HTML from the private snapshot.
2. Purge only the affected cache surface.
3. Repeat the logged-out readback: the chosen event is gone; Site Kit delayed gtag is unchanged.
4. Keep Beehiiv and the Gmail contact path as they were. This helper is not their runtime.

---

## Privacy-safe test evidence

The committed harness uses ids `sub-1`, `page-a`, `page-b`, `inquiry-1`, `later`, `once`. It never calls Beehiiv, Gmail, or `google-analytics.com`. Production personal data must not enter the repo, the issue, or the PR.

---

## Remaining KK decisions

1. Conversion choice.
2. Production approval for any later snippet or thank-you page.
3. GA4 key-event setup.

Proposed deployment owner after those decisions: KK, with an agent doing snapshot / readback only.
