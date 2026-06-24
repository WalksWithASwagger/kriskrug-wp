# Issue #174 — Gmail filter spec for contact-form notifications

**Context:** The kriskrug.co contact form works; leads arrive at `feelmoreplants@gmail.com`. Per the 2026-06-14 audit, ~104 Jetpack notification copies may be sitting in Gmail **spam** (SPF/DKIM alignment), so this filter (a) keeps future notifications out of spam and (b) labels them for fast triage. PII stays in Gmail — never in repo.

## Filter to create (Gmail → Settings → Filters → Create a new filter)

**Match (From):** the address WordPress/Jetpack sends notifications *from*. On most Jetpack/Pagely installs this is one of:
- `wordpress@kriskrug.co`
- `donotreply@wordpress.com` (Jetpack Forms default sender)

Use this in the filter's **From** field (covers both):
```
from:(wordpress@kriskrug.co OR donotreply@wordpress.com OR *@kriskrug.co)
```
*(Confirm the exact sender by opening one real notification in the inbox and copying its From address; narrow the filter to that once known.)*

**Optional Subject narrowing** (Jetpack form subject usually contains the page/form name):
```
subject:("contact" OR "form" OR your form's subject line)
```

## Actions to apply
- [ ] **Never send it to Spam**
- [ ] **Apply label:** `kriskrug.co/contact` (create the nested label)
- [ ] **Always mark as important** (optional)
- [ ] **Also apply filter to matching conversations** — tick this so the ~104 spam copies get rescued + labeled in one pass

## Spam rescue (one-time)
1. In Gmail search: `in:spam from:(wordpress@kriskrug.co OR donotreply@wordpress.com)`
2. Select all → **Not spam** (moves them to inbox; the new filter then labels them).

## Verification (closes #174)
After the filter is live, an agent runs **one sterile external test submission** (from a non-KK address) through the live contact form, then you (or the agent with Gmail access) confirm:
- [ ] Test notification landed in **Inbox**, not Spam
- [ ] It carries the `kriskrug.co/contact` label
- [ ] Record the redacted routing path (recipient *category*/alias only) in `CONTACT-FORM-DELIVERABILITY-FIX-2026-06-14.md`

## Out of scope / guardrails
- No message bodies copied into repo, issues, or commits (PII).
- No bulk newsletter adds from these submitters — CASL requires opt-in.
- Heavy SPF/DKIM/SMTP hardening only if the sterile external test actually lands in spam *after* the filter.
