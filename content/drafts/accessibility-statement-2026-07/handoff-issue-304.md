# Handoff — Accessibility statement packet (#304)

Date: 2026-07-08  
Lane: Track A, draft-only  
Related issues: #304 (this packet), #288 (statement draft), #48 (publish umbrella)

## What this packet is

A human-reviewable accessibility statement package for `kriskrug.co`, grounded in the live Aurora 1.3.36 state and the 2026-07-05 WCAG smoke closeout.

Primary artifact: `content/drafts/accessibility-statement-2026-07/README.md`

## What was verified

- Live theme Version: `1.3.36`
- `/accessibility/` → HTTP 404
- `/contact/` → HTTP 200
- No WordPress write, publish, footer change, or issue closure was performed

## Mapping back to open issues

| Issue | Role after this packet |
|---|---|
| #304 | Agent-safe draft packet complete; keep open until KK reviews or a publisher-mode follow-up is filed |
| #288 | Statement draft exists here (and earlier comment draft); still needs human review before publish |
| #48 | Still the publish umbrella: live `/accessibility/`, footer link, and page a11y verification remain KK/publisher work |

## Human gates before any publisher-mode follow-up

1. Confirm reporting channel: `/contact/`, direct email, or both.
2. Confirm response-time wording, if any.
3. Confirm public standard wording: WCAG 2.2 AA, WCAG 2.1 AA, or simpler WCAG AA.
4. Confirm whether #48 still requires AAA for the page itself, or whether AA plus semantic structure is the publish gate.
5. Recheck whether old draft page `11886` still exists and should be reused.

## Suggested next step after KK review

1. Authenticated slug/ID check for `/accessibility/`.
2. Body-only WordPress **draft** create/update with dry-run first.
3. Preview QA on desktop/mobile + keyboard.
4. Publish only with explicit KK approval.
5. Add footer link only after the page returns 200.

Do not present this draft as legally approved.
